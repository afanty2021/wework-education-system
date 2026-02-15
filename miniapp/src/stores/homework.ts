/**
 * 作业状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import HomeworkAPI, { type Homework, HomeworkSubmitStatus } from '@/api/homework'

/**
 * 作业状态管理
 */
export const useHomeworkStore = defineStore('homework', () => {
  // 状态
  const homeworks = ref<Homework[]>([])
  const currentHomework = ref<Homework | null>(null)
  const loading = ref(false)

  // 计算属性
  const totalCount = computed(() => homeworks.value.length)
  const pendingCount = computed(() =>
    homeworks.value.filter(h => !h.submission || h.submission.score === null).length
  )
  const submittedCount = computed(() =>
    homeworks.value.filter(h => h.submission && h.submission.score !== null).length
  )

  /**
   * 获取作业列表
   */
  async function fetchHomeworks(params?: Parameters<typeof HomeworkAPI.list>[0]) {
    loading.value = true
    try {
      const result = await HomeworkAPI.list(params)
      homeworks.value = result
      return result
    } catch (error) {
      console.error('获取作业列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取我的作业
   */
  async function fetchMyHomeworks(params?: Partial<Parameters<typeof HomeworkAPI.list>[0]>) {
    loading.value = true
    try {
      const result = await HomeworkAPI.getMyHomeworks(params)
      homeworks.value = result
      return result
    } catch (error) {
      console.error('获取我的作业失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取待完成作业
   */
  async function fetchPendingHomeworks() {
    loading.value = true
    try {
      const result = await HomeworkAPI.getPendingHomeworks()
      // 只保留未提交的作业
      homeworks.value = result.filter(h => !h.submission)
      return homeworks.value
    } catch (error) {
      console.error('获取待完成作业失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取作业详情
   */
  async function fetchHomeworkDetail(homeworkId: number) {
    loading.value = true
    try {
      const result = await HomeworkAPI.getById(homeworkId)
      currentHomework.value = result

      // 更新列表中的记录
      const index = homeworks.value.findIndex(item => item.id === homeworkId)
      if (index !== -1) {
        homeworks.value[index] = result
      }

      return result
    } catch (error) {
      console.error('获取作业详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 提交作业
   */
  async function submitHomework(homeworkId: number, content: string, attachments?: string[]) {
    loading.value = true
    try {
      const result = await HomeworkAPI.submit(homeworkId, { homeworkId, content, attachments })

      // 更新当前作业
      if (currentHomework.value?.id === homeworkId) {
        currentHomework.value.submission = result
      }

      // 更新列表中的作业
      const index = homeworks.value.findIndex(item => item.id === homeworkId)
      if (index !== -1) {
        homeworks.value[index].submission = result
      }

      return result
    } catch (error) {
      console.error('提交作业失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 按课程筛选作业
   */
  function filterByCourse(courseId: number): Homework[] {
    return homeworks.value.filter(h => h.course_id === courseId)
  }

  /**
   * 按状态筛选作业
   */
  function filterByStatus(status: HomeworkSubmitStatus): Homework[] {
    return homeworks.value.filter(h => {
      if (status === HomeworkSubmitStatus.NOT_SUBMITTED) {
        return !h.submission || h.submission.score === null
      }
      if (status === HomeworkSubmitStatus.SUBMITTED) {
        return h.submission && h.submission.score === null
      }
      return h.submission && h.submission.score !== null
    })
  }

  /**
   * 获取即将到期的作业
   */
  function getDueSoonHomeworks(days: number = 3): Homework[] {
    const now = new Date()
    const futureDate = new Date(now.getTime() + days * 24 * 60 * 60 * 1000)

    return homeworks.value.filter(h => {
      if (!h.due_date || h.submission) return false
      const dueDate = new Date(h.due_date)
      return dueDate >= now && dueDate <= futureDate
    })
  }

  /**
   * 获取已过期作业
   */
  function getExpiredHomeworks(): Homework[] {
    const now = new Date()
    return homeworks.value.filter(h => {
      if (!h.due_date || h.submission) return false
      return new Date(h.due_date) < now
    })
  }

  /**
   * 清除当前作业
   */
  function clearCurrentHomework() {
    currentHomework.value = null
  }

  /**
   * 清除所有数据
   */
  function clearAll() {
    homeworks.value = []
    currentHomework.value = null
  }

  return {
    // 状态
    homeworks,
    currentHomework,
    loading,

    // 计算属性
    totalCount,
    pendingCount,
    submittedCount,

    // 方法
    fetchHomeworks,
    fetchMyHomeworks,
    fetchPendingHomeworks,
    fetchHomeworkDetail,
    submitHomework,
    filterByCourse,
    filterByStatus,
    getDueSoonHomeworks,
    getExpiredHomeworks,
    clearCurrentHomework,
    clearAll
  }
})
