<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
// import { ElMessage } from 'element-plus' // Removed unused import
// 移除未使用的图标导入

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
  } catch (e) { // Changed variable name to avoid conflict if `error` is a global or other variable
    console.error("Error checking backend status:", e) // Added console log for the error
    backendStatus.value = 'disconnected'
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

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  /* Use Gemini text color from Tailwind config: colors.gray.700 or colors.gemini.onSurface */
  color: theme('colors.gray.700');
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* Use Gemini background color from Tailwind config: colors.gray.50 or colors.gemini.background */
  background-color: theme('colors.gray.50');
}

/* Remove or simplify gradient text if not aligned with Gemini style */
/* .gradient-text { ... } */

/* Modern card shadow - keep if subtle, otherwise simplify */
.card-shadow {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* Simplified shadow */
  transition: box-shadow 0.2s ease-out, transform 0.2s ease-out;
}

.card-shadow:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.08); /* Slightly more prominent on hover */
  transform: translateY(-1px);
}

/* Animations - keep if they are subtle and enhance UX */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); } /* Adjusted transform */
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); } /* Adjusted transform */
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounceIn {
  0% { opacity: 0; transform: scale(0.95); } /* Adjusted scale */
  /* Simpler bounce */
  70% { transform: scale(1.01); }
  100% { opacity: 1; transform: scale(1); }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out; /* Adjusted duration */
}

.animate-slide-up {
  animation: slideUp 0.5s ease-out; /* Adjusted duration */
}

.animate-bounce-in {
  animation: bounceIn 0.6s ease-out; /* Adjusted duration */
}

/* Element Plus Modernization - Align with Gemini color palette */
.el-button--primary {
  /* Use Tailwind primary color for background */
  background-color: theme('colors.primary.DEFAULT');
  border: none;
  border-radius: 8px; /* Slightly reduced border-radius */
  font-weight: 500; /* Adjusted font-weight */
  transition: background-color 0.2s ease-out, transform 0.2s ease-out, box-shadow 0.2s ease-out;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* Subtle shadow */
}

.el-button--primary:hover {
  /* Use Tailwind primary dark color for background on hover */
  background-color: theme('colors.primary.dark');
  transform: translateY(-1px);
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.07); /* Subtle hover shadow */
}

.el-button--primary:focus,
.el-button--primary:active {
    /* Ensure focus and active states are also styled */
    background-color: theme('colors.primary.dark');
    box-shadow: 0 0 0 3px theme('colors.primary.light / 50%'); /* Focus ring with Tailwind color */
}


.el-input__wrapper {
  border-radius: 8px; /* Slightly reduced border-radius */
  /* Use Tailwind gray for border */
  border: 1px solid theme('colors.gray.300');
  transition: border-color 0.2s ease-out, box-shadow 0.2s ease-out, background-color 0.2s ease-out;
  background-color: theme('colors.white'); /* Ensure default is white or very light gray */
  /* Removed backdrop-filter as it might not be typical Gemini style */
}

.el-input__wrapper:hover {
  /* Use Tailwind gray for border on hover */
  border-color: theme('colors.gray.400');
  background-color: theme('colors.white');
}

.el-input__wrapper.is-focus {
  /* Use Tailwind primary color for border and shadow on focus */
  border-color: theme('colors.primary.DEFAULT');
  box-shadow: 0 0 0 3px theme('colors.primary.light / 50%');
  background-color: theme('colors.white');
}

/* Gemini AI-style scrollbar - Simplified and uses Gemini grays */
::-webkit-scrollbar {
  width: 6px; /* Thinner scrollbar */
  height: 6px;
}

::-webkit-scrollbar-track {
  /* Use a very light Gemini gray for the track */
  background: theme('colors.gray.100');
}

::-webkit-scrollbar-thumb {
  /* Use a medium Gemini gray for the thumb */
  background: theme('colors.gray.400');
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  /* Slightly darker Gemini gray on hover */
  background: theme('colors.gray.500');
}

/* Remove background grid pattern if not desired, or use subtle Gemini grays */
/* .bg-grid-pattern { ... } */

</style>
