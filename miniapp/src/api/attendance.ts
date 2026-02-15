/**
 * 考勤相关API
 */
import { request } from './request'

/**
 * 考勤状态枚举
 */
export enum AttendanceStatus {
  PRESENT = 1,   // 出勤
  LEAVE = 2,     // 请假
  ABSENT = 3,    // 缺勤
  LATE = 4       // 迟到
}

/**
 * 考勤状态文本映射
 */
export const AttendanceStatusText: Record<AttendanceStatus, string> = {
  [AttendanceStatus.PRESENT]: '出勤',
  [AttendanceStatus.LEAVE]: '请假',
  [AttendanceStatus.ABSENT]: '缺勤',
  [AttendanceStatus.LATE]: '迟到'
}

/**
 * 考勤状态颜色映射
 */
export const AttendanceStatusColor: Record<AttendanceStatus, string> = {
  [AttendanceStatus.PRESENT]: '#52c41a',
  [AttendanceStatus.LEAVE]: '#1890ff',
  [AttendanceStatus.ABSENT]: '#ff4d4f',
  [AttendanceStatus.LATE]: '#faad14'
}

/**
 * 考勤记录
 */
export interface Attendance {
  id: number
  schedule_id: number
  schedule?: {
    id: number
    course_name: string
    start_time: string
    end_time: string
    classroom_name: string
  }
  student_id: number
  contract_id: number | null
  status: AttendanceStatus
  check_time: string | null
  check_method: number
  hours_consumed: number
  notes: string | null
  created_by: number | null
  created_at: string
}

/**
 * 考勤创建参数
 */
export interface AttendanceCreateParams {
  schedule_id: number
  student_id: number
  contract_id?: number
  status: AttendanceStatus
  check_time?: string
  check_method?: number
  hours_consumed?: number
  notes?: string
}

/**
 * 考勤更新参数
 */
export interface AttendanceUpdateParams {
  schedule_id?: number
  student_id?: number
  status?: AttendanceStatus
  check_time?: string
  check_method?: number
  hours_consumed?: number
  notes?: string
}

/**
 * 考勤列表查询参数
 */
export interface AttendanceListParams {
  skip?: number
  limit?: number
  schedule_id?: number
  student_id?: number
  contract_id?: number
  status?: AttendanceStatus
  start_date?: string
  end_date?: string
}

/**
 * 考勤统计
 */
export interface AttendanceStatistics {
  total_count: number
  present_count: number
  leave_count: number
  absent_count: number
  late_count: number
  present_rate: number
  total_hours_consumed: number
}

/**
 * 考勤API类
 */
export class AttendanceAPI {
  /**
   * 获取考勤列表
   */
  static async list(params?: AttendanceListParams): Promise<Attendance[]> {
    return request.get<Attendance[]>('/attendances', params)
  }

  /**
   * 获取考勤详情
   */
  static async getById(attendanceId: number): Promise<Attendance> {
    return request.get<Attendance>(`/attendances/${attendanceId}`)
  }

  /**
   * 创建考勤记录
   */
  static async create(data: AttendanceCreateParams): Promise<Attendance> {
    return request.post<Attendance>('/attendances', data)
  }

  /**
   * 更新考勤记录
   */
  static async update(attendanceId: number, data: AttendanceUpdateParams): Promise<Attendance> {
    return request.put<Attendance>(`/attendances/${attendanceId}`, data)
  }

  /**
   * 删除考勤记录
   */
  static async delete(attendanceId: number): Promise<void> {
    return request.delete<void>(`/attendances/${attendanceId}`)
  }

  /**
   * 获取学员考勤统计
   */
  static async getStudentStatistics(studentId: number): Promise<AttendanceStatistics> {
    return request.get<AttendanceStatistics>(`/attendances/statistics/student/${studentId}`)
  }

  /**
   * 获取排课考勤统计
   */
  static async getScheduleStatistics(scheduleId: number): Promise<AttendanceStatistics> {
    return request.get<AttendanceStatistics>(`/attendances/statistics/schedule/${scheduleId}`)
  }

  /**
   * 获取课程考勤统计
   */
  static async getCourseStatistics(
    courseId: number,
    startDate?: string,
    endDate?: string
  ): Promise<AttendanceStatistics> {
    return request.get<AttendanceStatistics>(`/attendances/statistics/course/${courseId}`, {
      start_date: startDate,
      end_date: endDate
    })
  }

  /**
   * 获取我的考勤记录
   */
  static async getMyAttendances(params?: Partial<AttendanceListParams>): Promise<Attendance[]> {
    return this.list({
      ...params
      // student_id会自动从当前用户信息中获取
    })
  }

  /**
   * 统计考勤数量
   */
  static async count(params?: Partial<AttendanceListParams>): Promise<{ count: number }> {
    return request.get('/attendances/count', params)
  }
}

export default AttendanceAPI
