# 安装指南

## 系统要求

### 硬件要求
- **内存**: 最少 4GB RAM，推荐 8GB 或更多
- **存储**: 至少 2GB 可用空间
- **网络**: 稳定的互联网连接（用于API调用和论文下载）

### 软件要求
- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **npm**: 8.0 或更高版本
- **Git**: 用于克隆仓库

## 快速安装

### 方式一：一键安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization

# 2. 运行一键启动脚本
python scripts/start_all.py
```

脚本会自动：
- 检查系统要求
- 安装Python和Node.js依赖
- 启动后端和前端服务

### 方式二：手动安装

#### 1. 克隆仓库

```bash
git clone https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization.git
cd AI-Agent-for-Automated-Literature-Review-Summarization
```

#### 2. 设置Python环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 下载spaCy语言模型
python -m spacy download en_core_web_sm
```

#### 3. 设置前端环境

```bash
# 进入前端目录
cd frontend/literature-review-frontend

# 安装Node.js依赖
npm install

# 返回项目根目录
cd ../..
```

#### 4. 配置环境变量

```bash
# 复制环境变量模板
cp config/config.example.env .env

# 编辑.env文件，填入您的API密钥
# 必需的配置：
# - DEEPSEEK_API_KEY: DeepSeek API密钥
# - OPENAI_API_KEY: OpenAI API密钥（用于嵌入）
```

#### 5. 启动服务

**启动后端服务**:
```bash
# 在项目根目录，确保虚拟环境已激活
python backend.py
```

**启动前端服务**:
```bash
# 在新的终端窗口
cd frontend/literature-review-frontend
npm run dev
```

## API密钥配置

### 1. DeepSeek API密钥（必需）

1. 访问 [DeepSeek平台](https://platform.deepseek.com/api_keys)
2. 注册账户并创建API密钥
3. 在`.env`文件中设置：
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

### 2. OpenAI API密钥（推荐）

1. 访问 [OpenAI平台](https://platform.openai.com/api-keys)
2. 创建API密钥
3. 在`.env`文件中设置：
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### 3. Semantic Scholar API密钥（可选）

1. 访问 [Semantic Scholar API](https://www.semanticscholar.org/product/api)
2. 申请API密钥
3. 在`.env`文件中设置：
   ```
   SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here
   ```

## 验证安装

### 1. 检查后端服务

```bash
# 检查后端健康状态
curl http://localhost:8000/api/status

# 或在浏览器中访问
http://localhost:8000/docs
```

### 2. 检查前端服务

在浏览器中访问：`http://localhost:5173`

### 3. 运行测试

```bash
# 运行CLI测试
python -m src.lit_review_agent.cli config-info

# 运行示例脚本
python scripts/run_example.py
```

## 故障排除

### 常见问题

#### 1. Python依赖安装失败

```bash
# 升级pip
python -m pip install --upgrade pip

# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt
```

#### 2. spaCy模型下载失败

```bash
# 手动下载模型
python -m spacy download en_core_web_sm --user

# 或使用直接链接
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

#### 3. Node.js依赖安装失败

```bash
# 清理npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf frontend/literature-review-frontend/node_modules
cd frontend/literature-review-frontend
npm install
```

#### 4. 端口被占用

```bash
# 检查端口使用情况
# Windows
netstat -an | findstr :8000
netstat -an | findstr :5173

# Linux/Mac
lsof -i :8000
lsof -i :5173

# 杀死占用端口的进程
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

#### 5. API密钥问题

- 确保API密钥有效且有足够额度
- 检查网络连接
- 验证`.env`文件格式正确

### 获取帮助

如果遇到其他问题：

1. 查看日志文件：`logs/app.log`
2. 检查GitHub Issues：[项目Issues](https://github.com/PrescottClub/AI-Agent-for-Automated-Literature-Review-Summarization/issues)
3. 提交新Issue并附上错误日志

## 高级配置

### 自定义配置

编辑`.env`文件以自定义系统行为：

```bash
# 调整日志级别
LOG_LEVEL=DEBUG

# 修改默认数据源
DEFAULT_RETRIEVAL_SOURCES=arxiv,semantic_scholar

# 调整处理限制
MAX_PAPERS_DEFAULT=50
MAX_REQUESTS_PER_MINUTE=30
```

### 数据库配置

默认使用ChromaDB作为向量数据库，数据存储在`./data/chroma_db`目录。

### 性能优化

1. **增加内存**: 提高系统性能
2. **SSD存储**: 加快数据库访问速度
3. **网络优化**: 使用稳定的网络连接
4. **并发设置**: 根据系统性能调整并发数量
