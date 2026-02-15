/**
 * 合同相关API
 */
import { request } from './request'

/**
 * 合同状态枚举
 */
export enum ContractStatus {
  ACTIVE = 1, // 生效
  COMPLETED = 2, // 完结
  REFUNDED = 3, // 退费
  EXPIRED = 4, // 过期
}

/**
 * 合同基础信息
 */
export interface Contract {
  id: number
  contract_no: string
  student_id: number
  student_name?: string
  course_id?: number
  course_name?: string
  total_hours: number // 总课时
  remaining_hours: number // 剩余课时
  unit_price: number // 单价
  total_amount: number // 总金额
  discount_amount: number // 折扣金额
  status: ContractStatus
  start_date?: string
  end_date?: string
  remark?: string
  created_at?: string
  updated_at?: string
}

/**
 * 合同创建参数
 */
export interface ContractCreateParams {
  contract_no: string
  student_id: number
  course_id?: number
  total_hours: number
  unit_price: number
  discount_amount?: number
  start_date?: string
  end_date?: string
  remark?: string
}

/**
 * 合同更新参数
 */
export interface ContractUpdateParams {
  course_id?: number
  total_hours?: number
  unit_price?: number
  discount_amount?: number
  status?: ContractStatus
  start_date?: string
  end_date?: string
  remark?: string
}

/**
 * 课时扣减参数
 */
export interface ContractDeductHoursParams {
  hours: number
  reason?: string
}

/**
 * 课时追加参数
 */
export interface ContractAddHoursParams {
  hours: number
  reason?: string
}

/**
 * 合同列表查询参数
 */
export interface ContractListParams {
  skip?: number
  limit?: number
  student_id?: number
  course_id?: number
  status?: ContractStatus | null
}

/**
 * 获取合同列表
 */
export function getContracts(params: ContractListParams): Promise<Contract[]> {
  return request.get('/api/v1/contracts', { params })
}

/**
 * 获取即将到期的合同
 */
export function getExpiringContracts(params?: {
  days?: number
  skip?: number
  limit?: number
}): Promise<Contract[]> {
  return request.get('/api/v1/contracts/expiring', { params })
}

/**
 * 获取合同详情
 * @param id 合同ID
 */
export function getContract(id: number): Promise<Contract> {
  return request.get(`/api/v1/contracts/${id}`)
}

/**
 * 根据合同编号获取合同
 * @param no 合同编号
 */
export function getContractByNo(no: string): Promise<Contract> {
  return request.get(`/api/v1/contracts/no/${no}`)
}

/**
 * 创建合同
 * @param data 合同信息
 */
export function createContract(data: ContractCreateParams): Promise<Contract> {
  return request.post('/api/v1/contracts', data)
}

/**
 * 更新合同
 * @param id 合同ID
 * @param data 合同信息
 */
export function updateContract(id: number, data: ContractUpdateParams): Promise<Contract> {
  return request.put(`/api/v1/contracts/${id}`, data)
}

/**
 * 删除合同
 * @param id 合同ID
 */
export function deleteContract(id: number): Promise<void> {
  return request.delete(`/api/v1/contracts/${id}`)
}

/**
 * 扣减课时
 * @param id 合同ID
 * @param data 扣减信息
 */
export function deductContractHours(id: number, data: ContractDeductHoursParams): Promise<Contract> {
  return request.post(`/api/v1/contracts/${id}/deduct`, data)
}

/**
 * 追加课时
 * @param id 合同ID
 * @param data 追加信息
 */
export function addContractHours(id: number, data: ContractAddHoursParams): Promise<Contract> {
  return request.post(`/api/v1/contracts/${id}/add-hours`, data)
}

/**
 * 标记合同过期
 * @param id 合同ID
 */
export function markContractExpired(id: number): Promise<Contract> {
  return request.post(`/api/v1/contracts/${id}/expire`)
}

/**
 * 统计合同数量
 */
export function countContracts(params?: {
  student_id?: number
  course_id?: number
  status?: ContractStatus
}): Promise<{ count: number }> {
  return request.get('/api/v1/contracts/stats/count', { params })
}
