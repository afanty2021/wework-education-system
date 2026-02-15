/**
 * Vue Router配置
 */
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 静态路由
const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
      hidden: true,
    },
  },
  {
    path: '/403',
    name: '403',
    component: () => import('@/views/error/403.vue'),
    meta: {
      title: '无权限',
      hidden: true,
    },
  },
  {
    path: '/404',
    name: '404',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面不存在',
      hidden: true,
    },
  },
  {
    path: '/500',
    name: '500',
    component: () => import('@/views/error/500.vue'),
    meta: {
      title: '服务器错误',
      hidden: true,
    },
  },
]

// 动态路由
const asyncRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/components/Layout.vue'),
    redirect: '/dashboard',
    meta: {
      title: '首页',
      icon: 'HomeFilled',
    },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {
          title: '仪表盘',
          icon: 'Odometer',
        },
      },
    ],
  },
  {
    path: '/courses',
    component: () => import('@/components/Layout.vue'),
    redirect: '/courses/index',
    meta: {
      title: '课程管理',
      icon: 'Reading',
    },
    children: [
      {
        path: 'index',
        name: 'Courses',
        component: () => import('@/views/courses/Index.vue'),
        meta: {
          title: '课程列表',
          icon: 'List',
        },
      },
      {
        path: 'form/:id?',
        name: 'CourseForm',
        component: () => import('@/views/courses/Form.vue'),
        meta: {
          title: '课程表单',
          hidden: true,
        },
      },
    ],
  },
  {
    path: '/students',
    component: () => import('@/components/Layout.vue'),
    redirect: '/students/index',
    meta: {
      title: '学员管理',
      icon: 'User',
    },
    children: [
      {
        path: 'index',
        name: 'Students',
        component: () => import('@/views/students/Index.vue'),
        meta: {
          title: '学员列表',
          icon: 'List',
        },
      },
      {
        path: 'form/:id?',
        name: 'StudentForm',
        component: () => import('@/views/students/Form.vue'),
        meta: {
          title: '学员表单',
          hidden: true,
        },
      },
    ],
  },
  {
    path: '/contracts',
    component: () => import('@/components/Layout.vue'),
    redirect: '/contracts/index',
    meta: {
      title: '合同管理',
      icon: 'Document',
    },
    children: [
      {
        path: 'index',
        name: 'Contracts',
        component: () => import('@/views/contracts/Index.vue'),
        meta: {
          title: '合同列表',
          icon: 'List',
        },
      },
      {
        path: 'form/:id?',
        name: 'ContractForm',
        component: () => import('@/views/contracts/Form.vue'),
        meta: {
          title: '合同表单',
          hidden: true,
        },
      },
    ],
  },
  {
    path: '/payments',
    component: () => import('@/components/Layout.vue'),
    redirect: '/payments/index',
    meta: {
      title: '缴费管理',
      icon: 'Money',
    },
    children: [
      {
        path: 'index',
        name: 'Payments',
        component: () => import('@/views/payments/Index.vue'),
        meta: {
          title: '缴费列表',
          icon: 'List',
        },
      },
    ],
  },
  {
    path: '/schedules',
    component: () => import('@/components/Layout.vue'),
    redirect: '/schedules/index',
    meta: {
      title: '排课管理',
      icon: 'Calendar',
    },
    children: [
      {
        path: 'index',
        name: 'Schedules',
        component: () => import('@/views/schedules/Index.vue'),
        meta: {
          title: '排课列表',
          icon: 'List',
        },
      },
      {
        path: 'form/:id?',
        name: 'ScheduleForm',
        component: () => import('@/views/schedules/Form.vue'),
        meta: {
          title: '排课表单',
          hidden: true,
        },
      },
    ],
  },
  {
    path: '/attendance',
    component: () => import('@/components/Layout.vue'),
    redirect: '/attendance/index',
    meta: {
      title: '考勤管理',
      icon: 'Clock',
    },
    children: [
      {
        path: 'index',
        name: 'Attendance',
        component: () => import('@/views/attendance/Index.vue'),
        meta: {
          title: '考勤列表',
          icon: 'List',
        },
      },
    ],
  },
  {
    path: '/notifications',
    component: () => import('@/components/Layout.vue'),
    redirect: '/notifications/index',
    meta: {
      title: '通知管理',
      icon: 'Bell',
    },
    children: [
      {
        path: 'index',
        name: 'Notifications',
        component: () => import('@/views/notifications/Index.vue'),
        meta: {
          title: '通知列表',
          icon: 'List',
        },
      },
    ],
  },
  {
    path: '/settings',
    component: () => import('@/components/Layout.vue'),
    redirect: '/settings/departments',
    meta: {
      title: '系统设置',
      icon: 'Setting',
    },
    children: [
      {
        path: 'departments',
        name: 'Departments',
        component: () => import('@/views/settings/Departments.vue'),
        meta: {
          title: '校区管理',
          icon: 'OfficeBuilding',
        },
      },
      {
        path: 'classrooms',
        name: 'Classrooms',
        component: () => import('@/views/settings/Classrooms.vue'),
        meta: {
          title: '教室管理',
          icon: 'House',
        },
      },
      {
        path: 'teachers',
        name: 'Teachers',
        component: () => import('@/views/settings/Teachers.vue'),
        meta: {
          title: '教师管理',
          icon: 'UserFilled',
        },
      },
    ],
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes: [...constantRoutes],
  scrollBehavior: () => ({
    top: 0,
    left: 0,
  }),
})

// 重置路由
function resetRouter(): void {
  const newRouter = createRouter({
    history: createWebHistory(),
    routes: constantRoutes,
  })
  ;(router as any).matcher = newRouter.match
}

// 路由白名单
const whiteList: string[] = ['/login', '/403', '/404', '/500']

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '教务管理系统'} - 教务管理系统`

  const userStore = useUserStore()

  // 判断是否登录
  if (userStore.isLoggedIn) {
    if (to.path === '/login') {
      // 已登录访问登录页，跳转到首页
      next({ path: '/' })
    } else {
      // 判断是否已获取用户信息
      if (!userStore.user) {
        try {
          await userStore.fetchUserInfo()
        } catch (error) {
          console.error('获取用户信息失败:', error)
        }
      }
      next()
    }
  } else {
    // 未登录
    if (whiteList.includes(to.path)) {
      // 白名单直接放行
      next()
    } else {
      // 跳转到登录页
      next({ path: '/login', query: { redirect: to.fullPath } })
    }
  }
})

// 路由后置守卫
router.afterEach((to) => {
  // 可以在这里做日志统计等操作
})

export { constantRoutes, asyncRoutes }
export default router
