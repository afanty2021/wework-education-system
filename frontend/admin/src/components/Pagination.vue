<script setup lang="ts">
import { computed } from 'vue'

// Props
const props = defineProps<{
  total: number
  page?: number
  pageSize?: number
}>()

// Emits
const emit = defineEmits<{
  (e: 'update:page', value: number): void
  (e: 'update:pageSize', value: number): void
  (e: 'size-change', value: number): void
  (e: 'current-change', value: number): void
  (e: 'change', page: number, pageSize: number): void
}>()

// 分页数据
const currentPage = computed({
  get: () => props.page || 1,
  set: (val: number) => emit('update:page', val),
})

const size = computed({
  get: () => props.pageSize || 10,
  set: (val: number) => emit('update:pageSize', val),
})

const totalPage = computed(() => Math.ceil(props.total / size.value))

// 页大小选项
const pageSizeOptions = [
  { label: '10条/页', value: 10 },
  { label: '20条/页', value: 20 },
  { label: '50条/页', value: 50 },
  { label: '100条/页', value: 100 },
]

// 处理页大小变化
function handleSizeChange(val: number): void {
  emit('update:pageSize', val)
  emit('size-change', val)
  emit('change', currentPage.value, val)
}

// 处理页码变化
function handleCurrentChange(val: number): void {
  emit('update:page', val)
  emit('current-change', val)
  emit('change', val, size.value)
}

// 页码格式化
function getPageIndex(index: number): number {
  return index
}
</script>

<template>
  <div class="pagination-wrapper">
    <div class="pagination-info">
      共
      <span class="total">{{ total }}</span>
      条记录
    </div>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="size"
      :page-sizes="pageSizeOptions"
      :total="total"
      :background="true"
      layout="prev, pager, next, sizes, jumper, total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<style lang="scss" scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.pagination-info {
  font-size: 14px;
  color: var(--el-text-color-regular);

  .total {
    margin: 0 4px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}
</style>
