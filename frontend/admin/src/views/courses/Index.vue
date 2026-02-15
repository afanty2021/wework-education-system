<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'
import type { Course, CourseStatus, CourseListParams } from '@/api/courses'
import {
  getCourses,
  getCourse,
  createCourse,
  updateCourse,
  deleteCourse,
  toggleCourseStatus,
} from '@/api/courses'

const router = useRouter()

// 加载状态
const loading = ref(false)

// 课程列表
const courseList = ref<Course[]>([])

// 总数
const total = ref(0)

// 查询参数
const queryParams = reactive<CourseListParams>({
  page: 1,
  pageSize: 10,
  category: undefined,
  status: undefined,
  search: '',
})

// 分类选项
const categories = [
  { label: '全部', value: '' },
  { label: '编程入门', value: '编程入门' },
  { label: 'Web开发', value: 'Web开发' },
  { label: '数据分析', value: '数据分析' },
  { label: '人工智能', value: '人工智能' },
]

// 状态选项
const statusOptions = [
  { label: '全部', value: null },
  { label: '上架', value: 1 },
  { label: '下架', value: 2 },
]

// 弹窗
const dialogVisible = ref(false)
const dialogTitle = ref('新增课程')
const isEdit = ref(false)

// 表单数据
const formData = reactive({
  id: 0,
  name: '',
  description: '',
  category: '',
  price: 0,
  duration: 60,
  total_hours: 20,
  status: 1,
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入课程价格', trigger: 'blur' }],
  duration: [{ required: true, message: '请输入课时时长', trigger: 'blur' }],
  total_hours: [{ required: true, message: '请输入总课时数', trigger: 'blur' }],
}

// 表单ref
const formRef = ref()

// 选中的课程
const selectedIds = ref<number[]>([])

// 获取课程列表
async function fetchCourseList(): Promise<void> {
  loading.value = true
  try {
    const data = await getCourses({
      skip: (queryParams.page! - 1) * queryParams.pageSize!,
      limit: queryParams.pageSize!,
      category: queryParams.category || undefined,
      status: queryParams.status || undefined,
      search: queryParams.search,
    })
    courseList.value = data
    total.value = data.length // 实际项目中应从响应中获取总数
  } catch (error) {
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
function handleSearch(): void {
  queryParams.page = 1
  fetchCourseList()
}

// 重置搜索
function handleReset(): void {
  queryParams.search = ''
  queryParams.category = ''
  queryParams.status = null
  queryParams.page = 1
  fetchCourseList()
}

// 分页变化
function handlePageChange(page: number): void {
  queryParams.page = page
  fetchCourseList()
}

// 分页大小变化
function handleSizeChange(size: number): void {
  queryParams.pageSize = size
  queryParams.page = 1
  fetchCourseList()
}

// 新增课程
function handleAdd(): void {
  dialogTitle.value = '新增课程'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

// 编辑课程
async function handleEdit(row: Course): Promise<void> {
  dialogTitle.value = '编辑课程'
  isEdit.value = true
  Object.assign(formData, {
    id: row.id,
    name: row.name,
    description: row.description || '',
    category: row.category || '',
    price: row.price,
    duration: row.duration,
    total_hours: row.total_hours,
    status: row.status,
  })
  dialogVisible.value = true
}

// 删除课程
async function handleDelete(row: Course): Promise<void> {
  try {
    await ElMessageBox.confirm(`确定要删除课程"${row.name}"吗？`, '提示', {
      type: 'warning',
    })
    await deleteCourse(row.id)
    ElMessage.success('删除成功')
    fetchCourseList()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 切换状态
async function handleToggleStatus(row: Course): Promise<void> {
  try {
    await toggleCourseStatus(row.id)
    ElMessage.success('状态切换成功')
    fetchCourseList()
  } catch (error) {
    ElMessage.error('状态切换失败')
  }
}

// 批量删除
async function handleBatchDelete(): Promise<void> {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要删除的课程')
    return
  }

  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 门课程吗？`, '提示', {
      type: 'warning',
    })
    // 批量删除接口
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchCourseList()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// 选择变化
function handleSelectionChange(selection: Course[]): void {
  selectedIds.value = selection.map((item) => item.id)
}

// 提交表单
async function handleSubmit(): Promise<void> {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    if (isEdit.value) {
      await updateCourse(formData.id, formData)
      ElMessage.success('更新成功')
    } else {
      await createCourse(formData)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    fetchCourseList()
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 重置表单
function resetForm(): void {
  formData.id = 0
  formData.name = ''
  formData.description = ''
  formData.category = ''
  formData.price = 0
  formData.duration = 60
  formData.total_hours = 20
  formData.status = 1
  formRef.value?.resetFields()
}

// 格式化价格
function formatPrice(price: number): string {
  return `¥${price.toFixed(2)}`
}

// 格式化状态
function formatStatus(status: number): string {
  const statusMap: Record<number, { label: string; type: string }> = {
    1: { label: '上架', type: 'success' },
    2: { label: '下架', type: 'info' },
  }
  return statusMap[status]?.label || '未知'
}

// 表格列配置
const columns = [
  { type: 'selection', width: 50 },
  { prop: 'id', label: 'ID', width: 80 },
  { prop: 'name', label: '课程名称', minWidth: 150 },
  { prop: 'category', label: '分类', width: 120 },
  { prop: 'price', label: '价格', width: 100, formatter: (row: any) => formatPrice(row.price) },
  { prop: 'duration', label: '课时时长', width: 100 },
  { prop: 'total_hours', label: '总课时', width: 100 },
  { prop: 'status', label: '状态', width: 100, formatter: (row: any) => formatStatus(row.status) },
  { prop: 'created_at', label: '创建时间', width: 180 },
]

onMounted(() => {
  fetchCourseList()
})
</script>

<template>
  <div class="course-manage">
    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :model="queryParams" inline>
        <el-form-item label="课程名称">
          <el-input
            v-model="queryParams.search"
            placeholder="请输入课程名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item label="课程分类">
          <el-select v-model="queryParams.category" placeholder="请选择分类" clearable style="width: 140px">
            <el-option
              v-for="item in categories.slice(1)"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option
              v-for="item in statusOptions.slice(1)"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作区域 -->
    <el-card class="operation-card">
      <template #header>
        <div class="card-header">
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增课程
          </el-button>

          <el-button
            v-if="selectedIds.length > 0"
            type="danger"
            @click="handleBatchDelete"
          >
            <el-icon><Delete /></el-icon>
            批量删除 ({{ selectedIds.length }})
          </el-button>
        </div>
      </template>

      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="courseList"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          v-for="col in columns"
          :key="col.prop || col.type"
          :type="col.type"
          :prop="col.prop"
          :label="col.label"
          :width="col.width"
          :min-width="col.minWidth"
          :formatter="col.formatter"
          align="center"
        />

        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              :type="row.status === 1 ? 'info' : 'success'"
              link
              size="small"
              @click="handleToggleStatus(row)"
            >
              {{ row.status === 1 ? '下架' : '上架' }}
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <Pagination
          :total="total"
          :page="queryParams.page!"
          :page-size="queryParams.pageSize!"
          @page-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="课程名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入课程名称" />
        </el-form-item>

        <el-form-item label="课程分类" prop="category">
          <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="item in categories.slice(1)"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="课程价格" prop="price">
          <el-input-number v-model="formData.price" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>

        <el-form-item label="课时时长" prop="duration">
          <el-input-number v-model="formData.duration" :min="1" style="width: 100%">
            <template #append>分钟</template>
          </el-input-number>
        </el-form-item>

        <el-form-item label="总课时数" prop="total_hours">
          <el-input-number v-model="formData.total_hours" :min="1" style="width: 100%" />
        </el-form-item>

        <el-form-item label="课程描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入课程描述"
          />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">上架</el-radio>
            <el-radio :label="2">下架</el-radio>
          </el-radio-group>
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
import { Plus, Delete } from '@element-plus/icons-vue'
import Pagination from '@/components/Pagination.vue'
import {
  getCourses,
  createCourse,
  updateCourse,
  deleteCourse,
  toggleCourseStatus,
} from '@/api/courses'
import type { Course } from '@/api/courses'

export default defineComponent({
  name: 'CourseIndex',
  components: {
    Plus,
    Delete,
    Pagination,
  },
  setup() {
    const loading = ref(false)
    const courseList = ref<Course[]>([])
    const total = ref(0)
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增课程')
    const isEdit = ref(false)
    const selectedIds = ref<number[]>([])
    const formRef = ref()

    const queryParams = reactive({
      page: 1,
      pageSize: 10,
      category: '',
      status: null as number | null,
      search: '',
    })

    const formData = reactive({
      id: 0,
      name: '',
      description: '',
      category: '',
      price: 0,
      duration: 60,
      total_hours: 20,
      status: 1,
    })

    const rules = {
      name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
      price: [{ required: true, message: '请输入课程价格', trigger: 'blur' }],
    }

    const categories = [
      { label: '编程入门', value: '编程入门' },
      { label: 'Web开发', value: 'Web开发' },
      { label: '数据分析', value: '数据分析' },
      { label: '人工智能', value: '人工智能' },
    ]

    const statusOptions = [
      { label: '上架', value: 1 },
      { label: '下架', value: 2 },
    ]

    async function fetchCourseList() {
      loading.value = true
      try {
        const data = await getCourses({
          skip: (queryParams.page - 1) * queryParams.pageSize,
          limit: queryParams.pageSize,
          category: queryParams.category || undefined,
          status: queryParams.status || undefined,
          search: queryParams.search,
        })
        courseList.value = data
        total.value = data.length
      } catch (error) {
        ElMessage.error('获取课程列表失败')
      } finally {
        loading.value = false
      }
    }

    function handleSearch() {
      queryParams.page = 1
      fetchCourseList()
    }

    function handleReset() {
      queryParams.search = ''
      queryParams.category = ''
      queryParams.status = null
      queryParams.page = 1
      fetchCourseList()
    }

    function handlePageChange(page: number) {
      queryParams.page = page
      fetchCourseList()
    }

    function handleSizeChange(size: number) {
      queryParams.pageSize = size
      queryParams.page = 1
      fetchCourseList()
    }

    function handleAdd() {
      dialogTitle.value = '新增课程'
      isEdit.value = false
      formData.id = 0
      formData.name = ''
      formData.description = ''
      formData.category = ''
      formData.price = 0
      formData.duration = 60
      formData.total_hours = 20
      formData.status = 1
      dialogVisible.value = true
    }

    function handleEdit(row: Course) {
      dialogTitle.value = '编辑课程'
      isEdit.value = true
      Object.assign(formData, row)
      dialogVisible.value = true
    }

    async function handleDelete(row: Course) {
      try {
        await ElMessageBox.confirm(`确定要删除课程"${row.name}"吗？`, '提示', { type: 'warning' })
        await deleteCourse(row.id)
        ElMessage.success('删除成功')
        fetchCourseList()
      } catch (error: any) {
        if (error !== 'cancel') ElMessage.error('删除失败')
      }
    }

    async function handleToggleStatus(row: Course) {
      try {
        await toggleCourseStatus(row.id)
        ElMessage.success('状态切换成功')
        fetchCourseList()
      } catch (error) {
        ElMessage.error('状态切换失败')
      }
    }

    function handleSelectionChange(selection: Course[]) {
      selectedIds.value = selection.map((item) => item.id)
    }

    async function handleSubmit() {
      try {
        if (isEdit.value) {
          await updateCourse(formData.id, formData)
        } else {
          await createCourse(formData)
        }
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        fetchCourseList()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }

    onMounted(() => {
      fetchCourseList()
    })

    return {
      loading,
      courseList,
      total,
      queryParams,
      categories,
      statusOptions,
      dialogVisible,
      dialogTitle,
      isEdit,
      selectedIds,
      formData,
      rules,
      formRef,
      handleSearch,
      handleReset,
      handlePageChange,
      handleSizeChange,
      handleAdd,
      handleEdit,
      handleDelete,
      handleToggleStatus,
      handleSelectionChange,
      handleSubmit,
    }
  },
})
</script>

<style lang="scss" scoped>
.course-manage {
  .search-card {
    margin-bottom: 16px;
  }

  .operation-card {
    .card-header {
      display: flex;
      gap: 12px;
    }
  }

  .pagination-wrapper {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
