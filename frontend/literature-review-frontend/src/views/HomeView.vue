<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50/30">
    <!-- 现代化导航栏 -->
    <nav class="bg-white/80 backdrop-blur-xl border-b border-slate-200/50 sticky top-0 z-40 shadow-sm shadow-slate-200/20">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex justify-between items-center h-16">
          <!-- Logo区域 -->
          <div class="flex items-center space-x-4 cursor-pointer group" @click="goToWelcome">
            <div class="w-9 h-9 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 rounded-xl flex items-center justify-center relative overflow-hidden shadow-lg shadow-blue-500/25 transition-all duration-300 group-hover:shadow-xl group-hover:shadow-blue-500/40 group-hover:scale-105">
              <!-- 动态光效 -->
              <div class="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent"></div>
              <div class="absolute top-1 right-1 w-1 h-1 bg-white/40 rounded-full"></div>
              <div class="absolute bottom-1 left-1 w-0.5 h-0.5 bg-white/30 rounded-full"></div>
              <!-- T字母 -->
              <span class="text-white text-sm font-bold relative z-10">T</span>
            </div>
            <div>
              <span class="text-lg font-bold gradient-text">Tsearch</span>
              <p class="text-xs text-slate-500 font-medium -mt-1">AI Literature Discovery</p>
            </div>
          </div>

          <!-- 右侧操作按钮 -->
          <div class="flex items-center space-x-3">
            <!-- 历史记录 -->
            <button @click="showHistory = true" class="nav-button relative group">
              <el-icon><Clock /></el-icon>
              <span v-if="searchHistory.length > 0" class="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
              <span class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">历史记录</span>
            </button>

            <!-- 系统设置 -->
            <button @click="showSettings = true" class="nav-button relative group">
              <el-icon><Setting /></el-icon>
              <span class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">设置</span>
            </button>

            <!-- 移动端菜单 -->
            <button @click="showMobileMenu = !showMobileMenu" class="md:hidden nav-button">
              <el-icon><Menu /></el-icon>
            </button>
          </div>
        </div>

        <!-- 移动端菜单 -->
        <div v-if="showMobileMenu" class="md:hidden border-t border-gray-100 py-3">
          <div class="flex flex-col space-y-2">
            <button @click="showHistory = true; showMobileMenu = false" class="mobile-nav-link">
              历史记录
            </button>
            <button @click="showSettings = true; showMobileMenu = false" class="mobile-nav-link">
              设置
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <div class="max-w-5xl mx-auto px-6 py-16">
      <!-- 现代化头部 -->
      <div class="text-center mb-16">
        <div class="inline-flex items-center px-4 py-2 bg-blue-50 border border-blue-200 rounded-full text-blue-700 text-sm font-medium mb-6">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          智能文献搜索
        </div>
        <h1 class="text-4xl md:text-5xl font-bold gradient-text mb-6 leading-tight">
          发现学术
          <span class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">洞察</span>
        </h1>
        <p class="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">使用自然语言描述您的研究需求，AI将为您找到最相关的学术文献</p>
      </div>

      <!-- 现代化搜索区域 -->
      <div class="mb-16">
        <div class="relative bg-white/80 backdrop-blur-sm border border-slate-200/50 rounded-3xl shadow-xl shadow-slate-200/20 overflow-hidden">
          <!-- 搜索输入框 -->
          <div class="p-8">
            <div class="relative">
              <el-input
                v-model="searchQuery"
                type="textarea"
                :rows="4"
                placeholder="用自然语言描述您的研究需求，例如：我想了解最近三年人工智能在医疗诊断领域的应用进展"
                class="w-full border-0 resize-none text-lg"
                @keyup.enter.ctrl="startSearch"
              />
              <!-- 搜索按钮 -->
              <div class="flex items-center justify-between mt-6">
                <div class="flex items-center space-x-2 text-sm text-slate-500">
                  <kbd class="px-2 py-1 bg-slate-100 rounded text-xs">Ctrl</kbd>
                  <span>+</span>
                  <kbd class="px-2 py-1 bg-slate-100 rounded text-xs">Enter</kbd>
                  <span>快速搜索</span>
                </div>
                <button
                  @click="startSearch"
                  :disabled="!searchQuery.trim() || isSearching"
                  class="group relative px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl font-semibold shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:scale-105 overflow-hidden"
                >
                  <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <span class="relative flex items-center">
                    <el-icon v-if="isSearching" class="animate-spin mr-2"><Loading /></el-icon>
                    {{ isSearching ? '搜索中...' : '开始搜索' }}
                    <svg v-if="!isSearching" class="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>

          <!-- 快速建议 -->
          <div class="px-8 pb-6 border-t border-slate-100">
            <div class="flex flex-wrap gap-3 mt-4">
              <span class="text-sm text-slate-500 font-medium">快速开始：</span>
              <button
                v-for="suggestion in naturalLanguageSuggestions.slice(0, 2)"
                :key="suggestion"
                @click="searchQuery = suggestion"
                class="px-4 py-2 text-sm text-slate-600 bg-slate-50 hover:bg-slate-100 rounded-xl transition-colors border border-slate-200 hover:border-slate-300"
              >
                {{ suggestion }}
              </button>
            </div>
          </div>
        </div>

        <!-- 高级选项（可折叠） -->
        <div v-if="showAdvancedOptions" class="mb-8">
          <div class="border border-gray-200 rounded-lg p-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
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
        <div class="mb-8 text-center">
          <button
            @click="showAdvancedOptions = !showAdvancedOptions"
            class="text-sm text-gray-600 hover:text-gray-900 transition-colors flex items-center mx-auto"
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
        <div v-if="actionPlan && actionPlan.length > 0" class="bg-gray-50 rounded-lg p-4 mb-6">
          <div class="flex items-center mb-3">
            <el-icon class="text-lg text-gray-600 mr-2"><TrendCharts /></el-icon>
            <h3 class="text-base font-medium text-gray-900">AI生成的行动计划</h3>
          </div>
          <div class="space-y-2">
            <div
              v-for="(step, index) in actionPlan"
              :key="index"
              class="flex items-start p-2 bg-white rounded border border-gray-100"
            >
              <div class="flex-shrink-0 w-6 h-6 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center text-xs font-medium mr-3 mt-0.5">
                {{ index + 1 }}
              </div>
              <div class="flex-1 text-sm text-gray-700">
                {{ step }}
              </div>
            </div>
          </div>
          <div class="mt-3 text-xs text-gray-500">
            此计划由AI根据您的查询自动生成
          </div>
        </div>

        <!-- 简洁的结果头部 -->
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-medium text-gray-900">
            找到 {{ searchResults.length }} 篇相关文献
          </h2>
          <div class="flex items-center space-x-3">
            <button
              @click="generateReport"
              :disabled="isGeneratingReport"
              class="px-3 py-1.5 bg-gray-900 text-white rounded-md text-sm font-medium hover:bg-gray-800 disabled:opacity-50 transition-colors"
            >
              {{ isGeneratingReport ? '生成中...' : '生成报告' }}
            </button>
            <el-select v-model="sortBy" placeholder="排序" size="small" class="w-20">
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
  Setting,
  Clock,
  DocumentRemove,
  Loading,
  TrendCharts,
  Delete,
  Menu,
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

/* 现代化导航样式 */
.nav-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(226, 232, 240, 0.5);
}

.nav-button:hover {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  color: #374151;
  border-radius: 6px;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;
  border: none;
  background: none;
  font-size: 14px;
}

.mobile-nav-link:hover {
  background-color: #f3f4f6;
}
</style>
