import axios from 'axios'

// API 基础配置
const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  },
)

// 文献检索接口
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

export interface Paper {
  title: string
  authors: string[]
  publishedDate: string
  source: string
  summary: string
  keywords?: string[]
  url?: string
  pdfUrl?: string
  fullTextRetrieved?: boolean
}

export interface SearchResult {
  papers: Paper[]
  totalCount: number
  processingTime: number
  summary?: string
  actionPlan?: string[] // AI生成的行动计划
}

// 文献检索
export const searchLiterature = async (params: SearchParams): Promise<SearchResult> => {
  try {
    const response = await api.post<SearchResult>('/api/search', params)
    return response.data
  } catch (error) {
    console.error('Search failed:', error)
    throw error
  }
}

// 生成综述报告
export const generateReport = async (papers: Paper[], title: string): Promise<string> => {
  try {
    const response = await api.post<{ report: string }>('/api/generate-report', {
      papers,
      title,
    })
    return response.data.report
  } catch (error) {
    console.error('Report generation failed:', error)
    throw error
  }
}

// 获取系统状态
export const getSystemStatus = async () => {
  try {
    const response = await api.get('/api/status')
    return response
  } catch (error) {
    console.error('Failed to get system status:', error)
    throw error
  }
}

export default api
