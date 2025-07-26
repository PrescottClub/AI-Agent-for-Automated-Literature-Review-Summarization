import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { AppSettings } from '@/types/paper'

export const useSettingsStore = defineStore('settings', () => {
  // 默认设置 - 只使用ArXiv
  const defaultSettings: AppSettings = {
    defaultSources: ['arxiv'],
    defaultMaxPapers: 20,
    language: 'zh',
    theme: 'auto',
  }

  // 当前设置
  const settings = ref<AppSettings>({ ...defaultSettings })

  // 显示设置对话框
  const showSettingsDialog = ref(false)

  // 应用设置
  const applySettings = (newSettings: Partial<AppSettings>) => {
    settings.value = { ...settings.value, ...newSettings }
    saveToStorage()
  }

  // 重置设置
  const resetSettings = () => {
    settings.value = { ...defaultSettings }
    saveToStorage()
  }

  // 保存到本地存储
  const saveToStorage = () => {
    localStorage.setItem('appSettings', JSON.stringify(settings.value))
  }

  // 从本地存储加载
  const loadFromStorage = () => {
    const saved = localStorage.getItem('appSettings')
    if (saved) {
      try {
        const parsedSettings = JSON.parse(saved)
        settings.value = { ...defaultSettings, ...parsedSettings }
      } catch (error) {
        console.error('Failed to load settings:', error)
        settings.value = { ...defaultSettings }
      }
    }
  }

  // 监听设置变化并自动保存
  watch(
    settings,
    () => {
      saveToStorage()
    },
    { deep: true },
  )

  return {
    settings,
    showSettingsDialog,
    applySettings,
    resetSettings,
    loadFromStorage,
  }
})
