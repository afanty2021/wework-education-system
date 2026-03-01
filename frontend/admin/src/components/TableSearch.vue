/**
 * TableSearch 表格搜索组件
 *
 * @description 带搜索建议的表格搜索输入框组件，支持防抖搜索和下拉建议
 *
 * @example
 * ```vue
 * <TableSearch
 *   v-model="searchText"
 *   placeholder="请输入搜索内容"
 *   @search="handleSearch"
 * />
 * ```
 */
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

/**
 * 组件属性
 */
interface Props {
  /** v-model 绑定值 */
  modelValue?: string
  /** 占位符文本 */
  placeholder?: string
  /** 输入框尺寸 */
  size?: 'small' | 'medium' | 'large'
  /** 是否禁用 */
  disabled?: boolean
  /** 是否可清除 */
  clearable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: '搜索...',
  size: 'medium',
  disabled: false,
  clearable: true,
})

/**
 * 组件事件
 */
const emit = defineEmits<{
  /** v-model 更新事件 */
  (e: 'update:modelValue', value: string): void
  /** 搜索事件 */
  (e: 'search', value: string): void
}>()

// 输入值双向绑定
const inputValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

// 搜索关键字
const keyword = ref('')

// 是否显示下拉建议
const showSuggestions = ref(false)

// 建议列表
const suggestions = ref<Array<{ label: string; value: string }>>([])

// 加载状态
const loading = ref(false)

// 下拉框 ref
const suggestionsRef = ref<HTMLElement>()

/**
 * 执行搜索
 * @param query - 搜索关键字
 */
async function handleSearch(query: string): Promise<void> {
  if (!query.trim()) {
    suggestions.value = []
    return
  }

  loading.value = true
  showSuggestions.value = true

  try {
    // TODO: 替换为真实搜索接口
    await new Promise((resolve) => setTimeout(resolve, 300))
    suggestions.value = [
      { label: `${query} - 选项1`, value: `${query}-1` },
      { label: `${query} - 选项2`, value: `${query}-2` },
      { label: `${query} - 选项3`, value: `${query}-3` },
    ].filter((item) => item.label.toLowerCase().includes(query.toLowerCase()))
  } finally {
    loading.value = false
  }
}

/**
 * 防抖搜索
 */
let searchTimer: ReturnType<typeof setTimeout>
function debounceSearch(): void {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    handleSearch(keyword.value)
  }, 300)
}

/**
 * 选择建议项
 * @param item - 选中的建议项
 */
function selectSuggestion(item: { label: string; value: string }): void {
  inputValue.value = item.label
  showSuggestions.value = false
  keyword.value = ''
  emit('search', item.label)
}

/**
 * 清除搜索
 */
function clearSearch(): void {
  keyword.value = ''
  suggestions.value = []
  showSuggestions.value = false
  emit('update:modelValue', '')
}

/**
 * 点击外部关闭下拉框
 * @param event - 点击事件
 */
function handleClickOutside(event: MouseEvent): void {
  const target = event.target as HTMLElement
  if (!target.closest('.table-search')) {
    showSuggestions.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

defineOptions({
  name: 'TableSearch',
})
</script>

<template>
  <div class="table-search" :class="`size-${size}`">
    <el-input
      v-model="keyword"
      :placeholder="placeholder"
      :disabled="disabled"
      :clearable="clearable"
      prefix-icon="Search"
      @input="debounceSearch"
      @clear="clearSearch"
      @focus="keyword && handleSearch(keyword)"
    />

    <transition name="slide-down">
      <div v-if="showSuggestions && suggestions.length > 0" ref="suggestionsRef" class="suggestions">
        <div
          v-for="item in suggestions"
          :key="item.value"
          class="suggestion-item"
          @click="selectSuggestion(item)"
        >
          {{ item.label }}
        </div>
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
.table-search {
  position: relative;
  width: 260px;

  &.size-small {
    width: 200px;
  }

  &.size-large {
    width: 320px;
  }
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 100;
  width: 100%;
  margin-top: 4px;
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  box-shadow: var(--el-box-shadow-light);
  max-height: 240px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 8px 12px;
  font-size: 14px;
  color: var(--el-text-color-regular);
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--el-fill-color-light);
  }
}

// 过渡动画
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
