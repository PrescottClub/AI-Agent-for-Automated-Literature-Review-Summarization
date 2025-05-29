@echo off
echo 🚀 启动前端开发服务器...
echo.

cd /d "%~dp0\..\frontend\literature-review-frontend"

echo 📍 当前目录: %CD%
echo.

echo 🔍 检查依赖...
if not exist "node_modules" (
    echo ❌ node_modules 不存在，正在安装依赖...
    npm install
    if errorlevel 1 (
        echo ❌ 依赖安装失败！
        pause
        exit /b 1
    )
)

echo ✅ 依赖检查完成
echo.

echo 🌐 启动 Vite 开发服务器...
echo 📱 前端将在 http://localhost:5173 启动
echo.

node "./node_modules/vite/bin/vite.js"

if errorlevel 1 (
    echo.
    echo ❌ 前端启动失败！
    echo 💡 可能的解决方案：
    echo    1. 检查 Node.js 是否正确安装
    echo    2. 删除 node_modules 文件夹并重新运行 npm install
    echo    3. 检查端口 5173 是否被占用
    pause
    exit /b 1
)
