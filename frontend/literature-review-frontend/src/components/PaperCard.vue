<template>
  <div class="paper-card-modern group" ref="cardRef">
    <!-- 卡片背景效果 -->
    <div class="absolute inset-0 bg-gradient-to-br from-white to-neutral-50 rounded-2xl shadow-soft group-hover:shadow-large transition-all duration-500 group-hover:-translate-y-2"></div>
    <div class="absolute inset-0 bg-gradient-to-br from-primary-50/50 to-secondary-50/30 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

    <!-- 卡片内容 -->
    <div class="relative p-8">
      <!-- 卡片头部 -->
      <div class="flex items-start justify-between mb-6">
        <div class="flex items-center space-x-4">
          <!-- 序号标识 -->
          <div class="w-10 h-10 bg-gradient-to-br from-primary-100 to-primary-200 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            <span class="text-primary-700 font-bold text-sm">#{{ index }}</span>
          </div>

          <!-- 状态标签 -->
          <div class="flex items-center space-x-2">
            <div v-if="paper.fullTextRetrieved"
                 class="px-3 py-1 bg-success-100 text-success-700 rounded-full text-xs font-semibold border border-success-200">
              <span class="flex items-center">
                <div class="w-1.5 h-1.5 bg-success-500 rounded-full mr-2"></div>
                Full Text
              </span>
            </div>
            <div class="px-3 py-1 rounded-full text-xs font-semibold border"
                 :class="getSourceStyle(paper.source)">
              {{ formatSource(paper.source) }}
            </div>
          </div>
        </div>

        <!-- 收藏按钮 -->
        <button @click.stop="toggleFavorite"
                class="p-3 rounded-xl transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary/50"
                :class="paper.isFavorite ? 'text-warning-500 bg-warning-50 hover:bg-warning-100' : 'text-neutral-400 hover:text-warning-500 hover:bg-warning-50'">
          <el-icon class="text-lg">
            <StarFilled v-if="paper.isFavorite" />
            <Star v-else />
          </el-icon>
        </button>
      </div>

      <!-- 论文标题 -->
      <div class="mb-6 cursor-pointer" @click="viewDetails">
        <h3 class="text-xl font-bold text-neutral-900 hover:text-primary-700 transition-colors duration-300 line-clamp-2 leading-tight">
          {{ paper.title }}
        </h3>
      </div>

      <!-- 元信息 -->
      <div class="space-y-4 mb-6">
        <!-- 作者信息 -->
        <div class="flex items-center text-neutral-600">
          <el-icon class="mr-3 text-neutral-400">
            <User />
          </el-icon>
          <span class="truncate font-medium">{{ formatAuthors(paper.authors) }}</span>
        </div>

        <!-- 发布日期和引用数 -->
        <div class="flex items-center justify-between text-neutral-600">
          <div class="flex items-center">
            <el-icon class="mr-3 text-neutral-400">
              <Calendar />
            </el-icon>
            <span class="font-medium">{{ formatDate(paper.publishedDate) }}</span>
          </div>

          <div v-if="paper.citations" class="flex items-center px-3 py-1 bg-info-50 text-info-700 rounded-full border border-info-200">
            <el-icon class="mr-2 text-sm">
              <TrendCharts />
            </el-icon>
            <span class="text-sm font-semibold">{{ paper.citations }} 引用</span>
          </div>
        </div>
      </div>

      <!-- 摘要 -->
      <div class="mb-6">
        <p class="text-neutral-700 leading-relaxed line-clamp-3">
          {{ paper.summary }}
        </p>
      </div>

      <!-- 关键词 -->
      <div v-if="paper.keywords && paper.keywords.length > 0" class="mb-8">
        <div class="flex flex-wrap gap-2">
          <span v-for="keyword in paper.keywords.slice(0, 4)" :key="keyword"
                class="px-3 py-1 bg-secondary-100 text-secondary-700 rounded-full text-xs font-medium border border-secondary-200 hover:bg-secondary-200 transition-colors duration-300">
            {{ keyword }}
          </span>
          <span v-if="paper.keywords.length > 4"
                class="px-3 py-1 bg-neutral-100 text-neutral-600 rounded-full text-xs font-medium border border-neutral-200">
            +{{ paper.keywords.length - 4 }} 更多
          </span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex items-center justify-between pt-4 border-t border-neutral-200">
        <div class="flex items-center space-x-3">
          <button v-if="paper.url" @click.stop="openLink(paper.url)"
                  class="group px-5 py-2.5 bg-gradient-to-r from-primary to-primary-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary/50">
            <span class="flex items-center">
              <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                <Link />
              </el-icon>
              查看论文
            </span>
          </button>

          <button v-if="paper.pdfUrl" @click.stop="downloadPdf"
                  class="group px-5 py-2.5 bg-neutral-600 hover:bg-neutral-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-medium transition-all duration-300 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-neutral-500/50">
            <span class="flex items-center">
              <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                <Download />
              </el-icon>
              下载PDF
            </span>
          </button>
        </div>

        <div class="flex items-center space-x-2">
          <button @click.stop="viewDetails"
                  class="p-3 text-neutral-500 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  title="查看详情">
            <el-icon>
              <View />
            </el-icon>
          </button>
          <button class="p-3 text-neutral-500 hover:text-secondary-600 hover:bg-secondary-50 rounded-xl transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-secondary/50"
                  title="分享">
            <el-icon>
              <Share />
            </el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { StarFilled, Star, User, Calendar, Link, Download, View, TrendCharts, Share } from '@element-plus/icons-vue'
import type { PropType } from 'vue'
import type { Paper } from '../types/paper'

const props = defineProps({
  paper: {
    type: Object as PropType<Paper>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const emit = defineEmits([
  'toggle-favorite',
  'view-details',
  'download-pdf'
])

const cardRef = ref<HTMLElement>()

// 格式化作者信息
const formatAuthors = (authors: string[] | undefined) => {
  if (!authors || authors.length === 0) return '未知作者'
  if (authors.length === 1) return authors[0]
  if (authors.length === 2) return authors.join(' 和 ')
  return `${authors[0]} 等`
}

// 格式化日期
const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '未知日期'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return dateString
  }
}

// 获取数据源样式
const getSourceStyle = (source: string) => {
  const styles: Record<string, string> = {
    arxiv: 'bg-orange-100 text-orange-700 border-orange-200',
    'semantic_scholar': 'bg-blue-100 text-blue-700 border-blue-200',
    pubmed: 'bg-green-100 text-green-700 border-green-200',
    default: 'bg-neutral-100 text-neutral-700 border-neutral-200'
  }
  return styles[source.toLowerCase()] || styles.default
}

// 格式化数据源名称
const formatSource = (source: string) => {
  const sourceNames: Record<string, string> = {
    arxiv: 'arXiv',
    'semantic_scholar': 'Semantic Scholar',
    pubmed: 'PubMed',
    default: source
  }
  return sourceNames[source.toLowerCase()] || sourceNames.default
}

const openLink = (url: string | undefined) => {
  if (url) {
    window.open(url, '_blank')
  }
}

const toggleFavorite = () => {
  emit('toggle-favorite', props.paper.id)
}

const viewDetails = () => {
  emit('view-details', props.paper)
}

const downloadPdf = () => {
  emit('download-pdf', props.paper)
}
</script>

<style scoped>
/* PaperCard 现代化样式 */
.paper-card-modern {
  position: relative;
  background: transparent;
  border-radius: 1.5rem;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.paper-card-modern:hover {
  transform: translateY(-8px);
}

/* 文本截断工具类 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 按钮悬停效果增强 */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

/* 渐变背景动画 */
@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* 发光效果 */
.shadow-glow {
  box-shadow: 0 0 20px rgba(14, 165, 233, 0.4);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .paper-card-modern {
    margin-bottom: 1rem;
  }

  .paper-card-modern:hover {
    transform: translateY(-4px);
  }
}

/* 减少动画偏好支持 */
@media (prefers-reduced-motion: reduce) {
  .paper-card-modern,
  .paper-card-modern:hover {
    transform: none;
    transition: none;
  }

  .group-hover\:scale-110:hover {
    transform: none;
  }
}
</style>
