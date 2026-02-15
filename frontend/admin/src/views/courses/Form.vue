<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCourse, createCourse, updateCourse } from '@/api/courses'

const route = useRoute()
const router = useRouter()

// 加载状态
const loading = ref(false)

// 表单数据
const formData = reactive({
  id: 0,
  name: '',
  description: '',
  category: '',
  price: 0,
  duration: 60,
  total_hours: 20,
  cover_image: '',
  status: 1,
})

// 分类选项
const categories = [
  { label: '编程入门', value: '编程入门' },
  { label: 'Web开发', value: 'Web开发' },
  { label: '数据分析', value: '数据分析' },
  { label: '人工智能', value: '人工智能' },
]

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入课程价格', trigger: 'blur' }],
  duration: [{ required: true, message: '请输入课时时长', trigger: 'blur' }],
  total_hours: [{ required: true, message: '请输入总课时数', trigger: 'blur' }],
}

// 表单ref
const formRef = ref()

// 是否编辑模式
const isEdit = computed(() => !!route.params.id)

// 获取课程详情
async function fetchCourseDetail(): Promise<void> {
  if (!isEdit.value) return

  loading.value = true
  try {
    const data = await getCourse(Number(route.params.id))
    Object.assign(formData, data)
  } catch (error) {
    ElMessage.error('获取课程详情失败')
  } finally {
    loading.value = false
  }
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

    router.push('/courses')
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 重置表单
function handleReset(): void {
  formRef.value?.resetFields()
}

// 返回列表
function goBack(): void {
  router.push('/courses')
}

onMounted(() => {
  if (isEdit.value) {
    fetchCourseDetail()
  }
})
</script>

<template>
  <div class="course-form">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-page-header @back="goBack">
            <template #content>
              <span class="page-title">{{ isEdit ? '编辑课程' : '新增课程' }}</span>
            </template>
          </el-page-header>
        </div>
      </template>

      <el-form
        ref="formRef"
        v-loading="loading"
        :model="formData"
        :rules="rules"
        label-width="120px"
        style="max-width: 800px"
      >
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="课程名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入课程名称" />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="课程分类" prop="category">
              <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%">
                <el-option
                  v-for="item in categories"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="课程价格" prop="price">
              <el-input-number v-model="formData.price" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="课时时长" prop="duration">
              <el-input-number v-model="formData.duration" :min="1" style="width: 100%">
                <template #append>分钟</template>
              </el-input-number>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="总课时数" prop="total_hours">
              <el-input-number v-model="formData.total_hours" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="课程封面">
              <el-upload
                action="#"
                list-type="picture-card"
                :auto-upload="false"
                :show-file-list="false"
              >
                <el-icon><Plus /></el-icon>
              </el-upload>
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="课程描述" prop="description">
              <el-input
                v-model="formData.description"
                type="textarea"
                :rows="4"
                placeholder="请输入课程描述"
              />
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="formData.status">
                <el-radio :label="1">上架</el-radio>
                <el-radio :label="2">下架</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '创建课程' }}
          </el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getCourse, createCourse, updateCourse } from '@/api/courses'

export default defineComponent({
  name: 'CourseForm',
  components: {
    Plus,
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const formRef = ref()

    const formData = reactive({
      id: 0,
      name: '',
      description: '',
      category: '',
      price: 0,
      duration: 60,
      total_hours: 20,
      cover_image: '',
      status: 1,
    })

    const categories = [
      { label: '编程入门', value: '编程入门' },
      { label: 'Web开发', value: 'Web开发' },
      { label: '数据分析', value: '数据分析' },
      { label: '人工智能', value: '人工智能' },
    ]

    const rules = {
      name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
      price: [{ required: true, message: '请输入课程价格', trigger: 'blur' }],
    }

    const isEdit = computed(() => !!route.params.id)

    async function fetchCourseDetail() {
      if (!isEdit.value) return
      loading.value = true
      try {
        const data = await getCourse(Number(route.params.id))
        Object.assign(formData, data)
      } catch (error) {
        ElMessage.error('获取课程详情失败')
      } finally {
        loading.value = false
      }
    }

    async function handleSubmit() {
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
        router.push('/courses')
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }

    function handleReset() {
      formRef.value?.resetFields()
    }

    function goBack() {
      router.push('/courses')
    }

    onMounted(() => {
      if (isEdit.value) {
        fetchCourseDetail()
      }
    })

    return {
      loading,
      formData,
      categories,
      rules,
      formRef,
      isEdit,
      handleSubmit,
      handleReset,
      goBack,
    }
  },
})
</script>

<style lang="scss" scoped>
.course-form {
  .card-header {
    display: flex;
    align-items: center;
  }

  .page-title {
    font-size: 18px;
    font-weight: 600;
  }
}
</style>
