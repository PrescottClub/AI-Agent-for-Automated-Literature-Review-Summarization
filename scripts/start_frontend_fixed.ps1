# 前端启动脚本 - 修复路径问题版本
Write-Host "🚀 启动前端开发服务器..." -ForegroundColor Green
Write-Host ""

# 获取脚本所在目录的父目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$frontendDir = Join-Path $projectRoot "frontend\literature-review-frontend"

Write-Host "📍 项目根目录: $projectRoot" -ForegroundColor Cyan
Write-Host "📍 前端目录: $frontendDir" -ForegroundColor Cyan
Write-Host ""

# 切换到前端目录
Set-Location $frontendDir

# 检查依赖
if (-not (Test-Path "node_modules")) {
    Write-Host "❌ node_modules 不存在，正在安装依赖..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败！" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit 1
    }
}

Write-Host "✅ 依赖检查完成" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 启动 Vite 开发服务器..." -ForegroundColor Green
Write-Host "📱 前端将在 http://localhost:5173 启动" -ForegroundColor Cyan
Write-Host ""

# 启动开发服务器
& node "./node_modules/vite/bin/vite.js"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ 前端启动失败！" -ForegroundColor Red
    Write-Host "💡 可能的解决方案：" -ForegroundColor Yellow
    Write-Host "   1. 检查 Node.js 是否正确安装" -ForegroundColor White
    Write-Host "   2. 删除 node_modules 文件夹并重新运行 npm install" -ForegroundColor White
    Write-Host "   3. 检查端口 5173 是否被占用" -ForegroundColor White
    Read-Host "按任意键退出"
    exit 1
}
