# 学员管理功能实现文档

## 实现概述

已成功实现完整的学员管理功能，包括 Schema、CRUD、Service 和 API 四个层面。

## 文件清单

### 1. Schema 层
**文件**: `backend/app/schemas/student.py`

**类**:
- `StudentBase` - 学员基础模型
- `StudentCreate` - 学员创建模型
- `StudentUpdate` - 学员更新模型
- `StudentResponse` - 学员响应模型
- `StudentListResponse` - 学员列表响应模型
- `StudentTagCreate` - 添加标签模型
- `StudentSearchQuery` - 学员搜索查询模型

### 2. CRUD 层
**文件**: `backend/app/crud/student.py`

**类**: `CRUDStudent`

**方法**:
- `get_all()` - 获取所有学员
- `get_by_id()` - 根据ID获取学员
- `get_by_mobile()` - 根据手机号获取学员
- `create()` - 创建学员
- `update()` - 更新学员
- `delete()` - 删除学员
- `count()` - 统计学员数量

### 3. Service 层
**文件**: `backend/app/services/student_service.py`

**类**: `StudentService`

**异常类**:
- `StudentServiceError` - 学员服务异常基类
- `StudentNotFoundError` - 学员不存在异常
- `InvalidStudentDataError` - 无效的学员数据异常

**查询服务**:
- `get_all_students()` - 获取学员列表（支持分页、筛选、搜索）
- `get_student_by_id()` - 根据ID获取学员详情
- `search_students()` - 按关键词搜索学员
- `count_students()` - 统计学员数量
- `get_students_by_tag()` - 根据标签获取学员

**管理服务**:
- `create_student()` - 创建学员（包含数据验证）
- `update_student()` - 更新学员信息（包含数据验证）
- `delete_student()` - 删除学员
- `update_student_status()` - 更新学员状态

**标签服务**:
- `add_tag_to_student()` - 为学员添加标签
- `remove_tag_from_student()` - 从学员移除标签
- `get_all_tags()` - 获取所有使用中的标签

### 4. API 层
**文件**: `backend/app/api/v1/students.py`

**端点**:

#### 基础 CRUD
- `GET /api/v1/students` - 获取学员列表
- `GET /api/v1/students/{id}` - 获取学员详情
- `POST /api/v1/students` - 创建学员
- `PUT /api/v1/students/{id}` - 更新学员
- `DELETE /api/v1/students/{id}` - 删除学员

#### 状态管理
- `PATCH /api/v1/students/{id}/status` - 更新学员状态

#### 标签管理
- `POST /api/v1/students/{id}/tags` - 为学员添加标签
- `DELETE /api/v1/students/{id}/tags/{tag}` - 从学员移除标签
- `GET /api/v1/students/tags/all` - 获取所有标签

## 查询参数

### 列表查询
- `skip` - 跳过记录数（默认0）
- `limit` - 返回记录数（默认100，最大100）
- `status` - 状态筛选（1:潜在 2:在读 3:已流失）
- `source` - 来源筛选
- `search` - 搜索关键词（姓名、手机号、家长手机号、家长姓名）

### 状态更新
- `status` - 新状态值（1:潜在 2:在读 3:已流失）

## 业务规则验证

### 创建学员时
1. 姓名不能为空
2. 手机号格式必须正确（11位数字）
3. 家长手机号格式必须正确（11位数字）
4. 性别值必须是1（男）或2（女）
5. 状态值必须是1（潜在）、2（在读）或3（已流失）
6. 手机号不能重复

### 更新学员时
1. 姓名不能为空（如果要更新）
2. 手机号格式必须正确
3. 手机号不能与其他学员重复
4. 性别值必须有效
5. 状态值必须有效

## 数据模型字段

### Student 模型
- `id` - 主键
- `name` - 学员姓名（必填）
- `nickname` - 昵称
- `gender` - 性别（1:男 2:女）
- `birthday` - 生日
- `mobile` - 手机号
- `parent_name` - 家长姓名
- `parent_wework_id` - 家长企业微信ID
- `parent_mobile` - 家长手机号
- `source` - 来源（线上推广/朋友介绍/地推等）
- `status` - 状态（1:潜在 2:在读 3:已流失）
- `tags` - 标签（JSON数组）
- `notes` - 备注
- `created_at` - 创建时间
- `updated_at` - 更新时间

## 测试文件

### 服务层测试
**文件**: `backend/tests/test_student_service.py`

**测试用例**:
- 创建学员成功
- 创建学员时姓名为空
- 创建学员时手机号格式不正确
- 获取学员详情成功
- 获取不存在的学员
- 更新学员成功
- 删除学员成功
- 添加标签成功
- 添加重复标签
- 移除标签成功
- 获取学员列表并筛选
- 搜索学员
- 更新学员状态
- 统计学员数量
- 根据标签获取学员
- 获取所有标签

### API 测试
**文件**: `backend/tests/test_student_api.py`

**测试用例**:
- 获取学员列表
- 分页获取学员列表
- 按状态筛选学员
- 搜索学员
- 创建学员成功
- 创建学员时姓名为空
- 创建学员时手机号格式不正确
- 获取学员详情成功
- 获取不存在的学员
- 更新学员成功
- 更新不存在的学员
- 删除学员成功
- 删除不存在的学员
- 更新学员状态
- 更新学员状态时状态值无效
- 为学员添加标签
- 添加空标签
- 从学员移除标签
- 获取所有标签

### 集成测试
**文件**: `backend/tests/test_student_integration.py`

**测试场景**:
- 完整的学员管理工作流程
- 学员筛选功能
- 学员数据验证
- API 端点测试

## 使用示例

### 创建学员
```python
from app.schemas.student import StudentCreate
from app.services.student_service import StudentService

student_data = StudentCreate(
    name="张三",
    nickname="小三",
    gender=1,
    birthday=date(2010, 1, 1),
    mobile="13800138000",
    parent_name="张父",
    parent_mobile="13900139000",
    source="线上推广",
    status=1
)

student = await StudentService.create_student(student_data, db_session)
```

### 更新学员
```python
from app.schemas.student import StudentUpdate

update_data = StudentUpdate(
    name="张三三",
    status=2
)

updated_student = await StudentService.update_student(
    student_id, update_data, db_session
)
```

### 添加标签
```python
student = await StudentService.add_tag_to_student(
    student_id, "VIP", db_session
)
```

### 搜索学员
```python
students = await StudentService.search_students("张三", db_session)
```

## 后续改进建议

1. **关联数据检查**: 在删除学员前，检查是否有关联的合同、考勤、作业等数据
2. **批量操作**: 支持批量创建、更新、删除学员
3. **导入导出**: 支持学员数据的批量导入和导出
4. **高级搜索**: 支持更复杂的搜索条件组合
5. **标签管理**: 实现标签的预定义和管理功能
6. **学员合并**: 支持合并重复学员记录
7. **历史记录**: 记录学员的变更历史

## 架构优势

1. **分层清晰**: Schema → CRUD → Service → API，职责分明
2. **异步支持**: 全异步实现，提高性能
3. **类型安全**: 完整的类型提示
4. **错误处理**: 自定义异常类，精确的错误信息
5. **数据验证**: Service 层包含完整的业务规则验证
6. **可测试性**: 每层都有对应的测试文件
7. **文档完善**: 每个函数都有详细的 docstring
