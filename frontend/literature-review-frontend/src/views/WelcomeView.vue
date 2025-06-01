<template>
  <div class="welcome-container">
    <!-- 简洁的背景 -->
    <div class="absolute inset-0 bg-gradient-to-br from-gray-50 via-white to-blue-50"></div>

    <!-- 主要内容 -->
    <div class="relative z-10 min-h-screen flex flex-col">
      <!-- 顶部导航 -->
      <nav class="flex items-center justify-between p-6 max-w-7xl mx-auto w-full">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <span class="text-white text-lg font-bold">T</span>
          </div>
          <span class="text-xl font-semibold text-gray-900">Tsearch</span>
        </div>
        <button @click="startJourney" class="text-gray-600 hover:text-gray-900 text-sm font-medium">
          进入应用 →
        </button>
      </nav>

      <!-- 主要内容区域 -->
      <div class="flex-1 flex items-center justify-center px-6">
        <div class="max-w-4xl mx-auto text-center">
          <!-- 主标题 -->
          <div class="mb-12">
            <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              智能文献发现引擎
            </h1>
            <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
              基于AI的学术研究助手，让文献综述变得简单高效。支持自然语言查询，智能分析，一键生成报告。
            </p>

            <!-- 主要CTA按钮 -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <button @click="startJourney"
                      class="px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                开始使用 Tsearch
              </button>
              <button @click="scrollToFeatures"
                      class="px-8 py-4 text-gray-700 border border-gray-300 rounded-xl font-semibold hover:border-gray-400 transition-all duration-200">
                了解更多
              </button>
            </div>
          </div>

          <!-- 简洁的特性展示 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16" ref="featuresSection">
            <div v-for="(feature, index) in features"
                 :key="index"
                 class="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300">
              <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4 mx-auto">
                <component :is="feature.icon" class="w-6 h-6 text-blue-600" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
              <p class="text-gray-600 text-sm leading-relaxed">{{ feature.description }}</p>
            </div>
          </div>

          <!-- 简洁的统计数据 -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8 py-12 border-t border-gray-200">
            <div v-for="(stat, index) in stats"
                 :key="index"
                 class="text-center">
              <div class="text-3xl font-bold text-gray-900 mb-1">{{ stat.value }}</div>
              <div class="text-sm text-gray-600">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部 -->
      <footer class="py-6 text-center text-sm text-gray-500 border-t border-gray-200">
        <div class="max-w-7xl mx-auto px-6">
          <p>© 2025 Tsearch. Created by Terence Qin. Powered by AI.</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  DataAnalysis,
  Document
} from '@element-plus/icons-vue'

const router = useRouter()
const featuresSection = ref<HTMLElement>()

// 特性数据
const features = ref([
  {
    icon: Search,
    title: '智能检索',
    description: '支持自然语言查询，多数据源整合，精准匹配相关文献'
  },
  {
    icon: DataAnalysis,
    title: 'AI分析',
    description: '深度学习算法分析文献内容，自动提取关键信息'
  },
  {
    icon: Document,
    title: '智能总结',
    description: '一键生成专业的文献综述报告，提升研究效率'
  }
])

// 统计数据
const stats = ref([
  { value: '10K+', label: '文献数据库' },
  { value: '99%', label: '检索准确率' },
  { value: '<5s', label: '响应时间' },
  { value: '24/7', label: '在线服务' }
])

// 方法
const startJourney = () => {
  router.push('/search')
}

const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'center'
  })
}
</script>

<style scoped>
.welcome-container {
  @apply relative min-h-screen;
}

/* 简洁的动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-container {
    @apply text-sm;
  }
}
</style>
