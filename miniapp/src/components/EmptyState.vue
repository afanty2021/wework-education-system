<script setup lang="ts">
defineProps<{
  image?: string
  text?: string
  description?: string
  buttonText?: string
}>()

const emit = defineEmits<{
  (e: 'click'): void
}>()

function onButtonClick() {
  emit('click')
}
</script>

<template>
  <view class="empty-state">
    <!-- 空状态图片 -->
    <image
      v-if="image"
      :src="image"
      class="empty-image"
      mode="aspectFit"
    />

    <!-- 默认空状态图片 -->
    <image
      v-else
      src="/static/images/empty.png"
      class="empty-image"
      mode="aspectFit"
    />

    <!-- 标题文本 -->
    <view class="empty-text">{{ text || '暂无数据' }}</view>

    <!-- 描述文本 -->
    <view class="empty-description" v-if="description">
      {{ description }}
    </view>

    <!-- 操作按钮 -->
    <view class="empty-button" v-if="buttonText" @click="onButtonClick">
      {{ buttonText }}
    </view>
  </view>
</template>

<style lang="scss" scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 40rpx;
}

.empty-image {
  width: 300rpx;
  height: 300rpx;
  margin-bottom: 32rpx;
}

.empty-text {
  font-size: 32rpx;
  color: #303133;
  font-weight: 500;
  margin-bottom: 16rpx;
}

.empty-description {
  font-size: 28rpx;
  color: #909399;
  text-align: center;
  margin-bottom: 32rpx;
}

.empty-button {
  font-size: 30rpx;
  color: #1890ff;
  padding: 20rpx 60rpx;
  border: 2rpx solid #1890ff;
  border-radius: 8rpx;
}
</style>
