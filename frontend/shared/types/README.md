# 前端共享类型使用指南

本目录包含企业微信教育系统的共享类型定义，供 `admin` 和 `h5` 项目共用。

## 使用方式

### 1. 配置路径别名

在项目的 `tsconfig.json` 中添加路径映射：

```json
{
  "compilerOptions": {
    "paths": {
      "@shared/*": ["../../shared/*"]
    }
  }
}
```

### 2. 使用共享类型

```typescript
// 在 admin 或 h5 项目中
import type { Student, StudentStatus, Course } from '@shared/types'

// 使用类型
const student: Student = {
  id: 1,
  name: '张三',
  status: StudentStatus.ACTIVE,
}
```

### 3. API 模块类型扩展

在各自的 API 文件中，可以从共享类型扩展：

```typescript
// 例如在 api/students.ts 中
import type { Student, StudentStatus } from '@shared/types'

// 扩展特定业务的参数
export interface StudentCreateParams extends Omit<Student, 'id' | 'created_at' | 'updated_at'> {
  // 添加创建时的特定字段
}
```

## 类型覆盖范围

| 模块 | 状态 | 说明 |
|------|------|------|
| 通用类型 | ✅ | PageParams, ApiResponse, CRUDResponse |
| 用户与认证 | ✅ | User, LoginParams, LoginResponse |
| 学员管理 | ✅ | Student, StudentStatus |
| 课程管理 | ✅ | Course, CourseStatus |
| 合同管理 | ✅ | Contract, ContractStatus |
| 支付管理 | ✅ | Payment, PaymentStatus |
| 考勤管理 | ✅ | Attendance, AttendanceStatus |
| 排课管理 | ✅ | Schedule, ScheduleStatus |
| 作业管理 | ✅ | Homework, HomeworkSubmission |
| 通知管理 | ✅ | Notification, NotificationType |

## 同步策略

当后端 API 变更时，需要同步更新本目录中的类型定义：
1. 修改 `shared/types/index.ts` 中的对应类型
2. 提交更新
3. 在 admin/h5 项目中重新导入使用
