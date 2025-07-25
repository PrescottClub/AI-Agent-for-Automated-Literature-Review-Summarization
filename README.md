# 🔍 Tsearch - AI Literature Discovery Engine

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/Powered_by-DeepSeek-orange.svg)](https://platform.deepseek.com/)

> **AI-powered literature discovery and review generation platform** | **Created by Terence Qin**

Tsearch is an intelligent literature discovery engine that leverages advanced AI technologies to streamline academic research. It combines natural language processing, vector search, and automated analysis to help researchers find, analyze, and synthesize academic literature efficiently.

## ✨ Key Features

- **🔍 Smart Search**: Natural language queries with intelligent paper discovery
- **🤖 AI Analysis**: Automated content analysis and trend identification  
- **📊 Report Generation**: One-click literature review and summary creation
- **🌐 Multi-Source**: Integration with arXiv, Semantic Scholar, and more
- **⚡ Real-time**: Fast, responsive web interface with live updates

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- API Keys: DeepSeek (required), OpenAI (for embeddings), Semantic Scholar (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tsearch.git
   cd tsearch
   ```

2. **Set up environment**
   ```bash
   # Copy configuration template
   cp config/config.env .env
   
   # Edit .env file with your API keys
   # DEEPSEEK_API_KEY=your-deepseek-api-key
   # OPENAI_API_KEY=your-openai-api-key
   ```

3. **Install dependencies**
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend/literature-review-frontend
   npm install
   cd ../..
   ```

4. **Start the application**
   ```bash
   # Option 1: Start both services
   python scripts/start_all.py
   
   # Option 2: Start individually
   python scripts/start_backend_only.py  # Backend: http://localhost:8000
   cd frontend/literature-review-frontend && npm run dev  # Frontend: http://localhost:5173
   ```

### Usage

1. Open http://localhost:5173 in your browser
2. Enter your research query in natural language
3. Review AI-generated literature analysis
4. Export reports and summaries

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue3 Frontend │    │  FastAPI Backend│    │   AI Core       │
│                 │    │                 │    │                 │
│ • Search UI     │◄──►│ • REST API      │◄──►│ • LLM Integration│
│ • Results View  │    │ • Data Validation│    │ • Vector Search │
│ • Report Export │    │ • Error Handling│    │ • Content Analysis│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌────────▼────────┐
                                               │  External APIs  │
                                               │                 │
                                               │ • arXiv         │
                                               │ • Semantic      │
                                               │   Scholar       │
                                               │ • ChromaDB      │
                                               └─────────────────┘
```

## 🛠️ Tech Stack

- **Frontend**: Vue 3, TypeScript, Tailwind CSS, Element Plus
- **Backend**: FastAPI, Python 3.9+, Pydantic
- **AI/ML**: DeepSeek API, OpenAI Embeddings, ChromaDB
- **Data Sources**: arXiv API, Semantic Scholar API
- **Deployment**: Docker, Docker Compose

## 📝 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Terence Qin** - _Creator and Maintainer_

## 🙏 Acknowledgments

- DeepSeek for providing powerful LLM capabilities
- arXiv and Semantic Scholar for academic data access
- The open-source community for excellent tools and libraries
