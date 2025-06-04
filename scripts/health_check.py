#!/usr/bin/env python3
"""
Tsearch 项目健康检查脚本
检查项目的各个组件是否正常工作
"""

import sys
import os
import subprocess
import importlib
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class HealthChecker:
    """项目健康检查器"""

    def __init__(self):
        self.project_root = project_root
        self.results = {
            "overall_status": "unknown",
            "checks": {},
            "warnings": [],
            "errors": [],
            "recommendations": []
        }

    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有健康检查"""
        print("🔍 开始 Tsearch 项目健康检查...")
        print("=" * 50)

        # 检查项目结构
        self.check_project_structure()

        # 检查Python依赖
        self.check_python_dependencies()

        # 检查Python语法
        self.check_python_syntax()

        # 检查配置文件
        self.check_configuration()

        # 检查前端依赖
        self.check_frontend_dependencies()

        # 检查数据目录
        self.check_data_directories()

        # 检查核心模块导入
        self.check_core_imports()

        # 运行性能基准测试
        self.run_performance_benchmark()

        # 生成总体状态
        self.generate_overall_status()

        # 输出结果
        self.print_results()

        return self.results

    def check_project_structure(self):
        """检查项目结构"""
        print("📁 检查项目结构...")

        required_dirs = [
            "src/lit_review_agent",
            "frontend/literature-review-frontend",
            "config",
            "data",
            "scripts",
            "tests"
        ]

        required_files = [
            "pyproject.toml",
            "README.md",
            "config/config.example.env",
            "src/lit_review_agent/__init__.py",
            "src/lit_review_agent/agent.py",
            "src/lit_review_agent/api_server.py"
        ]

        missing_dirs = []
        missing_files = []

        for dir_path in required_dirs:
            if not (self.project_root / dir_path).exists():
                missing_dirs.append(dir_path)

        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)

        status = "pass" if not missing_dirs and not missing_files else "fail"

        self.results["checks"]["project_structure"] = {
            "status": status,
            "missing_directories": missing_dirs,
            "missing_files": missing_files
        }

        if missing_dirs:
            self.results["errors"].append(f"缺少目录: {', '.join(missing_dirs)}")
        if missing_files:
            self.results["errors"].append(f"缺少文件: {', '.join(missing_files)}")

        print(f"   ✅ 项目结构检查: {status.upper()}")

    def check_python_dependencies(self):
        """检查Python依赖"""
        print("📦 检查Python依赖...")

        try:
            # 检查pyproject.toml
            pyproject_path = self.project_root / "pyproject.toml"
            if not pyproject_path.exists():
                self.results["checks"]["python_dependencies"] = {
                    "status": "fail",
                    "error": "pyproject.toml not found"
                }
                self.results["errors"].append("未找到 pyproject.toml 文件")
                return

            # 尝试导入关键依赖
            critical_packages = [
                "fastapi",
                "uvicorn",
                "chromadb",
                "sentence_transformers",
                "openai",
                "arxiv",
                "requests",
                "pydantic"
            ]

            missing_packages = []
            for package in critical_packages:
                try:
                    importlib.import_module(package)
                except ImportError:
                    missing_packages.append(package)

            status = "pass" if not missing_packages else "fail"

            self.results["checks"]["python_dependencies"] = {
                "status": status,
                "missing_packages": missing_packages,
                "checked_packages": critical_packages
            }

            if missing_packages:
                self.results["errors"].append(
                    f"缺少Python包: {', '.join(missing_packages)}")
                self.results["recommendations"].append(
                    "运行 'pip install -e .' 安装依赖")

            print(f"   ✅ Python依赖检查: {status.upper()}")

        except Exception as e:
            self.results["checks"]["python_dependencies"] = {
                "status": "error",
                "error": str(e)
            }
            self.results["errors"].append(f"Python依赖检查失败: {e}")
            print(f"   ❌ Python依赖检查: ERROR")

    def check_python_syntax(self):
        """检查Python语法"""
        print("🐍 检查Python语法...")

        python_files = []
        src_dir = self.project_root / "src"
        if src_dir.exists():
            python_files.extend(src_dir.rglob("*.py"))

        scripts_dir = self.project_root / "scripts"
        if scripts_dir.exists():
            python_files.extend(scripts_dir.rglob("*.py"))

        syntax_errors = []

        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: {e}")
            except Exception as e:
                # 忽略其他类型的错误（如导入错误）
                pass

        status = "pass" if not syntax_errors else "fail"

        self.results["checks"]["python_syntax"] = {
            "status": status,
            "files_checked": len(python_files),
            "syntax_errors": syntax_errors
        }

        if syntax_errors:
            self.results["errors"].extend(syntax_errors)

        print(f"   ✅ Python语法检查: {status.upper()} ({len(python_files)} 文件)")

    def check_configuration(self):
        """检查配置文件"""
        print("⚙️  检查配置文件...")

        config_issues = []

        # 检查示例配置文件
        example_config = self.project_root / "config" / "config.example.env"
        if not example_config.exists():
            config_issues.append("缺少 config.example.env 文件")

        # 检查是否有实际配置文件
        config_files = [
            self.project_root / "config" / "config.env",
            self.project_root / ".env"
        ]

        has_config = any(f.exists() for f in config_files)
        if not has_config:
            self.results["warnings"].append(
                "未找到配置文件，请复制 config.example.env 并配置")

        status = "pass" if not config_issues else "fail"

        self.results["checks"]["configuration"] = {
            "status": status,
            "has_config_file": has_config,
            "issues": config_issues
        }

        if config_issues:
            self.results["errors"].extend(config_issues)

        print(f"   ✅ 配置文件检查: {status.upper()}")

    def check_frontend_dependencies(self):
        """检查前端依赖"""
        print("🌐 检查前端依赖...")

        frontend_dir = self.project_root / "frontend" / "literature-review-frontend"

        if not frontend_dir.exists():
            self.results["checks"]["frontend_dependencies"] = {
                "status": "fail",
                "error": "前端目录不存在"
            }
            self.results["errors"].append("前端目录不存在")
            return

        package_json = frontend_dir / "package.json"
        node_modules = frontend_dir / "node_modules"

        issues = []

        if not package_json.exists():
            issues.append("缺少 package.json")

        if not node_modules.exists():
            self.results["warnings"].append("前端依赖未安装，请运行 'npm install'")

        status = "pass" if not issues else "fail"

        self.results["checks"]["frontend_dependencies"] = {
            "status": status,
            "has_package_json": package_json.exists(),
            "has_node_modules": node_modules.exists(),
            "issues": issues
        }

        if issues:
            self.results["errors"].extend(issues)

        print(f"   ✅ 前端依赖检查: {status.upper()}")

    def check_data_directories(self):
        """检查数据目录"""
        print("💾 检查数据目录...")

        data_dirs = [
            "data",
            "data/cache",
            "data/vector_store",
            "data/reports"
        ]

        created_dirs = []

        for dir_path in data_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(dir_path)
                except Exception as e:
                    self.results["errors"].append(f"无法创建目录 {dir_path}: {e}")

        self.results["checks"]["data_directories"] = {
            "status": "pass",
            "created_directories": created_dirs
        }

        if created_dirs:
            print(f"   ✅ 数据目录检查: PASS (创建了 {len(created_dirs)} 个目录)")
        else:
            print(f"   ✅ 数据目录检查: PASS")

    def check_core_imports(self):
        """检查核心模块导入"""
        print("🔧 检查核心模块导入...")

        import_errors = []

        try:
            from src.lit_review_agent.utils.config import Config
        except Exception as e:
            import_errors.append(f"Config: {e}")

        try:
            from src.lit_review_agent.agent import LiteratureAgent
        except Exception as e:
            import_errors.append(f"LiteratureAgent: {e}")

        try:
            from src.lit_review_agent.api_server import app
        except Exception as e:
            import_errors.append(f"API Server: {e}")

        status = "pass" if not import_errors else "fail"

        self.results["checks"]["core_imports"] = {
            "status": status,
            "import_errors": import_errors
        }

        if import_errors:
            self.results["errors"].extend(import_errors)

        print(f"   ✅ 核心模块导入检查: {status.upper()}")

    def run_performance_benchmark(self):
        """运行性能基准测试"""
        print("⚡ 运行性能基准测试...")

        benchmark_results = {}

        try:
            import time

            # 测试配置加载时间
            start_time = time.time()
            try:
                from src.lit_review_agent.utils.config import Config
                config = Config()
                config_load_time = time.time() - start_time
                benchmark_results["config_load_time"] = config_load_time
            except Exception as e:
                benchmark_results["config_load_error"] = str(e)

            # 测试缓存管理器初始化
            start_time = time.time()
            try:
                from src.lit_review_agent.utils.cache_manager import CacheManager
                cache_manager = CacheManager()
                cache_init_time = time.time() - start_time
                benchmark_results["cache_init_time"] = cache_init_time
            except Exception as e:
                benchmark_results["cache_init_error"] = str(e)

            # 测试性能监控器初始化
            start_time = time.time()
            try:
                from src.lit_review_agent.utils.performance_monitor import PerformanceMonitor
                perf_monitor = PerformanceMonitor(
                    enable_system_monitoring=False)
                perf_init_time = time.time() - start_time
                benchmark_results["performance_monitor_init_time"] = perf_init_time
            except Exception as e:
                benchmark_results["performance_monitor_error"] = str(e)

            # 评估性能
            performance_issues = []
            if "config_load_time" in benchmark_results and benchmark_results["config_load_time"] > 1.0:
                performance_issues.append("配置加载时间过长")

            if "cache_init_time" in benchmark_results and benchmark_results["cache_init_time"] > 0.5:
                performance_issues.append("缓存管理器初始化时间过长")

            status = "pass" if not performance_issues else "warning"

            self.results["checks"]["performance_benchmark"] = {
                "status": status,
                "benchmark_results": benchmark_results,
                "performance_issues": performance_issues
            }

            if performance_issues:
                self.results["warnings"].extend(performance_issues)

            print(f"   ✅ 性能基准测试: {status.upper()}")

        except Exception as e:
            self.results["checks"]["performance_benchmark"] = {
                "status": "error",
                "error": str(e)
            }
            self.results["errors"].append(f"性能基准测试失败: {e}")
            print(f"   ❌ 性能基准测试: ERROR")

    def generate_overall_status(self):
        """生成总体状态"""
        failed_checks = [
            name for name, check in self.results["checks"].items()
            if check["status"] == "fail"
        ]

        error_checks = [
            name for name, check in self.results["checks"].items()
            if check["status"] == "error"
        ]

        if error_checks or failed_checks:
            self.results["overall_status"] = "unhealthy"
        elif self.results["warnings"]:
            self.results["overall_status"] = "warning"
        else:
            self.results["overall_status"] = "healthy"

    def print_results(self):
        """打印检查结果"""
        print("\n" + "=" * 50)
        print("📊 健康检查结果")
        print("=" * 50)

        # 总体状态
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "unhealthy": "❌"
        }

        status_text = {
            "healthy": "健康",
            "warning": "有警告",
            "unhealthy": "不健康"
        }

        overall = self.results["overall_status"]
        print(f"总体状态: {status_emoji[overall]} {status_text[overall]}")

        # 详细检查结果
        print(f"\n检查详情:")
        for name, check in self.results["checks"].items():
            status = check["status"]
            emoji = "✅" if status == "pass" else "❌" if status == "fail" else "⚠️"
            print(f"  {emoji} {name}: {status.upper()}")

        # 错误
        if self.results["errors"]:
            print(f"\n❌ 错误 ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"  • {error}")

        # 警告
        if self.results["warnings"]:
            print(f"\n⚠️  警告 ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"  • {warning}")

        # 建议
        if self.results["recommendations"]:
            print(f"\n💡 建议:")
            for rec in self.results["recommendations"]:
                print(f"  • {rec}")

        print("\n" + "=" * 50)


def main():
    """主函数"""
    checker = HealthChecker()
    results = checker.run_all_checks()

    # 保存结果到文件
    results_file = project_root / "data" / "health_check_results.json"
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 详细结果已保存到: {results_file}")
    except Exception as e:
        print(f"⚠️  无法保存结果文件: {e}")

    # 返回适当的退出码
    if results["overall_status"] == "unhealthy":
        sys.exit(1)
    elif results["overall_status"] == "warning":
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
