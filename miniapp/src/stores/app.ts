/**
 * 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 应用状态管理
 */
export const useAppStore = defineStore('app', () => {
  // 状态
  const isInitialized = ref(false)
  const isDarkMode = ref(false)
  const currentVersion = ref('1.0.0')
  const deviceInfo = ref<UniApp.DeviceInfo | null>(null)

  /**
   * 初始化应用
   */
  function initApp() {
    if (isInitialized.value) return

    // 获取设备信息
    deviceInfo.value = uni.getDeviceInfo()

    // 加载用户偏好设置
    loadPreferences()

    isInitialized.value = true
  }

  /**
   * 加载用户偏好设置
   */
  function loadPreferences() {
    try {
      const darkMode = uni.getStorageSync('dark_mode')
      if (darkMode !== '') {
        isDarkMode.value = darkMode
      }
    } catch (error) {
      console.error('加载用户偏好设置失败:', error)
    }
  }

  /**
   * 切换深色模式
   */
  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value
    uni.setStorageSync('dark_mode', isDarkMode.value)

    // 应用深色模式样式
    if (isDarkMode.value) {
      uni.setTheme({
        light: false
      })
    } else {
      uni.setTheme({
        light: true
      })
    }
  }

  /**
   * 设置深色模式
   */
  function setDarkMode(value: boolean) {
    isDarkMode.value = value
    uni.setStorageSync('dark_mode', value)
  }

  /**
   * 获取设备信息
   */
  function getDeviceInfo() {
    return deviceInfo.value
  }

  /**
   * 获取屏幕宽度
   */
  function getScreenWidth(): number {
    return deviceInfo.value?.windowWidth || 375
  }

  /**
   * 获取屏幕高度
   */
  function getScreenHeight(): number {
    return deviceInfo.value?.windowHeight || 667
  }

  /**
   * 检查是否为iOS设备
   */
  function isIOS(): boolean {
    return deviceInfo.value?.platform === 'ios'
  }

  /**
   * 检查是否为Android设备
   */
  function isAndroid(): boolean {
    return deviceInfo.value?.platform === 'android'
  }

  return {
    // 状态
    isInitialized,
    isDarkMode,
    currentVersion,
    deviceInfo,

    // 方法
    initApp,
    loadPreferences,
    toggleDarkMode,
    setDarkMode,
    getDeviceInfo,
    getScreenWidth,
    getScreenHeight,
    isIOS,
    isAndroid
  }
})
