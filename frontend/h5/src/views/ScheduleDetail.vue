<template>
  <div class="schedule-detail-page">
    <van-loading v-if="loading" size="24" />
    <template v-else-if="schedule">
      <!-- 课程信息 -->
      <div class="schedule-info">
        <div class="info-header">
          <h2>{{ schedule.course_name || '课程详情' }}</h2>
          <van-tag :type="statusType">{{ statusText }}</van-tag>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <van-icon name="clock-o" />
            <span>{{ formatTime(schedule.start_time) }} - {{ formatTime(schedule.end_time) }}</span>
          </div>
          <div class="info-item">
            <van-icon name="location-o" />
            <span>{{ schedule.classroom_name || '未知教室' }}</span>
          </div>
          <div class="info-item">
            <van-icon name="user-o" />
            <span>{{ schedule.teacher_name || '待定' }}</span>
          </div>
          <div class="info-item">
            <van-icon name="friends-o" />
            <span>{{ schedule.enrolled_count }}/{{ schedule.max_students }} 人</span>
          </div>
        </div>
      </div>

      <!-- 学员名单 -->
      <div class="students-section">
        <div class="section-header">
          <h3>学员名单</h3>
          <van-button size="small" type="primary" @click="goToAttendance">
            考勤签到
          </van-button>
        </div>
        <div class="students-list" v-if="students.length > 0">
          <div v-for="(student, index) in students" :key="student.id" class="student-item">
            <span class="index">{{ index + 1 }}</span>
            <div class="student-info">
              <span class="name">{{ student.name }}</span>
              <span class="phone">{{ student.phone || student.parent_phone || '-' }}</span>
            </div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <p>暂无学员</p>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="actions" v-if="schedule.status === 1">
        <van-button type="primary" block @click="goToAttendance">
          考勤签到
        </van-button>
        <van-button plain type="primary" block @click="cancelSchedule">
          取消课程
        </van-button>
      </div>
    </template>
    <van-empty v-else description="课程不存在" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScheduleStore } from '@/stores/schedule'
import { showFail, showSuccess } from '@/stores/app'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const scheduleStore = useScheduleStore()

const scheduleId = computed(() => Number(route.params.id))
const schedule = computed(() => scheduleStore.currentSchedule)
const students = computed(() => scheduleStore.scheduleStudents)
const loading = computed(() => scheduleStore.loading)

const statusType = computed(() => {
  switch (schedule.value?.status) {
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
  switch (schedule.value?.status) {
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

onMounted(async () => {
  await scheduleStore.fetchScheduleDetail(scheduleId.value)
  if (schedule.value) {
    await scheduleStore.fetchScheduleStudents(scheduleId.value)
  }
})

function goToAttendance() {
  router.push(`/attendance/record/${scheduleId.value}`)
}

async function cancelSchedule() {
  showFail('取消课程功能开发中')
}
</script>

<style lang="scss" scoped>
.schedule-detail-page {
  padding: 16px;
  padding-bottom: 80px;
}

.schedule-info {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .info-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h2 {
      font-size: 20px;
      font-weight: 600;
      margin: 0;
    }
  }

  .info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .info-item {
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #666;

    .van-icon {
      margin-right: 8px;
      color: #999;
    }
  }
}

.students-section {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h3 {
      font-size: 16px;
      font-weight: 600;
      margin: 0;
    }
  }

  .students-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .student-item {
    display: flex;
    align-items: center;
    padding: 12px;
    background: #f5f5f5;
    border-radius: 8px;

    .index {
      width: 24px;
      height: 24px;
      background: #667eea;
      color: #fff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      margin-right: 12px;
    }

    .student-info {
      flex: 1;
      display: flex;
      justify-content: space-between;

      .name {
        font-weight: 500;
      }

      .phone {
        color: #999;
      }
    }
  }

  .empty-state {
    text-align: center;
    padding: 20px;
    color: #999;
  }
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: #fff;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}
</style>
