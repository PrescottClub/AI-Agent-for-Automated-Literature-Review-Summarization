<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- 现代化导航栏 -->
    <nav class="bg-white/90 backdrop-blur-xl border-b border-gray-200/50 sticky top-0 z-40 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo区域 -->
          <div class="flex items-center space-x-3 cursor-pointer" @click="goToWelcome">
            <div class="relative">
              <div class="w-10 h-10 bg-gradient-to-r from-indigo-600 to-purple-700 rounded-xl flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow duration-300">
                <span class="text-white text-xl font-bold">T</span>
              </div>
              <div class="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            </div>
            <div>
              <h1 class="text-xl font-bold gradient-text hover:scale-105 transition-transform duration-200">Tsearch</h1>
              <p class="text-xs text-gray-500">AI Literature Discovery</p>
            </div>
          </div>

          <!-- 中间导航链接 -->
          <div class="hidden md:flex items-center space-x-8">
            <router-link to="/search" class="nav-link">
              <el-icon class="mr-1"><Search /></el-icon>
              搜索
            </router-link>
            <router-link to="/about" class="nav-link">
              <el-icon class="mr-1"><Document /></el-icon>
              关于
            </router-link>
          </div>

          <!-- 右侧操作按钮 -->
          <div class="flex items-center space-x-3">
            <!-- 主题切换 -->
            <el-tooltip content="切换主题">
              <button @click="toggleTheme" class="nav-button">
                <el-icon><Sunny v-if="isDarkMode" /><Moon v-else /></el-icon>
              </button>
            </el-tooltip>

            <!-- 系统设置 -->
            <el-tooltip content="系统设置">
              <button @click="showSettings = true" class="nav-button">
                <el-icon><Setting /></el-icon>
              </button>
            </el-tooltip>

            <!-- 使用帮助 -->
            <el-tooltip content="使用帮助">
              <button @click="showHelp = true" class="nav-button">
                <el-icon><QuestionFilled /></el-icon>
              </button>
            </el-tooltip>

            <!-- 历史记录 -->
            <el-tooltip content="历史记录">
              <button @click="showHistory = true" class="nav-button relative">
                <el-icon><Clock /></el-icon>
                <span v-if="searchHistory.length > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {{ searchHistory.length > 9 ? '9+' : searchHistory.length }}
                </span>
              </button>
            </el-tooltip>

            <!-- 移动端菜单 -->
            <button @click="showMobileMenu = !showMobileMenu" class="md:hidden nav-button">
              <el-icon><Menu /></el-icon>
            </button>
          </div>
        </div>

        <!-- 移动端菜单 -->
        <div v-if="showMobileMenu" class="md:hidden border-t border-gray-200 py-4 animate-slide-down">
          <div class="flex flex-col space-y-3">
            <router-link to="/search" class="mobile-nav-link" @click="showMobileMenu = false">
              <el-icon class="mr-2"><Search /></el-icon>
              搜索文献
            </router-link>
            <router-link to="/about" class="mobile-nav-link" @click="showMobileMenu = false">
              <el-icon class="mr-2"><Document /></el-icon>
              关于我们
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 简洁的头部 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">文献搜索</h1>
        <p class="text-gray-600">使用自然语言描述您的研究需求</p>
      </div>

      <!-- 搜索区域 -->
      <div class="max-w-4xl mx-auto mb-8">
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm">
          <!-- 搜索输入框 -->
          <div class="p-6">
            <div class="relative">
              <el-input
                v-model="searchQuery"
                type="textarea"
                :rows="4"
                placeholder="用自然语言描述您的研究需求，例如：我想了解最近三年人工智能在医疗诊断领域的应用进展"
                class="w-full border-0 resize-none"
                @keyup.enter.ctrl="startSearch"
              />
              <div class="absolute bottom-3 right-3 flex items-center space-x-2">
                <span class="text-xs text-gray-400">Ctrl + Enter</span>
                <button
                  @click="startSearch"
                  :disabled="!searchQuery.trim() || isSearching"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <el-icon v-if="isSearching" class="animate-spin mr-1"><Loading /></el-icon>
                  {{ isSearching ? '搜索中...' : '搜索' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 快速建议 -->
          <div class="px-6 pb-4 border-t border-gray-100">
            <div class="flex flex-wrap gap-2 mt-3">
              <button
                v-for="suggestion in naturalLanguageSuggestions.slice(0, 3)"
                :key="suggestion"
                @click="searchQuery = suggestion"
                class="px-3 py-1 text-xs text-gray-600 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
              >
                {{ suggestion }}
              </button>
            </div>
          </div>
        </div>

        <!-- 高级选项（可折叠） -->
        <div v-if="showAdvancedOptions" class="max-w-4xl mx-auto mb-6">
          <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">数据源</label>
                <el-select v-model="selectedSources" multiple placeholder="选择数据源" class="w-full">
                  <el-option label="arXiv" value="arxiv" />
                  <el-option label="Semantic Scholar" value="semantic_scholar" />
                </el-select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">论文数量: {{ maxPapers }}</label>
                <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">选项</label>
                <div class="space-y-2">
                  <el-checkbox v-model="retrieveFullText">获取全文</el-checkbox>
                  <el-checkbox v-model="enableAIAnalysis">AI 分析</el-checkbox>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 高级选项切换 -->
        <div class="max-w-4xl mx-auto mb-8 text-center">
          <button
            @click="showAdvancedOptions = !showAdvancedOptions"
            class="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            {{ showAdvancedOptions ? '隐藏高级选项' : '显示高级选项' }}
            <el-icon class="ml-1" :class="{ 'rotate-180': showAdvancedOptions }">
              <ArrowDown />
            </el-icon>
          </button>
        </div>
      </div>

      <!-- 结果展示区域 -->
      <div v-if="searchResults.length > 0" class="animate-fade-in">
        <!-- 行动计划展示 -->
        <div v-if="actionPlan && actionPlan.length > 0" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 card-shadow mb-6">
          <div class="flex items-center mb-4">
            <el-icon class="text-2xl text-blue-600 mr-3"><TrendCharts /></el-icon>
            <h3 class="text-xl font-bold text-gray-900">🤖 AI生成的行动计划</h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div
              v-for="(step, index) in actionPlan"
              :key="index"
              class="flex items-start p-3 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
            >
              <div class="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-semibold mr-3">
                {{ index + 1 }}
              </div>
              <div class="flex-1 text-sm text-gray-700">
                {{ step }}
              </div>
            </div>
          </div>
          <div class="mt-4 text-xs text-gray-500 text-center">
            💡 此计划由AI根据您的查询自动生成，展示了文献检索和分析的主要步骤
          </div>
        </div>

        <!-- 简洁的结果头部 -->
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">
            找到 {{ searchResults.length }} 篇相关文献
          </h2>
          <div class="flex items-center space-x-3">
            <button
              @click="generateReport"
              :disabled="isGeneratingReport"
              class="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 transition-colors"
            >
              {{ isGeneratingReport ? '生成中...' : '生成报告' }}
            </button>
            <el-select v-model="sortBy" placeholder="排序" size="small" class="w-24">
              <el-option label="相关性" value="relevance" />
              <el-option label="时间" value="date" />
            </el-select>
          </div>
        </div>

        <!-- 论文列表 -->
        <div class="space-y-4">
          <div
            v-for="(paper, index) in searchResults"
            :key="index"
            class="transition-all duration-200"
          >
            <PaperCard :paper="paper" :index="index + 1" @select="togglePaperSelection" />
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!isSearching && hasSearched" class="text-center py-12">
        <el-icon class="text-6xl text-gray-400 mb-4"><DocumentRemove /></el-icon>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">未找到相关文献</h3>
        <p class="text-gray-500 mb-4">请尝试调整搜索关键词或扩大搜索范围</p>
        <el-button type="primary" @click="clearSearch">重新搜索</el-button>
      </div>

      <!-- 加载状态 -->
      <div v-if="isSearching" class="text-center py-12">
        <el-icon class="text-6xl text-blue-500 mb-4 animate-spin"><Loading /></el-icon>
        <h3 class="text-xl font-semibold text-gray-700 mb-2">正在检索文献...</h3>
        <p class="text-gray-500">{{ searchProgress }}</p>
      </div>
    </div>

    <!-- 设置对话框 -->
    <el-dialog v-model="showSettings" title="系统设置" width="600px">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">默认数据源</label>
          <el-checkbox-group v-model="defaultSources">
            <el-checkbox label="arxiv">arXiv</el-checkbox>
            <el-checkbox label="semantic_scholar">Semantic Scholar</el-checkbox>
          </el-checkbox-group>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">默认论文数量</label>
          <el-slider v-model="defaultMaxPapers" :min="5" :max="50" :step="5" show-input />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">语言偏好</label>
          <el-select v-model="language" class="w-full">
            <el-option label="中文" value="zh" />
            <el-option label="English" value="en" />
          </el-select>
        </div>
      </div>
      <template #footer>
        <el-button @click="showSettings = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </template>
    </el-dialog>

    <!-- 帮助对话框 -->
    <el-dialog v-model="showHelp" title="使用帮助" width="800px">
      <div class="space-y-4">
        <h4 class="text-lg font-semibold">如何使用</h4>
        <ol class="list-decimal list-inside space-y-2 text-gray-700">
          <li>在搜索框中输入您的研究主题</li>
          <li>选择合适的数据源和检索参数</li>
          <li>点击"开始检索"按钮</li>
          <li>查看检索结果并进行筛选</li>
          <li>生成综述报告</li>
        </ol>

        <h4 class="text-lg font-semibold mt-6">搜索技巧</h4>
        <ul class="list-disc list-inside space-y-2 text-gray-700">
          <li>使用具体的关键词组合</li>
          <li>尝试不同的同义词</li>
          <li>使用英文关键词可能获得更好的结果</li>
          <li>适当调整年份范围</li>
        </ul>
      </div>
    </el-dialog>

    <!-- 历史记录对话框 -->
    <el-dialog v-model="showHistory" title="搜索历史" width="600px">
      <div v-if="searchHistory.length === 0" class="text-center py-8 text-gray-500">
        暂无搜索历史
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="(item, index) in searchHistory"
          :key="index"
          class="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer"
          @click="loadHistoryItem(item)"
        >
          <div>
            <div class="font-medium">{{ item.query }}</div>
            <div class="text-sm text-gray-500">{{ item.date }} · {{ item.resultCount }} 篇论文</div>
          </div>
          <el-button type="danger" size="small" :icon="Delete" circle @click.stop="removeHistoryItem(index)" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  Document,
  Setting,
  QuestionFilled,
  Clock,
  DataAnalysis,
  DocumentRemove,
  Loading,
  TrendCharts,
  Microphone,
  Download,
  Filter,
  Delete,
  Menu,
  Sunny,
  Moon,
  ArrowDown
} from '@element-plus/icons-vue'
import PaperCard from '../components/PaperCard.vue'

// 定义Paper接口
interface Paper {
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
}

// 定义搜索历史项接口
interface SearchHistoryItem {
  query: string
  date: string
  resultCount: number
  params: {
    sources: string[]
    maxPapers: number
    retrieveFullText: boolean
    enableAIAnalysis: boolean
    yearStart?: number
    yearEnd?: number
  }
}

// 路由
const router = useRouter()

// 响应式数据
const searchQuery = ref('')
const selectedSources = ref(['arxiv', 'semantic_scholar'])
const maxPapers = ref(20)
const yearRange = ref<Date[]>([])
const retrieveFullText = ref(false)
const enableAIAnalysis = ref(true)
const isSearching = ref(false)
const isGeneratingReport = ref(false)
const hasSearched = ref(false)
const searchResults = ref<Paper[]>([])
const searchProgress = ref('')
const actionPlan = ref<string[]>([])  // 新增行动计划数据

// UI 状态
const showSettings = ref(false)
const showHelp = ref(false)
const showHistory = ref(false)
const showFilters = ref(false)
const showMobileMenu = ref(false)
const isDarkMode = ref(false)
const showAdvancedOptions = ref(false)

// 筛选和排序
const sortBy = ref('relevance')
const filterAuthor = ref('')
const filterKeyword = ref('')
const filterSource = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 设置
const defaultSources = ref(['arxiv', 'semantic_scholar'])
const defaultMaxPapers = ref(20)
const language = ref('zh')

// 搜索历史
const searchHistory = ref<SearchHistoryItem[]>([])

// 自然语言搜索建议
const naturalLanguageSuggestions = ref([
  '最近三年人工智能在医疗诊断领域的应用进展',
  '寻找关于深度学习优化算法的最新研究，重点关注transformer架构',
  '查找2020年以来量子计算在密码学中的应用研究',
  '我想了解机器学习在自动驾驶技术中的最新突破',
  '近期区块链技术在金融科技领域的创新应用有哪些',
  '自然语言处理在多语言翻译方面的最新进展'
])

// 年份快捷选项
const yearShortcuts = [
  {
    text: '最近一年',
    value: () => [new Date(new Date().getFullYear() - 1, 0, 1), new Date()]
  },
  {
    text: '最近三年',
    value: () => [new Date(new Date().getFullYear() - 3, 0, 1), new Date()]
  },
  {
    text: '最近五年',
    value: () => [new Date(new Date().getFullYear() - 5, 0, 1), new Date()]
  }
]

// 计算属性
const fullTextCount = computed(() =>
  searchResults.value.filter(paper => paper.fullTextRetrieved).length
)

const totalKeywords = computed(() =>
  searchResults.value.reduce((total, paper) => total + (paper.keywords?.length || 0), 0)
)

const uniqueSources = computed(() =>
  new Set(searchResults.value.map(paper => paper.source)).size
)

const filteredResults = computed(() => {
  let results = [...searchResults.value]

  // 应用筛选
  if (filterAuthor.value) {
    results = results.filter(paper =>
      paper.authors.some((author: string) =>
        author.toLowerCase().includes(filterAuthor.value.toLowerCase())
      )
    )
  }

  if (filterKeyword.value) {
    results = results.filter(paper =>
      paper.keywords?.some((keyword: string) =>
        keyword.toLowerCase().includes(filterKeyword.value.toLowerCase())
      ) || paper.title.toLowerCase().includes(filterKeyword.value.toLowerCase())
    )
  }

  if (filterSource.value) {
    results = results.filter(paper => paper.source === filterSource.value)
  }

  // 应用排序
  if (sortBy.value === 'date') {
    results.sort((a, b) => new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime())
  } else if (sortBy.value === 'citations') {
    results.sort((a, b) => (b.citations || 0) - (a.citations || 0))
  }

  return results
})

// 方法
const startSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  isSearching.value = true
  hasSearched.value = true
  searchProgress.value = '正在连接服务器...'

  try {
    const requestData = {
      rawQuery: searchQuery.value,  // Use natural language query
      sources: selectedSources.value,
      maxPapers: maxPapers.value,
      yearStart: yearRange.value?.[0]?.getFullYear(),
      yearEnd: yearRange.value?.[1]?.getFullYear(),
      retrieveFullText: retrieveFullText.value,
      enableAIAnalysis: enableAIAnalysis.value
    }

    searchProgress.value = '正在检索文献...'

    const response = await fetch('http://localhost:8000/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    searchResults.value = data.papers || []
    actionPlan.value = data.actionPlan || []  // 获取行动计划

    // 保存到搜索历史
    const historyItem: SearchHistoryItem = {
      query: searchQuery.value,
      date: new Date().toLocaleDateString('zh-CN'),
      resultCount: searchResults.value.length,
      params: requestData
    }
    searchHistory.value.unshift(historyItem)
    if (searchHistory.value.length > 10) {
      searchHistory.value = searchHistory.value.slice(0, 10)
    }

    ElMessage.success(`检索完成！找到 ${searchResults.value.length} 篇相关论文`)

  } catch (error) {
    console.error('Search error:', error)
    ElMessage.error('检索失败，请检查网络连接或稍后重试')
  } finally {
    isSearching.value = false
    searchProgress.value = ''
  }
}

const generateReport = async () => {
  if (searchResults.value.length === 0) {
    ElMessage.warning('没有可用的论文数据')
    return
  }

  isGeneratingReport.value = true

  try {
    const response = await fetch('http://localhost:8000/api/generate-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        papers: searchResults.value,
        title: `${searchQuery.value} - 文献综述报告`
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    // 显示报告内容
    ElMessageBox.alert(data.report, '综述报告', {
      dangerouslyUseHTMLString: false,
      customClass: 'report-dialog'
    })

  } catch (error) {
    console.error('Report generation error:', error)
    ElMessage.error('报告生成失败，请稍后重试')
  } finally {
    isGeneratingReport.value = false
  }
}

const startVoiceInput = () => {
  ElMessage.info('语音输入功能开发中...')
}

const exportResults = () => {
  const dataStr = JSON.stringify(searchResults.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `literature_search_${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
  ElMessage.success('结果已导出')
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  actionPlan.value = []  // 清除行动计划
  hasSearched.value = false
}

const togglePaperSelection = (paper: Paper) => {
  // 实现论文选择功能
  ElMessage.info('论文选择功能开发中...')
}

const saveSettings = () => {
  selectedSources.value = [...defaultSources.value]
  maxPapers.value = defaultMaxPapers.value
  showSettings.value = false
  ElMessage.success('设置已保存')
}

const loadHistoryItem = (item: SearchHistoryItem) => {
  searchQuery.value = item.query
  selectedSources.value = item.params.sources
  maxPapers.value = item.params.maxPapers
  retrieveFullText.value = item.params.retrieveFullText
  enableAIAnalysis.value = item.params.enableAIAnalysis
  showHistory.value = false
  ElMessage.success('已加载历史搜索')
}

const removeHistoryItem = (index: number) => {
  searchHistory.value.splice(index, 1)
  ElMessage.success('已删除历史记录')
}

const handlePageChange = (page: number) => {
  currentPage.value = page
}

// 新增方法
const goToWelcome = () => {
  router.push('/')
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  // 这里可以添加主题切换逻辑
  ElMessage.info(isDarkMode.value ? '已切换到深色模式' : '已切换到浅色模式')
}

// 生命周期
onMounted(() => {
  // 加载保存的设置
  const savedSettings = localStorage.getItem('literatureReviewSettings')
  if (savedSettings) {
    const settings = JSON.parse(savedSettings)
    defaultSources.value = settings.defaultSources || ['arxiv', 'semantic_scholar']
    defaultMaxPapers.value = settings.defaultMaxPapers || 20
    language.value = settings.language || 'zh'
  }

  // 加载搜索历史
  const savedHistory = localStorage.getItem('searchHistory')
  if (savedHistory) {
    searchHistory.value = JSON.parse(savedHistory)
  }
})

// 监听设置变化并保存
watch([defaultSources, defaultMaxPapers, language], () => {
  const settings = {
    defaultSources: defaultSources.value,
    defaultMaxPapers: defaultMaxPapers.value,
    language: language.value
  }
  localStorage.setItem('literatureReviewSettings', JSON.stringify(settings))
}, { deep: true })

// 监听搜索历史变化并保存
watch(searchHistory, () => {
  localStorage.setItem('searchHistory', JSON.stringify(searchHistory.value))
}, { deep: true })
</script>

<style scoped>
/* 组件特定样式 */
.transition-transform {
  transition: transform 0.3s ease;
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

.hover\:scale-\[1\.02\]:hover {
  transform: scale(1.02);
}

/* 报告对话框样式 */
:deep(.report-dialog) {
  max-width: 80vw;
  max-height: 80vh;
}

:deep(.report-dialog .el-message-box__content) {
  max-height: 60vh;
  overflow-y: auto;
  white-space: pre-wrap;
  font-family: monospace;
}

/* 动画优化 */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 导航样式 */
.nav-link {
  @apply flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200;
}

.nav-link.router-link-active {
  @apply text-blue-600 bg-blue-50;
}

.nav-button {
  @apply w-10 h-10 flex items-center justify-center text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200;
}

.mobile-nav-link {
  @apply flex items-center px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200;
}
</style>
