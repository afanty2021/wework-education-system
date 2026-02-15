<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

// Props
const props = defineProps<{
  modelValue: boolean
  title: string
  width?: string | number
  fullscreen?: boolean
  top?: string | number
  destroyOnClose?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()

// 弹窗显示
const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

// 表单ref
const formRef = ref<FormInstance>()

// 表单数据
const formData = ref<Record<string, any>>({})

// 表单规则
const rules = ref<FormRules>({})

// 是否加载中
const loading = ref(false)

// 插槽内容
const slotContent = ref<any>(null)

// 设置表单数据
function setFormData(data: Record<string, any>): void {
  formData.value = { ...data }
}

// 获取表单数据
function getFormData(): Record<string, any> {
  return { ...formData.value }
}

// 重置表单
function resetForm(): void {
  formRef.value?.resetFields()
}

// 表单验证
async function validate(): Promise<boolean> {
  if (!formRef.value) return false
  try {
    await formRef.value.validate()
    return true
  } catch {
    return false
  }
}

// 显示加载状态
function showLoading(): void {
  loading.value = true
}

// 隐藏加载状态
function hideLoading(): void {
  loading.value = false
}

// 确认
async function handleConfirm(): Promise<void> {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    emit('confirm')
  } catch {
    ElMessage.warning('请完善表单信息')
  }
}

// 取消
function handleCancel(): void {
  visible.value = false
  emit('cancel')
}

// 打开弹窗
function open(): void {
  visible.value = true
}

// 关闭弹窗
function close(): void {
  visible.value = false
}

// 暴露方法
defineExpose({
  setFormData,
  getFormData,
  resetForm,
  validate,
  showLoading,
  hideLoading,
  open,
  close,
})
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="title"
    :width="width || '600px'"
    :top="top || '100px'"
    :fullscreen="fullscreen"
    :destroy-on-close="destroyOnClose"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    class="form-dialog"
  >
    <template #header>
      <div class="dialog-header">
        <span class="title">{{ title }}</span>
      </div>
    </template>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      :label-width="100"
      :size="size"
      class="dialog-form"
    >
      <slot :formData="formData" :setFormData="setFormData" :loading="loading" />
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel" :loading="loading">取消</el-button>
        <el-button type="primary" @click="handleConfirm" :loading="loading">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import { defineComponent, ref, computed, provide } from 'vue'
import type { FormInstance } from 'element-plus'

export default defineComponent({
  name: 'FormDialog',
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    width: {
      type: [String, Number],
      default: '600px',
    },
    fullscreen: {
      type: Boolean,
      default: false,
    },
    top: {
      type: [String, Number],
      default: '100px',
    },
    destroyOnClose: {
      type: Boolean,
      default: true,
    },
  },
  emits: ['update:modelValue', 'confirm', 'cancel'],
  setup(props, { emit, expose }) {
    const formRef = ref<FormInstance>()
    const formData = ref<Record<string, any>>({})
    const rules = ref<FormRules>({})
    const loading = ref(false)

    const visible = computed({
      get: () => props.modelValue,
      set: (val) => emit('update:modelValue', val),
    })

    function setFormData(data: Record<string, any>) {
      formData.value = { ...data }
    }

    function getFormData() {
      return { ...formData.value }
    }

    function resetForm() {
      formRef.value?.resetFields()
    }

    async function validate() {
      if (!formRef.value) return false
      try {
        await formRef.value.validate()
        return true
      } catch {
        return false
      }
    }

    function showLoading() {
      loading.value = true
    }

    function hideLoading() {
      loading.value = false
    }

    async function handleConfirm() {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        emit('confirm')
      } catch {
        console.warn('表单验证失败')
      }
    }

    function handleCancel() {
      visible.value = false
      emit('cancel')
    }

    function open() {
      visible.value = true
    }

    function close() {
      visible.value = false
    }

    expose({
      setFormData,
      getFormData,
      resetForm,
      validate,
      showLoading,
      hideLoading,
      open,
      close,
    })

    return {
      formRef,
      formData,
      rules,
      loading,
      visible,
      setFormData,
      getFormData,
      resetForm,
      validate,
      showLoading,
      hideLoading,
      handleConfirm,
      handleCancel,
      open,
      close,
    }
  },
})
</script>

<style lang="scss" scoped>
.form-dialog {
  :deep(.el-dialog) {
    border-radius: 8px;
  }

  :deep(.el-dialog__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--el-border-color);
  }

  .dialog-header {
    .title {
      font-size: 16px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  :deep(.el-dialog__body) {
    padding: 20px;
  }

  :deep(.el-dialog__footer) {
    padding: 16px 20px;
    border-top: 1px solid var(--el-border-color);
  }

  .dialog-form {
    max-height: 60vh;
    overflow-y: auto;
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
}
</style>
