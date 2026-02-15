/**
 * 考勤相关 API
 */
import request from './request'
import { type AttendanceResponse, type AttendanceStatistics } from './types'

/**
 * 获取考勤列表
 */
export function getAttendances(params?: {
  skip?: number
  limit?: number
  schedule_id?: number
  student_id?: number
  contract_id?: number
  status?: number
}): Promise<AttendanceResponse[]> {
  return request.get('/attendance', { params })
}

/**
 * 获取考勤详情
 */
export function getAttendanceDetail(attendanceId: number): Promise<AttendanceResponse> {
  return request.get(`/attendance/${attendanceId}`)
}

/**
 * 获取排课的考勤记录
 */
export function getScheduleAttendances(scheduleId: number): Promise<AttendanceResponse[]> {
  return request.get(`/attendance/schedule/${scheduleId}`)
}

/**
 * 获取学员考勤记录
 */
export function getStudentAttendances(studentId: number, params?: {
  skip?: number
  limit?: number
}): Promise<AttendanceResponse[]> {
  return request.get(`/attendance/student/${studentId}`, { params })
}

/**
 * 创建考勤记录
 */
export function createAttendance(data: {
  schedule_id: number
  student_id: number
  contract_id?: number
  status: number
  check_method?: number
  hours_consumed?: number
  notes?: string
}): Promise<AttendanceResponse> {
  return request.post('/attendance', data)
}

/**
 * 批量创建考勤记录
 */
export function batchCreateAttendances(data: {
  attendances: Array<{
    schedule_id: number
    student_id: number
    contract_id?: number
    status: number
    check_method?: number
    hours_consumed?: number
    notes?: string
  }>
  auto_deduct_hours?: boolean
}): Promise<AttendanceResponse[]> {
  return request.post('/attendance/batch', data)
}

/**
 * 更新考勤记录
 */
export function updateAttendance(
  attendanceId: number,
  data: Partial<{
    status: number
    check_method: number
    hours_consumed: number
    notes: string
  }>
): Promise<AttendanceResponse> {
  return request.put(`/attendance/${attendanceId}`, data)
}

/**
 * 删除考勤记录
 */
export function deleteAttendance(attendanceId: number): Promise<void> {
  return request.delete(`/attendance/${attendanceId}`)
}

/**
 * 获取学员考勤统计
 */
export function getStudentAttendanceStatistics(studentId: number): Promise<AttendanceStatistics> {
  return request.get(`/attendance/statistics/student/${studentId}`)
}

/**
 * 获取排课考勤统计
 */
export function getScheduleAttendanceStatistics(scheduleId: number): Promise<AttendanceStatistics> {
  return request.get(`/attendance/statistics/schedule/${scheduleId}`)
}

/**
 * 获取课程考勤统计
 */
export function getCourseAttendanceStatistics(
  courseId: number,
  params?: { start_date?: string; end_date?: string }
): Promise<AttendanceStatistics> {
  return request.get(`/attendance/statistics/course/${courseId}`, { params })
}

/**
 * 考勤签到（快速签到）
 */
export function quickCheckIn(data: {
  schedule_id: number
  student_id: number
  check_method?: number
}): Promise<AttendanceResponse> {
  return request.post('/attendance/checkin', data)
}

/**
 * 批量签到
 */
export function batchCheckIn(data: {
  schedule_id: number
  student_ids: number[]
  check_method?: number
}): Promise<AttendanceResponse[]> {
  return request.post('/attendance/batch-checkin', data)
}
