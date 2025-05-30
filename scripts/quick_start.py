#!/usr/bin/env python3
"""
🚀 AI文献综述系统 - 快速启动脚本
===================================

一键启动 Docker 容器化的文献综述系统。

Usage:
    python scripts/quick_start.py [options]

Options:
    --build         重新构建 Docker 镜像
    --logs          显示容器日志
    --stop          停止所有服务
    --clean         清理所有容器和镜像
    --dev           启动开发环境
    --prod          启动生产环境
    --monitoring    启动监控服务
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_command(command, shell=True, check=True):
    """运行命令并处理错误"""
    print(f"🔧 执行命令: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            check=check, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print(f"✅ 输出: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return None

def check_docker():
    """检查 Docker 是否安装和运行"""
    print("🐳 检查 Docker 环境...")
    
    # 检查 Docker 是否安装
    result = run_command("docker --version", check=False)
    if result is None:
        print("❌ Docker 未安装或不可用")
        print("请先安装 Docker Desktop: https://www.docker.com/products/docker-desktop")
        return False
    
    # 检查 Docker 是否运行
    result = run_command("docker info", check=False)
    if result is None:
        print("❌ Docker 未运行")
        print("请启动 Docker Desktop")
        return False
    
    print("✅ Docker 环境正常")
    return True

def check_docker_compose():
    """检查 Docker Compose 是否可用"""
    print("🔧 检查 Docker Compose...")
    
    result = run_command("docker-compose --version", check=False)
    if result is None:
        # 尝试新版本命令
        result = run_command("docker compose version", check=False)
        if result is None:
            print("❌ Docker Compose 不可用")
            return False
    
    print("✅ Docker Compose 可用")
    return True

def build_images(force=False):
    """构建 Docker 镜像"""
    print("🏗️  构建 Docker 镜像...")
    
    command = "docker-compose build"
    if force:
        command += " --no-cache"
    
    result = run_command(command)
    if result:
        print("✅ 镜像构建完成")
        return True
    else:
        print("❌ 镜像构建失败")
        return False

def start_services(profile=None):
    """启动服务"""
    print("🚀 启动服务...")
    
    command = "docker-compose up -d"
    if profile:
        command += f" --profile {profile}"
    
    result = run_command(command)
    if result:
        print("✅ 服务启动成功")
        return True
    else:
        print("❌ 服务启动失败")
        return False

def stop_services():
    """停止所有服务"""
    print("⏹️  停止服务...")
    
    result = run_command("docker-compose down")
    if result:
        print("✅ 服务已停止")
        return True
    else:
        print("❌ 停止服务失败")
        return False

def show_logs():
    """显示服务日志"""
    print("📋 显示服务日志...")
    run_command("docker-compose logs -f --tail=100")

def clean_all():
    """清理所有容器和镜像"""
    print("🧹 清理 Docker 环境...")
    
    # 停止所有服务
    run_command("docker-compose down", check=False)
    
    # 删除相关镜像
    run_command("docker image prune -f", check=False)
    
    # 删除未使用的卷
    run_command("docker volume prune -f", check=False)
    
    print("✅ 清理完成")

def check_services():
    """检查服务状态"""
    print("🔍 检查服务状态...")
    
    # 检查容器状态
    result = run_command("docker-compose ps")
    
    # 等待服务启动
    print("⏳ 等待服务就绪...")
    time.sleep(10)
    
    # 检查健康状态
    print("🏥 检查服务健康状态...")
    run_command("curl -f http://localhost:8000/api/health || echo '后端服务检查失败'", check=False)
    
    print("\n🎉 服务状态检查完成!")
    print("📖 访问地址:")
    print("   - 前端界面: http://localhost:5174")
    print("   - 后端 API: http://localhost:8000")
    print("   - API 文档: http://localhost:8000/docs")
    print("   - 健康检查: http://localhost:8000/api/health")

def create_env_file():
    """创建环境变量文件"""
    env_file = project_root / "config" / ".env"
    env_example = project_root / "config" / "config.example.env"
    
    if not env_file.exists() and env_example.exists():
        print("📝 创建环境变量文件...")
        
        # 复制示例文件
        import shutil
        shutil.copy2(env_example, env_file)
        
        print(f"✅ 已创建 {env_file}")
        print("⚠️  请编辑 config/.env 文件并设置你的 API 密钥")
        print("   - DEEPSEEK_API_KEY=your_api_key_here")
        print("   - OPENAI_API_KEY=your_api_key_here (可选)")
        
        return False  # 需要用户手动配置
    
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AI文献综述系统 - 快速启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--build", action="store_true", help="重新构建 Docker 镜像")
    parser.add_argument("--logs", action="store_true", help="显示容器日志")
    parser.add_argument("--stop", action="store_true", help="停止所有服务")
    parser.add_argument("--clean", action="store_true", help="清理所有容器和镜像")
    parser.add_argument("--dev", action="store_true", help="启动开发环境")
    parser.add_argument("--prod", action="store_true", help="启动生产环境")
    parser.add_argument("--monitoring", action="store_true", help="启动监控服务")
    
    args = parser.parse_args()
    
    print("🤖 AI文献综述系统 - Docker 快速启动")
    print("=" * 50)
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    # 处理特殊命令
    if args.logs:
        show_logs()
        return
    
    if args.stop:
        stop_services()
        return
    
    if args.clean:
        clean_all()
        return
    
    # 检查环境
    if not check_docker():
        return
    
    if not check_docker_compose():
        return
    
    # 创建环境变量文件
    if not create_env_file():
        print("\n⚠️  请先配置 API 密钥后再运行")
        return
    
    # 构建镜像
    if args.build or not os.path.exists("Dockerfile"):
        if not build_images(force=args.build):
            return
    
    # 确定启动配置
    profile = None
    if args.prod:
        profile = "production"
    elif args.monitoring:
        profile = "monitoring"
    elif args.dev:
        profile = "development"
    
    # 启动服务
    if not start_services(profile):
        return
    
    # 检查服务状态
    check_services()
    
    print("\n🎊 启动完成!")
    print("💡 使用以下命令管理服务:")
    print("   python scripts/quick_start.py --logs    # 查看日志")
    print("   python scripts/quick_start.py --stop    # 停止服务")
    print("   python scripts/quick_start.py --clean   # 清理环境")

if __name__ == "__main__":
    main() 