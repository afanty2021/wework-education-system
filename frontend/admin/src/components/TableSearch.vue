<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Props
const props = withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
    size?: 'small' | 'medium' | 'large'
    disabled?: boolean
    clearable?: boolean
  }>(),
  {
    size: 'medium',
    disabled: false,
    clearable: true,
  }
)

// Emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

// 输入值
const inputValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

// 搜索关键字
const keyword = ref('')

// 是否显示下拉建议
const showSuggestions = ref(false)

// 建议列表
const suggestions = ref<any[]>([])

// 加载状态
const loading = ref(false)

// 下拉框ref
const suggestionsRef = ref()

// 模拟搜索（实际应用中替换为真实搜索）
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

// 防抖搜索
let searchTimer: ReturnType<typeof setTimeout>
function debounceSearch(): void {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    handleSearch(keyword.value)
  }, 300)
}

// 选择建议
function selectSuggestion(item: any): void {
  inputValue.value = item.label
  showSuggestions.value = false
  keyword.value = ''
}

// 清空
function clearSearch(): void {
  keyword.value = ''
  suggestions.value = []
  showSuggestions.value = false
}

// 点击外部关闭
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
</script>

<template>
  <div class="table-search" :class="`size-${size}`">
    <el-input
      v-model="keyword"
      :placeholder="placeholder || '搜索...'"
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

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onUnmounted } from 'vue'

export default defineComponent({
  name: 'TableSearch',
  props: {
    modelValue: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '',
    },
    size: {
      type: String as () => 'small' | 'medium' | 'large',
      default: 'medium',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: true,
    },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const keyword = ref('')
    const showSuggestions = ref(false)
    const suggestions = ref<any[]>([])
    const loading = ref(false)

    const inputValue = computed({
      get: () => props.modelValue,
      set: (val) => emit('update:modelValue', val),
    })

    async function handleSearch(query: string) {
      if (!query.trim()) {
        suggestions.value = []
        return
      }

      loading.value = true
      showSuggestions.value = true

      try {
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

    let searchTimer: ReturnType<typeof setTimeout>
    function debounceSearch() {
      clearTimeout(searchTimer)
      searchTimer = setTimeout(() => {
        handleSearch(keyword.value)
      }, 300)
    }

    function selectSuggestion(item: any) {
      inputValue.value = item.label
      showSuggestions.value = false
      keyword.value = ''
    }

    function clearSearch() {
      keyword.value = ''
      suggestions.value = []
      showSuggestions.value = false
    }

    function handleClickOutside(event: MouseEvent) {
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

    return {
      keyword,
      showSuggestions,
      suggestions,
      loading,
      inputValue,
      handleSearch,
      debounceSearch,
      selectSuggestion,
      clearSearch,
    }
  },
})
</script>

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
