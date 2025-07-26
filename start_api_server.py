#!/usr/bin/env python3
"""启动 API 服务器"""

import asyncio
import sys
import uvicorn
from pathlib import Path

# 添加项目根目录到 Python 路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def main():
    """启动 FastAPI 服务器"""
    print("🚀 正在启动 Literature Review API 服务器...")
    print("📍 服务器地址: http://localhost:8000")
    print("📖 API 文档: http://localhost:8000/docs")
    print("❤️  健康检查: http://localhost:8000/health")
    print()
    
    try:
        # 启动 FastAPI 服务器
        uvicorn.run(
            "src.lit_review_agent.api_server:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # 生产环境关闭热重载
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()