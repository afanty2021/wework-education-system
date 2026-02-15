/**
 * 课表相关API
 */
import { request } from './request'

/**
 * 排课基础信息
 */
export interface Schedule {
  id: number
  course_id: number
  course_name?: string
  teacher_id: number
  teacher_name?: string
  classroom_id: number
  classroom_name?: string
  department_id: number | null
  department_name?: string
  start_time: string
  end_time: string
  week_day: number | null
  recurring_type: string | null
  recurring_id: string | null
  max_students: number
  enrolled_count: number
  notes: string | null
  status: number
  created_by: number | null
  created_at: string
}

/**
 * 课表创建参数
 */
export interface ScheduleCreateParams {
  course_id: number
  teacher_id: number
  classroom_id: number
  department_id?: number
  start_time: string
  end_time: string
  week_day?: number
  recurring_type?: string
  max_students?: number
  notes?: string
}

/**
 * 课表更新参数
 */
export interface ScheduleUpdateParams {
  course_id?: number
  teacher_id?: number
  classroom_id?: number
  department_id?: number
  start_time?: string
  end_time?: string
  week_day?: number
  status?: number
  notes?: string
}

/**
 * 课表列表查询参数
 */
export interface ScheduleListParams {
  skip?: number
  limit?: number
  course_id?: number
  teacher_id?: number
  classroom_id?: number
  department_id?: number
  status?: number
  start_date?: string
  end_date?: string
}

/**
 * 课表冲突检测参数
 */
export interface ScheduleConflictCheckParams {
  teacher_id: number
  classroom_id: number
  start_time: string
  end_time: string
  exclude_schedule_id?: number
}

/**
 * 课表冲突检测响应
 */
export interface ScheduleConflictResponse {
  has_conflict: boolean
  teacher_conflicts: number[]
  classroom_conflicts: number[]
  course_conflicts: number[]
}

/**
 * 课表API类
 */
export class ScheduleAPI {
  /**
   * 获取课表列表
   */
  static async list(params?: ScheduleListParams): Promise<Schedule[]> {
    return request.get<Schedule[]>('/schedules', params)
  }

  /**
   * 获取课表详情
   */
  static async getById(scheduleId: number): Promise<Schedule> {
    return request.get<Schedule>(`/schedules/${scheduleId}`)
  }

  /**
   * 创建课表
   */
  static async create(data: ScheduleCreateParams): Promise<Schedule> {
    return request.post<Schedule>('/schedules', data)
  }

  /**
   * 更新课表
   */
  static async update(scheduleId: number, data: ScheduleUpdateParams): Promise<Schedule> {
    return request.put<Schedule>(`/schedules/${scheduleId}`, data)
  }

  /**
   * 删除课表
   */
  static async delete(scheduleId: number): Promise<void> {
    return request.delete<void>(`/schedules/${scheduleId}`)
  }

  /**
   * 检测冲突
   */
  static async checkConflicts(params: ScheduleConflictCheckParams): Promise<ScheduleConflictResponse> {
    return request.post<ScheduleConflictResponse>('/schedules/conflicts/check', params)
  }

  /**
   * 获取今日课表
   */
  static async getTodaySchedules(): Promise<Schedule[]> {
    const today = new Date().toISOString().split('T')[0]
    return request.get<Schedule[]>('/schedules', {
      start_date: today,
      end_date: today
    })
  }

  /**
   * 获取本周课表
   */
  static async getWeekSchedules(weekStart?: string): Promise<Schedule[]> {
    return request.get<Schedule[]>('/schedules', {
      start_date: weekStart
    })
  }

  /**
   * 统计课表数量
   */
  static async count(params?: Partial<ScheduleListParams>): Promise<{ count: number }> {
    return request.get('/schedules/stats/count', params)
  }
}

export default ScheduleAPI
