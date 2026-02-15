<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from '@/api/courses'

const loading = ref(false)
const departmentList = ref<any[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增校区')
const isEdit = ref(false)
const formRef = ref()

const queryParams = reactive({ page: 1, pageSize: 10 })

const formData = reactive({
  id: 0,
  name: '',
  parent_id: undefined as number | undefined,
  manager_id: undefined as number | undefined,
  address: '',
  contact: '',
})

const rules = {
  name: [{ required: true, message: '请输入校区名称', trigger: 'blur' }],
}

async function fetchList() {
  loading.value = true
  try {
    const data = await getDepartments({ skip: (queryParams.page - 1) * queryParams.pageSize, limit: queryParams.pageSize })
    departmentList.value = data
    total.value = data.length
  } catch { ElMessage.error('获取校区列表失败') }
  finally { loading.value = false }
}

function handleSearch() { queryParams.page = 1; fetchList() }
function handlePageChange(page: number) { queryParams.page = page; fetchList() }

function handleAdd() {
  dialogTitle.value = '新增校区'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑校区'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确定要删除校区"${row.name}"吗？`, '提示', { type: 'warning' })
    await deleteDepartment(row.id)
    ElMessage.success('删除成功')
    fetchList()
  } catch {}
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateDepartment(formData.id, formData)
    else await createDepartment(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchList()
  } catch { ElMessage.error('操作失败') }
}

function resetForm() {
  Object.assign(formData, { id: 0, name: '', parent_id: undefined, manager_id: undefined, address: '', contact: '' })
  formRef.value?.resetFields()
}

onMounted(() => fetchList())
</script>

<template>
  <div class="department-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item>
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>新增校区</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table v-loading="loading" :data="departmentList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="校区名称" min-width="150" />
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="contact" label="联系方式" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">{{ row.status === 1 ? '正常' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
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
        <el-form-item label="校区名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入校区名称" />
        </el-form-item>
        <el-form-item label="上级校区">
          <el-select v-model="formData.parent_id" placeholder="请选择上级校区" style="width: 100%" clearable>
            <el-option label="无" :value="undefined" />
          </el-select>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="formData.address" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="formData.contact" placeholder="请输入联系方式" />
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
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from '@/api/courses'

export default defineComponent({
  name: 'DepartmentsPage',
  components: { Plus, Pagination },
  setup() {
    const loading = ref(false)
    const departmentList = ref<any[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增校区')
    const isEdit = ref(false)
    const formRef = ref()

    const queryParams = reactive({ page: 1, pageSize: 10 })

    const formData = reactive({
      id: 0,
      name: '',
      parent_id: undefined as number | undefined,
      manager_id: undefined as number | undefined,
      address: '',
      contact: '',
    })

    const rules = { name: [{ required: true, message: '请输入校区名称', trigger: 'blur' }] }

    async function fetchList() {
      loading.value = true
      try {
        const data = await getDepartments({ skip: (queryParams.page - 1) * queryParams.pageSize, limit: queryParams.pageSize })
        departmentList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取校区列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchList() }
    function handleAdd() { dialogTitle.value = '新增校区'; isEdit.value = false; resetForm(); dialogVisible.value = true }
    function handleEdit(row: any) { dialogTitle.value = '编辑校区'; isEdit.value = true; Object.assign(formData, row); dialogVisible.value = true }
    async function handleDelete(row: any) {
      try {
        await ElMessageBox.confirm(`确定要删除校区"${row.name}"吗？`, '提示', { type: 'warning' })
        await deleteDepartment(row.id)
        ElMessage.success('删除成功')
        fetchList()
      } catch {}
    }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateDepartment(formData.id, formData)
        else await createDepartment(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchList()
      } catch { ElMessage.error('操作失败') }
    }
    function resetForm() { Object.assign(formData, { id: 0, name: '', parent_id: undefined, manager_id: undefined, address: '', contact: '' }) }

    onMounted(() => fetchList())

    return { loading, departmentList, total, queryParams, formData, rules, dialogVisible, dialogTitle, isEdit, formRef, handleSearch, handlePageChange, handleAdd, handleEdit, handleDelete, handleSubmit }
  },
})
</script>

<style lang="scss" scoped>
.department-manage { .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
