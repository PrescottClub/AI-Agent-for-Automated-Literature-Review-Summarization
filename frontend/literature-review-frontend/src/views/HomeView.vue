<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 backdrop-blur-md bg-white/5 border-b border-white/10">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center space-x-3 cursor-pointer group" @click="goToWelcome">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span class="text-white text-lg font-bold">T</span>
            </div>
            <div>
              <h1 class="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Tsearch
              </h1>
              <p class="text-xs text-gray-400 -mt-1">AI Literature Discovery</p>
            </div>
          </div>

          <!-- Navigation items -->
          <div class="hidden md:flex items-center space-x-6">
            <button @click="showHistory = true" class="flex items-center text-gray-300 hover:text-white transition-colors">
              <el-icon class="mr-2"><Clock /></el-icon>
              历史
            </button>
            <button @click="showSettings = true" class="flex items-center text-gray-300 hover:text-white transition-colors">
              <el-icon class="mr-2"><Setting /></el-icon>
              设置
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="relative z-10 pt-12 pb-20">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Hero Section -->
        <div class="text-center mb-16">
          <!-- Badge -->
          <div class="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2 mb-8">
            <div class="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
            <span class="text-blue-300 text-sm">Powered by Advanced AI</span>
          </div>

          <!-- Main Title -->
          <h1 class="text-4xl md:text-6xl font-bold text-white mb-6">
            <span class="block">Discover Academic</span>
            <span class="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Insights
            </span>
            <span class="block text-3xl md:text-4xl text-gray-300 font-light mt-2">
              Beyond Imagination
            </span>
          </h1>

          <!-- Subtitle -->
          <p class="text-lg text-gray-300 max-w-3xl mx-auto leading-relaxed mb-12">
            Transform your research with AI-powered literature discovery.
            Find, analyze, and synthesize academic papers with unprecedented precision.
          </p>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl mx-auto mb-16">
            <div class="bg-white/5 backdrop-blur border border-white/10 rounded-xl p-6 text-center">
              <div class="text-2xl mb-2">📚</div>
              <div class="text-2xl font-bold text-white">10M+</div>
              <div class="text-sm text-gray-400">Papers Indexed</div>
            </div>
            <div class="bg-white/5 backdrop-blur border border-white/10 rounded-xl p-6 text-center">
              <div class="text-2xl mb-2">🎯</div>
              <div class="text-2xl font-bold text-white">99.2%</div>
              <div class="text-sm text-gray-400">Accuracy</div>
            </div>
            <div class="bg-white/5 backdrop-blur border border-white/10 rounded-xl p-6 text-center">
              <div class="text-2xl mb-2">⚡</div>
              <div class="text-2xl font-bold text-white">2.3s</div>
              <div class="text-sm text-gray-400">Avg Response</div>
            </div>
          </div>
        </div>

        <!-- Search Interface -->
        <div class="max-w-4xl mx-auto mb-16">
          <div class="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-8">
            <div class="text-center mb-8">
              <h3 class="text-2xl font-bold text-white mb-2">
                Describe Your Research
              </h3>
              <p class="text-gray-300">
                Use natural language to express your research needs
              </p>
            </div>

            <div class="mb-6">
              <div class="relative">
                <el-input
                  v-model="searchQuery"
                  type="textarea"
                  :autosize="{ minRows: 4, maxRows: 8 }"
                  placeholder="例如：探索深度学习在医疗影像诊断中的最新突破，特别关注肺部疾病检测的创新方法..."
                  class="search-input"
                  @keyup.enter.ctrl="startSearch"
                />
              </div>
            </div>

            <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div class="flex items-center space-x-4 text-sm text-gray-400">
                <div class="flex items-center space-x-2">
                  <kbd class="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">Ctrl</kbd>
                  <span>+</span>
                  <kbd class="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">Enter</kbd>
                  <span>to search</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span>AI Ready</span>
                </div>
              </div>

              <button
                @click="startSearch"
                :disabled="!searchQuery.trim() || isSearching"
                class="relative px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div class="flex items-center">
                  <el-icon v-if="isSearching" class="animate-spin mr-2">
                    <Loading />
                  </el-icon>
                  <el-icon v-else class="mr-2">
                    <Search />
                  </el-icon>
                  <span>{{ isSearching ? 'Searching...' : 'Search Literature' }}</span>
                </div>
              </button>
            </div>

            <!-- Quick Suggestions -->
            <div v-if="naturalLanguageSuggestions.length > 0" class="mt-8">
              <p class="text-sm text-gray-400 mb-4">Quick Start</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <button
                  v-for="suggestion in naturalLanguageSuggestions.slice(0, 3)"
                  :key="suggestion"
                  @click="searchQuery = suggestion; startSearch()"
                  class="p-3 bg-white/5 border border-white/10 rounded-lg text-left text-sm text-gray-300 hover:bg-white/10 hover:border-white/20 transition-all"
                >
                  {{ suggestion }}
                </button>
              </div>
            </div>
          </div>

          <!-- Advanced Options -->
          <div class="text-center mt-6">
            <button
              @click="showAdvancedOptions = !showAdvancedOptions"
              class="text-gray-400 hover:text-white transition-colors"
            >
              {{ showAdvancedOptions ? 'Hide' : 'Show' }} Advanced Options
              <el-icon class="ml-2 transition-transform" :class="{ 'rotate-180': showAdvancedOptions }">
                <ArrowDown />
              </el-icon>
            </button>
          </div>

          <div v-if="showAdvancedOptions" class="mt-6 bg-white/5 backdrop-blur border border-white/10 rounded-xl p-6">
            <h4 class="text-lg font-semibold text-white mb-6">Advanced Settings</h4>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm text-gray-300 mb-2">Data Sources</label>
                <el-select v-model="selectedSources" multiple placeholder="Select sources" class="w-full">
                  <el-option label="arXiv" value="arxiv" />
                  <el-option label="Semantic Scholar" value="semantic_scholar" />
                </el-select>
              </div>

              <div>
                <label class="block text-sm text-gray-300 mb-2">Papers: {{ maxPapers }}</label>
                <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" class="mt-2" />
              </div>

              <div class="md:col-span-2">
                <div class="flex flex-wrap gap-4">
                  <label class="flex items-center text-gray-300">
                    <el-checkbox v-model="retrieveFullText" />
                    <span class="ml-2">Full Text</span>
                  </label>
                  <label class="flex items-center text-gray-300">
                    <el-checkbox v-model="enableAIAnalysis" />
                    <span class="ml-2">AI Analysis</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Results Section -->
        <div v-if="isSearching || searchResults.length > 0 || (actionPlan && actionPlan.length > 0)" class="max-w-7xl mx-auto">
          <!-- Loading Animation -->
          <div v-if="isSearching && searchResults.length === 0" class="text-center py-16">
            <div class="relative inline-block">
              <div class="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin"></div>
              <div class="absolute inset-0 w-16 h-16 border-4 border-purple-500/20 border-b-purple-500 rounded-full animate-spin animate-reverse"></div>
            </div>
            <h3 class="text-xl font-semibold text-white mt-6">AI Processing Your Query</h3>
            <p class="text-gray-400 mt-2">Analyzing requirements and searching literature...</p>
          </div>

          <!-- Action Plan -->
          <div v-if="actionPlan && actionPlan.length > 0" class="mb-12">
            <div class="bg-white/5 backdrop-blur border border-white/10 rounded-xl p-6">
              <div class="flex items-center mb-6">
                <div class="text-2xl mr-3">🤖</div>
                <h3 class="text-xl font-semibold text-white">AI Execution Plan</h3>
              </div>
              <div class="space-y-3">
                <div
                  v-for="(step, index) in actionPlan"
                  :key="index"
                  class="flex items-start space-x-3"
                >
                  <div class="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                    {{ index + 1 }}
                  </div>
                  <p class="text-gray-300">{{ step }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Results Grid -->
          <div v-if="searchResults.length > 0" class="space-y-8">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <h2 class="text-2xl font-bold text-white">Research Results</h2>
                <p class="text-gray-400">{{ searchResults.length }} papers found</p>
              </div>
              <button
                @click="generateReport"
                :disabled="isGeneratingReport"
                class="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition-colors disabled:opacity-50"
              >
                <el-icon v-if="isGeneratingReport" class="animate-spin mr-2">
                  <Loading />
                </el-icon>
                <el-icon v-else class="mr-2">
                  <Document />
                </el-icon>
                {{ isGeneratingReport ? 'Generating...' : 'Generate Report' }}
              </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              <PaperCard
                v-for="(paper, index) in searchResults"
                :key="paper.id"
                :paper="paper"
                :index="index + 1"
                @toggle-favorite="toggleFavorite"
                @view-details="viewDetailsModal"
                @download-pdf="downloadPdf"
                class="animate-fade-in-up"
                :style="{ animationDelay: `${index * 0.1}s` }"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialogs -->
    <el-dialog v-model="showSettings" title="Settings" width="600px">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Default Sources</label>
          <el-select v-model="defaultSources" multiple class="w-full">
            <el-option label="arXiv" value="arxiv" />
            <el-option label="Semantic Scholar" value="semantic_scholar" />
          </el-select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Default Max Papers</label>
          <el-input-number v-model="defaultMaxPapers" :min="5" :max="50" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Language</label>
          <el-select v-model="language" class="w-full">
            <el-option label="中文" value="zh" />
            <el-option label="English" value="en" />
          </el-select>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showHistory" title="Search History" width="600px">
      <div v-if="searchHistory.length === 0" class="text-center text-gray-500 py-8">
        暂无搜索历史
      </div>
      <div v-else class="space-y-4">
        <div
          v-for="(item, index) in searchHistory"
          :key="index"
          class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
          @click="searchQuery = item.query"
        >
          <div class="font-medium">{{ item.query }}</div>
          <div class="text-sm text-gray-500 mt-1">
            {{ item.date }} - {{ item.resultCount }} results
          </div>
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
  Loading,
  ArrowDown,
  Search,
  Document
} from '@element-plus/icons-vue'
import PaperCard from '../components/PaperCard.vue'
import type { Paper, SearchHistoryItem } from '@/types/paper'

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
const showHistory = ref(false)
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

// 移除未使用的函数，这些功能将在后续的组件拆分中实现

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
/* === CORE ANIMATIONS === */
@keyframes floatOrb {
  0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg); }
  33% { transform: translate3d(30px, -30px, 0) rotate(120deg); }
  66% { transform: translate3d(-20px, 20px, 0) rotate(240deg); }
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes particleFloat {
  0% {
    transform: rotate(0deg) translateX(40px) rotate(0deg);
    opacity: 0;
  }
  50% { opacity: 1; }
  100% {
    transform: rotate(360deg) translateX(40px) rotate(-360deg);
    opacity: 0;
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translate3d(0, 30px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

/* === LAYOUT & BACKGROUND === */
.floating-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(147, 51, 234, 0.3));
  filter: blur(40px);
  animation: floatOrb 20s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: 20%;
  animation-delay: -7s;
}

.orb-3 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 60%;
  animation-delay: -14s;
}

/* === NAVIGATION === */
.glass-nav {
  backdrop-filter: blur(20px) saturate(180%);
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  position: relative;
  perspective: 1000px;
}

.logo-3d {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
  transition: all 0.3s ease;
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.1),
    0 4px 32px rgba(59, 130, 246, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logo-3d:hover {
  transform: rotateY(15deg) rotateX(5deg) translateZ(10px);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.2),
    0 8px 40px rgba(59, 130, 246, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
  background: transparent;
  border: none;
  cursor: pointer;
}

.nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

/* === HERO SECTION === */
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 50px;
  color: #60a5fa;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 32px;
  backdrop-filter: blur(10px);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 900;
  line-height: 0.9;
  margin-bottom: 24px;
  color: white;
}

.hero-highlight {
  display: block;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b);
  background-size: 300% 300%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientShift 4s ease infinite;
  position: relative;
}

.hero-highlight::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b);
  background-size: 300% 300%;
  animation: gradientShift 4s ease infinite;
  filter: blur(30px);
  opacity: 0.3;
  z-index: -1;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 800px;
  margin: 0 auto 48px;
  line-height: 1.6;
}

/* === STATS GRID === */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  max-width: 800px;
  margin: 0 auto 80px;
}

.stat-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  animation: slideInUp 0.6s ease forwards;
}

.stat-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(59, 130, 246, 0.3);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

/* === SEARCH INTERFACE === */
.search-container {
  max-width: 900px;
  margin: 0 auto;
}

.search-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  backdrop-filter: blur(30px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 32px 64px rgba(0, 0, 0, 0.4);
}

.search-header {
  text-align: center;
  margin-bottom: 32px;
}

.search-input-wrapper {
  margin-bottom: 24px;
}

.search-gradient-border {
  position: relative;
  padding: 2px;
  border-radius: 16px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
  background-size: 200% 200%;
  animation: gradientShift 4s ease infinite;
}

.search-textarea :deep(.el-textarea__inner) {
  background: rgba(15, 23, 42, 0.8);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 16px;
  line-height: 1.6;
  padding: 20px;
  resize: none;
  backdrop-filter: blur(10px);
}

.search-textarea :deep(.el-textarea__inner)::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.search-textarea :deep(.el-textarea__inner):focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.search-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.kbd {
  display: inline-block;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
  color: rgba(255, 255, 255, 0.7);
}

.ai-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.search-button {
  position: relative;
  padding: 12px 32px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(59, 130, 246, 0.4);
}

.search-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
}

.button-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.search-button:hover .button-glow {
  opacity: 1;
}

/* === SUGGESTIONS === */
.suggestions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.suggestions-title {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.suggestions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.suggestion-pill {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: slideInUp 0.6s ease forwards;
}

.suggestion-pill:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  color: white;
}

/* === ADVANCED PANEL === */
.advanced-panel {
  margin-top: 24px;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(20px);
  animation: slideInUp 0.4s ease forwards;
}

.advanced-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.close-button {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-button:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.advanced-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 600;
}

.advanced-select :deep(.el-select__wrapper) {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
}

.advanced-slider :deep(.el-slider__runway) {
  background: rgba(255, 255, 255, 0.2);
}

.advanced-slider :deep(.el-slider__bar) {
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
}

.toggle-advanced {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.toggle-advanced:hover {
  color: white;
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.1);
}

/* === RESULTS SECTION === */
.results-section {
  margin-top: 80px;
}

.loading-animation {
  text-align: center;
  padding: 80px 0;
}

.loading-orb {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 32px;
}

.loading-core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 2s ease-in-out infinite;
}

.loading-ring {
  position: absolute;
  inset: 0;
  border: 2px solid transparent;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.loading-particles {
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 4px;
  height: 4px;
  background: #60a5fa;
  border-radius: 50%;
  animation: particleFloat 3s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.25s);
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 12px;
}

.loading-text {
  color: rgba(255, 255, 255, 0.6);
}

/* === ACTION PLAN === */
.action-plan {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  backdrop-filter: blur(20px);
}

.plan-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.plan-icon {
  font-size: 1.5rem;
}

.plan-header h3 {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
}

.plan-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.plan-step {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  animation: slideInUp 0.5s ease forwards;
}

.step-number {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.step-text {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

/* === RESULTS CONTAINER === */
.results-container {
  margin-top: 32px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.results-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.results-count {
  color: rgba(255, 255, 255, 0.6);
}

.generate-report-btn {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  background: linear-gradient(135deg, #059669, #10b981);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.generate-report-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(5, 150, 105, 0.4);
}

.papers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
}

.paper-card-animated {
  animation: slideInUp 0.6s ease forwards;
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .search-card {
    padding: 24px;
  }

  .search-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .papers-grid {
    grid-template-columns: 1fr;
  }

  .advanced-grid {
    grid-template-columns: 1fr;
  }
}

/* === BACKGROUND PATTERN === */
.bg-pattern {
  background-image: radial-gradient(circle at 2px 2px, rgba(156, 146, 172, 0.1) 1px, transparent 0);
  background-size: 60px 60px;
}

/* === SPIN ANIMATION === */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* === CUSTOM DIALOG === */
:deep(.custom-dialog .el-dialog) {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}

:deep(.custom-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.custom-dialog .el-dialog__title) {
  color: white;
}

:deep(.custom-dialog .el-dialog__body) {
  color: rgba(255, 255, 255, 0.8);
}
</style>
