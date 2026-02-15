/**
 * 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 深色模式
  const darkMode = ref(localStorage.getItem('darkMode') === 'true')

  // 加载状态
  const loading = ref(false)

  // Toast 消息
  const toastMessage = ref<string | null>(null)
  const toastType = ref<'success' | 'fail' | 'info'>('info')

  // 侧边栏展开状态
  const sidebarExpanded = ref(false)

  // 移动端菜单展开状态
  const mobileMenuOpen = ref(false)

  // 初始化
  initDarkMode()

  /**
   * 初始化深色模式
   */
  function initDarkMode() {
    // 优先使用系统设置
    if (!localStorage.getItem('darkMode')) {
      darkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyDarkMode()
  }

  /**
   * 应用深色模式
   */
  function applyDarkMode() {
    document.documentElement.classList.toggle('dark', darkMode.value)
    localStorage.setItem('darkMode', String(darkMode.value))
  }

  /**
   * 切换深色模式
   */
  function toggleDarkMode() {
    darkMode.value = !darkMode.value
    applyDarkMode()
  }

  /**
   * 设置深色模式
   */
  function setDarkMode(value: boolean) {
    darkMode.value = value
    applyDarkMode()
  }

  /**
   * 显示加载状态
   */
  function showLoading(message = '加载中...') {
    loading.value = true
    // vant Toast.loading(message)
    return loading
  }

  /**
   * 隐藏加载状态
   */
  function hideLoading() {
    loading.value = false
  }

  /**
   * 显示成功提示
   */
  function showSuccess(message: string) {
    toastMessage.value = message
    toastType.value = 'success'
    // vant Toast.success(message)
    clearToast()
  }

  /**
   * 显示失败提示
   */
  function showFail(message: string) {
    toastMessage.value = message
    toastType.value = 'fail'
    // vant Toast.fail(message)
    clearToast()
  }

  /**
   * 显示信息提示
   */
  function showInfo(message: string) {
    toastMessage.value = message
    toastType.value = 'info'
    // vant Toast.info(message)
    clearToast()
  }

  /**
   * 清除 Toast
   */
  function clearToast() {
    setTimeout(() => {
      toastMessage.value = null
    }, 3000)
  }

  /**
   * 切换侧边栏
   */
  function toggleSidebar() {
    sidebarExpanded.value = !sidebarExpanded.value
  }

  /**
   * 切换移动端菜单
   */
  function toggleMobileMenu() {
    mobileMenuOpen.value = !mobileMenuOpen.value
  }

  /**
   * 关闭移动端菜单
   */
  function closeMobileMenu() {
    mobileMenuOpen.value = false
  }

  return {
    // 状态
    darkMode,
    loading,
    toastMessage,
    toastType,
    sidebarExpanded,
    mobileMenuOpen,
    // 方法
    toggleDarkMode,
    setDarkMode,
    showLoading,
    hideLoading,
    showSuccess,
    showFail,
    showInfo,
    toggleSidebar,
    toggleMobileMenu,
    closeMobileMenu,
  }
})
