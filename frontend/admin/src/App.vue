<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'

const appStore = useAppStore()
const { isDark } = storeToRefs(appStore)
</script>

<template>
  <el-config-provider :locale="appStore.locale" :size="appStore.size">
    <RouterView />
  </el-config-provider>
</template>

<style lang="scss">
// 深色模式样式
html.dark {
  --el-bg-color: #1d1d1d;
  --el-bg-color-overlay: #2c2c2c;
  --el-fill-color-blank: #2c2c2c;
  --el-fill-color-light: #3a3a3a;
  --el-fill-color-lighter: #414243;
  --el-border-color: #4c4d4f;
  --el-border-color-light: #58595b;
  --el-border-color-lighter: #636465;
  --el-text-color-primary: #e5eaf3;
  --el-text-color-regular: #cfd3dc;
  --el-text-color-secondary: #a3a6ad;
  --el-text-color-placeholder: #8d9095;
}
</style>
