<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
// import { ElMessage } from 'element-plus' // Removed unused import
// 移除未使用的图标导入

import { getSystemStatus } from './api/literature'

// 检查后端连接状态
const backendStatus = ref<'checking' | 'connected' | 'disconnected'>('checking')
const retryCount = ref(0)
const maxRetries = 3

const checkBackendStatus = async () => {
  try {
    backendStatus.value = 'checking'
    await getSystemStatus()
    backendStatus.value = 'connected'
    retryCount.value = 0 // 重置重试计数
  } catch (error) {
    console.error('Backend status check failed:', error)
    backendStatus.value = 'disconnected'

    // 自动重试机制
    if (retryCount.value < maxRetries) {
      retryCount.value++
      setTimeout(() => {
        checkBackendStatus()
      }, 5000) // 5秒后重试
    }
  }
}

onMounted(() => {
  checkBackendStatus()
})
</script>

<template>
  <div id="app" class="min-h-screen bg-gray-50 text-gray-800">
    <!-- Removed complex background elements -->

    <!-- Top-level status indicator - can be restyled later if needed -->
    <div v-if="backendStatus === 'disconnected'"
         class="fixed top-4 right-4 bg-white border border-red-300 text-red-700 px-3 py-2 rounded-lg z-50 text-xs font-medium shadow-sm">
      <div class="flex items-center space-x-2">
        <div class="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse"></div>
        <span>服务未连接</span>
      </div>
    </div>

    <div v-else-if="backendStatus === 'connected'"
         class="fixed top-4 right-4 bg-white border border-green-300 text-green-700 px-3 py-2 rounded-lg z-50 text-xs font-medium shadow-sm">
      <div class="flex items-center space-x-2">
        <div class="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
        <span>已连接</span>
      </div>
    </div>

    <!-- Main content area -->
    <div class="relative z-10">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
/* App.vue 专用样式 - 仅保留应用级别的样式 */

#app {
  /* 保持最小的应用容器样式 */
}

/* 状态指示器样式 */
.status-indicator {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 50;
}
</style>
