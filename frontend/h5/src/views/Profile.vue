<template>
  <div class="profile-page">
    <!-- 用户信息头部 -->
    <div class="profile-header">
      <van-image
        round
        :src="userInfo?.avatar || defaultAvatar"
        class="avatar"
      />
      <div class="user-info">
        <h3 class="name">{{ userName }}</h3>
        <p class="role">{{ userRole === 'teacher' ? '教师' : userRole }}</p>
      </div>
      <van-button size="small" plain type="primary" @click="editProfile">
        编辑资料
      </van-button>
    </div>

    <!-- 统计信息 -->
    <div class="stats-card">
      <div class="stat-item" @click="goToSchedule">
        <span class="value">{{ scheduleCount }}</span>
        <span class="label">今日课程</span>
      </div>
      <div class="stat-item" @click="goToAttendance">
        <span class="value">{{ attendanceCount }}</span>
        <span class="label">本月考勤</span>
      </div>
      <div class="stat-item" @click="goToNotifications">
        <span class="value">{{ unreadCount }}</span>
        <span class="label">未读消息</span>
      </div>
    </div>

    <!-- 菜单列表 -->
    <div class="menu-list">
      <div class="menu-group">
        <div class="menu-item" @click="goToSchedule">
          <van-icon name="calendar-o" class="menu-icon" />
          <span>我的课表</span>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
        <div class="menu-item" @click="goToAttendance">
          <van-icon name="todo-list-o" class="menu-icon" />
          <span>考勤记录</span>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
        <div class="menu-item" @click="goToNotifications">
          <van-icon name="bell-o" class="menu-icon" />
          <span>消息通知</span>
          <van-badge v-if="unreadCount > 0" :content="unreadCount" max="99" />
          <van-icon name="arrow" class="arrow-icon" />
        </div>
      </div>

      <div class="menu-group">
        <div class="menu-item" @click="changePassword">
          <van-icon name="lock" class="menu-icon" />
          <span>修改密码</span>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
        <div class="menu-item" @click="toggleDarkMode">
          <van-icon :name="darkMode ? 'sun-o' : 'moon-o'" class="menu-icon" />
          <span>{{ darkMode ? '浅色模式' : '深色模式' }}</span>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
        <div class="menu-item" @click="clearCache">
          <van-icon name="delete" class="menu-icon" />
          <span>清除缓存</span>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
      </div>

      <div class="menu-group">
        <div class="menu-item" @click="showAbout">
          <van-icon name="info-o" class="menu-icon" />
          <span>关于</span>
          <span class="version">v1.0.0</span>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
      </div>
    </div>

    <!-- 退出登录 -->
    <div class="logout-section">
      <van-button type="danger" block round @click="logout">
        退出登录
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useScheduleStore } from '@/stores/schedule'
import { useAttendanceStore } from '@/stores/attendance'
import { useNotificationStore } from '@/stores/notification'
import { useAppStore } from '@/stores/app'
import { Dialog, Toast } from 'vant'

const router = useRouter()
const authStore = useAuthStore()
const scheduleStore = useScheduleStore()
const attendanceStore = useAttendanceStore()
const notificationStore = useNotificationStore()
const appStore = useAppStore()

// 默认头像
const defaultAvatar = 'https://avatars.githubusercontent.com/u/1?v=4'

// 计算属性
const userInfo = computed(() => authStore.userInfo)
const userName = computed(() => authStore.userName)
const userRole = computed(() => authStore.userRole)
const darkMode = computed(() => appStore.darkMode)

const scheduleCount = computed(() => scheduleStore.todaySchedules.length)
const attendanceCount = computed(() => attendanceStore.attendances.length)
const unreadCount = computed(() => notificationStore.unreadCount)

// 路由跳转
function goToSchedule() {
  router.push('/schedule')
}

function goToAttendance() {
  router.push('/attendance')
}

function goToNotifications() {
  router.push('/notifications')
}

function editProfile() {
  Toast('编辑资料功能开发中')
}

function changePassword() {
  Toast('修改密码功能开发中')
}

function toggleDarkMode() {
  appStore.toggleDarkMode()
}

function clearCache() {
  Dialog.confirm({
    title: '清除缓存',
    message: '确定要清除本地缓存吗？',
  }).then(() => {
    localStorage.clear()
    Toast.success('清除成功')
  })
}

function showAbout() {
  Dialog.alert({
    title: '关于',
    message: '企业微信教务系统 - 教师端\n版本：v1.0.0\n\n基于 Vue 3 + Vant 4 开发',
  })
}

async function logout() {
  Dialog.confirm({
    title: '退出登录',
    message: '确定要退出登录吗？',
  }).then(() => {
    authStore.logout()
  })
}

onMounted(async () => {
  await Promise.all([
    scheduleStore.fetchTodaySchedules(),
    attendanceStore.fetchAttendances(),
    notificationStore.fetchUnreadCount(),
  ])
})
</script>

<style lang="scss" scoped>
.profile-page {
  padding: 16px;
  padding-bottom: 100px;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #fff;
  margin-bottom: 16px;

  .avatar {
    width: 64px;
    height: 64px;
    margin-right: 16px;
  }

  .user-info {
    flex: 1;

    .name {
      font-size: 20px;
      font-weight: 600;
      margin: 0 0 4px;
    }

    .role {
      font-size: 14px;
      opacity: 0.9;
      margin: 0;
    }
  }
}

.stats-card {
  display: flex;
  justify-content: space-around;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-item {
  text-align: center;
  cursor: pointer;

  .value {
    display: block;
    font-size: 24px;
    font-weight: 600;
    color: #667eea;
  }

  .label {
    font-size: 12px;
    color: #999;
  }
}

.menu-list {
  .menu-group {
    background: #fff;
    border-radius: 12px;
    margin-bottom: 16px;
    overflow: hidden;
  }

  .menu-item {
    display: flex;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;

    &:last-child {
      border-bottom: none;
    }

    &:active {
      background: #f5f5f5;
    }

    .menu-icon {
      font-size: 20px;
      color: #667eea;
      margin-right: 12px;
    }

    span {
      flex: 1;
      font-size: 15px;
    }

    .version {
      font-size: 13px;
      color: #999;
    }

    .arrow-icon {
      color: #ccc;
    }

    :deep(.van-badge) {
      margin-right: 12px;
    }
  }
}

.logout-section {
  padding: 16px;
}
</style>
