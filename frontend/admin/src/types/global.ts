/**
 * 全局类型定义
 */

/**
 * 分页响应
 */
export interface PageResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
}

/**
 * 通用响应
 */
export interface Response<T> {
  code: number
  message: string
  data: T
}

/**
 * 分页参数
 */
export interface PaginationParams {
  page?: number
  page_size?: number
}

/**
 * 列表查询参数
 */
export interface ListQueryParams extends PaginationParams {
  search?: string
  status?: number | null
}

/**
 * 选项类型
 */
export interface Option<T = number> {
  label: string
  value: T
}

/**
 * 树形节点
 */
export interface TreeNode {
  id: number
  label: string
  children?: TreeNode[]
}

/**
 * 基础实体
 */
export interface BaseEntity {
  id: number
  created_at?: string
  updated_at?: string
}

/**
 * 带状态的实体
 */
export interface StatusEntity extends BaseEntity {
  status: number
}

/**
 * 金额类型
 */
export type Money = number | string

/**
 * 日期时间类型
 */
export type DateTime = string

/**
 * 枚举转选项
 */
export function enumToOptions<T extends number>(
  enumObj: { [key: number]: string },
  exclude?: T[]
): Option<T>[] {
  const options: Option<T>[] = []

  for (const [value, label] of Object.entries(enumObj)) {
    if (typeof value === 'string') continue
    const numValue = Number(value)
    if (exclude?.includes(numValue)) continue
    options.push({
      label: label as string,
      value: numValue as T,
    })
  }

  return options
}
