// 论文接口定义
export interface Paper {
  id: string
  title: string
  authors: string[]
  publishedDate: string
  source: string
  summary: string
  keywords?: string[]
  url?: string
  pdfUrl?: string
  fullTextRetrieved?: boolean
  citations?: number
  isFavorite?: boolean
}

// 搜索参数接口
export interface SearchParams {
  query?: string // 传统结构化查询
  rawQuery?: string // 自然语言查询
  sources: string[]
  maxPapers: number
  yearStart?: number
  yearEnd?: number
  retrieveFullText: boolean
  enableAIAnalysis: boolean
}

// 搜索结果接口
export interface SearchResult {
  papers: Paper[]
  totalCount: number
  processingTime: number
  summary?: string
  actionPlan?: string[] // AI生成的行动计划
}

// 搜索历史项接口
export interface SearchHistoryItem {
  query: string
  date: string
  resultCount: number
  params: SearchParams
}

// 应用设置接口
export interface AppSettings {
  defaultSources: string[]
  defaultMaxPapers: number
  language: 'zh' | 'en'
  theme: 'light' | 'dark' | 'auto'
}
