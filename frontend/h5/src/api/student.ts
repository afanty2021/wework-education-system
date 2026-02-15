/**
 * 学员相关 API
 */
import request from './request'

/**
 * 学员响应
 */
export interface StudentResponse {
  id: number
  name: string
  phone?: string
  parent_phone?: string
  age?: number
  gender?: number
  address?: string
  guardian_name?: string
  notes?: string
  is_active?: boolean
  created_at: string
  updated_at?: string
}

/**
 * 获取学员列表
 */
export function getStudents(params?: {
  skip?: number
  limit?: number
  name?: string
  phone?: string
  is_active?: boolean
}): Promise<StudentResponse[]> {
  return request.get('/students', { params })
}

/**
 * 获取学员详情
 */
export function getStudentDetail(studentId: number): Promise<StudentResponse> {
  return request.get(`/students/${studentId}`)
}

/**
 * 创建学员
 */
export function createStudent(data: {
  name: string
  phone?: string
  parent_phone?: string
  age?: number
  gender?: number
  address?: string
  guardian_name?: string
  notes?: string
}): Promise<StudentResponse> {
  return request.post('/students', data)
}

/**
 * 更新学员
 */
export function updateStudent(
  studentId: number,
  data: Partial<{
    name: string
    phone: string
    parent_phone: string
    age: number
    gender: number
    address: string
    guardian_name: string
    notes: string
    is_active: boolean
  }>
): Promise<StudentResponse> {
  return request.put(`/students/${studentId}`, data)
}

/**
 * 删除学员
 */
export function deleteStudent(studentId: number): Promise<void> {
  return request.delete(`/students/${studentId}`)
}

/**
 * 获取学员的合同列表
 */
export function getStudentContracts(studentId: number): Promise<Array<{
  id: number
  contract_no: string
  course_name: string
  total_hours: number
  remaining_hours: number
  status: number
  start_date: string
  end_date: string
}>> {
  return request.get(`/students/${studentId}/contracts`)
}

/**
 * 获取学员的考勤记录
 */
export function getStudentAttendanceRecords(studentId: number, params?: {
  skip?: number
  limit?: number
  start_date?: string
  end_date?: string
}): Promise<Array<{
  id: number
  schedule_name: string
  status: number
  check_time?: string
  hours_consumed: number
}>> {
  return request.get(`/students/${studentId}/attendance`, { params })
}
