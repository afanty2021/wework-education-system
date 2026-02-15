<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Attendance, AttendanceStatus, AttendanceListParams } from '@/api/attendance'
import { getAttendances, createAttendance, batchCreateAttendance } from '@/api/attendance'

const loading = ref(false)
const attendanceList = ref<Attendance[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const batchDialogVisible = ref(false)
const formRef = ref()
const batchFormRef = ref()

const queryParams = reactive<AttendanceListParams>({
  page: 1,
  pageSize: 10,
  schedule_id: undefined,
  student_id: undefined,
  status: null,
})

const formData = reactive({
  schedule_id: 0,
  student_id: 0,
  status: 1,
  remark: '',
})

const batchData = reactive({
  schedule_id: 0,
  attendances: [] as Array<{ student_id: number; status: number; remark: string }>,
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '正常出勤', value: 1 },
  { label: '缺勤', value: 2 },
  { label: '迟到', value: 3 },
  { label: '请假', value: 4 },
]

const statusMap = { 1: '正常出勤', 2: '缺勤', 3: '迟到', 4: '请假' }
const statusTypeMap = { 1: 'success', 2: 'danger', 3: 'warning', 4: 'info' }

async function fetchAttendanceList() {
  loading.value = true
  try {
    const data = await getAttendances({
      skip: (queryParams.page - 1) * queryParams.pageSize,
      limit: queryParams.pageSize,
      schedule_id: queryParams.schedule_id,
      student_id: queryParams.student_id,
      status: queryParams.status || undefined,
    })
    attendanceList.value = data
    total.value = data.length
  } catch { ElMessage.error('获取考勤列表失败') }
  finally { loading.value = false }
}

function handleSearch() { queryParams.page = 1; fetchAttendanceList() }
function handleReset() { Object.assign(queryParams, { page: 1, pageSize: 10, schedule_id: undefined, student_id: undefined, status: null }); fetchAttendanceList() }
function handlePageChange(page: number) { queryParams.page = page; fetchAttendanceList() }
function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchAttendanceList() }

function handleAdd() {
  resetForm()
  dialogVisible.value = true
}

function handleBatch() {
  batchData.schedule_id = 0
  batchData.attendances = []
  batchDialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    await createAttendance(formData)
    ElMessage.success('录入成功')
    dialogVisible.value = false
    fetchAttendanceList()
  } catch { ElMessage.error('录入失败') }
}

async function handleBatchSubmit() {
  if (!batchFormRef.value) return
  if (batchData.attendances.length === 0) {
    ElMessage.warning('请添加考勤记录')
    return
  }
  try {
    await batchCreateAttendance(batchData)
    ElMessage.success('批量录入成功')
    batchDialogVisible.value = false
    fetchAttendanceList()
  } catch { ElMessage.error('批量录入失败') }
}

function resetForm() {
  Object.assign(formData, { schedule_id: 0, student_id: 0, status: 1, remark: '' })
  formRef.value?.resetFields()
}

function formatStatus(status: number): string { return statusMap[status] || '未知' }

onMounted(() => fetchAttendanceList())
</script>

<template>
  <div class="attendance-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="排课">
          <el-select v-model="queryParams.schedule_id" placeholder="请选择排课" clearable style="width: 200px">
            <el-option label="Python入门 - 周一 10:00" :value="1" />
            <el-option label="Java进阶 - 周二 14:00" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="学员">
          <el-select v-model="queryParams.student_id" placeholder="请选择学员" clearable style="width: 160px">
            <el-option label="张三" :value="1" />
            <el-option label="李四" :value="2" />
          </el-select>
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
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>录入考勤</el-button>
          <el-button type="success" @click="handleBatch"><el-icon><Document /></el-icon>批量录入</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="attendanceList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="schedule_date" label="排课日期" width="120" />
        <el-table-column prop="student_name" label="学员姓名" width="100" />
        <el-table-column label="考勤状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTypeMap[row.status]">{{ formatStatus(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="check_in_time" label="签到时间" width="120" />
        <el-table-column prop="check_out_time" label="签退时间" width="120" />
        <el-table-column prop="duration" label="出勤时长" width="100">
          <template #default="{ row }">{{ row.duration || '-' }}分钟</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180" />
      </el-table>

      <div class="pagination-wrapper">
        <Pagination :total="total" :page="queryParams.page" :page-size="queryParams.pageSize" @page-change="handlePageChange" @size-change="handleSizeChange" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" title="录入考勤" width="500px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="formData" label-width="100px">
        <el-form-item label="排课" required>
          <el-select v-model="formData.schedule_id" placeholder="请选择排课" style="width: 100%">
            <el-option label="Python入门 - 周一 10:00" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="学员" required>
          <el-select v-model="formData.student_id" placeholder="请选择学员" style="width: 100%">
            <el-option label="张三" :value="1" />
            <el-option label="李四" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="考勤状态" required>
          <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
            <el-option v-for="(label, key) in statusMap" :key="key" :label="label" :value="Number(key)" />
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

    <el-dialog v-model="batchDialogVisible" title="批量录入考勤" width="700px" :close-on-click-modal="false">
      <el-form ref="batchFormRef" :model="batchData" label-width="100px">
        <el-form-item label="排课" required>
          <el-select v-model="batchData.schedule_id" placeholder="请选择排课" style="width: 100%">
            <el-option label="Python入门 - 周一 10:00" :value="1" />
          </el-select>
        </el-form-item>
        <el-divider content-position="left">考勤记录</el-divider>
        <el-table :data="batchData.attendances" border>
          <el-table-column label="学员" width="150">
            <template #default="{ row, $index }">
              <el-select v-model="row.student_id" placeholder="请选择学员" style="width: 100%">
                <el-option label="张三" :value="1" />
                <el-option label="李四" :value="2" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="150">
            <template #default="{ row }">
              <el-select v-model="row.status" placeholder="请选择状态" style="width: 100%">
                <el-option v-for="(label, key) in statusMap" :key="key" :label="label" :value="Number(key)" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="备注">
            <template #default="{ row }">
              <el-input v-model="row.remark" placeholder="请输入备注" />
            </template>
          </el-table-column>
          <el-table-column width="80">
            <template #default="{ $index }">
              <el-button type="danger" link size="small" @click="batchData.attendances.splice($index, 1)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button type="primary" plain style="margin-top: 16px" @click="batchData.attendances.push({ student_id: 0, status: 1, remark: '' })">
          <el-icon><Plus /></el-icon>添加记录
        </el-button>
      </el-form>
      <template #footer>
        <el-button @click="batchDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBatchSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Document } from '@element-plus/icons-vue'
import Pagination from '@/components/Pagination.vue'
import { getAttendances, createAttendance, batchCreateAttendance } from '@/api/attendance'

export default defineComponent({
  name: 'AttendanceIndex',
  components: { Plus, Document, Pagination },
  setup() {
    const loading = ref(false)
    const attendanceList = ref<any[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const batchDialogVisible = ref(false)
    const formRef = ref()
    const batchFormRef = ref()

    const queryParams = reactive<any>({ page: 1, pageSize: 10, schedule_id: undefined, student_id: undefined, status: null })

    const formData = reactive({ schedule_id: 0, student_id: 0, status: 1, remark: '' })
    const batchData = reactive({ schedule_id: 0, attendances: [] as Array<{ student_id: number; status: number; remark: string }> })

    const statusOptions = [{ label: '全部', value: null }, { label: '正常出勤', value: 1 }, { label: '缺勤', value: 2 }, { label: '迟到', value: 3 }, { label: '请假', value: 4 }]
    const statusMap = { 1: '正常出勤', 2: '缺勤', 3: '迟到', 4: '请假' }
    const statusTypeMap = { 1: 'success', 2: 'danger', 3: 'warning', 4: 'info' }

    async function fetchAttendanceList() {
      loading.value = true
      try {
        const data = await getAttendances(queryParams)
        attendanceList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取考勤列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchAttendanceList() }
    function handleReset() { Object.assign(queryParams, { page: 1, pageSize: 10, schedule_id: undefined, student_id: undefined, status: null }); fetchAttendanceList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchAttendanceList() }
    function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchAttendanceList() }
    function handleAdd() { resetForm(); dialogVisible.value = true }
    function handleBatch() { Object.assign(batchData, { schedule_id: 0, attendances: [] }); batchDialogVisible.value = true }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await createAttendance(formData)
        ElMessage.success('录入成功')
        dialogVisible.value = false
        fetchAttendanceList()
      } catch { ElMessage.error('录入失败') }
    }
    async function handleBatchSubmit() {
      if (batchData.attendances.length === 0) { ElMessage.warning('请添加考勤记录'); return }
      try {
        await batchCreateAttendance(batchData)
        ElMessage.success('批量录入成功')
        batchDialogVisible.value = false
        fetchAttendanceList()
      } catch { ElMessage.error('批量录入失败') }
    }
    function resetForm() { Object.assign(formData, { schedule_id: 0, student_id: 0, status: 1, remark: '' }) }
    function formatStatus(status: number): string { return statusMap[status] || '未知' }

    onMounted(() => fetchAttendanceList())

    return { loading, attendanceList, total, queryParams, statusOptions, statusMap, statusTypeMap, formData, batchData, dialogVisible, batchDialogVisible, formRef, batchFormRef, handleSearch, handleReset, handlePageChange, handleSizeChange, handleAdd, handleBatch, handleSubmit, handleBatchSubmit, formatStatus }
  },
})
</script>

<style lang="scss" scoped>
.attendance-manage { .search-card { margin-bottom: 16px; } .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
