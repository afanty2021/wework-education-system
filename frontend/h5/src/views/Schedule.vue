<template>
  <div class="schedule-page">
    <!-- 日期选择器 -->
    <div class="date-picker">
      <van-button size="small" plain @click="prevDay">
        <van-icon name="arrow-left" />
      </van-button>
      <div class="current-date" @click="showDatePicker = true">
        <span>{{ formattedDate }}</span>
        <van-icon name="arrow-down" />
      </div>
      <van-button size="small" plain @click="nextDay">
        <van-icon name="arrow-right" />
      </van-button>
      <van-button size="small" type="primary" plain @click="goToToday">今天</van-button>
    </div>

    <!-- 周视图 -->
    <div class="week-view">
      <div
        v-for="day in weekDays"
        :key="day.date"
        :class="['week-day', { active: day.date === selectedDate, today: day.isToday }]"
        @click="selectDate(day.date)"
      >
        <span class="weekday">{{ day.weekday }}</span>
        <span class="day">{{ day.day }}</span>
      </div>
    </div>

    <!-- 课表列表 -->
    <div class="schedule-list" v-if="filteredSchedules.length > 0">
      <ScheduleCard
        v-for="schedule in filteredSchedules"
        :key="schedule.id"
        :schedule="schedule"
        show-actions
        @click="goToDetail(schedule.id)"
        @attendance="goToAttendance(schedule.id)"
      />
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-else>
      <van-icon name="calendar-o" size="64" color="#ccc" />
      <p>{{ selectedDate === today ? '今日暂无课程' : '该日暂无课程' }}</p>
      <van-button type="primary" size="small" @click="goToToday">返回今天</van-button>
    </div>

    <!-- 日期选择器弹窗 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-date-picker
        v-model="dateValue"
        :min-date="minDate"
        :max-date="maxDate"
        @confirm="onDateConfirm"
        @cancel="showDatePicker = false"
      />
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import { useScheduleStore } from '@/stores/schedule'
import ScheduleCard from '@/components/ScheduleCard.vue'
import type { ScheduleResponse } from '@/api/types'

const router = useRouter()
const scheduleStore = useScheduleStore()

// 日期状态
const today = dayjs().format('YYYY-MM-DD')
const selectedDate = ref(today)
const showDatePicker = ref(false)
const dateValue = ref(dayjs().toArray().slice(0, 3) as [number, number, number])

// 日期范围
const minDate = dayjs().subtract(30, 'day').toDate()
const maxDate = dayjs().add(90, 'day').toDate()

// 周视图数据
const weekDays = computed(() => {
  const days = []
  const startOfWeek = dayjs(selectedDate.value).startOf('week')

  for (let i = 0; i < 7; i++) {
    const date = startOfWeek.add(i, 'day')
    days.push({
      date: date.format('YYYY-MM-DD'),
      weekday: date.format('dd'),
      day: date.format('D'),
      isToday: date.format('YYYY-MM-DD') === today,
    })
  }
  return days
})

// 格式化日期显示
const formattedDate = computed(() => {
  const date = dayjs(selectedDate.value)
  const isToday = selectedDate.value === today
  const isYesterday = selectedDate.value === dayjs().subtract(1, 'day').format('YYYY-MM-DD')
  const isTomorrow = selectedDate.value === dayjs().add(1, 'day').format('YYYY-MM-DD')

  let suffix = ''
  if (isToday) suffix = '（今天）'
  else if (isYesterday) suffix = '（昨天）'
  else if (isTomorrow) suffix = '（明天）'

  return date.format('YYYY年M月D日') + suffix
})

// 过滤后的课表
const filteredSchedules = computed(() => {
  return scheduleStore.weekSchedules.filter((schedule) => {
    const scheduleDate = dayjs(schedule.start_time).format('YYYY-MM-DD')
    return scheduleDate === selectedDate.value
  })
})

// 生命周期
onMounted(async () => {
  await scheduleStore.fetchWeekSchedules()
})

// 监听日期变化
watch(selectedDate, () => {
  // 可以在这里根据日期加载课表
})

// 选择日期
function selectDate(date: string) {
  selectedDate.value = date
}

// 上一天
function prevDay() {
  selectedDate.value = dayjs(selectedDate.value).subtract(1, 'day').format('YYYY-MM-DD')
}

// 下一天
function nextDay() {
  selectedDate.value = dayjs(selectedDate.value).add(1, 'day').format('YYYY-MM-DD')
}

// 跳转到今天
function goToToday() {
  selectedDate.value = today
}

// 日期选择确认
function onDateConfirm({ selectedValues }: { selectedValues: number[] }) {
  selectedDate.value = dayjs(selectedValues.join('-')).format('YYYY-MM-DD')
  showDatePicker.value = false
}

// 跳转到课表详情
function goToDetail(scheduleId: number) {
  router.push(`/schedule/${scheduleId}`)
}

// 跳转到考勤
function goToAttendance(scheduleId: number) {
  router.push(`/attendance/record/${scheduleId}`)
}
</script>

<style lang="scss" scoped>
.schedule-page {
  padding: 16px;
  padding-bottom: 80px;
}

.date-picker {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .current-date {
    display: flex;
    align-items: center;
    font-size: 16px;
    font-weight: 600;
    color: #333;

    .van-icon {
      margin-left: 4px;
      color: #999;
    }
  }
}

.week-view {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  padding: 12px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.week-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;

  &.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;

    .weekday,
    .day {
      color: #fff;
    }
  }

  &.today {
    .day {
      color: #667eea;
    }
  }

  &:not(.active):hover {
    background: #f5f5f5;
  }

  .weekday {
    font-size: 12px;
    color: #999;
    margin-bottom: 4px;
  }

  .day {
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }
}

.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;

  p {
    color: #999;
    margin: 16px 0;
  }
}
</style>
