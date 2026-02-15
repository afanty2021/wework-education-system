/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import AuthAPI from '@/api/auth'

/**
 * 用户信息接口
 */
interface UserInfo {
  id: number
  name: string
  avatar: string | null
  role: string
  wework_id: string | null
  phone?: string
  student_id?: number
}

/**
 * 用户状态管理
 */
export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string | null>(null)
  const userInfo = ref<UserInfo | null>(null)
  const isLoggedIn = ref(false)
  const loading = ref(false)

  // 计算属性
  const userId = computed(() => userInfo.value?.id || 0)
  const userName = computed(() => userInfo.value?.name || '未知用户')
  const userAvatar = computed(() => userInfo.value?.avatar || '/static/images/default-avatar.png')
  const userRole = computed(() => userInfo.value?.role || 'student')

  /**
   * 初始化：从本地存储恢复登录状态
   */
  function initFromStorage() {
    try {
      const storedToken = uni.getStorageSync('auth_token')
      const storedUserInfo = uni.getStorageSync('user_info')

      if (storedToken && storedUserInfo) {
        token.value = storedToken
        userInfo.value = JSON.parse(storedUserInfo)
        isLoggedIn.value = true
      }
    } catch (error) {
      console.error('从本地存储恢复登录状态失败:', error)
    }
  }

  /**
   * 检查登录状态
   */
  async function checkLoginStatus() {
    initFromStorage()

    if (token.value) {
      try {
        // 验证Token有效性
        const user = await AuthAPI.getCurrentUser()
        userInfo.value = user
        isLoggedIn.value = true
      } catch (error) {
        // Token无效，清除登录状态
        console.error('登录状态验证失败:', error)
        logout()
      }
    }
  }

  /**
   * 微信登录
   */
  async function wechatLogin(code: string, userInfo?: Record<string, unknown>) {
    loading.value = true
    try {
      const response = await AuthAPI.wechatLogin({ code, userInfo })

      // 保存Token
      token.value = response.access_token
      isLoggedIn.value = true

      // 持久化存储
      uni.setStorageSync('auth_token', response.access_token)

      // 获取用户信息
      const user = await AuthAPI.getCurrentUser()
      userInfo.value = user
      uni.setStorageSync('user_info', JSON.stringify(user))

      return user
    } catch (error) {
      console.error('微信登录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取用户信息
   */
  async function fetchUserInfo() {
    if (!token.value) return null

    try {
      const user = await AuthAPI.getCurrentUser()
      userInfo.value = user
      uni.setStorageSync('user_info', JSON.stringify(user))
      return user
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return null
    }
  }

  /**
   * 更新用户信息
   */
  function updateUserInfo(info: Partial<UserInfo>) {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...info }
      uni.setStorageSync('user_info', JSON.stringify(userInfo.value))
    }
  }

  /**
   * 退出登录
   */
  async function logout() {
    try {
      await AuthAPI.logout()
    } catch (error) {
      console.error('退出登录请求失败:', error)
    } finally {
      // 清除状态
      token.value = null
      userInfo.value = null
      isLoggedIn.value = false

      // 清除本地存储
      uni.removeStorageSync('auth_token')
      uni.removeStorageSync('user_info')
    }
  }

  /**
   * 设置Token
   */
  function setToken(newToken: string) {
    token.value = newToken
    isLoggedIn.value = true
    uni.setStorageSync('auth_token', newToken)
  }

  /**
   * 清除所有状态
   */
  function clearAll() {
    token.value = null
    userInfo.value = null
    isLoggedIn.value = false
    uni.removeStorageSync('auth_token')
    uni.removeStorageSync('user_info')
  }

  return {
    // 状态
    token,
    userInfo,
    isLoggedIn,
    loading,

    // 计算属性
    userId,
    userName,
    userAvatar,
    userRole,

    // 方法
    initFromStorage,
    checkLoginStatus,
    wechatLogin,
    fetchUserInfo,
    updateUserInfo,
    logout,
    setToken,
    clearAll
  }
})
