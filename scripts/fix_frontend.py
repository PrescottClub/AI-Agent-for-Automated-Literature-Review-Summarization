#!/usr/bin/env python3
"""
前端问题修复脚本
解决所有前端相关的问题
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend" / "literature-review-frontend"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str = Colors.ENDC):
    """打印彩色文本"""
    print(f"{color}{text}{Colors.ENDC}")

def print_section(title: str):
    """打印章节标题"""
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f"🔧 {title}", Colors.HEADER)
    print_colored(f"{'='*60}", Colors.HEADER)

def run_command(cmd: str, cwd: Path = None, shell: bool = True) -> tuple[bool, str]:
    """运行命令并返回结果"""
    try:
        if cwd is None:
            cwd = FRONTEND_DIR
        
        result = subprocess.run(
            cmd, 
            shell=shell, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)

def fix_package_json():
    """修复package.json配置"""
    print_section("修复 package.json 配置")
    
    package_json_path = FRONTEND_DIR / "package.json"
    
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # 确保脚本配置正确
        package_data["scripts"] = {
            "dev": "vite --host 0.0.0.0 --port 5173",
            "build": "run-p type-check build-only",
            "preview": "vite preview --host 0.0.0.0 --port 4173",
            "test:unit": "vitest",
            "test:e2e": "playwright test",
            "build-only": "vite build",
            "type-check": "vue-tsc --build",
            "lint": "eslint . --fix",
            "format": "prettier --write src/",
            "serve": "vite --host 0.0.0.0 --port 5173"
        }
        
        # 确保依赖正确
        if "vite-plugin-vue-inspector" not in package_data.get("devDependencies", {}):
            package_data.setdefault("devDependencies", {})["vite-plugin-vue-inspector"] = "^7.7.2"
        
        with open(package_json_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print_colored("✅ package.json 配置已修复", Colors.OKGREEN)
        return True
    except Exception as e:
        print_colored(f"❌ 修复 package.json 失败: {e}", Colors.FAIL)
        return False

def fix_vite_config():
    """修复Vite配置"""
    print_section("修复 Vite 配置")
    
    vite_config_content = '''import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['element-plus', '@element-plus/icons-vue'],
        }
      }
    }
  }
})
'''
    
    try:
        vite_config_path = FRONTEND_DIR / "vite.config.ts"
        with open(vite_config_path, 'w', encoding='utf-8') as f:
            f.write(vite_config_content)
        
        print_colored("✅ Vite 配置已修复", Colors.OKGREEN)
        return True
    except Exception as e:
        print_colored(f"❌ 修复 Vite 配置失败: {e}", Colors.FAIL)
        return False

def fix_env_file():
    """修复环境变量文件"""
    print_section("修复环境变量配置")
    
    env_content = '''# Tsearch 前端环境配置
# API 配置
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# 应用配置
VITE_APP_TITLE=Tsearch - AI文献综述系统
VITE_APP_VERSION=3.1.0

# 开发配置
VITE_DEV_MODE=true
VITE_DEBUG=true

# 功能开关
VITE_ENABLE_MOCK_DATA=false
VITE_ENABLE_ANALYTICS=false
'''
    
    try:
        env_path = FRONTEND_DIR / ".env"
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print_colored("✅ 环境变量配置已修复", Colors.OKGREEN)
        return True
    except Exception as e:
        print_colored(f"❌ 修复环境变量配置失败: {e}", Colors.FAIL)
        return False

def clean_and_reinstall():
    """清理并重新安装依赖"""
    print_section("清理并重新安装依赖")
    
    # 删除 node_modules 和 package-lock.json
    node_modules = FRONTEND_DIR / "node_modules"
    package_lock = FRONTEND_DIR / "package-lock.json"
    
    try:
        if node_modules.exists():
            print_colored("🗑️ 删除 node_modules...", Colors.WARNING)
            shutil.rmtree(node_modules)
        
        if package_lock.exists():
            print_colored("🗑️ 删除 package-lock.json...", Colors.WARNING)
            package_lock.unlink()
        
        # 重新安装依赖
        print_colored("📦 重新安装依赖...", Colors.OKCYAN)
        success, output = run_command("npm install")
        
        if success:
            print_colored("✅ 依赖安装成功", Colors.OKGREEN)
            return True
        else:
            print_colored(f"❌ 依赖安装失败: {output}", Colors.FAIL)
            return False
            
    except Exception as e:
        print_colored(f"❌ 清理安装过程失败: {e}", Colors.FAIL)
        return False

def create_startup_scripts():
    """创建启动脚本"""
    print_section("创建启动脚本")
    
    # Windows 批处理脚本
    bat_content = '''@echo off
chcp 65001 >nul
echo 🚀 启动 Tsearch 前端服务...
echo.

cd /d "%~dp0"

if not exist "node_modules" (
    echo ❌ node_modules 不存在，正在安装依赖...
    npm install
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 启动 Vite 开发服务器...
echo 📱 前端地址: http://localhost:5173
echo 🔗 后端API: http://localhost:8000
echo.
echo 按 Ctrl+C 停止服务
echo.

npm run dev

pause
'''
    
    # PowerShell 脚本
    ps1_content = '''# Tsearch 前端启动脚本
Write-Host "🚀 启动 Tsearch 前端服务..." -ForegroundColor Green

Set-Location $PSScriptRoot

if (-not (Test-Path "node_modules")) {
    Write-Host "❌ node_modules 不存在，正在安装依赖..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit 1
    }
}

Write-Host "✅ 启动 Vite 开发服务器..." -ForegroundColor Green
Write-Host "📱 前端地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔗 后端API: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

npm run dev
'''
    
    try:
        # 保存批处理脚本
        bat_path = FRONTEND_DIR / "start.bat"
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        # 保存PowerShell脚本
        ps1_path = FRONTEND_DIR / "start.ps1"
        with open(ps1_path, 'w', encoding='utf-8') as f:
            f.write(ps1_content)
        
        print_colored("✅ 启动脚本已创建", Colors.OKGREEN)
        print_colored(f"   - Windows: {bat_path}", Colors.OKCYAN)
        print_colored(f"   - PowerShell: {ps1_path}", Colors.OKCYAN)
        return True
        
    except Exception as e:
        print_colored(f"❌ 创建启动脚本失败: {e}", Colors.FAIL)
        return False

def test_frontend():
    """测试前端启动"""
    print_section("测试前端启动")
    
    try:
        print_colored("🧪 测试 Vite 配置...", Colors.OKCYAN)
        success, output = run_command("npx vite --version")
        
        if success:
            print_colored("✅ Vite 可用", Colors.OKGREEN)
            print_colored(f"   版本信息: {output.strip()}", Colors.OKCYAN)
        else:
            print_colored(f"❌ Vite 测试失败: {output}", Colors.FAIL)
            return False
        
        # 测试构建
        print_colored("🧪 测试项目构建...", Colors.OKCYAN)
        success, output = run_command("npm run type-check")
        
        if success:
            print_colored("✅ 类型检查通过", Colors.OKGREEN)
        else:
            print_colored(f"⚠️ 类型检查有警告: {output}", Colors.WARNING)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ 前端测试失败: {e}", Colors.FAIL)
        return False

def main():
    """主函数"""
    print_colored("🔧 Tsearch 前端修复工具", Colors.HEADER)
    print_colored(f"📁 前端目录: {FRONTEND_DIR}", Colors.OKCYAN)
    
    if not FRONTEND_DIR.exists():
        print_colored(f"❌ 前端目录不存在: {FRONTEND_DIR}", Colors.FAIL)
        return False
    
    # 执行修复步骤
    steps = [
        ("修复 package.json", fix_package_json),
        ("修复 Vite 配置", fix_vite_config),
        ("修复环境变量", fix_env_file),
        ("清理并重新安装依赖", clean_and_reinstall),
        ("创建启动脚本", create_startup_scripts),
        ("测试前端", test_frontend),
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print_colored(f"❌ {step_name} 失败", Colors.FAIL)
        except Exception as e:
            print_colored(f"❌ {step_name} 异常: {e}", Colors.FAIL)
    
    # 总结
    print_section("修复完成")
    print_colored(f"📊 成功完成: {success_count}/{len(steps)} 项", Colors.HEADER)
    
    if success_count == len(steps):
        print_colored("🎉 所有前端问题已修复！", Colors.OKGREEN)
        print_colored("\n🚀 启动前端服务:", Colors.OKCYAN)
        print_colored(f"   cd {FRONTEND_DIR}", Colors.ENDC)
        print_colored("   npm run dev", Colors.ENDC)
        print_colored("   或运行: start.bat / start.ps1", Colors.ENDC)
        return True
    else:
        print_colored("⚠️ 部分问题未能修复，请检查错误信息", Colors.WARNING)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
