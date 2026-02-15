<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Contract, ContractStatus, ContractListParams } from '@/api/contracts'
import { getContracts, createContract, updateContract, deleteContract } from '@/api/contracts'

const loading = ref(false)
const contractList = ref<Contract[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增合同')
const isEdit = ref(false)
const formRef = ref()

const queryParams = reactive<ContractListParams>({
  page: 1,
  pageSize: 10,
  student_id: undefined,
  course_id: undefined,
  status: null,
})

const formData = reactive({
  id: 0,
  contract_no: '',
  student_id: 0,
  course_id: undefined as number | undefined,
  total_hours: 20,
  unit_price: 100,
  discount_amount: 0,
  status: 1,
  start_date: '',
  end_date: '',
  remark: '',
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '生效', value: 1 },
  { label: '完结', value: 2 },
  { label: '退费', value: 3 },
  { label: '过期', value: 4 },
]

const rules = {
  contract_no: [{ required: true, message: '请输入合同编号', trigger: 'blur' }],
  student_id: [{ required: true, message: '请选择学员', trigger: 'change' }],
  total_hours: [{ required: true, message: '请输入总课时', trigger: 'blur' }],
  unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
}

async function fetchContractList() {
  loading.value = true
  try {
    const data = await getContracts({
      skip: (queryParams.page - 1) * queryParams.pageSize,
      limit: queryParams.pageSize,
      student_id: queryParams.student_id,
      course_id: queryParams.course_id,
      status: queryParams.status || undefined,
    })
    contractList.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('获取合同列表失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() { queryParams.page = 1; fetchContractList() }
function handleReset() { queryParams.student_id = undefined; queryParams.course_id = undefined; queryParams.status = null; queryParams.page = 1; fetchContractList() }
function handlePageChange(page: number) { queryParams.page = page; fetchContractList() }
function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchContractList() }

function handleAdd() {
  dialogTitle.value = '新增合同'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: Contract) {
  dialogTitle.value = '编辑合同'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function handleDelete(row: Contract) {
  try {
    await ElMessageBox.confirm(`确定要删除合同"${row.contract_no}"吗？`, '提示', { type: 'warning' })
    await deleteContract(row.id)
    ElMessage.success('删除成功')
    fetchContractList()
  } catch {}
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateContract(formData.id, formData)
    else await createContract(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchContractList()
  } catch { ElMessage.error('操作失败') }
}

function resetForm() {
  Object.assign(formData, { id: 0, contract_no: '', student_id: 0, course_id: undefined, total_hours: 20, unit_price: 100, discount_amount: 0, status: 1, start_date: '', end_date: '', remark: '' })
  formRef.value?.resetFields()
}

function formatStatus(status: number): string {
  const map = { 1: '生效', 2: '完结', 3: '退费', 4: '过期' }
  return map[status] || '未知'
}

function formatAmount(amount: number): string {
  return `¥${amount.toFixed(2)}`
}

onMounted(() => fetchContractList())
</script>

<template>
  <div class="contract-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="合同编号">
          <el-input v-model="queryParams.contract_no" placeholder="请输入合同编号" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option v-for="item in statusOptions.slice(1)" :key="item.value" :label="item.label" :value="item.value" />
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
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>新增合同</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="contractList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="contract_no" label="合同编号" min-width="150" />
        <el-table-column prop="student_name" label="学员姓名" width="100" />
        <el-table-column prop="course_name" label="课程名称" width="120" />
        <el-table-column prop="total_hours" label="总课时" width="80" />
        <el-table-column prop="remaining_hours" label="剩余课时" width="90" />
        <el-table-column label="总金额" width="100" formatter="(row) => formatAmount(row.total_amount)" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : row.status === 2 ? 'info' : row.status === 3 ? 'warning' : 'danger'">{{ formatStatus(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="end_date" label="到期日期" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <Pagination :total="total" :page="queryParams.page" :page-size="queryParams.pageSize" @page-change="handlePageChange" @size-change="handleSizeChange" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="合同编号" prop="contract_no">
              <el-input v-model="formData.contract_no" placeholder="请输入合同编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学员" prop="student_id">
              <el-select v-model="formData.student_id" placeholder="请选择学员" style="width: 100%">
                <el-option label="张三" :value="1" />
                <el-option label="李四" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="课程">
              <el-select v-model="formData.course_id" placeholder="请选择课程" style="width: 100%" clearable>
                <el-option label="Python入门" :value="1" />
                <el-option label="Java进阶" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总课时" prop="total_hours">
              <el-input-number v-model="formData.total_hours" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单价" prop="unit_price">
              <el-input-number v-model="formData.unit_price" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="折扣金额">
              <el-input-number v-model="formData.discount_amount" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="开始日期">
              <el-date-picker v-model="formData.start_date" type="date" placeholder="请选择开始日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期">
              <el-date-picker v-model="formData.end_date" type="date" placeholder="请选择结束日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
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
import { getContracts, createContract, updateContract, deleteContract } from '@/api/contracts'
import type { Contract } from '@/api/contracts'

export default defineComponent({
  name: 'ContractIndex',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const contractList = ref<Contract[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增合同')
    const isEdit = ref(false)
    const formRef = ref()

    const queryParams = reactive({ page: 1, pageSize: 10, student_id: undefined, course_id: undefined, status: null as number | null })

    const formData = reactive({ id: 0, contract_no: '', student_id: 0, course_id: undefined as number | undefined, total_hours: 20, unit_price: 100, discount_amount: 0, status: 1, start_date: '', end_date: '', remark: '' })

    const statusOptions = [
      { label: '全部', value: null },
      { label: '生效', value: 1 },
      { label: '完结', value: 2 },
      { label: '退费', value: 3 },
      { label: '过期', value: 4 },
    ]

    const rules = { contract_no: [{ required: true, message: '请输入合同编号', trigger: 'blur' }], student_id: [{ required: true, message: '请选择学员', trigger: 'change' }], total_hours: [{ required: true, message: '请输入总课时', trigger: 'blur' }], unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }] }

    async function fetchContractList() {
      loading.value = true
      try {
        const data = await getContracts(queryParams)
        contractList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取合同列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchContractList() }
    function handleReset() { queryParams.student_id = undefined; queryParams.course_id = undefined; queryParams.status = null; queryParams.page = 1; fetchContractList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchContractList() }
    function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchContractList() }
    function handleAdd() { dialogTitle.value = '新增合同'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    function handleEdit(row: Contract) { dialogTitle.value = '编辑合同'; isEdit.value = true; Object.assign(formData, row); dialogVisible.value = true }
    async function handleDelete(row: Contract) {
      try {
        await ElMessageBox.confirm(`确定要删除合同"${row.contract_no}"吗？`, '提示', { type: 'warning' })
        await deleteContract(row.id)
        ElMessage.success('删除成功')
        fetchContractList()
      } catch {}
    }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateContract(formData.id, formData)
        else await createContract(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchContractList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, contract_no: '', student_id: 0, course_id: undefined, total_hours: 20, unit_price: 100, discount_amount: 0, status: 1, start_date: '', end_date: '', remark: '' }) }
    function formatStatus(status: number): string { const map = { 1: '生效', 2: '完结', 3: '退费', 4: '过期' }; return map[status] || '未知' }
    function formatAmount(amount: number): string { return `¥${amount.toFixed(2)}` }

    onMounted(() => fetchContractList())

    return { loading, contractList, total, queryParams, statusOptions, formData, rules, dialogVisible, dialogTitle, isEdit, formRef, handleSearch, handleReset, handlePageChange, handleSizeChange, handleAdd, handleEdit, handleDelete, handleSubmit, formatStatus, formatAmount }
  },
})
</script>

<style lang="scss" scoped>
.contract-manage { .search-card { margin-bottom: 16px; } .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
