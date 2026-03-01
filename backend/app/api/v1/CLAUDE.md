[根目录](../../../CLAUDE.md) > [backend](../../) > [app/api](../) > **v1**

# API v1 - REST API 路由

> 最后更新：2026-02-16

## 模块职责

`backend/app/api/v1` 包含所有 REST API 路由，提供 HTTP 接口给前端和小程序使用。

## 目录结构

```
v1/
├── __init__.py           # 路由导出
├── auth.py               # 认证路由
├── students.py          # 学员管理
├── courses.py           # 课程管理
├── contracts.py         # 合同管理
├── payments.py          # 支付管理
├── schedules.py         # 排课管理
├── attendance.py         # 考勤管理
├── homeworks.py         # 作业管理
├── notifications.py      # 通知管理
├── tasks.py             # 任务管理
└── payment/
    ├── __init__.py
    ├── wechat.py        # 微信支付
    └── alipay.py        # 支付宝
```

## API 路由清单

### 认证 (Auth)
- `POST /api/v1/auth/wework` - 企业微信登录
- `GET /api/v1/auth/me` - 获取当前用户
- `POST /api/v1/auth/refresh` - 刷新 Token

### 学员管理 (Students)
- `GET /api/v1/students/` - 获取学员列表
- `POST /api/v1/students/` - 创建学员
- `GET /api/v1/students/{id}` - 获取学员详情
- `PUT /api/v1/students/{id}` - 更新学员
- `DELETE /api/v1/students/{id}` - 删除学员
- `POST /api/v1/students/{id}/tags` - 添加标签
- `DELETE /api/v1/students/{id}/tags/{tag}` - 删除标签
- `GET /api/v1/students/tags/all` - 获取所有标签

### 课程管理 (Courses)
- `GET /api/v1/courses/` - 获取课程列表
- `POST /api/v1/courses/` - 创建课程
- `GET /api/v1/courses/{id}` - 获取课程详情
- `PUT /api/v1/courses/{id}` - 更新课程
- `DELETE /api/v1/courses/{id}` - 删除课程
- `GET /api/v1/courses/classrooms` - 获取教室列表
- `POST /api/v1/courses/classrooms` - 创建教室
- `GET /api/v1/courses/departments` - 获取部门列表

### 合同管理 (Contracts)
- `GET /api/v1/contracts/` - 获取合同列表
- `POST /api/v1/contracts/` - 创建合同
- `GET /api/v1/contracts/{id}` - 获取合同详情
- `GET /api/v1/contracts/no/{contract_no}` - 根据合同号查询
- `PUT /api/v1/contracts/{id}` - 更新合同
- `DELETE /api/v1/contracts/{id}` - 删除合同
- `POST /api/v1/contracts/{id}/deduct` - 扣减课时
- `POST /api/v1/contracts/{id}/add-hours` - 添加课时
- `POST /api/v1/contracts/{id}/expire` - 合同到期
- `GET /api/v1/contracts/expiring` - 获取即将到期合同

### 支付管理 (Payments)
- `GET /api/v1/payments/` - 获取支付列表
- `POST /api/v1/payments/` - 创建支付
- `GET /api/v1/payments/{id}` - 获取支付详情
- `GET /api/v1/payments/no/{payment_no}` - 根据支付号查询
- `PUT /api/v1/payments/{id}` - 更新支付
- `DELETE /api/v1/payments/{id}` - 删除支付
- `POST /api/v1/payments/{id}/confirm` - 确认支付
- `POST /api/v1/payments/{id}/refund` - 退款

### 微信支付 (WeChat Pay)
- `POST /api/v1/payment/wechat/create` - 创建微信支付订单
- `POST /api/v1/payment/wechat/notify` - 微信支付回调
- `GET /api/v1/payment/wechat/orders/{order_no}` - 查询订单
- `POST /api/v1/payment/wechat/refund` - 申请退款

### 支付宝 (Alipay)
- `POST /api/v1/payment/alipay/create` - 创建支付宝订单
- `POST /api/v1/payment/alipay/notify` - 支付宝回调
- `GET /api/v1/payment/alipay/orders/{order_no}` - 查询订单

### 排课管理 (Schedules)
- `GET /api/v1/schedules/` - 获取排课列表
- `POST /api/v1/schedules/` - 创建排课
- `GET /api/v1/schedules/{id}` - 获取排课详情
- `PUT /api/v1/schedules/{id}` - 更新排课
- `DELETE /api/v1/schedules/{id}` - 删除排课
- `POST /api/v1/schedules/{id}/enroll` - 学员报名
- `POST /api/v1/schedules/{id}/cancel-enrollment` - 取消报名

### 考勤管理 (Attendance)
- `GET /api/v1/attendance/` - 获取考勤列表
- `POST /api/v1/attendance/` - 创建考勤记录
- `GET /api/v1/attendance/{id}` - 获取考勤详情
- `PUT /api/v1/attendance/{id}` - 更新考勤
- `DELETE /api/v1/attendance/{id}` - 删除考勤
- `GET /api/v1/attendance/statistics/student/{id}` - 学员考勤统计

### 作业管理 (Homeworks)
- `GET /api/v1/homeworks/` - 获取作业列表
- `POST /api/v1/homeworks/` - 发布作业
- `GET /api/v1/homeworks/{id}` - 获取作业详情
- `PUT /api/v1/homeworks/{id}` - 更新作业
- `DELETE /api/v1/homeworks/{id}` - 删除作业
- `POST /api/v1/homeworks/{id}/submit` - 提交作业

### 通知管理 (Notifications)
- `GET /api/v1/notifications/` - 获取通知列表
- `POST /api/v1/notifications/` - 发送通知
- `POST /api/v1/notifications/batch` - 批量发送
- `GET /api/v1/notifications/{id}` - 获取通知详情
- `PUT /api/v1/notifications/{id}` - 更新通知
- `DELETE /api/v1/notifications/{id}` - 删除通知

### 任务管理 (Tasks)
- `GET /api/v1/tasks/` - 获取任务列表
- `GET /api/v1/tasks/{id}` - 获取任务详情
- `POST /api/v1/tasks/{id}/pause` - 暂停任务
- `POST /api/v1/tasks/{id}/resume` - 恢复任务
- `POST /api/v1/tasks/{id}/trigger` - 触发任务
- `GET /api/v1/tasks/{id}/logs` - 查看任务日志

## 访问地址

- API 文档: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 变更记录

### 2026-02-16 - 环境搭建同步

- 添加 API 路由清单
- 更新访问地址

### 2026-02-14 - 模块初始化

- 创建所有 API 路由

---
