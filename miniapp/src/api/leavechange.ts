/**
 * 调课相关API
 * 调课功能需要后端支持，此处为预留接口
 */
import { request } from './request'

/**
 * 调课状态枚举
 */
export enum LeaveChangeStatus {
  PENDING = 1,    // 待审核
  APPROVED = 2,   // 已通过
  REJECTED = 3,   // 已拒绝
  CANCELLED = 4   // 已取消
}

/**
 * 调课状态文本
 */
export const LeaveChangeStatusText: Record<LeaveChangeStatus, string> = {
  [LeaveChangeStatus.PENDING]: '待审核',
  [LeaveChangeStatus.APPROVED]: '已通过',
  [LeaveChangeStatus.REJECTED]: '已拒绝',
  [LeaveChangeStatus.CANCELLED]: '已取消'
}

/**
 * 调课记录
 */
export interface LeaveChange {
  id: number
  student_id: number
  original_schedule_id: number
  target_schedule_id: number | null
  target_date: string | null
  reason: string
  status: LeaveChangeStatus
  approver_id: number | null
  approved_at: string | null
  reject_reason: string | null
  created_at: string
  updated_at: string
  // 关联信息
  original_schedule?: Schedule
  target_schedule?: Schedule
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
 * 调课申请参数
 */
export interface LeaveChangeApplyParams {
  student_id: number
  original_schedule_id: number
  target_schedule_id?: number
  target_date?: string
  reason: string
}

/**
 * 调课列表查询参数
 */
export interface LeaveChangeListParams {
  skip?: number
  limit?: number
  student_id?: number
  status?: LeaveChangeStatus
  start_date?: string
  end_date?: string
}

/**
 * 调课统计
 */
export interface LeaveChangeStats {
  total: number
  pending: number
  approved: number
  rejected: number
}

/**
 * 调课API类
 */
export class LeaveChangeAPI {
  /**
   * 获取调课列表
   */
  static async list(params?: LeaveChangeListParams): Promise<LeaveChange[]> {
    return request.get<LeaveChange[]>('/leave-changes', params)
  }

  /**
   * 获取调课详情
   */
  static async getById(leaveChangeId: number): Promise<LeaveChange> {
    return request.get<LeaveChange>(`/leave-changes/${leaveChangeId}`)
  }

  /**
   * 申请调课
   */
  static async apply(data: LeaveChangeApplyParams): Promise<LeaveChange> {
    return request.post<LeaveChange>('/leave-changes', data)
  }

  /**
   * 取消调课
   */
  static async cancel(leaveChangeId: number): Promise<void> {
    return request.delete<void>(`/leave-changes/${leaveChangeId}`)
  }

  /**
   * 统计调课数量
   */
  static async count(params?: Partial<LeaveChangeListParams>): Promise<{ count: number }> {
    return request.get('/leave-changes/count', params)
  }

  /**
   * 获取待审核的调课列表
   */
  static async getPendingLeaveChanges(): Promise<LeaveChange[]> {
    return request.get<LeaveChange[]>('/leave-changes', {
      status: LeaveChangeStatus.PENDING
    })
  }

  /**
   * 获取已通过的调课列表
   */
  static async getApprovedLeaveChanges(): Promise<LeaveChange[]> {
    return request.get<LeaveChange[]>('/leave-changes', {
      status: LeaveChangeStatus.APPROVED
    })
  }

  /**
   * 获取我的调课列表
   */
  static async getMyLeaveChanges(params?: LeaveChangeListParams): Promise<LeaveChange[]> {
    return request.get<LeaveChange[]>('/leave-changes/my', params)
  }

  /**
   * 调课统计
   */
  static async getStats(studentId?: number): Promise<LeaveChangeStats> {
    const params = studentId ? { student_id: studentId } : {}

    // 由于后端暂无调课API，返回模拟数据
    return {
      total: 0,
      pending: 0,
      approved: 0,
      rejected: 0
    }
  }
}

export default LeaveChangeAPI
