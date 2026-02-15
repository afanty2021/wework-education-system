<script setup lang="ts">
import { computed } from 'vue'
import type { Homework } from '@/api/homework'
import { HomeworkSubmitStatus, HomeworkSubmitStatusText } from '@/api/homework'

const props = defineProps<{
  homework: Homework
}>()

const emit = defineEmits<{
  (e: 'click', homework: Homework): void
}>()

/**
 * 格式化截止日期
 */
function formatDueDate(date: string | null): string {
  if (!date) return '无截止日期'
  const dueDate = new Date(date)
  const now = new Date()
  const diff = dueDate.getTime() - now.getTime()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

  if (days < 0) {
    return `已过期`
  } else if (days === 0) {
    return `今天截止`
  } else if (days === 1) {
    return `明天截止`
  } else if (days <= 7) {
    return `${days}天后截止`
  } else {
    return dueDate.toLocaleDateString('zh-CN', {
      month: 'long',
      day: 'numeric'
    })
  }
}

/**
 * 获取截止日期样式
 */
function getDueDateStyle(date: string | null): string {
  if (!date) return 'color: #909399'
  const dueDate = new Date(date)
  const now = new Date()
  const diff = dueDate.getTime() - now.getTime()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

  if (days < 0) {
    return 'color: #ff4d4f'
  } else if (days <= 1) {
    return 'color: #faad14'
  } else if (days <= 3) {
    return 'color: #1890ff'
  } else {
    return 'color: #909399'
  }
}

/**
 * 获取提交状态
 */
const submitStatus = computed(() => {
  const { homework } = props
  if (!homework.submission) {
    return HomeworkSubmitStatus.NOT_SUBMITTED
  } else if (homework.submission.score !== null) {
    return HomeworkSubmitStatus.GRADED
  } else {
    return HomeworkSubmitStatus.SUBMITTED
  }
})

/**
 * 获取提交状态文本
 */
const statusText = computed(() => {
  return HomeworkSubmitStatusText[submitStatus.value]
})

/**
 * 获取状态颜色
 */
const statusColor = computed(() => {
  switch (submitStatus.value) {
    case HomeworkSubmitStatus.NOT_SUBMITTED:
      return '#ff4d4f'
    case HomeworkSubmitStatus.SUBMITTED:
      return '#1890ff'
    case HomeworkSubmitStatus.GRADED:
      return '#52c41a'
    default:
      return '#909399'
  }
})

/**
 * 获取分数显示
 */
const scoreDisplay = computed(() => {
  const { homework } = props
  if (homework.submission?.score !== null && homework.submission?.score !== undefined) {
    return `${homework.submission.score}分`
  }
  return ''
})

/**
 * 点击卡片
 */
function onCardClick() {
  emit('click', props.homework)
}
</script>

<template>
  <view class="homework-card" @click="onCardClick">
    <!-- 标题和状态 -->
    <view class="header">
      <view class="title">{{ homework.title }}</view>
      <view class="status-tag" :style="{ color: statusColor, backgroundColor: statusColor + '20' }">
        {{ statusText }}
      </view>
    </view>

    <!-- 课程名称 -->
    <view class="course-name">{{ homework.course_name || `课程ID: ${homework.course_id}` }}</view>

    <!-- 内容预览 -->
    <view class="content-preview">
      {{ homework.content.slice(0, 100) }}{{ homework.content.length > 100 ? '...' : '' }}
    </view>

    <!-- 底部信息 -->
    <view class="footer">
      <!-- 截止日期 -->
      <view class="due-date" :style="getDueDateStyle(homework.due_date)">
        <text class="icon">截止：</text>
        <text class="text">{{ formatDueDate(homework.due_date) }}</text>
      </view>

      <!-- 分数 -->
      <view class="score" v-if="scoreDisplay">
        <text class="score-value">{{ scoreDisplay }}</text>
        <text class="score-max">/ {{ homework.max_score }}分</text>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.homework-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin: 16rpx 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;

  .title {
    font-size: 32rpx;
    font-weight: 600;
    color: #303133;
    flex: 1;
    margin-right: 16rpx;
  }

  .status-tag {
    font-size: 24rpx;
    font-weight: 500;
    padding: 6rpx 16rpx;
    border-radius: 6rpx;
    flex-shrink: 0;
  }
}

.course-name {
  font-size: 26rpx;
  color: #909399;
  margin-bottom: 12rpx;
}

.content-preview {
  font-size: 28rpx;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16rpx;
  border-top: 2rpx solid #f5f5f5;

  .due-date {
    display: flex;
    align-items: center;
    font-size: 24rpx;

    .icon {
      margin-right: 4rpx;
    }
  }

  .score {
    .score-value {
      font-size: 32rpx;
      font-weight: 600;
      color: #52c41a;
    }

    .score-max {
      font-size: 24rpx;
      color: #909399;
    }
  }
}
</style>
