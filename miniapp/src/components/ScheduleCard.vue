<script setup lang="ts">
import { computed } from 'vue'
import type { Schedule } from '@/api/schedule'
import { WeekDayText, ScheduleStatusText, ScheduleStatusColor } from '@/types'

const props = defineProps<{
  schedule: Schedule
  showDate?: boolean
}>()

const emit = defineEmits<{
  (e: 'click', schedule: Schedule): void
  (e: 'remind', schedule: Schedule): void
}>()

/**
 * 格式化时间
 */
function formatTime(time: string): string {
  return new Date(time).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 格式化日期
 */
function formatDate(time: string): string {
  return new Date(time).toLocaleDateString('zh-CN', {
    month: 'long',
    day: 'numeric'
  })
}

/**
 * 课程时间文本
 */
const timeText = computed(() => {
  const { schedule } = props
  return `${formatTime(schedule.start_time)} - ${formatTime(schedule.end_time)}`
})

/**
 * 星期文本
 */
const weekdayText = computed(() => {
  const { schedule } = props
  if (schedule.week_day) {
    return WeekDayText[schedule.week_day] || ''
  }
  return formatDate(schedule.start_time)
})

/**
 * 状态颜色
 */
const statusColor = computed(() => {
  const { schedule } = props
  return ScheduleStatusColor[schedule.status as keyof typeof ScheduleStatusColor] || '#1890ff'
})

/**
 * 状态文本
 */
const statusText = computed(() => {
  const { schedule } = props
  return ScheduleStatusText[schedule.status as keyof typeof ScheduleStatusText] || ''
})

/**
 * 点击卡片
 */
function onCardClick() {
  emit('click', props.schedule)
}

/**
 * 设置提醒
 */
function onRemind() {
  emit('remind', props.schedule)
}
</script>

<template>
  <view class="schedule-card" @click="onCardClick">
    <!-- 时间区域 -->
    <view class="time-area">
      <view class="weekday">{{ weekdayText }}</view>
      <view class="time">{{ timeText }}</view>
    </view>

    <!-- 课程信息 -->
    <view class="course-info">
      <view class="course-name">{{ schedule.course_name || `课程ID: ${schedule.course_id}` }}</view>
      <view class="course-detail">
        <view class="teacher" v-if="schedule.teacher_name">
          <text class="label">教师：</text>
          <text class="value">{{ schedule.teacher_name }}</text>
        </view>
        <view class="classroom" v-if="schedule.classroom_name">
          <text class="label">教室：</text>
          <text class="value">{{ schedule.classroom_name }}</text>
        </view>
      </view>
    </view>

    <!-- 状态标签 -->
    <view class="status-area">
      <view class="status-tag" :style="{ backgroundColor: statusColor }">
        {{ statusText }}
      </view>
      <view class="remind-btn" @click.stop="onRemind">
        <text class="icon">提醒</text>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.schedule-card {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin: 16rpx 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.time-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 140rpx;
  padding-right: 24rpx;
  border-right: 2rpx solid #f0f0f0;

  .weekday {
    font-size: 28rpx;
    font-weight: 600;
    color: #1890ff;
    margin-bottom: 8rpx;
  }

  .time {
    font-size: 24rpx;
    color: #909399;
  }
}

.course-info {
  flex: 1;
  padding: 0 24rpx;

  .course-name {
    font-size: 32rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 12rpx;
  }

  .course-detail {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;

    .teacher,
    .classroom {
      display: flex;
      align-items: center;
      font-size: 26rpx;

      .label {
        color: #909399;
      }

      .value {
        color: #606266;
      }
    }
  }
}

.status-area {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12rpx;

  .status-tag {
    font-size: 22rpx;
    color: #ffffff;
    padding: 6rpx 16rpx;
    border-radius: 6rpx;
  }

  .remind-btn {
    font-size: 24rpx;
    color: #1890ff;
    padding: 8rpx 0;
  }
}
</style>
