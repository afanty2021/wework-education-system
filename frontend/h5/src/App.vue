<template>
  <van-config-provider :theme="theme">
    <router-view />
  </van-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

const theme = computed(() => appStore.darkMode ? 'dark' : 'light')
</script>

<style scoped>
#app {
  width: 100%;
  height: 100%;
  min-height: 100vh;
}
</style>
