<template>
  <div class="paper-card group">
    <!-- 论文编号 -->
    <div class="absolute top-4 right-4 text-xs text-gray-400 font-mono">
      {{ index }}
    </div>

    <!-- 论文标题 -->
    <h4 class="text-lg font-medium text-gray-900 mb-3 pr-8 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2"
        @click="openLink(paper.url)">
      {{ paper.title }}
    </h4>

    <!-- 作者和日期信息 -->
    <div class="flex flex-wrap items-center gap-3 mb-3 text-sm text-gray-600">
      <span>{{ formatAuthors(paper.authors) }}</span>
      <span>•</span>
      <span>{{ formatDate(paper.publishedDate) }}</span>
      <span>•</span>
      <span class="text-xs bg-gray-100 px-2 py-1 rounded text-gray-700">
        {{ paper.source }}
      </span>
      <span v-if="paper.citations" class="text-xs">
        {{ paper.citations }} 引用
      </span>
    </div>

    <!-- 摘要 -->
    <div class="mb-4">
      <p class="text-gray-700 leading-relaxed text-sm">
        {{ truncateSummary(paper.summary) }}
      </p>
    </div>

    <!-- 关键词 -->
    <div v-if="paper.keywords && paper.keywords.length > 0" class="mb-4">
      <div class="flex flex-wrap gap-1">
        <span
          v-for="keyword in paper.keywords.slice(0, 4)"
          :key="keyword"
          class="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
        >
          {{ keyword }}
        </span>
        <span
          v-if="paper.keywords.length > 4"
          class="px-2 py-1 bg-gray-100 text-gray-500 rounded text-xs"
        >
          +{{ paper.keywords.length - 4 }}
        </span>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex items-center justify-between pt-3 border-t border-gray-100">
      <div class="flex items-center space-x-2">
        <button
          v-if="paper.url"
          @click="openLink(paper.url)"
          class="text-xs text-blue-600 hover:text-blue-800 transition-colors"
        >
          查看原文
        </button>
        <button
          v-if="paper.pdfUrl"
          @click="openLink(paper.pdfUrl)"
          class="text-xs text-green-600 hover:text-green-800 transition-colors"
        >
          下载PDF
        </button>
      </div>

      <div class="flex items-center space-x-1">
        <button @click="selectPaper(paper)" class="text-gray-400 hover:text-gray-600 transition-colors">
          <el-icon><Star /></el-icon>
        </button>
        <button class="text-gray-400 hover:text-gray-600 transition-colors">
          <el-icon><Share /></el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Star,
  Share
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
  position: relative;
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  transition: box-shadow 0.2s ease;
}

.paper-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 文本截断 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .paper-card {
    padding: 16px;
  }
}
</style>