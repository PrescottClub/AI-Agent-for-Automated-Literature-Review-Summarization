#!/usr/bin/env python3
"""
测试自然语言查询处理功能
Test script for natural language query processing functionality
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from lit_review_agent.utils.config import Config
from lit_review_agent.ai_core.llm_manager import LLMManager
from lit_review_agent.agent import LiteratureAgent


async def test_parameter_extraction():
    """测试参数提取功能"""
    print("=" * 60)
    print("测试自然语言参数提取功能")
    print("=" * 60)
    
    # 初始化LLM管理器
    config = Config()
    llm_manager = LLMManager(config)
    
    # 测试查询
    test_queries = [
        "我想了解最近三年人工智能在医疗诊断领域的应用进展",
        "寻找关于深度学习优化算法的最新研究，重点关注transformer架构",
        "查找2020年以来量子计算在密码学中的应用研究",
        "machine learning in healthcare applications from 2020 to 2023",
        "recent advances in natural language processing, focusing on transformer architectures",
        "quantum computing"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. 测试查询: {query}")
        print("-" * 50)
        
        try:
            # 提取参数
            params = await llm_manager.extract_core_research_params(query)
            
            print(f"提取的主题: {params.get('topic')}")
            print(f"时间限制: {params.get('time_limit')}")
            print(f"关注重点: {params.get('focus')}")
            
        except Exception as e:
            print(f"错误: {e}")


async def test_full_pipeline():
    """测试完整的自然语言查询流程"""
    print("\n" + "=" * 60)
    print("测试完整的自然语言查询流程")
    print("=" * 60)
    
    # 初始化Agent
    config = Config()
    agent = LiteratureAgent(config)
    
    # 测试查询
    test_query = "我想了解最近三年人工智能在医疗诊断领域的应用进展"
    
    print(f"测试查询: {test_query}")
    print("-" * 50)
    
    try:
        # 执行文献综述
        results = await agent.conduct_literature_review(
            raw_query=test_query,
            max_papers=5,  # 限制数量以便快速测试
            sources=["arxiv"],  # 只使用arXiv以便快速测试
            retrieve_full_text=False
        )
        
        print(f"\n✅ 成功完成查询!")
        print(f"处理的论文数量: {results.get('num_papers_processed', 0)}")
        print(f"研究主题: {results.get('research_topic', 'N/A')}")
        
        # 显示前几篇论文的标题
        papers = results.get('processed_papers', [])
        if papers:
            print(f"\n前{min(3, len(papers))}篇论文:")
            for i, paper in enumerate(papers[:3], 1):
                print(f"{i}. {paper.get('title', 'N/A')}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


async def test_api_compatibility():
    """测试API兼容性"""
    print("\n" + "=" * 60)
    print("测试API兼容性")
    print("=" * 60)
    
    # 初始化Agent
    config = Config()
    agent = LiteratureAgent(config)
    
    # 测试传统方式
    print("1. 测试传统结构化查询:")
    try:
        results1 = await agent.conduct_literature_review(
            research_topic="machine learning",
            max_papers=2,
            sources=["arxiv"],
            retrieve_full_text=False
        )
        print(f"✅ 传统方式成功，处理了 {results1.get('num_papers_processed', 0)} 篇论文")
    except Exception as e:
        print(f"❌ 传统方式失败: {e}")
    
    # 测试新的自然语言方式
    print("\n2. 测试自然语言查询:")
    try:
        results2 = await agent.conduct_literature_review(
            raw_query="machine learning applications in healthcare",
            max_papers=2,
            sources=["arxiv"],
            retrieve_full_text=False
        )
        print(f"✅ 自然语言方式成功，处理了 {results2.get('num_papers_processed', 0)} 篇论文")
    except Exception as e:
        print(f"❌ 自然语言方式失败: {e}")


async def main():
    """主函数"""
    print("🚀 开始测试自然语言查询处理功能")
    
    try:
        # 测试参数提取
        await test_parameter_extraction()
        
        # 测试完整流程
        await test_full_pipeline()
        
        # 测试API兼容性
        await test_api_compatibility()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
