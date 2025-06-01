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
  <div id="app" class="min-h-screen bg-white relative">
    <!-- 极简背景 - 仅保留微妙的纹理 -->
    <div class="fixed inset-0 pointer-events-none">
      <div class="absolute inset-0 bg-gradient-to-b from-gray-50/30 to-transparent"></div>
    </div>

    <!-- 后端状态指示器 - 极简设计 -->
    <div v-if="backendStatus === 'disconnected'"
         class="fixed top-6 right-6 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg z-50 text-sm">
      <div class="flex items-center space-x-2">
        <div class="w-2 h-2 bg-red-500 rounded-full"></div>
        <span>服务未连接</span>
      </div>
    </div>

    <div v-else-if="backendStatus === 'connected'"
         class="fixed top-6 right-6 bg-green-50 border border-green-200 text-green-700 px-4 py-2 rounded-lg z-50 text-sm">
      <div class="flex items-center space-x-2">
        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
        <span>已连接</span>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="relative z-10">
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
  line-height: 1.5;
  color: #111827;
  font-weight: 400;
}

/* 简化的文字效果 */
.gradient-text {
  color: #1f2937;
  font-weight: 600;
}

/* 简化的卡片阴影效果 */
.card-shadow {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease;
}

.card-shadow:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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

/* Element Plus 简化样式 */
.el-button--primary {
  background: #2563eb;
  border: 1px solid #2563eb;
  transition: all 0.2s ease;
}

.el-button--primary:hover {
  background: #1d4ed8;
  border-color: #1d4ed8;
}

.el-input__wrapper {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  transition: border-color 0.2s ease;
}

.el-input__wrapper:hover {
  border-color: #9ca3af;
}

.el-input__wrapper.is-focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 1px #2563eb;
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

/* 背景网格图案 */
.bg-grid-pattern {
  background-image:
    linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* 浮动动画 */
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(120deg); }
  66% { transform: translateY(10px) rotate(240deg); }
}

@keyframes float-delayed {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(15px) rotate(-120deg); }
  66% { transform: translateY(-10px) rotate(-240deg); }
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(180deg); }
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translate(-50%, -100%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

.animate-float {
  animation: float 8s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 10s ease-in-out infinite;
  animation-delay: 2s;
}

.animate-float-slow {
  animation: float-slow 12s ease-in-out infinite;
  animation-delay: 4s;
}

.animate-slide-down {
  animation: slide-down 0.5s ease-out;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .card-shadow {
    margin: 0 1rem;
  }
}
</style>
