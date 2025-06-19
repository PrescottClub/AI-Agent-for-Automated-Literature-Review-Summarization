#!/usr/bin/env python3
"""
简单的前端测试脚本
"""

import requests
import time

def test_frontend():
    """测试前端访问"""
    try:
        print("🔍 测试前端访问...")
        response = requests.get("http://localhost:5173", timeout=10)
        print(f"✅ 状态码: {response.status_code}")
        print(f"✅ 内容长度: {len(response.text)} 字符")
        
        if "Tsearch" in response.text:
            print("✅ 找到 Tsearch 标题")
        else:
            print("⚠️ 未找到 Tsearch 标题")
            
        if "app" in response.text:
            print("✅ 找到 Vue app 容器")
        else:
            print("⚠️ 未找到 Vue app 容器")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败 - 前端服务可能未启动")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_backend():
    """测试后端访问"""
    try:
        print("🔍 测试后端访问...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        data = response.json()
        print(f"✅ 后端状态: {data.get('status')}")
        print(f"✅ Agent状态: {data.get('agent_status')}")
        return True
    except Exception as e:
        print(f"❌ 后端测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Tsearch 简单连接测试")
    print("=" * 50)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"后端: {'✅ 正常' if backend_ok else '❌ 异常'}")
    print(f"前端: {'✅ 正常' if frontend_ok else '❌ 异常'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 系统完全可用!")
        print("🌐 前端: http://localhost:5173")
        print("📖 API文档: http://localhost:8000/docs")
    elif backend_ok:
        print("\n⚠️ 后端可用，前端有问题")
        print("📖 可以使用API文档: http://localhost:8000/docs")
    else:
        print("\n❌ 系统存在问题，需要检查服务状态")
