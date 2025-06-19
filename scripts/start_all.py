#!/usr/bin/env python3
"""
Tsearch - AI智能文献综述系统
一键启动脚本：同时启动后端API服务器和前端开发服务器
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_FILE = PROJECT_ROOT / "src" / "lit_review_agent" / "api_server.py"
FRONTEND_DIR = PROJECT_ROOT / "frontend" / "literature-review-frontend"


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
    UNDERLINE = '\033[4m'


def print_colored(message, color=Colors.OKGREEN):
    """打印彩色消息"""
    print(f"{color}{message}{Colors.ENDC}")


def print_header():
    """打印启动头部信息"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🚀 AI Literature Review System", Colors.HEADER)
    print_colored("   智能文献综述系统 - 统一启动器", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print()


def check_requirements():
    """检查系统要求"""
    print_colored("🔍 检查系统要求...", Colors.OKBLUE)

    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_colored("❌ Python 3.8+ 是必需的", Colors.FAIL)
        return False
    print_colored(
        f"✅ Python {python_version.major}.{python_version.minor}", Colors.OKGREEN)

    # 检查Node.js
    try:
        result = subprocess.run(['node', '--version'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print_colored(f"✅ Node.js {result.stdout.strip()}", Colors.OKGREEN)
        else:
            print_colored("❌ Node.js 未安装", Colors.FAIL)
            return False
    except FileNotFoundError:
        print_colored("❌ Node.js 未安装", Colors.FAIL)
        return False

    # 检查后端文件
    if not BACKEND_FILE.exists():
        print_colored("❌ 后端文件不存在", Colors.FAIL)
        return False
    print_colored("✅ 后端文件存在", Colors.OKGREEN)

    # 检查前端目录
    if not FRONTEND_DIR.exists():
        print_colored("❌ 前端目录不存在", Colors.FAIL)
        return False
    print_colored("✅ 前端目录存在", Colors.OKGREEN)

    print()
    return True


def setup_virtual_environment():
    """设置虚拟环境"""
    venv_path = PROJECT_ROOT / "venv"

    if not venv_path.exists():
        print_colored("🔧 创建虚拟环境...", Colors.WARNING)
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)])
        print_colored("✅ 虚拟环境创建成功", Colors.OKGREEN)
    else:
        print_colored("✅ 虚拟环境已存在", Colors.OKGREEN)

    return venv_path


def get_venv_python(venv_path):
    """获取虚拟环境的Python路径"""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "python"


def install_dependencies():
    """安装依赖"""
    print_colored("📦 检查并安装依赖...", Colors.OKBLUE)

    # 设置虚拟环境
    venv_path = setup_virtual_environment()
    venv_python = get_venv_python(venv_path)

    # 检查Python依赖
    try:
        result = subprocess.run([str(venv_python), '-c', 'import fastapi, uvicorn'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print_colored("✅ Python 依赖已安装", Colors.OKGREEN)
        else:
            raise ImportError("Dependencies not found")
    except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
        print_colored("📦 安装Python依赖...", Colors.WARNING)
        # 升级pip
        subprocess.run([str(venv_python), '-m', 'pip',
                       'install', '--upgrade', 'pip'])
        # 安装依赖
        subprocess.run([str(venv_python), '-m', 'pip',
                       'install', '-r', 'requirements.txt'])
        print_colored("✅ Python 依赖安装完成", Colors.OKGREEN)

    # 检查Node.js依赖
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        print_colored("📦 安装Node.js依赖...", Colors.WARNING)
        os.chdir(FRONTEND_DIR)
        subprocess.run(['npm', 'install'])
        os.chdir(PROJECT_ROOT)
        print_colored("✅ Node.js 依赖安装完成", Colors.OKGREEN)
    else:
        print_colored("✅ Node.js 依赖已安装", Colors.OKGREEN)

    print()
    return venv_python


def start_backend(venv_python):
    """启动后端服务"""
    print_colored("🔧 启动后端服务...", Colors.OKBLUE)
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

        # 等待服务启动并检查状态
        print_colored("⏳ 等待后端服务初始化...", Colors.WARNING)
        for i in range(15):  # 等待最多15秒
            time.sleep(1)
            if process.poll() is None:
                # 进程仍在运行，检查是否可以连接
                try:
                    import requests
                    response = requests.get(
                        "http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        print_colored(
                            "✅ 后端服务启动成功 (http://localhost:8000)", Colors.OKGREEN)
                        return process
                except:
                    continue  # 继续等待
            else:
                # 进程已停止
                break

        # 如果到这里，说明启动失败
        print_colored("❌ 后端服务启动失败", Colors.FAIL)
        if process.stdout:
            try:
                output = process.stdout.read()
                if output:
                    print_colored(f"错误输出: {output}", Colors.FAIL)
            except:
                pass
        return None
    except Exception as e:
        print_colored(f"❌ 后端启动错误: {e}", Colors.FAIL)
        return None


def start_frontend():
    """启动前端服务"""
    print_colored("🎨 启动前端服务...", Colors.OKBLUE)
    try:
        os.chdir(FRONTEND_DIR)

        # 优先使用npx vite，这样更可靠
        try:
            process = subprocess.Popen(
                ['npx', 'vite'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=FRONTEND_DIR
            )
        except:
            # 如果npx失败，尝试npm run dev
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=FRONTEND_DIR,
                shell=True
            )

        # 等待服务启动
        time.sleep(8)

        if process.poll() is None:
            print_colored("✅ 前端服务启动成功 (http://localhost:5173)", Colors.OKGREEN)
            return process
        else:
            print_colored("❌ 前端服务启动失败", Colors.FAIL)
            # 打印错误输出以便调试
            if process.stdout:
                output = process.stdout.read()
                print_colored(f"错误输出: {output}", Colors.FAIL)
            return None
    except Exception as e:
        print_colored(f"❌ 前端启动错误: {e}", Colors.FAIL)
        return None
    finally:
        os.chdir(PROJECT_ROOT)


def monitor_processes(backend_process, frontend_process):
    """监控进程状态"""
    print_colored("\n🎯 服务状态监控", Colors.OKBLUE)
    print_colored("按 Ctrl+C 停止所有服务", Colors.WARNING)
    print_colored("-" * 40, Colors.OKCYAN)

    try:
        while True:
            # 检查后端状态
            if backend_process and backend_process.poll() is not None:
                print_colored("❌ 后端服务已停止", Colors.FAIL)
                break

            # 检查前端状态
            if frontend_process and frontend_process.poll() is not None:
                print_colored("❌ 前端服务已停止", Colors.FAIL)
                break

            time.sleep(2)

    except KeyboardInterrupt:
        print_colored("\n🛑 正在停止服务...", Colors.WARNING)

        if backend_process:
            backend_process.terminate()
            print_colored("✅ 后端服务已停止", Colors.OKGREEN)

        if frontend_process:
            frontend_process.terminate()
            print_colored("✅ 前端服务已停止", Colors.OKGREEN)

        print_colored("👋 再见！", Colors.HEADER)


def main():
    """主函数"""
    print_header()

    # 检查系统要求
    if not check_requirements():
        print_colored("❌ 系统要求检查失败，请解决上述问题后重试", Colors.FAIL)
        sys.exit(1)

    # 安装依赖并获取虚拟环境Python路径
    venv_python = install_dependencies()

    # 启动服务
    print_colored("🚀 启动服务...", Colors.HEADER)

    backend_process = start_backend(venv_python)
    if not backend_process:
        print_colored("❌ 无法启动后端服务", Colors.FAIL)
        sys.exit(1)

    frontend_process = start_frontend()
    if not frontend_process:
        print_colored("❌ 无法启动前端服务", Colors.FAIL)
        if backend_process:
            backend_process.terminate()
        sys.exit(1)

    print_colored("\n🎉 所有服务启动成功！", Colors.OKGREEN)
    print_colored("📖 后端API文档: http://localhost:8000/docs", Colors.OKCYAN)
    print_colored("🌐 前端界面: http://localhost:5173", Colors.OKCYAN)

    # 自动打开浏览器显示欢迎页
    print_colored("🌐 正在打开浏览器...", Colors.OKBLUE)
    try:
        time.sleep(2)  # 等待前端完全启动
        webbrowser.open("http://localhost:5173")
        print_colored("✅ 浏览器已打开", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"⚠️ 无法自动打开浏览器: {e}", Colors.WARNING)
        print_colored("请手动访问: http://localhost:5173", Colors.OKCYAN)

    # 监控进程
    monitor_processes(backend_process, frontend_process)


if __name__ == "__main__":
    main()
