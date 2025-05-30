#!/usr/bin/env python3
"""
简化的后端启动脚本
专门用于启动和测试后端服务
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_FILE = PROJECT_ROOT / "src" / "lit_review_agent" / "api_server.py"

class Colors:
    """终端颜色定义"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.OKGREEN):
    """打印彩色消息"""
    print(f"{color}{message}{Colors.ENDC}")

def get_venv_python():
    """获取虚拟环境的Python路径"""
    venv_path = PROJECT_ROOT / "venv"
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "python"

def start_backend():
    """启动后端服务"""
    print_colored("🚀 启动 Tsearch 后端服务...", Colors.HEADER)
    
    venv_python = get_venv_python()
    
    if not venv_python.exists():
        print_colored("❌ 虚拟环境不存在，请先运行 python scripts/start_all.py", Colors.FAIL)
        return None
    
    try:
        # 使用虚拟环境的Python运行backend文件
        process = subprocess.Popen(
            [str(venv_python), str(BACKEND_FILE)],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        print_colored("⏳ 等待服务初始化...", Colors.WARNING)
        
        # 等待服务启动
        for i in range(20):  # 等待最多20秒
            time.sleep(1)
            if process.poll() is None:
                # 进程仍在运行，检查是否可以连接
                try:
                    import requests
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        print_colored("✅ 后端服务启动成功!", Colors.OKGREEN)
                        print_colored("📖 API文档: http://localhost:8000/docs", Colors.OKCYAN)
                        print_colored("🔗 健康检查: http://localhost:8000/health", Colors.OKCYAN)
                        
                        # 自动打开API文档
                        try:
                            webbrowser.open("http://localhost:8000/docs")
                            print_colored("🌐 已自动打开API文档", Colors.OKGREEN)
                        except:
                            pass
                        
                        return process
                except Exception as e:
                    print_colored(f"⏳ 等待中... ({i+1}/20)", Colors.WARNING)
                    continue
            else:
                # 进程已停止
                print_colored("❌ 后端进程意外停止", Colors.FAIL)
                break
        
        # 如果到这里，说明启动失败
        print_colored("❌ 后端服务启动失败", Colors.FAIL)
        if process.stdout:
            try:
                output = process.stdout.read()
                if output:
                    print_colored("错误输出:", Colors.FAIL)
                    print(output)
            except:
                pass
        return None
        
    except Exception as e:
        print_colored(f"❌ 启动错误: {e}", Colors.FAIL)
        return None

def main():
    """主函数"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🔧 Tsearch 后端服务启动器", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print()
    
    process = start_backend()
    
    if process:
        print_colored("\n🎯 服务监控中...", Colors.OKBLUE)
        print_colored("按 Ctrl+C 停止服务", Colors.WARNING)
        print_colored("-" * 40, Colors.OKCYAN)
        
        try:
            while True:
                if process.poll() is not None:
                    print_colored("❌ 后端服务已停止", Colors.FAIL)
                    break
                time.sleep(2)
        except KeyboardInterrupt:
            print_colored("\n🛑 正在停止服务...", Colors.WARNING)
            process.terminate()
            print_colored("✅ 服务已停止", Colors.OKGREEN)
    else:
        print_colored("\n💡 故障排除建议:", Colors.OKBLUE)
        print_colored("1. 检查虚拟环境是否正确安装", Colors.OKCYAN)
        print_colored("2. 确保所有依赖已安装: pip install -r requirements.txt", Colors.OKCYAN)
        print_colored("3. 检查端口8000是否被占用", Colors.OKCYAN)
        print_colored("4. 查看上方的错误输出信息", Colors.OKCYAN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n❌ 操作被用户取消", Colors.WARNING)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ 发生未预期的错误: {e}", Colors.FAIL)
        sys.exit(1)
