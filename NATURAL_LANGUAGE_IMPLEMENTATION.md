# AI Agent 自然语言查询处理实现报告

## 概述

本次实现成功为 AI Agent 添加了自然语言查询处理功能，使用户能够用自然语言描述研究需求，系统会自动提取关键参数并执行文献检索。

## 核心功能

### 1. 自然语言参数提取
- **位置**: `src/lit_review_agent/ai_core/llm_manager.py`
- **方法**: `extract_core_research_params()`
- **功能**: 从用户的自然语言查询中提取：
  - `topic`: 主要研究主题
  - `time_limit`: 时间限制（如"最近三年"、"2020年以来"）
  - `focus`: 特定关注点或关键词

### 2. 智能时间解析
- 支持多种时间表达方式：
  - "最近一年" → 设置为去年到今年
  - "最近三年" → 设置为三年前到今年
  - "since 2020" → 设置为2020年到今年
  - "2020 to 2023" → 设置为具体年份范围

### 3. 查询增强
- 自动将关注重点融入主题搜索
- 保持向后兼容性，支持传统结构化查询

## 实现的文件修改

### 1. LLM Manager (`src/lit_review_agent/ai_core/llm_manager.py`)
```python
async def extract_core_research_params(self, query: str) -> Dict[str, Optional[str]]
```
- 使用精心设计的提示词指导LLM提取参数
- 包含JSON解析和错误处理
- 提供回退机制确保系统稳定性

### 2. 主Agent类 (`src/lit_review_agent/agent.py`)
```python
async def conduct_literature_review(
    self,
    research_topic: str = None,
    raw_query: str = None,
    # ... 其他参数
)
```
- 新增 `raw_query` 参数支持自然语言输入
- 保持 `research_topic` 参数向后兼容
- 集成参数提取和时间解析逻辑

### 3. API服务器 (`src/lit_review_agent/api_server.py`)
```python
class SearchRequest(BaseModel):
    query: Optional[str] = None  # 传统查询
    rawQuery: Optional[str] = None  # 自然语言查询
    # ... 其他字段
```
- 支持两种查询方式
- 自动选择合适的处理方法

### 4. 前端界面 (`frontend/literature-review-frontend/src/views/HomeView.vue`)
- 将单行输入框改为多行文本区域
- 更新占位符文本提供自然语言示例
- 修改API调用使用 `rawQuery` 字段
- 添加智能提示和快速模板

### 5. Streamlit应用 (`src/lit_review_agent/app.py`)
- 更新输入组件为文本区域
- 修改查询处理逻辑使用自然语言

### 6. MCP服务器 (`src/lit_review_agent/mcp_server.py`)
- 添加 `raw_query` 参数支持
- 保持向后兼容性

## 使用示例

### 自然语言查询示例
```
我想了解最近三年人工智能在医疗诊断领域的应用进展
```
**系统解析结果**:
- topic: "人工智能在医疗诊断领域的应用"
- time_limit: "最近三年"
- focus: null

```
寻找关于深度学习优化算法的最新研究，重点关注transformer架构
```
**系统解析结果**:
- topic: "深度学习优化算法"
- time_limit: "最新"
- focus: "transformer架构"

### API调用示例
```javascript
// 新的自然语言方式
const response = await fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    rawQuery: "我想了解最近三年人工智能在医疗诊断领域的应用进展",
    sources: ["arxiv", "semantic_scholar"],
    maxPapers: 20
  })
});

// 传统方式仍然支持
const response = await fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "artificial intelligence medical diagnosis",
    sources: ["arxiv", "semantic_scholar"],
    maxPapers: 20,
    yearStart: 2021,
    yearEnd: 2024
  })
});
```

## 测试

创建了测试脚本 `test_natural_language.py` 用于验证功能：
- 参数提取测试
- 完整流程测试
- API兼容性测试

## 优势

1. **用户友好**: 用户可以用自然语言描述需求，无需学习特定语法
2. **智能解析**: 自动识别时间范围、关注重点等参数
3. **向后兼容**: 保持对现有API和界面的完全兼容
4. **错误处理**: 完善的错误处理和回退机制
5. **多语言支持**: 支持中文和英文自然语言查询

## 技术特点

1. **LLM驱动**: 使用大语言模型进行智能参数提取
2. **JSON结构化**: 标准化的参数提取格式
3. **时间智能**: 自动解析各种时间表达方式
4. **查询增强**: 自动优化搜索查询
5. **渐进式增强**: 在现有架构基础上添加新功能

## 下一步优化建议

1. **增强时间解析**: 支持更复杂的时间表达
2. **领域识别**: 自动识别研究领域并推荐相关数据源
3. **查询优化**: 基于历史数据优化查询效果
4. **多轮对话**: 支持澄清和细化查询需求
5. **个性化**: 基于用户历史偏好调整解析策略

## 结论

本次实现成功为AI Agent添加了强大的自然语言查询处理能力，大大提升了用户体验，同时保持了系统的稳定性和兼容性。用户现在可以用自然语言描述研究需求，系统会智能地理解并执行相应的文献检索任务。
