# 🚀 AI 智能文献综述系统 - 使用指南

## 📋 快速开始

### 方式一：使用启动脚本（推荐）

1. **启动后端服务器**
   ```bash
   # 双击运行或在命令行执行
   start_backend.bat
   ```
   
2. **启动前端界面**
   ```bash
   # 双击运行或在命令行执行
   start_simple_frontend.bat
   ```

3. **访问应用**
   - 打开浏览器访问：`http://localhost:8080`
   - 后端API文档：`http://localhost:8000/docs`

### 方式二：手动启动

1. **激活虚拟环境**
   ```bash
   venv\Scripts\activate
   ```

2. **启动后端**
   ```bash
   python api_server.py
   ```

3. **启动前端**
   ```bash
   cd frontend\simple-frontend
   python -m http.server 8080
   ```

## 🎯 功能使用

### 1. 文献检索

1. **输入研究主题**
   - 在搜索框中输入您的研究关键词
   - 例如："人工智能在医疗领域的应用"

2. **配置检索参数**
   - **数据源**：选择 arXiv、Semantic Scholar 等
   - **论文数量**：设置检索的论文数量（5-50篇）
   - **获取全文**：是否尝试获取PDF全文
   - **AI分析**：是否启用AI深度分析

3. **开始检索**
   - 点击"开始检索"按钮
   - 等待检索完成

### 2. 查看结果

检索完成后，您可以看到：

- **统计信息**：检索到的论文数量、全文获取数量等
- **论文列表**：每篇论文的详细信息
  - 标题和作者
  - 发表日期和来源
  - 摘要内容
  - 关键词标签
  - 操作按钮（查看原文、下载PDF）

### 3. 交互操作

- **查看原文**：点击"查看原文"按钮跳转到论文页面
- **下载PDF**：点击"下载PDF"按钮下载论文文件
- **关键词筛选**：点击关键词标签进行相关搜索

## 🔧 高级功能

### 1. API 接口使用

系统提供完整的RESTful API接口：

#### 文献检索 API
```http
POST http://localhost:8000/api/search
Content-Type: application/json

{
  "query": "人工智能在医疗领域的应用",
  "sources": ["arxiv", "semantic_scholar"],
  "maxPapers": 20,
  "retrieveFullText": false,
  "enableAIAnalysis": true
}
```

#### 系统状态 API
```http
GET http://localhost:8000/api/status
```

### 2. 命令行界面

```bash
# 激活虚拟环境
venv\Scripts\activate

# 进行文献综述
python -m src.lit_review_agent.cli review "研究主题" --max-papers 15

# 生成报告
python -m src.lit_review_agent.cli generate-report "报告标题" --input data.json --output report.md
```

### 3. Streamlit 界面

```bash
# 启动传统Streamlit界面
python -m streamlit run src/lit_review_agent/app.py
```

## 🛠️ 故障排除

### 常见问题

1. **后端启动失败**
   - 检查虚拟环境是否激活
   - 确认所有依赖已安装：`pip install -r requirements.txt`
   - 检查端口8000是否被占用

2. **前端无法访问**
   - 确认后端服务器正在运行
   - 检查端口8080是否被占用
   - 尝试刷新浏览器页面

3. **检索失败**
   - 检查网络连接
   - 确认API密钥配置正确
   - 查看后端日志输出

4. **NumPy版本冲突**
   ```bash
   pip install "numpy>=1.24.0,<2.0.0"
   ```

### 日志查看

- **后端日志**：在启动后端的命令行窗口中查看
- **前端日志**：在浏览器开发者工具的Console中查看

## 📊 性能优化

### 提高检索速度

1. **减少论文数量**：设置较小的maxPapers值
2. **关闭全文获取**：如不需要PDF全文，关闭此选项
3. **选择特定数据源**：只选择需要的数据源

### 提高结果质量

1. **使用精确关键词**：使用更具体的研究主题
2. **启用AI分析**：获得更深入的分析结果
3. **设置年份范围**：限制论文发表时间

## 🔐 配置说明

### 环境变量配置

在 `.env` 文件中配置：

```bash
# LLM配置
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_api_key_here

# 可选配置
OPENAI_API_KEY=your_openai_key
SEMANTIC_SCHOLAR_API_KEY=your_ss_key
```

### 数据源配置

- **arXiv**：无需API密钥，主要覆盖理工科领域
- **Semantic Scholar**：推荐申请API密钥，覆盖多学科

## 📞 技术支持

如遇到问题，请：

1. 查看本使用指南
2. 检查GitHub Issues
3. 查看项目README.md
4. 联系开发团队

---

**祝您使用愉快！** 🎉 