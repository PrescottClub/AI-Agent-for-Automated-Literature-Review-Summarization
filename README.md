# 🤖 AI Agent for Automated Literature Review & Summarization

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)
[![MCP](https://img.shields.io/badge/MCP-Supported-purple.svg)](https://modelcontextprotocol.io/)
[![RAG](https://img.shields.io/badge/RAG-Enabled-green.svg)](#)
[![AI Agent](https://img.shields.io/badge/AI_Agent-Autonomous-blue.svg)](#)

> **🚀 Intelligent Literature Review AI Agent - Making Academic Research More Efficient**  
> **Created by Terence Qin | 由 Terence Qin 创建**

An advanced **AI Agent** system powered by **Large Language Models (LLMs)**, **Retrieval-Augmented Generation (RAG)**, and **Model Context Protocol (MCP)** that autonomously discovers, analyzes, and synthesizes academic literature, saving researchers significant time while providing comprehensive insights across any research domain.

## 🧠 Core AI Features

### 🤖 **Autonomous AI Agent**
- **Self-Directing Research** - AI agent autonomously plans and executes complex literature review tasks
- **Multi-Step Reasoning** - Breaks down complex queries into manageable research steps
- **Adaptive Strategy** - Dynamically adjusts search strategies based on initial findings
- **Quality Assessment** - Automatically evaluates paper relevance and quality using AI
- **Synthesis Intelligence** - Connects disparate research findings to identify patterns and gaps

### 🔗 **Retrieval-Augmented Generation (RAG)**
- **Vector Knowledge Base** - ChromaDB-powered semantic search with 384-dimensional embeddings
- **Hybrid Retrieval** - Combines keyword search with semantic similarity for optimal results
- **Context-Aware Generation** - LLM responses grounded in retrieved academic literature
- **Dynamic Context Management** - Intelligent chunking and context window optimization
- **Multi-Source Integration** - Seamlessly combines information from multiple academic databases

### 🔌 **Model Context Protocol (MCP) Integration**
- **MCP Server Implementation** - Full MCP 1.0 compliant server for AI agent interoperability
- **Tool Ecosystem** - Extensible tools for literature search, analysis, and synthesis
- **Resource Management** - Exposés structured academic data as MCP resources
- **Claude Desktop Integration** - Native integration with Anthropic's Claude Desktop
- **Standard Compliance** - Follows MCP specifications for maximum compatibility

### 🧮 **Advanced LLM Integration**
- **Multi-Provider Support** - DeepSeek (primary), OpenAI, Ollama with intelligent fallback
- **Cost Optimization** - DeepSeek integration offers 90% cost savings vs OpenAI GPT-4
- **Prompt Engineering** - Specialized prompts for academic analysis and synthesis
- **Chain-of-Thought Reasoning** - Structured reasoning for complex literature analysis
- **Rate Limiting & Retry** - Robust handling of API limits with exponential backoff

### 📊 **Intelligent Analysis Engine**
- **Semantic Text Processing** - spaCy NLP pipeline for entity extraction and text analysis
- **Citation Network Analysis** - Identifies influential papers and research clusters
- **Trend Detection** - Temporal analysis of research directions and emerging topics
- **Gap Identification** - AI-powered identification of research opportunities
- **Quality Scoring** - Multi-factor relevance and quality assessment

### 🔍 **Multi-Modal Search Intelligence**
- **Semantic Search** - sentence-transformers (all-MiniLM-L6-v2) for deep semantic understanding
- **Cross-Database Query** - Unified search across arXiv, Semantic Scholar, and more
- **Query Expansion** - AI-powered query refinement and expansion
- **Result Deduplication** - Intelligent duplicate detection across sources
- **Relevance Ranking** - ML-powered ranking combining multiple relevance signals

## ✨ Key Features

### 🚀 **Smart Literature Discovery**
- **Multi-Source Retrieval** - arXiv, Semantic Scholar, and extensible to more databases
- **Semantic Search** - Vector similarity-based advanced semantic matching
- **Intelligent Filtering** - Filter by publication date, journal, and relevance
- **Batch Processing** - Support for large-scale literature batch retrieval and processing

### 🧠 **AI-Driven Analysis**
- **Multi-Format Summaries** - Executive summaries, key findings, bullet point summaries
- **Trend Identification** - Identify emerging topics and research hotspots
- **Research Gap Analysis** - Discover future research opportunities
- **Collaboration Network Insights** - Author and institution collaboration pattern analysis

### 📊 **Comprehensive Report Generation**
- **Professional Reports** - Support for Markdown, HTML, LaTeX formats
- **Executive Summaries** - Concise overviews for decision makers
- **Detailed Literature Reviews** - In-depth reports with statistical analysis
- **Citation Management** - Support for multiple academic citation formats

### 🎨 **Modern Frontend Interface**
- **Vue3 + TypeScript** - Modern frontend technology stack
- **Element Plus** - Elegant UI component library
- **Tailwind CSS** - Utility-first styling framework
- **Responsive Design** - Perfect adaptation to various devices
- **Real-time Status Monitoring** - Backend connection status display
- **Search History** - Automatic saving and management of search records
- **Advanced Filtering** - Multi-dimensional result filtering and sorting

## 🏗️ AI System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue3 Frontend │    │   FastAPI API   │    │   AI Agent Core │
│                 │    │                 │    │                 │
│ • Element Plus  │◄──►│ • RESTful API   │◄──►│ • LangChain     │
│ • Real-time UI  │    │ • CORS Support  │    │ • RAG Pipeline  │
│ • TypeScript    │    │ • Validation    │    │ • Vector Search │
│ • State Mgmt    │    │ • Error Handling│    │ • LLM Agents    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   AI Services   │
                    │                 │
                    │ • DeepSeek LLM  │
                    │ • ChromaDB      │
                    │ • spaCy NLP     │
                    │ • MCP Server    │
                    │ • Embeddings    │
                    └─────────────────┘
```

## 🎯 Target Users

- **🎓 Researchers and Academics** - Accelerate systematic reviews and meta-analyses
- **📚 Graduate Students** - Quickly understand research field status
- **🏢 R&D Teams** - Track technological progress and market trends
- **📈 Market Analysts** - Follow emerging technologies and scientific breakthroughs
- **💼 Consultants** - Provide evidence-based insights

## 🚀 Quick Start

### Environment Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher

### Option 1: One-Click Start (Recommended)

```bash
# Clone the project
git clone https://github.com/TerenceYin/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization

# One-click start all services
python scripts/start_all.py
```

### Option 2: Manual Setup

#### 1. Clone Project

```bash
git clone https://github.com/TerenceYin/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

#### 3. Configure Environment Variables

```bash
# Copy environment variable template
copy config\config.example.env .env

# Edit .env file, set the following configurations:
# LLM_PROVIDER=deepseek
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here  # For embeddings
# SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here
```

#### 4. Frontend Setup

```bash
cd frontend/literature-review-frontend
npm install
```

#### 5. Start Services

**Start Backend API Server**
```bash
# In project root directory
python backend.py
```
Server will start at `http://localhost:8000`

**Start Frontend Interface**
```bash
# In frontend/literature-review-frontend directory
cd frontend/literature-review-frontend
npx vite --host
```
Frontend will start at `http://localhost:5173`

## 🔌 MCP Protocol Integration

### Starting MCP Server
```bash
python -m uvicorn src.lit_review_agent.mcp_server:mcp_server --host 0.0.0.0 --port 8008 --reload
```

#### Available MCP Tools
- `conduct_literature_review` - Conduct comprehensive literature reviews
- `analyze_paper` - Analyze individual papers with AI
- `search_similar_papers` - Find similar papers using semantic search

#### Available MCP Resources
- `papers://{paper_id}` - Get specific paper information
- `collections://literature` - Get literature collection statistics

#### Claude Desktop Integration
Add to Claude Desktop configuration:
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

## 📖 Usage Guide

### Web Interface Usage

1. **Access Application**: Open browser and visit `http://localhost:5173`
2. **Enter Research Topic**: Type your research keywords in the search box
3. **Configure Search Parameters**:
   - Select Data Source (arXiv, Semantic Scholar)
   - Set Paper Limit
   - Select Year Range
   - Enable Full Text Extraction and AI Analysis
4. **Start Search**: Click "Start Search" button
5. **View Results**: Browse through the list of retrieved papers and statistics
6. **Advanced Features**:
   - Use Filters to filter by Author, Keyword, Data Source
   - Sort by Relevance, Time, Citation Count
   - Export Results as JSON Format
   - View Search History
7. **Generate Report**: Generate comprehensive review report based on search results

### MCP Server Usage

#### Starting MCP Server
```bash
python -m uvicorn src.lit_review_agent.mcp_server:mcp_server --host 0.0.0.0 --port 8008 --reload
```

#### Available MCP Tools
- `conduct_literature_review` - Conduct comprehensive literature reviews
- `analyze_paper` - Analyze individual papers with AI
- `search_similar_papers` - Find similar papers using semantic search

#### Available MCP Resources
- `papers://{paper_id}` - Get specific paper information
- `collections://literature` - Get literature collection statistics

#### Claude Desktop Integration
Add to Claude Desktop configuration:
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

### Command Line Interface Usage

#### Basic Literature Review
```bash
python -m src.lit_review_agent.cli review "人工智能在医疗领域的应用" ^
  --max-papers 15 ^
  --output-format json ^
  --output data/ai_healthcare.json
```

#### Generate Comprehensive Report
```bash
python -m src.lit_review_agent.cli generate-report ^
  "AI医疗应用综述报告" ^
  --input data/ai_healthcare.json ^
  --output reports/ai_healthcare_report.md ^
  --format markdown
```

#### Search Knowledge Base
```bash
python -m src.lit_review_agent.cli search "机器学习药物发现"
```

## 🔧 Configuration Instructions

### Environment Variable Configuration

| Variable Name | Description | Required | Default Value |
|-------------|-------------|----------|---------------|
| `LLM_PROVIDER` | LLM Provider | Yes | `deepseek` |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | Yes | - |
| `OPENAI_API_KEY` | OpenAI API Key (For embeddings) | Recommended | - |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API Key | No | - |
| `MAX_PAPERS_DEFAULT` | Default Maximum Papers | No | `20` |
| `ENABLE_FULL_TEXT` | Enable Full Text Extraction | No | `false` |

### Data Source Configuration

#### arXiv
- No API Key Required
- Supports Full Text PDF Download
- Primarily Covers Computer Science, Physics, Mathematics, etc.

#### Semantic Scholar
- Recommended to Apply for API Key to Increase Request Limits
- Covers Multiple Academic Fields
- Provides Rich Metadata and Citation Information

## 📁 Project Structure

```
AI-Agent-for-Automated-Literature-Review-Summarization/
├── .vscode/            # VSCode Editor Configuration
├── .streamlit/         # Streamlit Application Configuration
├── config/             # Configuration Files and Templates
│   └── config.example.env # Environment Variable Template
├── data/               # Storage of Raw Data, Processed Data
├── docs/               # Project Documentation
├── frontend/           # Frontend Application Code
│   ├── simple-frontend/ # Simple HTML/JS Frontend Example
│   └── literature-review-frontend/ # Vue3 Frontend Application
├── logs/               # Log Files
├── reports/            # Generated Reports
├── scripts/            # Helper Scripts
│   └── start_all.py    # One-Click Start Script
├── src/                # Main Python Source Code
│   ├── lit_review_agent/ # Literature Review Agent Core Logic
│   │   ├── __init__.py
│   │   ├── agent.py      # Agent Core Implementation
│   │   ├── cli.py        # Command Line Interface
│   │   ├── mcp_server.py # MCP Server (Enhanced Version)
│   │   ├── ai_core/      # AI Core Module
│   │   ├── processing/   # Data Processing Module
│   │   ├── retrieval/    # Retrieval Module
│   │   └── utils/        # Utility Functions
├── tests/              # Test Code
├── venv/               # Python Virtual Environment
├── .gitignore          # Git Ignore File
├── backend             # FastAPI Backend Service Entry
├── README.md           # Project Introduction and Usage Guide
└── requirements.txt    # Python Dependency Package List
```

## ��️ Technology Stack

### Backend Technology
- **Python 3.8+** - Core Programming Language
- **FastAPI** - Modern Web Framework
- **LangChain** - LLM Application Development Framework
- **ChromaDB** - Vector Database
- **Pydantic** - Data Validation and Settings Management
- **spaCy** - Natural Language Processing
- **sentence-transformers** - Text Embedding

### Frontend Technology
- **Vue 3** - Progressive JavaScript Framework
- **TypeScript** - Type-Safe JavaScript
- **Element Plus** - Vue 3 Component Library
- **Tailwind CSS** - Utility-First CSS Framework
- **Vite** - Modern Build Tool

### AI and Data Processing
- **DeepSeek** - Primary LLM Provider
- **OpenAI** - Alternative LLM and Embedding Service
- **Ollama** - Local LLM Support
- **arXiv API** - Academic Paper Retrieval
- **Semantic Scholar API** - Academic Search Engine

### Protocol and Standards
- **MCP (Model Context Protocol)** - AI Agent Communication Protocol
- **RESTful API** - Web Service Interface
- **JSON** - Data Exchange Format
- **Markdown** - Document Format

## 🆕 Latest Updates

### v2.0.0 (2024-12-28)
- ✨ **MCP Protocol Support Enhancement** - Added Multiple Tools and Resources
- 🎨 **Frontend Interface Full Optimization** - Modern Design and User Experience
- 🔍 **Advanced Search Function** - Filter, Sort, History Record
- 📊 **Real-time Status Monitoring** - Backend Connection Status Display
- 🚀 **One-Click Start Script** - Simplify Deployment and Launch Process
- 🐛 **Bug Fix** - Fixed Multiple Known Issues
- 📝 **Documentation Update** - Complete Usage Guide and API Documentation

### Main Improvements
1. **MCP Server Enhancement**
   - Added `analyze_paper` Tool
   - Added `search_similar_papers` Tool
   - Improved Parameter Validation and Error Handling
   - Supported MCP Resource Exposure

2. **Frontend Interface Optimization**
   - Responsive Design Improvement
   - Search History Management
   - Advanced Filtering and Sorting
   - Real-time Status Monitoring
   - Settings and Help Dialog

3. **System Stability**
   - Improved Error Handling
   - Optimized Performance
   - Enhanced Type Safety
   - Complete Test Coverage

## 🤝 Contribution Guidelines

We Welcome All Forms of Contributions! If You Have Any Improvement Suggestions or Found Bugs, Please Feel Free to Raise Issue or Submit Pull Request.

1. Fork This Repository
2. Create Your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit Your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This Project Uses MIT License. For Details, Please See [LICENSE](LICENSE) File.

## 🙏 Acknowledgments

- Thanks to Project Founder **Terence Qin** for His Pioneering Work and Continuous Maintenance
- Thanks to All Developers Who Contributed Code and Ideas to This Project
- Thanks to DeepSeek for Providing Powerful and Economical LLM Service
- Thanks to LangChain, FastAPI, Vue.js, etc. for Providing Excellent Tools in Open Source Community
- Thanks to Model Context Protocol Team for Driving AI Agent Standardization

## 📞 Contact Information

- **Project Page**: [GitHub Repository](https://github.com/TerenceYin/AI-Agent-for-Automated-Literature-Review-Summarization)
- **Issue Feedback**: [GitHub Issues](https://github.com/TerenceYin/AI-Agent-for-Automated-Literature-Review-Summarization/issues)
- **Discussion Exchange**: [GitHub Discussions](https://github.com/TerenceYin/AI-Agent-for-Automated-Literature-Review-Summarization/discussions)

---

**Let AI Empower Your Academic Research!🚀** 