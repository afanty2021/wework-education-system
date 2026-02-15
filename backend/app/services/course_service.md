# 课程服务实现总结

## 实现概览

本次任务完成了课程服务业务逻辑层的完整实现，包括课程、教室、校区的CRUD操作和业务规则验证。

## 实现的文件

### 1. 服务层 (`app/services/course_service.py`)

实现了 `CourseService` 类，包含以下功能：

#### 课程查询服务
- `get_all_courses()` - 获取课程列表，支持分页、分类筛选、状态筛选、关键词搜索
- `get_course_by_id()` - 根据ID获取课程详情
- `search_courses()` - 按名称/编码/分类/描述搜索课程
- `count_courses()` - 统计课程数量

#### 课程管理服务
- `create_course()` - 创建课程，包含完整的数据验证
- `update_course()` - 更新课程，支持部分字段更新
- `delete_course()` - 删除课程，检查关联的排课记录
- `toggle_course_status()` - 切换课程上架/下架状态

#### 教室管理服务
- `get_all_classrooms()` - 获取教室列表，支持校区和状态筛选
- `get_classroom_by_id()` - 根据ID获取教室详情
- `create_classroom()` - 创建教室，验证容量和校区
- `update_classroom()` - 更新教室信息
- `delete_classroom()` - 删除教室，检查关联的排课记录

#### 校区管理服务
- `get_all_departments()` - 获取校区列表
- `get_department_by_id()` - 根据ID获取校区详情
- `create_department()` - 创建校区，验证名称唯一性
- `update_department()` - 更新校区信息
- `delete_department()` - 删除校区，检查关联的教室和下级校区

#### 异常类
- `CourseServiceError` - 基础异常类
- `CourseNotFoundError` - 课程不存在
- `ClassroomNotFoundError` - 教室不存在
- `DepartmentNotFoundError` - 校区不存在
- `CourseHasSchedulesError` - 课程存在关联排课
- `InvalidCourseDataError` - 无效数据

### 2. 数据库连接更新 (`app/core/db.py`)

- 添加了异步数据库引擎支持（`async_engine`）
- 添加了异步会话工厂（`async_session_maker`）
- 更新了 `get_db()` 函数返回 `AsyncSession`
- 保留了同步支持用于管理任务（`get_sync_db()`）

### 3. Schema 更新 (`app/schemas/course.py`)

完全重写了 course schemas，添加了：
- 教室相关的 schemas（`ClassroomCreate`, `ClassroomUpdate`, `ClassroomResponse`）
- 校区相关的 schemas（`DepartmentCreate`, `DepartmentUpdate`, `DepartmentResponse`）
- 使用 Pydantic `Field` 添加了详细的字段描述
- 修正了字段名称以匹配数据库模型（`duration` vs `duration_minutes`）

### 4. API 路由更新 (`app/api/v1/courses.py`)

- 实现了所有 TODO 的 API 端点
- 添加了 `toggle_course_status` 路由
- 添加了查询参数验证（`Query`）
- 完善了异常处理和 HTTP 状态码
- 添加了详细的 API 文档字符串

### 5. 依赖更新 (`requirements.txt`)

- 添加了 `asyncpg==0.29.0` 用于异步 PostgreSQL 支持

### 6. 测试文件 (`tests/test_course_service.py`)

创建了完整的测试套件，包含：
- 课程创建、更新、删除、查询测试
- 教室创建、查询测试
- 校区创建、查询测试
- 边界条件和异常情况测试

### 7. 服务导出 (`app/services/__init__.py`)

导出 `AuthBusinessService` 和 `CourseService`

### 8. 文档 (`app/services/course_service.README.md`)

创建了完整的服务使用文档，包括：
- 功能模块说明
- 异常类型
- 业务规则
- 使用示例
- 数据模型映射

## 技术要点

### 1. 异步编程

所有服务方法都使用 `async/await` 模式：
```python
@staticmethod
async def get_course_by_id(course_id: int, session: AsyncSession) -> Course:
    result = await session.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise CourseNotFoundError(f"课程不存在: {course_id}")
    return course
```

### 2. SQLAlchemy 2.0 风格

使用现代化的查询语法：
```python
query = select(Course).where(
    and_(
        Course.code == course_data.code,
        Course.id != course_id
    )
)
```

### 3. 完整的类型提示

所有方法都有完整的类型注解：
```python
async def create_course(
    course_data: CourseCreate,
    session: AsyncSession
) -> Course:
```

### 4. 详细的日志记录

使用 Python logging 模块记录操作：
```python
logger.info(f"创建课程: name={course_data.name}, code={course_data.code}")
logger.warning(f"课程存在 {schedule_count} 个排课记录，无法删除")
logger.error(f"创建课程失败: {e}")
```

### 5. 业务规则验证

在服务层实现完整的业务逻辑：
- 数据有效性验证
- 唯一性检查
- 关联数据检查
- 事务处理

## 设计原则

### SOLID 原则

1. **单一职责**: 每个方法只做一件事
2. **开闭原则**: 通过异常类扩展，无需修改核心代码
3. **里氏替换**: 异常类继承自基类，可以互换使用
4. **接口隔离**: 方法参数精确，不强迫依赖不需要的接口
5. **依赖倒置**: 依赖 `AsyncSession` 抽象，不依赖具体实现

### DRY (Don't Repeat Yourself)

- 创建了可复用的异常类
- 统一的错误处理模式
- 共享的验证逻辑

### KISS (Keep It Simple, Stupid)

- 简单明了的方法命名
- 清晰的参数和返回值
- 直观的业务逻辑

### YAGNI (You Aren't Gonna Need It)

- 只实现当前需要的功能
- 不添加未来可能需要的功能
- 保持代码精简

## 数据流

```
API 层 (courses.py)
    ↓ 接收请求，验证参数
服务层 (course_service.py)
    ↓ 业务逻辑，数据验证
CRUD 层 (SQLModel/SQLAlchemy)
    ↓ 数据库操作
PostgreSQL 数据库
```

## 使用示例

### 在 API 路由中使用

```python
@router.post("", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        course = await CourseService.create_course(course_data, db)
        return course
    except InvalidCourseDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 在其他服务中调用

```python
from app.services.course_service import CourseService

async def schedule_course(db: AsyncSession):
    # 获取所有上架课程
    courses = await CourseService.get_all_courses(
        session=db,
        status=1
    )
    # 业务逻辑...
```

## 测试策略

### 单元测试

- 测试每个服务方法
- 覆盖正常流程和异常情况
- 使用 pytest 异步测试支持

### 集成测试

- 测试 API 路由与服务层的集成
- 测试事务处理
- 测试并发操作

## 后续工作

### 可选的增强功能

1. **添加缓存** - 对频繁查询的课程列表添加 Redis 缓存
2. **批量操作** - 支持批量创建/更新课程
3. **软删除** - 添加 deleted_at 字段支持软删除
4. **审计日志** - 记录所有数据变更历史
5. **权限控制** - 添加基于角色的访问控制
6. **数据导入导出** - 支持 Excel/CSV 批量导入导出
7. **课程统计** - 添加课程报名统计、收入统计
8. **教室预约** - 添加教室时间冲突检查

### 性能优化

- 添加数据库索引优化查询性能
- 实现查询结果分页优化
- 使用连接池优化数据库连接

## 总结

本次实现：
- ✅ 完成了完整的课程服务业务逻辑层
- ✅ 实现了课程、教室、校区的 CRUD 操作
- ✅ 添加了完整的业务规则验证
- ✅ 使用异步编程模式提高性能
- ✅ 遵循 SOLID、DRY、KISS、YAGNI 原则
- ✅ 添加了完整的类型提示和文档
- ✅ 创建了测试套件验证功能
- ✅ 提供了详细的使用文档

代码质量：
- ✅ 所有文件通过语法检查
- ✅ 遵循项目代码风格
- ✅ 使用现代 Python 异步编程
- ✅ 完整的异常处理和日志记录
