# API设计规范

## 1. 总则

### 1.1 设计原则

- **RESTful风格**: 遵循REST架构风格，使用标准HTTP方法
- **统一响应**: 所有API返回统一的响应格式
- **版本控制**: API版本通过URL路径控制
- **安全优先**: 所有API必须经过认证和授权
- **幂等性**: GET、PUT、DELETE操作保证幂等

### 1.2 基础URL结构

```
https://api.edu.example.com/v1/{module}/{resource}
```

示例：
- GET /v1/members - 获取会员列表
- POST /v1/members - 创建会员
- GET /v1/members/{id} - 获取会员详情
- PUT /v1/members/{id} - 更新会员信息

## 2. HTTP状态码

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功，无返回内容 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突 |
| 422 | Unprocessable Entity | 业务逻辑错误 |
| 500 | Internal Server Error | 服务器内部错误 |

## 3. 统一响应格式

### 3.1 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 具体数据
  },
  "timestamp": 1703123456789,
  "traceId": "abc123def456"
}
```

### 3.2 分页响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      // 数据列表
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5
    }
  },
  "timestamp": 1703123456789
}
```

### 3.3 错误响应

```json
{
  "code": 400,
  "message": "参数验证失败",
  "error": {
    "type": "VALIDATION_ERROR",
    "details": [
      {
        "field": "mobile",
        "message": "手机号格式不正确"
      }
    ]
  },
  "timestamp": 1703123456789,
  "traceId": "abc123def456"
}
```

## 4. 认证授权

### 4.1 认证方式

使用JWT Token进行认证：

```http
Authorization: Bearer <JWT_TOKEN>
```

### 4.2 Token格式

```json
{
  "sub": "user_id",
  "username": "john_doe",
  "roles": ["admin", "teacher"],
  "exp": 1703123456,
  "iat": 1703123456
}
```

### 4.3 刷新Token

```http
POST /v1/auth/refresh
Content-Type: application/json

{
  "refreshToken": "refresh_token_here"
}
```

## 5. API文档

### 5.1 会员管理API

#### 5.1.1 创建会员

```http
POST /v1/members
Content-Type: application/json
Authorization: Bearer <token>

{
  "realName": "张三",
  "mobile": "13800138000",
  "gender": 1,
  "birthday": "2000-01-01",
  "sourceType": 1
}
```

**响应**:
```json
{
  "code": 201,
  "message": "创建成功",
  "data": {
    "memberId": "uuid-string",
    "memberNo": "M20240101001",
    "realName": "张三",
    "mobile": "13800138000",
    "status": 1,
    "createdAt": "2024-01-01T10:00:00Z"
  }
}
```

#### 5.1.2 查询会员列表

```http
GET /v1/members?page=1&size=20&keyword=张三&status=1
Authorization: Bearer <token>
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | Integer | 否 | 页码，默认1 |
| size | Integer | 否 | 每页大小，默认20 |
| keyword | String | 否 | 搜索关键词 |
| status | Integer | 否 | 会员状态 |
| level | Integer | 否 | 会员等级 |

#### 5.1.3 更新会员信息

```http
PUT /v1/members/{memberId}
Content-Type: application/json
Authorization: Bearer <token>

{
  "realName": "张三丰",
  "gender": 1,
  "birthday": "2000-01-01",
  "address": "北京市朝阳区"
}
```

### 5.2 课程管理API

#### 5.2.1 创建课程

```http
POST /v1/courses
Content-Type: application/json
Authorization: Bearer <token>

{
  "courseName": "Python编程入门",
  "courseCode": "PY001",
  "courseTypeId": "uuid-of-type",
  "duration": 120,
  "maxStudents": 30,
  "price": 1999.00,
  "description": "从零开始学习Python编程"
}
```

#### 5.2.2 课程排课

```http
POST /v1/courses/{courseId}/schedules
Content-Type: application/json
Authorization: Bearer <token>

{
  "teacherId": "teacher-uuid",
  "classroomId": "classroom-uuid",
  "startTime": "2024-01-15T10:00:00Z",
  "endTime": "2024-01-15T12:00:00Z",
  "weekDay": 1
}
```

### 5.3 订单管理API

#### 5.3.1 创建订单

```http
POST /v1/orders
Content-Type: application/json
Authorization: Bearer <token>

{
  "memberId": "member-uuid",
  "orderType": 2,
  "items": [
    {
      "productId": "card-type-uuid",
      "productType": "card",
      "quantity": 1
    }
  ]
}
```

#### 5.3.2 订单支付

```http
POST /v1/orders/{orderId}/pay
Content-Type: application/json
Authorization: Bearer <token>

{
  "paymentMethod": 1,
  "channel": "wechat"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "发起支付成功",
  "data": {
    "paymentNo": "PAY20240101001",
    "qrCode": "data:image/png;base64,...",
    "expireTime": "2024-01-01T10:30:00Z"
  }
}
```

### 5.4 考勤管理API

#### 5.4.1 签到

```http
POST /v1/attendance/checkin
Content-Type: application/json
Authorization: Bearer <token>

{
  "memberId": "member-uuid",
  "scheduleId": "schedule-uuid",
  "checkinType": 1
}
```

#### 5.4.2 请假

```http
POST /v1/attendance/leave
Content-Type: application/json
Authorization: Bearer <token>

{
  "memberId": "member-uuid",
  "scheduleId": "schedule-uuid",
  "leaveType": 1,
  "reason": "身体不适",
  "startTime": "2024-01-15T10:00:00Z",
  "endTime": "2024-01-15T12:00:00Z"
}
```

## 6. 批量操作API

### 6.1 批量导入会员

```http
POST /v1/members/batch-import
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: members.xlsx
```

**响应**:
```json
{
  "code": 200,
  "message": "导入完成",
  "data": {
    "taskId": "task-uuid",
    "totalCount": 100,
    "successCount": 95,
    "failCount": 5,
    "fails": [
      {
        "row": 3,
        "reason": "手机号已存在"
      }
    ]
  }
}
```

### 6.2 批量发送通知

```http
POST /v1/notifications/batch
Content-Type: application/json
Authorization: Bearer <token>

{
  "memberIds": ["uuid1", "uuid2"],
  "title": "课程提醒",
  "content": "您有一节课即将开始",
  "type": 1,
  "channels": ["sms", "app"]
}
```

## 7. 文件上传API

### 7.1 获取上传凭证

```http
POST /v1/files/upload-token
Content-Type: application/json
Authorization: Bearer <token>

{
  "fileType": "image",
  "purpose": "avatar"
}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "uploadUrl": "https://oss.example.com/upload",
    "token": "upload-token",
    "key": "avatar/2024/01/01/uuid.jpg",
    "expireTime": 1703123456
  }
}
```

### 7.2 确认上传

```http
POST /v1/files/confirm
Content-Type: application/json
Authorization: Bearer <token>

{
  "key": "avatar/2024/01/01/uuid.jpg",
  "fileName": "avatar.jpg",
  "fileSize": 102400
}
```

## 8. 统计报表API

### 8.1 会员统计

```http
GET /v1/reports/members/statistics?startDate=2024-01-01&endDate=2024-01-31
Authorization: Bearer <token>
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "totalMembers": 1000,
    "newMembers": 50,
    "activeMembers": 800,
    "trend": [
      {
        "date": "2024-01-01",
        "count": 20
      }
    ]
  }
}
```

### 8.2 营收统计

```http
GET /v1/reports/revenue?startDate=2024-01-01&endDate=2024-01-31&groupBy=day
Authorization: Bearer <token>
```

## 9. WebSocket实时通信

### 9.1 连接建立

```javascript
const ws = new WebSocket('wss://api.edu.example.com/v1/ws');

// 认证
ws.send(JSON.stringify({
  type: 'auth',
  token: 'jwt-token'
}));
```

### 9.2 消息格式

```json
{
  "type": "notification",
  "data": {
    "id": "msg-uuid",
    "title": "系统通知",
    "content": "您有新的课程安排",
    "timestamp": 1703123456789
  }
}
```

## 10. API限流

### 10.1 限流规则

| 接口类型 | 限制 | 时间窗口 |
|---------|------|----------|
| 登录 | 5次/IP | 1分钟 |
| 短信验证码 | 1次/手机号 | 1分钟 |
| 一般接口 | 100次/用户 | 1分钟 |
| 上传接口 | 10次/用户 | 1分钟 |

### 10.2 限流响应

```json
{
  "code": 429,
  "message": "请求过于频繁",
  "error": {
    "type": "RATE_LIMIT_EXCEEDED",
    "retryAfter": 60
  }
}
```

## 11. 错误码定义

| 错误码 | 说明 |
|--------|------|
| 10001 | 参数错误 |
| 10002 | 资源不存在 |
| 10003 | 权限不足 |
| 10004 | 业务逻辑错误 |
| 20001 | 用户未登录 |
| 20002 | Token已过期 |
| 20003 | Token无效 |
| 30001 | 会员已存在 |
| 30002 | 会员卡余额不足 |
| 40001 | 订单已支付 |
| 40002 | 订单已取消 |

## 12. 最佳实践

### 12.1 请求优化

1. **使用分页**: 避免一次性返回大量数据
2. **字段选择**: 允许客户端指定需要的字段
3. **批量操作**: 提供批量接口减少请求次数
4. **缓存策略**: 合理设置缓存头

### 12.2 安全建议

1. **HTTPS**: 所有API必须使用HTTPS
2. **输入验证**: 严格校验所有输入参数
3. **SQL注入**: 使用参数化查询
4. **敏感数据**: 不在响应中返回密码等敏感信息

### 12.3 性能优化

1. **异步处理**: 耗时操作异步执行
2. **压缩响应**: 启用Gzip压缩
3. **CDN加速**: 静态资源使用CDN
4. **数据库优化**: 合理使用索引和查询优化

## 13. API测试

### 13.1 Postman集合

提供完整的Postman测试集合，包含所有API的示例请求。

### 13.2 自动化测试

```javascript
// Jest API测试示例
describe('Member API', () => {
  test('should create member', async () => {
    const response = await request(app)
      .post('/v1/members')
      .set('Authorization', `Bearer ${token}`)
      .send({
        realName: '测试用户',
        mobile: '13800138001'
      });

    expect(response.status).toBe(201);
    expect(response.body.code).toBe(201);
  });
});
```

## 14. 版本管理

### 14.1 版本策略

- 主版本：不兼容的API修改
- 次版本：向后兼容的功能性新增
- 修订版本：向后兼容的问题修正

### 14.2 版本兼容

- 新版本至少兼容旧版本6个月
- 废弃API提前3个月通知
- 提供迁移指南和工具

这份API设计规范确保了系统接口的一致性、安全性和可维护性，为前后端协作提供了清晰的指导。