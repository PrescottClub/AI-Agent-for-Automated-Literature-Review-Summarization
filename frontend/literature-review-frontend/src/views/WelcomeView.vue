<template>
  <div class="welcome-container">
    <!-- 主要内容 -->
    <div class="relative z-10 min-h-screen flex flex-col">
      <!-- 现代化顶部导航 -->
      <nav class="flex items-center justify-between p-8 max-w-7xl mx-auto w-full">
        <div class="flex items-center space-x-4">
          <!-- 重新设计的Logo -->
          <div class="relative group">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 rounded-2xl flex items-center justify-center relative overflow-hidden shadow-lg shadow-blue-500/25 transition-all duration-300 group-hover:shadow-xl group-hover:shadow-blue-500/40 group-hover:scale-105">
              <!-- 动态光效 -->
              <div class="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent"></div>
              <div class="absolute top-1 right-1 w-1.5 h-1.5 bg-white/40 rounded-full"></div>
              <div class="absolute bottom-1 left-1 w-1 h-1 bg-white/30 rounded-full"></div>
              <!-- 现代化T字母 -->
              <span class="text-white text-lg font-bold relative z-10 tracking-tight">T</span>
            </div>
          </div>
          <div>
            <h1 class="text-xl font-bold gradient-text">Tsearch</h1>
            <p class="text-xs text-slate-500 font-medium">AI Literature Discovery</p>
          </div>
        </div>
        <button @click="startJourney" class="group flex items-center space-x-2 px-4 py-2 text-slate-600 hover:text-slate-900 text-sm font-medium transition-all duration-200 hover:bg-slate-50 rounded-lg">
          <span>进入应用</span>
          <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </button>
      </nav>

      <!-- 主要内容区域 -->
      <div class="flex-1 flex items-center justify-center px-8">
        <div class="max-w-5xl mx-auto text-center">
          <!-- 现代化主标题 -->
          <div class="mb-20">
            <!-- 标签 -->
            <div class="inline-flex items-center px-4 py-2 bg-blue-50 border border-blue-200 rounded-full text-blue-700 text-sm font-medium mb-8">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
              </svg>
              AI驱动的学术研究平台
            </div>

            <h1 class="text-5xl md:text-7xl font-bold gradient-text mb-8 leading-tight tracking-tight">
              智能文献
              <br>
              <span class="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                发现引擎
              </span>
            </h1>

            <p class="text-xl md:text-2xl text-slate-600 mb-12 max-w-3xl mx-auto leading-relaxed font-light">
              基于AI的学术研究助手，让文献综述变得简单高效。
              <br class="hidden md:block">
              支持自然语言查询，智能分析，一键生成报告。
            </p>

            <!-- 现代化CTA按钮 -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <button @click="startJourney"
                      class="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl font-semibold text-lg shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 hover:scale-105 overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <span class="relative flex items-center">
                  开始使用 Tsearch
                  <svg class="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                  </svg>
                </span>
              </button>
              <button @click="scrollToFeatures"
                      class="px-8 py-4 text-slate-700 border-2 border-slate-200 rounded-2xl font-semibold text-lg hover:border-slate-300 hover:bg-slate-50 transition-all duration-300 hover:scale-105">
                了解更多
              </button>
            </div>
          </div>

          <!-- 现代化特性展示 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-24" ref="featuresSection">
            <div v-for="(feature, index) in features"
                 :key="index"
                 class="group relative p-8 bg-white/60 backdrop-blur-sm border border-slate-200/50 rounded-3xl hover:bg-white/80 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-slate-200/50">
              <!-- 装饰性渐变 -->
              <div class="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-purple-50/50 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

              <div class="relative z-10">
                <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-lg shadow-blue-500/25 group-hover:shadow-xl group-hover:shadow-blue-500/40 transition-all duration-300">
                  <component :is="feature.icon" class="w-7 h-7 text-white" />
                </div>
                <h3 class="text-xl font-bold text-slate-900 mb-4">{{ feature.title }}</h3>
                <p class="text-slate-600 leading-relaxed">{{ feature.description }}</p>
              </div>
            </div>
          </div>

          <!-- 现代化统计数据 -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8 py-16 border-t border-slate-200/50">
            <div v-for="(stat, index) in stats"
                 :key="index"
                 class="text-center group">
              <div class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2 group-hover:scale-110 transition-transform duration-300">{{ stat.value }}</div>
              <div class="text-sm text-slate-500 font-medium uppercase tracking-wider">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 现代化底部 -->
      <footer class="py-12 text-center border-t border-slate-200/50">
        <div class="max-w-7xl mx-auto px-8">
          <div class="flex items-center justify-center space-x-2 mb-4">
            <div class="w-6 h-6 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
              <span class="text-white text-xs font-bold">T</span>
            </div>
            <span class="text-slate-600 font-medium">Tsearch</span>
          </div>
          <p class="text-sm text-slate-500">© 2025 Tsearch. Created by Terence Qin with ❤️</p>
          <p class="text-xs text-slate-400 mt-2">Powered by AI • Built for Researchers</p>
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
