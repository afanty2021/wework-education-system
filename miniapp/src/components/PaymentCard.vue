<script setup lang="ts">
import { computed } from 'vue'
import type { Payment } from '@/api/payment'
import { PaymentStatusText, PaymentMethodText } from '@/api/payment'

const props = defineProps<{
  payment: Payment
  showContract?: boolean
}>()

const emit = defineEmits<{
  (e: 'click', payment: Payment): void
  (e: 'pay', payment: Payment): void
}>()

/**
 * 状态颜色映射
 */
const statusColorMap: Record<number, string> = {
  1: '#faad14',  // 待确认 - 黄色
  2: '#52c41a',  // 已确认 - 绿色
  3: '#ff4d4f'   // 已退款 - 红色
}

/**
 * 状态颜色
 */
const statusColor = computed(() => statusColorMap[props.payment.status] || '#999999')

/**
 * 状态文本
 */
const statusText = computed(() => PaymentStatusText[props.payment.status as keyof typeof PaymentStatusText] || '')

/**
 * 支付方式文本
 */
const paymentMethodText = computed(() => {
  return PaymentMethodText[props.payment.payment_method as keyof typeof PaymentMethodText] || ''
})

/**
 * 格式化金额
 */
function formatAmount(amount: string | number): string {
  return `¥${Number(amount).toFixed(2)}`
}

/**
 * 格式化日期
 */
function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * 点击卡片
 */
function onCardClick() {
  emit('click', props.payment)
}

/**
 * 立即支付
 */
function onPay() {
  emit('pay', props.payment)
}
</script>

<template>
  <view class="payment-card" @click="onCardClick">
    <!-- 头部信息 -->
    <view class="card-header">
      <view class="payment-no">缴费单号: {{ payment.payment_no }}</view>
      <view class="status-tag" :style="{ backgroundColor: statusColor }">
        {{ statusText }}
      </view>
    </view>

    <!-- 金额信息 -->
    <view class="amount-area">
      <view class="amount">{{ formatAmount(payment.amount) }}</view>
      <view class="hours" v-if="payment.hours">
        购买课时: {{ payment.hours }}课时
      </view>
    </view>

    <!-- 合同信息 -->
    <view class="contract-info" v-if="showContract && payment.contract">
      <view class="contract-name">
        {{ payment.contract.course_name || '课程包' }}
      </view>
      <view class="contract-detail">
        合同编号: {{ payment.contract.contract_no }}
      </view>
    </view>

    <!-- 支付信息 -->
    <view class="payment-info">
      <view class="payment-method">{{ paymentMethodText }}</view>
      <view class="payment-date" v-if="payment.payment_time">
        {{ formatDate(payment.payment_time) }}
      </view>
      <view class="payment-date" v-else>
        {{ formatDate(payment.created_at) }}
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-area" v-if="payment.status === 1">
      <view class="pay-btn" @click.stop="onPay">
        立即支付
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.payment-card {
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

  .payment-no {
    font-size: 26rpx;
    color: #909399;
  }

  .status-tag {
    font-size: 22rpx;
    color: #ffffff;
    padding: 6rpx 16rpx;
    border-radius: 6rpx;
  }
}

.amount-area {
  display: flex;
  flex-direction: column;
  margin-bottom: 16rpx;

  .amount {
    font-size: 48rpx;
    font-weight: 700;
    color: #303133;
    margin-bottom: 8rpx;
  }

  .hours {
    font-size: 26rpx;
    color: #606266;
  }
}

.contract-info {
  padding: 16rpx 0;
  border-top: 1rpx solid #f0f0f0;
  border-bottom: 1rpx solid #f0f0f0;
  margin-bottom: 16rpx;

  .contract-name {
    font-size: 28rpx;
    font-weight: 500;
    color: #303133;
    margin-bottom: 8rpx;
  }

  .contract-detail {
    font-size: 24rpx;
    color: #909399;
  }
}

.payment-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24rpx;
  color: #909399;
}

.action-area {
  display: flex;
  justify-content: flex-end;
  margin-top: 16rpx;

  .pay-btn {
    font-size: 26rpx;
    color: #ffffff;
    background-color: #1890ff;
    padding: 12rpx 32rpx;
    border-radius: 8rpx;
  }
}
</style>
