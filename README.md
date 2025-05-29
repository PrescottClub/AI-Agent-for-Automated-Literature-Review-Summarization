# 🔬 AI 智能文献综述与摘要生成系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)
[![MCP](https://img.shields.io/badge/MCP-Supported-purple.svg)](https://modelcontextprotocol.io/)

> **智能化文献综述与摘要生成代理 - 让学术研究更高效**  
> **Created by Terence Qin | 由 Terence Qin 创建**

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
- **实时状态监控** - 后端连接状态实时显示
- **搜索历史** - 自动保存和管理搜索记录
- **高级筛选** - 多维度结果筛选和排序

### 🔌 **MCP 协议支持**
- **Model Context Protocol** - 支持最新的 MCP 标准
- **多工具集成** - 文献检索、分析、相似性搜索
- **资源暴露** - 论文数据和统计信息作为 MCP 资源
- **Claude Desktop 集成** - 无缝集成到 Claude Desktop
- **参数验证** - 完整的输入验证和错误处理

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
                    │ • MCP Server    │
                    └─────────────────┘
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **npm**: 8.0 或更高版本

### 方式一：一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization

# 一键启动所有服务
python scripts/start_all.py
```

### 方式二：手动启动

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization
```

#### 2. 后端设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 下载 spaCy 模型
python -m spacy download en_core_web_sm
```

#### 3. 配置环境变量

```bash
# 复制环境变量模板
copy config\config.example.env .env

# 编辑 .env 文件，设置以下配置：
# LLM_PROVIDER=deepseek
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here  # 用于嵌入
# SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here
```

#### 4. 前端设置

```bash
cd frontend/literature-review-frontend
npm install
```

#### 5. 启动服务

**启动后端 API 服务器**
```bash
# 在项目根目录
python backend
```
服务器将在 `http://localhost:8000` 启动

**启动前端界面**
```bash
# 在 frontend/literature-review-frontend 目录
cd frontend/literature-review-frontend
npm run dev
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
6. **高级功能**:
   - 使用筛选器按作者、关键词、数据源筛选
   - 按相关性、时间、引用数排序
   - 导出结果为 JSON 格式
   - 查看搜索历史
7. **生成报告**: 基于检索结果生成综述报告

### MCP 服务器使用

#### 启动 MCP 服务器
```bash
python -m uvicorn src.lit_review_agent.mcp_server:mcp_server --host 0.0.0.0 --port 8008 --reload
```

#### 可用的 MCP 工具
- `conduct_literature_review` - 进行文献综述
- `analyze_paper` - 分析单篇论文
- `search_similar_papers` - 搜索相似论文

#### 可用的 MCP 资源
- `papers://{paper_id}` - 获取特定论文信息
- `collections://literature` - 获取文献集合统计

#### Claude Desktop 集成
在 Claude Desktop 的配置文件中添加：
```json
{
  "mcpServers": {
    "literature-review": {
      "command": "python",
      "args": ["-m", "uvicorn", "src.lit_review_agent.mcp_server:mcp_server", "--port", "8008"],
      "env": {
        "DEEPSEEK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

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

## 🔧 配置说明

### 环境变量配置

| 变量名 | 描述 | 必需 | 默认值 |
|--------|------|------|--------|
| `LLM_PROVIDER` | LLM 提供商 | 是 | `deepseek` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 是 | - |
| `OPENAI_API_KEY` | OpenAI API 密钥（用于嵌入） | 推荐 | - |
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
├── .vscode/            # VSCode 编辑器配置
├── .streamlit/         # Streamlit 应用配置
├── config/             # 配置文件和模板
│   └── config.example.env # 环境变量模板
├── data/               # 存储原始数据、处理后的数据
├── docs/               # 项目文档
├── frontend/           # 前端应用代码
│   ├── simple-frontend/ # 简单的 HTML/JS 前端示例
│   └── literature-review-frontend/ # Vue3 前端应用
├── logs/               # 日志文件
├── reports/            # 生成的报告
├── scripts/            # 辅助脚本
│   └── start_all.py    # 一键启动脚本
├── src/                # 主要的 Python 源代码
│   ├── lit_review_agent/ # 文献综述代理核心逻辑
│   │   ├── __init__.py
│   │   ├── agent.py      # Agent 核心实现
│   │   ├── cli.py        # 命令行界面
│   │   ├── mcp_server.py # MCP 服务器（增强版）
│   │   ├── ai_core/      # AI 核心模块
│   │   ├── processing/   # 数据处理模块
│   │   ├── retrieval/    # 检索模块
│   │   └── utils/        # 工具函数
├── tests/              # 测试代码
├── venv/               # Python 虚拟环境
├── .gitignore          # Git 忽略文件
├── backend             # FastAPI 后端服务入口
├── README.md           # 项目介绍和使用指南
└── requirements.txt    # Python 依赖包列表
```

## 🛠️ 技术栈

### 后端技术
- **Python 3.8+** - 核心编程语言
- **FastAPI** - 现代化 Web 框架
- **LangChain** - LLM 应用开发框架
- **ChromaDB** - 向量数据库
- **Pydantic** - 数据验证和设置管理
- **spaCy** - 自然语言处理
- **sentence-transformers** - 文本嵌入

### 前端技术
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript
- **Element Plus** - Vue 3 组件库
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Vite** - 现代化构建工具

### AI 和数据处理
- **DeepSeek** - 主要 LLM 提供商
- **OpenAI** - 备用 LLM 和嵌入服务
- **Ollama** - 本地 LLM 支持
- **arXiv API** - 学术论文检索
- **Semantic Scholar API** - 学术搜索引擎

### 协议和标准
- **MCP (Model Context Protocol)** - AI 代理通信协议
- **RESTful API** - Web 服务接口
- **JSON** - 数据交换格式
- **Markdown** - 文档格式

## 🆕 最新更新

### v2.0.0 (2024-12-28)
- ✨ **MCP 协议支持增强** - 新增多个工具和资源
- 🎨 **前端界面全面优化** - 现代化设计和用户体验
- 🔍 **高级搜索功能** - 筛选、排序、历史记录
- 📊 **实时状态监控** - 后端连接状态显示
- 🚀 **一键启动脚本** - 简化部署和启动流程
- 🐛 **Bug 修复** - 修复多个已知问题
- 📝 **文档更新** - 完善使用指南和 API 文档

### 主要改进
1. **MCP 服务器增强**
   - 新增 `analyze_paper` 工具
   - 新增 `search_similar_papers` 工具
   - 完善参数验证和错误处理
   - 支持 MCP 资源暴露

2. **前端界面优化**
   - 响应式设计改进
   - 搜索历史管理
   - 高级筛选和排序
   - 实时状态监控
   - 设置和帮助对话框

3. **系统稳定性**
   - 改进错误处理
   - 优化性能
   - 增强类型安全
   - 完善测试覆盖

## 🤝 贡献指南

我们欢迎各种形式的贡献！如果您有任何改进建议或发现了 Bug，请随时提出 Issue 或提交 Pull Request。

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📝 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢项目创始人 **Terence Qin** 的开创性工作和持续维护
- 感谢所有为本项目贡献代码和想法的开发者
- 感谢 DeepSeek 提供的强大且经济高效的 LLM 服务
- 感谢 LangChain, FastAPI, Vue.js 等开源社区提供的优秀工具
- 感谢 Model Context Protocol 团队推动 AI 代理标准化

## 📞 联系方式

- **项目主页**: [GitHub Repository](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization)
- **问题反馈**: [GitHub Issues](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/discussions)

---

**让 AI 为您的学术研究赋能！🚀** 