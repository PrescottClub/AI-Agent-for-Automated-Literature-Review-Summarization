<template>
  <div class="search-form">
    <div class="search-input-container">
      <el-input
        v-model="searchQuery"
        type="textarea"
        :autosize="{ minRows: 3, maxRows: 6 }"
        placeholder="输入你的研究查询，例如：人工智能在医疗诊断中的应用..."
        class="search-input"
        :disabled="searchStore.isSearching"
        @keyup.enter.ctrl="handleSearch"
      />
    </div>

    <div class="search-actions">
      <div class="search-tips">
        <span class="modern-kbd">Ctrl</span> + <span class="modern-kbd">Enter</span> 搜索
      </div>

      <el-button
        type="primary"
        :loading="searchStore.isSearching"
        :disabled="!searchQuery.trim()"
        @click="handleSearch"
      >
        <el-icon><Search /></el-icon>
        {{ searchStore.isSearching ? '搜索中...' : '开始搜索' }}
      </el-button>
    </div>

    <!-- 搜索建议 -->
    <div v-if="suggestions.length > 0" class="suggestions">
      <p class="suggestions-title">快速开始</p>
      <div class="suggestions-grid">
        <button
          v-for="suggestion in suggestions"
          :key="suggestion"
          class="suggestion-pill"
          @click="searchQuery = suggestion; handleSearch()"
        >
          {{ suggestion }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useSearchStore } from '@/stores/searchStore'

// 使用状态管理
const searchStore = useSearchStore()

// 本地状态
const searchQuery = ref('')

// 搜索建议
const suggestions = ref([
  '最近三年人工智能在医疗诊断领域的应用进展',
  '深度学习优化算法的最新研究，重点关注transformer架构',
  '2020年以来量子计算在密码学中的应用研究'
])

// 搜索处理
const handleSearch = async () => {
  if (!searchQuery.value.trim()) return

  try {
    await searchStore.startSearch(searchQuery.value)
  } catch (error) {
    console.error('Search failed:', error)
  }
}
</script>

<style scoped>
.search-form {
  max-width: 800px;
  margin: 0 auto;
}

.search-input-container {
  margin-bottom: 1rem;
}

.search-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  padding: 16px;
  font-size: 16px;
  line-height: 1.6;
  transition: all 0.2s ease;
}

.search-input :deep(.el-textarea__inner):focus {
  border-color: #1a73e8;
  box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.1);
}

.search-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-tips {
  color: #6b7280;
  font-size: 14px;
}

.suggestions {
  border-top: 1px solid #e5e7eb;
  padding-top: 1.5rem;
}

.suggestions-title {
  color: #6b7280;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.suggestions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.suggestion-pill {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.suggestion-pill:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

@media (max-width: 640px) {
  .search-actions {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .suggestion-pill {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
