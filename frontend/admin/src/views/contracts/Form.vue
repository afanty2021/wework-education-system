<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getContract, createContract, updateContract } from '@/api/contracts'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const formRef = ref()

const formData = reactive({
  id: 0,
  contract_no: '',
  student_id: 0,
  course_id: undefined as number | undefined,
  total_hours: 20,
  unit_price: 100,
  discount_amount: 0,
  start_date: '',
  end_date: '',
  remark: '',
})

const rules = {
  contract_no: [{ required: true, message: '请输入合同编号', trigger: 'blur' }],
  student_id: [{ required: true, message: '请选择学员', trigger: 'change' }],
  total_hours: [{ required: true, message: '请输入总课时', trigger: 'blur' }],
  unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
}

const isEdit = computed(() => !!route.params.id)

async function fetchDetail() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const data = await getContract(Number(route.params.id))
    Object.assign(formData, data)
  } catch { ElMessage.error('获取合同详情失败') }
  finally { loading.value = false }
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    if (isEdit.value) await updateContract(formData.id, formData)
    else await createContract(formData)
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    router.push('/contracts')
  } catch { ElMessage.error('操作失败') }
}

function handleReset() { formRef.value?.resetFields() }
function goBack() { router.push('/contracts') }

onMounted(() => { if (isEdit.value) fetchDetail() })
</script>

<template>
  <div class="contract-form">
    <el-card>
      <template #header>
        <el-page-header @back="goBack">
          <template #content>
            <span class="page-title">{{ isEdit ? '编辑合同' : '新增合同' }}</span>
          </template>
        </el-page-header>
      </template>
      <el-form ref="formRef" v-loading="loading" :model="formData" :rules="rules" label-width="100px" style="max-width: 800px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="合同编号" prop="contract_no">
              <el-input v-model="formData.contract_no" placeholder="请输入合同编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学员" prop="student_id">
              <el-select v-model="formData.student_id" placeholder="请选择学员" style="width: 100%">
                <el-option label="张三" :value="1" />
                <el-option label="李四" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="课程">
              <el-select v-model="formData.course_id" placeholder="请选择课程" style="width: 100%" clearable>
                <el-option label="Python入门" :value="1" />
                <el-option label="Java进阶" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总课时" prop="total_hours">
              <el-input-number v-model="formData.total_hours" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单价" prop="unit_price">
              <el-input-number v-model="formData.unit_price" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="折扣金额">
              <el-input-number v-model="formData.discount_amount" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="开始日期">
              <el-date-picker v-model="formData.start_date" type="date" placeholder="请选择开始日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期">
              <el-date-picker v-model="formData.end_date" type="date" placeholder="请选择结束日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">{{ isEdit ? '保存修改' : '创建合同' }}</el-button>
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
import { getContract, createContract, updateContract } from '@/api/contracts'

export default defineComponent({
  name: 'ContractForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const formRef = ref()

    const formData = reactive({
      id: 0,
      contract_no: '',
      student_id: 0,
      course_id: undefined as number | undefined,
      total_hours: 20,
      unit_price: 100,
      discount_amount: 0,
      start_date: '',
      end_date: '',
      remark: '',
    })

    const rules = {
      contract_no: [{ required: true, message: '请输入合同编号', trigger: 'blur' }],
      student_id: [{ required: true, message: '请选择学员', trigger: 'change' }],
      total_hours: [{ required: true, message: '请输入总课时', trigger: 'blur' }],
      unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
    }

    const isEdit = computed(() => !!route.params.id)

    async function fetchDetail() {
      if (!isEdit.value) return
      loading.value = true
      try {
        const data = await getContract(Number(route.params.id))
        Object.assign(formData, data)
      } catch { ElMessage.error('获取合同详情失败') }
      finally { loading.value = false }
    }

    async function handleSubmit() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        if (isEdit.value) await updateContract(formData.id, formData)
        else await createContract(formData)
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        router.push('/contracts')
      } catch { ElMessage.error('操作失败') }
    }

    function handleReset() { formRef.value?.resetFields() }
    function goBack() { router.push('/contracts') }

    onMounted(() => { if (isEdit.value) fetchDetail() })

    return { loading, formData, rules, formRef, isEdit, handleSubmit, handleReset, goBack }
  },
})
</script>

<style lang="scss" scoped>
.contract-form { .page-title { font-size: 18px; font-weight: 600; } }
</style>
