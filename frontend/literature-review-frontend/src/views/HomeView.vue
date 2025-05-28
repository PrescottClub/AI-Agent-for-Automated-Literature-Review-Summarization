<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- 导航栏 -->
    <nav class="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <el-icon class="text-white text-xl"><Document /></el-icon>
            </div>
            <div>
              <h1 class="text-xl font-bold gradient-text">AI Literature Review</h1>
              <p class="text-xs text-gray-500">智能文献综述系统</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <el-button type="primary" :icon="Setting" circle />
            <el-button type="info" :icon="User" circle />
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 头部介绍区域 -->
      <div class="text-center mb-12 animate-fade-in">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          🔬 AI 驱动的文献综述助手
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          基于先进的人工智能技术，为您提供高效、准确的学术文献检索、分析与总结服务
        </p>
        
        <!-- 特性卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up">
            <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-blue-600 text-2xl"><Search /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">智能检索</h3>
            <p class="text-gray-600">多数据源检索，语义理解，精准匹配</p>
          </div>
          
          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up" style="animation-delay: 0.1s">
            <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-green-600 text-2xl"><DataAnalysis /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">AI 分析</h3>
            <p class="text-gray-600">深度分析文献内容，提取关键信息</p>
          </div>
          
          <div class="bg-white rounded-2xl p-6 card-shadow animate-slide-up" style="animation-delay: 0.2s">
            <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
              <el-icon class="text-purple-600 text-2xl"><Document /></el-icon>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">智能总结</h3>
            <p class="text-gray-600">生成专业的文献综述报告</p>
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
              />
            </div>

            <!-- 配置选项 -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">数据源</label>
                <el-select v-model="selectedSources" multiple placeholder="选择数据源" class="w-full">
                  <el-option label="arXiv" value="arxiv" />
                  <el-option label="Semantic Scholar" value="semantic_scholar" />
                  <el-option label="PubMed" value="pubmed" />
                </el-select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">论文数量</label>
                <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" show-input />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">年份范围</label>
                <el-date-picker
                  v-model="yearRange"
                  type="yearrange"
                  placeholder="选择年份范围"
                  class="w-full"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">其他选项</label>
                <div class="space-y-2">
                  <el-checkbox v-model="retrieveFullText">获取全文</el-checkbox>
                  <el-checkbox v-model="enableAIAnalysis">AI 深度分析</el-checkbox>
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
                class="px-12 py-3 text-lg font-semibold rounded-xl"
              >
                <el-icon class="mr-2"><Search /></el-icon>
                {{ isSearching ? '正在检索...' : '开始检索' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 结果展示区域 -->
      <div v-if="searchResults.length > 0" class="animate-fade-in">
        <!-- 统计信息 -->
        <div class="bg-white rounded-2xl p-6 card-shadow mb-6">
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

        <!-- 论文列表 -->
        <div class="space-y-4">
          <h3 class="text-xl font-bold text-gray-900 mb-4">检索结果</h3>
          <div
            v-for="(paper, index) in searchResults"
            :key="index"
            class="bg-white rounded-2xl p-6 card-shadow animate-slide-up"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <PaperCard :paper="paper" :index="index + 1" />
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!isSearching && hasSearched" class="text-center py-12">
        <el-icon class="text-6xl text-gray-400 mb-4"><DocumentRemove /></el-icon>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">未找到相关文献</h3>
        <p class="text-gray-500">请尝试调整搜索关键词或扩大搜索范围</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Search,
  Document,
  Setting,
  User,
  DataAnalysis,
  DocumentRemove
} from '@element-plus/icons-vue'
import PaperCard from '@/components/PaperCard.vue'

// 响应式数据
const searchQuery = ref('')
const selectedSources = ref(['arxiv', 'semantic_scholar'])
const maxPapers = ref(20)
const yearRange = ref([])
const retrieveFullText = ref(false)
const enableAIAnalysis = ref(true)
const isSearching = ref(false)
const hasSearched = ref(false)
const searchResults = ref([])

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

// 方法
const startSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  isSearching.value = true
  hasSearched.value = true

  try {
    // 调用真实API
    const searchParams = {
      query: searchQuery.value,
      sources: selectedSources.value,
      maxPapers: maxPapers.value,
      yearStart: yearRange.value[0] ? new Date(yearRange.value[0]).getFullYear() : undefined,
      yearEnd: yearRange.value[1] ? new Date(yearRange.value[1]).getFullYear() : undefined,
      retrieveFullText: retrieveFullText.value,
      enableAIAnalysis: enableAIAnalysis.value
    }

    const response = await fetch('http://localhost:8000/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(searchParams)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()
    searchResults.value = result.papers || []

    ElMessage.success(`成功检索到 ${searchResults.value.length} 篇相关文献`)
  } catch (error) {
    console.error('Search error:', error)
    ElMessage.error('检索失败，请确保后端服务器正在运行')
    
    // 如果API调用失败，使用模拟数据
    searchResults.value = [
      {
        title: `人工智能在${searchQuery.value}领域的应用研究`,
        authors: ['张三', '李四', '王五'],
        publishedDate: '2024-01-15',
        source: 'arxiv',
        summary: `本文深入研究了人工智能技术在${searchQuery.value}领域的最新应用，包括机器学习、深度学习和自然语言处理等前沿技术的实际应用案例。`,
        keywords: ['人工智能', '机器学习', '深度学习', searchQuery.value],
        url: 'https://arxiv.org/abs/2401.12345',
        fullTextRetrieved: true
      },
      {
        title: `${searchQuery.value}中的机器学习方法综述`,
        authors: ['赵六', '钱七'],
        publishedDate: '2023-12-20',
        source: 'semantic_scholar',
        summary: `本综述分析了${searchQuery.value}领域中机器学习方法的发展现状、主要挑战和未来趋势，为相关研究提供了重要参考。`,
        keywords: ['机器学习', '数据分析', '算法优化'],
        url: 'https://example.com/paper2',
        fullTextRetrieved: false
      }
    ]
    ElMessage.info('已切换到演示模式')
  } finally {
    isSearching.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out;
}

.animate-bounce-in {
  animation: bounceIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
