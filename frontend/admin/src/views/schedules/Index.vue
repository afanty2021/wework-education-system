<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Schedule, ScheduleStatus, ScheduleListParams } from '@/api/schedules'
import { getSchedules, createSchedule, updateSchedule, deleteSchedule, cancelSchedule } from '@/api/schedules'

const loading = ref(false)
const scheduleList = ref<Schedule[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增排课')
const isEdit = ref(false)
const formRef = ref()

const queryParams = reactive<ScheduleListParams>({
  page: 1,
  pageSize: 10,
  course_id: undefined,
  teacher_id: undefined,
  classroom_id: undefined,
  status: null,
})

const formData = reactive({
  id: 0,
  course_id: 0,
  teacher_id: 0,
  classroom_id: undefined as number | undefined,
  department_id: undefined as number | undefined,
  scheduled_date: '',
  start_time: '',
  end_time: '',
  capacity: 30,
  remark: '',
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '已安排', value: 1 },
  { label: '已上课', value: 2 },
  { label: '已取消', value: 3 },
]

const rules = {
  course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }],
  scheduled_date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
}

async function fetchScheduleList() {
  loading.value = true
  try {
    const data = await getSchedules({
      skip: (queryParams.page - 1) * queryParams.pageSize,
      limit: queryParams.pageSize,
      course_id: queryParams.course_id,
      teacher_id: queryParams.teacher_id,
      classroom_id: queryParams.classroom_id,
      status: queryParams.status || undefined,
    })
    scheduleList.value = data
    total.value = data.length
  } catch { ElMessage.error('获取排课列表失败') }
  finally { loading.value = false }
}

function handleSearch() { queryParams.page = 1; fetchScheduleList() }
function handleReset() { Object.assign(queryParams, { page: 1, pageSize: 10, course_id: undefined, teacher_id: undefined, classroom_id: undefined, status: null }); fetchScheduleList() }
function handlePageChange(page: number) { queryParams.page = page; fetchScheduleList() }
function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchScheduleList() }

function handleAdd() {
  dialogTitle.value = '新增排课'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: Schedule) {
  dialogTitle.value = '编辑排课'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function handleDelete(row: Schedule) {
  try {
    await ElMessageBox.confirm(`确定要删除该排课吗？`, '提示', { type: 'warning' })
    await deleteSchedule(row.id)
    ElMessage.success('删除成功')
    fetchScheduleList()
  } catch {}
}

async function handleCancel(row: Schedule) {
  try {
    await ElMessageBox.confirm('确定要取消该排课吗？', '提示', { type: 'warning' })
    await cancelSchedule(row.id)
    ElMessage.success('取消成功')
    fetchScheduleList()
  } catch {}
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateSchedule(formData.id, formData)
    else await createSchedule(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchScheduleList()
  } catch { ElMessage.error('操作失败') }
}

function resetForm() {
  Object.assign(formData, { id: 0, course_id: 0, teacher_id: 0, classroom_id: undefined, department_id: undefined, scheduled_date: '', start_time: '', end_time: '', capacity: 30, remark: '' })
  formRef.value?.resetFields()
}

function formatStatus(status: number): string { const map = { 1: '已安排', 2: '已上课', 3: '已取消' }; return map[status] || '未知' }

onMounted(() => fetchScheduleList())
</script>

<template>
  <div class="schedule-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="课程">
          <el-select v-model="queryParams.course_id" placeholder="请选择课程" clearable style="width: 160px">
            <el-option label="Python入门" :value="1" />
            <el-option label="Java进阶" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="queryParams.teacher_id" placeholder="请选择教师" clearable style="width: 140px">
            <el-option label="张老师" :value="1" />
            <el-option label="李老师" :value="2" />
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
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>新增排课</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="scheduleList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="course_name" label="课程" width="120" />
        <el-table-column prop="teacher_name" label="教师" width="100" />
        <el-table-column prop="classroom_name" label="教室" width="100" />
        <el-table-column prop="scheduled_date" label="日期" width="120" />
        <el-table-column label="时间" width="120">
          <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
        </el-table-column>
        <el-table-column prop="enrolled_count" label="报名人数" width="100">
          <template #default="{ row }">{{ row.enrolled_count }}/{{ row.capacity }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? '' : row.status === 2 ? 'success' : 'info'">{{ formatStatus(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="row.status === 1" type="warning" link size="small" @click="handleCancel(row)">取消</el-button>
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
            <el-form-item label="课程" prop="course_id">
              <el-select v-model="formData.course_id" placeholder="请选择课程" style="width: 100%">
                <el-option label="Python入门" :value="1" />
                <el-option label="Java进阶" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="教师" prop="teacher_id">
              <el-select v-model="formData.teacher_id" placeholder="请选择教师" style="width: 100%">
                <el-option label="张老师" :value="1" />
                <el-option label="李老师" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="教室">
              <el-select v-model="formData.classroom_id" placeholder="请选择教室" style="width: 100%" clearable>
                <el-option label="教室101" :value="1" />
                <el-option label="教室102" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="容量">
              <el-input-number v-model="formData.capacity" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="日期" prop="scheduled_date">
              <el-date-picker v-model="formData.scheduled_date" type="date" placeholder="请选择日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="时间" prop="time">
              <el-time-picker
                v-model="formData.start_time"
                placeholder="开始时间"
                format="HH:mm"
                style="width: 45%"
              />
              <span style="margin: 0 8px">至</span>
              <el-time-picker
                v-model="formData.end_time"
                placeholder="结束时间"
                format="HH:mm"
                style="width: 45%"
              />
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
import { getSchedules, createSchedule, updateSchedule, deleteSchedule, cancelSchedule } from '@/api/schedules'
import type { Schedule } from '@/api/schedules'

export default defineComponent({
  name: 'ScheduleIndex',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const scheduleList = ref<Schedule[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增排课')
    const isEdit = ref(false)
    const formRef = ref()

    const queryParams = reactive<ScheduleListParams>({ page: 1, pageSize: 10, course_id: undefined, teacher_id: undefined, classroom_id: undefined, status: null })

    const formData = reactive({ id: 0, course_id: 0, teacher_id: 0, classroom_id: undefined as number | undefined, department_id: undefined as number | undefined, scheduled_date: '', start_time: '', end_time: '', capacity: 30, remark: '' })

    const statusOptions = [{ label: '全部', value: null }, { label: '已安排', value: 1 }, { label: '已上课', value: 2 }, { label: '已取消', value: 3 }]

    const rules = { course_id: [{ required: true, message: '请选择课程', trigger: 'change' }], teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }], scheduled_date: [{ required: true, message: '请选择日期', trigger: 'change' }], start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }], end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }] }

    async function fetchScheduleList() {
      loading.value = true
      try {
        const data = await getSchedules(queryParams)
        scheduleList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取排课列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchScheduleList() }
    function handleReset() { Object.assign(queryParams, { page: 1, pageSize: 10, course_id: undefined, teacher_id: undefined, classroom_id: undefined, status: null }); fetchScheduleList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchScheduleList() }
    function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchScheduleList() }
    function handleAdd() { dialogTitle.value = '新增排课'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    function handleEdit(row: Schedule) { dialogTitle.value = '编辑排课'; isEdit.value = true; Object.assign(formData, row); dialogVisible.value = true }
    async function handleDelete(row: Schedule) {
      try {
        await ElMessageBox.confirm('确定要删除该排课吗？', '提示', { type: 'warning' })
        await deleteSchedule(row.id)
        ElMessage.success('删除成功')
        fetchScheduleList()
      } catch {}
    }
    async function handleCancel(row: Schedule) {
      try {
        await ElMessageBox.confirm('确定要取消该排课吗？', '提示', { type: 'warning' })
        await cancelSchedule(row.id)
        ElMessage.success('取消成功')
        fetchScheduleList()
      } catch {}
    }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateSchedule(formData.id, formData)
        else await createSchedule(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchScheduleList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, course_id: 0, teacher_id: 0, classroom_id: undefined, department_id: undefined, scheduled_date: '', start_time: '', end_time: '', capacity: 30, remark: '' }) }
    function formatStatus(status: number): string { const map = { 1: '已安排', 2: '已上课', 3: '已取消' }; return map[status] || '未知' }

    onMounted(() => fetchScheduleList())

    return { loading, scheduleList, total, queryParams, statusOptions, formData, rules, dialogVisible, dialogTitle, isEdit, formRef, handleSearch, handleReset, handlePageChange, handleSizeChange, handleAdd, handleEdit, handleDelete, handleCancel, handleSubmit, formatStatus }
  },
})
</script>

<style lang="scss" scoped>
.schedule-manage { .search-card { margin-bottom: 16px; } .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
