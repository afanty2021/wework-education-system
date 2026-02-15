<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
import { ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus'
import {
  Bell,
  User,
  SwitchButton,
  Setting,
  Moon,
  Sunny,
} from '@element-plus/icons-vue'
import SvgIcon from '@/components/SvgIcon.vue'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()

// 是否有未读消息
const hasUnread = ref(false)

// 用户头像
const userAvatar = computed(() => userStore.userAvatar)

// 用户名称
const userName = computed(() => userStore.userName)

// 是否深色模式
const isDark = computed(() => appStore.isDark)

// 顶部菜单
const topMenuItems = [
  { title: '首页', path: '/dashboard' },
  { title: '课程', path: '/courses' },
  { title: '学员', path: '/students' },
  { title: '排课', path: '/schedules' },
]

// 切换主题
function handleToggleTheme(): void {
  appStore.toggleTheme()
}

// 跳转到个人设置
function goToSettings(): void {
  router.push('/settings/profile')
}

// 退出登录
async function handleLogout(): Promise<void> {
  await userStore.logout()
}

// 去往消息中心
function goToNotifications(): void {
  router.push('/notifications')
}
</script>

<template>
  <div class="app-header">
    <!-- 左侧：面包屑和搜索 -->
    <div class="header-left">
      <!-- 面包屑 -->
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="route.meta.title">
          {{ route.meta.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 右侧：功能按钮 -->
    <div class="header-right">
      <!-- 搜索框 -->
      <div class="header-search">
        <el-input
          placeholder="搜索..."
          prefix-icon="Search"
          size="small"
          clearable
          class="search-input"
        />
      </div>

      <!-- 消息通知 -->
      <div class="header-icon" @click="goToNotifications">
        <el-badge :value="hasUnread ? '' : 0" :hidden="!hasUnread" :max="99">
          <el-icon :size="20">
            <Bell />
          </el-icon>
        </el-badge>
      </div>

      <!-- 主题切换 -->
      <div class="header-icon" @click="handleToggleTheme">
        <el-icon :size="20">
          <component :is="isDark ? 'Sunny' : 'Moon'" />
        </el-icon>
      </div>

      <!-- 用户下拉菜单 -->
      <el-dropdown trigger="click" @command="handleLogout">
        <div class="user-info">
          <el-avatar :size="32" :src="userAvatar">
            {{ userName.charAt(0) }}
          </el-avatar>
          <span class="user-name">{{ userName }}</span>
          <el-icon class="dropdown-icon">
            <ArrowDown />
          </el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile" :icon="User" @click="goToSettings">
              个人设置
            </el-dropdown-item>
            <el-dropdown-item command="settings" :icon="Setting">
              系统设置
            </el-dropdown-item>
            <el-dropdown-item command="logout" :icon="SwitchButton" divided>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, h } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'

export default defineComponent({
  components: {
    ArrowDown,
  },
})
</script>

<style lang="scss" scoped>
.app-header {
  position: fixed;
  top: 0;
  right: 0;
  left: 220px;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color);
  box-shadow: var(--el-box-shadow-light);
  transition: left 0.3s;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-search {
  width: 240px;

  .search-input {
    :deep(.el-input__wrapper) {
      border-radius: 20px;
      background-color: var(--el-fill-color-light);
      box-shadow: none;
    }
  }
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--el-fill-color-light);
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--el-fill-color-light);
  }

  .user-name {
    max-width: 100px;
    overflow: hidden;
    font-size: 14px;
    color: var(--el-text-color-primary);
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .dropdown-icon {
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}

// 深色模式下的侧边栏调整
:global(.dark) {
  .app-header {
    left: 220px;
  }
}

// 侧边栏收起时的样式
:global(.sidebar-collapsed) {
  .app-header {
    left: 64px;
  }
}
</style>
