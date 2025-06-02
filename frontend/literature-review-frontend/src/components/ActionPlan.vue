<template>
  <div v-if="actionPlan && actionPlan.length > 0" class="action-plan">
    <div class="plan-header">
      <div class="plan-icon">🤖</div>
      <h3 class="plan-title">AI Execution Plan</h3>
    </div>

    <div class="plan-steps">
      <div
        v-for="(step, index) in actionPlan"
        :key="index"
        class="plan-step"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="step-number">
          {{ index + 1 }}
        </div>
        <p class="step-text">{{ step }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

defineProps({
  actionPlan: {
    type: Array as PropType<string[]>,
    default: () => []
  }
})
</script>

<style scoped>
.action-plan {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  backdrop-filter: blur(20px);
  animation: fadeIn 0.6s ease forwards;
}

.plan-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.plan-icon {
  font-size: 1.5rem;
}

.plan-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
}

.plan-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.plan-step {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  animation: slideInUp 0.5s ease forwards;
}

.step-number {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.step-text {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  margin: 0;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
