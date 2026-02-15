/**
 * API相关类型定义
 */

/**
 * 请求配置扩展
 */
import { AxiosRequestConfig } from 'axios'

export interface RequestConfig extends AxiosRequestConfig {
  /** 是否显示加载动画 */
  loading?: boolean
  /** 是否显示成功消息 */
  successMessage?: boolean
  /** 是否显示错误消息 */
  errorMessage?: boolean
}

/**
 * 上传响应
 */
export interface UploadResponse {
  url: string
  name: string
  size: number
  type: string
}

/**
 * 文件上传参数
 */
export interface UploadParams {
  /** 文件 */
  file: File
  /** 上传路径 */
  path?: string
  /** 文件名 */
  name?: string
}

/**
 * 导出参数
 */
export interface ExportParams {
  /** 数据 */
  data: any[]
  /** 文件名 */
  filename: string
  /** 表头 */
  headers?: string[]
  /** 工作表名 */
  sheetName?: string
}

/**
 * 导入参数
 */
export interface ImportParams {
  /** 文件 */
  file: File
  /** 导入模板 */
  template?: string
  /** 额外参数 */
  params?: Record<string, any>
}

/**
 * 导入响应
 */
export interface ImportResponse {
  success: number
  failed: number
  errors?: Array<{
    row: number
    message: string
  }>
}

/**
 * 下载参数
 */
export interface DownloadParams {
  /** 下载URL */
  url: string
  /** 文件名 */
  filename: string
  /** 请求参数 */
  params?: Record<string, any>
}

/**
 * 图表数据
 */
export interface ChartData {
  labels: string[]
  datasets: Array<{
    label: string
    data: number[]
    backgroundColor?: string | string[]
    borderColor?: string | string[]
  }>
}

/**
 * 统计卡片数据
 */
export interface StatCardData {
  title: string
  value: number | string
  change?: number
  changeType?: 'increase' | 'decrease' | 'neutral'
  icon?: string
  color?: string
}

/**
 * 日历事件
 */
export interface CalendarEvent {
  id: number
  title: string
  start: string
  end?: string
  allDay?: boolean
  color?: string
  type?: string
  data?: any
}

/**
 * 表格列配置
 */
export interface TableColumn {
  prop?: string
  label: string
  width?: string | number
  minWidth?: string | number
  align?: 'left' | 'center' | 'right'
  fixed?: 'left' | 'right'
  sortable?: boolean | 'custom'
  filters?: Array<{
    text: string
    value: string
  }>
  formatter?: (row: any, column: any, cellValue: any, index: number) => string
}

/**
 * 表单配置
 */
export interface FormConfig {
  /** 表单字段 */
  fields: FormField[]
  /** 表单规则 */
  rules?: Record<string, any[]>
  /** 布局 */
  layout?: {
    gutter?: number
    span?: number
  }
}

/**
 * 表单字段
 */
export interface FormField {
  /** 字段名 */
  prop: string
  /** 标签 */
  label: string
  /** 组件类型 */
  type: 'input' | 'select' | 'radio' | 'checkbox' | 'date' | 'datetime' | 'textarea' | 'switch' | 'number' | 'upload' | 'cascader' | 'tree-select'
  /** 组件属性 */
  attrs?: Record<string, any>
  /** 选项数据 */
  options?: Array<{
    label: string
    value: any
  }>
  /** 占位符 */
  placeholder?: string
  /** 是否必填 */
  required?: boolean
}

/**
 * 弹窗配置
 */
export interface DialogConfig {
  /** 标题 */
  title: string
  /** 宽度 */
  width?: string | number
  /** 是否显示 */
  visible: boolean
  /** 是否可拖拽 */
  draggable?: boolean
  /** 是否全屏 */
  fullscreen?: boolean
  /** 底部 */
  footer?: boolean
}

/**
 * 消息配置
 */
export interface MessageConfig {
  /** 消息内容 */
  message: string
  /** 消息类型 */
  type?: 'success' | 'warning' | 'info' | 'error'
  /** 显示时间 */
  duration?: number
}

/**
 * 确认框配置
 */
export interface ConfirmConfig {
  /** 标题 */
  title: string
  /** 内容 */
  content: string
  /** 类型 */
  type?: 'warning' | 'info' | 'success' | 'error'
  /** 确认按钮文本 */
  confirmText?: string
  /** 取消按钮文本 */
  cancelText?: string
}

/**
 * 标签配置
 */
export interface TagConfig {
  /** 标签文本 */
  label: string
  /** 标签值 */
  value: number | string
  /** 颜色类型 */
  type?: 'success' | 'warning' | 'info' | 'danger' | ''
}

/**
 * 下拉菜单项
 */
export interface DropdownItem {
  /** 文本 */
  label: string
  /** 值 */
  value: any
  /** 图标 */
  icon?: string
  /** 是否禁用 */
  disabled?: boolean
  /** 是否分隔线 */
  divided?: boolean
}

/**
 * 面包屑项
 */
export interface BreadcrumbItem {
  /** 文本 */
  text: string
  /** 路由 */
  to?: string | Record<string, any>
}

/**
 * 侧边栏菜单项
 */
export interface SidebarItem {
  /** 标题 */
  title: string
  /** 图标 */
  icon?: string
  /** 路由路径 */
  path?: string
  /** 子菜单 */
  children?: SidebarItem[]
  /** 是否隐藏 */
  hidden?: boolean
  /** 权限标识 */
  permission?: string
}

/**
 * 顶部导航项
 */
export interface HeaderItem {
  /** 标题 */
  title: string
  /** 图标 */
  icon?: string
  /** 路由路径 */
  path?: string
  /** 点击事件 */
  click?: () => void
}
