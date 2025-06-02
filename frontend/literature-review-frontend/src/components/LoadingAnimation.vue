<template>
  <div class="loading-container">
    <div class="loading-orb">
      <div class="loading-core"></div>
      <div class="loading-ring"></div>
      <div class="loading-ring secondary"></div>
    </div>

    <h3 class="loading-title">{{ title || 'AI Processing Your Query' }}</h3>
    <p class="loading-text">{{ subtitle || 'Analyzing requirements and searching literature...' }}</p>

    <div v-if="showProgress && progressSteps.length > 0" class="progress-steps">
      <div
        v-for="(step, index) in progressSteps"
        :key="index"
        class="progress-step"
        :class="{ active: index <= currentStep, completed: index < currentStep }"
      >
        <div class="step-indicator">
          <div v-if="index < currentStep" class="step-check">✓</div>
          <div v-else class="step-number">{{ index + 1 }}</div>
        </div>
        <span class="step-label">{{ step }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  progressSteps: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  currentStep: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.loading-container {
  text-align: center;
  padding: 80px 20px;
}

.loading-orb {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 32px;
}

.loading-core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 2s ease-in-out infinite;
}

.loading-ring {
  position: absolute;
  inset: 0;
  border: 2px solid transparent;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.loading-ring.secondary {
  border-top-color: #8b5cf6;
  animation-duration: 2s;
  animation-direction: reverse;
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 12px 0;
}

.loading-text {
  color: rgba(255, 255, 255, 0.6);
  margin: 0 0 32px 0;
}

.progress-steps {
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  opacity: 0.4;
}

.progress-step.active {
  opacity: 1;
  background: rgba(59, 130, 246, 0.1);
}

.progress-step.completed {
  opacity: 0.8;
  background: rgba(34, 197, 94, 0.1);
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.progress-step.active .step-indicator {
  background: #3b82f6;
}

.progress-step.completed .step-indicator {
  background: #22c55e;
}

.step-check {
  font-size: 14px;
  font-weight: bold;
}

.step-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.progress-step.active .step-label {
  color: white;
  font-weight: 500;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.05);
  }
}

@media (max-width: 640px) {
  .loading-container {
    padding: 60px 20px;
  }

  .loading-orb {
    width: 100px;
    height: 100px;
  }

  .loading-core {
    width: 50px;
    height: 50px;
  }

  .loading-title {
    font-size: 1.25rem;
  }
}
</style>
