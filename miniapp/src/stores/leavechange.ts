/**
 * 调课状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import LeaveChangeAPI, {
  type LeaveChange,
  type LeaveChangeListParams,
  type LeaveChangeStats,
  LeaveChangeStatus
} from '@/api/leavechange'

/**
 * 调课状态管理
 */
export const useLeaveChangeStore = defineStore('leavechange', () => {
  // 状态
  const leaveChanges = ref<LeaveChange[]>([])
  const currentLeaveChange = ref<LeaveChange | null>(null)
  const loading = ref(false)
  const stats = ref<LeaveChangeStats>({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0
  })

  // 计算属性
  /**
   * 待审核调课列表
   */
  const pendingLeaveChanges = computed(() =>
    leaveChanges.value.filter(lc => lc.status === LeaveChangeStatus.PENDING)
  )

  /**
   * 已通过调课列表
   */
  const approvedLeaveChanges = computed(() =>
    leaveChanges.value.filter(lc => lc.status === LeaveChangeStatus.APPROVED)
  )

  /**
   * 已拒绝调课列表
   */
  const rejectedLeaveChanges = computed(() =>
    leaveChanges.value.filter(lc => lc.status === LeaveChangeStatus.REJECTED)
  )

  /**
   * 获取调课列表
   */
  async function fetchLeaveChanges(params?: LeaveChangeListParams) {
    loading.value = true
    try {
      const result = await LeaveChangeAPI.list(params)
      leaveChanges.value = result
      return result
    } catch (error) {
      console.error('获取调课列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取调课详情
   */
  async function fetchLeaveChangeDetail(leaveChangeId: number) {
    loading.value = true
    try {
      const result = await LeaveChangeAPI.getById(leaveChangeId)
      currentLeaveChange.value = result
      return result
    } catch (error) {
      console.error('获取调课详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取我的调课列表
   */
  async function fetchMyLeaveChanges(params?: LeaveChangeListParams) {
    loading.value = true
    try {
      const result = await LeaveChangeAPI.getMyLeaveChanges(params)
      leaveChanges.value = result
      return result
    } catch (error) {
      console.error('获取我的调课列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 申请调课
   */
  async function applyLeaveChange(data: {
    student_id: number
    original_schedule_id: number
    target_schedule_id?: number
    target_date?: string
    reason: string
  }) {
    loading.value = true
    try {
      const result = await LeaveChangeAPI.apply(data)
      // 添加到列表开头
      leaveChanges.value.unshift(result)
      return result
    } catch (error) {
      console.error('申请调课失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 取消调课
   */
  async function cancelLeaveChange(leaveChangeId: number) {
    loading.value = true
    try {
      await LeaveChangeAPI.cancel(leaveChangeId)
      // 更新状态为已取消
      const index = leaveChanges.value.findIndex(lc => lc.id === leaveChangeId)
      if (index !== -1) {
        leaveChanges.value[index].status = LeaveChangeStatus.CANCELLED
      }
    } catch (error) {
      console.error('取消调课失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 统计调课
   */
  async function fetchStats(studentId?: number) {
    try {
      const result = await LeaveChangeAPI.getStats(studentId)
      stats.value = result
      return result
    } catch (error) {
      console.error('获取调课统计失败:', error)
      throw error
    }
  }

  /**
   * 清除当前调课
   */
  function clearCurrentLeaveChange() {
    currentLeaveChange.value = null
  }

  /**
   * 清除所有调课数据
   */
  function clearAll() {
    leaveChanges.value = []
    currentLeaveChange.value = null
  }

  return {
    // 状态
    leaveChanges,
    currentLeaveChange,
    loading,
    stats,

    // 计算属性
    pendingLeaveChanges,
    approvedLeaveChanges,
    rejectedLeaveChanges,

    // 方法
    fetchLeaveChanges,
    fetchLeaveChangeDetail,
    fetchMyLeaveChanges,
    applyLeaveChange,
    cancelLeaveChange,
    fetchStats,
    clearCurrentLeaveChange,
    clearAll
  }
})
