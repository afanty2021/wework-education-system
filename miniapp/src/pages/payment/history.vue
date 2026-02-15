<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePaymentStore } from '@/stores/payment'
import type { Payment } from '@/api/payment'
import PaymentCard from '@/components/PaymentCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const paymentStore = usePaymentStore()

// 页面状态
const loading = ref(true)

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true
  try {
    // 获取已缴费记录
    await paymentStore.fetchConfirmedPayments()
  } catch (error) {
    console.error('加载缴费记录失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 跳转到详情
 */
function onPaymentClick(payment: Payment) {
  uni.navigateTo({
    url: `/pages/payment/detail?id=${payment.id}`
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
  <view class="history-container">
    <!-- 缴费列表 -->
    <view class="history-list" v-if="paymentStore.confirmedPayments.length > 0">
      <PaymentCard
        v-for="payment in paymentStore.confirmedPayments"
        :key="payment.id"
        :payment="payment"
        :show-contract="true"
        @click="onPaymentClick"
      />
    </view>

    <!-- 空状态 -->
    <EmptyState
      v-else-if="!loading"
      text="暂无缴费记录"
      description="您还没有任何缴费记录"
    />
  </view>
</template>

<style lang="scss" scoped>
.history-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 40rpx;
}

.history-list {
  padding-top: 20rpx;
}
</style>
