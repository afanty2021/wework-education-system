<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

// 菜单列表
const menuItems = [
  { id: 'info', title: '个人信息', icon: 'user', url: '' },
  { id: 'bind', title: '绑定管理', icon: 'link', url: '' },
  { id: 'notification', title: '消息设置', icon: 'bell', url: '' },
  { id: 'help', title: '帮助中心', icon: 'question', url: '' },
  { id: 'about', title: '关于我们', icon: 'info', url: '' },
  { id: 'feedback', title: '意见反馈', icon: 'chat', url: '' }
]

/**
 * 跳转到编辑个人信息
 */
function navigateToEditProfile() {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

/**
 * 点击菜单项
 */
function onMenuClick(menuId: string) {
  switch (menuId) {
    case 'info':
      navigateToEditProfile()
      break
    case 'bind':
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      })
      break
    case 'notification':
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      })
      break
    case 'help':
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      })
      break
    case 'about':
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      })
      break
    case 'feedback':
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      })
      break
  }
}

/**
 * 退出登录
 */
function onLogout() {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        router.push('/pages/login/login')
      }
    }
  })
}

/**
 * 获取角色文本
 */
const roleText = computed(() => {
  const roleMap: Record<string, string> = {
    student: '学员',
    parent: '家长',
    teacher: '教师',
    manager: '管理员',
    admin: '管理员'
  }
  return roleMap[userStore.userRole] || '用户'
})
</script>

<template>
  <view class="profile-container">
    <!-- 用户信息头部 -->
    <view class="user-header" @click="navigateToEditProfile">
      <image class="avatar" :src="userStore.userAvatar" mode="aspectFill" />
      <view class="user-info">
        <view class="name">{{ userStore.userName }}</view>
        <view class="role-badge">{{ roleText }}</view>
      </view>
      <view class="edit-icon">></view>
    </view>

    <!-- 统计信息 -->
    <view class="stats-bar">
      <view class="stat-item">
        <text class="value">0</text>
        <text class="label">课程数</text>
      </view>
      <view class="stat-item">
        <text class="value">0</text>
        <text class="label">作业数</text>
      </view>
      <view class="stat-item">
        <text class="value">0%</text>
        <text class="label">出勤率</text>
      </view>
    </view>

    <!-- 快捷功能 -->
    <view class="quick-actions">
      <view class="action-item">
        <view class="icon homework">作</view>
        <text class="label">我的作业</text>
      </view>
      <view class="action-item">
        <view class="icon schedule">课</view>
        <text class="label">我的课表</text>
      </view>
      <view class="action-item">
        <view class="icon attendance">考</view>
        <text class="label">考勤记录</text>
      </view>
      <view class="action-item">
        <view class="icon contract">合</view>
        <text class="label">我的合同</text>
      </view>
    </view>

    <!-- 菜单列表 -->
    <view class="menu-list">
      <view
        v-for="item in menuItems"
        :key="item.id"
        class="menu-item"
        @click="onMenuClick(item.id)"
      >
        <view class="menu-left">
          <view class="menu-icon">{{ item.icon }}</view>
          <text class="menu-title">{{ item.title }}</text>
        </view>
        <view class="menu-right">
          <text class="arrow">></text>
        </view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-btn" @click="onLogout">
      退出登录
    </view>
  </view>
</template>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 60rpx;
}

.user-header {
  display: flex;
  align-items: center;
  padding: 40rpx 30rpx;
  background-color: #ffffff;

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
      margin-bottom: 12rpx;
    }

    .role-badge {
      display: inline-block;
      padding: 6rpx 16rpx;
      font-size: 24rpx;
      color: #1890ff;
      background-color: #e6f7ff;
      border-radius: 6rpx;
    }
  }

  .edit-icon {
    font-size: 32rpx;
    color: #c0c4cc;
  }
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

    .value {
      font-size: 40rpx;
      font-weight: 700;
      color: #303133;
    }

    .label {
      font-size: 24rpx;
      color: #909399;
      margin-top: 8rpx;
    }
  }
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  padding: 10rpx;
  margin: 0 20rpx;
  background-color: #ffffff;
  border-radius: 16rpx;

  .action-item {
    width: 25%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx 0;

    .icon {
      width: 80rpx;
      height: 80rpx;
      line-height: 80rpx;
      text-align: center;
      border-radius: 20rpx;
      font-size: 32rpx;
      font-weight: 600;
      color: #ffffff;
      margin-bottom: 12rpx;

      &.homework {
        background: linear-gradient(135deg, #52c41a, #389e0d);
      }

      &.schedule {
        background: linear-gradient(135deg, #1890ff, #096dd9);
      }

      &.attendance {
        background: linear-gradient(135deg, #faad14, #d48806);
      }

      &.contract {
        background: linear-gradient(135deg, #722ed1, #531dab);
      }
    }

    .label {
      font-size: 24rpx;
      color: #606266;
    }
  }
}

.menu-list {
  margin: 20rpx;
  background-color: #ffffff;
  border-radius: 16rpx;

  .menu-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 32rpx;
    border-bottom: 2rpx solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }

    .menu-left {
      display: flex;
      align-items: center;

      .menu-icon {
        width: 48rpx;
        height: 48rpx;
        line-height: 48rpx;
        text-align: center;
        background-color: #f5f5f5;
        border-radius: 8rpx;
        margin-right: 20rpx;
        font-size: 24rpx;
      }

      .menu-title {
        font-size: 30rpx;
        color: #303133;
      }
    }

    .menu-right {
      .arrow {
        font-size: 32rpx;
        color: #c0c4cc;
      }
    }
  }
}

.logout-btn {
  margin: 60rpx 20rpx;
  padding: 32rpx;
  text-align: center;
  font-size: 32rpx;
  color: #ff4d4f;
  background-color: #ffffff;
  border-radius: 16rpx;
}
</style>
