<script setup lang="ts">
import { computed } from 'vue'
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

// 主体区域样式
const mainStyle = computed(() => ({
  marginLeft: appStore.sidebarWidth,
  minHeight: '100vh',
  transition: 'margin-left 0.3s',
}))
</script>

<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <Sidebar />

    <!-- 主内容区 -->
    <div class="app-main" :style="mainStyle">
      <!-- 顶部导航 -->
      <Header />

      <!-- 页面内容 -->
      <div class="app-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.app-layout {
  min-height: 100vh;
  background-color: var(--el-bg-color);
}

.app-main {
  position: relative;
}

.app-content {
  padding: 20px;
  padding-top: 80px;
  min-height: calc(100vh - 60px);
  background-color: var(--el-bg-color);
}

// 过渡动画
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
