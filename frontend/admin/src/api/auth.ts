/**
 * 认证相关API
 */
import { request } from './request'

/**
 * 登录请求参数
 */
export interface LoginParams {
  code: string
}

/**
 * Token响应
 */
export interface TokenResponse {
  access_token: string
  token_type?: string
  expires_in?: number
}

/**
 * 用户信息响应
 */
export interface UserInfoResponse {
  id: number
  name: string
  avatar?: string
  role: string
  wework_id?: string
}

/**
 * 企业微信登录
 * @param code 企业微信授权码
 */
export function weworkLogin(code: string): Promise<TokenResponse> {
  return request.post('/api/v1/auth/wework', { code })
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser(): Promise<UserInfoResponse> {
  return request.get('/api/v1/auth/me')
}

/**
 * 刷新Token
 */
export function refreshToken(): Promise<TokenResponse> {
  return request.post('/api/v1/auth/refresh')
}

/**
 * 退出登录
 */
export function logout(): Promise<void> {
  return request.post('/api/v1/auth/logout')
}
