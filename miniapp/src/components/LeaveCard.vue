<script setup lang="ts">
import { computed } from 'vue'
import type { Attendance } from '@/api/leave'

const props = defineProps<{
  leave: Attendance
}>()

const emit = defineEmits<{
  (e: 'click', leave: Attendance): void
  (e: 'cancel', leave: Attendance): void
}>()

/**
 * 状态颜色映射
 */
const statusColorMap: Record<number, string> = {
  1: '#faad14',  // 待审核 - 黄色
  2: '#52c41a',  // 已通过 - 绿色
  3: '#ff4d4f',  // 已拒绝 - 红色
  4: '#909399'   // 已取消 - 灰色
}

/**
 * 状态颜色
 */
const statusColor = computed(() => {
  if (props.leave.check_time) {
    return statusColorMap[2] // 有签到时间表示已通过
  }
  return statusColorMap[1] // 无签到时间表示待审核
})

/**
 * 状态文本
 */
const statusText = computed(() => {
  if (props.leave.check_time) {
    return '已通过'
  }
  return '待审核'
})

/**
 * 课程名称
 */
const courseName = computed(() => {
  return props.leave.schedule?.course_name || '课程'
})

/**
 * 教师名称
 */
const teacherName = computed(() => {
  return props.leave.schedule?.teacher_name || ''
})

/**
 * 教室名称
 */
const classroomName = computed(() => {
  return props.leave.schedule?.classroom_name || ''
})

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
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * 点击卡片
 */
function onCardClick() {
  emit('click', props.leave)
}

/**
 * 取消请假
 */
function onCancel() {
  emit('cancel', props.leave)
}
</script>

<template>
  <view class="leave-card" @click="onCardClick">
    <!-- 头部信息 -->
    <view class="card-header">
      <view class="course-name">{{ courseName }}</view>
      <view class="status-tag" :style="{ backgroundColor: statusColor }">
        {{ statusText }}
      </view>
    </view>

    <!-- 时间信息 -->
    <view class="time-area">
      <view class="time-item">
        <text class="label">请假日期：</text>
        <text class="value">{{ leave.check_time ? formatDate(leave.check_time) : '待审批' }}</text>
      </view>
      <view class="time-item" v-if="leave.schedule">
        <text class="label">上课时间：</text>
        <text class="value">{{ formatTime(leave.schedule.start_time) }} - {{ formatTime(leave.schedule.end_time) }}</text>
      </view>
    </view>

    <!-- 详细信息 -->
    <view class="detail-area">
      <view class="detail-item" v-if="teacherName">
        <text class="label">授课教师：</text>
        <text class="value">{{ teacherName }}</text>
      </view>
      <view class="detail-item" v-if="classroomName">
        <text class="label">上课教室：</text>
        <text class="value">{{ classroomName }}</text>
      </view>
      <view class="detail-item">
        <text class="label">消耗课时：</text>
        <text class="value">{{ leave.hours_consumed }}课时</text>
      </view>
    </view>

    <!-- 请假原因 -->
    <view class="reason-area" v-if="leave.notes">
      <view class="label">请假原因：</view>
      <view class="reason">{{ leave.notes }}</view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-area" v-if="!leave.check_time">
      <view class="cancel-btn" @click.stop="onCancel">
        取消请假
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.leave-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin: 16rpx 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;

  .course-name {
    font-size: 32rpx;
    font-weight: 600;
    color: #303133;
  }

  .status-tag {
    font-size: 22rpx;
    color: #ffffff;
    padding: 6rpx 16rpx;
    border-radius: 6rpx;
  }
}

.time-area {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  margin-bottom: 16rpx;
  padding-bottom: 16rpx;
  border-bottom: 1rpx solid #f0f0f0;

  .time-item {
    display: flex;
    align-items: center;
    font-size: 26rpx;

    .label {
      color: #909399;
    }

    .value {
      color: #303133;
    }
  }
}

.detail-area {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  margin-bottom: 16rpx;

  .detail-item {
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

.reason-area {
  padding: 16rpx;
  background-color: #f5f7fa;
  border-radius: 8rpx;
  margin-bottom: 16rpx;

  .label {
    font-size: 24rpx;
    color: #909399;
    margin-bottom: 8rpx;
  }

  .reason {
    font-size: 26rpx;
    color: #606266;
    line-height: 1.5;
  }
}

.action-area {
  display: flex;
  justify-content: flex-end;

  .cancel-btn {
    font-size: 26rpx;
    color: #ff4d4f;
    padding: 12rpx 24rpx;
    border: 1rpx solid #ff4d4f;
    border-radius: 8rpx;
  }
}
</style>
