# 🔬 AI 智能文献综述与摘要生成系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)

> **智能化文献综述与摘要生成代理 - 让学术研究更高效**

一个基于人工智能的智能代理系统，能够**自动发现、分析和综合**学术文献，为研究人员节省大量时间，并提供任何研究领域的全面洞察。

## ✨ 核心特性

### 🚀 **智能文献检索**
- **多源检索** - 支持 arXiv、Semantic Scholar 等学术数据库
- **语义搜索** - 基于向量相似度的高级语义匹配
- **智能过滤** - 按发表日期、期刊和相关性筛选
- **批量处理** - 支持大规模文献批量检索和处理

### 🧠 **AI 驱动分析**
- **多格式摘要** - 支持执行摘要、关键发现、要点总结
- **趋势识别** - 识别新兴主题和研究热点
- **研究缺口分析** - 发现未来研究机会
- **合作网络洞察** - 作者和机构合作模式分析

### 📊 **全面报告生成**
- **专业报告** - 支持 Markdown、HTML、LaTeX 格式
- **执行摘要** - 为决策者提供简洁概览
- **详细文献综述** - 包含统计分析的深度报告
- **引用管理** - 支持多种学术引用格式

### 🔄 **灵活的 LLM 集成**
- **多 AI 供应商** - 默认 DeepSeek，支持 OpenAI、Ollama 等
- **成本优化** - DeepSeek 提供高性价比解决方案
- **智能回退** - 确保服务可靠性的多层保障
- **速率限制** - 自动处理 API 限制和重试

### 🎨 **现代化前端界面**
- **Vue3 + TypeScript** - 现代化的前端技术栈
- **Element Plus** - 优雅的 UI 组件库
- **Tailwind CSS** - 实用优先的样式框架
- **响应式设计** - 完美适配各种设备

## 🎯 适用人群

- **🎓 研究人员和学者** - 加速系统性综述和荟萃分析
- **📚 研究生** - 快速了解研究领域现状
- **🏢 研发团队** - 跟踪技术进展和市场趋势
- **📈 市场分析师** - 追踪新兴技术和科学突破
- **💼 咨询顾问** - 提供基于证据的洞察

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue3 前端     │    │   FastAPI 后端  │    │   Python 核心   │
│                 │    │                 │    │                 │
│ • Element Plus  │◄──►│ • RESTful API   │◄──►│ • LangChain     │
│ • Tailwind CSS  │    │ • CORS 支持     │    │ • ChromaDB      │
│ • TypeScript    │    │ • 数据验证      │    │ • PDF 处理      │
│ • Pinia 状态管理│    │ • 错误处理      │    │ • 向量搜索      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   外部服务      │
                    │                 │
                    │ • arXiv API     │
                    │ • Semantic      │
                    │   Scholar API   │
                    │ • DeepSeek LLM  │
                    │ • OpenAI API    │
                    └─────────────────┘
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **npm**: 8.0 或更高版本

### 1. 克隆项目

```bash
git clone https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization
```

### 2. 后端设置

#### 创建虚拟环境
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 下载 spaCy 模型
```bash
python -m spacy download en_core_web_sm
```

#### 配置环境变量
```bash
# 复制环境变量模板
copy config\config.example.env .env

# 编辑 .env 文件，设置以下配置：
# LLM_PROVIDER=deepseek
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
# SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here
```

### 3. 前端设置

```bash
cd frontend/literature-review-frontend
npm install
```

### 4. 启动服务

#### 启动后端 API 服务器
```bash
# 在项目根目录
python api_server.py
```
服务器将在 `http://localhost:8000` 启动

#### 启动前端界面

**方式一：简单HTML界面（推荐）**
```bash
# 直接在浏览器中打开
start frontend/simple-frontend/index.html
# 或者使用Python简单服务器
cd frontend/simple-frontend
python -m http.server 8080
```
然后访问 `http://localhost:8080`

**方式二：Vue3开发界面**
```bash
# 在 frontend/literature-review-frontend 目录
cd frontend/literature-review-frontend
node_modules\.bin\vite.cmd
```
前端将在 `http://localhost:5173` 启动

## 📖 使用指南

### Web 界面使用

1. **访问应用**: 打开浏览器访问 `http://localhost:5173`
2. **输入研究主题**: 在搜索框中输入您的研究关键词
3. **配置检索参数**: 
   - 选择数据源（arXiv、Semantic Scholar）
   - 设置论文数量限制
   - 选择年份范围
   - 启用全文获取和 AI 分析
4. **开始检索**: 点击"开始检索"按钮
5. **查看结果**: 浏览检索到的论文列表和统计信息
6. **生成报告**: 基于检索结果生成综述报告

### 命令行界面使用

#### 基本文献综述
```bash
python -m src.lit_review_agent.cli review "人工智能在医疗领域的应用" ^
  --max-papers 15 ^
  --output-format json ^
  --output data/ai_healthcare.json
```

#### 生成综合报告
```bash
python -m src.lit_review_agent.cli generate-report ^
  "AI医疗应用综述报告" ^
  --input data/ai_healthcare.json ^
  --output reports/ai_healthcare_report.md ^
  --format markdown
```

#### 搜索知识库
```bash
python -m src.lit_review_agent.cli search "机器学习药物发现"
```

### Streamlit 界面（传统界面）

```bash
python -m streamlit run src/lit_review_agent/app.py
```

### MCP 服务器（Model Context Protocol）

```bash
python -m uvicorn src.lit_review_agent.mcp_server:mcp_server --host 0.0.0.0 --port 8008 --reload
```

## 🔧 配置说明

### 环境变量配置

| 变量名 | 描述 | 必需 | 默认值 |
|--------|------|------|--------|
| `LLM_PROVIDER` | LLM 提供商 | 是 | `deepseek` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 是 | - |
| `OPENAI_API_KEY` | OpenAI API 密钥 | 否 | - |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API 密钥 | 否 | - |
| `MAX_PAPERS_DEFAULT` | 默认最大论文数 | 否 | `20` |
| `ENABLE_FULL_TEXT` | 启用全文提取 | 否 | `false` |

### 数据源配置

#### arXiv
- 无需 API 密钥
- 支持全文 PDF 下载
- 主要覆盖计算机科学、物理学、数学等领域

#### Semantic Scholar
- 推荐申请 API 密钥以提高请求限制
- 覆盖多个学科领域
- 提供丰富的元数据和引用信息

## 📁 项目结构

```
AI-Agent-for-Automated-Literature-Review-Summarization/
├── 📁 src/                          # Python 核心代码
│   └── 📁 lit_review_agent/
│       ├── 📄 agent.py              # 主要代理类
│       ├── 📄 cli.py                # 命令行界面
│       ├── 📄 app.py                # Streamlit 应用
│       ├── 📄 mcp_server.py         # MCP 服务器
│       ├── 📁 retrievers/           # 文献检索器
│       ├── 📁 processors/           # 文档处理器
│       ├── 📁 analyzers/            # 分析器
│       └── 📁 utils/                # 工具函数
├── 📁 frontend/                     # Vue3 前端
│   └── 📁 literature-review-frontend/
│       ├── 📁 src/
│       │   ├── 📁 components/       # Vue 组件
│       │   ├── 📁 views/            # 页面视图
│       │   ├── 📁 api/              # API 接口
│       │   └── 📁 assets/           # 静态资源
│       ├── 📄 package.json          # 前端依赖
│       └── 📄 vite.config.ts        # Vite 配置
├── 📁 config/                       # 配置文件
├── 📁 data/                         # 数据存储
├── 📁 logs/                         # 日志文件
├── 📁 tests/                        # 测试文件
├── 📄 api_server.py                 # FastAPI 服务器
├── 📄 requirements.txt              # Python 依赖
├── 📄 .env                          # 环境变量
└── 📄 README.md                     # 项目说明
```

## 🔌 API 接口

### 文献检索 API

```http
POST /api/search
Content-Type: application/json

{
  "query": "人工智能在医疗领域的应用",
  "sources": ["arxiv", "semantic_scholar"],
  "maxPapers": 20,
  "yearStart": 2020,
  "yearEnd": 2024,
  "retrieveFullText": false,
  "enableAIAnalysis": true
}
```

### 报告生成 API

```http
POST /api/generate-report
Content-Type: application/json

{
  "title": "AI医疗应用综述报告",
  "papers": [...]
}
```

### 系统状态 API

```http
GET /api/status
```

## 🧪 测试

### 运行单元测试
```bash
pytest tests/
```

### 运行集成测试
```bash
python test_setup.py
```

### 前端测试
```bash
cd frontend/literature-review-frontend
npm run test
```

## 🚀 部署

### Docker 部署（推荐）

```bash
# 构建镜像
docker build -t ai-literature-review .

# 运行容器
docker run -p 8000:8000 -p 5173:5173 ai-literature-review
```

### 传统部署

#### 后端部署
```bash
# 使用 Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app --bind 0.0.0.0:8000
```

#### 前端部署
```bash
cd frontend/literature-review-frontend
npm run build
# 将 dist/ 目录部署到 Web 服务器
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- Python: 遵循 PEP 8 规范
- TypeScript: 使用 ESLint 和 Prettier
- 提交信息: 使用 [Conventional Commits](https://conventionalcommits.org/)

## 📝 更新日志

### v1.2.0 (2024-05-28)
- ✨ 新增 Vue3 现代化前端界面
- 🚀 添加 FastAPI 后端 API 服务
- 🎨 重新设计用户界面，提升用户体验
- 🔧 优化文献检索算法
- 📱 添加响应式设计支持

### v1.1.0 (2024-05-27)
- ✨ 添加 MCP (Model Context Protocol) 支持
- 🔧 改进 Streamlit 界面设计
- 🐛 修复多个已知问题
- 📚 完善文档和使用指南

### v1.0.0 (2024-05-26)
- 🎉 首次发布
- 🔍 支持 arXiv 和 Semantic Scholar 检索
- 🤖 集成 DeepSeek 和 OpenAI LLM
- 📊 基础报告生成功能

## 🐛 问题反馈

如果您遇到任何问题或有功能建议，请：

1. 查看 [FAQ](docs/FAQ.md)
2. 搜索现有的 [Issues](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/issues)
3. 创建新的 Issue

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LangChain](https://langchain.com/) - 强大的 LLM 应用框架
- [DeepSeek](https://platform.deepseek.com/) - 高性价比的 LLM 服务
- [arXiv](https://arxiv.org/) - 开放的学术预印本库
- [Semantic Scholar](https://www.semanticscholar.org/) - 学术搜索引擎
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架

## 📞 联系我们

- 📧 邮箱: your-email@example.com
- 🐦 Twitter: [@your-twitter](https://twitter.com/your-twitter)
- 💬 讨论: [GitHub Discussions](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/discussions)

---

<div align="center">

**如果这个项目对您有帮助，请给我们一个 ⭐️ Star！**

Made with ❤️ by the AI Literature Review Team

</div> 