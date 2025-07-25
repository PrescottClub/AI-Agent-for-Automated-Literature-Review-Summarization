<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted, ref } from 'vue'

const appReady = ref(false)

onMounted(() => {
  console.log('🚀 Tsearch App initializing...')

  // 模拟应用初始化
  setTimeout(() => {
    appReady.value = true
    console.log('✅ Tsearch App ready with perfect animations')
  }, 100)
})
</script>

<template>
  <div id="app" class="min-h-screen bg-neutral-50 text-neutral-900 font-sans">
    <main class="relative">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* 简化的App样式 */
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
