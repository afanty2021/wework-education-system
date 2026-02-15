<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useScheduleStore } from '@/stores/schedule'
import { useAttendanceStore } from '@/stores/attendance'
import { useHomeworkStore } from '@/stores/homework'
import ScheduleCard from '@/components/ScheduleCard.vue'
import HomeworkCard from '@/components/HomeworkCard.vue'
import AttendanceCard from '@/components/AttendanceCard.vue'

const userStore = useUserStore()
const scheduleStore = useScheduleStore()
const attendanceStore = useAttendanceStore()
const homeworkStore = useHomeworkStore()

// 页面状态
const loading = ref(true)
const activeTab = ref(0)

// 统计数据
const stats = ref({
  todayCourses: 0,
  pendingHomeworks: 0,
  attendanceRate: 0
})

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true

  try {
    // 并行加载数据
    await Promise.all([
      loadTodaySchedule(),
      loadPendingHomeworks(),
      loadAttendanceStats()
    ])
  } catch (error) {
    console.error('加载首页数据失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 加载今日课表
 */
async function loadTodaySchedule() {
  try {
    const schedules = await scheduleStore.fetchTodaySchedules()
    stats.value.todayCourses = schedules.length
  } catch (error) {
    console.error('加载今日课表失败:', error)
  }
}

/**
 * 加载待完成作业
 */
async function loadPendingHomeworks() {
  try {
    const homeworks = await homeworkStore.fetchPendingHomeworks()
    stats.value.pendingHomeworks = homeworks.length
  } catch (error) {
    console.error('加载待完成作业失败:', error)
  }
}

/**
 * 加载考勤统计
 */
async function loadAttendanceStats() {
  try {
    if (userStore.userId) {
      const statistics = await attendanceStore.fetchStatistics(userStore.userId)
      stats.value.attendanceRate = statistics.present_rate
    }
  } catch (error) {
    console.error('加载考勤统计失败:', error)
  }
}

/**
 * 下拉刷新
 */
async function onPullDownRefresh() {
  await initPage()
  uni.stopPullDownRefresh()
}

/**
 * 跳转到课表页面
 */
function navigateToSchedule() {
  uni.navigateTo({
    url: '/pages/schedule/schedule'
  })
}

/**
 * 跳转到作业页面
 */
function navigateToHomework() {
  uni.navigateTo({
    url: '/pages/homework/homework'
  })
}

/**
 * 跳转到考勤页面
 */
function navigateToAttendance() {
  uni.navigateTo({
    url: '/pages/attendance/attendance'
  })
}

/**
 * 跳转到个人中心
 */
function navigateToProfile() {
  uni.switchTab({
    url: '/pages/profile/profile'
  })
}

/**
 * 跳转到课程详情
 */
function onScheduleClick(schedule: any) {
  uni.navigateTo({
    url: `/pages/schedule/detail?id=${schedule.id}`
  })
}

/**
 * 跳转到作业详情
 */
function onHomeworkClick(homework: any) {
  uni.navigateTo({
    url: `/pages/homework/detail?id=${homework.id}`
  })
}

/**
 * 跳转到考勤详情
 */
function onAttendanceClick(attendance: any) {
  uni.navigateTo({
    url: `/pages/attendance/attendance?id=${attendance.id}`
  })
}

// 页面加载
onMounted(() => {
  initPage()
})
</script>

<template>
  <view class="index-container">
    <!-- 头部用户信息 -->
    <view class="header">
      <view class="user-info" @click="navigateToProfile">
        <image class="avatar" :src="userStore.userAvatar" mode="aspectFill" />
        <view class="info">
          <view class="name">{{ userStore.userName }}</view>
          <view class="role">{{ userStore.userRole === 'student' ? '学员' : '家长' }}</view>
        </view>
      </view>
      <view class="date-info">
        <text class="date">{{ new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' }) }}</text>
        <text class="weekday">{{ ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][new Date().getDay()] }}</text>
      </view>
    </view>

    <!-- 快捷功能入口 -->
    <view class="quick-actions">
      <view class="action-item" @click="navigateToSchedule">
        <view class="icon schedule">课</view>
        <text class="label">今日课表</text>
        <text class="count" v-if="stats.todayCourses > 0">{{ stats.todayCourses }}节</text>
      </view>
      <view class="action-item" @click="navigateToHomework">
        <view class="icon homework">作</view>
        <text class="label">待交作业</text>
        <text class="count" v-if="stats.pendingHomeworks > 0">{{ stats.pendingHomeworks }}份</text>
      </view>
      <view class="action-item" @click="navigateToAttendance">
        <view class="icon attendance">考</view>
        <text class="label">考勤记录</text>
        <text class="rate" v-if="stats.attendanceRate > 0">{{ stats.attendanceRate.toFixed(0) }}%</text>
      </view>
    </view>

    <!-- 今日课表 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">今日课表</text>
        <text class="more" @click="navigateToSchedule">查看全部</text>
      </view>
      <view class="schedule-list" v-if="scheduleStore.todaySchedules.length > 0">
        <ScheduleCard
          v-for="schedule in scheduleStore.todaySchedules.slice(0, 3)"
          :key="schedule.id"
          :schedule="schedule"
          @click="onScheduleClick"
        />
      </view>
      <view class="empty-tip" v-else>
        <text>今日暂无课程</text>
      </view>
    </view>

    <!-- 待完成作业 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">待完成作业</text>
        <text class="more" @click="navigateToHomework">查看全部</text>
      </view>
      <view class="homework-list" v-if="homeworkStore.homeworks.length > 0">
        <HomeworkCard
          v-for="homework in homeworkStore.homeworks.slice(0, 2)"
          :key="homework.id"
          :homework="homework"
          @click="onHomeworkClick"
        />
      </view>
      <view class="empty-tip" v-else>
        <text>暂无待完成作业</text>
      </view>
    </view>

    <!-- 最近考勤 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">最近考勤</text>
        <text class="more" @click="navigateToAttendance">查看全部</text>
      </view>
      <view class="attendance-list" v-if="attendanceStore.attendances.length > 0">
        <AttendanceCard
          v-for="attendance in attendanceStore.getRecentRecords(3)"
          :key="attendance.id"
          :attendance="attendance"
          @click="onAttendanceClick"
        />
      </view>
      <view class="empty-tip" v-else>
        <text>暂无考勤记录</text>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.index-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 40rpx;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 40rpx 30rpx;
  background-color: #ffffff;

  .user-info {
    display: flex;
    align-items: center;

    .avatar {
      width: 100rpx;
      height: 100rpx;
      border-radius: 50%;
      margin-right: 20rpx;
      background-color: #f5f5f5;
    }

    .info {
      .name {
        font-size: 36rpx;
        font-weight: 600;
        color: #303133;
      }

      .role {
        font-size: 26rpx;
        color: #909399;
        margin-top: 6rpx;
      }
    }
  }

  .date-info {
    display: flex;
    flex-direction: column;
    align-items: flex-end;

    .date {
      font-size: 32rpx;
      font-weight: 600;
      color: #303133;
    }

    .weekday {
      font-size: 26rpx;
      color: #909399;
      margin-top: 6rpx;
    }
  }
}

.quick-actions {
  display: flex;
  justify-content: space-around;
  padding: 30rpx 20rpx;
  margin: 20rpx;
  background-color: #ffffff;
  border-radius: 16rpx;

  .action-item {
    display: flex;
    flex-direction: column;
    align-items: center;

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

      &.schedule {
        background: linear-gradient(135deg, #1890ff, #096dd9);
      }

      &.homework {
        background: linear-gradient(135deg, #52c41a, #389e0d);
      }

      &.attendance {
        background: linear-gradient(135deg, #faad14, #d48806);
      }
    }

    .label {
      font-size: 26rpx;
      color: #606266;
      margin-bottom: 4rpx;
    }

    .count,
    .rate {
      font-size: 24rpx;
      color: #1890ff;
      font-weight: 500;
    }
  }
}

.section {
  margin-top: 20rpx;

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 30rpx;

    .section-title {
      font-size: 32rpx;
      font-weight: 600;
      color: #303133;
    }

    .more {
      font-size: 26rpx;
      color: #909399;
    }
  }

  .empty-tip {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 60rpx 0;
    color: #909399;
    font-size: 28rpx;
  }
}
</style>
