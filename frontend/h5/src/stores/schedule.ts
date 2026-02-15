/**
 * 课表状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getTodaySchedules, getWeekSchedules, getScheduleDetail, getScheduleStudents, type ScheduleResponse } from '@/api/schedule'
import { useAuthStore } from './auth'

export const useScheduleStore = defineStore('schedule', () => {
  const authStore = useAuthStore()

  // 今日课表
  const todaySchedules = ref<ScheduleResponse[]>([])

  // 周课表
  const weekSchedules = ref<ScheduleResponse[]>([])

  // 当前选中的日期
  const selectedDate = ref<string>(new Date().toISOString().split('T')[0])

  // 当前查看的课表
  const currentSchedule = ref<ScheduleResponse | null>(null)

  // 课表学员名单
  const scheduleStudents = ref<Array<{
    id: number
    name: string
    phone?: string
    parent_phone?: string
  }>>([])

  // 加载状态
  const loading = ref(false)

  // 计算属性
  const teacherId = computed(() => authStore.userId)

  const filteredWeekSchedules = computed(() => {
    return weekSchedules.value.filter((schedule) => {
      const scheduleDate = new Date(schedule.start_time).toISOString().split('T')[0]
      return scheduleDate === selectedDate.value
    })
  })

  /**
   * 获取今日课表
   */
  async function fetchTodaySchedules() {
    loading.value = true
    try {
      todaySchedules.value = await getTodaySchedules(teacherId.value)
    } catch (error) {
      console.error('获取今日课表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取周课表
   */
  async function fetchWeekSchedules(date?: string) {
    loading.value = true
    try {
      weekSchedules.value = await getWeekSchedules(date, teacherId.value)
    } catch (error) {
      console.error('获取周课表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取课表详情
   */
  async function fetchScheduleDetail(scheduleId: number) {
    loading.value = true
    try {
      currentSchedule.value = await getScheduleDetail(scheduleId)
      return currentSchedule.value
    } catch (error) {
      console.error('获取课表详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取课表学员名单
   */
  async function fetchScheduleStudents(scheduleId: number) {
    try {
      const response = await getScheduleStudents(scheduleId)
      scheduleStudents.value = response.students
      return scheduleStudents.value
    } catch (error) {
      console.error('获取学员名单失败:', error)
      throw error
    }
  }

  /**
   * 设置选中日期
   */
  function setSelectedDate(date: string) {
    selectedDate.value = date
  }

  /**
   * 清空状态
   */
  function clearState() {
    todaySchedules.value = []
    weekSchedules.value = []
    currentSchedule.value = null
    scheduleStudents.value = []
    selectedDate.value = new Date().toISOString().split('T')[0]
  }

  return {
    // 状态
    todaySchedules,
    weekSchedules,
    selectedDate,
    currentSchedule,
    scheduleStudents,
    loading,
    // 计算属性
    teacherId,
    filteredWeekSchedules,
    // 方法
    fetchTodaySchedules,
    fetchWeekSchedules,
    fetchScheduleDetail,
    fetchScheduleStudents,
    setSelectedDate,
    clearState,
  }
})
