/**
 * 课程相关 API
 */
import request from './request'

/**
 * 课程响应
 */
export interface CourseResponse {
  id: number
  name: string
  description?: string
  category?: string
  duration?: number
  price?: number
  max_students?: number
  is_active?: boolean
  created_at: string
  updated_at?: string
}

/**
 * 获取课程列表
 */
export function getCourses(params?: {
  skip?: number
  limit?: number
  category?: string
  is_active?: boolean
}): Promise<CourseResponse[]> {
  return request.get('/courses', { params })
}

/**
 * 获取课程详情
 */
export function getCourseDetail(courseId: number): Promise<CourseResponse> {
  return request.get(`/courses/${courseId}`)
}

/**
 * 创建课程
 */
export function createCourse(data: {
  name: string
  description?: string
  category?: string
  duration?: number
  price?: number
  max_students?: number
}): Promise<CourseResponse> {
  return request.post('/courses', data)
}

/**
 * 更新课程
 */
export function updateCourse(
  courseId: number,
  data: Partial<{
    name: string
    description: string
    category: string
    duration: number
    price: number
    max_students: number
    is_active: boolean
  }>
): Promise<CourseResponse> {
  return request.put(`/courses/${courseId}`, data)
}

/**
 * 删除课程
 */
export function deleteCourse(courseId: number): Promise<void> {
  return request.delete(`/courses/${courseId}`)
}

/**
 * 获取课程分类列表
 */
export function getCourseCategories(): Promise<string[]> {
  return request.get('/courses/categories')
}
