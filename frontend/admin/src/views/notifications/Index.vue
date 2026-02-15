<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Notification, NotificationType, NotificationStatus, NotificationListParams } from '@/api/notifications'
import { getNotifications, createNotification, markAsRead, markAllAsRead } from '@/api/notifications'

const loading = ref(false)
const notificationList = ref<Notification[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const formRef = ref()

const queryParams = reactive<NotificationListParams>({
  page: 1,
  pageSize: 10,
  type: null,
  status: null,
})

const formData = reactive({
  type: 1,
  title: '',
  content: '',
  related_id: undefined,
  related_type: '',
})

const typeOptions = [
  { label: '合同到期', value: 1 },
  { label: '课程提醒', value: 2 },
  { label: '缴费提醒', value: 3 },
  { label: '考勤提醒', value: 4 },
  { label: '系统通知', value: 5 },
]

const statusOptions = [
  { label: '全部', value: null },
  { label: '未读', value: 1 },
  { label: '已读', value: 2 },
]

const typeMap = { 1: '合同到期', 2: '课程提醒', 3: '缴费提醒', 4: '考勤提醒', 5: '系统通知' }
const typeColorMap = { 1: 'warning', 2: 'success', 3: 'primary', 4: 'info', 5: '' }
const statusMap = { 1: '未读', 2: '已读' }
const statusTypeMap = { 1: 'danger', 2: 'success' }

async function fetchNotificationList() {
  loading.value = true
  try {
    const data = await getNotifications({
      skip: (queryParams.page - 1) * queryParams.pageSize,
      limit: queryParams.pageSize,
      type: queryParams.type || undefined,
      status: queryParams.status || undefined,
    })
    notificationList.value = data
    total.value = data.length
  } catch { ElMessage.error('获取通知列表失败') }
  finally { loading.value = false }
}

function handleSearch() { queryParams.page = 1; fetchNotificationList() }
function handleReset() { Object.assign(queryParams, { page: 1, pageSize: 10, type: null, status: null }); fetchNotificationList() }
function handlePageChange(page: number) { queryParams.page = page; fetchNotificationList() }
function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchNotificationList() }

function handleAdd() {
  Object.assign(formData, { type: 1, title: '', content: '', related_id: undefined, related_type: '' })
  dialogVisible.value = true
}

async function handleRead(row: Notification) {
  try {
    await markAsRead(row.id)
    ElMessage.success('标记成功')
    fetchNotificationList()
  } catch { ElMessage.error('标记失败') }
}

async function handleReadAll() {
  try {
    await markAllAsRead()
    ElMessage.success('全部标记为已读')
    fetchNotificationList()
  } catch { ElMessage.error('操作失败') }
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    await createNotification(formData)
    ElMessage.success('发送成功')
    dialogVisible.value = false
    fetchNotificationList()
  } catch { ElMessage.error('发送失败') }
}

function formatType(type: number): string { return typeMap[type] || '未知' }
function formatStatus(status: number): string { return statusMap[status] || '未知' }

onMounted(() => fetchNotificationList())
</script>

<template>
  <div class="notification-manage">
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="通知类型">
          <el-select v-model="queryParams.type" placeholder="请选择类型" clearable style="width: 140px">
            <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="阅读状态">
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
          <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>发送通知</el-button>
          <el-button @click="handleReadAll"><el-icon><Check /></el-icon>全部已读</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="notificationList" stripe>
        <el-table-column type="selection" width="50" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="typeColorMap[row.type]">{{ formatType(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTypeMap[row.status]">{{ formatStatus(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="120" fixed="right" align="center">
          <template #default="{ row }">
            <el-button v-if="row.status === 1" type="primary" link size="small" @click="handleRead(row)">标记已读</el-button>
            <el-button type="info" link size="small" @click="handleView(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <Pagination :total="total" :page="queryParams.page" :page-size="queryParams.pageSize" @page-change="handlePageChange" @size-change="handleSizeChange" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" title="发送通知" width="600px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="通知类型" prop="type">
          <el-select v-model="formData.type" placeholder="请选择类型" style="width: 100%">
            <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="通知标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入通知标题" />
        </el-form-item>
        <el-form-item label="通知内容" prop="content">
          <el-input v-model="formData.content" type="textarea" :rows="4" placeholder="请输入通知内容" />
        </el-form-item>
        <el-form-item label="关联业务">
          <el-row :gutter="12">
            <el-col :span="12">
              <el-input v-model="formData.related_type" placeholder="业务类型" />
            </el-col>
            <el-col :span="12">
              <el-input-number v-model="formData.related_id" placeholder="业务ID" style="width: 100%" />
            </el-col>
          </el-row>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">发送</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Check } from '@element-plus/icons-vue'
import Pagination from '@/components/Pagination.vue'
import { getNotifications, createNotification, markAsRead, markAllAsRead } from '@/api/notifications'

export default defineComponent({
  name: 'NotificationIndex',
  components: { Plus, Check, Pagination },
  setup() {
    const loading = ref(false)
    const notificationList = ref<any[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const formRef = ref()

    const queryParams = reactive<any>({ page: 1, pageSize: 10, type: null, status: null })

    const formData = reactive({ type: 1, title: '', content: '', related_id: undefined, related_type: '' })

    const typeOptions = [{ label: '合同到期', value: 1 }, { label: '课程提醒', value: 2 }, { label: '缴费提醒', value: 3 }, { label: '考勤提醒', value: 4 }, { label: '系统通知', value: 5 }]
    const statusOptions = [{ label: '全部', value: null }, { label: '未读', value: 1 }, { label: '已读', value: 2 }]

    const typeMap = { 1: '合同到期', 2: '课程提醒', 3: '缴费提醒', 4: '考勤提醒', 5: '系统通知' }
    const typeColorMap = { 1: 'warning', 2: 'success', 3: 'primary', 4: 'info', 5: '' }
    const statusMap = { 1: '未读', 2: '已读' }
    const statusTypeMap = { 1: 'danger', 2: 'success' }

    const rules = { type: [{ required: true, message: '请选择类型', trigger: 'change' }], title: [{ required: true, message: '请输入标题', trigger: 'blur' }], content: [{ required: true, message: '请输入内容', trigger: 'blur' }] }

    async function fetchNotificationList() {
      loading.value = true
      try {
        const data = await getNotifications(queryParams)
        notificationList.value = data
        total.value = data.length
      } catch { ElMessage.error('获取通知列表失败') }
      finally { loading.value = false }
    }

    function handleSearch() { queryParams.page = 1; fetchNotificationList() }
    function handleReset() { Object.assign(queryParams, { page: 1, pageSize: 10, type: null, status: null }); fetchNotificationList() }
    function handlePageChange(page: number) { queryParams.page = page; fetchNotificationList() }
    function handleSizeChange(size: number) { queryParams.pageSize = size; queryParams.page = 1; fetchNotificationList() }
    function handleAdd() { Object.assign(formData, { type: 1, title: '', content: '', related_id: undefined, related_type: '' }); dialogVisible.value = true }
    async function handleRead(row: any) {
      try {
        await markAsRead(row.id)
        ElMessage.success('标记成功')
        fetchNotificationList()
      } catch { ElMessage.error('标记失败') }
    }
    async function handleReadAll() {
      try {
        await markAllAsRead()
        ElMessage.success('全部标记为已读')
        fetchNotificationList()
      } catch { ElMessage.error('操作失败') }
    }
    function handleView(row: any) { }
    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        await createNotification(formData)
        ElMessage.success('发送成功')
        dialogVisible.value = false
        fetchNotificationList()
      } catch { ElMessage.error('发送失败') }
    }
    function formatType(type: number): string { return typeMap[type] || '未知' }
    function formatStatus(status: number): string { return statusMap[status] || '未知' }

    onMounted(() => fetchNotificationList())

    return { loading, notificationList, total, queryParams, typeOptions, statusOptions, typeMap, typeColorMap, statusMap, statusTypeMap, formData, rules, dialogVisible, formRef, handleSearch, handleReset, handlePageChange, handleSizeChange, handleAdd, handleRead, handleReadAll, handleView, handleSubmit, formatType, formatStatus }
  },
})
</script>

<style lang="scss" scoped>
.notification-manage { .search-card { margin-bottom: 16px; } .pagination-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; } }
</style>
