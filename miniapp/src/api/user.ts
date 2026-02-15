/**
 * 用户相关API
 */
import { request } from './request'

/**
 * 学员信息
 */
export interface Student {
  id: number
  name: string
  avatar: string | null
  phone: string | null
  gender: number | null
  birth_date: string | null
  grade: string | null
  school: string | null
  parent_name: string | null
  parent_phone: string | null
  address: string | null
  notes: string | null
  created_at: string
  updated_at: string | null
}

/**
 * 合同信息
 */
export interface Contract {
  id: number
  student_id: number
  course_id: number
  course_name?: string
  contract_no: string
  total_hours: number
  remaining_hours: number
  unit_price: number
  total_amount: number
  discount_amount: number
  status: number
  start_date: string
  end_date: string
  created_at: string
  updated_at: string | null
}

/**
 * 合同状态枚举
 */
export enum ContractStatus {
  ACTIVE = 1,      // 生效
  COMPLETED = 2,   // 完结
  REFUNDED = 3,    // 退费
  EXPIRED = 4      // 过期
}

/**
 * 合同状态文本
 */
export const ContractStatusText: Record<ContractStatus, string> = {
  [ContractStatus.ACTIVE]: '生效中',
  [ContractStatus.COMPLETED]: '已完结',
  [ContractStatus.REFUNDED]: '已退费',
  [ContractStatus.EXPIRED]: '已过期'
}

/**
 * 用户API类
 */
export class UserAPI {
  /**
   * 获取学员信息
   */
  static async getStudentInfo(studentId: number): Promise<Student> {
    return request.get<Student>(`/students/${studentId}`)
  }

  /**
   * 更新学员信息
   */
  static async updateStudent(studentId: number, data: Partial<Student>): Promise<Student> {
    return request.put<Student>(`/students/${studentId}`, data)
  }

  /**
   * 获取学员合同列表
   */
  static async getContracts(studentId: number): Promise<Contract[]> {
    return request.get<Contract[]>(`/contracts`, {
      student_id: studentId
    })
  }

  /**
   * 获取合同详情
   */
  static async getContractDetail(contractId: number): Promise<Contract> {
    return request.get<Contract>(`/contracts/${contractId}`)
  }

  /**
   * 获取我的合同
   */
  static async getMyContracts(): Promise<Contract[]> {
    return request.get<Contract[]>('/contracts')
  }
}

export default UserAPI
