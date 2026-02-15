/**
 * 缴费相关API
 */
import { request } from './request'

/**
 * 缴费状态枚举
 */
export enum PaymentStatus {
  PENDING = 1, // 待确认
  CONFIRMED = 2, // 已确认
  REFUNDED = 3, // 已退款
}

/**
 * 支付方式枚举
 */
export enum PaymentMethod {
  WECHAT = 1, // 微信
  ALIPAY = 2, // 支付宝
  CASH = 3, // 现金
  BANK_CARD = 4, // 银行卡
  TRANSFER = 5, // 转账
}

/**
 * 缴费基础信息
 */
export interface Payment {
  id: number
  payment_no: string
  contract_id: number
  contract_no?: string
  student_id?: number
  student_name?: string
  amount: number
  actual_amount: number // 实际收款金额
  payment_method: PaymentMethod
  status: PaymentStatus
  remark?: string
  confirmed_by?: string
  confirmed_at?: string
  refund_amount?: number
  refund_reason?: string
  created_at?: string
  updated_at?: string
}

/**
 * 缴费创建参数
 */
export interface PaymentCreateParams {
  payment_no: string
  contract_id: number
  amount: number
  payment_method: PaymentMethod
  remark?: string
}

/**
 * 缴费更新参数
 */
export interface PaymentUpdateParams {
  payment_method?: PaymentMethod
  remark?: string
}

/**
 * 缴费确认参数
 */
export interface PaymentConfirmParams {
  actual_amount: number
  remark?: string
}

/**
 * 退款参数
 */
export interface PaymentRefundParams {
  refund_amount: number
  refund_reason?: string
}

/**
 * 缴费列表查询参数
 */
export interface PaymentListParams {
  skip?: number
  limit?: number
  contract_id?: number
  status?: PaymentStatus | null
  payment_method?: PaymentMethod | null
}

/**
 * 获取缴费列表
 */
export function getPayments(params: PaymentListParams): Promise<Payment[]> {
  return request.get('/api/v1/payments', { params })
}

/**
 * 获取缴费详情
 * @param id 缴费ID
 */
export function getPayment(id: number): Promise<Payment> {
  return request.get(`/api/v1/payments/${id}`)
}

/**
 * 根据缴费编号获取缴费
 * @param no 缴费编号
 */
export function getPaymentByNo(no: string): Promise<Payment> {
  return request.get(`/api/v1/payments/no/${no}`)
}

/**
 * 创建缴费
 * @param data 缴费信息
 */
export function createPayment(data: PaymentCreateParams): Promise<Payment> {
  return request.post('/api/v1/payments', data)
}

/**
 * 更新缴费
 * @param id 缴费ID
 * @param data 缴费信息
 */
export function updatePayment(id: number, data: PaymentUpdateParams): Promise<Payment> {
  return request.put(`/api/v1/payments/${id}`, data)
}

/**
 * 删除缴费
 * @param id 缴费ID
 */
export function deletePayment(id: number): Promise<void> {
  return request.delete(`/api/v1/payments/${id}`)
}

/**
 * 确认缴费
 * @param id 缴费ID
 * @param data 确认信息
 */
export function confirmPayment(id: number, data: PaymentConfirmParams): Promise<Payment> {
  return request.post(`/api/v1/payments/${id}/confirm`, data)
}

/**
 * 退款
 * @param id 缴费ID
 * @param data 退款信息
 */
export function refundPayment(id: number, data: PaymentRefundParams): Promise<Payment> {
  return request.post(`/api/v1/payments/${id}/refund`, data)
}

/**
 * 统计缴费数量
 */
export function countPayments(params?: {
  contract_id?: number
  status?: PaymentStatus
  payment_method?: PaymentMethod
}): Promise<{ count: number }> {
  return request.get('/api/v1/payments/stats/count', { params })
}
