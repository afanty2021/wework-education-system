/**
 * 通知相关 API
 */
import request from './request'
import { type NotificationResponse, type NotificationListResponse } from './types'

/**
 * 获取通知列表
 */
export function getNotifications(params?: {
  skip?: number
  limit?: number
  type?: number
  receiver_id?: string
  receiver_type?: number
  status?: number
}): Promise<NotificationListResponse> {
  return request.get('/notifications', { params })
}

/**
 * 获取接收者的通知列表
 */
export function getReceiverNotifications(
  receiverId: string,
  params?: {
    skip?: number
    limit?: number
    unread_only?: boolean
  }
): Promise<NotificationResponse[]> {
  return request.get(`/notifications/receiver/${receiverId}`, { params })
}

/**
 * 获取未读通知数量
 */
export function getUnreadCount(receiverId: string, receiverType?: number): Promise<{
  receiver_id: string
  unread_count: number
}> {
  return request.get('/notifications/unread/count', { params: { receiver_id: receiverId, receiver_type: receiverType } })
}

/**
 * 获取通知详情
 */
export function getNotificationDetail(notificationId: number): Promise<NotificationResponse> {
  return request.get(`/notifications/${notificationId}`)
}

/**
 * 标记通知为已读
 */
export function markNotificationsAsRead(data: {
  notification_ids: number[]
}): Promise<{ marked_count: number }> {
  return request.post('/notifications/mark-read', data)
}

/**
 * 标记单条通知为已读
 */
export function markNotificationAsRead(notificationId: number): Promise<void> {
  return request.post(`/notifications/${notificationId}/read`)
}

/**
 * 标记所有通知为已读
 */
export function markAllNotificationsAsRead(receiverId: string): Promise<{ marked_count: number }> {
  return request.post('/notifications/mark-all-read', { receiver_id: receiverId })
}

/**
 * 创建通知
 */
export function createNotification(data: {
  type: number
  receiver_id: string
  receiver_type?: number
  title: string
  content?: string
  url?: string
}): Promise<NotificationResponse> {
  return request.post('/notifications', data)
}

/**
 * 批量创建通知
 */
export function batchCreateNotifications(data: {
  receiver_ids: string[]
  receiver_type: number
  type: number
  title: string
  content?: string
  url?: string
}): Promise<NotificationResponse[]> {
  return request.post('/notifications/batch', data)
}

/**
 * 更新通知
 */
export function updateNotification(
  notificationId: number,
  data: Partial<{
    title: string
    content: string
    url: string
    status: number
  }>
): Promise<NotificationResponse> {
  return request.put(`/notifications/${notificationId}`, data)
}

/**
 * 删除通知
 */
export function deleteNotification(notificationId: number): Promise<void> {
  return request.delete(`/notifications/${notificationId}`)
}

/**
 * 发送通知
 */
export function sendNotification(notificationId: number): Promise<NotificationResponse> {
  return request.post(`/notifications/${notificationId}/send`)
}

/**
 * 创建并发送通知
 */
export function createAndSendNotification(data: {
  type: number
  receiver_id: string
  receiver_type?: number
  title: string
  content?: string
  url?: string
}): Promise<NotificationResponse> {
  return request.post('/notifications/send-and-create', data)
}
