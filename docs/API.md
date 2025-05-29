# API 文档

## FastAPI 后端 API

### 基础信息

- **基础URL**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs`
- **OpenAPI规范**: `http://localhost:8000/openapi.json`

### 认证

目前API不需要认证，但建议在生产环境中添加适当的认证机制。

## 端点列表

### 1. 系统状态

#### GET `/`
获取API基本信息

**响应示例**:
```json
{
  "message": "AI Literature Review API",
  "version": "1.0.0",
  "status": "running"
}
```

#### GET `/api/status`
获取系统健康状态

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-29T10:30:00",
  "agent_initialized": true
}
```

### 2. 文献检索

#### POST `/api/search`
执行文献检索

**请求体**:
```json
{
  "query": "machine learning for drug discovery",
  "sources": ["arxiv", "semantic_scholar"],
  "maxPapers": 20,
  "yearStart": 2020,
  "yearEnd": 2024,
  "retrieveFullText": false,
  "enableAIAnalysis": true
}
```

**响应示例**:
```json
{
  "papers": [
    {
      "title": "论文标题",
      "authors": ["作者1", "作者2"],
      "abstract": "摘要内容",
      "url": "https://example.com/paper",
      "publishedDate": "2023-01-15",
      "source": "arxiv"
    }
  ],
  "summary": "AI生成的综述摘要",
  "keyInsights": ["洞察1", "洞察2"],
  "researchGaps": ["研究空白1", "研究空白2"],
  "statistics": {
    "totalPapers": 20,
    "dateRange": {
      "earliest": "2020-01-01",
      "latest": "2024-12-31"
    }
  }
}
```

### 3. 报告生成

#### POST `/api/generate-report`
生成综述报告

**请求体**:
```json
{
  "papers": [
    {
      "title": "论文标题",
      "authors": ["作者1"],
      "abstract": "摘要"
    }
  ],
  "title": "报告标题",
  "format": "markdown"
}
```

**响应示例**:
```json
{
  "content": "# 报告标题\n\n## 摘要\n...",
  "metadata": {
    "title": "报告标题",
    "format": "markdown",
    "generatedAt": "2025-01-29T10:30:00",
    "paperCount": 10
  }
}
```

### 4. 相似论文搜索

#### POST `/api/search-similar`
搜索相似论文

**请求体**:
```json
{
  "query": "深度学习在医疗诊断中的应用",
  "nResults": 10
}
```

**响应示例**:
```json
{
  "results": [
    {
      "title": "相似论文标题",
      "similarity": 0.85,
      "authors": ["作者1", "作者2"],
      "url": "https://example.com/paper"
    }
  ],
  "query": "深度学习在医疗诊断中的应用",
  "count": 10
}
```

## 错误处理

### 错误响应格式

```json
{
  "error": "错误类型",
  "message": "详细错误信息",
  "timestamp": "2025-01-29T10:30:00"
}
```

### 常见错误码

- **400 Bad Request**: 请求参数无效
- **404 Not Found**: 资源不存在
- **500 Internal Server Error**: 服务器内部错误
- **503 Service Unavailable**: 服务暂时不可用

## 使用示例

### Python 客户端示例

```python
import requests

# 执行文献检索
response = requests.post("http://localhost:8000/api/search", json={
    "query": "artificial intelligence in healthcare",
    "maxPapers": 15,
    "sources": ["arxiv", "semantic_scholar"]
})

if response.status_code == 200:
    results = response.json()
    print(f"找到 {len(results['papers'])} 篇论文")
else:
    print(f"错误: {response.status_code}")
```

### JavaScript 客户端示例

```javascript
// 执行文献检索
fetch('http://localhost:8000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'machine learning for drug discovery',
    maxPapers: 20,
    sources: ['arxiv', 'semantic_scholar']
  })
})
.then(response => response.json())
.then(data => {
  console.log('检索结果:', data);
})
.catch(error => {
  console.error('错误:', error);
});
```

## 速率限制

- 每分钟最多60个请求
- 大型检索任务可能需要更长时间
- 建议在请求之间添加适当的延迟

## 最佳实践

1. **批量处理**: 对于大量论文，建议分批处理
2. **缓存结果**: 相同查询的结果可以缓存以提高性能
3. **错误重试**: 实现指数退避的重试机制
4. **超时设置**: 设置合理的请求超时时间
5. **日志记录**: 记录API调用以便调试和监控
