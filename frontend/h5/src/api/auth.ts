/**
 * 认证相关 API
 */
import request from './request'

/**
 * 登录请求参数
 */
export interface LoginParams {
  /** 用户名 */
  username: string
  /** 密码 */
  password: string
}

/**
 * 企业微信登录请求参数
 */
export interface WeWorkLoginParams {
  /** 企业微信授权码 */
  code: string
}

/**
 * Token 响应
 */
export interface TokenResponse {
  /** 访问令牌 */
  access_token: string
  /** 刷新令牌 */
  refresh_token?: string
  /** 令牌类型 */
  token_type?: string
  /** 过期时间（秒） */
  expires_in?: number
}

/**
 * 用户信息
 */
export interface UserInfo {
  /** 用户ID */
  id: number
  /** 用户名 */
  username: string
  /** 姓名 */
  name: string
  /** 头像 */
  avatar?: string
  /** 角色 */
  role: string
  /** 企业微信ID */
  wework_id?: string
  /** 邮箱 */
  email?: string
  /** 手机号 */
  phone?: string
}

/**
 * 用户登录
 * @param data 登录参数
 */
export function login(data: LoginParams): Promise<TokenResponse> {
  return request.post('/auth/login', data)
}

/**
 * 企业微信登录
 * @param data 企业微信授权码
 */
export function weworkLogin(data: WeWorkLoginParams): Promise<TokenResponse> {
  return request.post('/auth/wework', data)
}

/**
 * 获取当前用户信息
 */
export function getUserInfo(): Promise<UserInfo> {
  return request.get('/auth/me')
}

/**
 * 刷新访问令牌
 */
export function refreshToken(): Promise<TokenResponse> {
  return request.post('/auth/refresh')
}

/**
 * 修改密码
 */
export function changePassword(data: { old_password: string; new_password: string }): Promise<void> {
  return request.post('/auth/change-password', data)
}

/**
 * 退出登录
 */
export function logout(): Promise<void> {
  return request.post('/auth/logout')
}
