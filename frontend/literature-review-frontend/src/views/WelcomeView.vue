<template>
  <div class="welcome-container">
    <!-- 背景动画层 -->
    <div class="absolute inset-0 overflow-hidden">
      <!-- 动态粒子背景 -->
      <div class="particles-bg">
        <div v-for="i in 50" :key="i" 
             class="particle" 
             :style="getParticleStyle(i)"></div>
      </div>
      
      <!-- 渐变网格 -->
      <div class="grid-overlay"></div>
    </div>

    <!-- 主要内容 -->
    <div class="relative z-10 min-h-screen flex items-center justify-center px-4">
      <div class="max-w-6xl mx-auto text-center">
        
        <!-- Logo和标题区域 -->
        <div class="mb-12 animate-fade-in-up">
          <!-- 3D Logo -->
          <div class="relative mb-8">
            <div class="logo-3d mx-auto">
              <div class="logo-face logo-front">
                <span class="text-6xl font-bold gradient-text">T</span>
              </div>
              <div class="logo-face logo-back">
                <span class="text-6xl font-bold text-white">T</span>
              </div>
            </div>
          </div>
          
          <h1 class="text-7xl font-bold mb-6">
            <span class="gradient-text-animated">Tsearch</span>
          </h1>
          
          <p class="text-2xl text-gray-600 mb-4 font-light">
            Terence's AI Literature Discovery Engine
          </p>
          
          <p class="text-lg text-gray-500 max-w-3xl mx-auto leading-relaxed">
            🚀 专为学术研究打造的智能文献发现平台，融合AI技术与现代设计，让文献检索变得简单而高效
          </p>
        </div>

        <!-- 特性展示卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div v-for="(feature, index) in features" 
               :key="index"
               class="feature-card"
               :style="{ animationDelay: `${index * 0.2}s` }">
            <div class="feature-icon">
              <component :is="feature.icon" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">{{ feature.title }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>

        <!-- 行动按钮 -->
        <div class="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
          <button @click="startJourney" 
                  class="cta-button cta-primary">
            <span class="relative z-10 flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              开始探索
            </span>
          </button>
          
          <button @click="showDemo" 
                  class="cta-button cta-secondary">
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              观看演示
            </span>
          </button>
        </div>

        <!-- 统计数据 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
          <div v-for="(stat, index) in stats" 
               :key="index"
               class="stat-item">
            <div class="text-4xl font-bold gradient-text mb-2">{{ stat.value }}</div>
            <div class="text-gray-600">{{ stat.label }}</div>
          </div>
        </div>

        <!-- 滚动提示 -->
        <div class="scroll-indicator">
          <div class="scroll-arrow"></div>
          <p class="text-sm text-gray-500 mt-2">向下滚动了解更多</p>
        </div>
      </div>
    </div>

    <!-- 演示模态框 -->
    <el-dialog v-model="showDemoModal" 
               title="产品演示" 
               width="80%" 
               :before-close="closeDemoModal">
      <div class="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
        <div class="text-center">
          <el-icon class="text-6xl text-gray-400 mb-4"><VideoPlay /></el-icon>
          <p class="text-gray-600">演示视频即将推出...</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  DataAnalysis,
  Document,
  VideoPlay
} from '@element-plus/icons-vue'

const router = useRouter()
const showDemoModal = ref(false)

// 特性数据
const features = ref([
  {
    icon: Search,
    title: '智能检索',
    description: '基于AI的语义搜索，理解您的研究意图，提供精准的文献匹配'
  },
  {
    icon: DataAnalysis,
    title: 'AI分析',
    description: '深度学习算法分析文献内容，自动提取关键信息和研究趋势'
  },
  {
    icon: Document,
    title: '智能总结',
    description: '自动生成专业的文献综述报告，节省您的宝贵时间'
  }
])

// 统计数据
const stats = ref([
  { value: '10K+', label: '文献数据库' },
  { value: '99%', label: '检索准确率' },
  { value: '5min', label: '平均响应时间' },
  { value: '24/7', label: '全天候服务' }
])

// 粒子样式生成
const getParticleStyle = (index: number) => {
  const size = Math.random() * 4 + 2
  const left = Math.random() * 100
  const animationDuration = Math.random() * 20 + 10
  const animationDelay = Math.random() * 5
  
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDuration: `${animationDuration}s`,
    animationDelay: `${animationDelay}s`
  }
}

// 方法
const startJourney = () => {
  router.push('/search')
}

const showDemo = () => {
  showDemoModal.value = true
}

const closeDemoModal = () => {
  showDemoModal.value = false
}

// 生命周期
onMounted(() => {
  // 添加页面加载动画
  document.body.style.overflow = 'hidden'
  setTimeout(() => {
    document.body.style.overflow = 'auto'
  }, 1000)
})
</script>

<style scoped>
.welcome-container {
  @apply relative min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100;
}

/* 粒子背景 */
.particles-bg {
  @apply absolute inset-0;
}

.particle {
  @apply absolute bg-blue-400/20 rounded-full;
  animation: float-particle linear infinite;
}

@keyframes float-particle {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

/* 网格覆盖层 */
.grid-overlay {
  @apply absolute inset-0 opacity-5;
  background-image: 
    linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* 3D Logo */
.logo-3d {
  @apply relative w-24 h-24;
  perspective: 1000px;
  animation: logo-rotate 6s ease-in-out infinite;
}

.logo-face {
  @apply absolute inset-0 flex items-center justify-center rounded-2xl;
  backface-visibility: hidden;
}

.logo-front {
  @apply bg-gradient-to-r from-blue-600 to-purple-700;
  transform: rotateY(0deg) translateZ(12px);
}

.logo-back {
  @apply bg-gradient-to-r from-purple-700 to-pink-600;
  transform: rotateY(180deg) translateZ(12px);
}

@keyframes logo-rotate {
  0%, 100% { transform: rotateY(0deg); }
  50% { transform: rotateY(180deg); }
}

/* 渐变文字动画 */
.gradient-text-animated {
  @apply bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% 100%;
  animation: gradient-shift 3s ease-in-out infinite;
}

@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* 特性卡片 */
.feature-card {
  @apply bg-white/80 backdrop-blur-md rounded-3xl p-8 shadow-lg border border-white/20;
  @apply hover:shadow-2xl hover:scale-105 transition-all duration-500;
  animation: slide-up 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(50px);
}

.feature-icon {
  @apply w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl;
  @apply flex items-center justify-center text-white mx-auto mb-6;
  @apply shadow-lg hover:shadow-xl transition-shadow duration-300;
}

/* CTA按钮 */
.cta-button {
  @apply px-8 py-4 rounded-2xl font-semibold text-lg transition-all duration-300;
  @apply transform hover:scale-105 hover:shadow-xl;
}

.cta-primary {
  @apply bg-gradient-to-r from-blue-600 to-purple-700 text-white;
  @apply hover:from-blue-700 hover:to-purple-800;
  @apply shadow-lg hover:shadow-2xl;
  position: relative;
  overflow: hidden;
}

.cta-primary::before {
  content: '';
  @apply absolute inset-0 bg-gradient-to-r from-white/20 to-transparent;
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.cta-primary:hover::before {
  transform: translateX(100%);
}

.cta-secondary {
  @apply bg-white/80 backdrop-blur-md text-gray-700 border-2 border-gray-200;
  @apply hover:bg-white hover:border-blue-300;
}

/* 统计项 */
.stat-item {
  @apply text-center;
  animation: fade-in-up 0.8s ease-out forwards;
  animation-delay: 1s;
  opacity: 0;
  transform: translateY(30px);
}

/* 滚动指示器 */
.scroll-indicator {
  @apply text-center;
  animation: bounce 2s infinite;
}

.scroll-arrow {
  @apply w-6 h-6 border-r-2 border-b-2 border-gray-400 mx-auto;
  transform: rotate(45deg);
}

/* 动画定义 */
@keyframes slide-up {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in-up {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 1s ease-out forwards;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .logo-3d {
    @apply w-16 h-16;
  }
  
  .feature-card {
    @apply p-6;
  }
  
  .cta-button {
    @apply px-6 py-3 text-base;
  }
}
</style>
