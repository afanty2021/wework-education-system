<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'

/**
 * 应用启动时执行
 */
onLaunch(() => {
  console.log('App Launch')

  // 初始化应用
  const appStore = useAppStore()
  appStore.initApp()

  // 检查登录状态
  const userStore = useUserStore()
  userStore.checkLoginStatus()
})

/**
 * 应用显示时执行
 */
onShow(() => {
  console.log('App Show')
})

/**
 * 应用隐藏时执行
 */
onHide(() => {
  console.log('App Hide')
})

/**
 * 错误处理
 */
export function handleError(error: Error) {
  console.error('应用错误:', error)
  uni.showToast({
    title: '应用出现错误',
    icon: 'none'
  })
}
</script>

<style lang="scss">
@import 'uview-plus/index.scss';

/* 全局样式 */
page {
  background-color: #f5f7fa;
  font-size: 28rpx;
  color: #303133;
}

/* 通用样式 */
.container {
  padding: 20rpx;
}

/* 卡片样式 */
.card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.08);
}

/* 文本溢出省略 */
.text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.text-ellipsis-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

/* Flex布局辅助类 */
.flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.flex-wrap {
  flex-wrap: wrap;
}

.justify-center {
  justify-content: center;
}

.justify-between {
  justify-content: space-between;
}

.justify-around {
  justify-content: space-around;
}

.align-center {
  align-items: center;
}

.align-start {
  align-items: flex-start;
}

/* 间距辅助类 */
.m-20 {
  margin: 20rpx;
}

.mt-20 {
  margin-top: 20rpx;
}

.mb-20 {
  margin-bottom: 20rpx;
}

.ml-20 {
  margin-left: 20rpx;
}

.mr-20 {
  margin-right: 20rpx;
}

.p-20 {
  padding: 20rpx;
}

.p-30 {
  padding: 30rpx;
}

/* 字体大小辅助类 */
.text-sm {
  font-size: 24rpx;
}

.text-base {
  font-size: 28rpx;
}

.text-lg {
  font-size: 32rpx;
}

.text-xl {
  font-size: 36rpx;
}

/* 字体颜色辅助类 */
.text-primary {
  color: #1890ff;
}

.text-success {
  color: #52c41a;
}

.text-warning {
  color: #faad14;
}

.text-error {
  color: #ff4d4f;
}

.text-muted {
  color: #909399;
}

/* 徽章样式 */
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4rpx 12rpx;
  font-size: 20rpx;
  border-radius: 20rpx;
}

.badge-primary {
  background-color: #e6f7ff;
  color: #1890ff;
}

.badge-success {
  background-color: #f6ffed;
  color: #52c41a;
}

.badge-warning {
  background-color: #fffbe6;
  color: #faad14;
}

.badge-error {
  background-color: #fff2f0;
  color: #ff4d4f;
}

/* 分割线 */
.divider {
  height: 1rpx;
  background-color: #e4e7ed;
  margin: 20rpx 0;
}

/* 安全区域 */
.safe-area-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
