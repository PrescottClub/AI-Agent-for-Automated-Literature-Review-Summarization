<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning, CircleCheck } from '@element-plus/icons-vue'

// 检查后端连接状态
const backendStatus = ref<'checking' | 'connected' | 'disconnected'>('checking')

const checkBackendStatus = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/status')
    if (response.ok) {
      backendStatus.value = 'connected'
    } else {
      backendStatus.value = 'disconnected'
    }
  } catch (error) {
    backendStatus.value = 'disconnected'
  }
}

onMounted(() => {
  checkBackendStatus()
})
</script>

<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
    <!-- 后端状态指示器 -->
    <div v-if="backendStatus === 'disconnected'" 
         class="fixed top-0 left-0 right-0 bg-red-500 text-white text-center py-2 z-50">
      <el-icon class="mr-2"><Warning /></el-icon>
      后端服务未连接，请确保后端服务器正在运行 (http://localhost:8000)
    </div>
    
    <div v-else-if="backendStatus === 'connected'" 
         class="fixed top-0 left-0 right-0 bg-green-500 text-white text-center py-1 z-50 text-sm">
      <el-icon class="mr-1"><CircleCheck /></el-icon>
      后端服务已连接
    </div>

    <!-- 主要内容 -->
    <div :class="{ 'pt-10': backendStatus !== 'checking' }">
      <RouterView />
    </div>
  </div>
</template>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #1f2937;
}

/* 渐变文字效果 */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片阴影效果 */
.card-shadow {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.3s ease;
}

.card-shadow:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 动画效果 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounceIn {
  0% { opacity: 0; transform: scale(0.9); }
  50% { transform: scale(1.02); }
  100% { opacity: 1; transform: scale(1); }
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out;
}

.animate-bounce-in {
  animation: bounceIn 0.8s ease-out;
}

/* Element Plus 自定义样式 */
.el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.el-input__wrapper {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

.el-input__wrapper:hover {
  border-color: #667eea;
}

.el-input__wrapper.is-focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .card-shadow {
    margin: 0 1rem;
  }
}
</style>
