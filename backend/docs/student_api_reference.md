# 学员管理 API 快速参考

## 基础信息
- **基础路径**: `/api/v1/students`
- **认证**: 需要企业微信 OAuth2 认证
- **响应格式**: JSON

## API 端点

### 1. 获取学员列表
```http
GET /api/v1/students
```

**查询参数**:
- `skip` (integer): 跳过记录数，默认0
- `limit` (integer): 返回记录数，默认100，最大100
- `status` (integer): 状态筛选 (1:潜在 2:在读 3:已流失)
- `source` (string): 来源筛选
- `search` (string): 搜索关键词

**响应**:
```json
[
  {
    "id": 1,
    "name": "张三",
    "nickname": "小三",
    "gender": 1,
    "birthday": "2010-01-01",
    "mobile": "13800138000",
    "parent_name": "张父",
    "parent_wework_id": "parent_wx_id",
    "parent_mobile": "13900139000",
    "source": "线上推广",
    "status": 2,
    "tags": "[\"VIP\", \"重点学员\"]",
    "notes": "备注信息",
    "created_at": "2026-02-14T10:00:00",
    "updated_at": "2026-02-14T10:00:00"
  }
]
```

### 2. 获取学员详情
```http
GET /api/v1/students/{id}
```

**响应**: 同上单个学员对象

### 3. 创建学员
```http
POST /api/v1/students
```

**请求体**:
```json
{
  "name": "张三",
  "nickname": "小三",
  "gender": 1,
  "birthday": "2010-01-01",
  "mobile": "13800138000",
  "parent_name": "张父",
  "parent_wework_id": "parent_wx_id",
  "parent_mobile": "13900139000",
  "source": "线上推广",
  "status": 1,
  "tags": "[\"VIP\"]",
  "notes": "备注"
}
```

**必填字段**:
- `name`: 学员姓名

**响应**: 201 Created + 学员对象

### 4. 更新学员
```http
PUT /api/v1/students/{id}
```

**请求体**: 所有字段都是可选的
```json
{
  "name": "张三三",
  "status": 2
}
```

**响应**: 200 OK + 更新后的学员对象

### 5. 删除学员
```http
DELETE /api/v1/students/{id}
```

**响应**: 204 No Content

### 6. 更新学员状态
```http
PATCH /api/v1/students/{id}/status?status=2
```

**查询参数**:
- `status` (必填): 新状态 (1:潜在 2:在读 3:已流失)

**响应**: 200 OK + 更新后的学员对象

### 7. 添加标签
```http
POST /api/v1/students/{id}/tags
```

**请求体**:
```json
{
  "tag": "VIP"
}
```

**响应**: 200 OK + 更新后的学员对象

### 8. 移除标签
```http
DELETE /api/v1/students/{id}/tags/{tag}
```

**响应**: 200 OK + 更新后的学员对象

### 9. 获取所有标签
```http
GET /api/v1/students/tags/all
```

**响应**:
```json
["VIP", "重点学员", "潜力股"]
```

## 状态码

- `200 OK`: 请求成功
- `201 Created`: 创建成功
- `204 No Content`: 删除成功
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 学员不存在
- `500 Internal Server Error`: 服务器错误

## 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

## 常见错误

1. **学员姓名不能为空**: 创建或更新学员时姓名为空
2. **手机号格式不正确**: 手机号不是11位数字
3. **手机号已被使用**: 尝试创建或更新为已存在的手机号
4. **学员不存在**: 尝试获取、更新或删除不存在的学员
5. **状态值无效**: 状态值不是1、2或3
6. **性别值无效**: 性别值不是1或2

## 使用示例

### cURL 示例

```bash
# 获取学员列表
curl -X GET "http://localhost:8000/api/v1/students?status=2&limit=10"

# 创建学员
curl -X POST "http://localhost:8000/api/v1/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "mobile": "13800138000",
    "status": 1
  }'

# 更新学员状态
curl -X PATCH "http://localhost:8000/api/v1/students/1/status?status=2"

# 添加标签
curl -X POST "http://localhost:8000/api/v1/students/1/tags" \
  -H "Content-Type: application/json" \
  -d '{"tag": "VIP"}'
```

### Python 示例

```python
import httpx

async def manage_students():
    async with httpx.AsyncClient() as client:
        # 获取学员列表
        response = await client.get(
            "http://localhost:8000/api/v1/students",
            params={"status": 2, "limit": 10}
        )
        students = response.json()

        # 创建学员
        student_data = {
            "name": "张三",
            "mobile": "13800138000",
            "status": 1
        }
        response = await client.post(
            "http://localhost:8000/api/v1/students",
            json=student_data
        )
        new_student = response.json()

        # 添加标签
        response = await client.post(
            f"http://localhost:8000/api/v1/students/{new_student['id']}/tags",
            json={"tag": "VIP"}
        )
```

### JavaScript 示例

```javascript
// 获取学员列表
const response = await fetch(
  'http://localhost:8000/api/v1/students?status=2&limit=10'
);
const students = await response.json();

// 创建学员
const newStudent = await fetch('http://localhost:8000/api/v1/students', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '张三',
    mobile: '13800138000',
    status: 1
  })
});
const student = await newStudent.json();

// 添加标签
await fetch(`http://localhost:8000/api/v1/students/${student.id}/tags`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ tag: 'VIP' })
});
```
