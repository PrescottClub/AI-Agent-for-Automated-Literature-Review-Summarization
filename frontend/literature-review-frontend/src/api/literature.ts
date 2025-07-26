import axios from 'axios'

// API 基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 120000  // 增加到2分钟

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.data)
    // 可以在这里添加认证 token
    return config
  },
  (error) => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  },
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('API Error Details:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url,
      method: error.config?.method,
    })
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

import type { Paper } from '@/types/paper'

export type { Paper }

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

// 测试API连接
export const testApiConnection = async () => {
  try {
    console.log('Testing API connection to:', API_BASE_URL)
    const response = await api.get('/health')
    console.log('Health check successful:', response.data)
    return response.data
  } catch (error) {
    console.error('API connection test failed:', error)
    throw error
  }
}

export default api
