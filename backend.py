"""
FastAPI 服务器 - 为 Vue3 前端提供 API 接口
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    from lit_review_agent.agent import LiteratureAgent
    from lit_review_agent.utils.config import Config
except ImportError as e:
    print(f"Warning: Could not import LiteratureAgent: {e}")
    LiteratureAgent = None
    Config = None

# 创建 FastAPI 应用
app = FastAPI(
    title="AI Literature Review API",
    description="智能文献综述系统 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue3 开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class SearchRequest(BaseModel):
    query: str
    sources: List[str] = ["arxiv", "semantic_scholar"]
    maxPapers: int = 20
    yearStart: Optional[int] = None
    yearEnd: Optional[int] = None
    retrieveFullText: bool = False
    enableAIAnalysis: bool = True

class ReportRequest(BaseModel):
    papers: List[Dict]
    title: str

# 响应模型
class Paper(BaseModel):
    title: str
    authors: List[str]
    publishedDate: str
    source: str
    summary: str
    keywords: Optional[List[str]] = []
    url: Optional[str] = None
    pdfUrl: Optional[str] = None
    fullTextRetrieved: Optional[bool] = False

class SearchResult(BaseModel):
    papers: List[Paper]
    totalCount: int
    processingTime: float
    summary: Optional[str] = None

# 全局变量
literature_agent = None

def get_agent():
    """获取文献代理实例"""
    global literature_agent
    if literature_agent is None and LiteratureAgent and Config:
        try:
            config = Config()
            literature_agent = LiteratureAgent(config)
        except Exception as e:
            print(f"Failed to initialize LiteratureAgent: {e}")
            literature_agent = None
    return literature_agent

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    print("🚀 启动 AI Literature Review API 服务器...")
    agent = get_agent()
    if agent:
        print("✅ 文献代理初始化成功")
    else:
        print("❌ 文献代理初始化失败，将使用模拟数据")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Literature Review API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    agent = get_agent()
    return {
        "status": "healthy" if agent else "demo",
        "timestamp": datetime.now().isoformat(),
        "agent_initialized": agent is not None
    }

@app.post("/api/search", response_model=SearchResult)
async def search_literature(request: SearchRequest):
    """文献检索"""
    start_time = time.time()
    
    try:
        agent = get_agent()
        
        print(f"🔍 开始检索: {request.query}")
        
        if agent:
            # 使用真实的代理
            search_params = {
                "query": request.query,
                "max_papers": request.maxPapers,
                "sources": request.sources,
                "full_text": request.retrieveFullText,
            }
            
            if request.yearStart:
                search_params["year_start"] = request.yearStart
            if request.yearEnd:
                search_params["year_end"] = request.yearEnd
            
            results = await asyncio.to_thread(agent.conduct_review, **search_params)
            
            # 转换结果格式
            papers = []
            if results and "processed_papers" in results:
                for paper_data in results["processed_papers"]:
                    paper = Paper(
                        title=paper_data.get("title", "未知标题"),
                        authors=paper_data.get("authors", []),
                        publishedDate=paper_data.get("published_date", ""),
                        source=paper_data.get("source", "unknown"),
                        summary=paper_data.get("ai_enhanced_summary", paper_data.get("original_summary", "")),
                        keywords=paper_data.get("keywords", []),
                        url=paper_data.get("url", ""),
                        pdfUrl=paper_data.get("pdf_url", ""),
                        fullTextRetrieved=paper_data.get("full_text_retrieved", False)
                    )
                    papers.append(paper)
        else:
            # 使用模拟数据
            await asyncio.sleep(1)  # 模拟处理时间
            papers = [
                Paper(
                    title=f"人工智能在{request.query}领域的应用研究",
                    authors=["张三", "李四", "王五"],
                    publishedDate="2024-01-15",
                    source="arxiv",
                    summary=f"本文深入研究了人工智能技术在{request.query}领域的最新应用，包括机器学习、深度学习和自然语言处理等前沿技术的实际应用案例。",
                    keywords=["人工智能", "机器学习", "深度学习", request.query],
                    url="https://arxiv.org/abs/2401.12345",
                    fullTextRetrieved=True
                ),
                Paper(
                    title=f"{request.query}中的机器学习方法综述",
                    authors=["赵六", "钱七"],
                    publishedDate="2023-12-20",
                    source="semantic_scholar",
                    summary=f"本综述分析了{request.query}领域中机器学习方法的发展现状、主要挑战和未来趋势，为相关研究提供了重要参考。",
                    keywords=["机器学习", "数据分析", "算法优化"],
                    url="https://example.com/paper2",
                    fullTextRetrieved=False
                ),
                Paper(
                    title=f"基于深度学习的{request.query}智能系统设计",
                    authors=["孙八", "周九", "吴十"],
                    publishedDate="2024-02-10",
                    source="arxiv",
                    summary=f"提出了一种基于深度学习的{request.query}智能系统架构，通过实验验证了该系统在实际应用中的有效性和可靠性。",
                    keywords=["深度学习", "智能系统", "系统架构"],
                    url="https://arxiv.org/abs/2402.67890",
                    fullTextRetrieved=True
                )
            ]
        
        processing_time = time.time() - start_time
        
        print(f"✅ 检索完成: 找到 {len(papers)} 篇论文，耗时 {processing_time:.2f}s")
        
        return SearchResult(
            papers=papers,
            totalCount=len(papers),
            processingTime=processing_time,
            summary=f"基于'{request.query}'的文献检索完成，共找到{len(papers)}篇相关论文。"
        )
        
    except Exception as e:
        print(f"❌ 检索失败: {e}")
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")

@app.post("/api/generate-report")
async def generate_report(request: ReportRequest):
    """生成综述报告"""
    try:
        print(f"📝 开始生成报告: {request.title}")
        
        # 模拟报告生成
        await asyncio.sleep(2)
        
        report = f"""# {request.title}

## 摘要

本报告基于 {len(request.papers)} 篇相关文献，对研究主题进行了全面的综述分析。通过系统性的文献调研和深入分析，本报告总结了该领域的研究现状、主要成果和发展趋势。

## 研究背景

随着科技的快速发展，该研究领域正在经历前所未有的变革。本综述旨在为研究人员和从业者提供该领域的全面视角。

## 主要发现

### 1. 研究现状
- 共检索到 {len(request.papers)} 篇高质量相关文献
- 研究涵盖了多个重要的技术方向和应用场景
- 近年来该领域的研究热度持续上升

### 2. 技术趋势
- 人工智能和机器学习技术的广泛应用
- 跨学科融合成为重要发展方向
- 实际应用场景不断扩展

### 3. 主要挑战
- 技术标准化程度有待提高
- 数据质量和隐私保护需要平衡
- 产业化应用仍面临诸多挑战

## 未来展望

基于当前的研究趋势和技术发展，我们预测该领域在未来几年将继续快速发展，特别是在以下几个方面：

1. **技术创新**: 新算法和新方法的不断涌现
2. **应用拓展**: 更多实际应用场景的探索
3. **标准化**: 行业标准和规范的逐步建立

## 结论

通过对现有文献的深入分析，我们发现该领域正处于快速发展阶段，具有广阔的研究前景和应用潜力。建议研究人员关注技术创新与实际应用的结合，推动该领域的持续健康发展。

## 参考文献

本报告基于 {len(request.papers)} 篇高质量学术论文，涵盖了该领域的主要研究成果和最新进展。

---
*报告生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*
*生成工具: AI Literature Review System*
        """
        
        print("✅ 报告生成完成")
        
        return {"report": report}
        
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动 FastAPI 服务器...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 