<script setup lang="ts">
import { computed } from 'vue'
import type { Attendance } from '@/api/attendance'
import { AttendanceStatusText, AttendanceStatusColor } from '@/api/attendance'

const props = defineProps<{
  attendance: Attendance
}>()

const emit = defineEmits<{
  (e: 'click', attendance: Attendance): void
}>()

/**
 * 格式化日期
 */
function formatDate(time: string): string {
  return new Date(time).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short'
  })
}

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
 * 获取课程名称
 */
const courseName = computed(() => {
  return props.attendance.schedule?.course_name || '未知课程'
})

/**
 * 获取上课时间
 */
const classTime = computed(() => {
  const { schedule } = props.attendance
  if (schedule) {
    const startTime = new Date(schedule.start_time).toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    })
    return `${startTime} ${schedule.classroom_name || ''}`
  }
  return ''
})

/**
 * 获取考勤状态文本
 */
const statusText = computed(() => {
  return AttendanceStatusText[props.attendance.status] || '未知'
})

/**
 * 获取考勤状态颜色
 */
const statusColor = computed(() => {
  return AttendanceStatusColor[props.attendance.status] || '#909399'
})

/**
 * 点击卡片
 */
function onCardClick() {
  emit('click', props.attendance)
}
</script>

<template>
  <view class="attendance-card" @click="onCardClick">
    <!-- 日期时间 -->
    <view class="date-time">
      <view class="date">{{ formatDate(attendance.created_at) }}</view>
      <view class="time" v-if="attendance.check_time">
        {{ formatTime(attendance.check_time) }}
      </view>
    </view>

    <!-- 课程信息 -->
    <view class="course-info">
      <view class="course-name">{{ courseName }}</view>
      <view class="class-info">{{ classTime }}</view>
    </view>

    <!-- 状态标签 -->
    <view class="status-tag" :style="{ color: statusColor, backgroundColor: statusColor + '20' }">
      {{ statusText }}
    </view>

    <!-- 消耗课时 -->
    <view class="hours-info">
      <text class="hours">{{ attendance.hours_consumed }}课时</text>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.attendance-card {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin: 16rpx 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.date-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 160rpx;
  padding-right: 20rpx;
  border-right: 2rpx solid #f0f0f0;

  .date {
    font-size: 26rpx;
    color: #303133;
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
    font-size: 30rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8rpx;
  }

  .class-info {
    font-size: 24rpx;
    color: #909399;
  }
}

.status-tag {
  font-size: 26rpx;
  font-weight: 500;
  padding: 8rpx 20rpx;
  border-radius: 8rpx;
  margin-right: 16rpx;
}

.hours-info {
  .hours {
    font-size: 24rpx;
    color: #606266;
  }
}
</style>
