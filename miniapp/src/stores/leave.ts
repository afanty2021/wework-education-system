/**
 * 请假状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import LeaveAPI, {
  type Attendance,
  type LeaveListParams,
  type LeaveStats,
  AttendanceStatus
} from '@/api/leave'

/**
 * 请假状态管理
 */
export const useLeaveStore = defineStore('leave', () => {
  // 状态
  const leaves = ref<Attendance[]>([])
  const currentLeave = ref<Attendance | null>(null)
  const loading = ref(false)
  const stats = ref<LeaveStats>({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0
  })

  // 计算属性
  /**
   * 待审核请假列表
   */
  const pendingLeaves = computed(() =>
    leaves.value.filter(l => l.status === AttendanceStatus.LEAVE && !l.check_time)
  )

  /**
   * 已通过请假列表
   */
  const approvedLeaves = computed(() =>
    leaves.value.filter(l => l.status === AttendanceStatus.LEAVE && l.check_time)
  )

  /**
   * 获取请假列表
   */
  async function fetchLeaves(params?: LeaveListParams) {
    loading.value = true
    try {
      const result = await LeaveAPI.list(params)
      leaves.value = result
      return result
    } catch (error) {
      console.error('获取请假列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取请假详情
   */
  async function fetchLeaveDetail(attendanceId: number) {
    loading.value = true
    try {
      const result = await LeaveAPI.getById(attendanceId)
      currentLeave.value = result
      return result
    } catch (error) {
      console.error('获取请假详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取我的请假列表
   */
  async function fetchMyLeaves(params?: LeaveListParams) {
    loading.value = true
    try {
      const result = await LeaveAPI.getMyLeaves(params)
      leaves.value = result
      return result
    } catch (error) {
      console.error('获取我的请假列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 申请请假
   */
  async function applyLeave(data: {
    schedule_id: number
    student_id: number
    leave_date: string
    reason: string
    hours?: number
  }) {
    loading.value = true
    try {
      const result = await LeaveAPI.apply(data)
      // 添加到列表开头
      leaves.value.unshift(result)
      return result
    } catch (error) {
      console.error('申请请假失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 取消请假
   */
  async function cancelLeave(attendanceId: number) {
    loading.value = true
    try {
      await LeaveAPI.cancel(attendanceId)
      // 从列表中移除
      leaves.value = leaves.value.filter(l => l.id !== attendanceId)
    } catch (error) {
      console.error('取消请假失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 统计请假
   */
  async function fetchStats(studentId?: number) {
    try {
      const result = await LeaveAPI.getStats(studentId)
      stats.value = result
      return result
    } catch (error) {
      console.error('获取请假统计失败:', error)
      throw error
    }
  }

  /**
   * 清除当前请假
   */
  function clearCurrentLeave() {
    currentLeave.value = null
  }

  /**
   * 清除所有请假数据
   */
  function clearAll() {
    leaves.value = []
    currentLeave.value = null
  }

  return {
    // 状态
    leaves,
    currentLeave,
    loading,
    stats,

    // 计算属性
    pendingLeaves,
    approvedLeaves,

    // 方法
    fetchLeaves,
    fetchLeaveDetail,
    fetchMyLeaves,
    applyLeave,
    cancelLeave,
    fetchStats,
    clearCurrentLeave,
    clearAll
  }
})
