<script setup lang="ts">
import { computed } from 'vue'
import type { Contract } from '@/api/payment'

const props = defineProps<{
  contract: Contract
}>()

const emit = defineEmits<{
  (e: 'click', contract: Contract): void
  (e: 'pay', contract: Contract): void
}>()

/**
 * 合同状态映射
 */
const contractStatusMap: Record<number, { text: string; color: string }> = {
  1: { text: '生效中', color: '#52c41a' },
  2: { text: '已完结', color: '#1890ff' },
  3: { text: '已退费', color: '#ff4d4f' },
  4: { text: '已过期', color: '#909399' }
}

/**
 * 状态信息
 */
const statusInfo = computed(() => {
  return contractStatusMap[props.contract.status] || { text: '未知', color: '#999999' }
})

/**
 * 剩余课时百分比
 */
const remainingPercent = computed(() => {
  if (props.contract.total_hours === 0) return 0
  return Math.round((props.contract.remaining_hours / props.contract.total_hours) * 100)
})

/**
 * 剩余课时颜色
 */
const remainingColor = computed(() => {
  if (remainingPercent.value > 50) return '#52c41a'
  if (remainingPercent.value > 20) return '#faad14'
  return '#ff4d4f'
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
  emit('click', props.contract)
}

/**
 * 立即缴费
 */
function onPay() {
  emit('pay', props.contract)
}
</script>

<template>
  <view class="contract-card" @click="onCardClick">
    <!-- 头部信息 -->
    <view class="card-header">
      <view class="contract-no">合同编号: {{ contract.contract_no }}</view>
      <view class="status-tag" :style="{ backgroundColor: statusInfo.color }">
        {{ statusInfo.text }}
      </view>
    </view>

    <!-- 课程信息 -->
    <view class="course-info">
      <view class="course-name">{{ contract.course_name || '课程包' }}</view>
      <view class="student-name" v-if="contract.student_name">
        学员: {{ contract.student_name }}
      </view>
    </view>

    <!-- 课时信息 -->
    <view class="hours-area">
      <view class="hours-item">
        <view class="hours-value">{{ contract.total_hours }}</view>
        <view class="hours-label">总课时</view>
      </view>
      <view class="hours-item">
        <view class="hours-value" :style="{ color: remainingColor }">{{ contract.remaining_hours }}</view>
        <view class="hours-label">剩余课时</view>
      </view>
      <view class="hours-item">
        <view class="hours-value">{{ remainingPercent }}%</view>
        <view class="hours-label">使用进度</view>
      </view>
    </view>

    <!-- 进度条 -->
    <view class="progress-area">
      <view class="progress-bar">
        <view
          class="progress-fill"
          :style="{ width: `${remainingPercent}%`, backgroundColor: remainingColor }"
        ></view>
      </view>
    </view>

    <!-- 金额信息 -->
    <view class="amount-area">
      <view class="amount-item">
        <text class="label">合同金额：</text>
        <text class="value">{{ formatAmount(contract.total_amount) }}</text>
      </view>
      <view class="amount-item">
        <text class="label">已缴金额：</text>
        <text class="value">{{ formatAmount(contract.paid_amount) }}</text>
      </view>
    </view>

    <!-- 有效期 -->
    <view class="validity-area">
      <text class="label">有效期：</text>
      <text class="value">{{ formatDate(contract.start_date) }} - {{ formatDate(contract.end_date) }}</text>
    </view>

    <!-- 操作按钮 -->
    <view class="action-area">
      <view class="pay-btn" @click.stop="onPay">
        立即缴费
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.contract-card {
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

  .contract-no {
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

.course-info {
  margin-bottom: 16rpx;

  .course-name {
    font-size: 32rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8rpx;
  }

  .student-name {
    font-size: 26rpx;
    color: #606266;
  }
}

.hours-area {
  display: flex;
  justify-content: space-around;
  padding: 16rpx 0;
  margin-bottom: 16rpx;
  border-top: 1rpx solid #f0f0f0;
  border-bottom: 1rpx solid #f0f0f0;

  .hours-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .hours-value {
      font-size: 36rpx;
      font-weight: 700;
      color: #303133;
    }

    .hours-label {
      font-size: 24rpx;
      color: #909399;
      margin-top: 4rpx;
    }
  }
}

.progress-area {
  margin-bottom: 16rpx;

  .progress-bar {
    height: 12rpx;
    background-color: #f0f0f0;
    border-radius: 6rpx;
    overflow: hidden;

    .progress-fill {
      height: 100%;
      border-radius: 6rpx;
      transition: width 0.3s ease;
    }
  }
}

.amount-area {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12rpx;

  .amount-item {
    font-size: 26rpx;

    .label {
      color: #909399;
    }

    .value {
      color: #303133;
      font-weight: 500;
    }
  }
}

.validity-area {
  font-size: 24rpx;
  color: #909399;
  margin-bottom: 16rpx;
}

.action-area {
  display: flex;
  justify-content: flex-end;

  .pay-btn {
    font-size: 26rpx;
    color: #ffffff;
    background-color: #1890ff;
    padding: 12rpx 32rpx;
    border-radius: 8rpx;
  }
}
</style>
