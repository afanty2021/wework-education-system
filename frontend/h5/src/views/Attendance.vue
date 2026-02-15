<template>
  <div class="attendance-page">
    <!-- 筛选器 -->
    <div class="filter-bar">
      <van-dropdown-menu>
        <van-dropdown-item v-model="statusFilter" :options="statusOptions" @change="onFilterChange" />
      </van-dropdown-menu>
    </div>

    <!-- 今日待考勤 -->
    <div class="section" v-if="todayPendingSchedules.length > 0">
      <div class="section-header">
        <h3>今日待考勤</h3>
      </div>
      <div class="pending-list">
        <div
          v-for="schedule in todayPendingSchedules"
          :key="schedule.id"
          class="pending-item"
          @click="goToRecord(schedule.id)"
        >
          <div class="item-info">
            <h4>{{ schedule.course_name || '课程' }}</h4>
            <p>{{ formatTime(schedule.start_time) }} - {{ formatTime(schedule.end_time) }}</p>
            <p>{{ schedule.classroom_name }}</p>
          </div>
          <div class="item-action">
            <van-icon name="arrow" />
          </div>
        </div>
      </div>
    </div>

    <!-- 考勤记录列表 -->
    <div class="section">
      <div class="section-header">
        <h3>考勤记录</h3>
        <span class="count">共 {{ attendances.length }} 条</span>
      </div>
      <div class="attendance-list" v-if="attendances.length > 0">
        <AttendanceCard
          v-for="record in attendances"
          :key="record.id"
          :record="record"
          @click="viewDetail(record)"
        />
      </div>
      <div class="empty-state" v-else>
        <van-icon name="todo-list-o" size="64" color="#ccc" />
        <p>暂无考勤记录</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="statistics-card">
      <h4>考勤统计</h4>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="value">{{ stats.present }}</span>
          <span class="label">出勤</span>
        </div>
        <div class="stat-item">
          <span class="value">{{ stats.leave }}</span>
          <span class="label">请假</span>
        </div>
        <div class="stat-item">
          <span class="value">{{ stats.absent }}</span>
          <span class="label">缺勤</span>
        </div>
        <div class="stat-item">
          <span class="value">{{ stats.late }}</span>
          <span class="label">迟到</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import { useAttendanceStore } from '@/stores/attendance'
import { useScheduleStore } from '@/stores/schedule'
import AttendanceCard from '@/components/AttendanceCard.vue'
import type { AttendanceResponse } from '@/api/types'

const router = useRouter()
const attendanceStore = useAttendanceStore()
const scheduleStore = useScheduleStore()

// 筛选状态
const statusFilter = ref(0)
const statusOptions = [
  { text: '全部', value: 0 },
  { text: '出勤', value: 1 },
  { text: '请假', value: 2 },
  { text: '缺勤', value: 3 },
  { text: '迟到', value: 4 },
]

// 考勤列表
const attendances = computed(() => attendanceStore.attendances)

// 今日待考勤的课表
const todayPendingSchedules = computed(() => {
  const today = dayjs().format('YYYY-MM-DD')
  return scheduleStore.todaySchedules.filter((s) => {
    const scheduleDate = dayjs(scheduleStore.selectedDate || new Date()).format('YYYY-MM-DD')
    return scheduleDate === today && s.status === 1
  })
})

// 统计数据
const stats = computed(() => {
  const counts = { present: 0, leave: 0, absent: 0, late: 0 }
  attendances.value.forEach((record) => {
    switch (record.status) {
      case 1:
        counts.present++
        break
      case 2:
        counts.leave++
        break
      case 3:
        counts.absent++
        break
      case 4:
        counts.late++
        break
    }
  })
  return counts
})

function formatTime(dateStr: string) {
  return dayjs(dateStr).format('HH:mm')
}

function onFilterChange() {
  attendanceStore.fetchAttendances({ status: statusFilter.value || undefined })
}

function goToRecord(scheduleId: number) {
  router.push(`/attendance/record/${scheduleId}`)
}

function viewDetail(record: AttendanceResponse) {
  // 可以跳转到详情页
}

onMounted(async () => {
  await Promise.all([
    attendanceStore.fetchAttendances(),
    scheduleStore.fetchTodaySchedules(),
  ])
})
</script>

<style lang="scss" scoped>
.attendance-page {
  padding: 16px;
  padding-bottom: 80px;
}

.filter-bar {
  margin-bottom: 16px;
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

  .count {
    font-size: 12px;
    color: #999;
  }
}

.pending-list {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.pending-item {
  display: flex;
  justify-content: space-between;
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

  .item-info {
    h4 {
      font-size: 16px;
      font-weight: 500;
      margin: 0 0 8px;
    }

    p {
      font-size: 13px;
      color: #999;
      margin: 4px 0;
    }
  }

  .item-action {
    color: #999;
  }
}

.attendance-list {
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
    margin: 16px 0 0;
  }
}

.statistics-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: #fff;

  h4 {
    font-size: 14px;
    margin: 0 0 16px;
    opacity: 0.9;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }

  .stat-item {
    text-align: center;

    .value {
      display: block;
      font-size: 24px;
      font-weight: 600;
    }

    .label {
      font-size: 12px;
      opacity: 0.8;
    }
  }
}
</style>
