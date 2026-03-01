/**
 * TableSkeleton 表格骨架屏组件
 *
 * @description 表格数据加载时显示的骨架屏，提升用户体验
 *
 * @example
 * ```vue
 * <TableSkeleton :rows="5" :columns="4" />
 * ```
 */
<script setup lang="ts">
/**
 * 骨架屏属性
 */
interface Props {
  /** 骨架屏行数 */
  rows?: number
  /** 骨架屏列数 */
  columns?: number
  /** 是否显示操作列 */
  showActions?: boolean
}

withDefaults(defineProps<Props>(), {
  rows: 5,
  columns: 4,
  showActions: true,
})
</script>

<template>
  <div class="table-skeleton">
    <!-- 表头 -->
    <div class="skeleton-header">
      <div v-for="col in columns" :key="`header-${col}`" class="skeleton-cell header" />
      <div v-if="showActions" class="skeleton-cell header action" />
    </div>

    <!-- 表格行 -->
    <div v-for="row in rows" :key="`row-${row}`" class="skeleton-row">
      <div v-for="col in columns" :key="`${row}-${col}`" class="skeleton-cell" />
      <div v-if="showActions" class="skeleton-cell action">
        <div class="skeleton-button" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use 'sass:color';

$skeleton-base-color: #f0f2f5;
$skeleton-highlight-color: #e6e8eb;

.table-skeleton {
  width: 100%;
}

.skeleton-header {
  display: flex;
  padding: 12px 16px;
  background-color: $skeleton-base-color;
  border-radius: 4px 4px 0 0;
}

.skeleton-row {
  display: flex;
  padding: 14px 16px;
  border-bottom: 1px solid #f0f2f5;

  &:last-child {
    border-bottom: none;
  }
}

.skeleton-cell {
  flex: 1;
  height: 16px;
  margin-right: 16px;
  background: linear-gradient(
    90deg,
    $skeleton-base-color 25%,
    $skeleton-highlight-color 50%,
    $skeleton-base-color 75%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-loading 1.5s ease-in-out infinite;

  &:last-child {
    margin-right: 0;
  }

  &.header {
    height: 14px;
    background-color: $skeleton-highlight-color;
  }

  &.action {
    width: 120px;
    flex: none;
  }
}

.skeleton-button {
  width: 60px;
  height: 24px;
  background: linear-gradient(
    90deg,
    $skeleton-base-color 25%,
    $skeleton-highlight-color 50%,
    $skeleton-base-color 75%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
