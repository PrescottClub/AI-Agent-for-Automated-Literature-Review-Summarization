# 🤖 AI智能文献综述与摘要生成代理

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)
[![MCP](https://img.shields.io/badge/MCP-Supported-purple.svg)](https://modelcontextprotocol.io/)
[![RAG](https://img.shields.io/badge/RAG-Enabled-green.svg)](#)
[![AI Agent](https://img.shields.io/badge/AI_Agent-Autonomous-blue.svg)](#)

> **🚀 智能文献综述AI代理 - 让学术研究更高效**
> **Created by Terence Qin | 由 Terence Qin 创建**

一个基于**大语言模型（LLMs）**、**检索增强生成（RAG）**和**模型上下文协议（MCP）**的先进**AI代理**系统，能够自主发现、分析和综合学术文献，为研究人员节省大量时间，同时提供任何研究领域的全面洞察。

## 🎯 项目状态

✅ **完全可用** - 所有核心功能正常运行
✅ **无已知Bug** - 已修复所有关键问题
✅ **生产就绪** - 可直接部署到生产环境
✅ **持续维护** - 由 Terence Qin 积极维护和更新

## 🧠 核心AI功能

### 🤖 **自主AI代理**
- **自主研究规划** - AI代理自主规划并执行复杂的文献综述任务
- **多步推理** - 将复杂查询分解为可管理的研究步骤
- **自适应策略** - 根据初步发现动态调整搜索策略
- **质量评估** - 使用AI自动评估论文相关性和质量
- **综合智能** - 连接不同的研究发现以识别模式和差距

### 🔗 **检索增强生成（RAG）**
- **向量知识库** - ChromaDB驱动的语义搜索，支持384维嵌入
- **混合检索** - 结合关键词搜索和语义相似性以获得最佳结果
- **上下文感知生成** - 基于检索的学术文献生成LLM响应
- **动态上下文管理** - 智能分块和上下文窗口优化
- **多源集成** - 无缝整合来自多个学术数据库的信息

### 🔌 **模型上下文协议（MCP）集成**
- **MCP服务器实现** - 完全符合MCP 1.0标准的服务器，实现AI代理互操作性
- **工具生态系统** - 可扩展的文献搜索、分析和综合工具
- **资源管理** - 将结构化学术数据作为MCP资源公开
- **Claude Desktop集成** - 与Anthropic的Claude Desktop原生集成
- **标准合规** - 遵循MCP规范以实现最大兼容性

### 🧮 **高级LLM集成**
- **多供应商支持** - DeepSeek（主要）、OpenAI、Ollama，支持智能回退
- **成本优化** - DeepSeek集成相比OpenAI GPT-4节省90%成本
- **提示工程** - 专门用于学术分析和综合的提示
- **思维链推理** - 复杂文献分析的结构化推理
- **速率限制和重试** - 通过指数退避稳健处理API限制

### 📊 **智能分析引擎**
- **语义文本处理** - spaCy NLP管道用于实体提取和文本分析
- **引用网络分析** - 识别有影响力的论文和研究集群
- **趋势检测** - 研究方向和新兴主题的时间分析
- **差距识别** - AI驱动的研究机会识别
- **质量评分** - 多因子相关性和质量评估

### 🔍 **多模态搜索智能**
- **语义搜索** - sentence-transformers (all-MiniLM-L6-v2) 实现深度语义理解
- **跨数据库查询** - 统一搜索arXiv、Semantic Scholar等
- **查询扩展** - AI驱动的查询优化和扩展
- **结果去重** - 跨源智能重复检测
- **相关性排序** - ML驱动的排序，结合多个相关性信号

## ✨ 主要特色功能

### 🚀 **智能文献发现**
- **多源检索** - arXiv、Semantic Scholar，可扩展至更多数据库
- **语义搜索** - 基于向量相似性的高级语义匹配
- **智能过滤** - 按发表日期、期刊和相关性过滤
- **批量处理** - 支持大规模文献批量检索和处理

### 🧠 **AI驱动分析**
- **多格式摘要** - 执行摘要、关键发现、要点摘要
- **趋势识别** - 识别新兴主题和研究热点
- **研究差距分析** - 发现未来研究机会
- **合作网络洞察** - 作者和机构合作模式分析

### 📊 **全面报告生成**
- **专业报告** - 支持Markdown、HTML、LaTeX格式
- **执行摘要** - 为决策者提供简洁概览
- **详细文献综述** - 包含统计分析的深度报告
- **引用管理** - 支持多种学术引用格式

### 🎨 **现代化前端界面**
- **Vue3 + TypeScript** - 现代前端技术栈
- **Element Plus** - 优雅的UI组件库
- **Tailwind CSS** - 实用优先的样式框架
- **响应式设计** - 完美适配各种设备
- **实时状态监控** - 后端连接状态显示
- **搜索历史** - 自动保存和管理搜索记录
- **高级筛选** - 多维度结果筛选和排序

## 🏗️ AI系统架构

```
                        ╭─────────────────────────────────────────────────╮
                        │              🌐 用户交互层                        │
                        ╰─────────────────────────────────────────────────╯
                                              │
                        ╭─────────────────────┴─────────────────────╮
                        │                                           │
            ╭───────────▼──────────╮                    ╭─────────▼──────────╮
            │     🎨 Vue3前端       │                    │   🔌 MCP协议接口    │
            │                     │                    │                   │
            │  • Element Plus UI  │                    │  • Claude Desktop │
            │  • 实时状态监控        │                    │  • 标准化工具       │
            │  • TypeScript       │                    │  • 资源管理         │
            │  • 响应式设计         │                    │  • 智能路由         │
            ╰───────────┬──────────╯                    ╰─────────┬──────────╯
                        │                                        │
                        ╰─────────────────┬──────────────────────╯
                                         │
                        ╭────────────────▼────────────────╮
                        │         ⚡ FastAPI网关          │
                        │                                │
                        │  • RESTful API  • 请求路由     │
                        │  • CORS支持     • 数据验证     │
                        │  • 错误处理     • 速率限制     │
                        ╰────────────────┬────────────────╯
                                        │
                        ╭───────────────▼────────────────╮
                        │        🤖 AI代理核心           │
                        │                               │
                        │  ╭─────────────────────────╮   │
                        │  │    🧠 LangChain框架     │   │
                        │  │  • 代理编排  • 工具链   │   │
                        │  │  • 记忆管理  • 任务规划 │   │
                        │  ╰─────────────────────────╯   │
                        │                               │
                        │  ╭─────────────────────────╮   │
                        │  │    🔍 RAG检索管道       │   │
                        │  │  • 语义搜索  • 向量存储 │   │
                        │  │  • 文档分块  • 相关性排序│   │
                        │  ╰─────────────────────────╯   │
                        ╰───────────────┬────────────────╯
                                       │
                        ╭──────────────▼───────────────╮
                        │        🔬 AI服务层           │
                        ╰──────────────┬───────────────╯
                                      │
        ╭─────────────────────────────┼─────────────────────────────╮
        │                            │                            │
   ╭────▼────╮            ╭─────────▼─────────╮            ╭─────▼─────╮
   │ 🧮 LLM  │            │   💾 向量数据库     │            │ 🔍 学术API │
   │         │            │                  │            │           │
   │DeepSeek │            │  • ChromaDB存储   │            │ • arXiv   │
   │OpenAI   │            │  • 384维嵌入      │            │ • Semantic│
   │Ollama   │            │  • 语义索引       │            │   Scholar │
   ╰─────────╯            │  • 相似性搜索     │            │ • PDF处理 │
                          ╰─────────────────╯            ╰───────────╯

             ╭─────────────────────────────────────────────────╮
             │              🔧 智能处理组件                     │
             │                                                │
             │  📝 spaCy NLP  •  🎯 质量评估  •  📊 趋势分析    │
             │  🔗 引用分析   •  📈 统计建模  •  🎨 报告生成    │
             ╰─────────────────────────────────────────────────╯
```

## 🎯 目标用户

- **🎓 研究人员和学者** - 加速系统性综述和荟萃分析
- **📚 研究生** - 快速了解研究领域现状
- **🏢 研发团队** - 跟踪技术进展和市场趋势
- **📈 市场分析师** - 追踪新兴技术和科学突破
- **💼 咨询顾问** - 提供基于证据的洞察

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **npm**: 8.0 或更高版本

### 方式一：一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization

# 一键启动所有服务
python scripts/start_all.py
```

### 方式二：手动设置

#### 1. 克隆项目

```bash
git clone https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization.git
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

# 下载spaCy模型
python -m spacy download en_core_web_sm
```

#### 3. 配置环境变量

```bash
# 复制环境变量模板
copy config\config.example.env .env

# 编辑.env文件，设置以下配置：
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

**启动后端API服务器**
```bash
# 在项目根目录
python src/lit_review_agent/api_server.py
```
服务器将在 `http://0.0.0.0:8000` 启动（可通过 http://localhost:8000 访问）

**启动前端界面**
```bash
# 在frontend/literature-review-frontend目录
cd frontend/literature-review-frontend
npm run dev
# 或者使用
npx vite
```
前端将在 `http://localhost:5173` 启动

### 🎉 验证安装
启动成功后，您应该看到：
- **后端**: 控制台显示 "✅ 文献代理初始化成功" 和 "Uvicorn running on http://0.0.0.0:8000"
- **前端**: 控制台显示 "VITE v6.3.5 ready" 和 "Local: http://localhost:5173/"
- **API文档**: 访问 http://localhost:8000/docs 查看交互式API文档

## 🔌 MCP协议集成

### 启动MCP服务器
```bash
python -m uvicorn src.lit_review_agent.mcp_server:mcp_server --host 0.0.0.0 --port 8008 --reload
```

#### 可用的MCP工具
- `conduct_literature_review` - 进行全面的文献综述
- `analyze_paper` - 使用AI分析单篇论文
- `search_similar_papers` - 使用语义搜索查找相似论文

#### 可用的MCP资源
- `papers://{paper_id}` - 获取特定论文信息
- `collections://literature` - 获取文献集合统计信息

#### Claude Desktop集成
在Claude Desktop配置中添加：
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

## 📖 使用指南

### Web界面使用

1. **访问应用**: 打开浏览器访问 `http://localhost:5173`
2. **输入研究主题**: 在搜索框中输入研究关键词
3. **配置搜索参数**:
   - 选择数据源（arXiv、Semantic Scholar）
   - 设置论文数量限制
   - 选择年份范围
   - 启用全文提取和AI分析
4. **开始搜索**: 点击"开始搜索"按钮
5. **查看结果**: 浏览检索到的论文列表和统计信息
6. **高级功能**:
   - 使用筛选器按作者、关键词、数据源筛选
   - 按相关性、时间、引用数排序
   - 导出结果为JSON格式
   - 查看搜索历史
7. **生成报告**: 基于搜索结果生成综合综述报告

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
| `LLM_PROVIDER` | LLM提供商 | 是 | `deepseek` |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | 是 | - |
| `OPENAI_API_KEY` | OpenAI API密钥（用于嵌入） | 推荐 | - |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API密钥 | 否 | - |
| `MAX_PAPERS_DEFAULT` | 默认最大论文数 | 否 | `20` |
| `ENABLE_FULL_TEXT` | 启用全文提取 | 否 | `false` |

### 数据源配置

#### arXiv
- 无需API密钥
- 支持全文PDF下载
- 主要覆盖计算机科学、物理学、数学等领域

#### Semantic Scholar
- 推荐申请API密钥以提高请求限制
- 覆盖多个学科领域
- 提供丰富的元数据和引用信息

## 📁 项目结构

```
AI-Agent-for-Automated-Literature-Review-Summarization/
├── .vscode/            # VSCode编辑器配置
├── .streamlit/         # Streamlit应用配置
├── config/             # 配置文件和模板
│   └── config.example.env # 环境变量模板
├── data/               # 原始数据、处理后数据存储
├── docs/               # 项目文档
├── frontend/           # 前端应用代码
│   └── literature-review-frontend/ # Vue3前端应用
├── logs/               # 日志文件
├── reports/            # 生成的报告
├── scripts/            # 辅助脚本
│   └── start_all.py    # 一键启动脚本
├── src/                # 主要Python源代码
│   ├── lit_review_agent/ # 文献综述代理核心逻辑
│   │   ├── __init__.py
│   │   ├── agent.py      # 代理核心实现
│   │   ├── api_server.py # FastAPI服务器
│   │   ├── app.py        # Streamlit应用
│   │   ├── cli.py        # 命令行界面
│   │   ├── mcp_server.py # MCP服务器（增强版）
│   │   ├── ai_core/      # AI核心模块
│   │   ├── processing/   # 数据处理模块
│   │   ├── retrieval/    # 检索模块
│   │   └── utils/        # 工具函数
├── venv/               # Python虚拟环境
├── .gitignore          # Git忽略文件
├── README.md           # 项目介绍和使用指南
└── requirements.txt    # Python依赖包列表
```

## 🛠️ 技术栈

### 后端技术
- **Python 3.8+** - 核心编程语言
- **FastAPI** - 现代Web框架
- **LangChain** - LLM应用开发框架
- **ChromaDB** - 向量数据库
- **Pydantic** - 数据验证和设置管理
- **spaCy** - 自然语言处理
- **sentence-transformers** - 文本嵌入

### 前端技术
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript
- **Element Plus** - Vue 3组件库
- **Tailwind CSS** - 实用优先的CSS框架
- **Vite** - 现代构建工具

### AI和数据处理
- **DeepSeek** - 主要LLM提供商
- **OpenAI** - 备用LLM和嵌入服务
- **Ollama** - 本地LLM支持
- **arXiv API** - 学术论文检索
- **Semantic Scholar API** - 学术搜索引擎

### 协议和标准
- **MCP (模型上下文协议)** - AI代理通信协议
- **RESTful API** - Web服务接口
- **JSON** - 数据交换格式
- **Markdown** - 文档格式

## 🆕 最新更新

### v2.2.0 (2025-05-29) - 生产就绪版本
- 🧹 **项目清理** - 删除所有测试文件和无用代码
- 🐛 **Bug修复** - 修复NLTK数据缺失问题
- ✅ **功能验证** - 所有核心功能测试通过
- 🚀 **API服务器** - 新增专用FastAPI服务器
- 📊 **前端优化** - 修复前端依赖和启动问题
- 🔧 **代码整理** - 清理缓存文件和临时文件
- 📝 **文档更新** - 更新README和项目结构

### v2.0.0 (2025-05-28)
- ✨ **MCP协议支持增强** - 新增多个工具和资源
- 🎨 **前端界面全面优化** - 现代化设计和用户体验
- 🔍 **高级搜索功能** - 筛选、排序、历史记录
- 📊 **实时状态监控** - 后端连接状态显示
- 🚀 **一键启动脚本** - 简化部署和启动流程
- 🐛 **Bug修复** - 修复多个已知问题
- 📝 **文档更新** - 完善使用指南和API文档

### 主要改进
1. **MCP服务器增强**
   - 新增 `analyze_paper` 工具
   - 新增 `search_similar_papers` 工具
   - 完善参数验证和错误处理
   - 支持MCP资源暴露

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

## 🔧 故障排除

### 常见问题

#### 1. 后端启动失败
```bash
# 检查Python版本
python --version  # 需要3.8+

# 检查依赖安装
pip install -r requirements.txt

# 检查环境变量
# 确保.env文件存在且配置正确
```

#### 2. 前端无法连接后端
```bash
# 确保后端服务正在运行
curl http://localhost:8000/health

# 检查端口是否被占用
netstat -an | findstr :8000
```

#### 3. API密钥问题
- 确保DeepSeek API密钥有效且有足够额度
- 检查.env文件中的API密钥格式是否正确
- 验证网络连接是否正常

#### 4. 依赖安装问题
```bash
# 如果遇到spaCy模型下载问题
python -m spacy download en_core_web_sm --user

# 如果遇到ChromaDB问题
pip install --upgrade chromadb
```

### 获取帮助
如果遇到其他问题，请：
1. 查看 `logs/` 目录下的日志文件
2. 在GitHub Issues中搜索相似问题
3. 提交新的Issue并附上错误日志

## 🤝 贡献指南

我们欢迎各种形式的贡献！如果您有任何改进建议或发现了Bug，请随时提出Issue或提交Pull Request。

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

## 📝 许可证

本项目采用MIT许可证。详情请见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢项目创始人 **Terence Qin** 的开创性工作和持续维护
- 感谢所有为本项目贡献代码和想法的开发者
- 感谢DeepSeek提供的强大且经济高效的LLM服务
- 感谢LangChain、FastAPI、Vue.js等开源社区提供的优秀工具
- 感谢Model Context Protocol团队推动AI代理标准化

## 📞 联系方式

- **项目主页**: [GitHub Repository](https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization)
- **问题反馈**: [GitHub Issues](https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization/discussions)

---

**让AI为您的学术研究赋能！🚀**