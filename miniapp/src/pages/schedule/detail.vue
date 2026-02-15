<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useScheduleStore } from '@/stores/schedule'
import type { Schedule } from '@/api/schedule'

const route = useRoute()
const scheduleStore = useScheduleStore()

// 页面状态
const loading = ref(true)
const schedule = ref<Schedule | null>(null)

// 课程ID
const scheduleId = computed(() => parseInt(route.query.id as string) || 0)

/**
 * 加载课程详情
 */
async function loadScheduleDetail() {
  if (!scheduleId.value) {
    uni.showToast({
      title: '参数错误',
      icon: 'error'
    })
    return
  }

  loading.value = true
  try {
    schedule.value = await scheduleStore.fetchScheduleDetail(scheduleId.value)
  } catch (error) {
    console.error('加载课程详情失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 格式化时间
 */
function formatTime(time: string): string {
  return new Date(time).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 设置提醒
 */
function setReminder() {
  uni.showModal({
    title: '课程提醒',
    content: '确定要设置课程开始提醒吗？',
    success: (res) => {
      if (res.confirm) {
        uni.showToast({
          title: '已设置提醒',
          icon: 'success'
        })
      }
    }
  })
}

/**
 * 分享课程
 */
function shareCourse() {
  uni.showShareMenu({
    menus: ['shareAppMessage', 'shareTimeline']
  })
}

import { computed } from 'vue'

onMounted(() => {
  loadScheduleDetail()
})
</script>

<template>
  <view class="schedule-detail-container" v-if="schedule">
    <!-- 课程信息卡片 -->
    <view class="course-card">
      <view class="course-header">
        <view class="course-name">{{ schedule.course_name || `课程ID: ${schedule.course_id}` }}</view>
        <view class="status-badge" :class="`status-${schedule.status}`">
          {{ ['已安排', '已上课', '已取消', '已调课'][schedule.status - 1] || '未知' }}
        </view>
      </view>

      <view class="course-time">
        <view class="time-item">
          <text class="label">开始时间</text>
          <text class="value">{{ formatTime(schedule.start_time) }}</text>
        </view>
        <view class="time-item">
          <text class="label">结束时间</text>
          <text class="value">{{ formatTime(schedule.end_time) }}</text>
        </view>
      </view>
    </view>

    <!-- 教师信息 -->
    <view class="info-card" v-if="schedule.teacher_name">
      <view class="card-title">教师信息</view>
      <view class="info-row">
        <text class="label">教师姓名</text>
        <text class="value">{{ schedule.teacher_name }}</text>
      </view>
    </view>

    <!-- 教室信息 -->
    <view class="info-card" v-if="schedule.classroom_name">
      <view class="card-title">教室信息</view>
      <view class="info-row">
        <text class="label">教室</text>
        <text class="value">{{ schedule.classroom_name }}</text>
      </view>
    </view>

    <!-- 备注信息 -->
    <view class="info-card" v-if="schedule.notes">
      <view class="card-title">备注</view>
      <view class="info-content">
        {{ schedule.notes }}
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-buttons">
      <button class="btn primary" @click="setReminder">
        <text class="icon">提醒</text>
        <text>设置提醒</text>
      </button>
      <button class="btn default" open-type="share">
        <text class="icon">分享</text>
        <text>分享课程</text>
      </button>
    </view>
  </view>

  <!-- 加载状态 -->
  <view class="loading-state" v-else-if="loading">
    <text>加载中...</text>
  </view>
</template>

<style lang="scss" scoped>
.schedule-detail-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20rpx;
}

.course-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;

  .course-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32rpx;

    .course-name {
      font-size: 40rpx;
      font-weight: 600;
      color: #303133;
    }

    .status-badge {
      font-size: 24rpx;
      padding: 8rpx 16rpx;
      border-radius: 8rpx;

      &.status-1 {
        background-color: #e6f7ff;
        color: #1890ff;
      }

      &.status-2 {
        background-color: #f6ffed;
        color: #52c41a;
      }

      &.status-3 {
        background-color: #fff2f0;
        color: #ff4d4f;
      }

      &.status-4 {
        background-color: #fffbe6;
        color: #faad14;
      }
    }
  }

  .course-time {
    .time-item {
      display: flex;
      align-items: center;
      padding: 16rpx 0;
      border-bottom: 2rpx solid #f5f5f5;

      &:last-child {
        border-bottom: none;
      }

      .label {
        width: 160rpx;
        font-size: 28rpx;
        color: #909399;
      }

      .value {
        flex: 1;
        font-size: 28rpx;
        color: #303133;
      }
    }
  }
}

.info-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;

  .card-title {
    font-size: 30rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 20rpx;
  }

  .info-row {
    display: flex;
    align-items: center;

    .label {
      width: 160rpx;
      font-size: 28rpx;
      color: #909399;
    }

    .value {
      flex: 1;
      font-size: 28rpx;
      color: #303133;
    }
  }

  .info-content {
    font-size: 28rpx;
    color: #606266;
    line-height: 1.6;
  }
}

.action-buttons {
  display: flex;
  gap: 20rpx;
  padding: 20rpx;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #ffffff;
  padding-bottom: calc(20rpx + constant(safe-area-inset-bottom));
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));

  .btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 88rpx;
    border-radius: 44rpx;
    font-size: 30rpx;

    .icon {
      margin-right: 8rpx;
    }

    &.primary {
      background-color: #1890ff;
      color: #ffffff;
    }

    &.default {
      background-color: #f5f5f5;
      color: #606266;
    }
  }
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400rpx;
  font-size: 28rpx;
  color: #909399;
}
</style>
