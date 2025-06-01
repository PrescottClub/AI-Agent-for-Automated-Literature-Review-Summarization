<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Bar - Simplified for Gemini style -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex justify-between items-center h-16">
          <!-- Logo Area - Simplified -->
          <div class="flex items-center space-x-3 cursor-pointer group" @click="goToWelcome">
            <div class="w-9 h-9 bg-primary-DEFAULT rounded-lg flex items-center justify-center shadow-sm transition-all duration-300 group-hover:shadow-md group-hover:scale-105">
              <!-- Simplified or generic icon if T is too specific, or keep T with simple styling -->
              <span class="text-white text-lg font-semibold">T</span>
            </div>
            <div>
              <!-- Removed gradient-text, use primary or darker gray color -->
              <span class="text-xl font-semibold text-gray-800">Tsearch</span>
              <p class="text-xs text-gray-500 font-medium -mt-0.5">AI Literature Discovery</p>
            </div>
          </div>

          <!-- Right Action Buttons - Simplified -->
          <div class="hidden md:flex items-center space-x-2">
            <button @click="showHistory = true" class="nav-button-gemini">
              <el-icon :size="20"><Clock /></el-icon>
              <span class="ml-1 text-sm">历史</span>
            </button>
            <button @click="showSettings = true" class="nav-button-gemini">
              <el-icon :size="20"><Setting /></el-icon>
              <span class="ml-1 text-sm">设置</span>
            </button>
          </div>

          <!-- Mobile Menu Button -->
          <div class="md:hidden">
            <button @click="showMobileMenu = !showMobileMenu" class="p-2 rounded-md text-gray-600 hover:text-gray-800 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-DEFAULT">
              <el-icon :size="24"><Menu /></el-icon>
            </button>
          </div>
        </div>

        <!-- Mobile Menu -->
        <div v-if="showMobileMenu" class="md:hidden border-t border-gray-200 py-2">
          <div class="flex flex-col space-y-1">
            <button @click="showHistory = true; showMobileMenu = false" class="mobile-nav-link-gemini">
              历史记录
            </button>
            <button @click="showSettings = true; showMobileMenu = false" class="mobile-nav-link-gemini">
              设置
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-10 sm:py-12">
      <!-- Header Section - Simplified -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center px-3 py-1 bg-primary-50 border border-primary-200 rounded-full text-primary-700 text-xs sm:text-sm font-medium mb-4">
          <el-icon class="mr-2"><Search /></el-icon> <!-- Using a generic search or lightbulb icon -->
          智能文献搜索
        </div>
        <!-- Removed gradient-text, use standard text colors -->
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-800 mb-4 leading-tight">
          发现学术 <span class="text-primary-DEFAULT">洞察</span>
        </h1>
        <p class="text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          使用自然语言描述您的研究需求，AI将为您找到最相关的学术文献
        </p>
      </div>

      <!-- Search Area - Simplified -->
      <div class="mb-12">
        <!-- Simplified card style -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <!-- Search Input -->
          <div class="p-4 sm:p-6">
            <el-input
              v-model="searchQuery"
              type="textarea"
              :autosize="{ minRows: 3, maxRows: 6 }"
              placeholder="用自然语言描述您的研究需求，例如：我想了解最近三年人工智能在医疗诊断领域的应用进展"
              class="w-full resize-none focus:border-primary-DEFAULT focus:ring-primary-DEFAULT"
              @keyup.enter.ctrl="startSearch"
            />
            <!-- Search Button and Shortcut Hint -->
            <div class="flex flex-col sm:flex-row items-center justify-between mt-4">
              <div class="flex items-center space-x-1 text-xs text-gray-500 mb-2 sm:mb-0">
                <kbd class="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded text-gray-700 font-mono">Ctrl</kbd>
                <span>+</span>
                <kbd class="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded text-gray-700 font-mono">Enter</kbd>
                <span>进行搜索</span>
              </div>
              <button
                @click="startSearch"
                :disabled="!searchQuery.trim() || isSearching"
                class="w-full sm:w-auto el-button el-button--primary"
              >
                <el-icon v-if="isSearching" class="animate-spin mr-1"><Loading /></el-icon>
                {{ isSearching ? '搜索中...' : '搜索文献' }}
              </button>
            </div>
          </div>

          <!-- Quick Suggestions - Simplified -->
          <div v-if="naturalLanguageSuggestions.length > 0" class="px-4 sm:px-6 pt-3 pb-4 border-t border-gray-200">
            <div class="flex flex-wrap gap-2">
              <button
                v-for="suggestion in naturalLanguageSuggestions.slice(0, 3)"
                :key="suggestion"
                @click="searchQuery = suggestion; startSearch()"
                class="px-2.5 py-1 text-xs sm:text-sm text-primary-700 bg-primary-50 hover:bg-primary-100 rounded-md transition-colors border border-primary-200"
              >
                {{ suggestion }}
              </button>
            </div>
          </div>
        </div>

        <!-- Advanced Options (Collapsible) - Simplified Styling -->
        <div v-if="showAdvancedOptions" class="mb-6">
          <!-- Simplified card style for advanced options -->
          <div class="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 shadow-sm">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">数据源</label>
                <el-select v-model="selectedSources" multiple placeholder="选择数据源" class="w-full">
                  <el-option label="arXiv" value="arxiv" />
                  <el-option label="Semantic Scholar" value="semantic_scholar" />
                  <!-- Add more sources if available -->
                </el-select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">论文数量: {{ maxPapers }}</label>
                <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">选项</label>
                <div class="space-y-2 mt-2">
                  <el-checkbox v-model="retrieveFullText">获取全文</el-checkbox>
                  <el-checkbox v-model="enableAIAnalysis">AI 分析</el-checkbox>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Toggle Advanced Options Button - Simplified -->
        <div class="mb-10 text-center">
          <button
            @click="showAdvancedOptions = !showAdvancedOptions"
            class="text-sm text-primary-600 hover:text-primary-700 transition-colors flex items-center justify-center mx-auto px-3 py-1.5 rounded-md hover:bg-primary-50"
          >
            {{ showAdvancedOptions ? '隐藏高级选项' : '显示高级选项' }}
            <el-icon class="ml-1 transition-transform duration-200" :class="{ 'rotate-180': showAdvancedOptions }">
              <ArrowDown />
            </el-icon>
          </button>
        </div>
      </div>

      <!-- Results Display Area - Apply Gemini Styling -->
      <div v-if="isSearching || searchResults.length > 0 || (actionPlan && actionPlan.length > 0)" class="animate-fade-in">
        <!-- Loading State (if isSearching is true and no results yet) -->
        <div v-if="isSearching && searchResults.length === 0 && (!actionPlan || actionPlan.length === 0)" class="text-center py-10">
          <el-icon class="text-4xl text-primary-DEFAULT animate-spin mb-4"><Loading /></el-icon>
          <p class="text-gray-600">正在努力搜索中，请稍候...</p>
        </div>

        <!-- Action Plan Display - Gemini Style -->
        <div v-if="actionPlan && actionPlan.length > 0" class="bg-blue-50 border border-blue-200 rounded-lg p-4 sm:p-5 mb-6 shadow-sm">
          <div class="flex items-center mb-2.5">
            <div class="w-5 h-5 bg-primary-DEFAULT text-white rounded-full flex items-center justify-center mr-2.5 flex-shrink-0">
              <el-icon :size="14"><InfoFilled /></el-icon> <!-- Or a more relevant icon -->
            </div>
            <h3 class="text-sm font-semibold text-primary-700">AI 生成的行动计划</h3>
          </div>
          <div class="space-y-1.5">
            <div
              v-for="(step, index) in actionPlan"
              :key="index"
              class="flex items-start text-sm text-gray-700"
            >
              <span class="flex-shrink-0 w-4 h-4 bg-blue-100 text-primary-700 rounded-full flex items-center justify-center text-xs font-medium mr-2.5 mt-0.5">
                {{ index + 1 }}
              </span>
              <span class="flex-1">{{ step }}</span>
            </div>
          </div>
        </div>

        <!-- Search Results Header - Gemini Style -->
        <div v-if="searchResults.length > 0" class="flex flex-col sm:flex-row items-center justify-between mb-5 pb-3 border-b border-gray-200">
          <div>
            <h2 class="text-xl font-semibold text-gray-800">搜索结果</h2>
            <p class="text-sm text-gray-600">共找到 {{ searchResults.length }} 篇相关文献</p>
          </div>
          <button
            v-if="searchResults.length > 0"
            @click="generateReport"
            :disabled="isGeneratingReport"
            class="el-button el-button--primary mt-3 sm:mt-0 w-full sm:w-auto"
          >
            <el-icon v-if="isGeneratingReport" class="animate-spin mr-1"><Loading /></el-icon>
            {{ isGeneratingReport ? '报告生成中...' : '生成文献报告' }}
          </button>
        </div>

        <!-- Results List (Assuming PaperCard is used here) -->
        <div v-if="searchResults.length > 0" class="space-y-4">
          <PaperCard
            v-for="paper in searchResults"
            :key="paper.id"
            :paper="paper"
            @toggle-favorite="toggleFavorite"
            @view-details="viewDetailsModal"
            @download-pdf="downloadPdf"
           />
        </div>

        <!-- No Results Message (if search is complete and no results) -->
        <div v-if="!isSearching && searchResults.length === 0 && searchQuery" class="text-center py-10 px-4">
          <el-icon class="text-5xl text-gray-400 mb-4"><Document /></el-icon>
          <h3 class="text-xl font-semibold text-gray-700 mb-2">未找到相关文献</h3>
          <p class="text-gray-500 max-w-md mx-auto">
            尝试调整您的搜索词或扩展搜索范围。如果您认为这是一个错误，请检查您的网络连接或稍后再试。
          </p>
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  Clock,
  DocumentRemove,
  Loading,
  Delete,
  Menu,
  ArrowDown,
  Search,
  InfoFilled,
  Document
} from '@element-plus/icons-vue'
import PaperCard from '../components/PaperCard.vue'

// 定义Paper接口
interface Paper {
  id: string;
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
const retrieveFullText = ref(false)
const enableAIAnalysis = ref(true)
const isSearching = ref(false)
const isGeneratingReport = ref(false)
const hasSearched = ref(false)
const searchResults = ref<Paper[]>([])
const searchProgress = ref('')
const actionPlan = ref<string[]>([])

// UI 状态
const showSettings = ref(false)
const showHelp = ref(false)
const showHistory = ref(false)
const showMobileMenu = ref(false)
const showAdvancedOptions = ref(false)

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
])

// 方法
const startSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  isSearching.value = true
  hasSearched.value = true
  searchResults.value = []
  actionPlan.value = []
  searchProgress.value = '正在连接服务器...'

  try {
    // Simulating API call with dummy data for now
    console.log(`Simulating search for: ${searchQuery.value}, Sources: ${selectedSources.value.join(', ')}, Max Papers: ${maxPapers.value}`);
    await new Promise(resolve => setTimeout(resolve, 1500));

    actionPlan.value = [
        '解析用户查询意图',
        '构建关键词组合: [\"AI\", \"医疗诊断\", \"最新进展\"]',
        '并行查询 arXiv, Semantic Scholar 数据库',
        '初步筛选到 87 篇相关文献',
        '根据摘要和关键词进行相关性排序',
        '提取关键信息并生成摘要洞察'
    ];

    searchResults.value = [
        { id: '1', title: 'AI在肿瘤早期诊断中的应用进展回顾', authors: ['张三', '李四'], publishedDate: '2023-10-15', source: 'arXiv', summary: '本文综述了人工智能技术，特别是深度学习，在多种癌症早期诊断中的最新应用和挑战...', keywords: ['AI', '癌症诊断', '深度学习'], url: '#', pdfUrl: '#', isFavorite: false },
        { id: '2', title: '基于Transformer的医疗影像智能分析平台', authors: ['王五'], publishedDate: '2024-01-20', source: 'Semantic Scholar', summary: '提出了一种基于Transformer架构的医疗影像分析平台，能够有效提升多种疾病的诊断准确率...', keywords: ['Transformer', '医疗影像', '智能诊断'], url: '#', pdfUrl: '#', isFavorite: true },
        { id: '3', title: '可解释AI在临床决策支持系统中的研究', authors: ['赵六', '孙七'], publishedDate: '2023-05-01', source: 'PubMed Central', summary: '探讨了可解释人工智能（XAI）在构建临床决策支持系统（CDSS）中的重要性及其实现方法...', keywords: ['XAI', '临床决策', '可解释性'], url: '#', pdfUrl: '#', isFavorite: false }
    ];

    const historyItem: SearchHistoryItem = {
      query: searchQuery.value,
      date: new Date().toLocaleDateString('zh-CN'),
      resultCount: searchResults.value.length,
      params: {
          sources: selectedSources.value,
          maxPapers: maxPapers.value,
          retrieveFullText: retrieveFullText.value,
          enableAIAnalysis: enableAIAnalysis.value
        }
    };
    searchHistory.value.unshift(historyItem);
    if (searchHistory.value.length > 10) {
      searchHistory.value = searchHistory.value.slice(0, 10);
    }
    ElMessage.success(`检索完成！找到 ${searchResults.value.length} 篇相关文献`);

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
    ElMessage.warning('没有可用的论文数据生成报告')
    return
  }
  isGeneratingReport.value = true
  // Simulate report generation
  await new Promise(resolve => setTimeout(resolve, 2000));
  const reportContent = searchResults.value.map(p => `Title: ${p.title}\nAuthors: ${p.authors.join(', ')}\n---`).join('\n\n');
  ElMessageBox.alert(`<pre>${reportContent}</pre>`, '文献综述报告（模拟）', {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭',
      customClass: 'report-dialog' // Ensure this class is defined in styles if used
  });
  isGeneratingReport.value = false;
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  actionPlan.value = []
  hasSearched.value = false
}

// PaperCard event handlers
const toggleFavorite = (paperId: string) => {
  const paper = searchResults.value.find(p => p.id === paperId);
  if (paper) {
    paper.isFavorite = !paper.isFavorite;
    ElMessage.success(paper.isFavorite ? '已收藏' : '取消收藏');
  }
};

const viewDetailsModal = (paper: Paper) => {
  ElMessageBox.alert(JSON.stringify(paper, null, 2), `论文详情: ${paper.title}`, {
      confirmButtonText: '关闭',
      customClass: 'report-dialog' // Using existing class for wider dialog
  });
};

const downloadPdf = (paper: Paper) => {
  if (paper.pdfUrl && paper.pdfUrl !== '#'){
    window.open(paper.pdfUrl, '_blank');
  } else {
    ElMessage.info('该论文暂无可用PDF链接。');
  }
};

const saveSettings = () => {
  // This function implies selectedSources and maxPapers might be set from defaultSources,
  // but they are directly v-modeled in the advanced search.
  // Assuming this is for a separate settings dialog not fully shown or used yet.
  // For now, just closes the dialog if showSettings is for a modal.
  showSettings.value = false
  ElMessage.success('设置已保存 (模拟)')
}

const loadHistoryItem = (item: SearchHistoryItem) => {
  searchQuery.value = item.query
  selectedSources.value = item.params.sources
  maxPapers.value = item.params.maxPapers
  retrieveFullText.value = item.params.retrieveFullText
  enableAIAnalysis.value = item.params.enableAIAnalysis
  showHistory.value = false
  startSearch(); // Optionally trigger search immediately
  ElMessage.success('已加载并执行历史搜索')
}

const removeHistoryItem = (index: number) => {
  searchHistory.value.splice(index, 1)
  ElMessage.success('已删除历史记录')
}

const goToWelcome = () => {
  router.push('/')
}

// Lifecycle
onMounted(() => {
  const savedSettings = localStorage.getItem('literatureReviewSettings');
  if (savedSettings) {
    const settings = JSON.parse(savedSettings);
    defaultSources.value = settings.defaultSources || ['arxiv', 'semantic_scholar'];
    defaultMaxPapers.value = settings.defaultMaxPapers || 20;
    language.value = settings.language || 'zh';
  }
  const savedHistory = localStorage.getItem('searchHistory');
  if (savedHistory) {
    searchHistory.value = JSON.parse(savedHistory);
  }
});

watch([defaultSources, defaultMaxPapers, language], (newValues) => {
  localStorage.setItem('literatureReviewSettings', JSON.stringify({
    defaultSources: newValues[0],
    defaultMaxPapers: newValues[1],
    language: newValues[2]
  }));
}, { deep: true });

watch(searchHistory, (newHistory) => {
  localStorage.setItem('searchHistory', JSON.stringify(newHistory));
}, { deep: true });
</script>

<style scoped>
/* Styles from previous step for nav-button-gemini and mobile-nav-link-gemini are assumed here */
.nav-button-gemini {
  @apply px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-primary-DEFAULT hover:bg-primary-50 transition-colors flex items-center;
}

.mobile-nav-link-gemini {
  @apply block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-primary-DEFAULT hover:bg-primary-50;
}

:deep(.el-textarea__inner) {
  border-radius: 0.5rem;
  border: 1px solid theme('colors.gray.300');
}

:deep(.el-textarea__inner:focus) {
  border-color: theme('colors.primary.DEFAULT');
  box-shadow: 0 0 0 3px theme('colors.primary.light / 50%');
}

/* Custom class for wider dialogs if needed, e.g., for report or details */
:deep(.report-dialog .el-dialog__body) {
  max-height: 70vh;
  overflow-y: auto;
}
:deep(.report-dialog pre) {
  white-space: pre-wrap; /* Ensures long lines wrap in the <pre> tag */
  word-break: break-all;  /* Breaks long words or URLs */
}

/* Add any additional scoped styles if necessary */
</style>
