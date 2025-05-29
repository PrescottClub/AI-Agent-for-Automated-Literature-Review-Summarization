import asyncio
from typing import List, Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tool_provider import ToolArgument, ToolInfo

# Assuming your LiteratureAgent and Config are structured to be imported like this
from .agent import LiteratureAgent
from .utils.config import Config
from .retrieval.base_retriever import LiteratureItem # For type hinting if needed

# Initialize the MCP server
mcp_server = FastMCP(
    name="LiteratureReviewAgentServer", 
    description="An advanced MCP server for AI-powered literature review and analysis."
)

# Global instance of the agent and config
agent_config: Optional[Config] = None
literature_agent: Optional[LiteratureAgent] = None

@mcp_server.lifespan()
async def app_lifespan_manager(server: FastMCP):
    """Manages the lifecycle of the LiteratureAgent instance."""
    global agent_config, literature_agent
    print("MCP Server: Initializing LiteratureAgent...")
    try:
        agent_config = Config()
        literature_agent = LiteratureAgent(config=agent_config)
        print("MCP Server: LiteratureAgent initialized successfully.")
        yield
    except Exception as e:
        print(f"MCP Server: Error during LiteratureAgent initialization: {e}")
        raise
    finally:
        print("MCP Server: Shutting down. (Cleanup if necessary)")

# Enhanced tool definitions with better validation
conduct_review_args = [
    ToolArgument(name="research_topic", description="The research topic to search for.", type="string", is_required=True),
    ToolArgument(name="max_papers", description="Maximum number of papers to retrieve (1-100).", type="integer", is_required=False, default_value=20),
    ToolArgument(name="sources", description="Comma-separated list of sources (arxiv,semantic_scholar).", type="string", is_required=False),
    ToolArgument(name="retrieve_full_text", description="Whether to download and process full PDF texts.", type="boolean", is_required=False, default_value=False),
    ToolArgument(name="year_start", description="Start year for filtering publications (e.g., 2020).", type="integer", is_required=False),
    ToolArgument(name="year_end", description="End year for filtering publications (e.g., 2024).", type="integer", is_required=False),
]

@mcp_server.tool(
    name="conduct_literature_review",
    description="Conducts a comprehensive literature review for a given research topic with AI-powered analysis.",
    arguments=conduct_review_args
)
async def conduct_literature_review_tool(
    research_topic: str,
    max_papers: int = 20,
    sources: Optional[str] = None,
    retrieve_full_text: bool = False,
    year_start: Optional[int] = None,
    year_end: Optional[int] = None
) -> Dict[str, Any]:
    """Enhanced MCP Tool wrapper for LiteratureAgent.conduct_literature_review"""
    if not literature_agent:
        raise Exception("LiteratureAgent not initialized. Check server logs.")

    # Input validation
    if max_papers < 1 or max_papers > 100:
        raise ValueError("max_papers must be between 1 and 100")
    
    if year_start and year_end and year_start > year_end:
        raise ValueError("year_start cannot be greater than year_end")

    print(f"MCP Tool: conduct_literature_review called with topic '{research_topic}'")
    
    source_list: Optional[List[str]] = None
    if sources:
        valid_sources = {"arxiv", "semantic_scholar"}
        source_list = [s.strip().lower() for s in sources.split(',') if s.strip()]
        invalid_sources = set(source_list) - valid_sources
        if invalid_sources:
            raise ValueError(f"Invalid sources: {invalid_sources}. Valid sources: {valid_sources}")

    try:
        results = await literature_agent.conduct_literature_review(
            research_topic=research_topic,
            max_papers=max_papers,
            sources=source_list,
            retrieve_full_text=retrieve_full_text,
            year_start=year_start,
            year_end=year_end
        )
        
        # Ensure results are JSON serializable
        if 'retrieved_items' in results and results['retrieved_items']:
            results['retrieved_items'] = [
                item.model_dump(mode='json') if isinstance(item, LiteratureItem) else item 
                for item in results['retrieved_items']
            ]
        if 'processed_papers' in results and results['processed_papers']:
            results['processed_papers'] = [
                item.model_dump(mode='json') if isinstance(item, LiteratureItem) else item 
                for item in results['processed_papers']
            ]
        
        print(f"MCP Tool: Review conducted. Retrieved {len(results.get('retrieved_items',[]))} items.")
        return results 
    except Exception as e:
        print(f"MCP Tool: Error during conduct_literature_review: {e}")
        return {"error": str(e), "details": "Failed to conduct literature review."}

# New tool: Analyze single paper
analyze_paper_args = [
    ToolArgument(name="paper_url", description="URL or identifier of the paper to analyze.", type="string", is_required=True),
    ToolArgument(name="analysis_type", description="Type of analysis: summary, keywords, methodology, findings.", type="string", is_required=False, default_value="summary"),
]

@mcp_server.tool(
    name="analyze_paper",
    description="Analyzes a single research paper and provides detailed insights.",
    arguments=analyze_paper_args
)
async def analyze_paper_tool(
    paper_url: str,
    analysis_type: str = "summary"
) -> Dict[str, Any]:
    """Analyzes a single research paper"""
    if not literature_agent:
        raise Exception("LiteratureAgent not initialized.")
    
    valid_types = {"summary", "keywords", "methodology", "findings"}
    if analysis_type not in valid_types:
        raise ValueError(f"Invalid analysis_type. Valid types: {valid_types}")
    
    try:
        # This would require implementing a single paper analysis method in LiteratureAgent
        # For now, return a placeholder
        return {
            "paper_url": paper_url,
            "analysis_type": analysis_type,
            "status": "Analysis feature coming soon",
            "message": "Single paper analysis will be implemented in the next version"
        }
    except Exception as e:
        return {"error": str(e), "details": "Failed to analyze paper."}

# New tool: Search similar papers
search_similar_args = [
    ToolArgument(name="query", description="Search query for finding similar papers.", type="string", is_required=True),
    ToolArgument(name="n_results", description="Number of similar papers to return (1-50).", type="integer", is_required=False, default_value=10),
]

@mcp_server.tool(
    name="search_similar_papers",
    description="Searches for papers similar to a given query using semantic search.",
    arguments=search_similar_args
)
async def search_similar_papers_tool(
    query: str,
    n_results: int = 10
) -> Dict[str, Any]:
    """Searches for similar papers using vector similarity"""
    if not literature_agent:
        raise Exception("LiteratureAgent not initialized.")
    
    if n_results < 1 or n_results > 50:
        raise ValueError("n_results must be between 1 and 50")
    
    try:
        results = await literature_agent.search_similar_papers(query, n_results)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {"error": str(e), "details": "Failed to search similar papers."}

# MCP Resources: Expose paper data as resources
@mcp_server.resource("papers://{paper_id}")
async def get_paper_resource(paper_id: str) -> Dict[str, Any]:
    """Exposes individual papers as MCP resources"""
    if not literature_agent:
        raise Exception("LiteratureAgent not initialized.")
    
    try:
        # This would require implementing a method to get paper by ID
        # For now, return a placeholder
        return {
            "paper_id": paper_id,
            "status": "Resource access coming soon",
            "message": "Paper resource access will be implemented in the next version"
        }
    except Exception as e:
        raise Exception(f"Failed to retrieve paper {paper_id}: {e}")

@mcp_server.resource("collections://literature")
async def get_literature_collection() -> Dict[str, Any]:
    """Exposes the literature collection statistics as a resource"""
    if not literature_agent:
        raise Exception("LiteratureAgent not initialized.")
    
    try:
        stats = literature_agent.get_statistics()
        return {
            "collection_name": "literature",
            "statistics": stats,
            "timestamp": "2024-01-01T00:00:00Z"  # Would use actual timestamp
        }
    except Exception as e:
        raise Exception(f"Failed to retrieve collection statistics: {e}")

if __name__ == "__main__":
    print("Starting enhanced MCP server for Literature Review Agent...")
    asyncio.run(mcp_server.run_async()) 