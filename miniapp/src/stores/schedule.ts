/**
 * 课表状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ScheduleAPI, { type Schedule } from '@/api/schedule'

/**
 * 课表状态管理
 */
export const useScheduleStore = defineStore('schedule', () => {
  // 状态
  const schedules = ref<Schedule[]>([])
  const todaySchedules = ref<Schedule[]>([])
  const weekSchedules = ref<Schedule[]>([])
  const currentSchedule = ref<Schedule | null>(null)
  const loading = ref(false)
  const currentWeekStart = ref<string>('')

  /**
   * 获取今日课表
   */
  async function fetchTodaySchedules() {
    loading.value = true
    try {
      const result = await ScheduleAPI.getTodaySchedules()
      todaySchedules.value = result
      return result
    } catch (error) {
      console.error('获取今日课表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取本周课表
   */
  async function fetchWeekSchedules(weekStart?: string) {
    loading.value = true
    try {
      const result = await ScheduleAPI.getWeekSchedules(weekStart)
      weekSchedules.value = result
      currentWeekStart.value = weekStart || new Date().toISOString()
      return result
    } catch (error) {
      console.error('获取本周课表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取课表列表
   */
  async function fetchSchedules(params?: Parameters<typeof ScheduleAPI.list>[0]) {
    loading.value = true
    try {
      const result = await ScheduleAPI.list(params)
      schedules.value = result
      return result
    } catch (error) {
      console.error('获取课表列表失败:', error)
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
      const result = await ScheduleAPI.getById(scheduleId)
      currentSchedule.value = result
      return result
    } catch (error) {
      console.error('获取课表详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 按日期筛选课表
   */
  function filterSchedulesByDate(date: string): Schedule[] {
    return schedules.value.filter(item => {
      const scheduleDate = new Date(item.start_time).toISOString().split('T')[0]
      return scheduleDate === date
    })
  }

  /**
   * 按星期几筛选课表
   */
  function filterSchedulesByWeekday(weekday: number): Schedule[] {
    return weekSchedules.value.filter(item => {
      return item.week_day === weekday
    })
  }

  /**
   * 清除当前课表
   */
  function clearCurrentSchedule() {
    currentSchedule.value = null
  }

  /**
   * 清除所有课表数据
   */
  function clearAll() {
    schedules.value = []
    todaySchedules.value = []
    weekSchedules.value = []
    currentSchedule.value = null
  }

  return {
    // 状态
    schedules,
    todaySchedules,
    weekSchedules,
    currentSchedule,
    loading,
    currentWeekStart,

    // 方法
    fetchTodaySchedules,
    fetchWeekSchedules,
    fetchSchedules,
    fetchScheduleDetail,
    filterSchedulesByDate,
    filterSchedulesByWeekday,
    clearCurrentSchedule,
    clearAll
  }
})
