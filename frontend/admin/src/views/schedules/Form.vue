<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getSchedule, createSchedule, updateSchedule } from '@/api/schedules'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const formRef = ref()

const formData = reactive({
  id: 0,
  course_id: 0,
  teacher_id: 0,
  classroom_id: undefined as number | undefined,
  scheduled_date: '',
  start_time: '',
  end_time: '',
  capacity: 30,
  remark: '',
})

const rules = {
  course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }],
  scheduled_date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
}

const isEdit = computed(() => !!route.params.id)

async function fetchDetail() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const data = await getSchedule(Number(route.params.id))
    Object.assign(formData, data)
  } catch { ElMessage.error('获取排课详情失败') }
  finally { loading.value = false }
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateSchedule(formData.id, formData)
    else await createSchedule(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    router.push('/schedules')
  } catch { ElMessage.error('操作失败') }
}

function handleReset() { formRef.value?.resetFields() }
function goBack() { router.push('/schedules') }

onMounted(() => { if (isEdit.value) fetchDetail() })
</script>

<template>
  <div class="schedule-form">
    <el-card>
      <template #header>
        <el-page-header @back="goBack">
          <template #content>
            <span class="page-title">{{ isEdit ? '编辑排课' : '新增排课' }}</span>
          </template>
        </el-page-header>
      </template>
      <el-form ref="formRef" v-loading="loading" :model="formData" :rules="rules" label-width="100px" style="max-width: 800px">
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
              <el-time-picker v-model="formData.start_time" placeholder="开始时间" format="HH:mm" style="width: 45%" />
              <span style="margin: 0 8px">至</span>
              <el-time-picker v-model="formData.end_time" placeholder="结束时间" format="HH:mm" style="width: 45%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">{{ isEdit ? '保存修改' : '创建排课' }}</el-button>
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
import { getSchedule, createSchedule, updateSchedule } from '@/api/schedules'

export default defineComponent({
  name: 'ScheduleForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const formRef = ref()

    const formData = reactive({
      id: 0,
      course_id: 0,
      teacher_id: 0,
      classroom_id: undefined as number | undefined,
      scheduled_date: '',
      start_time: '',
      end_time: '',
      capacity: 30,
      remark: '',
    })

    const rules = {
      course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
      teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }],
      scheduled_date: [{ required: true, message: '请选择日期', trigger: 'change' }],
      start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
      end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
    }

    const isEdit = computed(() => !!route.params.id)

    async function fetchDetail() {
      if (!isEdit.value) return
      loading.value = true
      try {
        const data = await getSchedule(Number(route.params.id))
        Object.assign(formData, data)
      } catch { ElMessage.error('获取排课详情失败') }
      finally { loading.value = false }
    }

    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateSchedule(formData.id, formData)
        else await createSchedule(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        router.push('/schedules')
      } catch { ElMessage.error('操作失败') }
    }

    function handleReset() { formRef.value?.resetFields() }
    function goBack() { router.push('/schedules') }

    onMounted(() => { if (isEdit.value) fetchDetail() })

    return { loading, formData, rules, formRef, isEdit, handleSubmit, handleReset, goBack }
  },
})
</script>

<style lang="scss" scoped>
.schedule-form { .page-title { font-size: 18px; font-weight: 600; } }
</style>
