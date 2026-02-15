/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/types/user'
import { weworkLogin, getCurrentUser, logout as logoutApi } from '@/api/auth'
import router from '@/router'

export const useUserStore = defineStore(
  'user',
  () => {
    // 状态
    const user = ref<UserInfo | null>(null)
    const token = ref<string | null>(localStorage.getItem('token'))
    const permissions = ref<string[]>([])

    // 计算属性
    const isLoggedIn = computed(() => !!token.value)
    const userName = computed(() => user.value?.name || '未知')
    const userAvatar = computed(() => user.value?.avatar || '')

    // 方法
    /**
     * 企业微信登录
     */
    async function login(code: string): Promise<void> {
      try {
        const response = await weworkLogin(code)
        token.value = response.access_token
        localStorage.setItem('token', response.access_token)

        // 获取用户信息
        await fetchUserInfo()

        // 跳转到首页
        router.push('/')
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    }

    /**
     * 获取用户信息
     */
    async function fetchUserInfo(): Promise<void> {
      try {
        const response = await getCurrentUser()
        user.value = response
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    /**
     * 登出
     */
    async function logout(): Promise<void> {
      try {
        await logoutApi()
      } catch (error) {
        console.error('登出接口调用失败:', error)
      } finally {
        // 清除状态
        token.value = null
        user.value = null
        permissions.value = []

        // 清除本地存储
        localStorage.removeItem('token')

        // 跳转到登录页
        router.push('/login')
      }
    }

    /**
     * 设置Token
     */
    function setToken(newToken: string): void {
      token.value = newToken
      localStorage.setItem('token', newToken)
    }

    /**
     * 清除Token
     */
    function clearToken(): void {
      token.value = null
      localStorage.removeItem('token')
    }

    /**
     * 初始化（应用启动时调用）
     */
    async function init(): Promise<void> {
      if (token.value) {
        await fetchUserInfo()
      }
    }

    return {
      // 状态
      user,
      token,
      permissions,
      // 计算属性
      isLoggedIn,
      userName,
      userAvatar,
      // 方法
      login,
      fetchUserInfo,
      logout,
      setToken,
      clearToken,
      init,
    }
  },
  {
    persist: {
      key: 'user',
      paths: ['token', 'permissions'],
    },
  }
)
