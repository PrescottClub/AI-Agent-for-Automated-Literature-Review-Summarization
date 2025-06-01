<template>
  <div class="paper-card group">
    <!-- 论文编号和状态 -->
    <div class="absolute top-6 right-6 flex items-center space-x-2">
      <div v-if="paper.fullTextRetrieved" class="w-2 h-2 bg-green-500 rounded-full animate-pulse" title="全文已获取"></div>
      <div class="px-3 py-1 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 rounded-full text-xs font-semibold border border-blue-200">
        #{{ index }}
      </div>
    </div>

    <!-- 论文标题 -->
    <h4 class="text-xl font-bold text-slate-900 mb-4 pr-16 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2 leading-tight"
        @click="openLink(paper.url)">
      {{ paper.title }}
    </h4>

    <!-- 作者和日期信息 -->
    <div class="flex flex-wrap items-center gap-4 mb-4 text-sm">
      <div class="flex items-center text-slate-600">
        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
        <span>{{ formatAuthors(paper.authors) }}</span>
      </div>
      <div class="flex items-center text-slate-600">
        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
        <span>{{ formatDate(paper.publishedDate) }}</span>
      </div>
      <div class="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-xs font-medium">
        {{ paper.source }}
      </div>
      <div v-if="paper.citations" class="flex items-center text-orange-600">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
        </svg>
        <span class="text-xs font-medium">{{ paper.citations }} 引用</span>
      </div>
    </div>

    <!-- 摘要 -->
    <div class="mb-6">
      <p class="text-slate-700 leading-relaxed">
        {{ truncateSummary(paper.summary) }}
      </p>
    </div>

    <!-- 关键词 -->
    <div v-if="paper.keywords && paper.keywords.length > 0" class="mb-6">
      <div class="flex flex-wrap gap-2">
        <span
          v-for="keyword in paper.keywords.slice(0, 5)"
          :key="keyword"
          class="px-3 py-1 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 rounded-full text-xs font-medium border border-blue-200 hover:bg-gradient-to-r hover:from-blue-100 hover:to-indigo-100 transition-colors"
        >
          {{ keyword }}
        </span>
        <span
          v-if="paper.keywords.length > 5"
          class="px-3 py-1 bg-slate-100 text-slate-500 rounded-full text-xs font-medium"
        >
          +{{ paper.keywords.length - 5 }}
        </span>
      </div>
    </div>

    <!-- 现代化操作按钮 -->
    <div class="flex items-center justify-between pt-6 border-t border-slate-100">
      <div class="flex items-center space-x-3">
        <button
          v-if="paper.url"
          @click="openLink(paper.url)"
          class="group flex items-center px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-xl text-sm font-medium transition-all duration-200 hover:scale-105"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
          </svg>
          查看原文
        </button>
        <button
          v-if="paper.pdfUrl"
          @click="openLink(paper.pdfUrl)"
          class="group flex items-center px-4 py-2 bg-green-50 hover:bg-green-100 text-green-700 rounded-xl text-sm font-medium transition-all duration-200 hover:scale-105"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          下载PDF
        </button>
      </div>

      <div class="flex items-center space-x-2">
        <button @click="selectPaper(paper)" class="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-yellow-500 hover:bg-yellow-50 rounded-lg transition-all duration-200">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
          </svg>
        </button>
        <button class="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-all duration-200">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 移除未使用的图标导入，改用SVG图标

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
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 24px;
  border: 1px solid rgba(226, 232, 240, 0.5);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.paper-card:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
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