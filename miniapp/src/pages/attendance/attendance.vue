<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAttendanceStore } from '@/stores/attendance'
import { useUserStore } from '@/stores/user'
import { AttendanceStatus, AttendanceStatusText } from '@/api/attendance'
import AttendanceCard from '@/components/AttendanceCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const attendanceStore = useAttendanceStore()
const userStore = useUserStore()

// 页面状态
const loading = ref(true)
const activeTab = ref(0)

// 统计卡片数据
const statistics = computed(() => ({
  total: attendanceStore.totalCount,
  present: attendanceStore.presentCount,
  leave: attendanceStore.leaveCount,
  absent: attendanceStore.absentCount,
  late: attendanceStore.lateCount,
  rate: attendanceStore.presentRate.toFixed(1)
}))

// 考勤列表（按状态筛选）
const filteredAttendances = computed(() => {
  if (activeTab.value === 0) {
    return attendanceStore.attendances
  }
  return attendanceStore.filterByStatus(activeTab.value as AttendanceStatus)
})

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true
  try {
    // 加载考勤列表
    await attendanceStore.fetchMyAttendances({ limit: 100 })

    // 加载统计数据
    if (userStore.userId) {
      await attendanceStore.fetchStatistics(userStore.userId)
    }
  } catch (error) {
    console.error('加载考勤数据失败:', error)
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
 * 跳转到考勤详情
 */
function onAttendanceClick(attendance: any) {
  uni.navigateTo({
    url: `/pages/attendance/attendance?id=${attendance.id}`
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
  <view class="attendance-container">
    <!-- 统计卡片 -->
    <view class="stats-card">
      <view class="stats-header">
        <text class="title">考勤统计</text>
        <text class="rate">{{ statistics.rate }}%</text>
      </view>
      <view class="stats-content">
        <view class="stat-item">
          <view class="stat-value">{{ statistics.present }}</view>
          <view class="stat-label">出勤</view>
        </view>
        <view class="stat-item">
          <view class="stat-value">{{ statistics.leave }}</view>
          <view class="stat-label">请假</view>
        </view>
        <view class="stat-item">
          <view class="stat-value">{{ statistics.absent }}</view>
          <view class="stat-label">缺勤</view>
        </view>
        <view class="stat-item">
          <view class="stat-value">{{ statistics.late }}</view>
          <view class="stat-label">迟到</view>
        </view>
      </view>
      <view class="stats-footer">
        <text class="total">总考勤 {{ statistics.total }} 次</text>
      </view>
    </view>

    <!-- 标签页 -->
    <view class="tabs">
      <view
        v-for="(tab, index) in ['全部', '出勤', '请假', '缺勤', '迟到']"
        :key="index"
        :class="['tab-item', { active: activeTab === index }]"
        @click="switchTab(index)"
      >
        {{ tab }}
      </view>
    </view>

    <!-- 考勤列表 -->
    <view class="attendance-list" v-if="filteredAttendances.length > 0">
      <AttendanceCard
        v-for="attendance in filteredAttendances"
        :key="attendance.id"
        :attendance="attendance"
        @click="onAttendanceClick"
      />
    </view>

    <!-- 空状态 -->
    <EmptyState
      v-else-if="!loading"
      text="暂无考勤记录"
      description="您的考勤记录将显示在这里"
    />
  </view>
</template>

<style lang="scss" scoped>
.attendance-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 40rpx;
}

.stats-card {
  background-color: #ffffff;
  margin: 20rpx;
  border-radius: 16rpx;
  padding: 32rpx;

  .stats-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32rpx;

    .title {
      font-size: 32rpx;
      font-weight: 600;
      color: #303133;
    }

    .rate {
      font-size: 48rpx;
      font-weight: 700;
      color: #52c41a;
    }
  }

  .stats-content {
    display: flex;
    justify-content: space-around;
    padding: 20rpx 0;
    background-color: #fafafa;
    border-radius: 12rpx;
    margin-bottom: 20rpx;

    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;

      .stat-value {
        font-size: 36rpx;
        font-weight: 600;
        color: #303133;
      }

      .stat-label {
        font-size: 24rpx;
        color: #909399;
        margin-top: 8rpx;
      }
    }
  }

  .stats-footer {
    text-align: center;

    .total {
      font-size: 26rpx;
      color: #909399;
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

.attendance-list {
  padding-top: 20rpx;
}
</style>
