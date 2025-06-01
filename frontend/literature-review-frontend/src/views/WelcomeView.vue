<template>
  <div class="welcome-container">
    <!-- 极简背景 -->
    <div class="absolute inset-0 bg-white"></div>

    <!-- 主要内容 -->
    <div class="relative z-10 min-h-screen flex flex-col">
      <!-- 顶部导航 -->
      <nav class="flex items-center justify-between p-8 max-w-6xl mx-auto w-full">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center relative overflow-hidden">
            <!-- 科技感背景纹理 -->
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-2 h-2 bg-blue-300/30 rounded-full"></div>
            <div class="absolute bottom-1 left-1 w-1 h-1 bg-blue-200/40 rounded-full"></div>
            <!-- T字母 -->
            <span class="text-white text-sm font-bold relative z-10">T</span>
          </div>
          <span class="text-lg font-semibold text-gray-900">Tsearch</span>
        </div>
        <button @click="startJourney" class="text-gray-600 hover:text-gray-900 text-sm transition-colors">
          进入应用 →
        </button>
      </nav>

      <!-- 主要内容区域 -->
      <div class="flex-1 flex items-center justify-center px-8">
        <div class="max-w-3xl mx-auto text-center">
          <!-- 主标题 -->
          <div class="mb-16">
            <h1 class="text-4xl md:text-5xl font-semibold text-gray-900 mb-6 leading-tight tracking-tight">
              智能文献发现引擎
            </h1>
            <p class="text-lg text-gray-600 mb-10 max-w-xl mx-auto leading-relaxed">
              基于AI的学术研究助手，让文献综述变得简单高效
            </p>

            <!-- 主要CTA按钮 -->
            <div class="flex flex-col sm:flex-row gap-3 justify-center items-center mb-16">
              <button @click="startJourney"
                      class="px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition-colors">
                开始使用 Tsearch
              </button>
              <button @click="scrollToFeatures"
                      class="px-6 py-3 text-gray-600 border border-gray-300 rounded-lg font-medium hover:border-gray-400 hover:text-gray-900 transition-colors">
                了解更多
              </button>
            </div>
          </div>

          <!-- 简洁的特性展示 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mb-20" ref="featuresSection">
            <div v-for="(feature, index) in features"
                 :key="index"
                 class="text-center">
              <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <component :is="feature.icon" class="w-5 h-5 text-gray-700" />
              </div>
              <h3 class="text-base font-medium text-gray-900 mb-2">{{ feature.title }}</h3>
              <p class="text-gray-600 text-sm leading-relaxed">{{ feature.description }}</p>
            </div>
          </div>

          <!-- 简洁的统计数据 -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8 py-12 border-t border-gray-100">
            <div v-for="(stat, index) in stats"
                 :key="index"
                 class="text-center">
              <div class="text-2xl font-semibold text-gray-900 mb-1">{{ stat.value }}</div>
              <div class="text-xs text-gray-500 uppercase tracking-wide">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部 -->
      <footer class="py-8 text-center text-xs text-gray-400 border-t border-gray-100">
        <div class="max-w-6xl mx-auto px-8">
          <p>© 2025 Tsearch. Created by Terence Qin.</p>
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
  position: relative;
  min-height: 100vh;
}

/* 简洁的动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-container {
    font-size: 0.875rem;
  }
}
</style>
