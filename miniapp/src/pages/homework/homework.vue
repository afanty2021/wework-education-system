<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useHomeworkStore } from '@/stores/homework'
import { HomeworkSubmitStatus, HomeworkSubmitStatusText } from '@/api/homework'
import HomeworkCard from '@/components/HomeworkCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const homeworkStore = useHomeworkStore()

// 页面状态
const loading = ref(true)
const activeTab = ref(0)

// 标签页配置
const tabs = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待提交' },
  { key: 'submitted', label: '已提交' },
  { key: 'graded', label: '已批改' }
]

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true
  try {
    await homeworkStore.fetchMyHomeworks({ limit: 100 })
  } catch (error) {
    console.error('加载作业数据失败:', error)
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
 * 获取筛选后的作业列表
 */
const filteredHomeworks = computed(() => {
  const homeworks = homeworkStore.homeworks

  switch (activeTab.value) {
    case 0: // 全部
      return homeworks
    case 1: // 待提交
      return homeworks.filter(h => !h.submission || h.submission.score === null)
    case 2: // 已提交
      return homeworks.filter(h => h.submission && h.submission.score === null)
    case 3: // 已批改
      return homeworks.filter(h => h.submission && h.submission.score !== null)
    default:
      return homeworks
  }
})

/**
 * 跳转到作业详情
 */
function onHomeworkClick(homework: any) {
  uni.navigateTo({
    url: `/pages/homework/detail?id=${homework.id}`
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
  <view class="homework-container">
    <!-- 统计信息 -->
    <view class="stats-bar">
      <view class="stat-item">
        <text class="stat-value">{{ homeworkStore.totalCount }}</text>
        <text class="stat-label">全部作业</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ homeworkStore.pendingCount }}</text>
        <text class="stat-label">待提交</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ homeworkStore.submittedCount }}</text>
        <text class="stat-label">已批改</text>
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
        <view class="tab-badge" v-if="index === 1 && homeworkStore.pendingCount > 0">
          {{ homeworkStore.pendingCount }}
        </view>
      </view>
    </view>

    <!-- 作业列表 -->
    <view class="homework-list" v-if="filteredHomeworks.length > 0">
      <HomeworkCard
        v-for="homework in filteredHomeworks"
        :key="homework.id"
        :homework="homework"
        @click="onHomeworkClick"
      />
    </view>

    <!-- 空状态 -->
    <EmptyState
      v-else-if="!loading"
      text="暂无作业"
      description="暂时没有需要完成的作业"
    />
  </view>
</template>

<style lang="scss" scoped>
.homework-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 40rpx;
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

    .tab-badge {
      position: absolute;
      top: 10rpx;
      right: 20rpx;
      min-width: 32rpx;
      height: 32rpx;
      line-height: 32rpx;
      text-align: center;
      font-size: 20rpx;
      color: #ffffff;
      background-color: #ff4d4f;
      border-radius: 16rpx;
      padding: 0 6rpx;
    }
  }
}

.homework-list {
  padding-top: 20rpx;
}
</style>
