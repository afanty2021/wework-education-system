<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'

const loading = ref(false)
const teacherList = ref<any[]>([
  { id: 1, name: '张老师', phone: '13800138001', email: 'zhang@edu.com', subject: 'Python', status: 1 },
  { id: 2, name: '李老师', phone: '13800138002', email: 'li@edu.com', subject: 'Java', status: 1 },
  { id: 3, name: '王老师', phone: '13800138003', email: 'wang@edu.com', subject: 'Web前端', status: 2 },
])
const total = ref(3)
const dialogVisible = ref(false)
const dialogTitle = ref('新增教师')
const isEdit = ref(false)
const formRef = ref()

const queryParams = reactive({ page: 1, pageSize: 10, search: '', status: null })

const formData = reactive({
  id: 0,
  name: '',
  phone: '',
  email: '',
  subject: '',
  status: 1,
  remark: '',
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '在职', value: 1 },
  { label: '离职', value: 2 },
]

const rules = {
  name: [{ required: true, message: '请输入教师姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
}

function fetchList() {
  loading.value = true
  setTimeout(() => {
    teacherList.value = [
      { id: 1, name: '张老师', phone: '13800138001', email: 'zhang@edu.com', subject: 'Python', status: 1 },
      { id: 2, name: '李老师', phone: '13800138002', email: 'li@edu.com', subject: 'Java', status: 1 },
      { id: 3, name: '王老师', phone: '13800138003', email: 'wang@edu.com', subject: 'Web前端', status: 2 },
    ]
    total.value = 3
    loading.value = false
  }, 500)
}

function handleSearch() { queryParams.page = 1; fetchList() }
function handleReset() { queryParams.search = ''; queryParams.status = null; queryParams.page = 1; fetchList() }
function handlePageChange(page: number) { queryParams.page = page; fetchList() }

function handleAdd() {
  dialogTitle.value = '新增教师'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑教师'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm(`确定要删除教师"${row.name}"吗？`, '提示', { type: 'warning' }).then(() => {
    ElMessage.success('删除成功')
    fetchList()
  }).catch(() => {})
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchList()
  } catch { ElMessage.error('操作失败') }
}

function resetForm() {
  Object.assign(formData, { id: 0, name: '', phone: '', email: '', subject: '', status: 1, remark: '' })
  formRef.value?.resetFields()
}

onMounted(() => fetchList())
</script>

<template>
  <div class="teacher-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="教师姓名">
          <el-input v-model="queryParams.search" placeholder="请输入教师姓名" clearable style="width: 180px" @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option v-for="item in statusOptions.slice(1)" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>新增教师</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table v-loading="loading" :data="teacherList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="教师姓名" min-width="120" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="subject" label="科目" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">{{ row.status === 1 ? '在职' : '离职' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-wrapper">
        <Pagination :total="total" :page="queryParams.page" :page-size="queryParams.pageSize" @page-change="handlePageChange" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="教师姓名" prop="name">
              <el-input v-model="formData.name" placeholder="请输入教师姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱">
              <el-input v-model="formData.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="科目">
              <el-input v-model="formData.subject" placeholder="请输入教授科目" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio :label="1">在职</el-radio>
                <el-radio :label="2">离职</el-radio>
              </el-radio-group>
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

export default defineComponent({
  name: 'TeachersPage',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const teacherList = ref<any[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增教师')
    const isEdit = ref(false)
    const formRef = ref()

    const queryParams = reactive({ page: 1, pageSize: 10, search: '', status: null as number | null })

    const formData = reactive({
      id: 0,
      name: '',
      phone: '',
      email: '',
      subject: '',
      status: 1,
      remark: '',
    })

    const statusOptions = [
      { label: '全部', value: null },
      { label: '在职', value: 1 },
      { label: '离职', value: 2 },
    ]

    const rules = {
      name: [{ required: true, message: '请输入教师姓名', trigger: 'blur' }],
      phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
    }

    function fetchList() {
      loading.value = true
      setTimeout(() => {
        teacherList.value = [
          { id: 1, name: '张老师', phone: '13800138001', email: 'zhang@edu.com', subject: 'Python', status: 1, remark: '' },
          { id: 2, name: '李老师', phone: '13800138002', email: 'li@edu.com', subject: 'Java', status: 1, remark: '' },
          { id: 3, name: '王老师', phone: '13800138003', email: 'wang@edu.com', subject: 'Web前端', status: 2, remark: '' },
        ]
        total.value = 3
        loading.value = false
      }, 500)
    }

    function handleSearch() { queryParams.page = 1; fetchList() }
    function handleReset() { queryParams.search = ''; queryParams.status = null; queryParams.page = 1; fetchList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchList() }
    function handleAdd() { dialogTitle.value = '新增教师'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    function handleEdit(row: any) { dialogTitle.value = '编辑教师'; isEdit.value = true; Object.assign(formData, row); dialogVisible.value = true }
    function handleDelete(row: any) {
      ElMessageBox.confirm(`确定要删除教师"${row.name}"吗？`, '提示', { type: 'warning' }).then(() => { ElMessage.success('删除成功'); fetchList() }).catch(() => {})
    }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, name: '', phone: '', email: '', subject: '', status: 1, remark: '' }) }

    onMounted(() => fetchList())

    return { loading, teacherList, total, queryParams, statusOptions, formData, rules, dialogVisible, dialogTitle, isEdit, formRef, handleSearch, handleReset, handlePageChange, handleAdd, handleEdit, handleDelete, handleSubmit }
  },
})
</script>

<style lang="scss" scoped>
.teacher-manage { .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
