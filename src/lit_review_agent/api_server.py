#!/usr/bin/env python3
"""
FastAPI 服务器 - 为 Vue3 前端提供 API 接口
"""

import asyncio
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta

# 添加src目录到Python路径
current_dir = Path(__file__).parent.parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from src.lit_review_agent.agent import LiteratureAgent
    from src.lit_review_agent.utils.config import Config
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    LiteratureAgent = None
    Config = None

# 导入认证中间件
try:
    from src.lit_review_agent.middleware.auth import (
        authenticate_user,
        create_access_token,
        users_db,
        ACCESS_TOKEN_EXPIRE_MINUTES,
        Token,
        User as AuthUser,
        get_current_active_user
    )
    print("Auth middleware imported successfully")
except ImportError as e:
    print(f"Warning: Could not import auth middleware: {e}")
    authenticate_user = None
    create_access_token = None
    users_db = None
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    Token = None
    AuthUser = None
    get_current_active_user = None

# 暂时禁用限流器
limiter = None

# 临时用户模型定义


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str

# 临时依赖函数


async def get_current_active_user():
    """临时用户依赖函数"""
    return User(username="demo_user", email="demo@example.com")

# 临时装饰器定义，直到实现真正的速率限制


def rate_limit_auth(func):
    """临时认证速率限制装饰器"""
    return func


def rate_limit_search(func):
    """临时搜索速率限制装饰器"""
    return func


def rate_limit_api(func):
    """临时API速率限制装饰器"""
    return func


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print(">> 启动 AI Literature Review API 服务器...")
    try:
        agent = get_agent()
        if agent:
            print(">> 文献代理初始化成功")
        else:
            print(">> 文献代理初始化失败，将使用模拟数据")
    except Exception as e:
        print(f">> 代理初始化异常: {e}")
        print(">> 将使用模拟数据模式运行")

    yield

    # 关闭时清理
    print(">> 关闭 AI Literature Review API 服务器...")
    global literature_agent
    if literature_agent:
        try:
            # 清理资源
            literature_agent = None
            print(">> 资源清理完成")
        except Exception as e:
            print(f">> 资源清理异常: {e}")


# 创建 FastAPI 应用
app = FastAPI(
    title="AI Literature Review API",
    description="智能文献综述系统 API",
    version="3.1.0",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "file://",
        "*"  # 开发环境允许所有源
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加安全中间件
if limiter:
    app.state.limiter = limiter

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


# 请求模型
class SearchRequest(BaseModel):
    query: Optional[str] = None  # Legacy structured query field
    rawQuery: Optional[str] = None  # New natural language query field
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
    actionPlan: Optional[List[str]] = None


# 全局变量
literature_agent = None


def get_agent():
    """获取文献代理实例"""
    global literature_agent
    if literature_agent is None:
        try:
            print(">> 正在初始化文献代理...")
            # 使用简化的配置来避免配置解析问题
            from src.lit_review_agent.retrieval.arxiv_client import ArxivClient
            from src.lit_review_agent.retrieval.semantic_scholar_client import SemanticScholarClient

            # 创建简化的代理对象
            class SimpleLiteratureAgent:
                def __init__(self):
                    self.arxiv_client = ArxivClient(
                        api_url="http://export.arxiv.org/api/",
                        max_results=100
                    )

                    # 简化的配置对象
                    class SimpleConfig:
                        def __init__(self):
                            self.semantic_scholar_api_key = None
                            self.semantic_scholar_timeout_seconds = 30
                            self.pdf_processing_timeout = 120
                            self.semantic_scholar_api_url = "https://api.semanticscholar.org/graph/v1"

                    self.semantic_scholar_client = SemanticScholarClient(
                        config=SimpleConfig())

                async def conduct_literature_review(self, **kwargs):
                    """简化的文献综述方法"""
                    query = kwargs.get('raw_query') or kwargs.get(
                        'research_topic') or kwargs.get('query')
                    max_papers = kwargs.get('max_papers', 20)
                    sources = kwargs.get('sources', ['arxiv'])

                    print(f">> 开始搜索: {query}")

                    all_papers = []

                    # 使用arXiv搜索
                    if 'arxiv' in sources:
                        try:
                            arxiv_results = await self.arxiv_client.search(
                                query=query,
                                max_results=min(max_papers, 10)
                            )
                            all_papers.extend(arxiv_results)
                            print(f">> 从arXiv获取到 {len(arxiv_results)} 篇论文")
                        except Exception as e:
                            print(f">> arXiv搜索失败: {e}")

                    # 使用Semantic Scholar搜索
                    if 'semantic_scholar' in sources:
                        try:
                            s2_results = await self.semantic_scholar_client.search(
                                query=query,
                                max_results=min(max_papers, 10)
                            )
                            all_papers.extend(s2_results)
                            print(
                                f">> 从Semantic Scholar获取到 {len(s2_results)} 篇论文")
                        except Exception as e:
                            print(f">> Semantic Scholar搜索失败: {e}")

                    # 转换为API格式
                    processed_papers = []
                    for paper in all_papers:
                        processed_papers.append({
                            'title': paper.title,
                            'authors': paper.authors,
                            'published_date': paper.publication_date.isoformat() if paper.publication_date else '',
                            'source': paper.source,
                            'summary': paper.abstract or '',
                            'keywords': [],
                            'url': paper.url,
                            'pdf_url': paper.pdf_url or '',
                            'full_text_retrieved': False
                        })

                    return {
                        'processed_papers': processed_papers,
                        'action_plan': [
                            f"🎯 确定研究主题：{query}",
                            "📚 选择数据源：arXiv",
                            f"🔎 执行检索策略：检索最多{max_papers}篇相关论文",
                            "📊 分析论文元数据：标题、作者、摘要等",
                            "📝 整理搜索结果"
                        ]
                    }

            literature_agent = SimpleLiteratureAgent()
            print(">> 简化文献代理初始化成功")
        except Exception as e:
            print(f">> 代理初始化失败: {e}")
            print(">> 将使用模拟数据模式")
            literature_agent = None
    return literature_agent


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Literature Review API",
        "version": "3.1.0",
        "status": "running",
    }


# 认证端点
@app.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录获取访问token"""
    if not authenticate_user:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Authentication not available"
        )

    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user


@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        agent = get_agent()
        agent_status = "healthy" if agent else "degraded"
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "agent_status": agent_status,
            "version": "3.1.0",
            "services": {
                "api": "running",
                "agent": agent_status,
                "database": "connected" if agent else "unavailable",
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "agent_status": "error",
        }


@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    agent = get_agent()
    return {
        "status": "healthy" if agent else "demo",
        "timestamp": datetime.now().isoformat(),
        "agent_initialized": agent is not None,
    }


@app.post("/api/search", response_model=SearchResult)
@rate_limit_search
async def search_literature(
    request: SearchRequest,
    current_user: User = Depends(get_current_active_user)
):
    """文献检索"""
    start_time = time.time()

    try:
        agent = get_agent()

        # Determine which query to use
        query_to_use = request.rawQuery or request.query
        if not query_to_use:
            raise HTTPException(
                status_code=400, detail="Either 'query' or 'rawQuery' must be provided"
            )

        print(f"开始检索: {query_to_use}")

        if agent:
            # 使用真实的代理
            if request.rawQuery:
                # Use natural language processing
                results = await agent.conduct_literature_review(
                    raw_query=request.rawQuery,
                    max_papers=request.maxPapers,
                    sources=request.sources,
                    retrieve_full_text=request.retrieveFullText,
                    year_start=request.yearStart,
                    year_end=request.yearEnd,
                )
            else:
                # Use legacy structured query
                results = await agent.conduct_literature_review(
                    research_topic=request.query,
                    max_papers=request.maxPapers,
                    sources=request.sources,
                    retrieve_full_text=request.retrieveFullText,
                    year_start=request.yearStart,
                    year_end=request.yearEnd,
                )

            # 转换结果格式
            papers = []
            action_plan = None

            if results and "processed_papers" in results:
                for paper_data in results["processed_papers"]:
                    paper = Paper(
                        title=paper_data.get("title", "未知标题"),
                        authors=paper_data.get("authors", []),
                        publishedDate=paper_data.get("published_date", ""),
                        source=paper_data.get("source", "unknown"),
                        summary=paper_data.get(
                            "ai_enhanced_summary", paper_data.get(
                                "summary", "")
                        ),
                        keywords=paper_data.get("keywords", []),
                        url=paper_data.get("url", ""),
                        pdfUrl=paper_data.get("pdf_url", ""),
                        fullTextRetrieved=paper_data.get(
                            "full_text_retrieved", False),
                    )
                    papers.append(paper)

                # Extract action plan from results
                action_plan = results.get("action_plan", [])
        else:
            # Agent not available - return error instead of mock data
            raise HTTPException(
                status_code=503,
                detail="Literature agent is not available. Please check system configuration and ensure all required services are running."
            )

        processing_time = time.time() - start_time

        print(f"检索完成: 找到 {len(papers)} 篇论文，耗时 {processing_time:.2f}s")

        return SearchResult(
            papers=papers,
            totalCount=len(papers),
            processingTime=processing_time,
            summary=f"基于'{query_to_use}'的文献检索完成，共找到{len(papers)}篇相关论文。",
            actionPlan=action_plan,
        )

    except Exception as e:
        print(f"检索失败: {e}")
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")


@app.post("/api/generate-report")
@rate_limit_api
async def generate_report(
    request: ReportRequest,
    current_user: User = Depends(get_current_active_user)
):
    """生成综述报告"""
    try:
        print(f"开始生成报告: {request.title}")

        agent = get_agent()
        if not agent:
            raise HTTPException(
                status_code=503,
                detail="Literature agent is not available for report generation"
            )

        # 使用真实的agent生成报告
        try:
            # 转换paper数据格式以便agent处理
            papers_data = []
            for paper in request.papers:
                papers_data.append({
                    "title": paper.title,
                    "authors": paper.authors,
                    "published_date": paper.publishedDate,
                    "source": paper.source,
                    "summary": paper.summary,
                    "keywords": paper.keywords,
                    "url": paper.url,
                    "full_text_retrieved": paper.fullTextRetrieved
                })

            # 调用agent的报告生成功能
            report_result = await agent.generate_comprehensive_report(
                papers_data=papers_data,
                topic=request.title,
                custom_prompt=getattr(request, 'customPrompt', None)
            )

            report = report_result.get('report', '') if isinstance(
                report_result, dict) else str(report_result)

            if not report.strip():
                raise HTTPException(
                    status_code=500,
                    detail="Generated report is empty"
                )

            print("报告生成完成")
            return {"report": report}

        except Exception as e:
            print(f"Agent报告生成异常: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Report generation failed: {str(e)}"
            )

    except Exception as e:
        print(f"报告生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    print("启动 FastAPI 服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
