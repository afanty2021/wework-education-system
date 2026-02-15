<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  name: string
  avatar?: string
  role?: string
  showArrow?: boolean
}>()

const emit = defineEmits<{
  (e: 'click'): void
}>()

/**
 * 默认头像
 */
const defaultAvatar = '/static/images/default-avatar.png'

/**
 * 头像地址
 */
const avatarUrl = computed(() => props.avatar || defaultAvatar)

/**
 * 点击事件
 */
function onClick() {
  emit('click')
}
</script>

<template>
  <view class="user-card" @click="onClick">
    <!-- 头像 -->
    <image class="avatar" :src="avatarUrl" mode="aspectFill" />

    <!-- 用户信息 -->
    <view class="user-info">
      <view class="name">{{ name }}</view>
      <view class="role" v-if="role">{{ role }}</view>
    </view>

    <!-- 箭头 -->
    <view class="arrow" v-if="showArrow">
      <text class="icon">></text>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.user-card {
  display: flex;
  align-items: center;
  padding: 32rpx;
  background-color: #ffffff;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  margin-right: 24rpx;
  background-color: #f5f5f5;
}

.user-info {
  flex: 1;

  .name {
    font-size: 36rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8rpx;
  }

  .role {
    font-size: 26rpx;
    color: #909399;
  }
}

.arrow {
  .icon {
    font-size: 32rpx;
    color: #c0c4cc;
  }
}
</style>
