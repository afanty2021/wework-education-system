<template>
  <div class="notification-detail-page">
    <van-loading v-if="loading" size="24" />
    <template v-else-if="notification">
      <!-- 通知头部 -->
      <div class="notification-header">
        <div class="header-top">
          <van-tag :type="typeTagType">{{ typeText }}</van-tag>
          <span class="time">{{ formatTime(notification.created_at) }}</span>
        </div>
        <h2 class="title">{{ notification.title }}</h2>
      </div>

      <!-- 通知内容 -->
      <div class="notification-content">
        <div class="content-text" v-if="notification.content">
          {{ notification.content }}
        </div>
        <div class="content-empty" v-else>
          <p>暂无内容</p>
        </div>
      </div>

      <!-- 跳转链接 -->
      <div class="notification-action" v-if="notification.url">
        <van-button type="primary" block @click="openUrl(notification.url)">
          前往查看
        </van-button>
      </div>

      <!-- 通知元信息 -->
      <div class="notification-meta">
        <div class="meta-item" v-if="notification.sent_at">
          <span class="label">发送时间：</span>
          <span class="value">{{ formatTime(notification.sent_at) }}</span>
        </div>
        <div class="meta-item" v-if="notification.read_at">
          <span class="label">阅读时间：</span>
          <span class="value">{{ formatTime(notification.read_at) }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions">
        <van-button
          v-if="notification.status !== 3"
          type="primary"
          block
          @click="markAsRead"
        >
          标记为已读
        </van-button>
        <van-button type="danger" plain block @click="deleteNotification">
          删除通知
        </van-button>
      </div>
    </template>
    <van-empty v-else description="通知不存在" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import { useNotificationStore } from '@/stores/notification'
import { showSuccess, showFail } from '@/stores/app'

const route = useRoute()
const notificationStore = useNotificationStore()

const notificationId = computed(() => Number(route.params.id))
const notification = computed(() => {
  return notificationStore.notifications.find((n) => n.id === notificationId.value)
})
const loading = computed(() => notificationStore.loading)

// 通知类型
const typeMap: Record<number, { text: string; type: 'primary' | 'success' | 'warning' | 'danger' | 'default' }> = {
  1: { text: '上课提醒', type: 'primary' },
  2: { text: '作业通知', type: 'success' },
  3: { text: '考勤通知', type: 'warning' },
  4: { text: '合同通知', type: 'danger' },
  5: { text: '系统通知', type: 'default' },
}

const typeText = computed(() => {
  return typeMap[notification.value?.type || 0]?.text || '通知'
})

const typeTagType = computed(() => {
  return typeMap[notification.value?.type || 0]?.type || 'default'
})

function formatTime(dateStr: string) {
  return dayjs(dateStr).format('YYYY年MM月DD日 HH:mm')
}

function openUrl(url: string) {
  window.open(url, '_blank')
}

async function markAsRead() {
  try {
    await notificationStore.markAsRead([notificationId.value])
    showSuccess('已标记为已读')
  } catch (error) {
    showFail('操作失败')
  }
}

async function deleteNotification() {
  try {
    await notificationStore.removeNotification(notificationId.value)
    showSuccess('删除成功')
    history.back()
  } catch (error) {
    showFail('删除失败')
  }
}

onMounted(async () => {
  await notificationStore.fetchNotificationDetail(notificationId.value)
})
</script>

<style lang="scss" scoped>
.notification-detail-page {
  padding: 16px;
  padding-bottom: 80px;
}

.notification-header {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .time {
    font-size: 12px;
    color: #999;
  }

  .title {
    font-size: 20px;
    font-weight: 600;
    margin: 0;
    line-height: 1.4;
  }
}

.notification-content {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;

  .content-text {
    font-size: 15px;
    line-height: 1.6;
    color: #333;
    white-space: pre-wrap;
  }

  .content-empty {
    text-align: center;
    color: #999;
    padding: 20px;
  }
}

.notification-action {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.notification-meta {
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 16px;

  .meta-item {
    display: flex;
    font-size: 13px;
    margin-bottom: 8px;

    &:last-child {
      margin-bottom: 0;
    }

    .label {
      color: #999;
      margin-right: 8px;
    }

    .value {
      color: #666;
    }
  }
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: #fff;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}
</style>
