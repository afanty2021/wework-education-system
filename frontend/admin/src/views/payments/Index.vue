<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Payment, PaymentStatus, PaymentListParams } from '@/api/payments'
import { getPayments, createPayment, confirmPayment, refundPayment } from '@/api/payments'

const loading = ref(false)
const paymentList = ref<Payment[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增缴费')
const isEdit = ref(false)
const formRef = ref()

const queryParams = reactive<PaymentListParams>({
  page: 1,
  pageSize: 10,
  contract_id: undefined,
  status: null,
  payment_method: null,
})

const formData = reactive({
  id: 0,
  payment_no: '',
  contract_id: 0,
  amount: 0,
  payment_method: 1,
  remark: '',
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '待确认', value: 1 },
  { label: '已确认', value: 2 },
  { label: '已退款', value: 3 },
]

const methodOptions = [
  { label: '微信', value: 1 },
  { label: '支付宝', value: 2 },
  { label: '现金', value: 3 },
  { label: '银行卡', value: 4 },
  { label: '转账', value: 5 },
]

const rules = {
  payment_no: [{ required: true, message: '请输入缴费编号', trigger: 'blur' }],
  contract_id: [{ required: true, message: '请选择合同', trigger: 'change' }],
  amount: [{ required: true, message: '请输入缴费金额', trigger: 'blur' }],
  payment_method: [{ required: true, message: '请选择支付方式', trigger: 'change' }],
}

async function fetchPaymentList() {
  loading.value = true
  try {
    const data = await getPayments({
      skip: (queryParams.page - 1) * queryParams.pageSize,
      limit: queryParams.pageSize,
      contract_id: queryParams.contract_id,
      status: queryParams.status || undefined,
      payment_method: queryParams.payment_method || undefined,
    })
    paymentList.value = data
    total.value = data.length
  } catch { ElMessage.error('获取缴费列表失败') }
  finally { loading.value = false }
}

function handleSearch() { queryParams.page = 1; fetchPaymentList() }
function handleReset() { queryParams.contract_id = undefined; queryParams.status = null; queryParams.payment_method = null; queryParams.page = 1; fetchPaymentList() }
function handlePageChange(page: number) { queryParams.page = page; fetchPaymentList() }
function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchPaymentList() }

function handleAdd() {
  dialogTitle.value = '新增缴费'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

async function handleConfirm(row: Payment) {
  try {
    await ElMessageBox.confirm(`确定要确认缴费"${row.payment_no}"吗？`, '提示', { type: 'warning' })
    await confirmPayment(row.id, { actual_amount: row.amount })
    ElMessage.success('确认成功')
    fetchPaymentList()
  } catch {}
}

async function handleRefund(row: Payment) {
  try {
    await ElMessageBox.confirm(`确定要退款"${row.payment_no}"吗？`, '提示', { type: 'warning' })
    await refundPayment(row.id, { refund_amount: row.amount, refund_reason: '客户申请退款' })
    ElMessage.success('退款成功')
    fetchPaymentList()
  } catch {}
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    await createPayment(formData)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    fetchPaymentList()
  } catch { ElMessage.error('操作失败') }
}

function resetForm() {
  Object.assign(formData, { id: 0, payment_no: '', contract_id: 0, amount: 0, payment_method: 1, remark: '' })
  formRef.value?.resetFields()
}

function formatStatus(status: number): string { const map = { 1: '待确认', 2: '已确认', 3: '已退款' }; return map[status] || '未知' }
function formatMethod(method: number): string { const map = { 1: '微信', 2: '支付宝', 3: '现金', 4: '银行卡', 5: '转账' }; return map[method] || '未知' }
function formatAmount(amount: number): string { return `¥${amount.toFixed(2)}` }

onMounted(() => fetchPaymentList())
</script>

<template>
  <div class="payment-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="缴费编号">
          <el-input v-model="queryParams.payment_no" placeholder="请输入缴费编号" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option v-for="item in statusOptions.slice(1)" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付方式">
          <el-select v-model="queryParams.payment_method" placeholder="请选择支付方式" clearable style="width: 140px">
            <el-option v-for="item in methodOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="operation-card">
      <template #header>
        <div class="card-header">
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>新增缴费</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="paymentList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="payment_no" label="缴费编号" min-width="150" />
        <el-table-column prop="student_name" label="学员姓名" width="100" />
        <el-table-column label="缴费金额" width="120" formatter="(row) => formatAmount(row.amount)" />
        <el-table-column prop="payment_method" label="支付方式" width="100" formatter="(row) => formatMethod(row.payment_method)" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 2 ? 'success' : row.status === 3 ? 'warning' : 'info'">{{ formatStatus(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button v-if="row.status === 1" type="success" link size="small" @click="handleConfirm(row)">确认</el-button>
            <el-button v-if="row.status === 2" type="warning" link size="small" @click="handleRefund(row)">退款</el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <Pagination :total="total" :page="queryParams.page" :page-size="queryParams.pageSize" @page-change="handlePageChange" @size-change="handleSizeChange" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="缴费编号" prop="payment_no">
          <el-input v-model="formData.payment_no" placeholder="请输入缴费编号" />
        </el-form-item>
        <el-form-item label="合同" prop="contract_id">
          <el-select v-model="formData.contract_id" placeholder="请选择合同" style="width: 100%">
            <el-option label="合同-2024001" :value="1" />
            <el-option label="合同-2024002" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="缴费金额" prop="amount">
          <el-input-number v-model="formData.amount" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="支付方式" prop="payment_method">
          <el-select v-model="formData.payment_method" placeholder="请选择支付方式" style="width: 100%">
            <el-option v-for="item in methodOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import Pagination from '@/components/Pagination.vue'
import { getPayments, createPayment, confirmPayment, refundPayment } from '@/api/payments'
import type { Payment } from '@/api/payments'

export default defineComponent({
  name: 'PaymentIndex',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const paymentList = ref<Payment[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增缴费')
    const isEdit = ref(false)
    const formRef = ref()

    const queryParams = reactive<PaymentListParams>({ page: 1, pageSize: 10, contract_id: undefined, status: null, payment_method: null })

    const formData = reactive({ id: 0, payment_no: '', contract_id: 0, amount: 0, payment_method: 1, remark: '' })

    const statusOptions = [{ label: '全部', value: null }, { label: '待确认', value: 1 }, { label: '已确认', value: 2 }, { label: '已退款', value: 3 }]
    const methodOptions = [{ label: '微信', value: 1 }, { label: '支付宝', value: 2 }, { label: '现金', value: 3 }, { label: '银行卡', value: 4 }, { label: '转账', value: 5 }]

    const rules = { payment_no: [{ required: true, message: '请输入缴费编号', trigger: 'blur' }], contract_id: [{ required: true, message: '请选择合同', trigger: 'change' }], amount: [{ required: true, message: '请输入缴费金额', trigger: 'blur' }], payment_method: [{ required: true, message: '请选择支付方式', trigger: 'change' }] }

    async function fetchPaymentList() {
      loading.value = true
      try {
        const data = await getPayments(queryParams)
        paymentList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取缴费列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchPaymentList() }
    function handleReset() { queryParams.contract_id = undefined; queryParams.status = null; queryParams.payment_method = null; queryParams.page = 1; fetchPaymentList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchPaymentList() }
    function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchPaymentList() }
    function handleAdd() { dialogTitle.value = '新增缴费'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    async function handleConfirm(row: Payment) {
      try {
        await ElMessageBox.confirm(`确定要确认缴费"${row.payment_no}"吗？`, '提示', { type: 'warning' })
        await confirmPayment(row.id, { actual_amount: row.amount })
        ElMessage.success('确认成功')
        fetchPaymentList()
      } catch {}
    }
    async function handleRefund(row: Payment) {
      try {
        await ElMessageBox.confirm(`确定要退款"${row.payment_no}"吗？`, '提示', { type: 'warning' })
        await refundPayment(row.id, { refund_amount: row.amount, refund_reason: '客户申请退款' })
        ElMessage.success('退款成功')
        fetchPaymentList()
      } catch {}
    }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        await createPayment(formData)
        ElMessage.success('创建成功')
        dialogVisible.value = false
        fetchPaymentList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, payment_no: '', contract_id: 0, amount: 0, payment_method: 1, remark: '' }) }
    function formatStatus(status: number): string { const map = { 1: '待确认', 2: '已确认', 3: '已退款' }; return map[status] || '未知' }
    function formatMethod(method: number): string { const map = { 1: '微信', 2: '支付宝', 3: '现金', 4: '银行卡', 5: '转账' }; return map[method] || '未知' }
    function formatAmount(amount: number): string { return `¥${amount.toFixed(2)}` }

    onMounted(() => fetchPaymentList())

    return { loading, paymentList, total, queryParams, statusOptions, methodOptions, formData, rules, dialogVisible, dialogTitle, isEdit, formRef, handleSearch, handleReset, handlePageChange, handleSizeChange, handleAdd, handleConfirm, handleRefund, handleSubmit, formatStatus, formatMethod, formatAmount }
  },
})
</script>

<style lang="scss" scoped>
.payment-manage { .search-card { margin-bottom: 16px; } .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
