/**
 * Vue Router 路由配置
 */
import { createRouter, createWebHistory, createRouterMatcher, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 布局组件
import MainLayout from '@/components/MainLayout.vue'

// 视图组件
import LoginView from '@/views/Login.vue'
import HomeView from '@/views/Home.vue'
import ScheduleView from '@/views/Schedule.vue'
import ScheduleDetailView from '@/views/ScheduleDetail.vue'
import AttendanceView from '@/views/Attendance.vue'
import AttendanceRecordView from '@/views/AttendanceRecord.vue'
import NotificationsView from '@/views/Notifications.vue'
import NotificationDetailView from '@/views/NotificationDetail.vue'
import ProfileView from '@/views/Profile.vue'
import NotFoundView from '@/views/NotFound.vue'

// 路由记录
const routes: RouteRecordRaw[] = [
  // 登录页
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false, title: '登录' },
  },

  // 主布局（需要认证）
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      // 首页
      {
        path: '',
        name: 'home',
        component: HomeView,
        meta: { title: '首页', tabBar: true, icon: 'home-o' },
      },

      // 课表
      {
        path: 'schedule',
        name: 'schedule',
        component: ScheduleView,
        meta: { title: '课表', tabBar: true, icon: 'calendar-o' },
      },
      {
        path: 'schedule/:id',
        name: 'schedule-detail',
        component: ScheduleDetailView,
        meta: { title: '课表详情', back: true },
      },

      // 考勤
      {
        path: 'attendance',
        name: 'attendance',
        component: AttendanceView,
        meta: { title: '考勤', tabBar: true, icon: 'todo-list-o' },
      },
      {
        path: 'attendance/record/:scheduleId',
        name: 'attendance-record',
        component: AttendanceRecordView,
        meta: { title: '考勤记录', back: true },
      },

      // 消息通知
      {
        path: 'notifications',
        name: 'notifications',
        component: NotificationsView,
        meta: { title: '消息', tabBar: true, icon: 'bell-o' },
      },
      {
        path: 'notifications/:id',
        name: 'notification-detail',
        component: NotificationDetailView,
        meta: { title: '通知详情', back: true },
      },

      // 个人中心
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView,
        meta: { title: '个人中心', tabBar: true, icon: 'user-o' },
      },
    ],
  },

  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { title: '页面不存在' },
  },
]

// 创建路由
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  },
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} | 企业微信教务系统`
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    const authStore = useAuthStore()

    // 如果未登录，跳转到登录页
    if (!authStore.isLoggedIn) {
      // 尝试初始化认证状态
      try {
        await authStore.initAuth()
        if (!authStore.isLoggedIn) {
          next({ name: 'login', query: { redirect: to.fullPath } })
          return
        }
      } catch {
        next({ name: 'login', query: { redirect: to.fullPath } })
        return
      }
    }
  }

  next()
})

// 路由后置守卫
router.afterEach((to, from) => {
  // 可以在这里添加页面统计等操作
})

export default router
