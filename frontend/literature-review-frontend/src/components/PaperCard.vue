<template>
  <div class="paper-card-3d" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave" ref="cardRef">
    <!-- Dynamic Background Gradient -->
    <div class="card-bg-gradient" :style="gradientStyle"></div>

    <!-- Floating Elements -->
    <div class="floating-elements">
      <div class="floating-dot dot-1"></div>
      <div class="floating-dot dot-2"></div>
      <div class="floating-dot dot-3"></div>
    </div>

    <!-- Card Content -->
    <div class="card-content">
      <!-- Header with 3D Badge -->
      <div class="card-header">
        <div class="index-badge">
          <span class="badge-text">#{{ index }}</span>
          <div class="badge-glow"></div>
        </div>

        <div class="status-indicators">
          <div v-if="paper.fullTextRetrieved" class="status-pill success">
            <div class="pill-dot"></div>
            <span>Full Text</span>
          </div>
          <div class="source-tag" :class="getSourceColor(paper.source)">
            {{ paper.source }}
          </div>
        </div>

        <button @click.stop="toggleFavorite" class="favorite-btn" :class="{ active: paper.isFavorite }">
          <div class="star-container">
            <el-icon class="star-icon">
              <StarFilled v-if="paper.isFavorite" />
              <Star v-else />
            </el-icon>
            <div class="star-glow"></div>
          </div>
        </button>
      </div>

      <!-- Title with Magnetic Effect -->
      <div class="title-container" @click="viewDetails">
        <h3 class="paper-title">{{ paper.title }}</h3>
        <div class="title-underline"></div>
      </div>

      <!-- Meta Information with Icons -->
      <div class="meta-section">
        <div class="meta-item">
          <div class="meta-icon">
            <el-icon><User /></el-icon>
          </div>
          <span class="meta-text">{{ formatAuthors(paper.authors) }}</span>
        </div>

        <div class="meta-item">
          <div class="meta-icon">
            <el-icon><Calendar /></el-icon>
          </div>
          <span class="meta-text">{{ formatDate(paper.publishedDate) }}</span>
        </div>

        <div v-if="paper.citations" class="meta-item citations">
          <div class="meta-icon">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <span class="meta-text">{{ paper.citations }} citations</span>
        </div>
      </div>

      <!-- Abstract with Gradient Fade -->
      <div class="abstract-container">
        <p class="abstract-text">{{ paper.summary }}</p>
        <div class="abstract-fade"></div>
      </div>

      <!-- Keywords with Floating Animation -->
      <div v-if="paper.keywords && paper.keywords.length > 0" class="keywords-section">
        <div class="keywords-grid">
          <span
            v-for="(keyword, index) in paper.keywords.slice(0, 4)"
            :key="keyword"
            class="keyword-pill"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            {{ keyword }}
          </span>
          <span v-if="paper.keywords.length > 4" class="more-keywords">
            +{{ paper.keywords.length - 4 }}
          </span>
        </div>
      </div>

      <!-- Action Buttons with Morphing Effects -->
      <div class="actions-section">
        <div class="primary-actions">
          <button v-if="paper.url" @click.stop="openLink(paper.url)" class="action-btn primary">
            <div class="btn-content">
              <el-icon class="btn-icon"><Link /></el-icon>
              <span>View Paper</span>
            </div>
            <div class="btn-ripple"></div>
          </button>

          <button v-if="paper.pdfUrl" @click.stop="downloadPdf" class="action-btn secondary">
            <div class="btn-content">
              <el-icon class="btn-icon"><Download /></el-icon>
              <span>Download</span>
            </div>
            <div class="btn-ripple"></div>
          </button>
        </div>

        <div class="secondary-actions">
          <button @click.stop="viewDetails" class="icon-btn" title="View Details">
            <el-icon><View /></el-icon>
            <div class="icon-btn-glow"></div>
          </button>
          <button class="icon-btn" title="Share">
            <el-icon><Share /></el-icon>
            <div class="icon-btn-glow"></div>
          </button>
        </div>
      </div>
    </div>

    <!-- Holographic Border Effect -->
    <div class="holographic-border"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { StarFilled, Star, User, Calendar, Link, Download, View, TrendCharts, Share } from '@element-plus/icons-vue'
import type { PropType } from 'vue'

export interface Paper {
  id: string
  title: string
  authors: string[]
  publishedDate: string
  source: string
  summary: string
  keywords?: string[]
  url?: string
  pdfUrl?: string
  fullTextRetrieved?: boolean
  citations?: number
  isFavorite?: boolean
}

const props = defineProps({
  paper: {
    type: Object as PropType<Paper>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const emit = defineEmits([
  'toggle-favorite',
  'view-details',
  'download-pdf'
])

// 3D Effect State
const cardRef = ref<HTMLElement>()
const mouseX = ref(0)
const mouseY = ref(0)
const isHovered = ref(false)

const gradientStyle = computed(() => {
  if (!isHovered.value) return {}

  const x = mouseX.value
  const y = mouseY.value

  return {
    background: `radial-gradient(circle at ${x}% ${y}%, rgba(59, 130, 246, 0.15) 0%, rgba(147, 51, 234, 0.1) 50%, transparent 70%)`
  }
})

const handleMouseMove = (e: MouseEvent) => {
  if (!cardRef.value) return

  const rect = cardRef.value.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100

  mouseX.value = x
  mouseY.value = y
  isHovered.value = true

  // 3D Transform
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const rotateX = ((e.clientY - rect.top) - centerY) / 10
  const rotateY = ((e.clientX - rect.left) - centerX) / 10

  cardRef.value.style.transform = `perspective(1000px) rotateX(${-rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`
}

const handleMouseLeave = () => {
  isHovered.value = false
  if (cardRef.value) {
    cardRef.value.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)'
  }
}

const getSourceColor = (source: string) => {
  const colors: Record<string, string> = {
    'arXiv': 'arxiv',
    'Semantic Scholar': 'scholar',
    'PubMed': 'pubmed',
    'default': 'default'
  }
  return colors[source] || colors.default
}

// Event Handlers
const formatAuthors = (authors: string[] | undefined) => {
  if (!authors || authors.length === 0) return 'Unknown Authors'
  if (authors.length <= 2) return authors.join(', ')
  return `${authors[0]} et al.`
}

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return 'Unknown Date'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' })
  } catch {
    return dateString
  }
}

const openLink = (url: string | undefined) => {
  if (url && url !== '#') {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

const toggleFavorite = () => {
  emit('toggle-favorite', props.paper.id)
}

const viewDetails = () => {
  emit('view-details', props.paper)
}

const downloadPdf = () => {
  emit('download-pdf', props.paper)
}
</script>

<style scoped>
/* === CORE CARD STYLING === */
.paper-card-3d {
  position: relative;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 0;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  transform-style: preserve-3d;
  cursor: pointer;
  min-height: 400px;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.paper-card-3d:hover {
  box-shadow:
    0 30px 60px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(59, 130, 246, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

/* === BACKGROUND EFFECTS === */
.card-bg-gradient {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.paper-card-3d:hover .card-bg-gradient {
  opacity: 1;
}

.floating-elements {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  border-radius: 20px;
}

.floating-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(59, 130, 246, 0.6);
  border-radius: 50%;
  filter: blur(1px);
}

.dot-1 {
  top: 20%;
  left: 85%;
  animation: floatDot 4s ease-in-out infinite;
}

.dot-2 {
  top: 70%;
  left: 10%;
  animation: floatDot 4s ease-in-out infinite reverse;
  animation-delay: -2s;
}

.dot-3 {
  top: 40%;
  right: 15%;
  animation: floatDot 4s ease-in-out infinite;
  animation-delay: -1s;
}

@keyframes floatDot {
  0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0.3; }
  50% { transform: translateY(-10px) translateX(5px); opacity: 1; }
}

/* === HOLOGRAPHIC BORDER === */
.holographic-border {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  background: linear-gradient(45deg,
    transparent 30%,
    rgba(59, 130, 246, 0.1) 50%,
    transparent 70%
  );
  background-size: 200% 200%;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
  animation: holographicShift 3s ease infinite;
}

.paper-card-3d:hover .holographic-border {
  opacity: 1;
}

@keyframes holographicShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* === CARD CONTENT === */
.card-content {
  position: relative;
  z-index: 10;
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* === HEADER SECTION === */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.index-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 51, 234, 0.2));
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.index-badge:hover {
  transform: scale(1.1) translateZ(10px);
}

.badge-text {
  font-size: 14px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
}

.badge-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 14px;
  filter: blur(8px);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.index-badge:hover .badge-glow {
  opacity: 0.6;
}

.status-indicators {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-direction: column;
}

.status-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  backdrop-filter: blur(10px);
}

.status-pill.success {
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: rgba(34, 197, 94, 1);
}

.pill-dot {
  width: 6px;
  height: 6px;
  background: currentColor;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.source-tag {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.source-tag.arxiv {
  background: rgba(183, 28, 28, 0.2);
  border: 1px solid rgba(183, 28, 28, 0.3);
  color: rgba(252, 165, 165, 1);
}

.source-tag.scholar {
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: rgba(147, 197, 253, 1);
}

.source-tag.default {
  background: rgba(107, 114, 128, 0.2);
  border: 1px solid rgba(107, 114, 128, 0.3);
  color: rgba(209, 213, 219, 1);
}

/* === FAVORITE BUTTON === */
.favorite-btn {
  position: relative;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.star-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.star-icon {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  z-index: 2;
}

.favorite-btn.active .star-icon {
  color: #fbbf24;
  transform: scale(1.2);
}

.star-glow {
  position: absolute;
  inset: -4px;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.favorite-btn.active .star-glow {
  opacity: 1;
}

.favorite-btn:hover .star-icon {
  transform: scale(1.1);
  color: #fbbf24;
}

/* === TITLE SECTION === */
.title-container {
  position: relative;
  cursor: pointer;
  margin-bottom: 12px;
}

.paper-title {
  font-size: 18px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: all 0.3s ease;
}

.title-container:hover .paper-title {
  color: rgba(59, 130, 246, 0.9);
  transform: translateX(4px);
}

.title-underline {
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 1px;
  width: 0;
  transition: width 0.4s ease;
}

.title-container:hover .title-underline {
  width: 100%;
}

/* === META SECTION === */
.meta-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.meta-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.2s ease;
}

.meta-item:hover .meta-icon {
  background: rgba(59, 130, 246, 0.2);
  color: rgba(59, 130, 246, 0.9);
  transform: scale(1.1);
}

.meta-text {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.meta-item.citations .meta-icon {
  background: rgba(34, 197, 94, 0.1);
  color: rgba(34, 197, 94, 0.8);
}

/* === ABSTRACT === */
.abstract-container {
  position: relative;
  flex: 1;
  margin-bottom: 16px;
}

.abstract-text {
  font-size: 14px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.abstract-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(transparent, rgba(255, 255, 255, 0.05));
  pointer-events: none;
}

/* === KEYWORDS === */
.keywords-section {
  margin-bottom: 20px;
}

.keywords-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.keyword-pill {
  padding: 4px 10px;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.25);
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  color: rgba(147, 197, 253, 0.9);
  transition: all 0.3s ease;
  animation: slideInUp 0.5s ease forwards;
}

.keyword-pill:hover {
  background: rgba(59, 130, 246, 0.25);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.more-keywords {
  padding: 4px 10px;
  background: rgba(107, 114, 128, 0.15);
  border: 1px solid rgba(107, 114, 128, 0.25);
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  color: rgba(156, 163, 175, 0.9);
}

/* === ACTIONS === */
.actions-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.primary-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  position: relative;
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 8px 16px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.action-btn.primary {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
  border-color: rgba(59, 130, 246, 0.3);
}

.action-btn.secondary {
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.2), rgba(147, 51, 234, 0.1));
  border-color: rgba(147, 51, 234, 0.3);
}

.btn-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.btn-icon {
  font-size: 14px;
}

.btn-ripple {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  transform: scale(0);
  opacity: 0;
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.action-btn:hover .btn-ripple {
  transform: scale(1);
  opacity: 1;
}

.secondary-actions {
  display: flex;
  gap: 4px;
}

.icon-btn {
  position: relative;
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
}

.icon-btn:hover {
  color: rgba(59, 130, 246, 0.9);
  background: rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.icon-btn-glow {
  position: absolute;
  inset: 0;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.icon-btn:hover .icon-btn-glow {
  opacity: 1;
}

/* === ANIMATIONS === */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

/* === RESPONSIVE === */
@media (max-width: 640px) {
  .card-content {
    padding: 20px;
  }

  .paper-title {
    font-size: 16px;
  }

  .meta-section {
    gap: 6px;
  }

  .meta-item {
    font-size: 12px;
  }

  .actions-section {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .primary-actions {
    justify-content: center;
  }

  .secondary-actions {
    justify-content: center;
  }
}
</style>
