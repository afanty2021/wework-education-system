<script setup lang="ts">
import { ref, computed } from 'vue'

/**
 * TabBar配置项
 */
interface TabBarItem {
  pagePath: string
  text: string
  iconPath?: string
  selectedIconPath?: string
  badge?: string | number
}

const props = defineProps<{
  current: number
  list: TabBarItem[]
}>()

const emit = defineEmits<{
  (e: 'change', index: number): void
}>()

/**
 * Tab点击事件
 */
function onTabClick(index: number) {
  emit('change', index)
}

/**
 * 获取图标路径
 */
function getIconPath(item: TabBarItem, isSelected: boolean): string {
  return isSelected && item.selectedIconPath ? item.selectedIconPath : item.iconPath || ''
}
</script>

<template>
  <view class="custom-tabbar">
    <view
      v-for="(item, index) in list"
      :key="index"
      class="tabbar-item"
      @click="onTabClick(index)"
    >
      <image
        v-if="item.iconPath || item.selectedIconPath"
        :src="getIconPath(item, current === index)"
        class="tabbar-icon"
        mode="aspectFit"
      />
      <text :class="['tabbar-text', { active: current === index }]">
        {{ item.text }}
      </text>
      <view v-if="item.badge" class="tabbar-badge">
        {{ item.badge }}
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.custom-tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 100rpx;
  background-color: #ffffff;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 999;
}

.tabbar-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
  padding: 10rpx 0;
}

.tabbar-icon {
  width: 48rpx;
  height: 48rpx;
  margin-bottom: 6rpx;
}

.tabbar-text {
  font-size: 22rpx;
  color: #999999;
  transition: color 0.2s;

  &.active {
    color: #1890ff;
    font-weight: 500;
  }
}

.tabbar-badge {
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
  padding: 0 8rpx;
}
</style>
