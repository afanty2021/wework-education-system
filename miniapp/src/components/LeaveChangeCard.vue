<script setup lang="ts">
import { computed } from 'vue'
import type { LeaveChange } from '@/api/leavechange'
import { LeaveChangeStatusText } from '@/api/leavechange'

const props = defineProps<{
  leaveChange: LeaveChange
}>()

const emit = defineEmits<{
  (e: 'click', leaveChange: LeaveChange): void
  (e: 'cancel', leaveChange: LeaveChange): void
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
const statusColor = computed(() => statusColorMap[props.leaveChange.status] || '#999999')

/**
 * 状态文本
 */
const statusText = computed(() => LeaveChangeStatusText[props.leaveChange.status] || '')

/**
 * 原课程名称
 */
const originalCourseName = computed(() => {
  return props.leaveChange.original_schedule?.course_name || '课程'
})

/**
 * 目标课程名称
 */
const targetCourseName = computed(() => {
  if (props.leaveChange.target_schedule) {
    return props.leaveChange.target_schedule.course_name || '课程'
  }
  return '待安排'
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
  emit('click', props.leaveChange)
}

/**
 * 取消调课
 */
function onCancel() {
  emit('cancel', props.leaveChange)
}
</script>

<template>
  <view class="leave-change-card" @click="onCardClick">
    <!-- 头部信息 -->
    <view class="card-header">
      <view class="title">调课申请</view>
      <view class="status-tag" :style="{ backgroundColor: statusColor }">
        {{ statusText }}
      </view>
    </view>

    <!-- 调课信息 -->
    <view class="change-area">
      <!-- 原课程 -->
      <view class="course-item original">
        <view class="label">原课程</view>
        <view class="course-name">{{ originalCourseName }}</view>
        <view class="course-time" v-if="leaveChange.original_schedule">
          {{ formatDate(leaveChange.original_schedule.start_time) }}
          {{ formatTime(leaveChange.original_schedule.start_time) }} -
          {{ formatTime(leaveChange.original_schedule.end_time) }}
        </view>
      </view>

      <!-- 箭头 -->
      <view class="arrow">
        <text class="icon">-></text>
      </view>

      <!-- 目标课程 -->
      <view class="course-item target">
        <view class="label">目标课程</view>
        <view class="course-name">{{ targetCourseName }}</view>
        <view class="course-time" v-if="leaveChange.target_date">
          {{ formatDate(leaveChange.target_date) }}
        </view>
        <view class="course-time" v-else-if="leaveChange.target_schedule">
          {{ formatDate(leaveChange.target_schedule.start_time) }}
          {{ formatTime(leaveChange.target_schedule.start_time) }} -
          {{ formatTime(leaveChange.target_schedule.end_time) }}
        </view>
        <view class="course-time" v-else>
          待安排
        </view>
      </view>
    </view>

    <!-- 调课原因 -->
    <view class="reason-area" v-if="leaveChange.reason">
      <view class="label">调课原因：</view>
      <view class="reason">{{ leaveChange.reason }}</view>
    </view>

    <!-- 审核信息 -->
    <view class="approve-area" v-if="leaveChange.status === 3 && leaveChange.reject_reason">
      <view class="label">拒绝原因：</view>
      <view class="reject-reason">{{ leaveChange.reject_reason }}</view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-area" v-if="leaveChange.status === 1">
      <view class="cancel-btn" @click.stop="onCancel">
        取消申请
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.leave-change-card {
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

  .title {
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

.change-area {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16rpx;
  background-color: #f5f7fa;
  border-radius: 8rpx;
  margin-bottom: 16rpx;

  .course-item {
    flex: 1;

    .label {
      font-size: 22rpx;
      color: #909399;
      margin-bottom: 8rpx;
    }

    .course-name {
      font-size: 28rpx;
      font-weight: 500;
      color: #303133;
      margin-bottom: 4rpx;
    }

    .course-time {
      font-size: 24rpx;
      color: #606266;
    }
  }

  .arrow {
    padding: 0 16rpx;
    color: #1890ff;
    font-size: 32rpx;
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

.approve-area {
  padding: 16rpx;
  background-color: #fff2f0;
  border-radius: 8rpx;
  margin-bottom: 16rpx;

  .label {
    font-size: 24rpx;
    color: #ff4d4f;
    margin-bottom: 8rpx;
  }

  .reject-reason {
    font-size: 26rpx;
    color: #ff4d4f;
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
