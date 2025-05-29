"""
MCP Server for Literature Review Agent
提供MCP协议支持的文献综述服务器
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp.tool_provider import ToolArgument
    MCP_AVAILABLE = True
except ImportError:
    print("Warning: MCP dependencies not available. MCP server will not work.")
    print("Install with: pip install mcp")
    MCP_AVAILABLE = False
    FastMCP = None
    ToolArgument = None

# Import our agent components
from .agent import LiteratureAgent
from .utils.config import Config

# Global instances
agent_config: Optional[Config] = None
literature_agent: Optional[LiteratureAgent] = None

def create_mcp_server():
    """创建MCP服务器实例"""
    if not MCP_AVAILABLE:
        print("❌ MCP not available. Please install MCP dependencies.")
        return None
    
    server = FastMCP(
        name="LiteratureReviewAgent",
        description="AI-powered literature review and analysis server"
    )
    
    @server.lifespan()
    async def lifespan_manager():
        """管理服务器生命周期"""
        global agent_config, literature_agent
        print("🚀 Initializing Literature Review Agent...")
        
        try:
            agent_config = Config()
            literature_agent = LiteratureAgent(config=agent_config)
            print("✅ Literature Review Agent initialized successfully")
            yield
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            raise
        finally:
            print("🔄 Shutting down Literature Review Agent...")
    
    @server.tool(
        name="conduct_literature_review",
        description="Conduct a comprehensive literature review on a research topic",
        arguments=[
            ToolArgument(
                name="research_topic",
                description="The research topic to review",
                type="string",
                is_required=True
            ),
            ToolArgument(
                name="max_papers",
                description="Maximum number of papers to retrieve (1-100)",
                type="integer",
                is_required=False,
                default_value=20
            ),
            ToolArgument(
                name="sources",
                description="Comma-separated list of sources (arxiv,semantic_scholar)",
                type="string",
                is_required=False
            ),
            ToolArgument(
                name="retrieve_full_text",
                description="Whether to download full PDF texts",
                type="boolean",
                is_required=False,
                default_value=False
            )
        ]
    )
    async def conduct_review(
        research_topic: str,
        max_papers: int = 20,
        sources: Optional[str] = None,
        retrieve_full_text: bool = False
    ) -> Dict[str, Any]:
        """执行文献综述"""
        if not literature_agent:
            return {"error": "Literature agent not initialized"}
        
        # 验证参数
        if max_papers < 1 or max_papers > 100:
            return {"error": "max_papers must be between 1 and 100"}
        
        # 处理数据源
        source_list = None
        if sources:
            source_list = [s.strip() for s in sources.split(',')]
        
        try:
            print(f"🔍 Starting literature review for: {research_topic}")
            results = await literature_agent.conduct_literature_review(
                research_topic=research_topic,
                max_papers=max_papers,
                sources=source_list,
                retrieve_full_text=retrieve_full_text
            )
            
            # 确保结果可序列化
            if 'papers' in results:
                results['papers'] = [
                    paper.model_dump() if hasattr(paper, 'model_dump') else paper
                    for paper in results['papers']
                ]
            
            print(f"✅ Review completed. Found {len(results.get('papers', []))} papers")
            return results
            
        except Exception as e:
            print(f"❌ Error during literature review: {e}")
            return {"error": str(e)}
    
    @server.tool(
        name="search_similar_papers",
        description="Search for papers similar to a query using semantic search",
        arguments=[
            ToolArgument(
                name="query",
                description="Search query",
                type="string",
                is_required=True
            ),
            ToolArgument(
                name="n_results",
                description="Number of results to return (1-50)",
                type="integer",
                is_required=False,
                default_value=10
            )
        ]
    )
    async def search_similar(query: str, n_results: int = 10) -> Dict[str, Any]:
        """搜索相似论文"""
        if not literature_agent:
            return {"error": "Literature agent not initialized"}
        
        if n_results < 1 or n_results > 50:
            return {"error": "n_results must be between 1 and 50"}
        
        try:
            results = await literature_agent.search_similar_papers(query, n_results)
            return {
                "query": query,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {"error": str(e)}
    
    @server.resource("papers://{paper_id}")
    async def get_paper(paper_id: str) -> Dict[str, Any]:
        """获取特定论文信息"""
        if not literature_agent:
            raise Exception("Literature agent not initialized")
        
        # 这里应该实现从数据库获取论文的逻辑
        return {
            "paper_id": paper_id,
            "message": "Paper retrieval feature coming soon",
            "timestamp": datetime.now().isoformat()
        }
    
    @server.resource("collections://literature")
    async def get_collection_stats() -> Dict[str, Any]:
        """获取文献集合统计信息"""
        if not literature_agent:
            raise Exception("Literature agent not initialized")
        
        try:
            stats = literature_agent.get_statistics()
            return {
                "collection": "literature",
                "statistics": stats,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to get statistics: {e}")
    
    return server

# 创建服务器实例
mcp_server = create_mcp_server() if MCP_AVAILABLE else None

async def run_mcp_server():
    """运行MCP服务器"""
    if not mcp_server:
        print("❌ Cannot start MCP server - not available")
        return
    
    print("🚀 Starting MCP Literature Review Server...")
    await mcp_server.run_async()

if __name__ == "__main__":
    if MCP_AVAILABLE:
        asyncio.run(run_mcp_server())
    else:
        print("❌ MCP dependencies not available. Please install with: pip install mcp")
