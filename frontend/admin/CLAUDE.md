[根目录](../../../CLAUDE.md) > [frontend](../) > **admin**

# Frontend Admin - 管理后台前端

> 最后更新：2026-02-16

## 模块职责

`frontend/admin` 是基于 Vue 3 + Element Plus 的管理后台前端应用。

## 技术栈

- Vue 3.4.21
- Element Plus 2.12+
- Vite 5+
- TypeScript
- Pinia 状态管理

## 目录结构

```
admin/
├── src/
│   ├── api/              # API 请求
│   │   ├── request.ts   # axios 封装
│   │   ├── auth.ts      # 认证 API
│   │   ├── students.ts  # 学员 API
│   │   ├── courses.ts  # 课程 API
│   │   ├── contracts.ts # 合同 API
│   │   ├── payments.ts # 支付 API
│   │   ├── schedules.ts # 排课 API
│   │   ├── attendance.ts # 考勤 API
│   │   └── notifications.ts # 通知 API
│   ├── stores/          # Pinia 状态管理
│   │   ├── app.ts      # 应用状态
│   │   └── user.ts     # 用户状态
│   ├── types/           # TypeScript 类型
│   ├── router/          # Vue Router
│   ├── views/           # 页面组件
│   ├── App.vue
│   └── main.ts
└── package.json
```

## 启动开发服务器

```bash
cd frontend/admin
npm run dev
# 访问地址: http://localhost:3000
```

## 变更记录

### 2026-02-16

| ID | 时间 | 类型 | 标题 | 阅读量 |
|----|------|------|------|--------|
| #4215 | 12:30 | 🔴 | 修复多个 Vue 组件语法错误和代码重复 | ~145 |
| #4214 | 12:26 | 🔴 | 修复多个 Vue 组件语法错误和代码重复 | ~131 |
| #4211 | 12:23 | 🔄 | 清理 TableSearch.vue 重复的 script 块 | ~38 |
| #4209 | 12:22 | 🔄 | 重构 FormDialog.vue 从 Options API 转为 Composition API | ~82 |
| #4208 | 12:21 | 🔄 | 移除 Sidebar.vue 未使用的 JSX renderMenu 函数 | ~169 |
| #4207 | 12:19 | 🔄 | 重构 Dashboard.vue 使用 Vue 3 Composition API | ~85 |
| #4206 | " | 🔄 | 重构 Dashboard.vue 使用单一 script setup 块 | ~74 |
| #4202 | 12:18 | 🔴 | 修复 Dashboard.vue Vue 3 组件结构 | ~160 |

### 2026-02-14

| ID | 时间 | 类型 | 标题 | 阅读量 |
|----|------|------|------|--------|
| #3867 | 18:03 | 🔵 | 前端 admin 目录结构存在但文件为空 | ~180 |
</claude-mem-context>