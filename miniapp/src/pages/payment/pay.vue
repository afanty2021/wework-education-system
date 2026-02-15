<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { usePaymentStore } from '@/stores/payment'
import { PaymentMethod, PaymentMethodText } from '@/api/payment'

const paymentStore = usePaymentStore()

// 页面状态
const loading = ref(true)
const paying = ref(false)
const paymentId = ref<number>(0)
const selectedMethod = ref<PaymentMethod>(PaymentMethod.WECHAT)

// 支付方式列表
const paymentMethods = [
  { value: PaymentMethod.WECHAT, label: '微信支付', icon: '/static/payment/wechat.png' },
  { value: PaymentMethod.ALIPAY, label: '支付宝', icon: '/static/payment/alipay.png' },
  { value: PaymentMethod.CASH, label: '现金', icon: '/static/payment/cash.png' },
  { value: PaymentMethod.BANK_CARD, label: '银行卡', icon: '/static/payment/bank.png' },
  { value: PaymentMethod.TRANSFER, label: '转账', icon: '/static/payment/transfer.png' }
]

/**
 * 格式化金额
 */
function formatAmount(amount: string | number): string {
  return `¥${Number(amount).toFixed(2)}`
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
 * 选择支付方式
 */
function selectMethod(method: PaymentMethod) {
  selectedMethod.value = method
}

/**
 * 发起支付
 */
async function handlePay() {
  if (paying.value) return

  paying.value = true

  try {
    // 模拟微信支付流程
    // 实际应该调用 PaymentAPI.wechatPay()

    uni.showLoading({
      title: '发起支付中...'
    })

    // 模拟支付延迟
    await new Promise(resolve => setTimeout(resolve, 1500))

    uni.hideLoading()

    // 模拟支付成功
    uni.showToast({
      title: '支付成功',
      icon: 'success'
    })

    // 跳转到详情页
    setTimeout(() => {
      uni.redirectTo({
        url: `/pages/payment/detail?id=${paymentId.value}`
      })
    }, 1500)

  } catch (error) {
    console.error('支付失败:', error)
    uni.hideLoading()
    uni.showToast({
      title: '支付失败',
      icon: 'none'
    })
  } finally {
    paying.value = false
  }
}

/**
 * 返回上一页
 */
function goBack() {
  uni.navigateBack()
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
  <view class="pay-container">
    <!-- 加载中 -->
    <view v-if="loading" class="loading-container">
      <text>加载中...</text>
    </view>

    <!-- 支付内容 -->
    <view v-else-if="paymentStore.currentPayment" class="pay-content">
      <!-- 金额信息 -->
      <view class="amount-area">
        <view class="amount-label">待支付金额</view>
        <view class="amount-value">
          {{ formatAmount(paymentStore.currentPayment.amount) }}
        </view>
        <view class="payment-no">
          缴费单号: {{ paymentStore.currentPayment.payment_no }}
        </view>
      </view>

      <!-- 支付方式选择 -->
      <view class="method-area">
        <view class="method-title">选择支付方式</view>
        <view class="method-list">
          <view
            v-for="method in paymentMethods"
            :key="method.value"
            :class="['method-item', { active: selectedMethod === method.value }]"
            @click="selectMethod(method.value)"
          >
            <view class="method-info">
              <text class="method-label">{{ method.label }}</text>
            </view>
            <view :class="['radio', { checked: selectedMethod === method.value }]">
              <text v-if="selectedMethod === method.value">&#10003;</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 底部操作栏 -->
      <view class="bottom-area">
        <view class="pay-btn" :class="{ disabled: paying }" @click="handlePay">
          {{ paying ? '支付中...' : '确认支付' }}
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
.pay-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
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

.pay-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.amount-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60rpx 40rpx;
  background-color: #ffffff;
  margin-bottom: 20rpx;

  .amount-label {
    font-size: 26rpx;
    color: #909399;
    margin-bottom: 16rpx;
  }

  .amount-value {
    font-size: 72rpx;
    font-weight: 700;
    color: #ff4d4f;
    margin-bottom: 16rpx;
  }

  .payment-no {
    font-size: 24rpx;
    color: #909399;
  }
}

.method-area {
  flex: 1;
  background-color: #ffffff;
  padding: 24rpx;

  .method-title {
    font-size: 28rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 16rpx;
  }

  .method-list {
    display: flex;
    flex-direction: column;
  }

  .method-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24rpx;
    border: 2rpx solid #f0f0f0;
    border-radius: 12rpx;
    margin-bottom: 16rpx;

    &.active {
      border-color: #1890ff;
      background-color: #f0f7ff;
    }

    .method-info {
      .method-label {
        font-size: 28rpx;
        color: #303133;
      }
    }

    .radio {
      width: 40rpx;
      height: 40rpx;
      border-radius: 50%;
      border: 2rpx solid #d9d9d9;
      display: flex;
      justify-content: center;
      align-items: center;

      &.checked {
        border-color: #1890ff;
        background-color: #1890ff;
        color: #ffffff;
        font-size: 24rpx;
      }
    }
  }
}

.bottom-area {
  padding: 20rpx;
  background-color: #ffffff;

  .pay-btn {
    width: 100%;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    color: #ffffff;
    background-color: #1890ff;
    border-radius: 16rpx;

    &.disabled {
      background-color: #ccc;
    }
  }
}
</style>
