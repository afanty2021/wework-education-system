/**
 * 认证相关API
 */
import { request } from './request'

/**
 * 微信小程序登录请求参数
 */
export interface WeChatLoginParams {
  code: string
  userInfo?: {
    nickName: string
    avatarUrl: string
    gender: number
    city: string
    province: string
    country: string
  }
}

/**
 * 登录响应数据
 */
export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
}

/**
 * 用户信息响应
 */
export interface UserInfoResponse {
  id: number
  name: string
  avatar: string | null
  role: string
  wework_id: string | null
  phone?: string
  student_id?: number
}

/**
 * 认证API类
 */
export class AuthAPI {
  /**
   * 微信登录
   */
  static async wechatLogin(params: WeChatLoginParams): Promise<LoginResponse> {
    return request.post<LoginResponse>('/auth/wechat-miniapp', params)
  }

  /**
   * 获取当前用户信息
   */
  static async getCurrentUser(): Promise<UserInfoResponse> {
    return request.get<UserInfoResponse>('/auth/me')
  }

  /**
   * 刷新Token
   */
  static async refreshToken(): Promise<LoginResponse> {
    return request.post<LoginResponse>('/auth/refresh')
  }

  /**
   * 退出登录
   */
  static async logout(): Promise<void> {
    return request.post<void>('/auth/logout')
  }
}

export default AuthAPI
