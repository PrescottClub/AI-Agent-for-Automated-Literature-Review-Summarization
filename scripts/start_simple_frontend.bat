@echo off
echo 🚀 启动简单前端界面...
cd "frontend\simple-frontend"
echo 正在启动Python HTTP服务器...
echo 请在浏览器中访问: http://localhost:8080
python -m http.server 8080
pause 