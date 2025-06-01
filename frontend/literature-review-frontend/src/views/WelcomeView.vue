<template>
  <div class="min-h-screen bg-gray-50 text-gray-700">
    <!-- Main content container -->
    <div class="relative z-10 flex flex-col min-h-screen">
      <!-- Simplified Navigation -->
      <nav class="flex items-center justify-between p-6 sm:p-8 max-w-7xl mx-auto w-full">
        <div class="flex items-center space-x-3">
          <div class="w-9 h-9 sm:w-10 sm:h-10 bg-primary-DEFAULT rounded-lg flex items-center justify-center shadow-sm">
            <span class="text-white text-lg sm:text-xl font-semibold">T</span>
          </div>
          <div>
            <h1 class="text-lg sm:text-xl font-semibold text-gray-800">Tsearch</h1>
            <p class="text-xs text-gray-500">AI Literature Discovery</p>
          </div>
        </div>
        <button @click="startJourney" class="el-button el-button--primary el-button--small sm:el-button--medium">
          进入应用 <el-icon class="ml-1 el-icon--right"><ArrowRightBold /></el-icon>
        </button>
      </nav>

      <!-- Main Hero Section -->
      <div class="flex-1 flex items-center justify-center px-4 sm:px-6 text-center">
        <div class="max-w-3xl mx-auto">
          <div class="mb-12 sm:mb-16">
            <div class="inline-flex items-center px-3 py-1 bg-primary-50 border border-primary-200 rounded-full text-primary-700 text-sm font-medium mb-6">
              <el-icon class="mr-1.5" :size="16"><Star /></el-icon> <!-- Using a generic star or idea icon -->
              AI驱动的学术研究平台
            </div>

            <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-800 mb-6 leading-tight">
              智能文献 <span class="text-primary-DEFAULT">发现引擎</span>
            </h1>

            <p class="text-lg sm:text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
              基于AI的学术研究助手，让文献综述变得简单高效。
              支持自然语言查询，智能分析，一键生成报告。
            </p>

            <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center">
              <button @click="startJourney"
                      class="el-button el-button--primary el-button--large w-full sm:w-auto">
                开始使用 Tsearch <el-icon class="ml-1.5 el-icon--right"><Promotion /></el-icon>
              </button>
              <button @click="scrollToFeatures"
                      class="el-button el-button--large w-full sm:w-auto">
                了解更多 <el-icon class="ml-1.5 el-icon--right"><InfoFilled /></el-icon>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Features Section - Simplified Styling -->
      <div class="py-12 sm:py-16 bg-white" ref="featuresSection">
        <div class="max-w-5xl mx-auto px-4 sm:px-6">
            <h2 class="text-3xl font-bold text-gray-800 text-center mb-10 sm:mb-12">核心功能</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
                <div v-for="(feature, index) in features"
                    :key="index"
                    class="bg-gray-50 p-6 rounded-lg border border-gray-200 transition-all duration-300 hover:shadow-lg hover:border-primary-200">
                    <div class="w-12 h-12 bg-primary-100 text-primary-600 rounded-lg flex items-center justify-center mb-4">
                        <component :is="feature.icon" class="w-6 h-6" />
                    </div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">{{ feature.title }}</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">{{ feature.description }}</p>
                </div>
            </div>
        </div>
      </div>

      <!-- Stats Section - Simplified -->
      <div class="py-12 sm:py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4 sm:px-6">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 sm:gap-8">
                <div v-for="(stat, index) in stats"
                    :key="index"
                    class="text-center bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                    <div class="text-3xl font-bold text-primary-DEFAULT mb-1">{{ stat.value }}</div>
                    <div class="text-sm text-gray-500">{{ stat.label }}</div>
                </div>
            </div>
        </div>
      </div>

      <!-- Footer - Simplified -->
      <footer class="py-8 sm:py-10 text-center border-t border-gray-200 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
          <div class="flex items-center justify-center space-x-2 mb-3">
            <div class="w-7 h-7 bg-primary-DEFAULT rounded-md flex items-center justify-center">
              <span class="text-white text-sm font-semibold">T</span>
            </div>
            <span class="text-gray-700 font-medium">Tsearch</span>
          </div>
          <p class="text-sm text-gray-500">© {{ new Date().getFullYear() }} Tsearch. Created by Terence Qin.</p>
          <p class="text-xs text-gray-400 mt-1">Powered by AI • Built for Researchers</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  Search,      // For features
  DataAnalysis,// For features
  Document,    // For features
  ArrowRightBold, // For nav button
  Promotion,   // For CTA button
  InfoFilled,  // For CTA button
  Star         // For hero badge icon
} from '@element-plus/icons-vue';

const router = useRouter();
const featuresSection = ref<HTMLElement | null>(null); // Ensure HTMLElement or null for ref type

const features = ref([
  {
    icon: Search, // Using imported icon component directly
    title: '智能检索',
    description: '支持自然语言查询，多数据源整合，精准匹配相关文献。'
  },
  {
    icon: DataAnalysis,
    title: 'AI分析',
    description: '深度学习算法分析文献内容，自动提取关键信息和趋势。'
  },
  {
    icon: Document,
    title: '智能总结',
    description: '一键生成专业的文献综述报告，大幅提升研究效率。'
  }
]);

const stats = ref([
  { value: '1M+', label: '文献数据库' }, // Adjusted stat value for example
  { value: '98%', label: '检索准确率' },
  { value: '<3s', label: '平均响应' },
  { value: '24/7', label: '稳定服务' }
]);

const startJourney = () => {
  router.push('/search'); // Assuming '/search' is the route for HomeView
};

const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start' // Changed to start for better scroll position
  });
};
</script>

<style scoped>
/* Scoped styles for WelcomeView - keep minimal, rely on Tailwind and App.vue globals */

/* Optional: Add a subtle hover effect for feature cards if not covered by Tailwind */
.hover\:shadow-lg:hover {
  /* Tailwind's shadow-lg is usually sufficient */
}
</style>
