/**
 * 轻量级动画系统
 * 使用纯CSS动画和简单的JavaScript控制
 */

export class SimpleAnimations {
  /**
   * 淡入动画
   */
  static fadeIn(element: HTMLElement, duration: number = 300): void {
    element.style.opacity = '0'
    element.style.transition = `opacity ${duration}ms ease-out`
    
    requestAnimationFrame(() => {
      element.style.opacity = '1'
    })
  }

  /**
   * 淡入上升动画
   */
  static fadeInUp(element: HTMLElement, duration: number = 500, delay: number = 0): void {
    element.style.opacity = '0'
    element.style.transform = 'translateY(20px)'
    element.style.transition = `all ${duration}ms ease-out ${delay}ms`
    
    requestAnimationFrame(() => {
      element.style.opacity = '1'
      element.style.transform = 'translateY(0)'
    })
  }

  /**
   * 缩放动画
   */
  static scaleIn(element: HTMLElement, duration: number = 300): void {
    element.style.transform = 'scale(0.9)'
    element.style.opacity = '0'
    element.style.transition = `all ${duration}ms ease-out`
    
    requestAnimationFrame(() => {
      element.style.transform = 'scale(1)'
      element.style.opacity = '1'
    })
  }

  /**
   * 滑入动画
   */
  static slideIn(element: HTMLElement, direction: 'left' | 'right' | 'up' | 'down' = 'up', duration: number = 400): void {
    const transforms = {
      left: 'translateX(-30px)',
      right: 'translateX(30px)',
      up: 'translateY(30px)',
      down: 'translateY(-30px)'
    }
    
    element.style.opacity = '0'
    element.style.transform = transforms[direction]
    element.style.transition = `all ${duration}ms ease-out`
    
    requestAnimationFrame(() => {
      element.style.opacity = '1'
      element.style.transform = 'translate(0, 0)'
    })
  }

  /**
   * 批量动画
   */
  static animateSequence(elements: HTMLElement[], animationType: 'fadeInUp' | 'slideIn' = 'fadeInUp', stagger: number = 100): void {
    elements.forEach((element, index) => {
      const delay = index * stagger
      
      if (animationType === 'fadeInUp') {
        this.fadeInUp(element, 500, delay)
      } else if (animationType === 'slideIn') {
        setTimeout(() => this.slideIn(element), delay)
      }
    })
  }

  /**
   * 悬停效果
   */
  static addHoverEffect(element: HTMLElement): void {
    element.style.transition = 'transform 0.3s ease-out, box-shadow 0.3s ease-out'
    
    element.addEventListener('mouseenter', () => {
      element.style.transform = 'translateY(-4px)'
      element.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.15)'
    })
    
    element.addEventListener('mouseleave', () => {
      element.style.transform = 'translateY(0)'
      element.style.boxShadow = ''
    })
  }

  /**
   * 脉冲动画
   */
  static pulse(element: HTMLElement): void {
    element.style.animation = 'pulse 2s infinite'
  }

  /**
   * 移除所有动画
   */
  static removeAnimations(element: HTMLElement): void {
    element.style.transition = ''
    element.style.transform = ''
    element.style.opacity = ''
    element.style.animation = ''
  }
}

/**
 * 动画工具函数
 */
export const animationUtils = {
  /**
   * 等待动画完成
   */
  waitForAnimation(element: HTMLElement): Promise<void> {
    return new Promise((resolve) => {
      const handleAnimationEnd = () => {
        element.removeEventListener('transitionend', handleAnimationEnd)
        element.removeEventListener('animationend', handleAnimationEnd)
        resolve()
      }
      
      element.addEventListener('transitionend', handleAnimationEnd)
      element.addEventListener('animationend', handleAnimationEnd)
    })
  },

  /**
   * 检查元素是否在视口中
   */
  isInViewport(element: HTMLElement): boolean {
    const rect = element.getBoundingClientRect()
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    )
  },

  /**
   * 滚动触发动画
   */
  onScrollIntoView(element: HTMLElement, callback: () => void): void {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          callback()
          observer.unobserve(element)
        }
      })
    }, { threshold: 0.1 })
    
    observer.observe(element)
  }
}
