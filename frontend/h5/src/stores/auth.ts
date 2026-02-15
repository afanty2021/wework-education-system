/**
 * 认证状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { login as loginApi, weworkLogin, getUserInfo, refreshToken, logout as logoutApi, type TokenResponse, type UserInfo } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()

  // 状态
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshTokenValue = ref<string | null>(localStorage.getItem('refresh_token'))
  const userInfo = ref<UserInfo | null>(null)
  const isRefreshing = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const userId = computed(() => userInfo.value?.id)
  const userName = computed(() => userInfo.value?.name || userInfo.value?.username)
  const userRole = computed(() => userInfo.value?.role)

  // 保存 Token
  function saveToken(response: TokenResponse) {
    token.value = response.access_token
    if (response.refresh_token) {
      refreshTokenValue.value = response.refresh_token
      localStorage.setItem('refresh_token', response.refresh_token)
    }
    localStorage.setItem('access_token', response.access_token)
  }

  // 清除 Token
  function clearToken() {
    token.value = null
    refreshTokenValue.value = null
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  /**
   * 用户名密码登录
   */
  async function loginAction(params: { username: string; password: string }) {
    try {
      const response = await loginApi(params)
      saveToken(response)
      await fetchUserInfo()
      return { success: true }
    } catch (error) {
      return { success: false, error: (error as Error).message }
    }
  }

  /**
   * 企业微信登录
   */
  async function weworkLoginAction(code: string) {
    try {
      const response = await weworkLogin({ code })
      saveToken(response)
      await fetchUserInfo()
      return { success: true }
    } catch (error) {
      return { success: false, error: (error as Error).message }
    }
  }

  /**
   * 获取用户信息
   */
  async function fetchUserInfo() {
    try {
      const info = await getUserInfo()
      userInfo.value = info
      return info
    } catch (error) {
      clearToken()
      throw error
    }
  }

  /**
   * 刷新访问令牌
   */
  async function refreshTokenAction() {
    if (!refreshTokenValue.value) {
      throw new Error('No refresh token')
    }

    try {
      const response = await refreshToken()
      saveToken(response)
      return response
    } catch (error) {
      clearToken()
      throw error
    }
  }

  /**
   * 初始化认证状态
   */
  async function initAuth() {
    if (token.value) {
      try {
        await fetchUserInfo()
      } catch {
        clearToken()
      }
    }
  }

  /**
   * 退出登录
   */
  async function logout() {
    try {
      await logoutApi()
    } finally {
      clearToken()
      router.push('/login')
    }
  }

  return {
    // 状态
    token,
    refreshTokenValue,
    userInfo,
    isRefreshing,
    // 计算属性
    isLoggedIn,
    userId,
    userName,
    userRole,
    // 方法
    loginAction,
    weworkLoginAction,
    fetchUserInfo,
    refreshTokenAction,
    initAuth,
    logout,
    clearToken,
  }
})
