<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-50 via-primary-50/30 to-secondary-50/20">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-primary-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-secondary-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float" style="animation-delay: 2s;"></div>
    </div>

    <div class="relative z-10 flex flex-col min-h-screen">
      <nav class="flex items-center justify-between p-6 lg:p-8 max-w-7xl mx-auto w-full">
        <div class="flex items-center space-x-4">
          <div class="relative group">
            <div class="w-12 h-12 bg-gradient-to-br from-primary to-primary-600 rounded-2xl flex items-center justify-center shadow-lg">
              <span class="text-white text-xl font-bold tracking-tight">T</span>
            </div>
          </div>
          <div>
            <h1 class="text-xl font-bold text-neutral-900 tracking-tight">Tsearch</h1>
            <p class="text-sm text-neutral-500 font-medium">AI Literature Discovery</p>
          </div>
        </div>

        <button @click="startJourney" class="px-6 py-3 bg-gradient-to-r from-primary to-primary-600 text-white font-medium rounded-xl shadow-lg">
          <span class="flex items-center">
            进入应用
            <el-icon class="ml-2">
              <ArrowRightBold />
            </el-icon>
          </span>
        </button>
      </nav>

      <div ref="heroSection" class="flex-1 flex items-center justify-center px-6 lg:px-8 text-center">
        <div class="max-w-4xl mx-auto">
          <div class="mb-16 lg:mb-20">
            <div class="inline-flex items-center px-4 py-2 bg-white/80 backdrop-blur-sm border border-primary-200/50 rounded-full text-primary-700 text-sm font-semibold mb-8">
              <el-icon class="mr-2 text-primary-500" :size="18">
                <Star />
              </el-icon>
              AI驱动的学术研究平台
            </div>

            <h1 class="text-5xl lg:text-7xl font-bold text-neutral-900 mb-8 leading-tight">
              智能文献
              <span class="gradient-text-primary block lg:inline">发现引擎</span>
            </h1>

            <p class="text-xl lg:text-2xl text-neutral-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              基于AI的学术研究助手，让文献综述变得简单高效。
              <br class="hidden lg:block">
              支持自然语言查询，智能分析，一键生成专业报告。
            </p>

            <div class="flex flex-col lg:flex-row gap-4 justify-center items-center">
              <button @click="startJourney" class="px-8 py-4 bg-gradient-to-r from-primary to-primary-600 text-white font-semibold rounded-2xl shadow-lg">
                <span class="flex items-center justify-center">
                  开始使用 Tsearch
                  <el-icon class="ml-3">
                    <Promotion />
                  </el-icon>
                </span>
              </button>

              <button @click="scrollToFeatures" class="px-8 py-4 bg-white/80 backdrop-blur-sm text-neutral-700 font-semibold rounded-2xl border border-neutral-200">
                <span class="flex items-center justify-center">
                  了解更多
                  <el-icon class="ml-3">
                    <InfoFilled />
                  </el-icon>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <section class="py-20 lg:py-24 bg-white/50 backdrop-blur-sm" ref="featuresSection">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl lg:text-5xl font-bold text-neutral-900 mb-6">核心功能</h2>
            <p class="text-xl text-neutral-600 max-w-2xl mx-auto">强大的AI技术栈，为学术研究提供全方位支持</p>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div v-for="(feature, index) in features" :key="index" class="feature-card group relative">
              <div class="relative p-8 lg:p-10 bg-white rounded-3xl shadow-soft">
                <div class="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mb-6">
                  <component :is="feature.icon" class="w-8 h-8 text-primary-600" />
                </div>
                <h3 class="text-xl font-bold text-neutral-900 mb-4">{{ feature.title }}</h3>
                <p class="text-neutral-600 leading-relaxed">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section ref="statsSection" class="py-16 lg:py-20 bg-gradient-to-r from-neutral-900 via-neutral-800 to-neutral-900 text-white">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-8">
            <div v-for="(stat, index) in stats" :key="index" class="text-center">
              <div class="text-4xl lg:text-5xl font-bold mb-2">{{ stat.value }}</div>
              <div class="text-neutral-400 font-medium">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <footer class="py-12 lg:py-16 bg-white border-t border-neutral-200">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
          <div class="text-center">
            <div class="flex items-center justify-center space-x-3 mb-6">
              <div class="w-10 h-10 bg-gradient-to-br from-primary to-primary-600 rounded-xl flex items-center justify-center">
                <span class="text-white text-lg font-bold">T</span>
              </div>
              <span class="text-2xl font-bold text-neutral-900">Tsearch</span>
            </div>
            <p class="text-neutral-600 font-medium">© {{ new Date().getFullYear() }} Tsearch. Created by Terence Qin.</p>
            <p class="text-sm text-neutral-500">Powered by AI • Built for Researchers • Made with ❤️</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  DataAnalysis,
  Document,
  ArrowRightBold,
  Promotion,
  InfoFilled,
  Star
} from '@element-plus/icons-vue'

const router = useRouter()
const featuresSection = ref<HTMLElement | null>(null)
const heroSection = ref<HTMLElement | null>(null)
const statsSection = ref<HTMLElement | null>(null)

const features = [
  {
    icon: markRaw(Search),
    title: '智能检索',
    description: '支持自然语言查询，多数据源整合，精准匹配相关文献。基于先进的语义理解技术，让搜索更加智能和精准。'
  },
  {
    icon: markRaw(DataAnalysis),
    title: 'AI分析',
    description: '深度学习算法分析文献内容，自动提取关键信息和趋势。智能识别研究热点，发现潜在的研究机会。'
  },
  {
    icon: markRaw(Document),
    title: '智能总结',
    description: '一键生成专业的文献综述报告，大幅提升研究效率。自动整理文献脉络，生成结构化的研究报告。'
  }
]

const stats = [
  { value: '10M+', label: '文献数据库' },
  { value: '99.2%', label: '检索准确率' },
  { value: '<2s', label: '平均响应时间' },
  { value: '24/7', label: '全天候服务' }
]

const startJourney = () => {
  console.log('🚀 Starting journey to search page...')
  router.push('/search')
}

const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start'
  })
}
</script>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.gradient-text-primary {
  background: linear-gradient(135deg, #0ea5e9, #0284c7, #a855f7);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
