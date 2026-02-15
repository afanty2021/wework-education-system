# Course Service Documentation

## 课程服务业务逻辑层

### 概述

`CourseService` 提供了课程、教室、校区的完整业务逻辑处理。所有方法都是异步的，遵循 SOLID 原则，提供了清晰的异常处理和完整的日志记录。

### 功能模块

#### 1. 课程查询服务

- `get_all_courses()` - 获取课程列表，支持分页和筛选
- `get_course_by_id()` - 根据ID获取课程详情
- `search_courses()` - 按名称/分类搜索课程
- `count_courses()` - 统计课程数量

#### 2. 课程管理服务

- `create_course()` - 创建课程，包含验证逻辑
- `update_course()` - 更新课程，包含权限检查
- `delete_course()` - 删除课程，包含关联检查
- `toggle_course_status()` - 切换课程上架/下架状态

#### 3. 教室管理服务

- `get_all_classrooms()` - 获取教室列表
- `get_classroom_by_id()` - 根据ID获取教室详情
- `create_classroom()` - 创建教室
- `update_classroom()` - 更新教室信息
- `delete_classroom()` - 删除教室

#### 4. 校区管理服务

- `get_all_departments()` - 获取校区列表
- `get_department_by_id()` - 根据ID获取校区详情
- `create_department()` - 创建校区
- `update_department()` - 更新校区信息
- `delete_department()` - 删除校区

### 异常类型

- `CourseServiceError` - 课程服务异常基类
- `CourseNotFoundError` - 课程不存在异常
- `ClassroomNotFoundError` - 教室不存在异常
- `DepartmentNotFoundError` - 校区不存在异常
- `CourseHasSchedulesError` - 课程存在关联排课异常
- `InvalidCourseDataError` - 无效的课程数据异常

### 业务规则

#### 课程管理
- 课程编码必须唯一
- 课程时长必须大于0
- 课程价格不能为负数
- 删除课程前检查是否有关联的排课记录

#### 教室管理
- 教室容量必须大于0
- 删除教室前检查是否有关联的排课记录
- 教室可以关联到校区

#### 校区管理
- 校区名称必须唯一
- 删除校区前检查是否有关联的教室或下级校区
- 校区可以设置上级校区形成层级结构

### 使用示例

#### API 路由中使用

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import CourseService, InvalidCourseDataError

router = APIRouter()

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
```

#### 直接调用服务

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.course_service import CourseService

async def my_business_function(db: AsyncSession):
    # 获取所有上架课程
    courses = await CourseService.get_all_courses(
        session=db,
        status=1,
        skip=0,
        limit=100
    )

    # 创建新课程
    from app.schemas.course import CourseCreate
    course_data = CourseCreate(
        name="Python编程基础",
        code="PY101",
        duration=90,
        price=Decimal("150.00"),
        category="编程",
        color="#409EFF",
        max_students=30
    )
    new_course = await CourseService.create_course(course_data, db)

    return new_course
```

### 数据模型映射

#### Course 模型
- `id`: 主键
- `name`: 课程名称
- `code`: 课程编码（唯一）
- `category`: 课程分类
- `color`: 显示颜色
- `duration`: 单节课时长(分钟)
- `price`: 单价(元/课时)
- `max_students`: 最大人数
- `description`: 课程描述
- `status`: 状态 (1:上架 2:下架)
- `created_at`: 创建时间
- `updated_at`: 更新时间

#### Classroom 模型
- `id`: 主键
- `name`: 教室名称
- `department_id`: 所属校区
- `capacity`: 容纳人数
- `equipment`: 设备 JSON数组
- `status`: 状态 (1:可用 2:维护中)
- `created_at`: 创建时间

#### Department 模型
- `id`: 主键
- `name`: 校区名称（唯一）
- `parent_id`: 上级校区
- `manager_id`: 负责人
- `address`: 地址
- `contact`: 联系方式
- `status`: 状态
- `created_at`: 创建时间

### 测试

运行课程服务测试：

```bash
cd backend
pytest tests/test_course_service.py -v
```

### 注意事项

1. **异步操作**: 所有服务方法都需要 `AsyncSession` 参数，使用 `await` 调用
2. **异常处理**: 服务方法会抛出特定异常，建议在 API 层捕获并转换为 HTTP 响应
3. **事务管理**: 服务方法内部处理事务提交和回滚，不需要外部管理
4. **数据验证**: 所有创建和更新操作都会进行数据验证
5. **关联检查**: 删除操作前会检查关联数据，防止数据不一致

### 未来扩展

- [ ] 添加课程分类管理
- [ ] 添加课程标签系统
- [ ] 添加课程评价功能
- [ ] 添加教室设备管理
- [ ] 添加校区容量统计
- [ ] 添加课程推荐算法
