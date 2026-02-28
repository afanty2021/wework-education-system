# API 类型同步约定

本文档约定前后端 API 类型的同步方式，确保类型一致性。

## 原则

1. **单一职责**：后端定义 Schema，前端引用或扩展
2. **版本同步**：API 变更时同步更新类型定义
3. **类型优先**：后端优先使用 TypeScript 友好类型

## 同步流程

```
后端修改 Schema → 更新 docs/api-types.md → 前端同步更新 shared/types
```

## API 命名规范

### URL 规范

| 方法 | URL | 说明 |
|------|-----|------|
| GET | /api/v1/{resource} | 获取列表 |
| GET | /api/v1/{resource}/{id} | 获取单个 |
| POST | /api/v1/{resource} | 创建 |
| PUT | /api/v1/{resource}/{id} | 更新 |
| DELETE | /api/v1/{resource}/{id} | 删除 |

### 响应格式

```typescript
// 成功响应
{
  "code": 0,
  "message": "success",
  "data": { ... }
}

// 分页响应
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "pageSize": 20
  }
}

// 错误响应
{
  "code": 400,
  "message": "错误描述"
}
```

### 状态码规范

| 状态码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 类型文件位置

| 类型 | 位置 |
|------|------|
| 后端 Schema | `backend/app/schemas/*.py` |
| 后端 Model | `backend/app/models/*.py` |
| 前端共享类型 | `frontend/shared/types/index.ts` |
| API 文档 | `docs/API.md` |

## 变更日志

每次 API 变更需要更新：

1. 后端 Schema 文档注释
2. `docs/API.md`
3. `frontend/shared/types/index.ts`

## 建议：未来可自动化

当项目成熟后，可考虑：
- 使用 OpenAPI (Swagger) 生成 TypeScript 类型
- 使用 `orval` 或 `openapi-typescript-codegen` 自动化
