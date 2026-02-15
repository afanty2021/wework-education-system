/**
 * 缴费相关API
 */
import { request } from './request'

/**
 * 缴费状态枚举
 */
export enum PaymentStatus {
  PENDING = 1,   // 待确认
  CONFIRMED = 2, // 已确认
  REFUNDED = 3   // 已退款
}

/**
 * 缴费状态文本
 */
export const PaymentStatusText: Record<PaymentStatus, string> = {
  [PaymentStatus.PENDING]: '待确认',
  [PaymentStatus.CONFIRMED]: '已确认',
  [PaymentStatus.REFUNDED]: '已退款'
}

/**
 * 缴费方式枚举
 */
export enum PaymentMethod {
  WECHAT = 1,   // 微信
  ALIPAY = 2,   // 支付宝
  CASH = 3,     // 现金
  BANK_CARD = 4, // 银行卡
  TRANSFER = 5  // 转账
}

/**
 * 缴费方式文本
 */
export const PaymentMethodText: Record<PaymentMethod, string> = {
  [PaymentMethod.WECHAT]: '微信支付',
  [PaymentMethod.ALIPAY]: '支付宝',
  [PaymentMethod.CASH]: '现金',
  [PaymentMethod.BANK_CARD]: '银行卡',
  [PaymentMethod.TRANSFER]: '转账'
}

/**
 * 缴费记录
 */
export interface Payment {
  id: number
  payment_no: string
  contract_id: number
  amount: string | number
  hours: string | number | null
  payment_method: PaymentMethod
  payment_channel: string | null
  transaction_id: string | null
  trade_no: string | null
  payment_time: string | null
  operator_id: number | null
  status: PaymentStatus
  remark: string | null
  created_at: string
  updated_at: string
  // 关联信息
  contract?: Contract
}

/**
 * 合同信息
 */
export interface Contract {
  id: number
  contract_no: string
  student_id: number
  course_id: number | null
  course_name?: string
  student_name?: string
  total_hours: number
  remaining_hours: number
  total_amount: string | number
  paid_amount: string | number
  start_date: string
  end_date: string
  status: number
}

/**
 * 缴费创建参数
 */
export interface PaymentCreateParams {
  contract_id: number
  amount: number
  hours?: number
  payment_method: PaymentMethod
  payment_channel?: string
  transaction_id?: string
  trade_no?: string
  remark?: string
}

/**
 * 缴费列表查询参数
 */
export interface PaymentListParams {
  skip?: number
  limit?: number
  contract_id?: number
  status?: PaymentStatus
  payment_method?: PaymentMethod
}

/**
 * 微信支付参数
 */
export interface WechatPayParams {
  payment_id: number
  openid: string
}

/**
 * 微信支付结果
 */
export interface WechatPayResult {
  order_id: string
  prepay_id: string
  pay_sign: string
  timestamp: string
  nonce_str: string
  sign_type?: string
}

/**
 * 缴费统计
 */
export interface PaymentStats {
  total_pending: number
  total_confirmed: number
  total_refunded: number
  total_amount: number
}

/**
 * 缴费API类
 */
export class PaymentAPI {
  /**
   * 获取缴费列表
   */
  static async list(params?: PaymentListParams): Promise<Payment[]> {
    return request.get<Payment[]>('/payments', params)
  }

  /**
   * 获取缴费详情
   */
  static async getById(paymentId: number): Promise<Payment> {
    return request.get<Payment>(`/payments/${paymentId}`)
  }

  /**
   * 根据缴费编号获取
   */
  static async getByNo(paymentNo: string): Promise<Payment> {
    return request.get<Payment>(`/payments/no/${paymentNo}`)
  }

  /**
   * 创建缴费
   */
  static async create(data: PaymentCreateParams): Promise<Payment> {
    return request.post<Payment>('/payments', data)
  }

  /**
   * 更新缴费
   */
  static async update(paymentId: number, data: Partial<PaymentCreateParams>): Promise<Payment> {
    return request.put<Payment>(`/payments/${paymentId}`, data)
  }

  /**
   * 删除缴费
   */
  static async delete(paymentId: number): Promise<void> {
    return request.delete<void>(`/payments/${paymentId}`)
  }

  /**
   * 确认缴费
   */
  static async confirm(paymentId: number, hours: number, remark?: string): Promise<Payment> {
    return request.post<Payment>(`/payments/${paymentId}/confirm`, { hours, remark })
  }

  /**
   * 退款
   */
  static async refund(paymentId: number, refundAmount: number, refundHours?: number, refundReason?: string): Promise<Payment> {
    return request.post<Payment>(`/payments/${paymentId}/refund`, {
      refund_amount: refundAmount,
      refund_hours: refundHours,
      refund_reason: refundReason
    })
  }

  /**
   * 统计缴费数量
   */
  static async count(params?: Partial<PaymentListParams>): Promise<{ count: number }> {
    return request.get('/payments/stats/count', params)
  }

  /**
   * 获取我的缴费列表
   */
  static async getMyPayments(params?: PaymentListParams): Promise<Payment[]> {
    return request.get<Payment[]>('/payments/my', params)
  }

  /**
   * 获取待缴费列表
   */
  static async getPendingPayments(): Promise<Payment[]> {
    return request.get<Payment[]>('/payments', { status: PaymentStatus.PENDING })
  }

  /**
   * 获取已缴费列表
   */
  static async getConfirmedPayments(): Promise<Payment[]> {
    return request.get<Payment[]>('/payments', { status: PaymentStatus.CONFIRMED })
  }

  /**
   * 微信支付
   */
  static async wechatPay(params: WechatPayParams): Promise<WechatPayResult> {
    return request.post<WechatPayResult>('/payment/wechat', params)
  }

  /**
   * 查询支付状态
   */
  static async checkPaymentStatus(paymentId: number): Promise<{ status: PaymentStatus }> {
    return request.get(`/payments/${paymentId}/status`)
  }
}

export default PaymentAPI
