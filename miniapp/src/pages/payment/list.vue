<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { usePaymentStore } from '@/stores/payment'
import type { Payment } from '@/api/payment'
import PaymentCard from '@/components/PaymentCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const paymentStore = usePaymentStore()

// 页面状态
const loading = ref(true)
const activeTab = ref(0)

// 标签页配置
const tabs = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待缴费' },
  { key: 'confirmed', label: '已缴费' },
  { key: 'refunded', label: '已退款' }
]

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true
  try {
    await paymentStore.fetchPayments({ limit: 100 })
  } catch (error) {
    console.error('加载缴费数据失败:', error)
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
 * 获取筛选后的缴费列表
 */
const filteredPayments = computed(() => {
  const payments = paymentStore.payments

  switch (activeTab.value) {
    case 0: // 全部
      return payments
    case 1: // 待缴费
      return paymentStore.pendingPayments
    case 2: // 已缴费
      return paymentStore.confirmedPayments
    case 3: // 已退款
      return paymentStore.refundedPayments
    default:
      return payments
  }
})

/**
 * 跳转到缴费详情
 */
function onPaymentClick(payment: Payment) {
  uni.navigateTo({
    url: `/pages/payment/detail?id=${payment.id}`
  })
}

/**
 * 跳转到支付页面
 */
function onPayClick(payment: Payment) {
  uni.navigateTo({
    url: `/pages/payment/pay?id=${payment.id}`
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
  <view class="payment-container">
    <!-- 统计信息 -->
    <view class="stats-bar">
      <view class="stat-item">
        <text class="stat-value">{{ paymentStore.stats.total_pending }}</text>
        <text class="stat-label">待缴费</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ paymentStore.stats.total_confirmed }}</text>
        <text class="stat-label">已缴费</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">¥{{ paymentStore.totalPendingAmount.toFixed(2) }}</text>
        <text class="stat-label">待缴金额</text>
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

    <!-- 缴费列表 -->
    <view class="payment-list" v-if="filteredPayments.length > 0">
      <PaymentCard
        v-for="payment in filteredPayments"
        :key="payment.id"
        :payment="payment"
        :show-contract="true"
        @click="onPaymentClick"
        @pay="onPayClick"
      />
    </view>

    <!-- 空状态 -->
    <EmptyState
      v-else-if="!loading"
      text="暂无缴费记录"
      description="暂时没有需要处理的缴费"
    />
  </view>
</template>

<style lang="scss" scoped>
.payment-container {
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
  }
}

.payment-list {
  padding-top: 20rpx;
}
</style>
