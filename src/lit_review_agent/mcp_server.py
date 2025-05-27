import asyncio
from typing import List, Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tool_provider import ToolArgument, ToolInfo

# Assuming your LiteratureAgent and Config are structured to be imported like this
from .agent import LiteratureAgent
from .utils.config import Config
from .retrieval.base_retriever import LiteratureItem # For type hinting if needed

# Initialize the MCP server
# The name "LiteratureReviewAgentServer" will be used by MCP clients to identify this server.
mcp_server = FastMCP(name="LiteratureReviewAgentServer", description="An MCP server for the Literature Review Agent.")

# Global instance of the agent and config (can be managed differently, e.g., with lifespan events)
# It's generally better to initialize potentially heavy objects within a lifespan manager
# for more complex MCP server setups, but this is a simpler start.
agent_config: Optional[Config] = None
literature_agent: Optional[LiteratureAgent] = None

# --- MCP Lifespan Management (Optional but Recommended for Production) ---
# MCP servers can have lifespan events to manage resources like database connections
# or initializing heavy objects like your LiteratureAgent.

@mcp_server.lifespan()
async def app_lifespan_manager(server: FastMCP):
    """Manages the lifecycle of the LiteratureAgent instance."""
    global agent_config, literature_agent
    print("MCP Server: Initializing LiteratureAgent...")
    try:
        agent_config = Config()  # Load default config or from a file/env
        literature_agent = LiteratureAgent(config=agent_config)
        print("MCP Server: LiteratureAgent initialized successfully.")
        yield  # The server runs while this yield is active
    except Exception as e:
        print(f"MCP Server: Error during LiteratureAgent initialization: {e}")
        # Potentially re-raise or handle as critical failure
        raise
    finally:
        print("MCP Server: Shutting down. (Cleanup if necessary)")
        # Add any cleanup logic here if needed when the server stops

# --- Define MCP Tools ---

# We need to map the LiteratureAgent's methods to MCP tools.
# Let's start with `conduct_literature_review`.

# Helper to generate ToolArgument from function signatures or Pydantic models if available
# For now, defining them manually based on the agent.py
conduct_review_args = [
    ToolArgument(name="research_topic", description="The topic to search for.", type="string", is_required=True),
    ToolArgument(name="max_papers", description="Maximum number of papers to retrieve and process.", type="integer", is_required=False, default_value=20),
    ToolArgument(name="sources", description="A comma-separated list of sources (e.g., 'arxiv,semantic_scholar').", type="string", is_required=False),
    ToolArgument(name="retrieve_full_text", description="Whether to attempt to download and process full PDF texts.", type="boolean", is_required=False, default_value=False),
    ToolArgument(name="year_start", description="Optional start year for filtering publications.", type="integer", is_required=False),
    ToolArgument(name="year_end", description="Optional end year for filtering publications.", type="integer", is_required=False),
]

@mcp_server.tool(
    name="conduct_literature_review",
    description="Conducts a comprehensive literature review for a given research topic.",
    arguments=conduct_review_args
)
async def conduct_literature_review_tool(
    research_topic: str,
    max_papers: int = 20,
    sources: Optional[str] = None, # MCP will pass string, we parse to list
    retrieve_full_text: bool = False,
    year_start: Optional[int] = None,
    year_end: Optional[int] = None
) -> Dict[str, Any]: # Return type should be JSON serializable
    """MCP Tool wrapper for LiteratureAgent.conduct_literature_review"""
    if not literature_agent:
        raise Exception("LiteratureAgent not initialized. Check server logs.")

    print(f"MCP Tool: conduct_literature_review called with topic '{research_topic}'")
    
    source_list: Optional[List[str]] = None
    if sources:
        source_list = [s.strip().lower() for s in sources.split(',') if s.strip()]

    try:
        # Assuming conduct_literature_review returns a dictionary that is JSON serializable
        # LiteratureItem objects within results might need conversion if they are not inherently serializable
        results = await literature_agent.conduct_literature_review(
            research_topic=research_topic,
            max_papers=max_papers,
            sources=source_list,
            retrieve_full_text=retrieve_full_text,
            year_start=year_start,
            year_end=year_end
        )
        # Ensure results are JSON serializable.
        # LiteratureItem is a Pydantic model, so use .model_dump()
        if 'retrieved_items' in results and results['retrieved_items']:
            results['retrieved_items'] = [
                item.model_dump(mode='json') if isinstance(item, LiteratureItem) else item 
                for item in results['retrieved_items']
            ]
        if 'processed_papers' in results and results['processed_papers']: # Assuming processed_papers also contains LiteratureItem
            results['processed_papers'] = [
                item.model_dump(mode='json') if isinstance(item, LiteratureItem) else item 
                for item in results['processed_papers']
            ]
        
        print(f"MCP Tool: Review conducted. Retrieved {len(results.get('retrieved_items',[]))} items.")
        return results 
    except Exception as e:
        print(f"MCP Tool: Error during conduct_literature_review: {e}")
        # Return a structured error or raise an MCP-specific error
        return {"error": str(e), "details": "Failed to conduct literature review."}

# --- Define MCP Resources (Placeholder) ---
# Example: Exposing individual papers as resources (requires more design)
# @mcp_server.resource("papers://{paper_id}")
# async def get_paper_resource(paper_id: str) -> Dict[str, Any]:
#     if not literature_agent:
#         raise Exception("LiteratureAgent not initialized.")
#     # This would require a method in LiteratureAgent to fetch a specific paper by ID
#     # paper_data = await literature_agent.get_paper_details(paper_id)
#     # if paper_data:
#     #     return paper_data # Ensure it's JSON serializable
#     # else:
#     #     raise Exception(f"Paper with ID {paper_id} not found.") # MCP will handle as error
#     return {"paper_id": paper_id, "status": "Not implemented yet"}


# --- Main entry point for running the MCP server directly ---
# This allows running `python -m src.lit_review_agent.mcp_server`
# Or using `mcp dev src/lit_review_agent/mcp_server.py`

if __name__ == "__main__":
    print("Starting MCP server for Literature Review Agent...")
    # The mcp_server.run() method will block and serve requests.
    # It uses stdio transport by default if run directly like this,
    # which is suitable for Claude Desktop integration or local testing.
    # For network-based access, you'd configure a different transport (e.g., HTTP).
    asyncio.run(mcp_server.run_async()) # Use run_async for the FastMCP server with lifespan 