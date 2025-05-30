# 🤖 Tsearch - AI智能文献综述与摘要生成系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)
[![Status](https://img.shields.io/badge/Status-Production_Ready-green.svg)](#)

> **🚀 Tsearch - 让学术研究更高效的AI智能助手**
> **Created by Terence Qin | 由 Terence Qin 创建**

**Tsearch：赋能科研创新，您的智能文献分析引擎。** 本系统深度融合前沿大语言模型（LLMs）与检索增强生成（RAG）技术，致力于解决学术研究中信息过载、文献筛选耗时等核心痛点。Tsearch能够自动化实现文献的智能发现、精准解析与高效整合，为科研人员、高校师生及企业研发团队提供强大、便捷的文献研究支持，助力洞察学术趋势，加速知识转化与创新突破。

## 🎯 项目状态

✅ **生产就绪** - 所有核心功能正常运行，可直接使用
✅ **稳定可靠** - 经过全面测试，无已知关键Bug
✅ **持续维护** - 由 Terence Qin 积极维护和更新
✅ **开箱即用** - 支持一键启动，快速部署

## ✨ 核心功能

### 🧠 **智能自然语言查询**
- **自然语言理解** - 支持中英文自然语言查询，无需学习特定语法
- **智能参数提取** - 自动从查询中提取主题、时间范围、关注重点
- **查询增强** - AI自动优化搜索关键词，提升检索精度
- **多语言支持** - 支持中文和英文查询处理

### 📋 **智能行动计划**
- **透明执行** - 展示AI生成的详细行动计划，让用户了解每个步骤
- **动态定制** - 根据查询参数自动调整计划内容
- **进度可视** - 清晰的步骤编号和执行状态
- **用户友好** - 直观的图标和描述，提升用户体验

### 🔍 **智能文献搜索**
- **多数据源** - 支持arXiv、Semantic Scholar等主流学术数据库
- **语义搜索** - 基于AI的深度语义理解，找到真正相关的论文
- **智能过滤** - 按时间、期刊、相关性等多维度筛选
- **批量处理** - 支持大规模文献检索和分析

### 🤖 **AI驱动分析**
- **自动摘要** - 生成论文摘要和关键发现
- **趋势识别** - 发现研究热点和新兴方向
- **质量评估** - AI自动评估论文质量和相关性
- **研究差距** - 识别未来研究机会

### 📊 **智能报告生成**
- **综合报告** - 自动生成文献综述报告
- **多种格式** - 支持Markdown、HTML、JSON等格式
- **可视化** - 生成统计图表和趋势分析
- **引用管理** - 自动整理和格式化参考文献

### 🎨 **现代化界面**
- **Vue3前端** - 响应式设计，支持各种设备
- **实时监控** - 显示搜索进度和系统状态
- **历史记录** - 自动保存搜索历史
- **高级筛选** - 多维度结果筛选和排序

## 🏗️ 系统架构

```mermaid
graph TD
    A[🎨 Vue3 前端<br/>• 响应式界面<br/>• 实时状态监控<br/>• 搜索历史管理]
    B{⚡ FastAPI 后端<br/>• RESTful API<br/>• 数据验证<br/>• 错误处理}
    C{🤖 AI 代理核心<br/>• 智能搜索<br/>• 文献分析<br/>• 报告生成}
    D[🧮 LLM<br/>DeepSeek / OpenAI]
    E[💾 向量数据库<br/>ChromaDB<br/>• 语义搜索]
    F[🔍 学术API<br/>arXiv / Semantic Scholar]

    A --> B
    B --> C
    C --> D
    C --> E
    C --> F

    style A fill:#f8fafc,stroke:#3b82f6,stroke-width:3px,color:#1e293b
    style B fill:#fefefe,stroke:#6366f1,stroke-width:3px,color:#1e293b
    style C fill:#f0fdf4,stroke:#10b981,stroke-width:3px,color:#1e293b
    style D fill:#fffbeb,stroke:#f59e0b,stroke-width:3px,color:#1e293b
    style E fill:#fef3f2,stroke:#ef4444,stroke-width:3px,color:#1e293b
    style F fill:#f0f9ff,stroke:#06b6d4,stroke-width:3px,color:#1e293b
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



## 📖 使用指南

### Web界面使用

1. **访问应用**: 打开浏览器访问 `http://localhost:5173`

2. **智能自然语言查询**: 在搜索框中用自然语言描述您的研究需求
   ```
   示例查询：
   • 我想了解最近三年人工智能在医疗诊断领域的应用进展
   • 寻找关于深度学习优化算法的最新研究，重点关注transformer架构
   • 查找2020年以来量子计算在密码学中的应用研究
   • 机器学习在自动驾驶技术中的最新突破
   ```

3. **查看AI行动计划**: 提交查询后，系统会显示智能生成的执行计划
   - 🎯 确定研究主题
   - 📅 设定时间范围
   - 🔍 重点关注领域
   - 📚 选择数据源
   - 🔎 执行检索策略
   - 📊 分析论文元数据
   - 🤖 AI智能分析
   - 📝 生成最终报告

4. **配置搜索参数**（可选）:
   - 选择数据源（arXiv、Semantic Scholar）
   - 设置论文数量限制
   - 选择年份范围
   - 启用全文提取和AI分析

5. **开始搜索**: 点击"开始搜索"按钮

6. **查看结果**: 浏览检索到的论文列表和统计信息

7. **高级功能**:
   - 使用筛选器按作者、关键词、数据源筛选
   - 按相关性、时间、引用数排序
   - 导出结果为JSON格式
   - 查看搜索历史

8. **生成报告**: 基于搜索结果生成综合综述报告

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

## 🔧 开发环境

### VS Code推荐扩展
- **Vue Language Features (Volar)** - Vue3支持
- **TypeScript Vue Plugin (Volar)** - TypeScript支持
- **Python** - Python语言支持
- **Prettier** - 代码格式化

## 📁 项目结构

```
Tsearch/
├── 📁 config/                    # 配置文件
│   └── config.example.env
├── 📁 data/                      # 数据存储
│   ├── chroma_db/               # 向量数据库
│   └── outputs/                 # 输出文件
├── 📁 frontend/                  # Vue3前端
│   └── literature-review-frontend/
├── 📁 scripts/                   # 启动脚本
│   ├── cleanup_project.py       # 项目清理
│   ├── start_all.py            # 一键启动
│   ├── start_backend_only.py   # 后端启动
│   └── quick_start.py          # 快速启动
├── 📁 src/                       # 核心代码
│   └── lit_review_agent/
│       ├── agent.py             # 主Agent (含自然语言处理)
│       ├── api_server.py        # API服务器 (含行动计划)
│       ├── app.py              # Streamlit应用
│       ├── ai_core/            # AI核心模块
│       ├── processing/         # 数据处理
│       ├── retrieval/          # 文献检索
│       └── utils/              # 工具函数
├── 📁 tests/                     # 测试代码
├── 📁 venv/                      # Python虚拟环境
├── 📄 README.md                 # 项目说明
└── 📄 requirements.txt          # Python依赖
```

## 🛠️ 技术栈

### 核心技术
- **Python 3.8+** + **FastAPI** - 后端API服务
- **Vue 3** + **TypeScript** - 现代前端界面
- **ChromaDB** - 向量数据库存储
- **DeepSeek/OpenAI** - AI大语言模型
- **Docker** - 容器化部署

## 🆕 最新更新

### v3.1.0 (2025-05-30) - 智能化升级版本
- 🧠 **自然语言查询** - 支持中英文自然语言查询，无需学习特定语法
- 📋 **智能行动计划** - AI生成详细执行计划，提升系统透明度
- 🎯 **智能参数提取** - 自动从查询中提取主题、时间范围、关注重点
- 🔧 **查询增强** - AI自动优化搜索关键词，提升检索精度
- 🎨 **界面优化** - 新增行动计划展示组件，提升用户体验
- 🧹 **项目清理** - 优化项目结构，清理不必要文件
- 📝 **文档更新** - 完善使用指南，添加自然语言查询示例
- ✅ **全面测试** - 所有新功能经过完整测试验证

### v3.0.0 (2025-05-30) - 生产优化版本
- 🚀 **系统全面优化** - 完成所有核心功能优化和稳定性提升
- 🔒 **安全增强** - 新增安全中间件，包含速率限制和输入验证
- 📊 **性能监控** - 实时系统指标收集和健康状态监控
- 🧹 **项目精简** - 移除复杂的CI/CD配置，专注核心功能
- 🛡️ **错误处理** - 改进异常处理和资源管理
- 📝 **文档优化** - 简化README，突出核心功能和使用方法
- ✅ **稳定可靠** - 经过全面测试，确保生产环境稳定运行

### v2.3.0 (2025-05-29) - 稳定性增强版本
- 🔧 **后端稳定性优化** - 改进API服务器错误处理和资源管理
- 🏥 **健康检查增强** - 新增详细的系统状态监控
- 🧹 **项目清理** - 删除测试数据库和无用文件
- 🛡️ **异常处理改进** - 增强代理初始化的错误处理
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

# 检查虚拟环境
# 确保使用虚拟环境中的Python
venv\Scripts\python.exe --version  # Windows
source venv/bin/activate && python --version  # Linux/Mac

# 测试后端启动
python scripts/start_backend_only.py
```

#### 1.1 后端服务不稳定
```bash
# 检查健康状态
curl http://localhost:8000/health

# 查看详细状态信息
curl http://localhost:8000/api/status

# 检查日志文件
type logs\app.log  # Windows
cat logs/app.log   # Linux/Mac

# 重启后端服务
# 停止当前服务 (Ctrl+C)
# 重新启动
python scripts/start_backend_only.py
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