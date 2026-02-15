# 部署指南

## 企业微信教务系统部署指南

本文档详细介绍如何在不同环境下部署企业微信教务系统。

---

## 目录

1. [环境要求](#环境要求)
2. [开发环境部署](#开发环境部署)
3. [生产环境部署](#生产环境部署)
4. [Docker 部署](#docker-部署)
5. [数据库迁移](#数据库迁移)
6. [配置说明](#配置说明)
7. [常见问题](#常见问题)

---

## 环境要求

### 硬件要求

- CPU: 2 核以上
- 内存: 4GB 以上
- 硬盘: 50GB 以上

### 软件要求

- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Nginx (生产环境)
- Docker & Docker Compose (容器化部署)

---

## 开发环境部署

### 1. 克隆项目

```bash
git clone https://github.com/your-repo/wework-education-system.git
cd wework-education-system
```

### 2. 创建虚拟环境

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量示例文件
cp backend/.env.example backend/.env

# 编辑 .env 文件，修改以下配置：
# - DB_PASSWORD: 设置数据库密码
# - SECRET_KEY: 设置 JWT 密钥
```

### 5. 启动数据库

使用 Docker 启动 PostgreSQL 和 Redis：

```bash
docker run -d \
  --name education_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=education_db \
  -p 5432:5432 \
  postgres:15-alpine

docker run -d \
  --name education_redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 6. 初始化数据库

```bash
cd backend
python -c "from app.core.db import create_db_and_tables; import asyncio; asyncio.run(create_db_and_tables())"
```

### 7. 启动应用

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. 访问应用

- API 文档: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

---

## 生产环境部署

### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install -y curl git nginx docker.io docker-compose
```

### 2. 配置防火墙

```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 3. 部署项目

```bash
# 克隆项目
git clone https://github.com/your-repo/wework-education-system.git
cd wework-education-system

# 配置环境变量
cp backend/.env.example backend/.env
nano backend/.env
```

### 4. 配置 SSL 证书

```bash
# 使用 Let's Encrypt 免费证书
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 5. 启动服务

```bash
cd deployment
docker-compose -f docker-compose.prod.yml up -d
```

### 6. 查看日志

```bash
docker-compose -f docker-compose.prod.yml logs -f backend
```

---

## Docker 部署

### 开发环境

```bash
cd deployment
docker-compose up -d
```

### 生产环境

```bash
cd deployment
docker-compose -f docker-compose.prod.yml up -d
```

### 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps

# 重启服务
docker-compose restart

# 构建镜像
docker-compose build
```

---

## 数据库迁移

### 首次运行

```bash
# 创建初始迁移
cd backend
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 后续更新

```bash
# 创建新迁移
alembic revision --autogenerate -m "Add new field"

# 查看迁移状态
alembic current

# 升级
alembic upgrade +1

# 降级
alembic downgrade -1
```

---

## 配置说明

### 环境变量

| 变量名 | 描述 | 必填 | 默认值 |
|--------|------|------|--------|
| ENVIRONMENT | 环境类型 | 是 | development |
| DB_USER | 数据库用户名 | 是 | postgres |
| DB_PASSWORD | 数据库密码 | 是 | - |
| DB_HOST | 数据库主机 | 否 | localhost |
| DB_PORT | 数据库端口 | 否 | 5432 |
| DB_NAME | 数据库名称 | 否 | education_db |
| REDIS_URL | Redis 连接地址 | 是 | redis://localhost:6379/0 |
| SECRET_KEY | JWT 密钥 | 是 | - |
| WEWORK_CORP_ID | 企业微信 ID | 是 | - |
| WEWORK_AGENT_ID | 企业微信应用 ID | 是 | - |
| WEWORK_SECRET | 企业微信密钥 | 是 | - |
| WECHAT_MCH_ID | 微信支付商户号 | 否 | - |
| ALIPAY_APP_ID | 支付宝应用 ID | 否 | - |

### 端口说明

| 端口 | 服务 |
|------|------|
| 80 | HTTP |
| 443 | HTTPS |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8000 | Backend API |

---

## 常见问题

### Q: 数据库连接失败

**解决方案:**
1. 检查 PostgreSQL 是否运行: `docker ps | grep postgres`
2. 检查环境变量配置是否正确
3. 验证数据库用户名和密码

### Q: Redis 连接失败

**解决方案:**
1. 检查 Redis 是否运行: `docker ps | grep redis`
2. 检查 REDIS_URL 配置

### Q: 企业微信登录失败

**解决方案:**
1. 检查企业微信配置是否正确
2. 确认 Corp ID、Agent ID、Secret 是否有效
3. 检查回调地址是否可访问

### Q: 支付功能无法使用

**解决方案:**
1. 检查微信支付/支付宝配置
2. 确认商户号和密钥是否正确
3. 检查回调通知地址是否可公网访问

### Q: 如何更新应用

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build backend

# 重启服务
docker-compose restart backend
```

---

## 监控和维护

### 日志查看

```bash
# 应用日志
docker-compose logs -f backend

# Nginx 日志
docker-compose logs -f nginx

# PostgreSQL 日志
docker-compose logs -f db
```

### 性能监控

建议使用以下工具监控:
- Prometheus + Grafana
- Sentry (错误追踪)
- Jaeger (分布式追踪)

### 备份策略

```bash
# 数据库备份
docker exec education_db pg_dump -U postgres education_db > backup.sql

# 数据恢复
docker exec -i education_db psql -U postgres education_db < backup.sql
```

---

## 安全建议

1. **使用强密码**: 设置复杂的数据库密码和 JWT 密钥
2. **启用 HTTPS**: 生产环境必须使用 SSL 证书
3. **限制端口**: 只开放必要的端口
4. **定期更新**: 及时更新依赖包
5. **日志审计**: 定期检查访问日志
6. **数据备份**: 定期备份数据库

---

## 相关文档

- [API 文档](./API.md)
- [数据库文档](./DATABASE.md)
- [开发指南](./development.md)
