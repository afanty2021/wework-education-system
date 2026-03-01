# 企业微信教育系统 - 环境搭建指南

> 更新时间：2026-02-16

## 环境概述

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.11 | Conda 虚拟环境 |
| PostgreSQL | 15 | Docker 容器运行 |
| Redis | 7 | Docker 容器运行 |
| Node.js | 18+ | 前端依赖管理 |
| FastAPI | 0.110.0 | 后端框架 |
| Vue 3 | 3.4.21 | 前端框架 |

## 环境搭建步骤

### 1. Conda 环境创建

```bash
# 创建 Python 3.11 环境
conda create -n wework-education python=3.11 -y

# 激活环境
conda activate wework-education
```

### 2. 后端依赖安装

```bash
cd backend

# 安装依赖
pip install -r requirements.txt
```

### 3. Docker 服务启动

```bash
# 检查 Docker 状态
docker ps

# PostgreSQL 和 Redis 已在 Docker Desktop 中运行
# 容器名称: english_teaching_postgres, english_teaching_redis
```

### 4. 环境变量配置

在 `backend/.env` 中配置：

```env
# 数据库配置
WEWORK_EDU_DB_PASSWORD=postgres

# Redis 配置
REDIS_URL=redis://:redis_password@localhost:6379/0

# JWT 配置
WEWORK_EDU_SECRET_KEY=your-secret-key

# 企业微信配置（后续填写）
WEWORK_CORP_ID=your_corp_id
WEWORK_AGENT_ID=your_agent_id
WEWORK_SECRET=your_secret

# 支付配置（后续填写）
WECHAT_MCH_ID=your_mch_id
ALIPAY_APP_ID=your_app_id
```

### 5. 前端依赖安装

```bash
cd frontend/admin
npm install
```

## 服务启动

### 后端服务

```bash
# 方式1: 使用 Docker 容器（已在运行）
docker ps | grep english_teaching

# 方式2: 本地启动
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端服务

```bash
cd frontend/admin
npm run dev
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 后端 API 文档 | http://localhost:8000/api/docs |
| 前端管理后台 | http://localhost:3001 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## 数据库初始化

```bash
cd backend

# 运行 Alembic 迁移
alembic upgrade head

# 或使用 SQLModel 创建所有表
python -c "
from sqlmodel import SQLModel, create_engine
from app.models.user import User
from app.models.student import Student
from app.models.course import Course, Classroom, Department
from app.models.contract import Contract
from app.models.payment import Payment
from app.models.schedule import Schedule
from app.models.attendance import Attendance
from app.models.homework import Homework, HomeworkSubmission
from app.models.notification import Notification
from app.models.miniapp_user import MiniAppUser
from app.models.task_log import TaskLog, TaskStatistics

DATABASE_URL = 'postgresql://berton@localhost:5432/english_teaching'
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
print('数据库表创建成功！')
"
```

## 注意事项

1. **Redis 密码**: `redis_password`（从 Docker 容器配置获取）
2. **PostgreSQL 用户**: `berton`（本地连接无需密码）
3. **数据库名称**: `english_teaching`（非 education_db）
4. **wechatpayv3**: 包名为 `wechatpayv3`（非 wechatpay-python-v3），清华源已支持

## 额外依赖（测试需要）

```bash
pip install email-validator aiosqlite greenlet
```

## 测试结果

```bash
pytest tests/ -v
# 结果: 118 passed, 36 skipped, 13 warnings
```

## 依赖版本

```
fastapi==0.110.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.20
alembic==1.13.1
psycopg2-binary==2.9.9
asyncpg==0.29.0
redis==5.0.1
python-jose[cryptography]==3.3.0
pydantic==2.6.0
pytest==7.4.4
pytest-asyncio==0.23.3
alipay-sdk-python==3.7.20
wechatpayv3==2.0.1
```
