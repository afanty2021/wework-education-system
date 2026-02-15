/**
 * 考勤状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import AttendanceAPI, { type Attendance, type AttendanceStatistics, AttendanceStatus } from '@/api/attendance'

/**
 * 考勤状态管理
 */
export const useAttendanceStore = defineStore('attendance', () => {
  // 状态
  const attendances = ref<Attendance[]>([])
  const statistics = ref<AttendanceStatistics | null>(null)
  const loading = ref(false)

  // 计算属性
  const totalCount = computed(() => statistics.value?.total_count || 0)
  const presentCount = computed(() => statistics.value?.present_count || 0)
  const leaveCount = computed(() => statistics.value?.leave_count || 0)
  const absentCount = computed(() => statistics.value?.absent_count || 0)
  const lateCount = computed(() => statistics.value?.late_count || 0)
  const presentRate = computed(() => statistics.value?.present_rate || 0)

  /**
   * 获取考勤列表
   */
  async function fetchAttendances(params?: Parameters<typeof AttendanceAPI.list>[0]) {
    loading.value = true
    try {
      const result = await AttendanceAPI.list(params)
      attendances.value = result
      return result
    } catch (error) {
      console.error('获取考勤列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取我的考勤记录
   */
  async function fetchMyAttendances(params?: Partial<Parameters<typeof AttendanceAPI.list>[0]>) {
    loading.value = true
    try {
      const result = await AttendanceAPI.getMyAttendances(params)
      attendances.value = result
      return result
    } catch (error) {
      console.error('获取我的考勤记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取考勤统计
   */
  async function fetchStatistics(studentId: number) {
    loading.value = true
    try {
      const result = await AttendanceAPI.getStudentStatistics(studentId)
      statistics.value = result
      return result
    } catch (error) {
      console.error('获取考勤统计失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取考勤详情
   */
  async function fetchAttendanceDetail(attendanceId: number) {
    loading.value = true
    try {
      const result = await AttendanceAPI.getById(attendanceId)
      // 更新列表中的记录
      const index = attendances.value.findIndex(item => item.id === attendanceId)
      if (index !== -1) {
        attendances.value[index] = result
      }
      return result
    } catch (error) {
      console.error('获取考勤详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 按状态筛选考勤
   */
  function filterByStatus(status: AttendanceStatus): Attendance[] {
    return attendances.value.filter(item => item.status === status)
  }

  /**
   * 按月份筛选考勤
   */
  function filterByMonth(year: number, month: number): Attendance[] {
    return attendances.value.filter(item => {
      const date = new Date(item.created_at)
      return date.getFullYear() === year && date.getMonth() + 1 === month
    })
  }

  /**
   * 获取最近考勤记录
   */
  function getRecentRecords(limit: number = 5): Attendance[] {
    return attendances.value
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, limit)
  }

  /**
   * 清除所有数据
   */
  function clearAll() {
    attendances.value = []
    statistics.value = null
  }

  return {
    // 状态
    attendances,
    statistics,
    loading,

    // 计算属性
    totalCount,
    presentCount,
    leaveCount,
    absentCount,
    lateCount,
    presentRate,

    // 方法
    fetchAttendances,
    fetchMyAttendances,
    fetchStatistics,
    fetchAttendanceDetail,
    filterByStatus,
    filterByMonth,
    getRecentRecords,
    clearAll
  }
})
