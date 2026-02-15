<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import { getClassrooms, createClassroom, updateClassroom, deleteClassroom } from '@/api/courses'

const loading = ref(false)
const classroomList = ref<any[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增教室')
const isEdit = ref(false)
const formRef = ref()

const queryParams = reactive({ page: 1, pageSize: 10, department_id: undefined, status: null })

const formData = reactive({
  id: 0,
  name: '',
  capacity: 30,
  department_id: undefined as number | undefined,
  equipment: [] as string[],
})

const statusOptions = [
  { label: '全部', value: null },
  { label: '可用', value: 1 },
  { label: '维护中', value: 2 },
]

const rules = {
  name: [{ required: true, message: '请输入教室名称', trigger: 'blur' }],
  capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }],
}

async function fetchList() {
  loading.value = true
  try {
    const data = await getClassrooms({ skip: (queryParams.page - 1) * queryParams.pageSize, limit: queryParams.pageSize })
    classroomList.value = data
    total.value = data.length
  } catch { ElMessage.error('获取教室列表失败') }
  finally { loading.value = false }
}

function handleSearch() { queryParams.page = 1; fetchList() }
function handleReset() { queryParams.department_id = undefined; queryParams.status = null; queryParams.page = 1; fetchList() }
function handlePageChange(page: number) { queryParams.page = page; fetchList() }

function handleAdd() {
  dialogTitle.value = '新增教室'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑教室'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确定要删除教室"${row.name}"吗？`, '提示', { type: 'warning' })
    await deleteClassroom(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch {}
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateClassroom(formData.id, formData)
    else await createClassroom(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchList()
  } catch { ElMessage.error('操作失败') }
}

function resetForm() {
  Object.assign(formData, { id: 0, name: '', capacity: 30, department_id: undefined, equipment: [] })
  formRef.value?.resetFields()
}

onMounted(() => fetchList())
</script>

<template>
  <div class="classroom-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option v-for="item in statusOptions.slice(1)" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>新增教室</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table v-loading="loading" :data="classroomList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="教室名称" min-width="120" />
        <el-table-column prop="capacity" label="容量" width="100" />
        <el-table-column prop="department_name" label="所属校区" width="150" />
        <el-table-column prop="equipment" label="设备" min-width="150">
          <template #default="{ row }">
            <el-tag v-for="eq in row.equipment" :key="eq" size="small" class="mr-2">{{ eq }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'warning'">{{ row.status === 1 ? '可用' : '维护中' }}</el-tag>
          </template>
        </el-table-column>
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
        <el-form-item label="教室名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入教室名称" />
        </el-form-item>
        <el-form-item label="容量" prop="capacity">
          <el-input-number v-model="formData.capacity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="所属校区">
          <el-select v-model="formData.department_id" placeholder="请选择校区" style="width: 100%" clearable>
            <el-option label="总校区" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="设备">
          <el-checkbox-group v-model="formData.equipment">
            <el-checkbox label="投影仪" />
            <el-checkbox label="白板" />
            <el-checkbox label="空调" />
            <el-checkbox label="电脑" />
            <el-checkbox label="音响" />
          </el-checkbox-group>
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
import { getClassrooms, createClassroom, updateClassroom, deleteClassroom } from '@/api/courses'

export default defineComponent({
  name: 'ClassroomsPage',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const classroomList = ref<any[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增教室')
    const isEdit = ref(false)
    const formRef = ref()

    const queryParams = reactive({ page: 1, pageSize: 10, department_id: undefined, status: null as number | null })

    const formData = reactive({
      id: 0,
      name: '',
      capacity: 30,
      department_id: undefined as number | undefined,
      equipment: [] as string[],
    })

    const statusOptions = [
      { label: '全部', value: null },
      { label: '可用', value: 1 },
      { label: '维护中', value: 2 },
    ]

    const rules = {
      name: [{ required: true, message: '请输入教室名称', trigger: 'blur' }],
      capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }],
    }

    async function fetchList() {
      loading.value = true
      try {
        const data = await getClassrooms({ skip: (queryParams.page - 1) * queryParams.pageSize, limit: queryParams.pageSize })
        classroomList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取教室列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchList() }
    function handleReset() { queryParams.department_id = undefined; queryParams.status = null; queryParams.page = 1; fetchList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchList() }
    function handleAdd() { dialogTitle.value = '新增教室'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    function handleEdit(row: any) { dialogTitle.value = '编辑教室'; isEdit.value = true; Object.assign(formData, row); dialogVisible.value = true }
    async function handleDelete(row: any) {
      try {
        await ElMessageBox.confirm(`确定要删除教室"${row.name}"吗？`, '提示', { type: 'warning' })
        await deleteClassroom(row.id)
        ElMessage.success('删除成功')
        fetchList()
      } catch {}
    }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateClassroom(formData.id, formData)
        else await createClassroom(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, name: '', capacity: 30, department_id: undefined, equipment: [] }) }

    onMounted(() => fetchList())

    return { loading, classroomList, total, queryParams, statusOptions, formData, rules, dialogVisible, dialogTitle, isEdit, formRef, handleSearch, handleReset, handlePageChange, handleAdd, handleEdit, handleDelete, handleSubmit }
  },
})
</script>

<style lang="scss" scoped>
.classroom-manage { .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } .mr-2 { margin-right: 4px; } }
</style>
