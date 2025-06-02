<template>
  <div v-if="papers && papers.length > 0" class="results-grid">
    <PaperCard
      v-for="(paper, index) in papers"
      :key="paper.id"
      :paper="paper"
      :index="index + 1"
      @toggle-favorite="$emit('toggle-favorite', $event)"
      @view-details="$emit('view-details', $event)"
      @download-pdf="$emit('download-pdf', $event)"
      class="paper-card-animated"
      :style="{ animationDelay: `${index * 0.1}s` }"
    />
  </div>

  <div v-else-if="showEmpty" class="empty-results">
    <div class="empty-icon">📚</div>
    <h3 class="empty-title">No Results Found</h3>
    <p class="empty-text">Try adjusting your search terms or expanding your criteria</p>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import type { Paper } from '@/types/paper'
import PaperCard from './PaperCard.vue'

defineProps({
  papers: {
    type: Array as PropType<Paper[]>,
    default: () => []
  },
  showEmpty: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-favorite', 'view-details', 'download-pdf'])
</script>

<style scoped>
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
  animation: fadeIn 0.6s ease forwards;
}

.paper-card-animated {
  animation: slideInUp 0.6s ease forwards;
  opacity: 0;
}

.empty-results {
  text-align: center;
  padding: 80px 20px;
  opacity: 0.7;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  margin: 0 0 12px 0;
}

.empty-text {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .results-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .empty-results {
    padding: 60px 20px;
  }

  .empty-icon {
    font-size: 3rem;
  }

  .empty-title {
    font-size: 1.25rem;
  }
}
</style>
