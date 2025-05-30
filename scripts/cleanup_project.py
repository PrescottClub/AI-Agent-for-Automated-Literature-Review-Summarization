#!/usr/bin/env python3
"""
项目清理脚本
清理不必要的文件和目录，优化项目结构
"""

import os
import shutil
import glob
from pathlib import Path


def cleanup_python_cache():
    """清理Python缓存文件"""
    print("🧹 清理Python缓存文件...")
    
    # 清理__pycache__目录
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            print(f"  删除: {cache_dir}")
            shutil.rmtree(cache_dir)
    
    # 清理.pyc文件
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for file in pyc_files:
        print(f"  删除: {file}")
        os.remove(file)
    
    print("✅ Python缓存清理完成")


def cleanup_logs():
    """清理日志文件"""
    print("🧹 清理日志文件...")
    
    log_patterns = ['**/*.log', '**/logs/*.log', 'logs/*']
    for pattern in log_patterns:
        for file in glob.glob(pattern, recursive=True):
            if os.path.isfile(file):
                print(f"  删除: {file}")
                os.remove(file)
    
    print("✅ 日志文件清理完成")


def cleanup_temp_files():
    """清理临时文件"""
    print("🧹 清理临时文件...")
    
    temp_patterns = [
        '**/*.tmp',
        '**/*.temp',
        '**/*~',
        '**/Thumbs.db',
        '**/.DS_Store'
    ]
    
    for pattern in temp_patterns:
        for file in glob.glob(pattern, recursive=True):
            if os.path.isfile(file):
                print(f"  删除: {file}")
                os.remove(file)
    
    print("✅ 临时文件清理完成")


def cleanup_test_outputs():
    """清理测试输出文件"""
    print("🧹 清理测试输出...")
    
    test_patterns = [
        'test_*.py',  # 根目录的测试文件
        '.pytest_cache',
        '.coverage',
        'htmlcov',
        'coverage.xml'
    ]
    
    for pattern in test_patterns:
        for item in glob.glob(pattern):
            if os.path.isfile(item):
                print(f"  删除文件: {item}")
                os.remove(item)
            elif os.path.isdir(item):
                print(f"  删除目录: {item}")
                shutil.rmtree(item)
    
    print("✅ 测试输出清理完成")


def cleanup_build_artifacts():
    """清理构建产物"""
    print("🧹 清理构建产物...")
    
    build_patterns = [
        'build',
        'dist',
        '*.egg-info',
        '.eggs'
    ]
    
    for pattern in build_patterns:
        for item in glob.glob(pattern):
            if os.path.isdir(item):
                print(f"  删除目录: {item}")
                shutil.rmtree(item)
    
    print("✅ 构建产物清理完成")


def optimize_project_structure():
    """优化项目结构"""
    print("🔧 优化项目结构...")
    
    # 确保必要的目录存在
    required_dirs = [
        'logs',
        'data/outputs',
        'data/chroma_db'
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  确保目录存在: {dir_path}")
    
    # 创建.gitkeep文件保持空目录
    gitkeep_dirs = ['logs', 'data/outputs']
    for dir_path in gitkeep_dirs:
        gitkeep_file = Path(dir_path) / '.gitkeep'
        if not gitkeep_file.exists():
            gitkeep_file.touch()
            print(f"  创建: {gitkeep_file}")
    
    print("✅ 项目结构优化完成")


def check_project_health():
    """检查项目健康状态"""
    print("🔍 检查项目健康状态...")
    
    # 检查关键文件
    critical_files = [
        'requirements.txt',
        'src/lit_review_agent/agent.py',
        'src/lit_review_agent/api_server.py',
        'frontend/literature-review-frontend/package.json',
        'README.md'
    ]
    
    missing_files = []
    for file_path in critical_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print("  ❌ 缺失关键文件:")
        for file_path in missing_files:
            print(f"    - {file_path}")
    
    # 检查目录结构
    critical_dirs = [
        'src/lit_review_agent',
        'frontend/literature-review-frontend',
        'scripts',
        'config'
    ]
    
    missing_dirs = []
    for dir_path in critical_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
        else:
            print(f"  ✅ {dir_path}/")
    
    if missing_dirs:
        print("  ❌ 缺失关键目录:")
        for dir_path in missing_dirs:
            print(f"    - {dir_path}/")
    
    print("✅ 项目健康检查完成")


def main():
    """主函数"""
    print("🚀 开始项目清理和优化...")
    print("=" * 50)
    
    try:
        # 清理操作
        cleanup_python_cache()
        cleanup_logs()
        cleanup_temp_files()
        cleanup_test_outputs()
        cleanup_build_artifacts()
        
        # 优化操作
        optimize_project_structure()
        
        # 健康检查
        check_project_health()
        
        print("=" * 50)
        print("🎉 项目清理和优化完成！")
        print("\n📋 清理总结:")
        print("  ✅ Python缓存文件已清理")
        print("  ✅ 日志文件已清理")
        print("  ✅ 临时文件已清理")
        print("  ✅ 测试输出已清理")
        print("  ✅ 构建产物已清理")
        print("  ✅ 项目结构已优化")
        print("  ✅ 项目健康状态良好")
        
    except Exception as e:
        print(f"❌ 清理过程中出现错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
