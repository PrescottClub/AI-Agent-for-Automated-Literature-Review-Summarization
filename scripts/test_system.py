#!/usr/bin/env python3
"""
Tsearch 系统测试脚本
测试后端API功能和基本可用性
"""

import requests
import json
import time
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def test_api_health():
    """测试API健康状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API健康检查通过")
            print(f"   状态: {data.get('status')}")
            print(f"   版本: {data.get('version')}")
            print(f"   Agent状态: {data.get('agent_status')}")
            return True
        else:
            print(f"❌ API健康检查失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到API服务器: {e}")
        return False

def test_api_search():
    """测试API搜索功能"""
    try:
        search_data = {
            "query": "machine learning",
            "max_papers": 3,
            "sources": ["arxiv"],
            "enable_ai_analysis": False,
            "enable_full_text": False
        }
        
        print("🔍 测试搜索功能...")
        response = requests.post(
            "http://localhost:8000/api/search",
            json=search_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 搜索功能正常")
            print(f"   找到论文: {data.get('totalCount', 0)}篇")
            print(f"   处理时间: {data.get('processingTime', 0):.2f}秒")
            
            # 显示前几篇论文
            papers = data.get('papers', [])
            for i, paper in enumerate(papers[:2]):
                print(f"   论文{i+1}: {paper.get('title', '无标题')[:50]}...")
            
            return True
        else:
            print(f"❌ 搜索功能失败: HTTP {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 搜索请求失败: {e}")
        return False

def test_config_loading():
    """测试配置加载"""
    try:
        from lit_review_agent.utils.config import Config
        config = Config()
        print(f"✅ 配置加载成功")
        print(f"   应用名称: {config.app_name}")
        print(f"   LLM提供商: {config.llm_provider}")
        print(f"   调试模式: {config.debug}")
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_basic_imports():
    """测试基本模块导入"""
    try:
        from lit_review_agent.agent import LiteratureAgent
        from lit_review_agent.utils.helpers import clean_text
        from lit_review_agent.exceptions import LiteratureReviewError
        
        print("✅ 核心模块导入成功")
        
        # 测试基本功能
        cleaned = clean_text("  Hello   World!  ")
        if cleaned == "Hello World!":
            print("✅ 文本清理功能正常")
        else:
            print("⚠️ 文本清理功能异常")
            
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始 Tsearch 系统测试")
    print("=" * 50)
    
    tests = [
        ("配置加载", test_config_loading),
        ("模块导入", test_basic_imports),
        ("API健康检查", test_api_health),
        ("API搜索功能", test_api_search),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
        return 0
    elif passed >= total * 0.7:
        print("⚠️ 大部分测试通过，系统基本可用")
        return 1
    else:
        print("❌ 多个测试失败，系统存在问题")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
