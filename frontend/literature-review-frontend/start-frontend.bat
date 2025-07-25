@echo off
echo 🚀 启动 Tsearch 前端服务...
echo.

REM 切换到当前目录
cd /d "%~dp0"

REM 检查 node_modules 是否存在
if not exist "node_modules" (
    echo ❌ node_modules 不存在，正在安装依赖...
    npm install
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动开发服务器
echo ✅ 启动 Vite 开发服务器...
echo 📱 前端地址: http://localhost:5173
echo 🔗 后端API: http://localhost:8000
echo.
echo 按 Ctrl+C 停止服务
echo.

node_modules\.bin\vite.cmd

pause
