/**
 * 用户相关类型定义
 */

/**
 * 用户信息
 */
export interface UserInfo {
  id: number
  name: string
  avatar?: string
  role: string
  wework_id?: string
  phone?: string
  email?: string
  department?: string
}

/**
 * 登录参数
 */
export interface LoginParams {
  /** 企业微信授权码 */
  code: string
}

/**
 * Token信息
 */
export interface TokenInfo {
  access_token: string
  token_type?: string
  expires_in?: number
}

/**
 * 用户状态
 */
export interface UserState {
  /** 用户信息 */
  user: UserInfo | null
  /** Token */
  token: string | null
  /** 是否登录 */
  isLoggedIn: boolean
}

/**
 * 权限配置
 */
export interface Permission {
  /** 权限标识 */
  code: string
  /** 权限名称 */
  name: string
  /** 权限类型 */
  type: 'menu' | 'button' | 'api'
  /** 父级ID */
  parent_id?: number
  /** 路由路径 */
  path?: string
  /** 图标 */
  icon?: string
  /** 排序 */
  sort?: number
}

/**
 * 角色信息
 */
export interface Role {
  /** 角色ID */
  id: number
  /** 角色名称 */
  name: string
  /** 角色编码 */
  code: string
  /** 角色描述 */
  description?: string
  /** 权限列表 */
  permissions: Permission[]
}

/**
 * 路由信息（带权限）
 */
export interface RouteInfo {
  /** 路由路径 */
  path: string
  /** 路由名称 */
  name: string
  /** 组件路径 */
  component: string
  /** 重定向地址 */
  redirect?: string
  /** 路由元信息 */
  meta?: {
    title: string
    icon?: string
    hidden?: boolean
    roles?: string[]
    affix?: boolean
    breadcrumb?: boolean
  }
  /** 子路由 */
  children?: RouteInfo[]
}

/**
 * 快捷导航
 */
export interface QuickLink {
  /** 标题 */
  title: string
  /** 图标 */
  icon?: string
  /** 路由路径 */
  path: string
  /** 描述 */
  description?: string
}

/**
 * 最近操作
 */
export interface RecentAction {
  /** 操作类型 */
  type: string
  /** 操作标题 */
  title: string
  /** 操作时间 */
  time: string
  /** 相关数据 */
  data?: any
}
