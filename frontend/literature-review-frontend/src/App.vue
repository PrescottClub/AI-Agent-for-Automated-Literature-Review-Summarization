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

/* Modern UI Components */
.modern-nav-button {
  @apply flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white/60 border border-gray-200/50 rounded-lg hover:bg-white/80 hover:text-brand-600 hover:border-brand-300 transition-all duration-200 backdrop-blur-sm;
}

.mobile-nav-link-modern {
  @apply flex items-center w-full px-4 py-3 text-sm font-medium text-gray-700 hover:bg-white/60 hover:text-brand-600 rounded-lg transition-all duration-200;
}

.modern-search-button {
  @apply relative px-6 py-3 bg-gradient-to-r from-brand-500 to-brand-600 text-white font-semibold rounded-xl shadow-lg hover:from-brand-600 hover:to-brand-700 hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none overflow-hidden;
}

.modern-action-button {
  @apply relative px-5 py-2.5 bg-gradient-to-r from-gray-600 to-gray-700 text-white font-medium rounded-lg shadow-md hover:from-gray-700 hover:to-gray-800 hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none overflow-hidden;
}

.modern-textarea .el-textarea__inner {
  @apply border-2 border-gray-200 rounded-xl bg-gray-50/50 backdrop-blur-sm focus:border-brand-400 focus:bg-white transition-all duration-200 resize-none font-medium;
  min-height: 120px !important;
}

.modern-kbd {
  @apply px-2 py-1 bg-gray-100 border border-gray-300 rounded-md text-gray-700 font-mono text-xs shadow-sm;
}

.suggestion-chip {
  @apply relative px-4 py-2 text-sm font-medium text-brand-700 bg-gradient-to-r from-brand-50 to-purple-50 border border-brand-200/50 rounded-full hover:border-brand-300 hover:shadow-md transition-all duration-200 animate-fade-in-up overflow-hidden;
}

.advanced-toggle-button {
  @apply relative inline-flex items-center px-6 py-3 text-sm font-medium text-gray-600 bg-white/60 border border-gray-200/50 rounded-full hover:text-brand-600 hover:border-brand-300 hover:bg-white/80 transition-all duration-200 backdrop-blur-sm overflow-hidden;
}

.modern-select .el-select__wrapper {
  @apply border-2 border-gray-200 rounded-lg bg-gray-50/50 backdrop-blur-sm hover:border-gray-300 focus:border-brand-400 transition-all duration-200;
}

.modern-slider .el-slider__runway {
  @apply bg-gray-200 rounded-full;
}

.modern-slider .el-slider__bar {
  @apply bg-gradient-to-r from-brand-400 to-brand-500 rounded-full;
}

.modern-slider .el-slider__button {
  @apply border-2 border-white shadow-lg bg-gradient-to-r from-brand-400 to-brand-500;
}

.modern-checkbox .el-checkbox__input.is-checked .el-checkbox__inner {
  @apply bg-gradient-to-r from-brand-400 to-brand-500 border-brand-500;
}

.modern-checkbox-label {
  @apply flex items-center cursor-pointer hover:text-brand-600 transition-colors duration-200;
}

/* Enhanced animations */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-shimmer {
  animation: shimmer 2s linear infinite;
  background: linear-gradient(110deg, #f0f0f0 8%, #e0e0e0 18%, #f0f0f0 33%);
  background-size: 200px 100%;
}

/* Glass morphism effects */
.glass-card {
  backdrop-filter: blur(20px) saturate(180%);
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

/* Gradient text utilities */
.text-gradient-brand {
  background: linear-gradient(135deg, #1a73e8 0%, #4285f4 50%, #8ab4f8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.text-gradient-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Responsive improvements */
@media (max-width: 640px) {
  .modern-search-button {
    @apply w-full justify-center;
  }

  .suggestion-chip {
    @apply text-xs px-3 py-1.5;
  }
}

</style>
