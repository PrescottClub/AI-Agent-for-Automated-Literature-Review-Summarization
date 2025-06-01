<template>
  <div class="paper-card bg-white border border-gray-200 rounded-lg p-4 sm:p-5 shadow-sm hover:shadow-md transition-shadow duration-200">
    <!-- Paper Index and Status -->
    <div class="absolute top-4 right-4 flex items-center space-x-2">
      <div v-if="paper.fullTextRetrieved" class="w-2 h-2 bg-green-500 rounded-full" title="全文已获取"></div>
      <div v-if="paper.isFavorite" @click.stop="toggleFavorite" class="text-yellow-500 hover:text-yellow-400 cursor-pointer" title="取消收藏">
        <el-icon :size="18"><StarFilled /></el-icon>
      </div>
       <div v-else @click.stop="toggleFavorite" class="text-gray-400 hover:text-yellow-500 cursor-pointer" title="点击收藏">
        <el-icon :size="18"><Star /></el-icon>
      </div>
      <div class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full text-xs font-medium">
        #{{ index }}
      </div>
    </div>

    <!-- Paper Title -->
    <h4 class="text-lg font-semibold text-gray-800 mb-2 pr-16 hover:text-primary-DEFAULT transition-colors cursor-pointer line-clamp-2 leading-normal"
        @click="viewDetails">
      {{ paper.title }}
    </h4>

    <!-- Authors and Date -->
    <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mb-3 text-xs sm:text-sm text-gray-500">
      <div class="flex items-center">
        <el-icon class="mr-1" :size="14"><User /></el-icon>
        <span>{{ formatAuthors(paper.authors) }}</span>
      </div>
      <div class="flex items-center">
        <el-icon class="mr-1" :size="14"><Calendar /></el-icon>
        <span>{{ formatDate(paper.publishedDate) }}</span>
      </div>
      <div class="px-2 py-0.5 bg-gray-100 text-gray-700 rounded-full text-xs">
        {{ paper.source }}
      </div>
      <div v-if="paper.citations" class="flex items-center text-gray-600">
        <el-icon class="mr-0.5" :size="14"><TrendCharts /></el-icon> <!-- Citation icon -->
        <span class="text-xs font-medium">{{ paper.citations }} 引用</span>
      </div>
    </div>

    <!-- Abstract -->
    <div class="mb-4">
      <p class="text-sm text-gray-600 leading-relaxed line-clamp-3">
        {{ paper.summary }} <!-- Removed truncateSummary, rely on line-clamp -->
      </p>
    </div>

    <!-- Keywords -->
    <div v-if="paper.keywords && paper.keywords.length > 0" class="mb-4">
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="keyword in paper.keywords.slice(0, 4)"
          :key="keyword"
          class="px-2 py-0.5 bg-primary-50 text-primary-700 rounded-full text-xs font-medium border border-primary-100"
        >
          {{ keyword }}
        </span>
        <span
          v-if="paper.keywords.length > 4"
          class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full text-xs font-medium"
        >
          +{{ paper.keywords.length - 4 }}
        </span>
      </div>
    </div>

    <!-- Action Buttons - Gemini Style -->
    <div class="flex items-center justify-between pt-3 border-t border-gray-200">
      <div class="flex items-center space-x-2 sm:space-x-3">
        <button
          v-if="paper.url"
          @click.stop="openLink(paper.url)"
          class="action-button-gemini text-primary-600 hover:text-primary-700"
        >
          <el-icon :size="16" class="mr-0.5 sm:mr-1"><Link /></el-icon>查看原文
        </button>
        <button
          v-if="paper.pdfUrl"
          @click.stop="downloadPdf"
          class="action-button-gemini text-blue-600 hover:text-blue-700"
        >
          <el-icon :size="16" class="mr-0.5 sm:mr-1"><Download /></el-icon>下载PDF
        </button>
      </div>

      <div class="flex items-center space-x-1 sm:space-x-2">
        <button @click.stop="viewDetails" class="icon-button-gemini" title="查看详情">
          <el-icon :size="18"><View /></el-icon>
        </button>
        <!-- Add other actions like share, cite if needed -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { StarFilled, Star, User, Calendar, Link, Download, View, TrendCharts } from '@element-plus/icons-vue'; // Ensure all used icons are imported
import type { PropType } from 'vue'; // Import PropType for better prop typing

export interface Paper { // Ensure this interface matches the one in HomeView or a shared types file
  id: string; // Added id
  title: string;
  authors: string[];
  publishedDate: string;
  source: string;
  summary: string;
  keywords?: string[];
  url?: string;
  pdfUrl?: string;
  fullTextRetrieved?: boolean;
  citations?: number;
  isFavorite?: boolean; // Added for favorite toggle
}

const props = defineProps({
  paper: {
    type: Object as PropType<Paper>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
});

const emit = defineEmits([
  'toggle-favorite',
  'view-details',
  'download-pdf'
]);

const formatAuthors = (authors: string[] | undefined) => {
  if (!authors || authors.length === 0) return '未知作者';
  if (authors.length <= 2) return authors.join(', ');
  return `${authors.slice(0, 1).join(', ')} 等`; // Show first author and '等' for brevity
};

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '未知日期';
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch {
    return dateString;
  }
};

const openLink = (url: string | undefined) => {
  if (url && url !== '#') {
    window.open(url, '_blank', 'noopener,noreferrer');
  } else {
    // Optionally inform user if no link is available, or disable button
    console.warn('No valid URL provided for openLink');
  }
};

const toggleFavorite = () => {
  emit('toggle-favorite', props.paper.id);
};

const viewDetails = () => {
  emit('view-details', props.paper);
};

const downloadPdf = () => {
  emit('download-pdf', props.paper);
  // Actual download logic might be in parent or a service if it's complex (e.g. needs auth)
  // For direct links, this is fine. If pdfUrl is a trigger for parent to fetch and download, that's also fine.
};

</script>

<style scoped>
.paper-card {
  /* Using Tailwind classes directly in the template for most styling */
}

.action-button-gemini {
  @apply flex items-center px-1.5 sm:px-2 py-1 rounded-md text-xs sm:text-sm font-medium transition-colors hover:bg-gray-100;
}

.icon-button-gemini {
  @apply p-1.5 rounded-full text-gray-500 hover:text-primary-DEFAULT hover:bg-primary-50 transition-colors;
}

/* Line clamp utility (if not globally available via Tailwind plugin) */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
