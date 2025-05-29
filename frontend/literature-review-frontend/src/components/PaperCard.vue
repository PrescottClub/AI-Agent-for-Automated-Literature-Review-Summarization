<template>
  <div class="paper-card">
    <!-- 论文编号 -->
    <div class="absolute top-4 right-4 bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm font-semibold">
      #{{ index }}
    </div>

    <!-- 论文标题 -->
    <h4 class="text-xl font-bold text-gray-900 mb-3 pr-16">
      {{ paper.title }}
    </h4>

    <!-- 作者和日期信息 -->
    <div class="flex flex-wrap items-center gap-4 mb-4 text-sm text-gray-600">
      <div class="flex items-center">
        <el-icon class="mr-1"><User /></el-icon>
        <span>{{ formatAuthors(paper.authors) }}</span>
      </div>
      <div class="flex items-center">
        <el-icon class="mr-1"><Calendar /></el-icon>
        <span>{{ formatDate(paper.publishedDate) }}</span>
      </div>
      <div class="flex items-center">
        <el-icon class="mr-1"><DataBoard /></el-icon>
        <span class="uppercase font-medium">{{ paper.source }}</span>
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
    <div class="flex items-center justify-between pt-4 border-t border-gray-100">
      <div class="flex items-center space-x-3">
        <el-button
          v-if="paper.url"
          type="primary"
          size="small"
          :icon="Link"
          @click="openLink(paper.url)"
        >
          查看原文
        </el-button>
        <el-button
          v-if="paper.pdfUrl"
          type="success"
          size="small"
          :icon="Download"
          @click="openLink(paper.pdfUrl)"
        >
          下载PDF
        </el-button>
      </div>
      
      <div class="flex items-center space-x-2">
        <el-tooltip content="全文已获取" v-if="paper.fullTextRetrieved">
          <el-icon class="text-green-500"><CircleCheck /></el-icon>
        </el-tooltip>
        <el-tooltip content="收藏">
          <el-button type="info" size="small" :icon="Star" circle @click="selectPaper(paper)" />
        </el-tooltip>
        <el-tooltip content="分享">
          <el-button type="info" size="small" :icon="Share" circle />
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

<style scoped>
.paper-card {
  @apply relative bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300;
}

.keyword-tag {
  @apply bg-blue-50 text-blue-700 border-blue-200;
}

.keyword-tag:hover {
  @apply bg-blue-100;
}
</style> 