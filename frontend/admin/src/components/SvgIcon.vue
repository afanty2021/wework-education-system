<script setup lang="ts">
import { useAttrs, useSlots, computed } from 'vue'

// Props
const props = defineProps<{
  name: string
  size?: number | string
  color?: string
}>()

// 属性
const attrs = useAttrs()
const slots = useSlots()

// 图标样式
const iconStyle = computed(() => {
  const style: Record<string, string> = {}

  if (props.size) {
    style.fontSize = `${props.size}px`
  }

  if (props.color) {
    style.color = props.color
  }

  return { ...style, ...attrs.style }
})
</script>

<template>
  <svg class="svg-icon" :style="iconStyle" aria-hidden="true">
    <use :xlink:href="`#icon-${name}`" :fill="color" />
  </svg>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'SvgIcon',
  props: {
    name: {
      type: String,
      required: true,
    },
    size: {
      type: [Number, String],
      default: 16,
    },
    color: {
      type: String,
      default: '',
    },
  },
})
</script>

<style lang="scss" scoped>
.svg-icon {
  width: 1em;
  height: 1em;
  overflow: hidden;
  vertical-align: -0.15em;
  fill: currentColor;
}
</style>
