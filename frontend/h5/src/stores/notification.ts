/**
 * 通知状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getNotifications,
  getUnreadCount,
  getNotificationDetail,
  markNotificationsAsRead,
  deleteNotification,
  type NotificationResponse,
  type NotificationListResponse,
} from '@/api/notifications'
import { useAuthStore } from './auth'

export const useNotificationStore = defineStore('notification', () => {
  const authStore = useAuthStore()

  // 通知列表
  const notifications = ref<NotificationResponse[]>([])

  // 未读数量
  const unreadCount = ref(0)

  // 加载状态
  const loading = ref(false)

  // 分页
  const pagination = ref({
    skip: 0,
    limit: 20,
    hasMore: true,
  })

  // 计算属性
  const receiverId = computed(() => String(authStore.userId))

  /**
   * 获取通知列表
   */
  async function fetchNotifications(params?: {
    type?: number
    status?: number
    refresh?: boolean
  }) {
    loading.value = true
    try {
      if (params?.refresh) {
        pagination.value.skip = 0
        notifications.value = []
      }

      const response = await getNotifications({
        skip: pagination.value.skip,
        limit: pagination.value.limit,
        receiver_id: receiverId.value,
        type: params?.type,
        status: params?.status,
      })

      if (params?.refresh || pagination.value.skip === 0) {
        notifications.value = response.items
      } else {
        notifications.value = [...notifications.value, ...response.items]
      }

      unreadCount.value = response.unread_count
      pagination.value.skip += response.items.length
      pagination.value.hasMore = notifications.value.length < response.total

      return response
    } catch (error) {
      console.error('获取通知列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 加载更多通知
   */
  async function loadMoreNotifications() {
    if (loading.value || !pagination.value.hasMore) {
      return
    }
    await fetchNotifications()
  }

  /**
   * 刷新通知列表
   */
  async function refreshNotifications() {
    return fetchNotifications({ refresh: true })
  }

  /**
   * 获取未读数量
   */
  async function fetchUnreadCount() {
    try {
      const response = await getUnreadCount(receiverId.value)
      unreadCount.value = response.unread_count
      return response.unread_count
    } catch (error) {
      console.error('获取未读数量失败:', error)
      throw error
    }
  }

  /**
   * 获取通知详情
   */
  async function fetchNotificationDetail(notificationId: number): Promise<NotificationResponse> {
    try {
      const notification = await getNotificationDetail(notificationId)
      // 更新列表中的通知状态
      const index = notifications.value.findIndex((item) => item.id === notificationId)
      if (index !== -1) {
        notifications.value[index] = notification
      }
      return notification
    } catch (error) {
      console.error('获取通知详情失败:', error)
      throw error
    }
  }

  /**
   * 标记通知为已读
   */
  async function markAsRead(notificationIds: number[]) {
    try {
      await markNotificationsAsRead({ notification_ids: notificationIds })
      // 更新本地状态
      notificationIds.forEach((id) => {
        const notification = notifications.value.find((item) => item.id === id)
        if (notification) {
          notification.status = 3 // 已读状态
        }
      })
      // 减少未读数量
      unreadCount.value = Math.max(0, unreadCount.value - notificationIds.length)
    } catch (error) {
      console.error('标记已读失败:', error)
      throw error
    }
  }

  /**
   * 标记所有通知为已读
   */
  async function markAllAsRead() {
    try {
      const unreadIds = notifications.value
        .filter((item) => item.status !== 3)
        .map((item) => item.id)
      if (unreadIds.length > 0) {
        await markAsRead(unreadIds)
      }
    } catch (error) {
      console.error('标记全部已读失败:', error)
      throw error
    }
  }

  /**
   * 删除通知
   */
  async function removeNotification(notificationId: number) {
    try {
      await deleteNotification(notificationId)
      // 从列表中移除
      notifications.value = notifications.value.filter((item) => item.id !== notificationId)
    } catch (error) {
      console.error('删除通知失败:', error)
      throw error
    }
  }

  /**
   * 清空状态
   */
  function clearState() {
    notifications.value = []
    unreadCount.value = 0
    pagination.value = {
      skip: 0,
      limit: 20,
      hasMore: true,
    }
  }

  return {
    // 状态
    notifications,
    unreadCount,
    loading,
    pagination,
    // 方法
    fetchNotifications,
    loadMoreNotifications,
    refreshNotifications,
    fetchUnreadCount,
    fetchNotificationDetail,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearState,
  }
})
