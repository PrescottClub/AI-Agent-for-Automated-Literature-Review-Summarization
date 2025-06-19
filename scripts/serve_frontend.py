#!/usr/bin/env python3
"""
简单的HTTP服务器来提供前端测试页面
避免CORS问题
"""

import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path

def start_server():
    """启动HTTP服务器"""
    PORT = 8080
    
    # 切换到项目根目录
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 前端测试服务器启动在 http://localhost:{PORT}")
        print(f"📁 服务目录: {project_root}")
        print(f"🔗 测试页面: http://localhost:{PORT}/test_frontend.html")
        print("按 Ctrl+C 停止服务器")
        
        # 延迟打开浏览器
        def open_browser():
            time.sleep(2)
            webbrowser.open(f"http://localhost:{PORT}/test_frontend.html")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")

if __name__ == "__main__":
    import os
    start_server()
