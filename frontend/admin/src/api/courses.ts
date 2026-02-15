/**
 * 课程相关API
 */
import { request } from './request'

/**
 * 课程状态枚举
 */
export enum CourseStatus {
  ON_SALE = 1, // 上架
  OFF_SALE = 2, // 下架
}

/**
 * 课程基础信息
 */
export interface Course {
  id: number
  name: string
  description?: string
  category?: string
  price: number
  duration: number // 课时时长（分钟）
  total_hours: number // 总课时数
  status: CourseStatus
  cover_image?: string
  created_at?: string
  updated_at?: string
}

/**
 * 课程创建参数
 */
export interface CourseCreateParams {
  name: string
  description?: string
  category?: string
  price: number
  duration: number
  total_hours: number
  cover_image?: string
}

/**
 * 课程更新参数
 */
export interface CourseUpdateParams extends Partial<CourseCreateParams> {
  status?: CourseStatus
}

/**
 * 课程列表查询参数
 */
export interface CourseListParams {
  skip?: number
  limit?: number
  category?: string
  status?: CourseStatus | null
  search?: string
}

/**
 * 课程列表响应
 */
export interface CourseListResponse {
  data: Course[]
  total: number
}

/**
 * 获取课程列表
 */
export function getCourses(params: CourseListParams): Promise<Course[]> {
  return request.get('/api/v1/courses', { params })
}

/**
 * 获取课程详情
 * @param id 课程ID
 */
export function getCourse(id: number): Promise<Course> {
  return request.get(`/api/v1/courses/${id}`)
}

/**
 * 创建课程
 * @param data 课程信息
 */
export function createCourse(data: CourseCreateParams): Promise<Course> {
  return request.post('/api/v1/courses', data)
}

/**
 * 更新课程
 * @param id 课程ID
 * @param data 课程信息
 */
export function updateCourse(id: number, data: CourseUpdateParams): Promise<Course> {
  return request.put(`/api/v1/courses/${id}`, data)
}

/**
 * 删除课程
 * @param id 课程ID
 */
export function deleteCourse(id: number): Promise<void> {
  return request.delete(`/api/v1/courses/${id}`)
}

/**
 * 切换课程状态
 * @param id 课程ID
 */
export function toggleCourseStatus(id: number): Promise<Course> {
  return request.patch(`/api/v1/courses/${id}/toggle-status`)
}

// ==================== 教室相关API ====================

/**
 * 教室状态枚举
 */
export enum ClassroomStatus {
  AVAILABLE = 1, // 可用
  MAINTENANCE = 2, // 维护中
}

/**
 * 教室信息
 */
export interface Classroom {
  id: number
  name: string
  capacity: number
  department_id?: number
  department_name?: string
  equipment?: string[]
  status: ClassroomStatus
}

/**
 * 教室创建参数
 */
export interface ClassroomCreateParams {
  name: string
  capacity: number
  department_id?: number
  equipment?: string[]
}

/**
 * 教室更新参数
 */
export interface ClassroomUpdateParams extends Partial<ClassroomCreateParams> {
  status?: ClassroomStatus
}

/**
 * 获取教室列表
 */
export function getClassrooms(params?: {
  skip?: number
  limit?: number
  department_id?: number
  status?: ClassroomStatus
}): Promise<Classroom[]> {
  return request.get('/api/v1/courses/classrooms', { params })
}

/**
 * 获取教室详情
 * @param id 教室ID
 */
export function getClassroom(id: number): Promise<Classroom> {
  return request.get(`/api/v1/courses/classrooms/${id}`)
}

/**
 * 创建教室
 * @param data 教室信息
 */
export function createClassroom(data: ClassroomCreateParams): Promise<Classroom> {
  return request.post('/api/v1/courses/classrooms', data)
}

/**
 * 更新教室
 * @param id 教室ID
 * @param data 教室信息
 */
export function updateClassroom(id: number, data: ClassroomUpdateParams): Promise<Classroom> {
  return request.put(`/api/v1/courses/classrooms/${id}`, data)
}

/**
 * 删除教室
 * @param id 教室ID
 */
export function deleteClassroom(id: number): Promise<void> {
  return request.delete(`/api/v1/courses/classrooms/${id}`)
}

// ==================== 校区相关API ====================

/**
 * 校区信息
 */
export interface Department {
  id: number
  name: string
  parent_id?: number
  manager_id?: number
  address?: string
  contact?: string
  status: number
}

/**
 * 获取校区列表
 */
export function getDepartments(params?: {
  skip?: number
  limit?: number
  status?: number
}): Promise<Department[]> {
  return request.get('/api/v1/courses/departments', { params })
}

/**
 * 获取校区详情
 * @param id 校区ID
 */
export function getDepartment(id: number): Promise<Department> {
  return request.get(`/api/v1/courses/departments/${id}`)
}

/**
 * 创建校区
 * @param data 校区信息
 */
export function createDepartment(data: Partial<Department>): Promise<Department> {
  return request.post('/api/v1/courses/departments', data)
}

/**
 * 更新校区
 * @param id 校区ID
 * @param data 校区信息
 */
export function updateDepartment(id: number, data: Partial<Department>): Promise<Department> {
  return request.put(`/api/v1/courses/departments/${id}`, data)
}

/**
 * 删除校区
 * @param id 校区ID
 */
export function deleteDepartment(id: number): Promise<void> {
  return request.delete(`/api/v1/courses/departments/${id}`)
}
