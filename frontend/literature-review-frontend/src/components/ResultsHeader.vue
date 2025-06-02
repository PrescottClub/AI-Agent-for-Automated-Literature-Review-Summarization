<template>
  <div class="results-header">
    <div class="results-info">
      <h2 class="results-title">Research Results</h2>
      <p class="results-count">{{ resultCount }} papers found</p>
    </div>

    <el-button
      type="success"
      :loading="isGeneratingReport"
      :disabled="resultCount === 0"
      @click="$emit('generate-report')"
      class="generate-report-btn"
    >
      <el-icon v-if="isGeneratingReport" class="animate-spin">
        <Loading />
      </el-icon>
      <el-icon v-else>
        <Document />
      </el-icon>
      {{ isGeneratingReport ? 'Generating...' : 'Generate Report' }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { Document, Loading } from '@element-plus/icons-vue'

defineProps({
  resultCount: {
    type: Number,
    default: 0
  },
  isGeneratingReport: {
    type: Boolean,
    default: false
  }
})

defineEmits(['generate-report'])
</script>

<style scoped>
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.results-info {
  flex: 1;
}

.results-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 4px 0;
}

.results-count {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.generate-report-btn {
  min-width: 160px;
}

@media (max-width: 640px) {
  .results-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .generate-report-btn {
    width: 100%;
  }
}
</style>
