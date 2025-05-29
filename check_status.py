#!/usr/bin/env python3
"""系统状态检查脚本"""

import requests
import subprocess
import sys
import time

def check_backend():
    """检查后端服务状态"""
    try:
        # 先尝试API状态端点
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正在运行 (http://localhost:8000)")
            return True
    except requests.exceptions.RequestException:
        pass
    
    try:
        # 再尝试根端点
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正在运行 (http://localhost:8000)")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("❌ 后端服务未启动")
    return False

def check_frontend():
    """检查前端服务状态"""
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正在运行 (http://localhost:5173)")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("❌ 前端服务未启动")
    return False

def check_processes():
    """检查相关进程"""
    try:
        # 检查Python进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        python_processes = len([line for line in result.stdout.split('\n') if 'python.exe' in line])
        
        # 检查Node.js进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq node.exe'], 
                              capture_output=True, text=True, shell=True)
        node_processes = len([line for line in result.stdout.split('\n') if 'node.exe' in line])
        
        print(f"🔍 Python进程数: {python_processes}")
        print(f"🔍 Node.js进程数: {node_processes}")
        
    except Exception as e:
        print(f"❌ 进程检查失败: {e}")

def main():
    print("🔍 AI文献综述系统状态检查")
    print("=" * 40)
    
    # 检查服务状态
    backend_running = check_backend()
    frontend_running = check_frontend()
    
    print("\n📊 进程状态:")
    check_processes()
    
    print("\n📝 服务访问地址:")
    if backend_running:
        print("🔗 后端API: http://localhost:8000")
    if frontend_running:
        print("🔗 前端界面: http://localhost:5173")
    
    if not backend_running or not frontend_running:
        print("\n💡 启动服务:")
        print("后端: python -m src.lit_review_agent.app")
        print("前端: cd frontend/literature-review-frontend && npm run dev")

if __name__ == "__main__":
    main() 