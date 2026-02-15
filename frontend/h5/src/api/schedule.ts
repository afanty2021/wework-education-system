/**
 * 课表相关 API
 */
import request from './request'
import { type ScheduleResponse } from './types'

/**
 * 获取课表列表
 * @param params 查询参数
 */
export function getSchedules(params?: {
  skip?: number
  limit?: number
  course_id?: number
  teacher_id?: number
  classroom_id?: number
  department_id?: number
  status?: number
}): Promise<ScheduleResponse[]> {
  return request.get('/schedules', { params })
}

/**
 * 获取今日课表
 */
export function getTodaySchedules(teacherId?: number): Promise<ScheduleResponse[]> {
  return request.get('/schedules/today', { params: { teacher_id: teacherId } })
}

/**
 * 获取指定日期的课表
 */
export function getSchedulesByDate(date: string, teacherId?: number): Promise<ScheduleResponse[]> {
  return request.get('/schedules/date', { params: { date, teacher_id: teacherId } })
}

/**
 * 获取周课表
 */
export function getWeekSchedules(date?: string, teacherId?: number): Promise<ScheduleResponse[]> {
  return request.get('/schedules/week', { params: { date, teacher_id: teacherId } })
}

/**
 * 获取课表详情
 */
export function getScheduleDetail(scheduleId: number): Promise<ScheduleResponse> {
  return request.get(`/schedules/${scheduleId}`)
}

/**
 * 获取课表学员名单
 */
export function getScheduleStudents(scheduleId: number): Promise<{
  students: Array<{
    id: number
    name: string
    phone?: string
    parent_phone?: string
  }>
}> {
  return request.get(`/schedules/${scheduleId}/students`)
}

/**
 * 创建课表
 */
export function createSchedule(data: {
  course_id: number
  teacher_id?: number
  classroom_id: number
  department_id?: number
  start_time: string
  end_time: string
  week_day?: number
  recurring_type?: string
  max_students?: number
  notes?: string
}): Promise<ScheduleResponse> {
  return request.post('/schedules', data)
}

/**
 * 更新课表
 */
export function updateSchedule(
  scheduleId: number,
  data: Partial<{
    course_id: number
    classroom_id: number
    start_time: string
    end_time: string
    status: number
    notes: string
  }>
): Promise<ScheduleResponse> {
  return request.put(`/schedules/${scheduleId}`, data)
}

/**
 * 取消课表
 */
export function cancelSchedule(scheduleId: number): Promise<ScheduleResponse> {
  return request.post(`/schedules/${scheduleId}/cancel`)
}

/**
 * 删除课表
 */
export function deleteSchedule(scheduleId: number): Promise<void> {
  return request.delete(`/schedules/${scheduleId}`)
}

/**
 * 检测课表冲突
 */
export function checkScheduleConflicts(data: {
  teacher_id: number
  classroom_id: number
  start_time: string
  end_time: string
  exclude_schedule_id?: number
}): Promise<{
  has_conflict: boolean
  teacher_conflicts: number[]
  classroom_conflicts: number[]
  course_conflicts: number[]
}> {
  return request.post('/schedules/conflicts/check', data)
}
