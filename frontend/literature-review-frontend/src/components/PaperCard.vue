<template>
  <div class="paper-card" ref="cardRef">
    <!-- Card Content -->
    <div class="p-6">
      <!-- Header -->
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0 w-8 h-8 bg-blue-500/20 text-blue-400 rounded-lg flex items-center justify-center text-sm font-semibold">
            #{{ index }}
          </div>

          <div class="flex items-center space-x-2">
            <div v-if="paper.fullTextRetrieved" class="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs font-medium">
              Full Text
            </div>
            <div class="px-2 py-1 bg-gray-500/20 text-gray-400 rounded text-xs font-medium" :class="getSourceColor(paper.source)">
              {{ paper.source }}
            </div>
          </div>
        </div>

        <button @click.stop="toggleFavorite" class="p-2 hover:bg-white/10 rounded-lg transition-colors" :class="{ 'text-yellow-400': paper.isFavorite, 'text-gray-400': !paper.isFavorite }">
          <el-icon>
            <StarFilled v-if="paper.isFavorite" />
            <Star v-else />
          </el-icon>
        </button>
      </div>

      <!-- Title -->
      <div class="mb-4 cursor-pointer" @click="viewDetails">
        <h3 class="text-lg font-semibold text-white hover:text-blue-400 transition-colors line-clamp-2">
          {{ paper.title }}
        </h3>
      </div>

      <!-- Meta Information -->
      <div class="space-y-2 mb-4 text-sm">
        <div class="flex items-center text-gray-400">
          <el-icon class="mr-2"><User /></el-icon>
          <span class="truncate">{{ formatAuthors(paper.authors) }}</span>
        </div>

        <div class="flex items-center justify-between text-gray-400">
          <div class="flex items-center">
            <el-icon class="mr-2"><Calendar /></el-icon>
            <span>{{ formatDate(paper.publishedDate) }}</span>
          </div>

          <div v-if="paper.citations" class="flex items-center">
            <el-icon class="mr-1"><TrendCharts /></el-icon>
            <span>{{ paper.citations }}</span>
          </div>
        </div>
      </div>

      <!-- Abstract -->
      <div class="mb-4">
        <p class="text-gray-300 text-sm leading-relaxed line-clamp-3">
          {{ paper.summary }}
        </p>
      </div>

      <!-- Keywords -->
      <div v-if="paper.keywords && paper.keywords.length > 0" class="mb-6">
        <div class="flex flex-wrap gap-2">
          <span
            v-for="keyword in paper.keywords.slice(0, 4)"
            :key="keyword"
            class="px-2 py-1 bg-purple-500/20 text-purple-300 rounded text-xs"
          >
            {{ keyword }}
          </span>
          <span v-if="paper.keywords.length > 4" class="px-2 py-1 bg-gray-500/20 text-gray-400 rounded text-xs">
            +{{ paper.keywords.length - 4 }}
          </span>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <button v-if="paper.url" @click.stop="openLink(paper.url)" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors">
            <el-icon class="mr-1"><Link /></el-icon>
            View Paper
          </button>

          <button v-if="paper.pdfUrl" @click.stop="downloadPdf" class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-medium transition-colors">
            <el-icon class="mr-1"><Download /></el-icon>
            Download
          </button>
        </div>

        <div class="flex items-center space-x-2">
          <button @click.stop="viewDetails" class="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-all" title="View Details">
            <el-icon><View /></el-icon>
          </button>
          <button class="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-all" title="Share">
            <el-icon><Share /></el-icon>
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
import type { Paper } from '@/types/paper'

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

const formatAuthors = (authors: string[] | undefined) => {
  if (!authors || authors.length === 0) return 'Unknown authors'
  if (authors.length === 1) return authors[0]
  if (authors.length === 2) return authors.join(' and ')
  return `${authors[0]} et al.`
}

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return 'Unknown date'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return dateString
  }
}

const getSourceColor = (source: string) => {
  const colors: Record<string, string> = {
    arxiv: 'bg-orange-500/20 text-orange-400',
    'semantic_scholar': 'bg-blue-500/20 text-blue-400',
    pubmed: 'bg-green-500/20 text-green-400',
    default: 'bg-gray-500/20 text-gray-400'
  }
  return colors[source.toLowerCase()] || colors.default
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
.paper-card {
  @apply bg-white/5 backdrop-blur border border-white/10 rounded-xl hover:bg-white/10 hover:border-white/20 transition-all duration-300;
}

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
</style>
