<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getStudent, createStudent, updateStudent } from '@/api/students'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const formRef = ref()
const allTags = ref<string[]>([])

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

const rules = {
  name: [{ required: true, message: '请输入学员姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
}

const isEdit = computed(() => !!route.params.id)

async function fetchDetail() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const data = await getStudent(Number(route.params.id))
    Object.assign(formData, data)
  } catch { ElMessage.error('获取学员详情失败') }
  finally { loading.value = false }
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateStudent(formData.id, formData)
    else await createStudent(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    router.push('/students')
  } catch { ElMessage.error('操作失败') }
}

function handleReset() { formRef.value?.resetFields() }
function goBack() { router.push('/students') }

onMounted(() => { if (isEdit.value) fetchDetail() })
</script>

<template>
  <div class="student-form">
    <el-card>
      <template #header>
        <el-page-header @back="goBack">
          <template #content>
            <span class="page-title">{{ isEdit ? '编辑学员' : '新增学员' }}</span>
          </template>
        </el-page-header>
      </template>
      <el-form ref="formRef" v-loading="loading" :model="formData" :rules="rules" label-width="100px" style="max-width: 800px">
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
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio :label="1">潜在</el-radio>
                <el-radio :label="2">在读</el-radio>
                <el-radio :label="3">已流失</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="标签">
              <el-select v-model="formData.tags" multiple filterable allow-create placeholder="请选择或创建标签" style="width: 100%">
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
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">{{ isEdit ? '保存修改' : '创建学员' }}</el-button>
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
import { getStudent, createStudent, updateStudent } from '@/api/students'

export default defineComponent({
  name: 'StudentForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const formRef = ref()
    const allTags = ref<string[]>([])

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

    const rules = {
      name: [{ required: true, message: '请输入学员姓名', trigger: 'blur' }],
      phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
    }

    const isEdit = computed(() => !!route.params.id)

    async function fetchDetail() {
      if (!isEdit.value) return
      loading.value = true
      try {
        const data = await getStudent(Number(route.params.id))
        Object.assign(formData, data)
      } catch { ElMessage.error('获取学员详情失败') }
      finally { loading.value = false }
    }

    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateStudent(formData.id, formData)
        else await createStudent(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        router.push('/students')
      } catch { ElMessage.error('操作失败') }
    }

    function handleReset() { formRef.value?.resetFields() }
    function goBack() { router.push('/students') }

    onMounted(() => { if (isEdit.value) fetchDetail() })

    return { loading, formData, rules, formRef, isEdit, allTags, handleSubmit, handleReset, goBack }
  },
})
</script>

<style lang="scss" scoped>
.student-form { .page-title { font-size: 18px; font-weight: 600; } }
</style>
