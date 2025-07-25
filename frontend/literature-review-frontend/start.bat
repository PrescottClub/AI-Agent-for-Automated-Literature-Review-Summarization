@echo off
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

REM 直接使用node运行vite，避免路径问题
node node_modules\vite\bin\vite.js --host 0.0.0.0 --port 5173

pause
