<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- 导航栏 -->
    <nav class="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-indigo-600 to-purple-700 rounded-xl flex items-center justify-center">
              <span class="text-white text-xl font-bold">T</span>
            </div>
            <div>
              <h1 class="text-xl font-bold gradient-text">Tsearch</h1>
              <p class="text-xs text-gray-500">Terence's AI Literature Discovery</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <el-tooltip content="系统设置">
              <el-button type="primary" :icon="Setting" circle @click="showSettings = true" />
            </el-tooltip>
            <el-tooltip content="使用帮助">
              <el-button type="info" :icon="QuestionFilled" circle @click="showHelp = true" />
            </el-tooltip>
            <el-tooltip content="历史记录">
              <el-button type="success" :icon="Clock" circle @click="showHistory = true" />
            </el-tooltip>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 头部介绍区域 -->
      <div class="text-center mb-12 animate-fade-in">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          � Tsearch - 智能文献发现引擎
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          专为Terence打造的AI驱动文献搜索平台，让学术研究更高效、更精准
        </p>

        <!-- 特性卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up hover:scale-105 transition-transform">
            <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-blue-600 text-2xl"><Search /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">智能检索</h3>
            <p class="text-gray-600">多数据源检索，语义理解，精准匹配</p>
          </div>

          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up hover:scale-105 transition-transform" style="animation-delay: 0.1s">
            <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-green-600 text-2xl"><DataAnalysis /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">AI 分析</h3>
            <p class="text-gray-600">深度分析文献内容，提取关键信息</p>
          </div>

          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up hover:scale-105 transition-transform" style="animation-delay: 0.2s">
            <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-purple-600 text-2xl"><Document /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">智能总结</h3>
            <p class="text-gray-600">生成专业的文献综述报告</p>
          </div>

          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up hover:scale-105 transition-transform" style="animation-delay: 0.3s">
            <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-orange-600 text-2xl"><TrendCharts /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">趋势分析</h3>
            <p class="text-gray-600">识别研究热点和发展趋势</p>
          </div>
        </div>
      </div>

      <!-- 搜索区域 -->
      <div class="bg-white rounded-3xl p-8 card-shadow mb-8 animate-bounce-in">
        <div class="max-w-4xl mx-auto">
          <h3 class="text-2xl font-bold text-gray-900 mb-6 text-center">开始您的文献综述</h3>

          <div class="space-y-6">
            <!-- 搜索输入 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">研究主题</label>
              <el-input
                v-model="searchQuery"
                placeholder="请输入您的研究主题，例如：人工智能在医疗领域的应用"
                size="large"
                class="w-full"
                :prefix-icon="Search"
                @keyup.enter="startSearch"
              >
                <template #append>
                  <el-button :icon="Microphone" @click="startVoiceInput" />
                </template>
              </el-input>
              <!-- 快速搜索建议 -->
              <div class="mt-2 flex flex-wrap gap-2">
                <el-tag
                  v-for="suggestion in searchSuggestions"
                  :key="suggestion"
                  class="cursor-pointer hover:bg-blue-100"
                  @click="searchQuery = suggestion"
                >
                  {{ suggestion }}
                </el-tag>
              </div>
            </div>

            <!-- 配置选项 -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">数据源</label>
                <el-select v-model="selectedSources" multiple placeholder="选择数据源" class="w-full">
                  <el-option label="arXiv" value="arxiv">
                    <span class="flex items-center">
                      <el-icon class="mr-2"><Document /></el-icon>
                      arXiv
                    </span>
                  </el-option>
                  <el-option label="Semantic Scholar" value="semantic_scholar">
                    <span class="flex items-center">
                      <el-icon class="mr-2"><Search /></el-icon>
                      Semantic Scholar
                    </span>
                  </el-option>
                </el-select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">论文数量: {{ maxPapers }}</label>
                <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" show-input />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">年份范围</label>
                <el-date-picker
                  v-model="yearRange"
                  type="yearrange"
                  placeholder="选择年份范围"
                  class="w-full"
                  :shortcuts="yearShortcuts"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">其他选项</label>
                <div class="space-y-2">
                  <el-checkbox v-model="retrieveFullText">
                    <span class="flex items-center">
                      <el-icon class="mr-1"><Download /></el-icon>
                      获取全文
                    </span>
                  </el-checkbox>
                  <el-checkbox v-model="enableAIAnalysis">
                    <span class="flex items-center">
                      <el-icon class="mr-1"><DataAnalysis /></el-icon>
                      AI 深度分析
                    </span>
                  </el-checkbox>
                </div>
              </div>
            </div>

            <!-- 搜索按钮 -->
            <div class="text-center">
              <el-button
                type="primary"
                size="large"
                :loading="isSearching"
                @click="startSearch"
                class="px-12 py-3 text-lg font-semibold rounded-xl mr-4"
                :disabled="!searchQuery.trim()"
              >
                <el-icon class="mr-2"><Search /></el-icon>
                {{ isSearching ? '正在检索...' : '开始检索' }}
              </el-button>

              <el-button
                v-if="searchResults.length > 0"
                type="success"
                size="large"
                @click="generateReport"
                :loading="isGeneratingReport"
                class="px-8 py-3 text-lg font-semibold rounded-xl"
              >
                <el-icon class="mr-2"><Document /></el-icon>
                {{ isGeneratingReport ? '生成中...' : '生成报告' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 结果展示区域 -->
      <div v-if="searchResults.length > 0" class="animate-fade-in">
        <!-- 统计信息和操作栏 -->
        <div class="bg-white rounded-2xl p-6 card-shadow mb-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-gray-900">检索结果</h3>
            <div class="flex items-center space-x-2">
              <el-select v-model="sortBy" placeholder="排序方式" class="w-32">
                <el-option label="相关性" value="relevance" />
                <el-option label="时间" value="date" />
                <el-option label="引用数" value="citations" />
              </el-select>
              <el-button :icon="Filter" @click="showFilters = !showFilters">筛选</el-button>
              <el-button :icon="Download" @click="exportResults">导出</el-button>
            </div>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center">
              <div class="text-3xl font-bold text-blue-600">{{ searchResults.length }}</div>
              <div class="text-sm text-gray-600">检索到的论文</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-green-600">{{ fullTextCount }}</div>
              <div class="text-sm text-gray-600">获取全文</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-purple-600">{{ totalKeywords }}</div>
              <div class="text-sm text-gray-600">关键词总数</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-orange-600">{{ uniqueSources }}</div>
              <div class="text-sm text-gray-600">数据源</div>
            </div>
          </div>
        </div>

        <!-- 筛选器 -->
        <div v-if="showFilters" class="bg-white rounded-2xl p-6 card-shadow mb-6 animate-slide-up">
          <h4 class="text-lg font-semibold mb-4">高级筛选</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">作者</label>
              <el-input v-model="filterAuthor" placeholder="输入作者姓名" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">关键词</label>
              <el-input v-model="filterKeyword" placeholder="输入关键词" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">数据源</label>
              <el-select v-model="filterSource" placeholder="选择数据源" class="w-full">
                <el-option label="全部" value="" />
                <el-option label="arXiv" value="arxiv" />
                <el-option label="Semantic Scholar" value="semantic_scholar" />
              </el-select>
            </div>
          </div>
        </div>

        <!-- 论文列表 -->
        <div class="space-y-4">
          <div
            v-for="(paper, index) in filteredResults"
            :key="index"
            class="bg-white rounded-2xl p-6 card-shadow animate-slide-up hover:scale-[1.02] transition-all duration-300"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <PaperCard :paper="paper" :index="index + 1" @select="togglePaperSelection" />
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="filteredResults.length > pageSize" class="flex justify-center mt-8">
          <el-pagination
            :current-page="currentPage"
            @current-change="handlePageChange"
            :page-size="pageSize"
            :total="filteredResults.length"
            layout="prev, pager, next, jumper"
            class="bg-white rounded-xl p-4 card-shadow"
          />
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
  Delete
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

// UI 状态
const showSettings = ref(false)
const showHelp = ref(false)
const showHistory = ref(false)
const showFilters = ref(false)

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

// 搜索建议
const searchSuggestions = ref([
  '人工智能在医疗领域的应用',
  '机器学习算法优化',
  '深度学习图像识别',
  '自然语言处理技术',
  '区块链技术应用',
  '量子计算发展'
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
      query: searchQuery.value,
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
</style>
