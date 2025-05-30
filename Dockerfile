# 🚀 AI文献综述系统 - 多阶段 Dockerfile
# ===================================================

# 阶段1: 前端构建
FROM node:18-alpine AS frontend-builder

LABEL maintainer="Terence Qin <prescottchun@163.com>"
LABEL description="AI Agent for Automated Literature Review & Summarization"

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/literature-review-frontend/package*.json ./

# 安装前端依赖
RUN npm ci --only=production && npm cache clean --force

# 复制前端源码
COPY frontend/literature-review-frontend/ ./

# 构建前端
RUN npm run build

# 阶段2: Python 后端
FROM python:3.9-slim AS backend

WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 复制 Python 依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 spaCy 模型
RUN python -m spacy download en_core_web_sm

# 创建应用目录结构
RUN mkdir -p /app/data /app/logs /app/config

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/
COPY setup.py ./

# 从前端构建阶段复制静态文件
COPY --from=frontend-builder /app/frontend/dist ./static/

# 创建非root用户
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app && \
    chmod +x /app/src/lit_review_agent/api_server.py

# 切换到非root用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["python", "-m", "uvicorn", "src.lit_review_agent.api_server:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1"]

# 元数据标签
LABEL version="2.0.0" \
      description="AI Agent for Literature Review and Summarization" \
      architecture="multi-stage" \
      components="Vue3+FastAPI+ChromaDB" \
      maintainer="Terence Qin" 