#!/usr/bin/env python3
"""
Tsearch 最终系统测试
验证所有功能是否正常工作
"""

import requests
import time
import json
import sys
from pathlib import Path

def print_header(title):
    """打印测试标题"""
    print("\n" + "=" * 60)
    print(f"🧪 {title}")
    print("=" * 60)

def print_result(test_name, success, details=""):
    """打印测试结果"""
    status = "✅ 通过" if success else "❌ 失败"
    print(f"{status} {test_name}")
    if details:
        print(f"   详情: {details}")

def test_backend_health():
    """测试后端健康状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, f"状态: {data.get('status')}, Agent: {data.get('agent_status')}"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_api_search():
    """测试API搜索功能"""
    try:
        search_data = {
            "query": "artificial intelligence",
            "max_papers": 3,
            "sources": ["arxiv"],
            "enable_ai_analysis": False
        }
        
        response = requests.post(
            "http://localhost:8000/api/search",
            json=search_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            paper_count = data.get('totalCount', 0)
            processing_time = data.get('processingTime', 0)
            return True, f"找到 {paper_count} 篇论文, 耗时 {processing_time:.2f}s"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

def test_frontend_access():
    """测试前端访问"""
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            return True, "前端页面可访问"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_api_docs():
    """测试API文档"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            return True, "API文档可访问"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_natural_language_query():
    """测试自然语言查询"""
    try:
        search_data = {
            "query": "我想了解机器学习在医疗诊断中的最新应用",
            "max_papers": 2,
            "sources": ["arxiv"],
            "enable_ai_analysis": True
        }
        
        response = requests.post(
            "http://localhost:8000/api/search",
            json=search_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            has_action_plan = bool(data.get('actionPlan'))
            paper_count = data.get('totalCount', 0)
            return True, f"自然语言处理成功, 行动计划: {has_action_plan}, 论文: {paper_count}篇"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def main():
    """主测试函数"""
    print_header("Tsearch 最终系统测试")
    
    tests = [
        ("后端健康检查", test_backend_health),
        ("API文档访问", test_api_docs),
        ("前端页面访问", test_frontend_access),
        ("基础搜索功能", test_api_search),
        ("自然语言查询", test_natural_language_query),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 正在测试: {test_name}")
        try:
            success, details = test_func()
            print_result(test_name, success, details)
            results.append((test_name, success, details))
        except Exception as e:
            print_result(test_name, False, f"测试异常: {e}")
            results.append((test_name, False, f"测试异常: {e}"))
    
    # 统计结果
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print_header("测试结果汇总")
    
    for test_name, success, details in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {details}")
    
    print(f"\n📊 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统完全可用！")
        print("\n🚀 您可以开始使用 Tsearch 进行文献综述了：")
        print("   • 前端界面: http://localhost:5173")
        print("   • API文档: http://localhost:8000/docs")
        print("   • 测试页面: test_frontend.html")
        return 0
    elif passed >= total * 0.8:
        print("\n⚠️ 大部分测试通过，系统基本可用")
        print("   建议检查失败的测试项目")
        return 1
    else:
        print("\n❌ 多个测试失败，系统存在问题")
        print("   请检查服务是否正常启动")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
