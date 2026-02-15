/**
 * 作业相关API
 */
import { request } from './request'

/**
 * 作业提交状态
 */
export enum HomeworkSubmitStatus {
  NOT_SUBMITTED = 0,  // 未提交
  SUBMITTED = 1,      // 已提交
  GRADED = 2         // 已批改
}

/**
 * 作业提交状态文本
 */
export const HomeworkSubmitStatusText: Record<HomeworkSubmitStatus, string> = {
  [HomeworkSubmitStatus.NOT_SUBMITTED]: '未提交',
  [HomeworkSubmitStatus.SUBMITTED]: '已提交',
  [HomeworkSubmitStatus.GRADED]: '已批改'
}

/**
 * 作业基础信息
 */
export interface Homework {
  id: number
  course_id: number
  course_name?: string
  title: string
  content: string
  due_date: string | null
  max_score: number
  is_active: boolean
  created_at: string
  updated_at: string | null
  // 以下字段可能在详情中返回
  submission?: HomeworkSubmission
}

/**
 * 作业创建参数
 */
export interface HomeworkCreateParams {
  course_id: number
  title: string
  content: string
  due_date?: string
  max_score?: number
}

/**
 * 作业更新参数
 */
export interface HomeworkUpdateParams {
  title?: string
  content?: string
  due_date?: string
  max_score?: number
  is_active?: boolean
}

/**
 * 作业列表查询参数
 */
export interface HomeworkListParams {
  skip?: number
  limit?: number
  course_id?: number
  is_active?: boolean
}

/**
 * 作业提交记录
 */
export interface HomeworkSubmission {
  id: number
  homework_id: number
  student_id: number
  content: string
  attachments: string[] | null
  score: number | null
  teacher_remark: string | null
  submitted_at: string
}

/**
 * 作业提交创建参数
 */
export interface HomeworkSubmissionCreateParams {
  homework_id: number
  content: string
  attachments?: string[]
}

/**
 * 作业API类
 */
export class HomeworkAPI {
  /**
   * 获取作业列表
   */
  static async list(params?: HomeworkListParams): Promise<Homework[]> {
    return request.get<Homework[]>('/homeworks', params)
  }

  /**
   * 获取作业详情
   */
  static async getById(homeworkId: number): Promise<Homework> {
    return request.get<Homework>(`/homeworks/${homeworkId}`)
  }

  /**
   * 创建作业
   */
  static async create(data: HomeworkCreateParams): Promise<Homework> {
    return request.post<Homework>('/homeworks', data)
  }

  /**
   * 更新作业
   */
  static async update(homeworkId: number, data: HomeworkUpdateParams): Promise<Homework> {
    return request.put<Homework>(`/homeworks/${homeworkId}`, data)
  }

  /**
   * 删除作业
   */
  static async delete(homeworkId: number): Promise<void> {
    return request.delete<void>(`/homeworks/${homeworkId}`)
  }

  /**
   * 提交作业
   */
  static async submit(homeworkId: number, data: HomeworkSubmissionCreateParams): Promise<HomeworkSubmission> {
    return request.post<HomeworkSubmission>(`/homeworks/${homeworkId}/submit`, data)
  }

  /**
   * 获取我的作业列表
   */
  static async getMyHomeworks(params?: Partial<HomeworkListParams>): Promise<Homework[]> {
    return this.list(params)
  }

  /**
   * 获取待完成作业
   */
  static async getPendingHomeworks(): Promise<Homework[]> {
    return request.get<Homework[]>('/homeworks', {
      is_active: true
      // 需要后端支持按提交状态筛选
    })
  }

  /**
   * 获取已过期作业
   */
  static async getExpiredHomeworks(): Promise<Homework[]> {
    return request.get<Homework[]>('/homeworks', {
      is_active: true
      // 需要后端支持按截止日期筛选
    })
  }
}

export default HomeworkAPI
