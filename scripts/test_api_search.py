#!/usr/bin/env python3
"""
测试API搜索功能
"""

import requests
import json
import time

def test_api_search():
    """测试API搜索功能"""
    url = "http://localhost:8000/api/search"
    
    # 测试数据
    test_data = {
        "query": "quantum computing",
        "max_papers": 2,
        "sources": ["arxiv"],
        "enable_ai_analysis": False,
        "enable_full_text": False
    }
    
    print("🔍 测试API搜索功能...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(test_data, indent=2)}")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            url,
            json=test_data,
            timeout=60
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"处理时间: {processing_time:.2f}秒")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 搜索成功！")
            print(f"找到论文数量: {data.get('totalCount', 0)}")
            
            papers = data.get('papers', [])
            for i, paper in enumerate(papers, 1):
                print(f"\n{i}. {paper.get('title', '无标题')}")
                print(f"   作者: {', '.join(paper.get('authors', []))}")
                print(f"   发布日期: {paper.get('publishedDate', '未知')}")
                print(f"   来源: {paper.get('source', '未知')}")
                if paper.get('summary'):
                    print(f"   摘要: {paper.get('summary')[:100]}...")
            
            return True
        else:
            print(f"❌ 搜索失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

if __name__ == "__main__":
    success = test_api_search()
    if success:
        print("\n🎉 API搜索测试成功！")
    else:
        print("\n❌ API搜索测试失败！")
