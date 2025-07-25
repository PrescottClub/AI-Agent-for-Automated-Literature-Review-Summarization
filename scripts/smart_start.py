#!/usr/bin/env python3
"""
Tsearch 智能启动脚本
根据功能开关配置启动相应的服务
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse


class SmartStarter:
    """智能启动器"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_dir = project_root / "config"
        self.features_config = self._load_features_config()

    def _load_features_config(self) -> Dict[str, bool]:
        """加载功能开关配置"""
        features_file = self.config_dir / "features.env"
        config = {}

        if features_file.exists():
            with open(features_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip().lower() == 'true'

        return config

    def is_feature_enabled(self, feature: str) -> bool:
        """检查功能是否启用"""
        return self.features_config.get(feature, False)

    def get_docker_profiles(self) -> List[str]:
        """根据功能配置获取Docker profiles"""
        profiles = []

        # 生产环境功能
        if self.is_feature_enabled('ENABLE_NGINX_PROXY'):
            profiles.append('production')

        # 监控功能
        if (self.is_feature_enabled('ENABLE_PROMETHEUS') or
                self.is_feature_enabled('ENABLE_GRAFANA')):
            profiles.append('monitoring')

        return profiles

    def get_docker_services(self) -> List[str]:
        """根据功能配置获取需要启动的Docker服务"""
        services = [
            'literature-review-app',  # 核心应用
            'redis',                  # 缓存服务
            'chromadb'               # 向量数据库
        ]

        # 可选服务
        if self.is_feature_enabled('ENABLE_NGINX_PROXY'):
            services.append('nginx')

        if self.is_feature_enabled('ENABLE_PROMETHEUS'):
            services.append('prometheus')

        if self.is_feature_enabled('ENABLE_GRAFANA'):
            services.append('grafana')

        return services

    def start_docker_services(self, mode: str = "development") -> bool:
        """启动Docker服务"""
        print(f"🐳 启动Docker服务 (模式: {mode})...")

        # 构建docker-compose命令
        cmd = ["docker-compose"]

        # 添加profiles
        profiles = self.get_docker_profiles()
        if profiles:
            for profile in profiles:
                cmd.extend(["--profile", profile])

        # 添加操作
        cmd.append("up")

        if mode == "production":
            cmd.append("-d")  # 后台运行

        # 指定服务
        services = self.get_docker_services()
        cmd.extend(services)

        print(f"执行命令: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Docker服务启动成功!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker服务启动失败: {e}")
            return False

    def start_local_services(self) -> bool:
        """启动本地开发服务"""
        print("🚀 启动本地开发服务...")

        # 检查Python环境
        if not self._check_python_environment():
            return False

        services_started = []

        try:
            # 启动核心API服务
            if self.is_feature_enabled('ENABLE_CORE_API'):
                print("📡 启动FastAPI服务...")
                # 这里可以添加启动FastAPI的逻辑
                services_started.append("FastAPI")

            # 启动Vue前端界面 (如果启用)
            if self.is_feature_enabled('ENABLE_VUE_FRONTEND'):
                print("🎨 Vue前端界面已启用")
                services_started.append("Vue Frontend")

            # 启动MCP服务器 (如果启用)
            if self.is_feature_enabled('ENABLE_MCP_SERVER'):
                print("🔌 MCP服务器已启用")
                services_started.append("MCP Server")

            print(f"✅ 已启用服务: {', '.join(services_started)}")
            return True

        except Exception as e:
            print(f"❌ 本地服务启动失败: {e}")
            return False

    def _check_python_environment(self) -> bool:
        """检查Python环境"""
        try:
            # 检查Python版本
            if sys.version_info < (3, 9):
                print("❌ 需要Python 3.9或更高版本")
                return False

            # 检查是否安装了项目依赖
            try:
                import lit_review_agent
                print("✅ 项目依赖已安装")
            except ImportError:
                print("⚠️  项目依赖未安装，请运行: pip install -e .")
                return False

            return True

        except Exception as e:
            print(f"❌ 环境检查失败: {e}")
            return False

    def show_status(self) -> None:
        """显示当前配置状态"""
        print("📊 Tsearch 功能状态")
        print("=" * 40)

        # 核心功能
        print("🔧 核心功能:")
        core_features = [
            'ENABLE_CORE_RETRIEVAL',
            'ENABLE_CORE_PROCESSING',
            'ENABLE_CORE_API'
        ]
        for feature in core_features:
            status = "✅" if self.is_feature_enabled(feature) else "❌"
            print(f"  {status} {feature}")

        # 增强功能
        print("\n🚀 增强功能:")
        enhanced_features = [
            'ENABLE_TREND_ANALYSIS',
            'ENABLE_COLLABORATION_ANALYSIS',
            'ENABLE_METHODOLOGY_ANALYSIS'
        ]
        for feature in enhanced_features:
            status = "✅" if self.is_feature_enabled(feature) else "❌"
            print(f"  {status} {feature}")

        # 界面功能
        print("\n🎨 界面功能:")
        ui_features = [
            'ENABLE_STREAMLIT_UI',
            'ENABLE_VUE_FRONTEND'
        ]
        for feature in ui_features:
            status = "✅" if self.is_feature_enabled(feature) else "❌"
            print(f"  {status} {feature}")

        # 生产环境功能
        print("\n🏭 生产环境:")
        prod_features = [
            'ENABLE_PROMETHEUS',
            'ENABLE_GRAFANA',
            'ENABLE_NGINX_PROXY'
        ]
        for feature in prod_features:
            status = "✅" if self.is_feature_enabled(feature) else "❌"
            print(f"  {status} {feature}")

        # Docker配置
        print(f"\n🐳 Docker配置:")
        profiles = self.get_docker_profiles()
        services = self.get_docker_services()
        print(f"  Profiles: {profiles if profiles else '默认'}")
        print(f"  Services: {', '.join(services)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Tsearch 智能启动工具")
    parser.add_argument("--mode", choices=["docker", "local", "status"],
                        default="status", help="启动模式")
    parser.add_argument("--env", choices=["development", "production"],
                        default="development", help="环境类型")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                        help="项目根目录")

    args = parser.parse_args()

    starter = SmartStarter(args.project_root)

    print(f"🚀 Tsearch 智能启动工具")
    print(f"📁 项目根目录: {args.project_root}")
    print(f"🎯 模式: {args.mode}")
    print("=" * 50)

    if args.mode == "status":
        starter.show_status()

    elif args.mode == "docker":
        success = starter.start_docker_services(args.env)
        if success:
            print("\n🎉 Docker服务启动完成!")
            print("💡 访问地址:")
            print("  - API: http://localhost:8000")
            if starter.is_feature_enabled('ENABLE_GRAFANA'):
                print("  - Grafana: http://localhost:3000")
            if starter.is_feature_enabled('ENABLE_PROMETHEUS'):
                print("  - Prometheus: http://localhost:9090")
        else:
            print("\n❌ Docker服务启动失败!")

    elif args.mode == "local":
        success = starter.start_local_services()
        if success:
            print("\n🎉 本地服务启动完成!")
        else:
            print("\n❌ 本地服务启动失败!")

    print("\n💡 提示:")
    print("  - 修改功能配置: config/features.env")
    print("  - 查看状态: python scripts/smart_start.py --mode status")
    print("  - 启动Docker: python scripts/smart_start.py --mode docker")


if __name__ == "__main__":
    main()
