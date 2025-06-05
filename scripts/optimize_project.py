#!/usr/bin/env python3
"""
Tsearch 项目优化脚本
根据分析报告建议优化项目结构和配置
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Any
import argparse


class ProjectOptimizer:
    """项目优化器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backup_dir = project_root / "backups"
        
    def create_backup(self, files: List[Path]) -> None:
        """创建文件备份"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
            
        for file_path in files:
            if file_path.exists():
                backup_path = self.backup_dir / file_path.name
                shutil.copy2(file_path, backup_path)
                print(f"✅ 备份文件: {file_path} -> {backup_path}")
    
    def optimize_docker_config(self) -> None:
        """优化 Docker 配置"""
        print("🐳 优化 Docker 配置...")
        
        # 检查 Dockerfile 是否已优化
        dockerfile = self.project_root / "Dockerfile"
        if dockerfile.exists():
            content = dockerfile.read_text()
            if "pyproject.toml" in content and "requirements.txt" not in content:
                print("✅ Dockerfile 已优化 (使用 pyproject.toml)")
            else:
                print("⚠️  Dockerfile 需要手动优化")
        
        # 检查 docker-compose.yml 配置
        compose_file = self.project_root / "docker-compose.yml"
        if compose_file.exists():
            content = compose_file.read_text()
            if "${UVICORN_WORKERS:-1}" in content:
                print("✅ docker-compose.yml 已优化 (参数化配置)")
            else:
                print("⚠️  docker-compose.yml 需要手动优化")
    
    def analyze_non_core_modules(self) -> Dict[str, Dict[str, Any]]:
        """分析非核心模块"""
        modules = {
            "trend_analyzer": {
                "path": "src/lit_review_agent/ai_core/trend_analyzer.py",
                "description": "趋势分析功能 - 增强功能，非核心",
                "core": False,
                "size_kb": 0,
                "dependencies": ["llm_manager", "text_processor"]
            },
            "streamlit_app": {
                "path": "src/lit_review_agent/app.py", 
                "description": "Streamlit Web界面 - 与Vue3前端重合",
                "core": False,
                "size_kb": 0,
                "dependencies": ["streamlit", "agent"]
            },
            "mcp_server": {
                "path": "src/lit_review_agent/mcp_server.py",
                "description": "MCP协议服务器 - 特定工具链支持",
                "core": False,
                "size_kb": 0,
                "dependencies": ["mcp", "agent"]
            }
        }
        
        # 计算文件大小
        for module_name, info in modules.items():
            file_path = self.project_root / info["path"]
            if file_path.exists():
                info["size_kb"] = round(file_path.stat().st_size / 1024, 2)
                info["exists"] = True
            else:
                info["exists"] = False
                
        return modules
    
    def create_feature_flags(self) -> None:
        """创建功能开关配置"""
        print("🎛️  创建功能开关配置...")
        
        feature_config = """# Tsearch 功能开关配置
# ================================

# 核心功能 (不可禁用)
ENABLE_CORE_RETRIEVAL=true
ENABLE_CORE_PROCESSING=true
ENABLE_CORE_API=true

# 增强功能 (可选)
ENABLE_TREND_ANALYSIS=true
ENABLE_COLLABORATION_ANALYSIS=true
ENABLE_METHODOLOGY_ANALYSIS=true

# 界面功能
ENABLE_STREAMLIT_UI=true
ENABLE_VUE_FRONTEND=true

# 协议支持
ENABLE_MCP_SERVER=false
ENABLE_CLI_INTERFACE=true

# 监控功能 (生产环境)
ENABLE_PROMETHEUS=false
ENABLE_GRAFANA=false
ENABLE_NGINX_PROXY=false

# 开发功能
ENABLE_DEBUG_MODE=false
ENABLE_PERFORMANCE_MONITORING=true
"""
        
        config_path = self.project_root / "config" / "features.env"
        config_path.write_text(feature_config)
        print(f"✅ 功能配置已创建: {config_path}")
    
    def generate_optimization_report(self) -> None:
        """生成优化报告"""
        print("\n📊 生成项目优化报告...")
        
        modules = self.analyze_non_core_modules()
        
        report = f"""# Tsearch 项目优化报告
生成时间: {os.popen('date').read().strip()}

## 项目结构分析

### 核心模块 ✅
- API服务器 (api_server.py)
- 文献检索代理 (agent.py)
- 检索客户端 (retrieval/)
- 文本处理 (processing/)
- 配置管理 (utils/config.py)

### 非核心模块分析
"""
        
        for name, info in modules.items():
            status = "存在" if info["exists"] else "不存在"
            report += f"""
#### {name}
- 路径: {info['path']}
- 状态: {status}
- 大小: {info['size_kb']} KB
- 描述: {info['description']}
- 依赖: {', '.join(info['dependencies'])}
- 建议: {'保留作为可选功能' if info['core'] else '可考虑精简或标记为可选'}
"""
        
        report += f"""
## 优化建议

### 已完成 ✅
- Docker配置优化 (依赖管理、镜像版本固定)
- 环境变量参数化
- 安全配置增强

### 待实施 📋
1. **功能模块化**: 使用功能开关控制非核心功能
2. **配置统一**: 完善配置管理系统
3. **错误处理**: 增强异常处理和恢复机制
4. **性能优化**: 优化LLM交互和缓存策略

### 精简建议 🎯
- 保留所有模块但添加功能开关
- 在生产环境中可选择性禁用非核心功能
- 通过配置文件控制功能启用状态

## 下一步行动
1. 使用功能开关配置 (config/features.env)
2. 根据部署环境选择启用的功能
3. 监控核心功能性能和稳定性
4. 逐步优化非核心功能的实现
"""
        
        report_path = self.project_root / "docs" / "optimization_report.md"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        print(f"✅ 优化报告已生成: {report_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Tsearch 项目优化工具")
    parser.add_argument("--action", choices=["analyze", "optimize", "report"], 
                       default="analyze", help="执行的操作")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                       help="项目根目录")
    
    args = parser.parse_args()
    
    optimizer = ProjectOptimizer(args.project_root)
    
    print(f"🚀 Tsearch 项目优化工具")
    print(f"📁 项目根目录: {args.project_root}")
    print("=" * 50)
    
    if args.action == "analyze":
        print("🔍 分析项目结构...")
        modules = optimizer.analyze_non_core_modules()
        
        print("\n📋 非核心模块分析:")
        for name, info in modules.items():
            status = "✅" if info["exists"] else "❌"
            print(f"{status} {name}: {info['description']} ({info['size_kb']} KB)")
        
        optimizer.optimize_docker_config()
        
    elif args.action == "optimize":
        print("⚙️  执行项目优化...")
        optimizer.create_feature_flags()
        optimizer.optimize_docker_config()
        print("✅ 优化完成!")
        
    elif args.action == "report":
        optimizer.generate_optimization_report()
    
    print("\n🎉 操作完成!")
    print("💡 建议: 查看生成的配置文件和报告，根据需要调整功能开关")


if __name__ == "__main__":
    main()
