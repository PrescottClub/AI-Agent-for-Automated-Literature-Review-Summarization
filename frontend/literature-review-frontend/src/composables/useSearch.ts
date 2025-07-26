import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { SearchParams } from '@/types/paper'

// 搜索建议数据
const searchSuggestions = [
  '最近三年人工智能在医疗诊断领域的应用进展',
  '深度学习优化算法的最新研究，重点关注transformer架构',
  '2020年以来量子计算在密码学中的应用研究',
  '机器学习在气候变化预测中的应用现状与挑战',
  '区块链技术在供应链管理中的创新应用',
  '自然语言处理在智能客服系统中的技术突破',
  '计算机视觉在自动驾驶汽车中的关键技术',
  '生物信息学中的大数据分析方法与工具',
]

// 数据源选项 - 只支持ArXiv
const sourceOptions = [
  { label: 'arXiv', value: 'arxiv', description: '物理学、数学、计算机科学等预印本' },
  // 其他数据源暂不支持
  // { label: 'PubMed', value: 'pubmed', description: '生物医学文献数据库' },
  // { label: 'IEEE Xplore', value: 'ieee', description: '工程技术和计算机科学' },
  // { label: 'ACM Digital Library', value: 'acm', description: '计算机科学专业数据库' },
]

// 搜索进度步骤
const searchProgressSteps = [
  '解析查询意图',
  '构建搜索策略',
  '并行查询数据库',
  '筛选相关文献',
  '相关性排序',
  '生成摘要洞察',
]

export function useSearch() {
  // 搜索状态
  const isSearching = ref(false)
  const searchProgress = ref('')
  const currentProgressStep = ref(0)

  // 搜索参数 - 只使用ArXiv
  const searchParams = ref<SearchParams>({
    sources: ['arxiv'],
    maxPapers: 20,
    retrieveFullText: false,
    enableAIAnalysis: true,
  })

  // 计算属性
  const selectedSourceLabels = computed(() => {
    return searchParams.value.sources.map((source) => {
      const option = sourceOptions.find((opt) => opt.value === source)
      return option?.label || source
    })
  })

  // 验证搜索查询
  const validateQuery = (query: string): boolean => {
    if (!query.trim()) {
      ElMessage.warning('请输入搜索关键词')
      return false
    }

    if (query.length < 3) {
      ElMessage.warning('搜索关键词至少需要3个字符')
      return false
    }

    if (query.length > 500) {
      ElMessage.warning('搜索查询过长，请控制在500字符以内')
      return false
    }

    return true
  }

  // 生成智能搜索建议
  const generateSearchSuggestions = (currentQuery: string = '') => {
    if (!currentQuery.trim()) {
      return searchSuggestions.slice(0, 6)
    }

    // 基于当前查询生成相关建议
    const keywords = currentQuery.toLowerCase().split(/\s+/)
    const relevantSuggestions = searchSuggestions.filter((suggestion) => {
      return keywords.some((keyword) => suggestion.toLowerCase().includes(keyword))
    })

    return relevantSuggestions.length > 0
      ? relevantSuggestions.slice(0, 3)
      : searchSuggestions.slice(0, 3)
  }

  // 模拟搜索进度
  const simulateSearchProgress = async () => {
    currentProgressStep.value = 0

    for (let i = 0; i < searchProgressSteps.length; i++) {
      currentProgressStep.value = i
      searchProgress.value = searchProgressSteps[i]

      // 模拟每个步骤的处理时间
      const delay = Math.random() * 800 + 200 // 200-1000ms
      await new Promise((resolve) => setTimeout(resolve, delay))
    }

    currentProgressStep.value = searchProgressSteps.length
  }

  // 格式化搜索参数
  const formatSearchParams = (
    query: string,
    customParams?: Partial<SearchParams>,
  ): SearchParams => {
    return {
      ...searchParams.value,
      ...customParams,
      rawQuery: query,
      query: query.length > 100 ? undefined : query, // 长查询使用rawQuery
    }
  }

  // 获取搜索历史建议
  const getHistoryBasedSuggestions = (searchHistory: { query: string }[]) => {
    if (searchHistory.length === 0) return []

    // 提取历史搜索中的关键词
    const historicalKeywords = searchHistory
      .slice(0, 5) // 只考虑最近5次搜索
      .map((item) => item.query)
      .join(' ')
      .split(/\s+/)
      .filter((word) => word.length > 2)

    // 基于历史关键词推荐相关搜索
    return generateSearchSuggestions(historicalKeywords.join(' '))
  }

  return {
    // 状态
    isSearching,
    searchProgress,
    currentProgressStep,
    searchParams,

    // 数据
    sourceOptions,
    searchProgressSteps,

    // 计算属性
    selectedSourceLabels,

    // 方法
    validateQuery,
    generateSearchSuggestions,
    simulateSearchProgress,
    formatSearchParams,
    getHistoryBasedSuggestions,
  }
}
