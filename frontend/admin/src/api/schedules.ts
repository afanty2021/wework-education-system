/**
 * 排课相关API
 */
import { request } from './request'

/**
 * 排课状态枚举
 */
export enum ScheduleStatus {
  SCHEDULED = 1, // 已安排
  COMPLETED = 2, // 已上课
  CANCELLED = 3, // 已取消
  RESCHEDULED = 4, // 已调课
}

/**
 * 排课基础信息
 */
export interface Schedule {
  id: number
  course_id: number
  course_name?: string
  teacher_id: number
  teacher_name?: string
  classroom_id?: number
  classroom_name?: string
  department_id?: number
  department_name?: string
  scheduled_date: string // 日期
  start_time: string // 开始时间 HH:mm
  end_time: string // 结束时间 HH:mm
  duration: number // 课时时长（分钟）
  enrolled_count: number // 已报名人数
  capacity: number // 最大容量
  status: ScheduleStatus
  remark?: string
  created_at?: string
  updated_at?: string
}

/**
 * 排课创建参数
 */
export interface ScheduleCreateParams {
  course_id: number
  teacher_id: number
  classroom_id?: number
  department_id?: number
  scheduled_date: string
  start_time: string
  end_time: string
  capacity?: number
  remark?: string
}

/**
 * 排课更新参数
 */
export interface ScheduleUpdateParams {
  course_id?: number
  teacher_id?: number
  classroom_id?: number
  department_id?: number
  scheduled_date?: string
  start_time?: string
  end_time?: string
  capacity?: number
  status?: ScheduleStatus
  remark?: string
}

/**
 * 学员报名参数
 */
export interface ScheduleEnrollParams {
  student_ids: number[]
}

/**
 * 冲突检测参数
 */
export interface ScheduleConflictCheckParams {
  course_id?: number
  teacher_id: number
  classroom_id?: number
  department_id?: number
  scheduled_date: string
  start_time: string
  end_time: string
  exclude_schedule_id?: number
}

/**
 * 冲突检测结果
 */
export interface ScheduleConflictResponse {
  has_conflict: boolean
  conflicts: Array<{
    type: 'teacher' | 'classroom' | 'course'
    schedule_id: number
    message: string
  }>
}

/**
 * 排课列表查询参数
 */
export interface ScheduleListParams {
  skip?: number
  limit?: number
  course_id?: number
  teacher_id?: number
  classroom_id?: number
  department_id?: number
  status?: ScheduleStatus | null
}

/**
 * 获取排课列表
 */
export function getSchedules(params: ScheduleListParams): Promise<Schedule[]> {
  return request.get('/api/v1/schedules', { params })
}

/**
 * 获取排课详情
 * @param id 排课ID
 */
export function getSchedule(id: number): Promise<Schedule> {
  return request.get(`/api/v1/schedules/${id}`)
}

/**
 * 创建排课
 * @param data 排课信息
 */
export function createSchedule(data: ScheduleCreateParams): Promise<Schedule> {
  return request.post('/api/v1/schedules', data)
}

/**
 * 更新排课
 * @param id 排课ID
 * @param data 排课信息
 */
export function updateSchedule(id: number, data: ScheduleUpdateParams): Promise<Schedule> {
  return request.put(`/api/v1/schedules/${id}`, data)
}

/**
 * 删除排课
 * @param id 排课ID
 */
export function deleteSchedule(id: number): Promise<void> {
  return request.delete(`/api/v1/schedules/${id}`)
}

/**
 * 学员报名
 * @param id 排课ID
 * @param data 报名信息
 */
export function enrollStudent(id: number, data: ScheduleEnrollParams): Promise<Schedule> {
  return request.post(`/api/v1/schedules/${id}/enroll`, data)
}

/**
 * 取消报名
 * @param id 排课ID
 * @param student_id 学员ID
 * @param count 取消人数
 */
export function cancelEnrollment(
  id: number,
  student_id: number,
  count?: number
): Promise<Schedule> {
  return request.post(`/api/v1/schedules/${id}/cancel-enrollment`, null, {
    params: { student_id, count },
  })
}

/**
 * 取消排课
 * @param id 排课ID
 */
export function cancelSchedule(id: number): Promise<Schedule> {
  return request.post(`/api/v1/schedules/${id}/cancel`)
}

/**
 * 检测排课冲突
 * @param data 检测参数
 */
export function checkScheduleConflicts(data: ScheduleConflictCheckParams): Promise<ScheduleConflictResponse> {
  return request.post('/api/v1/schedules/conflicts/check', data)
}

/**
 * 创建循环排课
 */
export function createRecurringSchedules(
  data: ScheduleCreateParams,
  recurringType: 'weekly' | 'biweekly',
  recurringCount: number,
  intervalDays?: number
): Promise<Schedule[]> {
  return request.post('/api/v1/schedules/recurring', data, {
    params: { recurring_type: recurringType, recurring_count: recurringCount, interval_days: intervalDays },
  })
}

/**
 * 统计排课数量
 */
export function countSchedules(params?: {
  course_id?: number
  teacher_id?: number
  classroom_id?: number
  department_id?: number
  status?: ScheduleStatus
}): Promise<{ count: number }> {
  return request.get('/api/v1/schedules/stats/count', { params })
}
