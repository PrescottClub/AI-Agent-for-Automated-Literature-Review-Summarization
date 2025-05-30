# AI Agent 文献综述项目偏好设置

## 用户偏好

### 开发环境
- **操作系统**: Windows (主要)，需要考虑 PowerShell 兼容性
- **Python版本**: 3.8+ 
- **Node.js版本**: 16.0+
- **包管理器**: npm (前端), pip (后端)
- **虚拟环境**: venv (Python 自带)

### 代码风格偏好
- **响应语言**: 中文，但编程使用英文
- **代码注释**: 中英文混合，重要部分使用中文说明
- **命令连接符**: 在 Windows 中使用 ";" 而不是 "&&"

### 技术栈偏好
- **后端框架**: FastAPI (主要), Streamlit (辅助)
- **前端框架**: Vue 3 + TypeScript + Element Plus
- **AI模型**: DeepSeek (主要), OpenAI (备用)
- **数据库**: ChromaDB (向量存储)
- **样式框架**: Tailwind CSS

### 项目结构偏好
- **模块化设计**: 清晰的模块分离 (retrieval, processing, ai_core 等)
- **配置管理**: 使用 .env 和配置类
- **文档**: 详细的 README 和优化报告
- **测试**: pytest 框架
- **代码质量**: black, flake8, ESLint, Prettier

## 项目特定规则

### 目录结构规范
```
src/lit_review_agent/           # 主应用代码
├── ai_core/                    # AI 核心功能
├── retrieval/                  # 文献检索
├── processing/                 # 数据处理
├── utils/                      # 工具函数
├── interface/                  # 接口层
└── modules/                    # 功能模块

frontend/literature-review-frontend/  # 前端应用
├── src/                        # 源码
├── public/                     # 静态资源
└── e2e/                        # 端到端测试
```

### 命名约定
- **文件名**: 使用下划线 (snake_case) for Python, kebab-case for frontend
- **类名**: PascalCase
- **函数名**: snake_case (Python), camelCase (TypeScript)
- **常量**: UPPER_SNAKE_CASE
- **组件名**: PascalCase (Vue)

### API 设计规范
- **路径前缀**: `/api/v1/`
- **响应格式**: JSON with status, data, message
- **错误处理**: 统一错误码和消息格式
- **CORS**: 允许前端跨域访问

### 部署和运行偏好
- **开发模式**: 使用启动脚本 `python scripts/start_all.py`
- **生产模式**: Docker 容器化部署 (计划中)
- **端口配置**: 后端 8000, 前端 5174
- **环境变量**: 使用 .env 文件管理敏感信息

### 质量控制
- **代码审查**: 关注安全性和性能
- **测试覆盖**: 核心功能必须有单元测试
- **文档更新**: 代码变更时同步更新文档
- **版本控制**: 语义化版本号

### AI Agent 特定规则
- **模型选择**: 优先使用 DeepSeek 降低成本
- **提示工程**: 针对学术文献优化的提示模板
- **RAG 策略**: 语义搜索 + 关键词搜索混合检索
- **MCP 协议**: 遵循 MCP 1.0 标准实现
- **错误处理**: 优雅降级，避免系统崩溃 