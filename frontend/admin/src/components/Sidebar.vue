<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import SvgIcon from '@/components/SvgIcon.vue'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

// 菜单列表
const menuItems = computed(() => appStore.menuItems)

// 是否收起
const isCollapsed = computed(() => appStore.sidebarCollapsed)

// 当前路由路径
const currentPath = computed(() => route.path)

// 切换侧边栏
function toggleSidebar(): void {
  appStore.toggleSidebar()
}

// 处理菜单点击
function handleMenuClick(item: any): void {
  if (item.path && item.children?.length === 0) {
    router.push(item.path)
  }
}
</script>

<template>
  <div class="app-sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Logo区域 -->
    <div class="sidebar-logo">
      <div class="logo-icon">
        <SvgIcon name="education" size="32" />
      </div>
      <transition name="fade">
        <div v-if="!isCollapsed" class="logo-text">
          <span class="logo-title">教务管理系统</span>
          <span class="logo-subtitle">Education</span>
        </div>
      </transition>
    </div>

    <!-- 菜单区域 -->
    <el-scrollbar class="sidebar-menu">
      <el-menu
        :default-active="currentPath"
        :collapse="isCollapsed"
        :unique-opened="true"
        background-color="transparent"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        router
      >
        <template v-for="item in menuItems" :key="item.path || item.title">
          <!-- 有子菜单 -->
          <el-sub-menu
            v-if="item.children && item.children.length > 0"
            :index="item.path || item.title"
          >
            <template #title>
              <SvgIcon v-if="item.icon" :name="item.icon" size="18" />
              <span>{{ item.title }}</span>
            </template>
            <template v-for="child in item.children" :key="child.path">
              <el-menu-item :index="child.path" :route="{ path: child.path }">
                <SvgIcon v-if="child.icon" :name="child.icon" size="16" />
                <span>{{ child.title }}</span>
              </el-menu-item>
            </template>
          </el-sub-menu>

          <!-- 无子菜单 -->
          <el-menu-item
            v-else
            :index="item.path"
            :route="{ path: item.path }"
          >
            <SvgIcon v-if="item.icon" :name="item.icon" size="18" />
            <span>{{ item.title }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-scrollbar>

    <!-- 收起/展开按钮 -->
    <div class="sidebar-toggle" @click="toggleSidebar">
      <el-icon :size="20">
        <component :is="isCollapsed ? 'Expand' : 'Fold'" />
      </el-icon>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, h } from 'vue'
import { Expand, Fold } from '@element-plus/icons-vue'

export default defineComponent({
  components: {
    Expand,
    Fold,
  },
})
</script>

<style lang="scss" scoped>
.app-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 200;
  display: flex;
  flex-direction: column;
  width: 220px;
  height: 100vh;
  background-color: #304156;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  transition: width 0.3s;

  &.collapsed {
    width: 64px;

    .sidebar-logo {
      padding: 16px 12px;
      justify-content: center;
    }

    .menu-item-content {
      justify-content: center;
      padding-right: 0;
    }
  }
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 20px;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .logo-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
    border-radius: 10px;
    color: white;
  }

  .logo-text {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .logo-title {
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    letter-spacing: 1px;
  }

  .logo-subtitle {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    letter-spacing: 2px;
  }
}

.sidebar-menu {
  flex: 1;
  overflow-x: hidden;
  overflow-y: auto;

  :deep(.el-menu) {
    border-right: none;
  }

  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    height: 50px;
    line-height: 50px;

    &:hover {
      background-color: #263445;
    }

    &.is-active {
      background-color: #409eff !important;
    }
  }
}

.menu-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-right: 16px;
  overflow: hidden;
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #bfcbd9;
  cursor: pointer;
  transition: color 0.3s;

  &:hover {
    color: #409eff;
    background-color: #263445;
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
