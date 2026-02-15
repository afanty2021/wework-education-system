<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLeaveChangeStore } from '@/stores/leavechange'

const leaveChangeStore = useLeaveChangeStore()

// 页面状态
const loading = ref(true)
const leaveChangeId = ref<number>(0)

/**
 * 加载调课详情
 */
async function loadLeaveChangeDetail() {
  loading.value = true
  try {
    await leaveChangeStore.fetchLeaveChangeDetail(leaveChangeId.value)
  } catch (error) {
    console.error('加载调课详情失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 取消调课申请
 */
function cancelLeaveChange() {
  uni.showModal({
    title: '提示',
    content: '确定要取消该调课申请吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await leaveChangeStore.cancelLeaveChange(leaveChangeId.value)
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
    leaveChangeId.value = parseInt(options.id)
    loadLeaveChangeDetail()
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
  <view class="leavechange-detail-container">
    <!-- 加载中 -->
    <view v-if="loading" class="loading-container">
      <text>加载中...</text>
    </view>

    <!-- 空状态 -->
    <view v-else-if="!leaveChangeStore.currentLeaveChange" class="empty-container">
      <text>未找到调课记录</text>
    </view>

    <!-- 调课详情 -->
    <view v-else class="detail-content">
      <!-- 状态卡片 -->
      <view class="status-card" :class="{
        pending: leaveChangeStore.currentLeaveChange.status === 1,
        approved: leaveChangeStore.currentLeaveChange.status === 2,
        rejected: leaveChangeStore.currentLeaveChange.status === 3
      }">
        <view class="status-icon">
          <text v-if="leaveChangeStore.currentLeaveChange.status === 1">!</text>
          <text v-else-if="leaveChangeStore.currentLeaveChange.status === 2">&#10003;</text>
          <text v-else>&#10005;</text>
        </view>
        <view class="status-text">
          {{ leaveChangeStore.currentLeaveChange.status === 1 ? '待审核' :
             leaveChangeStore.currentLeaveChange.status === 2 ? '已通过' : '已拒绝' }}
        </view>
      </view>

      <!-- 原课程信息 -->
      <view class="info-card" v-if="leaveChangeStore.currentLeaveChange.original_schedule">
        <view class="info-title">原课程</view>
        <view class="info-item">
          <text class="label">课程名称</text>
          <text class="value">{{ leaveChangeStore.currentLeaveChange.original_schedule.course_name || '课程' }}</text>
        </view>
        <view class="info-item">
          <text class="label">上课时间</text>
          <text class="value">
            {{ leaveChangeStore.currentLeaveChange.original_schedule.start_time.replace('T', ' ').slice(0, 16) }}
          </text>
        </view>
      </view>

      <!-- 目标课程信息 -->
      <view class="info-card">
        <view class="info-title">目标课程</view>
        <view class="info-item" v-if="leaveChangeStore.currentLeaveChange.target_date">
          <text class="label">希望日期</text>
          <text class="value">{{ leaveChangeStore.currentLeaveChange.target_date }}</text>
        </view>
        <view class="info-item" v-else-if="leaveChangeStore.currentLeaveChange.target_schedule">
          <text class="label">课程名称</text>
          <text class="value">{{ leaveChangeStore.currentLeaveChange.target_schedule.course_name || '课程' }}</text>
        </view>
        <view class="info-item" v-else>
          <text class="label">目标课程</text>
          <text class="value">待安排</text>
        </view>
      </view>

      <!-- 调课原因 -->
      <view class="info-card">
        <view class="info-title">调课原因</view>
        <view class="reason">{{ leaveChangeStore.currentLeaveChange.reason }}</view>
      </view>

      <!-- 拒绝原因 -->
      <view class="info-card" v-if="leaveChangeStore.currentLeaveChange.status === 3 && leaveChangeStore.currentLeaveChange.reject_reason">
        <view class="info-title">拒绝原因</view>
        <view class="reason reject">{{ leaveChangeStore.currentLeaveChange.reject_reason }}</view>
      </view>

      <!-- 申请时间 -->
      <view class="info-card">
        <view class="info-title">申请信息</view>
        <view class="info-item">
          <text class="label">申请时间</text>
          <text class="value">
            {{ new Date(leaveChangeStore.currentLeaveChange.created_at).toLocaleString('zh-CN') }}
          </text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-area" v-if="leaveChangeStore.currentLeaveChange.status === 1">
        <view class="cancel-btn" @click="cancelLeaveChange">
          取消申请
        </view>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.leavechange-detail-container {
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
  border-radius: 16rpx;
  margin-bottom: 20rpx;

  &.pending {
    background-color: #faad14;
  }

  &.approved {
    background-color: #52c41a;
  }

  &.rejected {
    background-color: #ff4d4f;
  }

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

    &.reject {
      color: #ff4d4f;
    }
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
