/**
 * 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { SidebarItem } from '@/types/api'

export const useAppStore = defineStore(
  'app',
  () => {
    // 侧边栏状态
    const sidebarCollapsed = ref<boolean>(false)
    const sidebarWidth = computed(() => (sidebarCollapsed.value ? '64px' : '220px'))

    // 顶部菜单
    const topMenuIndex = ref<number>(0)

    // 主题
    const isDark = ref<boolean>(false)

    // 语言
    const locale = ref<'zh-cn' | 'en'>('zh-cn')

    // 组件大小
    const size = ref<'default' | 'small' | 'large'>('default')

    // 加载状态
    const loading = ref<boolean>(false)

    // 面包屑
    const breadcrumbs = ref<Array<{ title: string; to?: string }>>([])

    // 菜单配置
    const menuItems = ref<SidebarItem[]>([
      {
        title: '仪表盘',
        icon: 'Odometer',
        path: '/dashboard',
      },
      {
        title: '课程管理',
        icon: 'Reading',
        path: '/courses',
      },
      {
        title: '学员管理',
        icon: 'User',
        path: '/students',
      },
      {
        title: '合同管理',
        icon: 'Document',
        path: '/contracts',
      },
      {
        title: '缴费管理',
        icon: 'Money',
        path: '/payments',
      },
      {
        title: '排课管理',
        icon: 'Calendar',
        path: '/schedules',
      },
      {
        title: '考勤管理',
        icon: 'Clock',
        path: '/attendance',
      },
      {
        title: '通知管理',
        icon: 'Bell',
        path: '/notifications',
      },
      {
        title: '系统设置',
        icon: 'Setting',
        path: '/settings',
        children: [
          {
            title: '校区管理',
            path: '/settings/departments',
          },
          {
            title: '教室管理',
            path: '/settings/classrooms',
          },
          {
            title: '教师管理',
            path: '/settings/teachers',
          },
        ],
      },
    ])

    // 方法
    /**
     * 切换侧边栏
     */
    function toggleSidebar(): void {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }

    /**
     * 设置侧边栏状态
     */
    function setSidebarCollapsed(collapsed: boolean): void {
      sidebarCollapsed.value = collapsed
    }

    /**
     * 设置顶部菜单索引
     */
    function setTopMenuIndex(index: number): void {
      topMenuIndex.value = index
    }

    /**
     * 切换主题
     */
    function toggleTheme(): void {
      isDark.value = !isDark.value
      updateHtmlClass()
    }

    /**
     * 设置主题
     */
    function setTheme(dark: boolean): void {
      isDark.value = dark
      updateHtmlClass()
    }

    /**
     * 更新HTML类名
     */
    function updateHtmlClass(): void {
      if (isDark.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    /**
     * 设置语言
     */
    function setLocale(lang: 'zh-cn' | 'en'): void {
      locale.value = lang
    }

    /**
     * 设置组件大小
     */
    function setSize(s: 'default' | 'small' | 'large'): void {
      size.value = s
    }

    /**
     * 设置加载状态
     */
    function setLoading(loadingState: boolean): void {
      loading.value = loadingState
    }

    /**
     * 设置面包屑
     */
    function setBreadcrumbs(items: Array<{ title: string; to?: string }>): void {
      breadcrumbs.value = items
    }

    /**
     * 添加面包屑
     */
    function addBreadcrumb(item: { title: string; to?: string }): void {
      breadcrumbs.value.push(item)
    }

    /**
     * 清空面包屑
     */
    function clearBreadcrumbs(): void {
      breadcrumbs.value = []
    }

    /**
     * 初始化主题
     */
    function initTheme(): void {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        isDark.value = savedTheme === 'dark'
      } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        isDark.value = true
      }
      updateHtmlClass()
    }

    return {
      // 状态
      sidebarCollapsed,
      sidebarWidth,
      topMenuIndex,
      isDark,
      locale,
      size,
      loading,
      breadcrumbs,
      menuItems,
      // 计算属性
      sidebarWidth,
      // 方法
      toggleSidebar,
      setSidebarCollapsed,
      setTopMenuIndex,
      toggleTheme,
      setTheme,
      setLocale,
      setSize,
      setLoading,
      setBreadcrumbs,
      addBreadcrumb,
      clearBreadcrumbs,
      initTheme,
    }
  },
  {
    persist: {
      key: 'app',
      paths: ['sidebarCollapsed', 'isDark', 'locale', 'size'],
    },
  }
)
