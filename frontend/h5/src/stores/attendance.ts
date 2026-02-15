/**
 * 考勤状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getAttendances,
  getScheduleAttendances,
  createAttendance,
  batchCreateAttendances,
  updateAttendance,
  deleteAttendance,
  getStudentAttendanceStatistics,
  getScheduleAttendanceStatistics,
  type AttendanceResponse,
  type AttendanceStatistics,
} from '@/api/attendance'
import { useAuthStore } from './auth'

export const useAttendanceStore = defineStore('attendance', () => {
  const authStore = useAuthStore()

  // 考勤记录列表
  const attendances = ref<AttendanceResponse[]>([])

  // 当前排课的考勤记录
  const scheduleAttendances = ref<AttendanceResponse[]>([])

  // 当前选中的排课ID
  const currentScheduleId = ref<number | null>(null)

  // 考勤统计
  const statistics = ref<AttendanceStatistics | null>(null)

  // 加载状态
  const loading = ref(false)

  // 计算属性
  const teacherId = computed(() => authStore.userId)

  // 统计各类考勤数量
  const statsCount = computed(() => {
    const counts = {
      present: 0,
      leave: 0,
      absent: 0,
      late: 0,
      total: attendances.value.length,
    }
    attendances.value.forEach((item) => {
      switch (item.status) {
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

  /**
   * 获取考勤列表
   */
  async function fetchAttendances(params?: {
    schedule_id?: number
    student_id?: number
    status?: number
    skip?: number
    limit?: number
  }) {
    loading.value = true
    try {
      attendances.value = await getAttendances({
        ...params,
        teacher_id: teacherId.value,
      })
      return attendances.value
    } catch (error) {
      console.error('获取考勤列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取排课的考勤记录
   */
  async function fetchScheduleAttendances(scheduleId: number) {
    loading.value = true
    currentScheduleId.value = scheduleId
    try {
      scheduleAttendances.value = await getScheduleAttendances(scheduleId)
      return scheduleAttendances.value
    } catch (error) {
      console.error('获取排课考勤记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 创建考勤记录
   */
  async function createAttendanceRecord(data: {
    schedule_id: number
    student_id: number
    contract_id?: number
    status: number
    check_method?: number
    hours_consumed?: number
    notes?: string
  }) {
    try {
      const record = await createAttendance(data)
      // 添加到列表
      if (currentScheduleId.value === data.schedule_id) {
        scheduleAttendances.value.push(record)
      }
      return record
    } catch (error) {
      console.error('创建考勤记录失败:', error)
      throw error
    }
  }

  /**
   * 批量创建考勤记录
   */
  async function batchCreateAttendanceRecords(data: {
    attendances: Array<{
      schedule_id: number
      student_id: number
      contract_id?: number
      status: number
      check_method?: number
      hours_consumed?: number
      notes?: string
    }>
    auto_deduct_hours?: boolean
  }) {
    try {
      const records = await batchCreateAttendances(data)
      return records
    } catch (error) {
      console.error('批量创建考勤记录失败:', error)
      throw error
    }
  }

  /**
   * 更新考勤记录
   */
  async function updateAttendanceRecord(
    attendanceId: number,
    data: Partial<{
      status: number
      check_method: number
      hours_consumed: number
      notes: string
    }>
  ) {
    try {
      const record = await updateAttendance(attendanceId, data)
      // 更新列表中的记录
      const index = attendances.value.findIndex((item) => item.id === attendanceId)
      if (index !== -1) {
        attendances.value[index] = record
      }
      const scheduleIndex = scheduleAttendances.value.findIndex((item) => item.id === attendanceId)
      if (scheduleIndex !== -1) {
        scheduleAttendances.value[scheduleIndex] = record
      }
      return record
    } catch (error) {
      console.error('更新考勤记录失败:', error)
      throw error
    }
  }

  /**
   * 删除考勤记录
   */
  async function deleteAttendanceRecord(attendanceId: number) {
    try {
      await deleteAttendance(attendanceId)
      // 从列表中移除
      attendances.value = attendances.value.filter((item) => item.id !== attendanceId)
      scheduleAttendances.value = scheduleAttendances.value.filter((item) => item.id !== attendanceId)
    } catch (error) {
      console.error('删除考勤记录失败:', error)
      throw error
    }
  }

  /**
   * 获取学员考勤统计
   */
  async function fetchStudentStatistics(studentId: number): Promise<AttendanceStatistics> {
    try {
      statistics.value = await getStudentAttendanceStatistics(studentId)
      return statistics.value
    } catch (error) {
      console.error('获取学员考勤统计失败:', error)
      throw error
    }
  }

  /**
   * 获取排课考勤统计
   */
  async function fetchScheduleStatistics(scheduleId: number): Promise<AttendanceStatistics> {
    try {
      statistics.value = await getScheduleAttendanceStatistics(scheduleId)
      return statistics.value
    } catch (error) {
      console.error('获取排课考勤统计失败:', error)
      throw error
    }
  }

  /**
   * 清空状态
   */
  function clearState() {
    attendances.value = []
    scheduleAttendances.value = []
    currentScheduleId.value = null
    statistics.value = null
  }

  return {
    // 状态
    attendances,
    scheduleAttendances,
    currentScheduleId,
    statistics,
    loading,
    // 计算属性
    teacherId,
    statsCount,
    // 方法
    fetchAttendances,
    fetchScheduleAttendances,
    createAttendanceRecord,
    batchCreateAttendanceRecords,
    updateAttendanceRecord,
    deleteAttendanceRecord,
    fetchStudentStatistics,
    fetchScheduleStatistics,
    clearState,
  }
})
