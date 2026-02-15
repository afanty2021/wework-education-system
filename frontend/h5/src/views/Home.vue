<template>
  <div class="home-page">
    <!-- 顶部用户信息 -->
    <div class="header">
      <div class="user-info">
        <van-image
          round
          :src="userInfo?.avatar || defaultAvatar"
          class="avatar"
        />
        <div class="info">
          <h3 class="name">{{ userName }}</h3>
          <p class="role">{{ userRole === 'teacher' ? '教师' : userRole }}</p>
        </div>
      </div>
      <div class="date-info">
        <p class="date">{{ currentDate }}</p>
        <p class="weekday">{{ currentWeekday }}</p>
      </div>
    </div>

    <!-- 今日概览 -->
    <div class="section">
      <div class="section-header">
        <h3>今日概览</h3>
      </div>
      <div class="overview-cards">
        <div class="card" @click="goToSchedule">
          <div class="card-icon course">
            <van-icon name="calendar-o" size="24" />
          </div>
          <div class="card-content">
            <p class="count">{{ todayScheduleCount }}</p>
            <p class="label">今日课程</p>
          </div>
        </div>
        <div class="card" @click="goToAttendance">
          <div class="card-icon attendance">
            <van-icon name="todo-list-o" size="24" />
          </div>
          <div class="card-content">
            <p class="count">{{ pendingAttendanceCount }}</p>
            <p class="label">待考勤</p>
          </div>
        </div>
        <div class="card" @click="goToNotifications">
          <div class="card-icon notification">
            <van-icon name="bell-o" size="24" />
            <span v-if="unreadCount > 0" class="badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
          </div>
          <div class="card-content">
            <p class="count">{{ unreadCount }}</p>
            <p class="label">未读消息</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 今日课程 -->
    <div class="section">
      <div class="section-header">
        <h3>今日课程</h3>
        <van-button size="small" type="primary" plain @click="goToSchedule">
          查看全部
        </van-button>
      </div>
      <div class="schedule-list" v-if="todaySchedules.length > 0">
        <ScheduleCard
          v-for="schedule in todaySchedules"
          :key="schedule.id"
          :schedule="schedule"
          @click="goToScheduleDetail(schedule.id)"
        />
      </div>
      <div class="empty-state" v-else>
        <van-icon name="calendar-o" size="48" color="#ccc" />
        <p>今日暂无课程</p>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="section">
      <div class="section-header">
        <h3>快捷操作</h3>
      </div>
      <div class="quick-actions">
        <div class="action-item" @click="goToAttendance">
          <div class="action-icon">
            <van-icon name="edit" size="24" />
          </div>
          <p>考勤签到</p>
        </div>
        <div class="action-item" @click="goToNotifications">
          <div class="action-icon">
            <van-icon name="notification" size="24" />
          </div>
          <p>发送通知</p>
        </div>
        <div class="action-item" @click="goToProfile">
          <div class="action-icon">
            <van-icon name="user-o" size="24" />
          </div>
          <p>个人中心</p>
        </div>
        <div class="action-item" @click="toggleDarkMode">
          <div class="action-icon">
            <van-icon :name="darkMode ? 'sun-o' : 'moon-o'" size="24" />
          </div>
          <p>{{ darkMode ? '浅色模式' : '深色模式' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import { useAuthStore } from '@/stores/auth'
import { useScheduleStore } from '@/stores/schedule'
import { useNotificationStore } from '@/stores/notification'
import { useAppStore } from '@/stores/app'
import ScheduleCard from '@/components/ScheduleCard.vue'

dayjs.locale('zh-cn')

const router = useRouter()
const authStore = useAuthStore()
const scheduleStore = useScheduleStore()
const notificationStore = useNotificationStore()
const appStore = useAppStore()

// 默认头像
const defaultAvatar = 'https://avatars.githubusercontent.com/u/1?v=4'

// 计算属性
const userInfo = computed(() => authStore.userInfo)
const userName = computed(() => authStore.userName)
const userRole = computed(() => authStore.userRole)
const darkMode = computed(() => appStore.darkMode)

const currentDate = computed(() => dayjs().format('YYYY年MM月DD日'))
const currentWeekday = computed(() => dayjs().format('dddd'))

const todaySchedules = computed(() => scheduleStore.todaySchedules)
const todayScheduleCount = computed(() => todaySchedules.value.length)
const pendingAttendanceCount = computed(() => {
  // 简化的待考勤计算
  return todaySchedules.value.filter((s) => s.status === 1).length
})
const unreadCount = computed(() => notificationStore.unreadCount)

// 生命周期
onMounted(async () => {
  await Promise.all([
    scheduleStore.fetchTodaySchedules(),
    notificationStore.fetchNotifications(),
    notificationStore.fetchUnreadCount(),
  ])
})

// 路由跳转
function goToSchedule() {
  router.push('/schedule')
}

function goToScheduleDetail(scheduleId: number) {
  router.push(`/schedule/${scheduleId}`)
}

function goToAttendance() {
  router.push('/attendance')
}

function goToNotifications() {
  router.push('/notifications')
}

function goToProfile() {
  router.push('/profile')
}

function toggleDarkMode() {
  appStore.toggleDarkMode()
}
</script>

<style lang="scss" scoped>
.home-page {
  padding: 16px;
  padding-bottom: 80px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #fff;
}

.user-info {
  display: flex;
  align-items: center;

  .avatar {
    width: 50px;
    height: 50px;
    margin-right: 12px;
  }

  .name {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 4px;
  }

  .role {
    font-size: 12px;
    opacity: 0.8;
    margin: 0;
  }
}

.date-info {
  text-align: right;

  .date {
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 4px;
  }

  .weekday {
    font-size: 12px;
    opacity: 0.8;
    margin: 0;
  }
}

.section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
  }
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .card-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 8px;
    position: relative;

    &.course {
      background: #e3f2fd;
      color: #1976d2;
    }

    &.attendance {
      background: #fce4ec;
      color: #c2185b;
    }

    &.notification {
      background: #fff3e0;
      color: #f57c00;
    }

    .badge {
      position: absolute;
      top: -4px;
      right: -4px;
      min-width: 18px;
      height: 18px;
      padding: 0 4px;
      background: #f44336;
      color: #fff;
      font-size: 10px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }

  .card-content {
    .count {
      font-size: 24px;
      font-weight: 600;
      margin: 0 0 4px;
      color: #333;
    }

    .label {
      font-size: 12px;
      color: #999;
      margin: 0;
    }
  }
}

.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  background: #f5f5f5;
  border-radius: 12px;

  p {
    color: #999;
    margin: 12px 0 0;
  }
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.action-item {
  text-align: center;
  padding: 12px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .action-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 8px;
  }

  p {
    font-size: 12px;
    color: #666;
    margin: 0;
  }
}
</style>
