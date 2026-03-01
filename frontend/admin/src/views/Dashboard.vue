<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElCard, ElRow, ElCol, ElButton, ElTag, ElProgress, ElIcon } from 'element-plus'
import {
  User,
  Document,
  Money,
  Clock,
  TrendCharts,
  ArrowRight,
  Bell,
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 统计数据
const stats = ref({
  studentCount: 156,
  contractCount: 89,
  todayPayment: 12800,
  weekSchedules: 24,
})

// 今日待办
const todos = ref([
  { id: 1, title: '张三的合同即将到期', type: 'contract', urgent: true },
  { id: 2, title: '李四的课程需要排课', type: 'schedule', urgent: false },
  { id: 3, title: '王五的缴费需要确认', type: 'payment', urgent: true },
  { id: 4, title: '今日考勤数据待录入', type: 'attendance', urgent: false },
])

// 最近活动
const recentActivities = ref([
  { id: 1, user: '张三', action: '创建合同', time: '10分钟前', type: 'contract' },
  { id: 2, user: '李四', action: '完成缴费', time: '30分钟前', type: 'payment' },
  { id: 3, user: '王五', action: '报名课程', time: '1小时前', type: 'student' },
  { id: 4, user: '赵六', action: '预约试听', time: '2小时前', type: 'schedule' },
  { id: 5, user: '钱七', action: '提交作业', time: '3小时前', type: 'homework' },
])

// 快捷入口
const quickActions = [
  { title: '添加学员', icon: 'User', path: '/students/form', color: '#409eff' },
  { title: '创建合同', icon: 'Document', path: '/contracts/form', color: '#67c23a' },
  { title: '录入缴费', icon: 'Money', path: '/payments', color: '#e6a23c' },
  { title: '排课管理', icon: 'Calendar', path: '/schedules', color: '#909399' },
]

// 用户名称
const userName = computed(() => userStore.userName || '管理员')

// 跳转到详情
function goToDetail(type: string, id?: number): void {
  const routes: Record<string, string> = {
    contract: '/contracts',
    schedule: '/schedules',
    payment: '/payments',
    attendance: '/attendance',
    student: '/students',
  }
  router.push(routes[type] || '/')
}

// 跳转到快捷入口
function goToQuickAction(path: string): void {
  router.push(path)
}

// 格式化时间
function formatTime(time: string): string {
  return time
}
</script>

<template>
  <div class="dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">
          早上好，{{ userName }}
        </h1>
        <p class="welcome-subtitle">
          今天是 {{ new Date().toLocaleDateString('zh-CN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
        </p>
      </div>
      <div class="welcome-actions">
        <el-button type="primary" @click="goToQuickAction('/courses/form')">
          新建课程
        </el-button>
        <el-button @click="goToQuickAction('/schedules/form')">
          快速排课
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon student">
              <el-icon :size="32">
                <User />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.studentCount }}</div>
              <div class="stat-label">学员总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><TrendCharts /></el-icon>
              12%
            </span>
            <span class="stat-text">较上周</span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon contract">
              <el-icon :size="32">
                <Document />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.contractCount }}</div>
              <div class="stat-label">活跃合同</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><TrendCharts /></el-icon>
              8%
            </span>
            <span class="stat-text">较上周</span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon payment">
              <el-icon :size="32">
                <Money />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">¥{{ stats.todayPayment.toLocaleString() }}</div>
              <div class="stat-label">今日收款</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend down">
              <el-icon><TrendCharts /></el-icon>
              5%
            </span>
            <span class="stat-text">较昨日</span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon schedule">
              <el-icon :size="32">
                <Clock />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.weekSchedules }}</div>
              <div class="stat-label">本周排课</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><TrendCharts /></el-icon>
              15%
            </span>
            <span class="stat-text">较上周</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 主要内容区 -->
    <el-row :gutter="20">
      <!-- 左侧：待办和活动 -->
      <el-col :xs="24" :lg="16">
        <!-- 今日待办 -->
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><Bell /></el-icon>
                今日待办
              </span>
              <el-button text type="primary" size="small" @click="goToDetail('all')">
                查看全部
                <el-icon class="arrow-icon"><ArrowRight /></el-icon>
              </el-button>
            </div>
          </template>

          <div class="todo-list">
            <div
              v-for="todo in todos"
              :key="todo.id"
              class="todo-item"
              :class="{ urgent: todo.urgent }"
              @click="goToDetail(todo.type)"
            >
              <div class="todo-indicator" :class="{ urgent: todo.urgent }" />
              <div class="todo-content">
                <div class="todo-title">{{ todo.title }}</div>
                <div class="todo-meta">
                  <el-tag v-if="todo.urgent" type="danger" size="small">紧急</el-tag>
                  <span class="todo-type">{{ todo.type }}</span>
                </div>
              </div>
              <el-icon class="todo-arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>

        <!-- 最近活动 -->
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><Clock /></el-icon>
                最近活动
              </span>
            </div>
          </template>

          <div class="activity-list">
            <div
              v-for="activity in recentActivities"
              :key="activity.id"
              class="activity-item"
            >
              <div class="activity-avatar">
                {{ activity.user.charAt(0) }}
              </div>
              <div class="activity-content">
                <div class="activity-text">
                  <span class="activity-user">{{ activity.user }}</span>
                  {{ activity.action }}
                </div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：快捷入口和进度 -->
      <el-col :xs="24" :lg="8">
        <!-- 快捷入口 -->
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">快捷入口</span>
            </div>
          </template>

          <div class="quick-actions">
            <div
              v-for="(action, index) in quickActions"
              :key="index"
              class="quick-action"
              @click="goToQuickAction(action.path)"
            >
              <div class="quick-icon" :style="{ backgroundColor: action.color }">
                <el-icon :size="24">
                  <component :is="action.icon" />
                </el-icon>
              </div>
              <div class="quick-title">{{ action.title }}</div>
            </div>
          </div>
        </el-card>

        <!-- 课时消耗进度 -->
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">课时消耗情况</span>
            </div>
          </template>

          <div class="progress-list">
            <div class="progress-item">
              <div class="progress-label">
                <span>Python入门班</span>
                <span class="progress-value">75%</span>
              </div>
              <el-progress :percentage="75" :stroke-width="8" color="#67c23a" />
            </div>

            <div class="progress-item">
              <div class="progress-label">
                <span>Java进阶班</span>
                <span class="progress-value">45%</span>
              </div>
              <el-progress :percentage="45" :stroke-width="8" color="#409eff" />
            </div>

            <div class="progress-item">
              <div class="progress-label">
                <span>Web前端班</span>
                <span class="progress-value">90%</span>
              </div>
              <el-progress :percentage="90" :stroke-width="8" color="#e6a23c" />
            </div>

            <div class="progress-item">
              <div class="progress-label">
                <span>数据结构班</span>
                <span class="progress-value">30%</span>
              </div>
              <el-progress :percentage="30" :stroke-width="8" color="#909399" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.dashboard {
  padding: 0;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #fff;

  .welcome-title {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .welcome-subtitle {
    font-size: 14px;
    opacity: 0.9;
  }

  .welcome-actions {
    display: flex;
    gap: 12px;

    :deep(.el-button) {
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.5);
      color: #fff;

      &:hover {
        background: rgba(255, 255, 255, 0.3);
      }
    }
  }
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  :deep(.el-card__body) {
    padding: 20px;
  }

  .stat-content {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
  }

  .stat-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 12px;

    &.student {
      background: rgba(64, 158, 255, 0.1);
      color: #409eff;
    }

    &.contract {
      background: rgba(103, 194, 58, 0.1);
      color: #67c23a;
    }

    &.payment {
      background: rgba(230, 162, 60, 0.1);
      color: #e6a23c;
    }

    &.schedule {
      background: rgba(144, 147, 153, 0.1);
      color: #909399;
    }
  }

  .stat-info {
    .stat-value {
      font-size: 28px;
      font-weight: 600;
      color: #303133;
    }

    .stat-label {
      font-size: 14px;
      color: #909399;
      margin-top: 4px;
    }
  }

  .stat-footer {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #909399;
  }

  .stat-trend {
    display: flex;
    align-items: center;
    gap: 4px;

    &.up {
      color: #67c23a;
    }

    &.down {
      color: #f56c6c;
    }
  }
}

.section-card {
  margin-bottom: 20px;

  :deep(.el-card__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--el-border-color-lighter);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #303133;

    .arrow-icon {
      margin-left: 4px;
    }
  }
}

.todo-list {
  .todo-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: #f5f7fa;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      background: #ecf5ff;

      .todo-arrow {
        opacity: 1;
      }
    }

    &:last-child {
      margin-bottom: 0;
    }

    &.urgent {
      background: #fef0f0;

      &:hover {
        background: #fde2e2;
      }
    }
  }

  .todo-indicator {
    width: 4px;
    height: 24px;
    background: #e4e7ed;
    border-radius: 2px;

    &.urgent {
      background: #f56c6c;
    }
  }

  .todo-content {
    flex: 1;
  }

  .todo-title {
    font-size: 14px;
    color: #303133;
    margin-bottom: 4px;
  }

  .todo-meta {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .todo-type {
    font-size: 12px;
    color: #909399;
    text-transform: capitalize;
  }

  .todo-arrow {
    color: #909399;
    opacity: 0;
    transition: opacity 0.3s;
  }
}

.activity-list {
  .activity-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid #f0f2f5;

    &:last-child {
      border-bottom: none;
    }
  }

  .activity-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    font-size: 14px;
    font-weight: 600;
    color: #fff;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
  }

  .activity-content {
    flex: 1;
  }

  .activity-text {
    font-size: 14px;
    color: #303133;
    margin-bottom: 4px;

    .activity-user {
      font-weight: 600;
      color: #409eff;
      margin-right: 4px;
    }
  }

  .activity-time {
    font-size: 12px;
    color: #909399;
  }
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;

  .quick-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 20px 16px;
    background: #f5f7fa;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      background: #ecf5ff;
      transform: translateY(-2px);
    }
  }

  .quick-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    color: #fff;
  }

  .quick-title {
    font-size: 13px;
    font-weight: 500;
    color: #303133;
  }
}

.progress-list {
  .progress-item {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 13px;
    color: #606266;

    .progress-value {
      font-weight: 600;
      color: #303133;
    }
  }
}

// 响应式
@media (max-width: 768px) {
  .welcome-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;

    .welcome-title {
      font-size: 24px;
    }
  }

  .stat-card {
    margin-bottom: 16px;
  }

  .quick-actions {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
