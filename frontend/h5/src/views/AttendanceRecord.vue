<template>
  <div class="attendance-record-page">
    <!-- 课表信息 -->
    <div class="schedule-info" v-if="schedule">
      <h3>{{ schedule.course_name || '课程' }}</h3>
      <p>{{ formatTime(schedule.start_time) }} - {{ formatTime(schedule.end_time) }}</p>
      <p>{{ schedule.classroom_name }}</p>
    </div>

    <!-- 学员列表 -->
    <div class="students-section">
      <div class="section-header">
        <h3>学员考勤 ({{ students.length }}人)</h3>
        <van-button size="small" type="primary" @click="batchCheckIn">
          批量签到
        </van-button>
      </div>

      <div class="students-list">
        <div
          v-for="student in students"
          :key="student.id"
          class="student-item"
          :class="{ checked: getStudentStatus(student.id) }"
        >
          <div class="student-info">
            <span class="name">{{ student.name }}</span>
            <span class="phone">{{ student.phone || student.parent_phone || '-' }}</span>
          </div>
          <div class="attendance-actions">
            <van-button
              size="small"
              :type="getStudentStatus(student.id) === 1 ? 'success' : 'default'"
              @click="checkIn(student.id, 1)"
            >
              出勤
            </van-button>
            <van-button
              size="small"
              :type="getStudentStatus(student.id) === 4 ? 'warning' : 'default'"
              @click="checkIn(student.id, 4)"
            >
              迟到
            </van-button>
            <van-button
              size="small"
              :type="getStudentStatus(student.id) === 2 ? 'primary' : 'default'"
              @click="checkIn(student.id, 2)"
            >
              请假
            </van-button>
            <van-button
              size="small"
              :type="getStudentStatus(student.id) === 3 ? 'danger' : 'default'"
              @click="checkIn(student.id, 3)"
            >
              缺勤
            </van-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 已考勤统计 -->
    <div class="statistics" v-if="students.length > 0">
      <div class="stat-item">
        <span class="value">{{ checkedCount }}</span>
        <span class="label">已考勤</span>
      </div>
      <div class="stat-item">
        <span class="value">{{ uncheckedCount }}</span>
        <span class="label">待考勤</span>
      </div>
      <div class="stat-item">
        <span class="value">{{ presentRate }}%</span>
        <span class="label">出勤率</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import { useScheduleStore } from '@/stores/schedule'
import { useAttendanceStore } from '@/stores/attendance'
import { showSuccess, showFail } from '@/stores/app'

const route = useRoute()
const scheduleStore = useScheduleStore()
const attendanceStore = useAttendanceStore()

const scheduleId = computed(() => Number(route.params.scheduleId))

// 课表信息
const schedule = computed(() => scheduleStore.currentSchedule)

// 学员名单
const students = computed(() => scheduleStore.scheduleStudents)

// 已考勤记录
const attendanceRecords = computed(() => attendanceStore.scheduleAttendances)

// 学员考勤状态映射
const studentStatusMap = computed(() => {
  const map: Record<number, number> = {}
  attendanceRecords.value.forEach((record) => {
    map[record.student_id] = record.status
  })
  return map
})

// 获取学员考勤状态
function getStudentStatus(studentId: number) {
  return studentStatusMap.value[studentId]
}

// 计算属性
const checkedCount = computed(() => attendanceRecords.value.length)
const uncheckedCount = computed(() => students.value.length - checkedCount.value)
const presentRate = computed(() => {
  if (students.value.length === 0) return 0
  const present = attendanceRecords.value.filter((r) => r.status === 1 || r.status === 4).length
  return Math.round((present / students.value.length) * 100)
})

function formatTime(dateStr: string) {
  return dayjs(dateStr).format('HH:mm')
}

// 签到
async function checkIn(studentId: number, status: number) {
  try {
    // 检查是否已存在记录
    const existing = attendanceRecords.value.find((r) => r.student_id === studentId)
    if (existing) {
      await attendanceStore.updateAttendanceRecord(existing.id, { status })
    } else {
      await attendanceStore.createAttendanceRecord({
        schedule_id: scheduleId.value,
        student_id: studentId,
        status,
        check_method: 1, // 手动签到
      })
    }
    showSuccess('签到成功')
  } catch (error) {
    showFail('签到失败')
  }
}

// 批量签到
async function batchCheckIn() {
  try {
    const uncheckedStudents = students.value.filter(
      (s) => !studentStatusMap.value[s.id]
    )
    if (uncheckedStudents.length === 0) {
      showFail('没有待考勤的学员')
      return
    }

    await attendanceStore.batchCreateAttendanceRecords({
      attendances: uncheckedStudents.map((s) => ({
        schedule_id: scheduleId.value,
        student_id: s.id,
        status: 1, // 批量签到默认出勤
        check_method: 1,
      })),
    })
    showSuccess(`已为 ${uncheckedStudents.length} 名学员签到`)
  } catch (error) {
    showFail('批量签到失败')
  }
}

onMounted(async () => {
  await scheduleStore.fetchScheduleDetail(scheduleId.value)
  await scheduleStore.fetchScheduleStudents(scheduleId.value)
  await attendanceStore.fetchScheduleAttendances(scheduleId.value)
})
</script>

<style lang="scss" scoped>
.attendance-record-page {
  padding: 16px;
  padding-bottom: 80px;
}

.schedule-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 16px;

  h3 {
    font-size: 18px;
    margin: 0 0 8px;
  }

  p {
    font-size: 14px;
    margin: 4px 0;
    opacity: 0.9;
  }
}

.students-section {
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
}

.students-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.student-item {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  &.checked {
    border-left: 3px solid #667eea;
  }

  .student-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;

    .name {
      font-weight: 500;
    }

    .phone {
      color: #999;
    }
  }

  .attendance-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;

    .van-button {
      flex: 1;
      min-width: 60px;
    }
  }
}

.statistics {
  display: flex;
  justify-content: space-around;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-top: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-item {
  text-align: center;

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
</style>
