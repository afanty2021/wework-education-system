<template>
  <div class="main-layout">
    <!-- 主内容区域 -->
    <div class="main-content">
      <router-view />
    </div>

    <!-- 底部导航栏 -->
    <TabBar />
  </div>
</template>

<script setup lang="ts">
import TabBar from './TabBar.vue'
</script>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f5f5f5;
}

.main-content {
  flex: 1;
  padding-bottom: 60px;
  overflow-x: hidden;
}
</style>
