<template>
  <div class="schedule-card" @click="handleClick">
    <div class="card-time">
      <span class="time-range">{{ formatTime(schedule.start_time) }} - {{ formatTime(schedule.end_time) }}</span>
      <van-tag :type="statusType" size="small">{{ statusText }}</van-tag>
    </div>
    <div class="card-content">
      <h4 class="course-name">{{ schedule.course_name || '课程' }}</h4>
      <div class="course-info">
        <span class="info-item">
          <van-icon name="location-o" />
          {{ schedule.classroom_name || '未知教室' }}
        </span>
        <span class="info-item">
          <van-icon name="friends-o" />
          {{ schedule.enrolled_count }}/{{ schedule.max_students }}人
        </span>
      </div>
    </div>
    <div class="card-actions" v-if="showActions" @click.stop="handleAttendance">
      <van-button size="small" type="primary">
        考勤
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import dayjs from 'dayjs'
import type { ScheduleResponse } from '@/api/types'

const props = defineProps<{
  schedule: ScheduleResponse
  showActions?: boolean
}>()

const emit = defineEmits<{
  click: []
  attendance: []
}>()

// 状态类型
const statusType = computed(() => {
  switch (props.schedule.status) {
    case 1:
      return 'primary'
    case 2:
      return 'success'
    case 3:
      return 'danger'
    case 4:
      return 'warning'
    default:
      return 'default'
  }
})

const statusText = computed(() => {
  switch (props.schedule.status) {
    case 1:
      return '已安排'
    case 2:
      return '已上课'
    case 3:
      return '已取消'
    case 4:
      return '已调课'
    default:
      return '未知'
  }
})

function formatTime(dateStr: string) {
  return dayjs(dateStr).format('HH:mm')
}

function handleClick() {
  emit('click')
}

function handleAttendance() {
  emit('attendance')
}
</script>

<style lang="scss" scoped>
.schedule-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s;

  &:active {
    transform: scale(0.98);
    background: #f5f5f5;
  }
}

.card-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
  padding-right: 16px;
  border-right: 1px solid #f5f5f5;

  .time-range {
    font-size: 12px;
    font-weight: 600;
    color: #667eea;
    margin-bottom: 8px;
  }
}

.card-content {
  flex: 1;
  padding: 0 16px;

  .course-name {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 8px;
    color: #333;
  }

  .course-info {
    display: flex;
    gap: 16px;

    .info-item {
      display: flex;
      align-items: center;
      font-size: 13px;
      color: #999;

      .van-icon {
        margin-right: 4px;
      }
    }
  }
}

.card-actions {
  :deep(.van-button) {
    height: 32px;
    font-size: 13px;
  }
}
</style>
