#!/usr/bin/env python3
"""
Git 自动提交和推送脚本
自动化处理代码提交、版本标记和推送到GitHub
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

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

def print_header():
    """打印头部信息"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("🚀 AI Literature Review System", Colors.HEADER)
    print_colored("   Git 自动提交和推送工具", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print()

def run_command(command, description=""):
    """运行命令并处理错误"""
    if description:
        print_colored(f"🔄 {description}...", Colors.OKBLUE)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=PROJECT_ROOT
        )
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ 错误: {e}", Colors.FAIL)
        if e.stderr:
            print_colored(f"详细错误: {e.stderr}", Colors.FAIL)
        return False

def check_git_status():
    """检查Git状态"""
    print_colored("🔍 检查Git状态...", Colors.OKBLUE)
    
    # 检查是否在Git仓库中
    if not (PROJECT_ROOT / ".git").exists():
        print_colored("❌ 当前目录不是Git仓库", Colors.FAIL)
        return False
    
    # 检查是否有未提交的更改
    result = subprocess.run(
        "git status --porcelain", 
        shell=True, 
        capture_output=True, 
        text=True,
        cwd=PROJECT_ROOT
    )
    
    if not result.stdout.strip():
        print_colored("✅ 没有未提交的更改", Colors.WARNING)
        return False
    
    print_colored("✅ 发现未提交的更改", Colors.OKGREEN)
    print("更改的文件:")
    for line in result.stdout.strip().split('\n'):
        print(f"  {line}")
    print()
    return True

def get_commit_message():
    """获取提交信息"""
    print_colored("📝 生成提交信息...", Colors.OKBLUE)
    
    # 默认提交信息
    default_message = f"""🚀 v2.0.0 - 全面优化升级

✨ 新功能:
- MCP 协议支持增强 - 新增多个工具和资源
- 前端界面全面优化 - 现代化设计和用户体验
- 高级搜索功能 - 筛选、排序、历史记录
- 实时状态监控 - 后端连接状态显示
- 一键启动脚本 - 简化部署和启动流程

🔧 改进:
- MCP 服务器增强 - 完善参数验证和错误处理
- 前端界面优化 - 响应式设计和交互体验
- 系统稳定性提升 - 错误处理和性能优化
- 文档更新完善 - 使用指南和API文档

🐛 修复:
- 修复TypeScript类型错误
- 修复前端组件导入问题
- 优化配置加载逻辑
- 改进错误处理机制

📚 文档:
- 更新README文档
- 完善MCP使用指南
- 添加一键启动说明
- 优化项目结构说明

提交时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    print_colored("默认提交信息:", Colors.OKCYAN)
    print(default_message)
    print()
    
    choice = input("是否使用默认提交信息? (y/n) [y]: ").strip().lower()
    
    if choice in ['n', 'no']:
        print_colored("请输入自定义提交信息 (按Ctrl+C取消):", Colors.OKBLUE)
        try:
            custom_message = input("提交信息: ").strip()
            if custom_message:
                return custom_message
        except KeyboardInterrupt:
            print_colored("\n❌ 操作已取消", Colors.WARNING)
            return None
    
    return default_message

def create_tag():
    """创建版本标签"""
    tag_name = "v2.0.0"
    tag_message = "AI Literature Review System v2.0.0 - 全面优化升级版本"
    
    print_colored(f"🏷️ 创建版本标签 {tag_name}...", Colors.OKBLUE)
    
    # 检查标签是否已存在
    result = subprocess.run(
        f"git tag -l {tag_name}", 
        shell=True, 
        capture_output=True, 
        text=True,
        cwd=PROJECT_ROOT
    )
    
    if result.stdout.strip():
        print_colored(f"⚠️ 标签 {tag_name} 已存在，跳过创建", Colors.WARNING)
        return True
    
    # 创建标签
    return run_command(
        f'git tag -a {tag_name} -m "{tag_message}"',
        f"创建标签 {tag_name}"
    )

def main():
    """主函数"""
    print_header()
    
    # 切换到项目根目录
    os.chdir(PROJECT_ROOT)
    
    # 检查Git状态
    if not check_git_status():
        print_colored("没有需要提交的更改，退出", Colors.WARNING)
        return
    
    # 获取提交信息
    commit_message = get_commit_message()
    if not commit_message:
        print_colored("❌ 未提供提交信息，退出", Colors.FAIL)
        return
    
    print_colored("🚀 开始Git操作...", Colors.HEADER)
    
    # 添加所有更改
    if not run_command("git add .", "添加所有更改"):
        return
    
    # 提交更改
    if not run_command(f'git commit -m "{commit_message}"', "提交更改"):
        return
    
    # 创建版本标签
    if not create_tag():
        print_colored("⚠️ 标签创建失败，但提交成功", Colors.WARNING)
    
    # 推送到远程仓库
    print_colored("📤 推送到远程仓库...", Colors.OKBLUE)
    
    # 推送代码
    if not run_command("git push origin main", "推送代码到main分支"):
        # 尝试推送到master分支
        if not run_command("git push origin master", "推送代码到master分支"):
            print_colored("❌ 推送失败，请检查远程仓库配置", Colors.FAIL)
            return
    
    # 推送标签
    if not run_command("git push origin --tags", "推送标签"):
        print_colored("⚠️ 标签推送失败", Colors.WARNING)
    
    print_colored("\n🎉 所有操作完成！", Colors.OKGREEN)
    print_colored("✅ 代码已成功提交并推送到GitHub", Colors.OKGREEN)
    print_colored("🏷️ 版本标签已创建", Colors.OKGREEN)
    print_colored("📖 请查看GitHub仓库确认更改", Colors.OKCYAN)
    
    # 显示最新提交信息
    print_colored("\n📋 最新提交信息:", Colors.OKBLUE)
    run_command("git log --oneline -1", "")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n❌ 操作被用户取消", Colors.WARNING)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ 发生未预期的错误: {e}", Colors.FAIL)
        sys.exit(1) 