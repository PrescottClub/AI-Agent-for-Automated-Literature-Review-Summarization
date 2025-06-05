# Tsearch 快速启动指南

## 🚀 项目概述

Tsearch 是一个基于 AI 的智能文献综述与摘要生成系统，经过全面优化后具备以下特性：

- 🔬 **智能文献检索**: 支持 arXiv、Semantic Scholar 等多数据源
- 🤖 **AI 驱动分析**: 基于大语言模型的智能摘要和分析
- 🎨 **现代化界面**: Vue3 前端 + FastAPI 后端
- 🐳 **容器化部署**: Docker 一键部署，支持生产环境
- ⚡ **性能优化**: 缓存系统和性能监控
- 🎛️ **功能模块化**: 灵活的功能开关控制

## 📋 快速开始

### 1. 环境准备

#### 系统要求
- Python 3.9+
- Node.js 18+ (用于前端构建)
- Docker & Docker Compose (推荐)

#### 克隆项目
```bash
git clone https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization
```

### 2. 配置设置

#### 复制配置文件
```bash
cp config/config.example.env .env
```

#### 编辑配置文件
```bash
vim .env
```

**必需配置**:
```env
# DeepSeek API (推荐)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# OpenAI API (用于嵌入)
OPENAI_API_KEY=your_openai_api_key_here

# 可选：Semantic Scholar API (提高速率限制)
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here
```

### 3. 启动方式选择

#### 🐳 方式一：Docker 部署 (推荐)

**开发环境**:
```bash
python scripts/smart_start.py --mode docker --env development
```

**生产环境**:
```bash
python scripts/smart_start.py --mode docker --env production
```

#### 💻 方式二：本地开发

**安装依赖**:
```bash
pip install -e .
python -m spacy download en_core_web_sm
```

**启动服务**:
```bash
python scripts/smart_start.py --mode local
```

### 4. 访问应用

启动成功后，可通过以下地址访问：

- **主应用**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **Streamlit 界面**: http://localhost:8501 (如果启用)
- **Grafana 监控**: http://localhost:3000 (生产环境)

## 🎛️ 功能配置

### 查看功能状态
```bash
python scripts/smart_start.py --mode status
```

### 自定义功能开关
编辑 `config/features.env`:

```env
# 核心功能 (不可禁用)
ENABLE_CORE_RETRIEVAL=true
ENABLE_CORE_PROCESSING=true
ENABLE_CORE_API=true

# 增强功能 (可选)
ENABLE_TREND_ANALYSIS=true
ENABLE_COLLABORATION_ANALYSIS=true
ENABLE_METHODOLOGY_ANALYSIS=true

# 界面功能
ENABLE_STREAMLIT_UI=true
ENABLE_VUE_FRONTEND=true

# 协议支持
ENABLE_MCP_SERVER=false
ENABLE_CLI_INTERFACE=true

# 监控功能 (生产环境)
ENABLE_PROMETHEUS=false
ENABLE_GRAFANA=false
ENABLE_NGINX_PROXY=false
```

## 🔧 常用操作

### 项目健康检查
```bash
python scripts/health_check.py
```

### 项目优化分析
```bash
# 分析项目结构
python scripts/optimize_project.py --action analyze

# 生成优化报告
python scripts/optimize_project.py --action report
```

### 使用 CLI 工具
```bash
# 查看帮助
tsearch --help

# 执行文献综述
tsearch review "machine learning in healthcare" --max-papers 20
```

### 使用 API
```python
import requests

# 执行文献综述
response = requests.post("http://localhost:8000/api/v1/literature-review", json={
    "raw_query": "深度学习在医疗诊断中的应用",
    "max_papers": 20,
    "sources": ["arxiv", "semantic_scholar"]
})

results = response.json()
```

## 🛠️ 开发指南

### 项目结构
```
src/lit_review_agent/
├── agent.py              # 核心代理
├── api_server.py         # FastAPI 服务器
├── app.py               # Streamlit 界面
├── cli.py               # 命令行工具
├── mcp_server.py        # MCP 协议服务器
├── ai_core/             # AI 核心功能
├── processing/          # 文本处理
├── retrieval/           # 文献检索
└── utils/               # 工具模块
```

### 添加新功能
1. 在相应模块中实现功能
2. 在 `config/features.env` 中添加功能开关
3. 在 `scripts/smart_start.py` 中添加启动逻辑
4. 更新文档和测试

### 性能监控
```python
from src.lit_review_agent.utils.performance_monitor import monitor_performance

@monitor_performance
def my_function():
    # 函数逻辑
    pass
```

### 缓存使用
```python
from src.lit_review_agent.utils.cache_manager import cache_api_response

@cache_api_response
def api_call():
    # API 调用逻辑
    pass
```

## 🐛 故障排除

### 常见问题

**1. API 密钥错误**
- 检查 `.env` 文件中的 API 密钥是否正确
- 确保 API 密钥有足够的配额

**2. Docker 启动失败**
- 检查 Docker 是否正在运行
- 确保端口 8000, 6379, 8001 未被占用

**3. 依赖安装失败**
- 确保 Python 版本 >= 3.9
- 尝试使用虚拟环境

**4. 前端构建失败**
- 确保 Node.js 版本 >= 18
- 检查网络连接，可能需要配置 npm 镜像

### 获取帮助

**健康检查**:
```bash
python scripts/health_check.py
```

**查看日志**:
```bash
# Docker 日志
docker-compose logs -f literature-review-app

# 本地日志
tail -f logs/app.log
```

**重置环境**:
```bash
# 清理 Docker 环境
docker-compose down -v
docker system prune -f

# 重新启动
python scripts/smart_start.py --mode docker
```

## 📚 更多资源

- **详细文档**: [docs/optimization_summary.md](optimization_summary.md)
- **API 文档**: http://localhost:8000/docs
- **项目仓库**: https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization
- **问题反馈**: GitHub Issues

---

🎉 **恭喜！** 您已成功启动 Tsearch 系统。开始您的智能文献综述之旅吧！
