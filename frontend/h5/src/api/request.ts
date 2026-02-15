/**
 * Axios HTTP 请求封装
 */
import axios, { type AxiosRequestConfig, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const authStore = useAuthStore()

    // 添加 Token
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }

    // 添加语言
    config.headers['Accept-Language'] = 'zh-CN'

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { code, data, message } = response.data

    // 业务成功
    if (code === 0 || code === 200 || response.status === 200) {
      return response.data
    }

    // 业务失败
    return Promise.reject(new Error(message || '请求失败'))
  },
  async (error) => {
    const { response } = error

    // 处理 HTTP 错误
    if (response) {
      switch (response.status) {
        case 401:
          // Token 过期，尝试刷新
          const authStore = useAuthStore()
          if (authStore.refreshToken && !authStore.isRefreshing) {
            try {
              authStore.isRefreshing = true
              await authStore.refreshTokenAction()
              // 重新发送请求
              return request(error.config)
            } catch {
              // 刷新失败，清除 Token 并跳转登录
              authStore.logout()
              router.push('/login')
            } finally {
              authStore.isRefreshing = false
            }
          } else {
            authStore.logout()
            router.push('/login')
          }
          break
        case 403:
          return Promise.reject(new Error('没有权限访问'))
        case 404:
          return Promise.reject(new Error('请求的资源不存在'))
        case 500:
          return Promise.reject(new Error('服务器错误'))
        default:
          return Promise.reject(new Error(response.data?.message || '请求失败'))
      }
    }

    // 网络错误
    if (!window.navigator.onLine) {
      return Promise.reject(new Error('网络连接已断开'))
    }

    return Promise.reject(error)
  }
)

export default request
