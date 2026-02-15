/**
 * 通知相关API
 */
import { request } from './request'

/**
 * 通知类型枚举
 */
export enum NotificationType {
  CONTRACT_EXPIRY = 1, // 合同到期
  CLASS_REMINDER = 2, // 课程提醒
  PAYMENT_REMINDER = 3, // 缴费提醒
  ATTENDANCE_REMINDER = 4, // 考勤提醒
  SYSTEM = 5, // 系统通知
}

/**
 * 通知状态枚举
 */
export enum NotificationStatus {
  UNREAD = 1, // 未读
  READ = 2, // 已读
}

/**
 * 通知记录
 */
export interface Notification {
  id: number
  type: NotificationType
  title: string
  content: string
  related_id?: number // 相关业务ID
  related_type?: string // 相关业务类型
  status: NotificationStatus
  is_push: boolean // 是否已推送
  created_at?: string
  read_at?: string
}

/**
 * 通知创建参数
 */
export interface NotificationCreateParams {
  type: NotificationType
  title: string
  content: string
  related_id?: number
  related_type?: string
  user_ids?: number[] // 指定用户，不传则发送全部
}

/**
 * 通知列表查询参数
 */
export interface NotificationListParams {
  skip?: number
  limit?: number
  type?: NotificationType | null
  status?: NotificationStatus | null
  is_push?: boolean | null
}

/**
 * 获取通知列表
 */
export function getNotifications(params: NotificationListParams): Promise<Notification[]> {
  return request.get('/api/v1/notifications', { params })
}

/**
 * 获取通知详情
 * @param id 通知ID
 */
export function getNotification(id: number): Promise<Notification> {
  return request.get(`/api/v1/notifications/${id}`)
}

/**
 * 创建通知
 * @param data 通知信息
 */
export function createNotification(data: NotificationCreateParams): Promise<Notification> {
  return request.post('/api/v1/notifications', data)
}

/**
 * 删除通知
 * @param id 通知ID
 */
export function deleteNotification(id: number): Promise<void> {
  return request.delete(`/api/v1/notifications/${id}`)
}

/**
 * 标记通知已读
 * @param id 通知ID
 */
export function markAsRead(id: number): Promise<Notification> {
  return request.patch(`/api/v1/notifications/${id}/read`)
}

/**
 * 批量标记通知已读
 * @param ids 通知ID数组
 */
export function batchMarkAsRead(ids: number[]): Promise<void> {
  return request.post('/api/v1/notifications/read-batch', { ids })
}

/**
 * 标记全部通知已读
 */
export function markAllAsRead(): Promise<void> {
  return request.post('/api/v1/notifications/read-all')
}

/**
 * 获取未读通知数量
 */
export function getUnreadCount(): Promise<{ count: number }> {
  return request.get('/api/v1/notifications/unread-count')
}
