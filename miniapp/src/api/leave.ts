/**
 * 请假相关API
 * 使用attendance API，status=2表示请假
 */
import { request } from './request'

/**
 * 考勤状态枚举
 */
export enum AttendanceStatus {
  PRESENT = 1,  // 出勤
  LEAVE = 2,   // 请假
  ABSENT = 3,   // 缺勤
  LATE = 4      // 迟到
}

/**
 * 考勤状态文本
 */
export const AttendanceStatusText: Record<AttendanceStatus, string> = {
  [AttendanceStatus.PRESENT]: '出勤',
  [AttendanceStatus.LEAVE]: '请假',
  [AttendanceStatus.ABSENT]: '缺勤',
  [AttendanceStatus.LATE]: '迟到'
}

/**
 * 请假申请状态
 */
export enum LeaveStatus {
  PENDING = 1,    // 待审核
  APPROVED = 2,    // 已通过
  REJECTED = 3,   // 已拒绝
  CANCELLED = 4   // 已取消
}

/**
 * 请假状态文本
 */
export const LeaveStatusText: Record<LeaveStatus, string> = {
  [LeaveStatus.PENDING]: '待审核',
  [LeaveStatus.APPROVED]: '已通过',
  [LeaveStatus.REJECTED]: '已拒绝',
  [LeaveStatus.CANCELLED]: '已取消'
}

/**
 * 考勤记录（用于请假）
 */
export interface Attendance {
  id: number
  schedule_id: number
  student_id: number
  contract_id: number | null
  status: AttendanceStatus
  check_time: string | null
  check_method: number
  hours_consumed: number
  notes: string | null
  created_by: number | null
  created_at: string
  // 关联信息
  schedule?: Schedule
  student?: Student
}

/**
 * 排课信息
 */
export interface Schedule {
  id: number
  course_id: number
  course_name?: string
  teacher_id: number
  teacher_name?: string
  classroom_id: number
  classroom_name?: string
  start_time: string
  end_time: string
  week_day: number | null
}

/**
 * 学员信息
 */
export interface Student {
  id: number
  name: string
  phone: string | null
  avatar?: string | null
}

/**
 * 请假申请参数
 */
export interface LeaveApplyParams {
  schedule_id: number
  student_id: number
  leave_date: string
  reason: string
  hours?: number
}

/**
 * 请假列表查询参数
 */
export interface LeaveListParams {
  skip?: number
  limit?: number
  student_id?: number
  schedule_id?: number
  status?: AttendanceStatus
  start_date?: string
  end_date?: string
}

/**
 * 请假统计
 */
export interface LeaveStats {
  total: number
  pending: number
  approved: number
  rejected: number
}

/**
 * 请假API类
 */
export class LeaveAPI {
  /**
   * 获取请假列表
   * 使用attendance API，筛选status=2（请假）
   */
  static async list(params?: LeaveListParams): Promise<Attendance[]> {
    return request.get<Attendance[]>('/attendances', {
      ...params,
      status: AttendanceStatus.LEAVE
    })
  }

  /**
   * 获取我的请假列表
   */
  static async getMyLeaves(params?: LeaveListParams): Promise<Attendance[]> {
    return request.get<Attendance[]>('/attendances/my', {
      ...params,
      status: AttendanceStatus.LEAVE
    })
  }

  /**
   * 获取请假详情
   */
  static async getById(attendanceId: number): Promise<Attendance> {
    return request.get<Attendance>(`/attendances/${attendanceId}`)
  }

  /**
   * 申请请假
   */
  static async apply(data: LeaveApplyParams): Promise<Attendance> {
    return request.post<Attendance>('/attendances', {
      schedule_id: data.schedule_id,
      student_id: data.student_id,
      status: AttendanceStatus.LEAVE,
      check_time: data.leave_date,
      hours_consumed: data.hours || 1,
      notes: data.reason
    })
  }

  /**
   * 取消请假
   */
  static async cancel(attendanceId: number): Promise<Attendance> {
    return request.delete<Attendance>(`/attendances/${attendanceId}`)
  }

  /**
   * 统计请假数量
   */
  static async count(params?: Partial<LeaveListParams>): Promise<{ count: number }> {
    return request.get('/attendances/count', {
      ...params,
      status: AttendanceStatus.LEAVE
    })
  }

  /**
   * 获取待审核的请假列表
   */
  static async getPendingLeaves(): Promise<Attendance[]> {
    return request.get<Attendance[]>('/attendances', {
      status: AttendanceStatus.LEAVE
    })
  }

  /**
   * 获取已通过的请假列表
   */
  static async getApprovedLeaves(): Promise<Attendance[]> {
    return request.get<Attendance[]>('/attendances', {
      status: AttendanceStatus.LEAVE
    })
  }

  /**
   * 请假统计
   */
  static async getStats(studentId?: number): Promise<LeaveStats> {
    const params = studentId ? { student_id: studentId } : {}

    // 获取所有请假记录统计
    const allLeaves = await request.get<Attendance[]>('/attendances', {
      ...params,
      status: AttendanceStatus.LEAVE
    })

    return {
      total: allLeaves.length,
      pending: allLeaves.filter(l => l.status === AttendanceStatus.LEAVE && !l.check_time).length,
      approved: allLeaves.filter(l => l.check_time).length,
      rejected: 0
    }
  }
}

export default LeaveAPI
