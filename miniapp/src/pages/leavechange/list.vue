<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useLeaveChangeStore } from '@/stores/leavechange'
import type { LeaveChange } from '@/api/leavechange'
import LeaveChangeCard from '@/components/LeaveChangeCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const leaveChangeStore = useLeaveChangeStore()

// 页面状态
const loading = ref(true)
const activeTab = ref(0)

// 标签页配置
const tabs = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待审核' },
  { key: 'approved', label: '已通过' },
  { key: 'rejected', label: '已拒绝' }
]

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true
  try {
    await leaveChangeStore.fetchLeaveChanges({ limit: 100 })
  } catch (error) {
    console.error('加载调课数据失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 切换标签
 */
function switchTab(index: number) {
  activeTab.value = index
}

/**
 * 获取筛选后的调课列表
 */
const filteredLeaveChanges = computed(() => {
  const leaveChanges = leaveChangeStore.leaveChanges

  switch (activeTab.value) {
    case 0: // 全部
      return leaveChanges
    case 1: // 待审核
      return leaveChangeStore.pendingLeaveChanges
    case 2: // 已通过
      return leaveChangeStore.approvedLeaveChanges
    case 3: // 已拒绝
      return leaveChangeStore.rejectedLeaveChanges
    default:
      return leaveChanges
  }
})

/**
 * 跳转到调课详情
 */
function onLeaveChangeClick(leaveChange: LeaveChange) {
  uni.navigateTo({
    url: `/pages/leavechange/detail?id=${leaveChange.id}`
  })
}

/**
 * 取消调课
 */
async function onCancelLeaveChange(leaveChange: LeaveChange) {
  uni.showModal({
    title: '提示',
    content: '确定要取消该调课申请吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await leaveChangeStore.cancelLeaveChange(leaveChange.id)
          uni.showToast({
            title: '取消成功',
            icon: 'success'
          })
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

/**
 * 跳转到申请调课
 */
function goToApply() {
  uni.navigateTo({
    url: '/pages/leavechange/apply'
  })
}

/**
 * 下拉刷新
 */
async function onPullDownRefresh() {
  await initPage()
  uni.stopPullDownRefresh()
}

onMounted(() => {
  initPage()
})
</script>

<template>
  <view class="leavechange-container">
    <!-- 统计信息 -->
    <view class="stats-bar">
      <view class="stat-item">
        <text class="stat-value">{{ leaveChangeStore.stats.total }}</text>
        <text class="stat-label">全部调课</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ leaveChangeStore.stats.pending }}</text>
        <text class="stat-label">待审核</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ leaveChangeStore.stats.approved }}</text>
        <text class="stat-label">已通过</text>
      </view>
    </view>

    <!-- 标签页 -->
    <view class="tabs">
      <view
        v-for="(tab, index) in tabs"
        :key="tab.key"
        :class="['tab-item', { active: activeTab === index }]"
        @click="switchTab(index)"
      >
        {{ tab.label }}
      </view>
    </view>

    <!-- 调课列表 -->
    <view class="leavechange-list" v-if="filteredLeaveChanges.length > 0">
      <LeaveChangeCard
        v-for="leaveChange in filteredLeaveChanges"
        :key="leaveChange.id"
        :leave-change="leaveChange"
        @click="onLeaveChangeClick"
        @cancel="onCancelLeaveChange"
      />
    </view>

    <!-- 空状态 -->
    <EmptyState
      v-else-if="!loading"
      text="暂无调课记录"
      description="暂时没有调课记录"
    />

    <!-- 申请调课按钮 -->
    <view class="fab-button" @click="goToApply">
      <text class="icon">+</text>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.leavechange-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 120rpx;
}

.stats-bar {
  display: flex;
  justify-content: space-around;
  padding: 30rpx;
  margin: 20rpx;
  background-color: #ffffff;
  border-radius: 16rpx;

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .stat-value {
      font-size: 40rpx;
      font-weight: 700;
      color: #303133;
    }

    .stat-label {
      font-size: 24rpx;
      color: #909399;
      margin-top: 8rpx;
    }
  }
}

.tabs {
  display: flex;
  padding: 20rpx 30rpx;
  background-color: #ffffff;
  border-bottom: 2rpx solid #f0f0f0;

  .tab-item {
    flex: 1;
    text-align: center;
    padding: 20rpx 0;
    font-size: 28rpx;
    color: #909399;
    position: relative;

    &.active {
      color: #1890ff;
      font-weight: 500;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 48rpx;
        height: 6rpx;
        background-color: #1890ff;
        border-radius: 3rpx;
      }
    }
  }
}

.leavechange-list {
  padding-top: 20rpx;
}

.fab-button {
  position: fixed;
  right: 40rpx;
  bottom: 60rpx;
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  background-color: #1890ff;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4rpx 20rpx rgba(24, 144, 255, 0.4);

  .icon {
    font-size: 60rpx;
    color: #ffffff;
    font-weight: 300;
  }
}
</style>
