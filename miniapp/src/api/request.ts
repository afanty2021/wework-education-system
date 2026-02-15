/**
 * API请求封装
 * 统一的请求处理模块
 */
import { useUserStore } from '@/stores/user'

// 环境变量
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

/**
 * 请求配置接口
 */
interface RequestConfig {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  data?: Record<string, unknown>
  params?: Record<string, unknown>
  headers?: Record<string, string>
  timeout?: number
}

/**
 * 请求响应接口
 */
interface RequestResponse<T = unknown> {
  data: T
  code: number
  message: string
}

/**
 * 分页数据接口
 */
interface PageData<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

/**
 * 网络请求类
 */
class Request {
  private baseUrl: string
  private defaultTimeout: number = 15000

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  /**
   * 发起请求
   */
  async request<T>(config: RequestConfig): Promise<T> {
    const { url, method = 'GET', data, params, headers = {} } = config

    // 获取Token
    const userStore = useUserStore()
    const token = userStore.token

    // 设置默认请求头
    const defaultHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    // 添加认证Token
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`
    }

    // 合并请求头
    const requestHeaders = { ...defaultHeaders, ...headers }

    // 构建请求参数
    const requestParams: UniApp.RequestOptions = {
      url: this.baseUrl + url,
      method,
      header: requestHeaders,
      timeout: config.timeout || this.defaultTimeout,
      success: (res: UniApp.RequestSuccess) => {
        this.handleSuccess<T>(res)
      },
      fail: (err: UniApp.RequestFail) => {
        this.handleError(err)
      }
    }

    // 处理参数
    if (method === 'GET') {
      requestParams.data = params || data
    } else {
      requestParams.data = data
    }

    // 发起请求
    return new Promise<T>((resolve, reject) => {
      uni.request({
        ...requestParams,
        success: (res) => {
          const result = this.handleResponse<T>(res)
          if (result.code === 200 || result.code === 0) {
            resolve(result.data as T)
          } else {
            reject(new Error(result.message || '请求失败'))
          }
        },
        fail: (err) => {
          reject(this.handleError(err))
        }
      })
    })
  }

  /**
   * 处理成功响应
   */
  private handleSuccess<T>(res: UniApp.RequestSuccess): T {
    return res.data as T
  }

  /**
   * 处理错误响应
   */
  private handleError(err: UniApp.RequestFail): Error {
    console.error('请求错误:', err)

    if (err.errMsg.includes('timeout')) {
      return new Error('请求超时，请稍后重试')
    }

    if (err.errMsg.includes('network')) {
      return new Error('网络连接失败，请检查网络设置')
    }

    return new Error(err.errMsg || '请求失败')
  }

  /**
   * 处理响应数据
   */
  private handleResponse<T>(res: UniApp.RequestSuccess): RequestResponse<T> {
    // 微信小程序返回的数据结构
    if (typeof res.data === 'string') {
      try {
        return JSON.parse(res.data)
      } catch {
        return {
          data: res.data as unknown as T,
          code: 0,
          message: '请求成功'
        }
      }
    }

    return res.data as RequestResponse<T>
  }

  /**
   * GET请求
   */
  get<T>(url: string, params?: Record<string, unknown>, config?: Partial<RequestConfig>): Promise<T> {
    return this.request<T>({
      url,
      method: 'GET',
      params,
      ...config
    })
  }

  /**
   * POST请求
   */
  post<T>(url: string, data?: Record<string, unknown>, config?: Partial<RequestConfig>): Promise<T> {
    return this.request<T>({
      url,
      method: 'POST',
      data,
      ...config
    })
  }

  /**
   * PUT请求
   */
  put<T>(url: string, data?: Record<string, unknown>, config?: Partial<RequestConfig>): Promise<T> {
    return this.request<T>({
      url,
      method: 'PUT',
      data,
      ...config
    })
  }

  /**
   * DELETE请求
   */
  delete<T>(url: string, params?: Record<string, unknown>, config?: Partial<RequestConfig>): Promise<T> {
    return this.request<T>({
      url,
      method: 'DELETE',
      params,
      ...config
    })
  }
}

// 创建请求实例
export const request = new Request(API_BASE_URL)

// 导出Request类便于扩展
export { Request, API_BASE_URL }
