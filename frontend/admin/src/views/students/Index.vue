<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Student, StudentStatus, StudentListParams } from '@/api/students'
import {
  getStudents,
  createStudent,
  updateStudent,
  deleteStudent,
  updateStudentStatus,
  getAllTags,
} from '@/api/students'

const loading = ref(false)
const studentList = ref<Student[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增学员')
const isEdit = ref(false)
const selectedIds = ref<number[]>([])
const allTags = ref<string[]>([])
const formRef = ref()

const queryParams = reactive<StudentListParams>({
  page: 1,
  pageSize: 10,
  status: null,
  source: '',
  search: '',
})

const formData = reactive({
  id: 0,
  name: '',
  phone: '',
  email: '',
  wechat: '',
  guardian_name: '',
  guardian_phone: '',
  source: '',
  tags: [] as string[],
  status: 1,
  remark: '',
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '潜在', value: 1 },
  { label: '在读', value: 2 },
  { label: '已流失', value: 3 },
]

const rules = {
  name: [{ required: true, message: '请输入学员姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
}

async function fetchStudentList() {
  loading.value = true
  try {
    const data = await getStudents({
      skip: (queryParams.page - 1) * queryParams.pageSize,
      limit: queryParams.pageSize,
      status: queryParams.status || undefined,
      source: queryParams.source,
      search: queryParams.search,
    })
    studentList.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('获取学员列表失败')
  } finally {
    loading.value = false
  }
}

async function fetchAllTags() {
  try {
    allTags.value = await getAllTags()
  } catch (error) {
    console.error('获取标签失败')
  }
}

function handleSearch() {
  queryParams.page = 1
  fetchStudentList()
}

function handleReset() {
  queryParams.search = ''
  queryParams.status = null
  queryParams.source = ''
  queryParams.page = 1
  fetchStudentList()
}

function handlePageChange(page: number) {
  queryParams.page = page
  fetchStudentList()
}

function handleSizeChange(size: number) {
  queryParams.pageSize = size
  queryParams.page = 1
  fetchStudentList()
}

function handleAdd() {
  dialogTitle.value = '新增学员'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: Student) {
  dialogTitle.value = '编辑学员'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function handleDelete(row: Student) {
  try {
    await ElMessageBox.confirm(`确定要删除学员"${row.name}"吗？`, '提示', { type: 'warning' })
    await deleteStudent(row.id)
    ElMessage.success('删除成功')
    fetchStudentList()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

async function handleStatusChange(row: Student, status: number) {
  try {
    await updateStudentStatus(row.id, status)
    ElMessage.success('状态更新成功')
    fetchStudentList()
  } catch (error) {
    ElMessage.error('状态更新失败')
  }
}

function handleSelectionChange(selection: Student[]) {
  selectedIds.value = selection.map((item) => item.id)
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) {
      await updateStudent(formData.id, formData)
    } else {
      await createStudent(formData)
    }
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchStudentList()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function resetForm() {
  formData.id = 0
  formData.name = ''
  formData.phone = ''
  formData.email = ''
  formData.wechat = ''
  formData.guardian_name = ''
  formData.guardian_phone = ''
  formData.source = ''
  formData.tags = []
  formData.status = 1
  formData.remark = ''
  formRef.value?.resetFields()
}

function formatStatus(status: number): string {
  const map = { 1: '潜在', 2: '在读', 3: '已流失' }
  return map[status] || '未知'
}

onMounted(() => {
  fetchStudentList()
  fetchAllTags()
})
</script>

<template>
  <div class="student-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="学员姓名">
          <el-input v-model="queryParams.search" placeholder="请输入学员姓名" clearable style="width: 180px" @keyup.enter="handleSearch" />
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
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增学员
          </el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="studentList" stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" min-width="100" />
        <el-table-column prop="phone" label="联系电话" min-width="120" />
        <el-table-column prop="source" label="来源" width="100" />
        <el-table-column prop="tags" label="标签" min-width="150">
          <template #default="{ row }">
            <el-tag v-for="tag in row.tags" :key="tag" size="small" class="tag-item">{{ tag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 2 ? 'success' : row.status === 3 ? 'info' : 'warning'">
              {{ formatStatus(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="row.status !== 2" type="success" link size="small" @click="handleStatusChange(row, 2)">转为在读</el-button>
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
            <el-form-item label="学员姓名" prop="name">
              <el-input v-model="formData.name" placeholder="请输入学员姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="微信号">
              <el-input v-model="formData.wechat" placeholder="请输入微信号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱">
              <el-input v-model="formData.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="家长姓名">
              <el-input v-model="formData.guardian_name" placeholder="请输入家长姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="家长电话">
              <el-input v-model="formData.guardian_phone" placeholder="请输入家长电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学员来源">
              <el-input v-model="formData.source" placeholder="请输入学员来源" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" style="width: 100%">
                <el-option v-for="item in statusOptions.slice(1)" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="标签">
              <el-select v-model="formData.tags" multiple filterable allow-create default-first-option placeholder="请选择或创建标签" style="width: 100%">
                <el-option v-for="tag in allTags" :key="tag" :label="tag" :value="tag" />
              </el-select>
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
import { getStudents, createStudent, updateStudent, deleteStudent, updateStudentStatus, getAllTags } from '@/api/students'
import type { Student } from '@/api/students'

export default defineComponent({
  name: 'StudentIndex',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const studentList = ref<Student[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增学员')
    const isEdit = ref(false)
    const selectedIds = ref<number[]>([])
    const allTags = ref<string[]>([])
    const formRef = ref()

    const queryParams = reactive({ page: 1, pageSize: 10, status: null as number | null, source: '', search: '' })

    const formData = reactive({
      id: 0, name: '', phone: '', email: '', wechat: '', guardian_name: '', guardian_phone: '', source: '', tags: [] as string[], status: 1, remark: '',
    })

    const statusOptions = [
      { label: '全部', value: null },
      { label: '潜在', value: 1 },
      { label: '在读', value: 2 },
      { label: '已流失', value: 3 },
    ]

    const rules = {
      name: [{ required: true, message: '请输入学员姓名', trigger: 'blur' }],
      phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
    }

    async function fetchStudentList() {
      loading.value = true
      try {
        const data = await getStudents(queryParams)
        studentList.value = data
        total.value = data.length
      } catch (error) {
        ElMessage.error('获取学员列表失败')
      } finally {
        loading.value = false
      }
    }

    async function fetchAllTags() {
      try {
        allTags.value = await getAllTags()
      } catch {}
    }

    function handleSearch() { queryParams.page = 1; fetchStudentList() }
    function handleReset() { queryParams.search = ''; queryParams.status = null; queryParams.source = ''; queryParams.page = 1; fetchStudentList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchStudentList() }
    function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchStudentList() }
    function handleAdd() { dialogTitle.value = '新增学员'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    function handleEdit(row: Student) { dialogTitle.value = '编辑学员'; isEdit.value = true; Object.assign(formData, row); dialogVisible.value = true }
    async function handleDelete(row: Student) {
      try {
        await ElMessageBox.confirm(`确定要删除学员"${row.name}"吗？`, '提示', { type: 'warning' })
        await deleteStudent(row.id)
        ElMessage.success('删除成功')
        fetchStudentList()
      } catch {}
    }
    async function handleStatusChange(row: Student, status: number) {
      try {
        await updateStudentStatus(row.id, status)
        ElMessage.success('状态更新成功')
        fetchStudentList()
      } catch { ElMessage.error('状态更新失败') }
    }
    function handleSelectionChange(selection: Student[]) { selectedIds.value = selection.map((item) => item.id) }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateStudent(formData.id, formData)
        else await createStudent(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchStudentList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, name: '', phone: '', email: '', wechat: '', guardian_name: '', guardian_phone: '', source: '', tags: [], status: 1, remark: '' }); formRef.value?.resetFields() }

    onMounted(() => { fetchStudentList(); fetchAllTags() })

    return { loading, studentList, total, queryParams, statusOptions, formData, rules, dialogVisible, dialogTitle, isEdit, selectedIds, allTags, formRef, handleSearch, handleReset, handlePageChange, handleSizeChange, handleAdd, handleEdit, handleDelete, handleStatusChange, handleSelectionChange, handleSubmit }
  },
})
</script>

<style lang="scss" scoped>
.student-manage {
  .search-card { margin-bottom: 16px; }
  .tag-item { margin-right: 4px; }
  .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; }
}
</style>
