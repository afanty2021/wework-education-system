<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useLeaveStore } from '@/stores/leave'

const leaveStore = useLeaveStore()

// 页面状态
const loading = ref(true)
const leaveId = ref<number>(0)

/**
 * 状态颜色
 */
const statusColor = computed(() => {
  if (leaveStore.currentLeave?.check_time) {
    return '#52c41a' // 已通过 - 绿色
  }
  return '#faad14' // 待审核 - 黄色
})

/**
 * 状态文本
 */
const statusText = computed(() => {
  if (leaveStore.currentLeave?.check_time) {
    return '已通过'
  }
  return '待审核'
})

/**
 * 课程名称
 */
const courseName = computed(() => {
  return leaveStore.currentLeave?.schedule?.course_name || '课程'
})

/**
 * 教师名称
 */
const teacherName = computed(() => {
  return leaveStore.currentLeave?.schedule?.teacher_name || ''
})

/**
 * 教室名称
 */
const classroomName = computed(() => {
  return leaveStore.currentLeave?.schedule?.classroom_name || ''
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
 * 格式化日期时间
 */
function formatDateTime(date: string): string {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 加载请假详情
 */
async function loadLeaveDetail() {
  loading.value = true
  try {
    await leaveStore.fetchLeaveDetail(leaveId.value)
  } catch (error) {
    console.error('加载请假详情失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 取消请假
 */
function cancelLeave() {
  uni.showModal({
    title: '提示',
    content: '确定要取消该请假申请吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await leaveStore.cancelLeave(leaveId.value)
          uni.showToast({
            title: '取消成功',
            icon: 'success'
          })
          setTimeout(() => {
            uni.navigateBack()
          }, 1500)
        } catch (error) {
          uni.showToast({
            title: '取消失败',
            icon: 'none'
          })
        }
      }
    }
  })
}

onMounted(() => {
  // 获取页面参数
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = currentPage?.options || {}

  if (options.id) {
    leaveId.value = parseInt(options.id)
    loadLeaveDetail()
  } else {
    uni.showToast({
      title: '参数错误',
      icon: 'none'
    })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  }
})
</script>

<template>
  <view class="leave-detail-container">
    <!-- 加载中 -->
    <view v-if="loading" class="loading-container">
      <text>加载中...</text>
    </view>

    <!-- 请假详情 -->
    <view v-else-if="leaveStore.currentLeave" class="detail-content">
      <!-- 状态卡片 -->
      <view class="status-card">
        <view class="status-icon">
          <text v-if="!leaveStore.currentLeave.check_time">!</text>
          <text v-else>&#10003;</text>
        </view>
        <view class="status-text">{{ statusText }}</view>
      </view>

      <!-- 课程信息 -->
      <view class="info-card">
        <view class="info-title">课程信息</view>
        <view class="info-item">
          <text class="label">课程名称</text>
          <text class="value">{{ courseName }}</text>
        </view>
        <view class="info-item" v-if="teacherName">
          <text class="label">授课教师</text>
          <text class="value">{{ teacherName }}</text>
        </view>
        <view class="info-item" v-if="classroomName">
          <text class="label">上课教室</text>
          <text class="value">{{ classroomName }}</text>
        </view>
        <view class="info-item" v-if="leaveStore.currentLeave.schedule">
          <text class="label">上课时间</text>
          <text class="value">
            {{ formatTime(leaveStore.currentLeave.schedule.start_time) }} -
            {{ formatTime(leaveStore.currentLeave.schedule.end_time) }}
          </text>
        </view>
      </view>

      <!-- 请假信息 -->
      <view class="info-card">
        <view class="info-title">请假信息</view>
        <view class="info-item">
          <text class="label">请假日期</text>
          <text class="value">
            {{ leaveStore.currentLeave.check_time
              ? leaveStore.currentLeave.check_time.split('T')[0]
              : '待审批' }}
          </text>
        </view>
        <view class="info-item">
          <text class="label">消耗课时</text>
          <text class="value">{{ leaveStore.currentLeave.hours_consumed }}课时</text>
        </view>
      </view>

      <!-- 请假原因 -->
      <view class="info-card" v-if="leaveStore.currentLeave.notes">
        <view class="info-title">请假原因</view>
        <view class="reason">{{ leaveStore.currentLeave.notes }}</view>
      </view>

      <!-- 申请时间 -->
      <view class="info-card">
        <view class="info-title">申请信息</view>
        <view class="info-item">
          <text class="label">申请时间</text>
          <text class="value">{{ formatDateTime(leaveStore.currentLeave.created_at) }}</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-area" v-if="!leaveStore.currentLeave.check_time">
        <view class="cancel-btn" @click="cancelLeave">
          取消请假
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-else class="empty-container">
      <text>未找到请假记录</text>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.leave-detail-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.loading-container,
.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400rpx;
  color: #909399;
  font-size: 28rpx;
}

.detail-content {
  padding: 20rpx;
}

.status-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx;
  background-color: #faad14;
  border-radius: 16rpx;
  margin-bottom: 20rpx;

  .status-icon {
    width: 100rpx;
    height: 100rpx;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 48rpx;
    color: #ffffff;
    margin-bottom: 16rpx;
  }

  .status-text {
    font-size: 32rpx;
    font-weight: 600;
    color: #ffffff;
  }
}

.info-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;

  .info-title {
    font-size: 28rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 16rpx;
    padding-bottom: 16rpx;
    border-bottom: 1rpx solid #f0f0f0;
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    padding: 12rpx 0;

    .label {
      font-size: 26rpx;
      color: #909399;
    }

    .value {
      font-size: 26rpx;
      color: #303133;
    }
  }

  .reason {
    font-size: 26rpx;
    color: #606266;
    line-height: 1.6;
  }
}

.action-area {
  padding: 20rpx;

  .cancel-btn {
    width: 100%;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    color: #ff4d4f;
    background-color: #ffffff;
    border: 2rpx solid #ff4d4f;
    border-radius: 16rpx;
  }
}
</style>
