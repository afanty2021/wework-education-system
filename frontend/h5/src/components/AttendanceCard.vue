<template>
  <div class="attendance-card" @click="handleClick">
    <div class="card-status">
      <van-tag :type="statusType" size="medium">{{ statusText }}</van-tag>
    </div>
    <div class="card-content">
      <div class="course-info">
        <span class="course-name">{{ record.schedule_name || '课程' }}</span>
        <span class="student-name">{{ record.student_name || '学员' }}</span>
      </div>
      <div class="card-meta">
        <span class="meta-item" v-if="record.check_time">
          <van-icon name="clock-o" />
          {{ formatTime(record.check_time) }}
        </span>
        <span class="meta-item" v-if="record.hours_consumed">
          <van-icon name="balance-list-o" />
          {{ record.hours_consumed }}课时
        </span>
      </div>
    </div>
    <div class="card-arrow">
      <van-icon name="arrow" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import dayjs from 'dayjs'
import type { AttendanceResponse } from '@/api/types'

const props = defineProps<{
  record: AttendanceResponse
}>()

const emit = defineEmits<{
  click: []
}>()

// 状态类型
const statusType = computed(() => {
  switch (props.record.status) {
    case 1:
      return 'success'
    case 2:
      return 'primary'
    case 3:
      return 'danger'
    case 4:
      return 'warning'
    default:
      return 'default'
  }
})

const statusText = computed(() => {
  switch (props.record.status) {
    case 1:
      return '出勤'
    case 2:
      return '请假'
    case 3:
      return '缺勤'
    case 4:
      return '迟到'
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
</script>

<style lang="scss" scoped>
.attendance-card {
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

.card-status {
  margin-right: 16px;
}

.card-content {
  flex: 1;

  .course-info {
    display: flex;
    flex-direction: column;
    margin-bottom: 8px;

    .course-name {
      font-size: 15px;
      font-weight: 500;
      color: #333;
      margin-bottom: 4px;
    }

    .student-name {
      font-size: 13px;
      color: #666;
    }
  }

  .card-meta {
    display: flex;
    gap: 16px;

    .meta-item {
      display: flex;
      align-items: center;
      font-size: 12px;
      color: #999;

      .van-icon {
        margin-right: 4px;
      }
    }
  }
}

.card-arrow {
  color: #ccc;
}
</style>
