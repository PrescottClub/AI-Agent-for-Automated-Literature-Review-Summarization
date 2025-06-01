<template>
  <div class="paper-card group">
    <!-- 论文编号和状态指示器 -->
    <div class="absolute top-4 right-4 flex items-center space-x-2">
      <div v-if="paper.fullTextRetrieved" class="w-3 h-3 bg-green-400 rounded-full animate-pulse" title="全文已获取"></div>
      <div class="bg-gradient-to-r from-blue-100 to-purple-100 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold shadow-sm">
        #{{ index }}
      </div>
    </div>

    <!-- 论文标题 -->
    <h4 class="text-xl font-bold text-gray-900 mb-3 pr-20 hover:text-blue-600 transition-colors duration-200 cursor-pointer line-clamp-2"
        @click="openLink(paper.url)">
      {{ paper.title }}
    </h4>

    <!-- 作者和日期信息 -->
    <div class="flex flex-wrap items-center gap-4 mb-4 text-sm">
      <div class="flex items-center text-gray-600 hover:text-blue-600 transition-colors duration-200">
        <el-icon class="mr-1"><User /></el-icon>
        <span>{{ formatAuthors(paper.authors) }}</span>
      </div>
      <div class="flex items-center text-gray-600">
        <el-icon class="mr-1"><Calendar /></el-icon>
        <span>{{ formatDate(paper.publishedDate) }}</span>
      </div>
      <div class="flex items-center">
        <el-icon class="mr-1 text-gray-500"><DataBoard /></el-icon>
        <span class="px-2 py-1 bg-gray-100 text-gray-700 rounded-md text-xs font-medium uppercase tracking-wide">
          {{ paper.source }}
        </span>
      </div>
      <div v-if="paper.citations" class="flex items-center text-orange-600">
        <el-icon class="mr-1"><TrendCharts /></el-icon>
        <span class="text-xs">{{ paper.citations }} 引用</span>
      </div>
    </div>

    <!-- 摘要 -->
    <div class="mb-4">
      <p class="text-gray-700 leading-relaxed">
        {{ truncateSummary(paper.summary) }}
      </p>
    </div>

    <!-- 关键词 -->
    <div v-if="paper.keywords && paper.keywords.length > 0" class="mb-4">
      <div class="flex flex-wrap gap-2">
        <el-tag
          v-for="keyword in paper.keywords.slice(0, 6)"
          :key="keyword"
          size="small"
          type="info"
          effect="light"
          class="keyword-tag"
        >
          {{ keyword }}
        </el-tag>
        <el-tag
          v-if="paper.keywords.length > 6"
          size="small"
          type="info"
          effect="plain"
        >
          +{{ paper.keywords.length - 6 }} 更多
        </el-tag>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex items-center justify-between pt-4 border-t border-gray-100 group-hover:border-gray-200 transition-colors duration-200">
      <div class="flex items-center space-x-3">
        <button
          v-if="paper.url"
          @click="openLink(paper.url)"
          class="action-button action-primary"
        >
          <el-icon class="mr-1"><Link /></el-icon>
          查看原文
        </button>
        <button
          v-if="paper.pdfUrl"
          @click="openLink(paper.pdfUrl)"
          class="action-button action-success"
        >
          <el-icon class="mr-1"><Download /></el-icon>
          下载PDF
        </button>
      </div>

      <div class="flex items-center space-x-2">
        <el-tooltip content="收藏论文">
          <button @click="selectPaper(paper)" class="action-icon-button hover:text-yellow-500">
            <el-icon><Star /></el-icon>
          </button>
        </el-tooltip>
        <el-tooltip content="分享论文">
          <button class="action-icon-button hover:text-blue-500">
            <el-icon><Share /></el-icon>
          </button>
        </el-tooltip>
        <el-tooltip content="更多操作">
          <button class="action-icon-button hover:text-gray-700">
            <el-icon><MoreFilled /></el-icon>
          </button>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  User,
  Calendar,
  DataBoard,
  Link,
  Download,
  CircleCheck,
  Star,
  Share,
  TrendCharts,
  MoreFilled
} from '@element-plus/icons-vue'

export interface Paper {
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
}

interface Props {
  paper: Paper
  index: number
}

interface Emits {
  (e: 'select', paper: Paper): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 格式化作者列表
const formatAuthors = (authors: string[]) => {
  if (!authors || authors.length === 0) return '未知作者'
  if (authors.length <= 3) return authors.join(', ')
  return `${authors.slice(0, 3).join(', ')} 等`
}

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '未知日期'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN')
  } catch {
    return dateString
  }
}

// 截断摘要
const truncateSummary = (summary: string) => {
  if (!summary) return '暂无摘要'
  return summary.length > 300 ? summary.substring(0, 300) + '...' : summary
}

// 打开链接
const openLink = (url: string) => {
  window.open(url, '_blank')
}

// 选择论文
const selectPaper = (paper: Paper) => {
  emit('select', paper)
}
</script>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PaperCard'
})
</script>

<style scoped>
.paper-card {
  @apply relative bg-white rounded-2xl p-6 shadow-sm border border-gray-100;
  @apply hover:shadow-xl hover:border-blue-200 hover:-translate-y-1;
  @apply transition-all duration-300 ease-out;
  @apply backdrop-blur-sm bg-white/95;
}

.keyword-tag {
  @apply bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 border border-blue-200;
  @apply hover:from-blue-100 hover:to-indigo-100 hover:border-blue-300;
  @apply transition-all duration-200;
}

.action-button {
  @apply px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200;
  @apply flex items-center space-x-1;
}

.action-primary {
  @apply bg-gradient-to-r from-blue-500 to-blue-600 text-white;
  @apply hover:from-blue-600 hover:to-blue-700 hover:shadow-lg;
  @apply transform hover:scale-105;
}

.action-success {
  @apply bg-gradient-to-r from-green-500 to-green-600 text-white;
  @apply hover:from-green-600 hover:to-green-700 hover:shadow-lg;
  @apply transform hover:scale-105;
}

.action-icon-button {
  @apply w-8 h-8 flex items-center justify-center rounded-lg;
  @apply text-gray-400 hover:bg-gray-100 transition-all duration-200;
  @apply transform hover:scale-110;
}

/* 文本截断 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 悬停效果 */
.paper-card:hover .keyword-tag {
  @apply transform scale-105;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .paper-card {
    @apply p-4;
  }

  .action-button {
    @apply px-3 py-1 text-xs;
  }
}
</style>