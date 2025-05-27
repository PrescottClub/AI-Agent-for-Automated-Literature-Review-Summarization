# 🔬 AI Literature Review & Summarization Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)

> **智能化文献综述与摘要生成代理 - 让研究更高效**

一个基于AI的智能代理，能够**自动发现、分析和综合**学术文献，为研究人员节省大量时间，并提供任何研究领域的全面洞察。

## ✨ 核心特性

### 🚀 **智能文献检索**
- **多源检索** - 支持arXiv、Semantic Scholar等学术数据库
- **语义搜索** - 基于向量相似度的高级语义匹配
- **智能过滤** - 按发表日期、期刊和相关性筛选

### 🧠 **AI驱动分析**
- **多格式摘要** - 支持执行摘要、关键发现、要点总结
- **趋势识别** - 识别新兴主题和研究热点
- **研究缺口分析** - 发现未来研究机会
- **合作网络洞察** - 作者和机构合作模式分析

### 📊 **全面报告生成**
- **专业报告** - 支持Markdown、HTML、LaTeX格式
- **执行摘要** - 为决策者提供简洁概览
- **详细文献综述** - 包含统计分析的深度报告
- **引用管理** - 支持多种学术引用格式

### 🔄 **灵活的LLM集成**
- **多AI供应商** - 默认DeepSeek，支持OpenAI、Ollama等
- **成本优化** - DeepSeek提供高性价比解决方案
- **智能回退** - 确保服务可靠性的多层保障
- **速率限制** - 自动处理API限制和重试

## 🎯 适用人群

- **🎓 研究人员和学者** - 加速系统性综述和荟萃分析
- **📚 研究生** - 快速了解研究领域现状
- **🏢 研发团队** - 跟踪技术进展和市场趋势
- **📈 市场分析师** - 追踪新兴技术和科学突破
- **💼 咨询顾问** - 提供基于证据的洞察

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization

# 创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 下载spaCy模型
python -m spacy download en_core_web_sm

# 运行设置向导
python -m src.lit_review_agent.cli setup
```

### 配置

复制配置文件并设置API密钥：

```bash
# 复制配置模板
copy config\config.example.env .env

# 编辑 .env 文件，添加以下配置：
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # 用于embedding
```

### 快速体验

```bash
# 1. 进行文献综述
python -m src.lit_review_agent.cli review "人工智能在医疗领域的应用" ^
  --max-papers 15 ^
  --output-format json ^
  --output data/ai_healthcare.json

# 2. 生成综合报告
python -m src.lit_review_agent.cli generate-report ^
  "AI医疗应用综述报告" ^
  --input data/ai_healthcare.json ^
  --output reports/ai_healthcare_report.md ^
  --format markdown

# 3. 搜索知识库
python -m src.lit_review_agent.cli search "机器学习药物发现"
```

## 📖 详细使用指南

### 命令行界面

#### 设置和配置
```bash
# 查看设置向导
python -m src.lit_review_agent.cli setup

# 查看当前配置
python -m src.lit_review_agent.cli config-info

# 查看系统统计
python -m src.lit_review_agent.cli stats
```

#### 文献综述
```bash
python -m src.lit_review_agent.cli review "研究主题" [选项]
```

**主要选项：**
- `--max-papers N`: 检索论文数量（默认：10）
- `--sources SOURCE1,SOURCE2`: 指定数据源（arxiv,semantic_scholar）
- `--full-text`: 尝试提取PDF全文
- `--year-start YEAR`: 起始年份过滤
- `--year-end YEAR`: 结束年份过滤
- `--format FORMAT`: 输出格式（json, markdown）
- `--output FILE`: 输出文件路径

#### 报告生成
```bash
python -m src.lit_review_agent.cli generate-report "报告标题" ^
  --input 输入文件.json ^
  --output 输出文件.md ^
  --format markdown
```

**支持格式：**
- `markdown`: Markdown格式报告
- `html`: HTML网页格式
- `latex`: LaTeX学术格式

### Python API

```python
import asyncio
from src.lit_review_agent import LiteratureAgent, Config

async def main():
    # 初始化配置
    config = Config()
    agent = LiteratureAgent(config)
    
    # 进行文献综述
    results = await agent.conduct_literature_review(
        research_topic="深度学习在计算机视觉中的应用",
        max_papers=20,
        sources=["arxiv", "semantic_scholar"],
        retrieve_full_text=False,
        year_start=2020,
        year_end=2024
    )
    
    # 生成报告
    report = await agent.generate_full_report(
        papers=results['papers'],
        topic="深度学习视觉应用综述",
        output_format="markdown"
    )
    
    print(f"处理了 {results['num_papers_processed']} 篇论文")
    print(f"报告长度: {len(report.get('content', ''))} 字符")

# 运行
asyncio.run(main())
```

## 🏗 系统架构

```
📁 AI Literature Review Agent
├── 🔍 文献检索层
│   ├── ArXiv API客户端
│   ├── Semantic Scholar客户端
│   └── PDF文本提取器
├── 🧠 AI核心引擎
│   ├── 多LLM管理器 (DeepSeek, OpenAI)
│   ├── 文献摘要生成器
│   ├── 趋势分析器
│   └── 报告生成器
├── 💾 知识管理
│   ├── 向量数据库 (ChromaDB)
│   ├── Embedding生成
│   └── 语义搜索
├── 🔧 文本处理
│   ├── spaCy NLP管道
│   ├── 关键词提取
│   └── 文本分块策略
└── 🖥 用户界面
    ├── CLI命令行工具
    ├── Python API
    └── 配置管理系统
```

## 📊 示例输出

### 执行摘要
> "本次对47篇AI医疗领域最新论文的综合分析显示三大趋势：(1) **基础模型**在医学影像中的应用显著提升诊断准确率73%，(2) **联邦学习**方法在保护隐私的同时维持模型性能，(3) **多模态融合**正成为临床数据整合的新前沿..."

### 关键洞察
- **94%的综述论文**发表于近2年，表明该领域发展迅速
- **顶级合作网络**主要在斯坦福、MIT和Google Health之间
- **新兴方法**：宪法AI、工具增强推理、检索增强生成
- **研究缺口**：长期安全性研究、监管框架开发

## 🛠 高级配置

### 环境变量配置

```bash
# 核心LLM设置
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_MODEL=deepseek-chat

# OpenAI设置（embedding必需）
OPENAI_API_KEY=sk-xxx
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# 可选：Semantic Scholar API
SEMANTIC_SCHOLAR_API_KEY=your_key

# 处理限制
ARXIV_MAX_RESULTS=100
MAX_TOKENS_PER_REQUEST=4000
MAX_REQUESTS_PER_MINUTE=60

# 存储配置
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
OUTPUT_DIR=./data/outputs
```

### 自定义embedding模型

```bash
# 向量存储的sentence-transformers模型
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2  # 默认
# SENTENCE_TRANSFORMER_MODEL=all-mpnet-base-v2  # 更高质量
# SENTENCE_TRANSFORMER_MODEL=paraphrase-multilingual-MiniLM-L12-v2  # 多语言
```

## 🧪 测试

```bash
# 运行设置验证
python test_setup.py

# 测试基本功能（需要API密钥）
python -m src.lit_review_agent.cli review "test topic" --max-papers 3

# 验证配置
python -m src.lit_review_agent.cli config-info
```

## 🛡 安全与隐私

- **API密钥加密存储** - 本地安全管理
- **本地处理选项** - 敏感研究的隐私保护
- **无数据保留** - 不存储处理过的论文内容
- **审计日志** - 机构合规要求支持

## 🚨 故障排除

### 常见问题

1. **配置错误**
   ```bash
   python -m src.lit_review_agent.cli config-info
   ```

2. **依赖缺失**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **API限制**
   - 检查API密钥配置
   - 调整请求频率设置
   - 使用备用API提供商

4. **内存不足**
   - 减少`max_papers`参数
   - 调整`MAX_CHUNK_SIZE`配置
   - 关闭`retrieve_full_text`选项

## 📈 性能优化

- **批处理优化** - 自动批量处理请求
- **异步处理** - 并发API调用
- **智能缓存** - 向量数据库持久化
- **增量更新** - 避免重复处理

## 🤝 贡献指南

我们欢迎社区贡献！请查看[贡献指南](CONTRIBUTING.md)了解详情。

### 开发环境设置
```bash
# 开发安装
git clone <repository>
cd AI-Agent-for-Automated-Literature-Review-Summarization
pip install -e ".[dev]"

# 安装预提交钩子
pre-commit install

# 运行测试
python -m pytest tests/ -v
```

## 📄 许可证

本项目基于MIT许可证开源 - 详见[LICENSE](LICENSE)文件。

## 🌟 Star历史

如果这个项目对您有帮助，请给我们一个⭐！

## 💬 社区与支持

- **🐛 问题报告**: [GitHub Issues](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/issues)
- **💡 功能请求**: [GitHub Discussions](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/discussions)
- **📧 邮件联系**: support@example.com

---

<div align="center">

**💡 为研究社区而生，用❤️打造**

[⭐ 点赞项目](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization) • [🍴 Fork项目](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/fork) • [🐛 报告Bug](https://github.com/your-username/AI-Agent-for-Automated-Literature-Review-Summarization/issues)

</div> 