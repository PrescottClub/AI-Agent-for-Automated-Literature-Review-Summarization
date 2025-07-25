# Tsearch 前端启动脚本
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
