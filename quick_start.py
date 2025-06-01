#!/usr/bin/env python3
"""
Quick Start Script for Tsearch AI Literature Review System
快速启动脚本 - Tsearch AI文献综述系统
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def setup_environment():
    """设置环境变量"""
    print("🔧 设置环境变量...")
    
    # 设置基本环境变量
    env_vars = {
        'LLM_PROVIDER': 'mock',
        'LOG_LEVEL': 'INFO',
        'DEBUG': 'false',
        'LLM_TIMEOUT_SECONDS': '60',
        'DEFAULT_RETRIEVAL_SOURCES': 'arxiv,semantic_scholar',
        'SPACY_MODEL_NAME': 'en_core_web_sm',
        'OUTPUT_DIR': './data/outputs',
        'MAX_REQUESTS_PER_MINUTE': '60',
        'REPORT_FORMAT': 'markdown'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ 环境变量设置完成")

def ensure_directories():
    """确保必要的目录存在"""
    print("📁 创建必要目录...")
    
    directories = [
        'data/outputs',
        'data/chroma_db', 
        'logs'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录创建完成")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端API服务器...")
    
    # 添加src到Python路径
    sys.path.append('src')
    
    try:
        import uvicorn
        from lit_review_agent.api_server import app
        
        # 在新线程中启动服务器
        def run_server():
            uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        print("✅ 后端服务器启动成功 - http://localhost:8000")
        return True
        
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        print("💡 尝试手动启动: python src/lit_review_agent/api_server.py")
        return False

def start_frontend():
    """启动前端服务"""
    print("🎨 启动前端开发服务器...")
    
    frontend_dir = Path("frontend/literature-review-frontend")
    
    if not frontend_dir.exists():
        print("❌ 前端目录不存在")
        return False
    
    try:
        # 检查npm是否可用
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        
        # 切换到前端目录并启动开发服务器
        print("正在启动Vite开发服务器...")
        os.chdir(frontend_dir)
        
        # 启动前端开发服务器
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ 前端服务器启动成功 - http://localhost:5173")
        return frontend_process
        
    except subprocess.CalledProcessError:
        print("❌ npm不可用，请安装Node.js和npm")
        return False
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Tsearch AI Literature Review System - 快速启动")
    print("=" * 60)
    
    # 设置环境
    setup_environment()
    ensure_directories()
    
    # 启动后端
    backend_ok = start_backend()
    
    if backend_ok:
        time.sleep(2)  # 等待后端启动
        
        # 启动前端
        frontend_process = start_frontend()
        
        if frontend_process:
            print("\n🎉 系统启动完成!")
            print("-" * 40)
            print("📊 后端API: http://localhost:8000")
            print("📊 API文档: http://localhost:8000/docs")
            print("🎨 前端界面: http://localhost:5173")
            print("-" * 40)
            print("按 Ctrl+C 停止服务")
            
            try:
                frontend_process.wait()
            except KeyboardInterrupt:
                print("\n👋 正在停止服务...")
                frontend_process.terminate()
        else:
            print("\n⚠️ 前端启动失败，但后端正常运行")
            print("📊 后端API: http://localhost:8000")
            print("请手动启动前端: cd frontend/literature-review-frontend && npm run dev")
    else:
        print("\n❌ 启动失败，请检查环境配置")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 