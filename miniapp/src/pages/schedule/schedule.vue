<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useScheduleStore } from '@/stores/schedule'
import { WeekDayFullText } from '@/types'
import ScheduleCard from '@/components/ScheduleCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const scheduleStore = useScheduleStore()

// 页面状态
const loading = ref(true)
const currentWeek = ref(new Date())
const currentWeekday = ref(new Date().getDay() || 7)

// 一周日期
const weekDates = computed(() => {
  const dates = []
  const today = new Date()
  const dayOfWeek = today.getDay() || 7
  const monday = new Date(today)
  monday.setDate(today.getDate() - dayOfWeek + 1)

  for (let i = 0; i < 7; i++) {
    const date = new Date(monday)
    date.setDate(monday.getDate() + i)
    dates.push({
      date,
      weekday: i + 1,
      day: date.getDate(),
      month: date.getMonth() + 1,
      isToday: date.toDateString() === today.toDateString()
    })
  }
  return dates
})

// 当前选中日期的课表
const currentDaySchedules = computed(() => {
  const selectedDate = weekDates.value.find(d => d.weekday === currentWeekday.value)
  if (!selectedDate) return []
  const dateStr = selectedDate.date.toISOString().split('T')[0]
  return scheduleStore.filterSchedulesByDate(dateStr)
})

/**
 * 初始化页面数据
 */
async function initPage() {
  loading.value = true
  try {
    await scheduleStore.fetchWeekSchedules()
  } catch (error) {
    console.error('加载课表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 选择星期几
 */
function selectWeekday(weekday: number) {
  currentWeekday.value = weekday
}

/**
 * 上周
 */
function previousWeek() {
  const newDate = new Date(currentWeek.value)
  newDate.setDate(newDate.getDate() - 7)
  currentWeek.value = newDate
}

/**
 * 下周
 */
function nextWeek() {
  const newDate = new Date(currentWeek.value)
  newDate.setDate(newDate.getDate() + 7)
  currentWeek.value = newDate
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
 * 设置课程提醒
 */
function onRemind(schedule: any) {
  uni.showModal({
    title: '课程提醒',
    content: `确定要设置${schedule.course_name || '课程'}的提醒吗？`,
    success: (res) => {
      if (res.confirm) {
        uni.showToast({
          title: '已设置提醒',
          icon: 'success'
        })
      }
    }
  })
}

/**
 * 下拉刷新
 */
async function onPullDownRefresh() {
  await initPage()
  uni.stopPullDownRefresh()
}

onMounted(() => {
  initPage()
})
</script>

<template>
  <view class="schedule-container">
    <!-- 周导航 -->
    <view class="week-nav">
      <view class="nav-btn" @click="previousWeek">
        <text class="icon">&lt;</text>
      </view>
      <view class="week-title">
        {{ currentWeek.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' }) }}
      </view>
      <view class="nav-btn" @click="nextWeek">
        <text class="icon">&gt;</text>
      </view>
    </view>

    <!-- 星期选择器 -->
    <scroll-view scroll-x class="weekday-scroll">
      <view class="weekday-list">
        <view
          v-for="item in weekDates"
          :key="item.weekday"
          :class="['weekday-item', { active: currentWeekday === item.weekday, today: item.isToday }]"
          @click="selectWeekday(item.weekday)"
        >
          <text class="weekday-name">{{ WeekDayFullText[item.weekday] }}</text>
          <text class="weekday-date">{{ item.month }}/{{ item.day }}</text>
          <view class="today-dot" v-if="item.isToday"></view>
        </view>
      </view>
    </scroll-view>

    <!-- 课表列表 -->
    <view class="schedule-list" v-if="currentDaySchedules.length > 0">
      <ScheduleCard
        v-for="schedule in currentDaySchedules"
        :key="schedule.id"
        :schedule="schedule"
        @click="onScheduleClick"
        @remind="onRemind"
      />
    </view>

    <!-- 空状态 -->
    <EmptyState
      v-else
      text="当日暂无课程"
      description="选择其他日期查看课表"
    />
  </view>
</template>

<style lang="scss" scoped>
.schedule-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 40rpx;
}

.week-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx;
  background-color: #ffffff;

  .nav-btn {
    width: 60rpx;
    height: 60rpx;
    line-height: 60rpx;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 50%;

    .icon {
      font-size: 32rpx;
      color: #606266;
    }
  }

  .week-title {
    font-size: 34rpx;
    font-weight: 600;
    color: #303133;
  }
}

.weekday-scroll {
  white-space: nowrap;
  background-color: #ffffff;
  border-bottom: 2rpx solid #f0f0f0;

  .weekday-list {
    display: flex;
    padding: 20rpx 10rpx;
  }

  .weekday-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16rpx 24rpx;
    margin: 0 10rpx;
    border-radius: 12rpx;
    position: relative;
    transition: background-color 0.2s;

    &.active {
      background-color: #e6f7ff;

      .weekday-name {
        color: #1890ff;
        font-weight: 600;
      }
    }

    &.today {
      .weekday-date {
        color: #1890ff;
      }
    }

    .weekday-name {
      font-size: 26rpx;
      color: #606266;
      margin-bottom: 6rpx;
    }

    .weekday-date {
      font-size: 24rpx;
      color: #909399;
    }

    .today-dot {
      position: absolute;
      top: 8rpx;
      right: 8rpx;
      width: 12rpx;
      height: 12rpx;
      background-color: #ff4d4f;
      border-radius: 50%;
    }
  }
}

.schedule-list {
  padding-top: 20rpx;
}
</style>
