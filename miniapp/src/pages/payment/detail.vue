<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePaymentStore } from '@/stores/payment'
import { PaymentStatusText, PaymentMethodText } from '@/api/payment'

const paymentStore = usePaymentStore()

// 页面状态
const loading = ref(true)
const paymentId = ref<number>(0)

/**
 * 格式化金额
 */
function formatAmount(amount: string | number): string {
  return `¥${Number(amount).toFixed(2)}`
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
 * 加载缴费详情
 */
async function loadPaymentDetail() {
  loading.value = true
  try {
    await paymentStore.fetchPaymentDetail(paymentId.value)
  } catch (error) {
    console.error('加载缴费详情失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 跳转到支付页面
 */
function goToPay() {
  uni.navigateTo({
    url: `/pages/payment/pay?id=${paymentId.value}`
  })
}

/**
 * 跳转到缴费记录
 */
function goToHistory() {
  uni.navigateTo({
    url: '/pages/payment/history'
  })
}

onMounted(() => {
  // 获取页面参数
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = currentPage?.options || {}

  if (options.id) {
    paymentId.value = parseInt(options.id)
    loadPaymentDetail()
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
  <view class="payment-detail-container">
    <!-- 加载中 -->
    <view v-if="loading" class="loading-container">
      <text>加载中...</text>
    </view>

    <!-- 缴费详情 -->
    <view v-else-if="paymentStore.currentPayment" class="detail-content">
      <!-- 状态卡片 -->
      <view class="status-card" :class="{ pending: paymentStore.currentPayment.status === 1 }">
        <view class="status-icon">
          <text v-if="paymentStore.currentPayment.status === 1">!</text>
          <text v-else-if="paymentStore.currentPayment.status === 2">&#10003;</text>
          <text v-else>&#8635;</text>
        </view>
        <view class="status-text">
          {{ PaymentStatusText[paymentStore.currentPayment.status as keyof typeof PaymentStatusText] }}
        </view>
      </view>

      <!-- 金额信息 -->
      <view class="amount-card">
        <view class="amount-label">缴费金额</view>
        <view class="amount-value">
          {{ formatAmount(paymentStore.currentPayment.amount) }}
        </view>
        <view class="hours-info" v-if="paymentStore.currentPayment.hours">
          购买课时: {{ paymentStore.currentPayment.hours }}课时
        </view>
      </view>

      <!-- 基本信息 -->
      <view class="info-card">
        <view class="info-title">基本信息</view>
        <view class="info-item">
          <text class="label">缴费单号</text>
          <text class="value">{{ paymentStore.currentPayment.payment_no }}</text>
        </view>
        <view class="info-item">
          <text class="label">支付方式</text>
          <text class="value">
            {{ PaymentMethodText[paymentStore.currentPayment.payment_method as keyof typeof PaymentMethodText] }}
          </text>
        </view>
        <view class="info-item">
          <text class="label">创建时间</text>
          <text class="value">{{ formatDateTime(paymentStore.currentPayment.created_at) }}</text>
        </view>
        <view class="info-item" v-if="paymentStore.currentPayment.payment_time">
          <text class="label">支付时间</text>
          <text class="value">{{ formatDateTime(paymentStore.currentPayment.payment_time) }}</text>
        </view>
      </view>

      <!-- 合同信息 -->
      <view class="info-card" v-if="paymentStore.currentPayment.contract">
        <view class="info-title">合同信息</view>
        <view class="info-item">
          <text class="label">合同编号</text>
          <text class="value">{{ paymentStore.currentPayment.contract.contract_no }}</text>
        </view>
        <view class="info-item">
          <text class="label">课程</text>
          <text class="value">{{ paymentStore.currentPayment.contract.course_name || '课程包' }}</text>
        </view>
        <view class="info-item">
          <text class="label">学员</text>
          <text class="value">{{ paymentStore.currentPayment.contract.student_name || '-' }}</text>
        </view>
      </view>

      <!-- 备注 -->
      <view class="info-card" v-if="paymentStore.currentPayment.remark">
        <view class="info-title">备注</view>
        <view class="remark">{{ paymentStore.currentPayment.remark }}</view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-area" v-if="paymentStore.currentPayment.status === 1">
        <view class="pay-btn" @click="goToPay">
          立即支付
        </view>
      </view>

      <view class="action-area" v-else>
        <view class="history-btn" @click="goToHistory">
          查看缴费记录
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-else class="empty-container">
      <text>未找到缴费记录</text>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.payment-detail-container {
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
  background-color: #52c41a;
  border-radius: 16rpx;
  margin-bottom: 20rpx;

  &.pending {
    background-color: #faad14;
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

.amount-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx;
  background-color: #ffffff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;

  .amount-label {
    font-size: 26rpx;
    color: #909399;
    margin-bottom: 16rpx;
  }

  .amount-value {
    font-size: 64rpx;
    font-weight: 700;
    color: #303133;
    margin-bottom: 16rpx;
  }

  .hours-info {
    font-size: 26rpx;
    color: #606266;
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

  .remark {
    font-size: 26rpx;
    color: #606266;
    line-height: 1.6;
  }
}

.action-area {
  padding: 20rpx;

  .pay-btn {
    width: 100%;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    color: #ffffff;
    background-color: #1890ff;
    border-radius: 16rpx;
  }

  .history-btn {
    width: 100%;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    color: #1890ff;
    background-color: #ffffff;
    border: 2rpx solid #1890ff;
    border-radius: 16rpx;
  }
}
</style>
