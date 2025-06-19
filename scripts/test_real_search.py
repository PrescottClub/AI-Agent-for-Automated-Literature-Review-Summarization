#!/usr/bin/env python3
"""
测试真实的文献搜索功能
绕过配置问题，直接测试arXiv API
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

async def test_arxiv_search():
    """测试arXiv搜索功能"""
    try:
        from lit_review_agent.retrieval.arxiv_client import ArxivClient
        
        print("🔍 测试arXiv搜索功能...")
        
        # 创建arXiv客户端
        arxiv_client = ArxivClient(
            api_url="http://export.arxiv.org/api/",
            max_results=100
        )
        
        # 执行搜索
        query = "machine learning"
        max_results = 3
        
        print(f"搜索查询: {query}")
        print(f"最大结果数: {max_results}")
        
        results = await arxiv_client.search(query=query, max_results=max_results)
        
        print(f"\n✅ 搜索成功！找到 {len(results)} 篇论文:")
        
        for i, paper in enumerate(results, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   作者: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
            print(f"   发布日期: {paper.published_date}")
            print(f"   来源: {paper.source}")
            print(f"   URL: {paper.url}")
            if paper.abstract:
                print(f"   摘要: {paper.abstract[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ arXiv搜索失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_semantic_scholar_search():
    """测试Semantic Scholar搜索功能"""
    try:
        from lit_review_agent.retrieval.semantic_scholar_client import SemanticScholarClient
        
        print("\n🔍 测试Semantic Scholar搜索功能...")
        
        # 创建简单配置对象
        class SimpleConfig:
            def __init__(self):
                self.semantic_scholar_api_key = None
                self.semantic_scholar_timeout_seconds = 30
        
        config = SimpleConfig()
        
        # 创建Semantic Scholar客户端
        s2_client = SemanticScholarClient(config=config)
        
        # 执行搜索
        query = "machine learning"
        max_results = 3
        
        print(f"搜索查询: {query}")
        print(f"最大结果数: {max_results}")
        
        results = await s2_client.search(query=query, max_results=max_results)
        
        print(f"\n✅ 搜索成功！找到 {len(results)} 篇论文:")
        
        for i, paper in enumerate(results, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   作者: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
            print(f"   发布日期: {paper.published_date}")
            print(f"   来源: {paper.source}")
            print(f"   URL: {paper.url}")
            if paper.abstract:
                print(f"   摘要: {paper.abstract[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Semantic Scholar搜索失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主测试函数"""
    print("🚀 开始测试真实文献搜索功能")
    print("=" * 50)
    
    # 测试arXiv
    arxiv_success = await test_arxiv_search()
    
    # 测试Semantic Scholar
    s2_success = await test_semantic_scholar_search()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"   arXiv搜索: {'✅ 成功' if arxiv_success else '❌ 失败'}")
    print(f"   Semantic Scholar搜索: {'✅ 成功' if s2_success else '❌ 失败'}")
    
    if arxiv_success or s2_success:
        print("\n🎉 至少一个数据源可以正常工作！")
        print("💡 建议: 更新API服务器以使用真实数据而不是模拟数据")
        return 0
    else:
        print("\n❌ 所有数据源都无法正常工作")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
