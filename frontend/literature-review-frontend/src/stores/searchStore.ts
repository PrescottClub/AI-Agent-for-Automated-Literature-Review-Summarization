import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Paper, SearchParams, SearchHistoryItem } from '@/types/paper'
import { searchLiterature, generateReport } from '@/api/literature'
import { ElMessage } from 'element-plus'

export const useSearchStore = defineStore('search', () => {
  // 搜索状态
  const isSearching = ref(false)
  const isGeneratingReport = ref(false)
  const hasSearched = ref(false)

  // 搜索结果
  const searchResults = ref<Paper[]>([])
  const actionPlan = ref<string[]>([])
  const totalCount = ref(0)
  const processingTime = ref(0)

  // 搜索历史
  const searchHistory = ref<SearchHistoryItem[]>([])

  // 当前搜索查询
  const currentQuery = ref('')
  const searchParams = ref<SearchParams>({
    sources: ['arxiv'], // 只使用ArXiv
    maxPapers: 20,
    retrieveFullText: false,
    enableAIAnalysis: true,
  })

  // 计算属性
  const favoriteResults = computed(() => searchResults.value.filter((paper) => paper.isFavorite))

  const resultsBySource = computed(() => {
    const grouped: Record<string, Paper[]> = {}
    searchResults.value.forEach((paper) => {
      if (!grouped[paper.source]) {
        grouped[paper.source] = []
      }
      grouped[paper.source].push(paper)
    })
    return grouped
  })

  // 搜索方法
  const startSearch = async (query: string, params?: Partial<SearchParams>) => {
    if (!query.trim()) {
      ElMessage.warning('请输入搜索关键词')
      return
    }

    try {
      isSearching.value = true
      hasSearched.value = true
      currentQuery.value = query

      const searchData: SearchParams = {
        ...searchParams.value,
        ...params,
        rawQuery: query,
      }

      const result = await searchLiterature(searchData)

      searchResults.value = result.papers || []
      actionPlan.value = result.actionPlan || []
      totalCount.value = result.totalCount || 0
      processingTime.value = result.processingTime || 0

      // 保存搜索历史
      addToHistory(query, searchData, result.papers?.length || 0)

      ElMessage.success(`检索完成！找到 ${searchResults.value.length} 篇相关文献`)
    } catch (error) {
      console.error('Search error:', error)
      ElMessage.error('检索失败，请检查网络连接或稍后重试')
      searchResults.value = []
      actionPlan.value = []
    } finally {
      isSearching.value = false
    }
  }

  // 添加到搜索历史
  const addToHistory = (query: string, params: SearchParams, resultCount: number) => {
    const historyItem: SearchHistoryItem = {
      query,
      date: new Date().toLocaleDateString('zh-CN'),
      resultCount,
      params,
    }

    searchHistory.value.unshift(historyItem)

    // 只保留最近10次搜索
    if (searchHistory.value.length > 10) {
      searchHistory.value = searchHistory.value.slice(0, 10)
    }

    // 保存到本地存储
    saveHistoryToStorage()
  }

  // 切换收藏状态
  const toggleFavorite = (paperId: string) => {
    const paper = searchResults.value.find((p) => p.id === paperId)
    if (paper) {
      paper.isFavorite = !paper.isFavorite
      ElMessage.success(paper.isFavorite ? '已收藏' : '取消收藏')
    }
  }

  // 生成报告
  const generateLiteratureReport = async (title?: string) => {
    if (searchResults.value.length === 0) {
      ElMessage.warning('没有可用的论文数据生成报告')
      return ''
    }

    try {
      isGeneratingReport.value = true
      const reportTitle = title || `文献综述报告 - ${currentQuery.value}`
      const report = await generateReport(searchResults.value, reportTitle)
      ElMessage.success('报告生成成功')
      return report
    } catch (error) {
      console.error('Report generation error:', error)
      ElMessage.error('报告生成失败')
      return ''
    } finally {
      isGeneratingReport.value = false
    }
  }

  // 重置搜索状态
  const resetSearch = () => {
    searchResults.value = []
    actionPlan.value = []
    currentQuery.value = ''
    hasSearched.value = false
    totalCount.value = 0
    processingTime.value = 0
  }

  // 清空历史记录
  const clearHistory = () => {
    searchHistory.value = []
    localStorage.removeItem('searchHistory')
    ElMessage.success('历史记录已清空')
  }

  // 从本地存储加载历史
  const loadHistoryFromStorage = () => {
    const savedHistory = localStorage.getItem('searchHistory')
    if (savedHistory) {
      try {
        searchHistory.value = JSON.parse(savedHistory)
      } catch (error) {
        console.error('Failed to load search history:', error)
      }
    }
  }

  // 保存历史到本地存储
  const saveHistoryToStorage = () => {
    localStorage.setItem('searchHistory', JSON.stringify(searchHistory.value))
  }

  return {
    // 状态
    isSearching,
    isGeneratingReport,
    hasSearched,
    searchResults,
    actionPlan,
    totalCount,
    processingTime,
    searchHistory,
    currentQuery,
    searchParams,

    // 计算属性
    favoriteResults,
    resultsBySource,

    // 方法
    startSearch,
    toggleFavorite,
    generateLiteratureReport,
    resetSearch,
    clearHistory,
    loadHistoryFromStorage,
    saveHistoryToStorage,
  }
})
