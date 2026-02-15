<template>
  <div
    class="notification-card"
    :class="{ unread: notification.status !== 3 }"
    @click="handleClick"
  >
    <div class="card-icon" :class="iconClass">
      <van-icon :name="iconName" />
    </div>
    <div class="card-content">
      <div class="card-header">
        <h4 class="title">{{ notification.title }}</h4>
        <span class="time">{{ formatTime(notification.created_at) }}</span>
      </div>
      <p class="content" v-if="notification.content">
        {{ notification.content }}
      </p>
    </div>
    <div class="card-arrow">
      <van-icon name="arrow" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import dayjs from 'dayjs'
import type { NotificationResponse } from '@/api/types'

const props = defineProps<{
  notification: NotificationResponse
}>()

const emit = defineEmits<{
  click: []
  read: []
}>()

// 图标名称
const iconName = computed(() => {
  switch (props.notification.type) {
    case 1:
      return 'calendar-o'
    case 2:
      return 'edit'
    case 3:
      return 'todo-list-o'
    case 4:
      return 'contract'
    case 5:
      return 'info-o'
    default:
      return 'bell-o'
  }
})

// 图标样式
const iconClass = computed(() => {
  switch (props.notification.type) {
    case 1:
      return 'class'
    case 2:
      return 'homework'
    case 3:
      return 'attendance'
    case 4:
      return 'contract'
    case 5:
      return 'system'
    default:
      return 'default'
  }
})

function formatTime(dateStr: string) {
  const date = dayjs(dateStr)
  const now = dayjs()
  const diff = now.diff(date, 'day')

  if (diff === 0) {
    return date.format('HH:mm')
  } else if (diff === 1) {
    return '昨天 ' + date.format('HH:mm')
  } else if (diff < 7) {
    return date.format('dddd HH:mm')
  } else {
    return date.format('YYYY-MM-DD HH:mm')
  }
}

function handleClick() {
  emit('click')
}
</script>

<style lang="scss" scoped>
.notification-card {
  display: flex;
  align-items: flex-start;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s;

  &:active {
    transform: scale(0.98);
    background: #f5f5f5;
  }

  &.unread {
    border-left: 3px solid #667eea;

    .card-icon {
      background: #e3f2fd;
    }
  }
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-right: 12px;

  &.class {
    background: #e3f2fd;
    color: #1976d2;
  }

  &.homework {
    background: #f3e5f5;
    color: #7b1fa2;
  }

  &.attendance {
    background: #fff3e0;
    color: #f57c00;
  }

  &.contract {
    background: #e8f5e9;
    color: #388e3c;
  }

  &.system {
    background: #fafafa;
    color: #757575;
  }
}

.card-content {
  flex: 1;
  min-width: 0;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;

    .title {
      font-size: 15px;
      font-weight: 500;
      margin: 0;
      color: #333;
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .time {
      font-size: 12px;
      color: #999;
      margin-left: 8px;
      white-space: nowrap;
    }
  }

  .content {
    font-size: 13px;
    color: #666;
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
}

.card-arrow {
  color: #ccc;
  margin-left: 8px;
}
</style>
