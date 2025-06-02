/**
 * 防抖函数 - 防止快速重复调用
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number,
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }

    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数 - 限制调用频率
 */
export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number,
): (...args: Parameters<T>) => void {
  let inThrottle: boolean

  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * 延迟加载图片
 */
export function lazyLoadImage(src: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(src)
    img.onerror = reject
    img.src = src
  })
}

/**
 * 检查是否支持现代浏览器特性
 */
export const browserSupport = {
  intersectionObserver: 'IntersectionObserver' in window,
  webp: () => {
    const canvas = document.createElement('canvas')
    canvas.width = 1
    canvas.height = 1
    return canvas.toDataURL('image/webp').indexOf('webp') !== -1
  },
  localStorage: (() => {
    try {
      localStorage.setItem('test', 'test')
      localStorage.removeItem('test')
      return true
    } catch {
      return false
    }
  })(),
  requestIdleCallback: 'requestIdleCallback' in window,
}

/**
 * 批量处理任务以避免阻塞主线程
 */
export function batchProcess<T>(
  items: T[],
  processor: (item: T) => void,
  batchSize = 50,
): Promise<void> {
  return new Promise((resolve) => {
    let index = 0

    function processBatch() {
      const endIndex = Math.min(index + batchSize, items.length)

      for (; index < endIndex; index++) {
        processor(items[index])
      }

      if (index < items.length) {
        if (browserSupport.requestIdleCallback) {
          requestIdleCallback(processBatch)
        } else {
          setTimeout(processBatch, 0)
        }
      } else {
        resolve()
      }
    }

    processBatch()
  })
}

/**
 * 内存友好的大数组处理
 */
export function createVirtualList<T>(items: T[], containerHeight: number, itemHeight: number) {
  const visibleCount = Math.ceil(containerHeight / itemHeight)
  const bufferSize = Math.min(5, visibleCount)

  return {
    getVisibleItems: (scrollTop: number) => {
      const startIndex = Math.floor(scrollTop / itemHeight)
      const endIndex = Math.min(startIndex + visibleCount + bufferSize, items.length)
      const actualStartIndex = Math.max(0, startIndex - bufferSize)

      return {
        items: items.slice(actualStartIndex, endIndex),
        startIndex: actualStartIndex,
        offsetY: actualStartIndex * itemHeight,
      }
    },
    getTotalHeight: () => items.length * itemHeight,
  }
}

/**
 * 简单的缓存实现
 */
export class SimpleCache<T> {
  private cache = new Map<string, { data: T; timestamp: number }>()
  private maxAge: number
  private maxSize: number

  constructor(maxAge = 5 * 60 * 1000, maxSize = 100) {
    // 5分钟，100条
    this.maxAge = maxAge
    this.maxSize = maxSize
  }

  get(key: string): T | null {
    const item = this.cache.get(key)

    if (!item) return null

    if (Date.now() - item.timestamp > this.maxAge) {
      this.cache.delete(key)
      return null
    }

    return item.data
  }

  set(key: string, data: T): void {
    // 清理过期数据
    if (this.cache.size >= this.maxSize) {
      const oldestKey = this.cache.keys().next().value
      if (oldestKey) {
        this.cache.delete(oldestKey)
      }
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    })
  }

  clear(): void {
    this.cache.clear()
  }

  size(): number {
    return this.cache.size
  }
}

/**
 * 预加载关键资源
 */
export function preloadResources(urls: string[]): Promise<unknown[]> {
  return Promise.allSettled(
    urls.map((url) => {
      if (url.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
        return lazyLoadImage(url)
      } else {
        return fetch(url, { method: 'HEAD' })
      }
    }),
  )
}
