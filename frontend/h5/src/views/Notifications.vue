<template>
  <div class="notifications-page">
    <!-- 筛选标签 -->
    <div class="filter-tabs">
      <van-tabs v-model:active="activeTab" @change="onTabChange">
        <van-tab name="all" title="全部" />
        <van-tab name="unread" title="未读">
          <template #title>
            <span>未读</span>
            <van-badge v-if="unreadCount > 0" :content="unreadCount" max="99" />
          </template>
        </van-tab>
        <van-tab name="class" title="上课提醒" />
        <van-tab name="homework" title="作业通知" />
        <van-tab name="attendance" title="考勤通知" />
      </van-tabs>
    </div>

    <!-- 操作栏 -->
    <div class="action-bar" v-if="notifications.length > 0">
      <van-button size="small" type="primary" plain @click="markAllAsRead" :disabled="unreadCount === 0">
        全部标为已读
      </van-button>
    </div>

    <!-- 通知列表 -->
    <div class="notification-list" v-if="notifications.length > 0" ref="listRef">
      <NotificationCard
        v-for="notification in notifications"
        :key="notification.id"
        :notification="notification"
        @click="goToDetail(notification.id)"
        @read="markAsRead([notification.id])"
      />
      <!-- 加载更多 -->
      <div class="load-more" v-if="pagination.hasMore" @click="loadMore">
        <van-loading v-if="loading" size="16" />
        <span v-else>加载更多</span>
      </div>
      <div class="no-more" v-else>
        <span>没有更多了</span>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-else>
      <van-icon name="bell-o" size="64" color="#ccc" />
      <p>暂无通知</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notification'
import NotificationCard from '@/components/NotificationCard.vue'

const router = useRouter()
const notificationStore = useNotificationStore()

// 当前标签
const activeTab = ref('all')

// 列表引用
const listRef = ref<HTMLElement>()

// 计算属性
const notifications = computed(() => notificationStore.notifications)
const unreadCount = computed(() => notificationStore.unreadCount)
const loading = computed(() => notificationStore.loading)
const pagination = computed(() => notificationStore.pagination)

// Tab 类型映射
const typeMap: Record<string, number | undefined> = {
  class: 1,
  homework: 2,
  attendance: 3,
}

// Tab 切换
function onTabChange(name: string) {
  const type = typeMap[name]
  notificationStore.fetchNotifications({ type: type, refresh: true })
}

// 加载更多
function loadMore() {
  notificationStore.loadMoreNotifications()
}

// 标记已读
async function markAsRead(ids: number[]) {
  await notificationStore.markAsRead(ids)
}

// 标记全部已读
async function markAllAsRead() {
  await notificationStore.markAllAsRead()
}

// 跳转到详情
function goToDetail(id: number) {
  router.push(`/notifications/${id}`)
}

// 生命周期
onMounted(async () => {
  await notificationStore.fetchNotifications({ refresh: true })
})

onUnmounted(() => {
  notificationStore.clearState()
})
</script>

<style lang="scss" scoped>
.notifications-page {
  padding: 16px;
  padding-bottom: 80px;
}

.filter-tabs {
  background: #fff;
  border-radius: 12px;
  margin-bottom: 16px;
  overflow: hidden;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;
}

.notification-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.load-more,
.no-more {
  text-align: center;
  padding: 16px;
  color: #999;
  font-size: 14px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;

  p {
    color: #999;
    margin: 16px 0 0;
  }
}
</style>
