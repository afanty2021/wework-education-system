/**
 * 考勤相关API
 */
import { request } from './request'

/**
 * 考勤状态枚举
 */
export enum AttendanceStatus {
  PRESENT = 1, // 正常出勤
  ABSENT = 2, // 缺勤
  LATE = 3, // 迟到
  LEAVE = 4, // 请假
  MAKEUP = 5, // 补课
}

/**
 * 考勤记录
 */
export interface Attendance {
  id: number
  schedule_id: number
  student_id: number
  student_name?: string
  schedule_date: string
  status: AttendanceStatus
  check_in_time?: string // 签到时间
  check_out_time?: string // 签退时间
  duration?: number // 实际出勤时长（分钟）
  remark?: string
  created_at?: string
  updated_at?: string
}

/**
 * 考勤创建参数
 */
export interface AttendanceCreateParams {
  schedule_id: number
  student_id: number
  status: AttendanceStatus
  remark?: string
}

/**
 * 批量考勤参数
 */
export interface BatchAttendanceParams {
  schedule_id: number
  attendances: Array<{
    student_id: number
    status: AttendanceStatus
    remark?: string
  }>
}

/**
 * 考勤列表查询参数
 */
export interface AttendanceListParams {
  skip?: number
  limit?: number
  schedule_id?: number
  student_id?: number
  status?: AttendanceStatus | null
  start_date?: string
  end_date?: string
}

/**
 * 获取考勤列表
 */
export function getAttendances(params: AttendanceListParams): Promise<Attendance[]> {
  return request.get('/api/v1/attendance', { params })
}

/**
 * 获取考勤详情
 * @param id 考勤ID
 */
export function getAttendance(id: number): Promise<Attendance> {
  return request.get(`/api/v1/attendance/${id}`)
}

/**
 * 创建考勤记录
 * @param data 考勤信息
 */
export function createAttendance(data: AttendanceCreateParams): Promise<Attendance> {
  return request.post('/api/v1/attendance', data)
}

/**
 * 批量创建考勤记录
 * @param data 批量考勤信息
 */
export function batchCreateAttendance(data: BatchAttendanceParams): Promise<Attendance[]> {
  return request.post('/api/v1/attendance/batch', data)
}

/**
 * 更新考勤记录
 * @param id 考勤ID
 * @param data 考勤信息
 */
export function updateAttendance(id: number, data: Partial<AttendanceCreateParams>): Promise<Attendance> {
  return request.put(`/api/v1/attendance/${id}`, data)
}

/**
 * 删除考勤记录
 * @param id 考勤ID
 */
export function deleteAttendance(id: number): Promise<void> {
  return request.delete(`/api/v1/attendance/${id}`)
}

/**
 * 获取排课学员列表
 * @param schedule_id 排课ID
 */
export function getScheduleStudents(schedule_id: number): Promise<Array<{
  id: number
  name: string
  status: number
}>> {
  return request.get(`/api/v1/attendance/schedule/${schedule_id}/students`)
}

/**
 * 考勤统计
 */
export function getAttendanceStats(params?: {
  start_date?: string
  end_date?: string
  course_id?: number
  student_id?: number
}): Promise<{
  total: number
  present: number
  absent: number
  late: number
  leave: number
  makeup: number
  attendance_rate: number
}> {
  return request.get('/api/v1/attendance/stats', { params })
}
