/**
 * 学员相关API
 */
import { request } from './request'

/**
 * 学员状态枚举
 */
export enum StudentStatus {
  POTENTIAL = 1, // 潜在
  ACTIVE = 2, // 在读
  LOST = 3, // 已流失
}

/**
 * 学员基础信息
 */
export interface Student {
  id: number
  name: string
  phone?: string
  email?: string
  wechat?: string
  guardian_name?: string
  guardian_phone?: string
  source?: string
  tags: string[]
  status: StudentStatus
  remark?: string
  avatar?: string
  created_at?: string
  updated_at?: string
}

/**
 * 学员创建参数
 */
export interface StudentCreateParams {
  name: string
  phone?: string
  email?: string
  wechat?: string
  guardian_name?: string
  guardian_phone?: string
  source?: string
  tags?: string[]
  remark?: string
  avatar?: string
}

/**
 * 学员更新参数
 */
export interface StudentUpdateParams extends Partial<StudentCreateParams> {
  status?: StudentStatus
}

/**
 * 学员列表查询参数
 */
export interface StudentListParams {
  skip?: number
  limit?: number
  status?: StudentStatus | null
  source?: string
  search?: string
}

/**
 * 标签创建参数
 */
export interface StudentTagParams {
  tag: string
}

/**
 * 获取学员列表
 */
export function getStudents(params: StudentListParams): Promise<Student[]> {
  return request.get('/api/v1/students', { params })
}

/**
 * 获取学员详情
 * @param id 学员ID
 */
export function getStudent(id: number): Promise<Student> {
  return request.get(`/api/v1/students/${id}`)
}

/**
 * 创建学员
 * @param data 学员信息
 */
export function createStudent(data: StudentCreateParams): Promise<Student> {
  return request.post('/api/v1/students', data)
}

/**
 * 更新学员
 * @param id 学员ID
 * @param data 学员信息
 */
export function updateStudent(id: number, data: StudentUpdateParams): Promise<Student> {
  return request.put(`/api/v1/students/${id}`, data)
}

/**
 * 删除学员
 * @param id 学员ID
 */
export function deleteStudent(id: number): Promise<void> {
  return request.delete(`/api/v1/students/${id}`)
}

/**
 * 更新学员状态
 * @param id 学员ID
 * @param status 新状态
 */
export function updateStudentStatus(id: number, status: StudentStatus): Promise<Student> {
  return request.patch(`/api/v1/students/${id}/status`, null, {
    params: { status },
  })
}

// ==================== 学员标签API ====================

/**
 * 为学员添加标签
 * @param id 学员ID
 * @param tag 标签
 */
export function addStudentTag(id: number, tag: string): Promise<Student> {
  return request.post(`/api/v1/students/${id}/tags`, { tag })
}

/**
 * 从学员移除标签
 * @param id 学员ID
 * @param tag 标签
 */
export function removeStudentTag(id: number, tag: string): Promise<Student> {
  return request.delete(`/api/v1/students/${id}/tags/${encodeURIComponent(tag)}`)
}

/**
 * 获取所有标签
 */
export function getAllTags(): Promise<string[]> {
  return request.get('/api/v1/students/tags/all')
}
