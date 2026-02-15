/**
 * 缴费状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import PaymentAPI, {
  type Payment,
  type PaymentListParams,
  type PaymentStats,
  PaymentStatus
} from '@/api/payment'

/**
 * 缴费状态管理
 */
export const usePaymentStore = defineStore('payment', () => {
  // 状态
  const payments = ref<Payment[]>([])
  const currentPayment = ref<Payment | null>(null)
  const loading = ref(false)
  const stats = ref<PaymentStats>({
    total_pending: 0,
    total_confirmed: 0,
    total_refunded: 0,
    total_amount: 0
  })

  // 计算属性
  /**
   * 待缴费列表
   */
  const pendingPayments = computed(() =>
    payments.value.filter(p => p.status === PaymentStatus.PENDING)
  )

  /**
   * 已缴费列表
   */
  const confirmedPayments = computed(() =>
    payments.value.filter(p => p.status === PaymentStatus.CONFIRMED)
  )

  /**
   * 已退款列表
   */
  const refundedPayments = computed(() =>
    payments.value.filter(p => p.status === PaymentStatus.REFUNDED)
  )

  /**
   * 待缴费总金额
   */
  const totalPendingAmount = computed(() =>
    pendingPayments.value.reduce((sum, p) => sum + Number(p.amount), 0)
  )

  /**
   * 获取缴费列表
   */
  async function fetchPayments(params?: PaymentListParams) {
    loading.value = true
    try {
      const result = await PaymentAPI.list(params)
      payments.value = result
      return result
    } catch (error) {
      console.error('获取缴费列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取缴费详情
   */
  async function fetchPaymentDetail(paymentId: number) {
    loading.value = true
    try {
      const result = await PaymentAPI.getById(paymentId)
      currentPayment.value = result
      return result
    } catch (error) {
      console.error('获取缴费详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取我的缴费列表
   */
  async function fetchMyPayments(params?: PaymentListParams) {
    loading.value = true
    try {
      const result = await PaymentAPI.getMyPayments(params)
      payments.value = result
      return result
    } catch (error) {
      console.error('获取我的缴费列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取待缴费列表
   */
  async function fetchPendingPayments() {
    loading.value = true
    try {
      const result = await PaymentAPI.getPendingPayments()
      payments.value = result
      return result
    } catch (error) {
      console.error('获取待缴费列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取已缴费列表
   */
  async function fetchConfirmedPayments() {
    loading.value = true
    try {
      const result = await PaymentAPI.getConfirmedPayments()
      payments.value = result
      return result
    } catch (error) {
      console.error('获取已缴费列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 统计缴费
   */
  async function fetchStats() {
    try {
      const [pending, confirmed, refunded] = await Promise.all([
        PaymentAPI.count({ status: PaymentStatus.PENDING }),
        PaymentAPI.count({ status: PaymentStatus.CONFIRMED }),
        PaymentAPI.count({ status: PaymentStatus.REFUNDED })
      ])

      stats.value = {
        total_pending: pending.count,
        total_confirmed: confirmed.count,
        total_refunded: refunded.count,
        total_amount: 0
      }
      return stats.value
    } catch (error) {
      console.error('获取缴费统计失败:', error)
      throw error
    }
  }

  /**
   * 清除当前缴费
   */
  function clearCurrentPayment() {
    currentPayment.value = null
  }

  /**
   * 清除所有缴费数据
   */
  function clearAll() {
    payments.value = []
    currentPayment.value = null
  }

  return {
    // 状态
    payments,
    currentPayment,
    loading,
    stats,

    // 计算属性
    pendingPayments,
    confirmedPayments,
    refundedPayments,
    totalPendingAmount,

    // 方法
    fetchPayments,
    fetchPaymentDetail,
    fetchMyPayments,
    fetchPendingPayments,
    fetchConfirmedPayments,
    fetchStats,
    clearCurrentPayment,
    clearAll
  }
})
