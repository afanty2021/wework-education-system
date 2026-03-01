[根目录](../../../CLAUDE.md) > [backend](../../) > [app](../) > **tasks**

# Tasks - 定时任务模块

> 最后更新：2026-02-16

# 定时任务功能实现总结

## 实现时间
2026-02-14

## 实现内容

### 1. 任务模块（`backend/app/tasks/`）

**创建的文件：**
- `__init__.py` - 任务模块初始化
- `reminders.py` - 到期提醒任务
- `contract_expiry.py` - 合同到期检查任务
- `statistics.py` - 统计数据汇总任务

### 2. 到期提醒任务（`reminders.py`）

**实现的功能：**

#### 2.1 合同到期提醒
- `check_contract_expiry_reminders()` - 检查合同到期和课时不足
- `_send_contract_expiry_reminder()` - 发送合同到期提醒
- `_send_low_hours_reminder()` - 发送课时不足提醒

**提醒规则：**
- 合同到期提前30天提醒（可配置）
- 课时不足阈值：4课时（可配置）
- 通过企业微信发送消息
- 记录通知发送状态

#### 2.2 排课提醒
- `check_class_reminders()` - 检查排课提醒
- `_send_class_reminder()` - 发送上课提醒

**提醒规则：**
- 上课前2小时提醒（可配置）
- 包含课程、教师、时间信息
- 发送给家长企业微信

#### 2.3 生日祝福
- `send_birthday_greetings()` - 发送生日祝福
- `_send_birthday_greeting()` - 发送个人生日祝福

**祝福规则：**
- 每天早上9点发送
- 包含学员年龄
- 发送给家长企业微信

### 3. 合同到期检查任务（`contract_expiry.py`）

**实现的功能：**

#### 3.1 过期合同检查
- `check_and_mark_expired_contracts()` - 检查并标记过期合同

**检查规则：**
- 每日凌晨0点执行
- 自动标记过期合同为状态4
- 统计即将到期合同（30天内）

#### 3.2 合同剩余价值计算
- `calculate_remaining_value()` - 计算所有生效合同的剩余价值

**计算内容：**
- 总剩余价值
- 总剩余课时
- 按学员分组的合同统计

#### 3.3 续费提醒生成
- `generate_renewal_reminders()` - 生成续费提醒

**提醒优先级：**
- 高优先级：7天内
- 中优先级：30天内
- 低优先级：60天内

#### 3.4 到期统计分析
- `get_contract_expiry_statistics()` - 获取合同到期统计

**统计维度：**
- 按时间段分组（7天一组）
- 按月份分组
- 风险价值计算（60天内）

#### 3.5 过期合同清理
- `cleanup_expired_contracts()` - 清理过期合同数据

**清理规则：**
- 过期365天后的合同
- 支持归档或删除

### 4. 统计数据汇总任务（`statistics.py`）

**实现的功能：**

#### 4.1 考勤统计
- `summarize_daily_attendance()` - 每日汇总考勤统计

**统计内容：**
- 总课程数、总出勤数
- 出勤、请假、缺勤、迟到数
- 出勤率计算
- 按课程分组统计

#### 4.2 缴费统计
- `summarize_daily_payments()` - 每日汇总缴费统计

**统计内容：**
- 总缴费笔数、缴费总额
- 按缴费方式分组
- 按支付渠道分组
- 退费统计

#### 4.3 合同统计
- `summarize_daily_contracts()` - 每日汇总合同统计

**统计内容：**
- 新签合同数和金额
- 生效合同数
- 总剩余课时和价值
- 按课时包类型分组
- 按状态分组

#### 4.4 学员统计
- `summarize_daily_students()` - 每日汇总学员统计

**统计内容：**
- 总学员数、新增学员数
- 在读学员数
- 按状态分组
- 按来源分组

#### 4.5 综合统计
- `generate_daily_summary()` - 生成每日综合统计汇总

**汇总内容：**
- 考勤、缴费、合同、学员统计

#### 4.6 趋势分析
- `analyze_trends()` - 分析指定天数内的趋势

**分析指标：**
- 每日趋势数据
- 日均缴费和金额
- 增长率计算

### 5. 调度器增强（`backend/app/core/scheduler.py`）

**新增功能：**

#### 5.1 任务执行装饰器
- `log_task_execution()` - 记录任务执行情况
- `retry_on_failure()` - 失败重试装饰器

**装饰器功能：**
- 记录任务开始/结束时间
- 记录执行结果
- 失败自动重试（可配置次数和延迟）

#### 5.2 任务调度器增强
- 事件监听器（执行完成、执行错误）
- 任务注册表管理
- 任务暂停/恢复功能
- 任务状态查询

**新增方法：**
- `pause_job()` - 暂停任务
- `resume_job()` - 恢复任务
- `get_jobs()` - 获取所有任务
- `get_job()` - 获取指定任务
- `get_registered_tasks()` - 获取已注册任务列表
- `print_jobs_status()` - 打印任务状态

#### 5.3 默认任务注册
- `register_default_tasks()` - 注册默认定时任务

**默认任务配置：**
- 每日上午9点：合同到期提醒
- 每2小时：排课提醒
- 每日上午9点：生日祝福
- 每日凌晨0点：检查过期合同
- 每日上午10点：计算合同剩余价值
- 每日凌晨1点：每日统计汇总
- 每周日凌晨2点：每周趋势分析

### 6. 任务执行日志模型（`backend/app/models/task_log.py`）

**创建的模型：**

#### 6.1 TaskLog - 任务执行日志
- `task_id` - 任务ID
- `task_name` - 任务名称
- `trigger_type` - 触发器类型
- `start_time` - 开始时间
- `end_time` - 结束时间
- `duration` - 执行耗时
- `status` - 状态（1:运行中 2:成功 3:失败）
- `result` - 执行结果
- `error_message` - 错误信息
- `retry_count` - 重试次数

#### 6.2 TaskStatistics - 任务统计
- `task_id` - 任务ID
- `task_name` - 任务名称
- `stat_date` - 统计日期
- `total_runs` - 总执行次数
- `success_runs` - 成功次数
- `failed_runs` - 失败次数
- `avg_duration` - 平均执行时长
- `max_duration` - 最大执行时长
- `min_duration` - 最小执行时长
- `last_run_time` - 最后执行时间
- `last_run_status` - 最后执行状态

### 7. 任务管理API（`backend/app/api/v1/tasks.py`）

**实现的端点：**

#### 7.1 任务管理
- `GET /api/v1/tasks` - 获取所有任务列表
- `GET /api/v1/tasks/{task_id}` - 获取任务详情
- `POST /api/v1/tasks/{task_id}/pause` - 暂停任务
- `POST /api/v1/tasks/{task_id}/resume` - 恢复任务
- `POST /api/v1/tasks/{task_id}/trigger` - 手动触发任务

#### 7.2 任务日志
- `GET /api/v1/tasks/{task_id}/logs` - 获取任务执行日志
- `GET /api/v1/tasks/{task_id}/statistics` - 获取任务统计

#### 7.3 调度器管理
- `GET /api/v1/tasks/scheduler/status` - 获取调度器状态
- `POST /api/v1/tasks/scheduler/shutdown` - 关闭调度器
- `POST /api/v1/tasks/scheduler/start` - 启动调度器

### 8. 主应用集成（`backend/app/main.py`）

**更新内容：**
- 导入任务调度器
- 在启动生命周期中注册并启动调度器
- 在关闭生命周期中关闭调度器

## 技术实现特点

### 1. 异步操作
- 所有任务函数都是异步的
- 使用 `async_session_maker()` 获取数据库会话
- 使用 `await` 进行异步调用

### 2. 企业微信集成
- 通过 `wework_service` 发送消息
- 支持文本消息和卡片消息
- 记录消息发送状态

### 3. 任务调度
- 使用 APScheduler 异步调度器
- 支持 Cron 表达式
- 支持固定间隔调度
- 任务执行日志记录
- 失败重试机制

### 4. 通知记录
- 所有发送的通知都会记录到数据库
- 包含发送时间、状态、错误信息
- 支持查询通知历史

### 5. 统计汇总
- 按日期汇总统计数据
- 支持多维度分组统计
- 趋势分析功能

## 业务规则

### 1. 合同到期提醒
- 提前30天默认（可配置）
- 课时不足4课时提醒（可配置）
- 发送给家长企业微信

### 2. 排课提醒
- 上课前2小时提醒（可配置）
- 包含课程、教师、时间信息

### 3. 生日祝福
- 学员生日当天早上9点发送
- 包含年龄信息

### 4. 过期合同处理
- 自动标记为过期状态
- 每日检查一次
- 可选清理功能

## 代码质量

- **SOLID 原则**
  - 单一职责：每个任务函数只负责一个功能
  - 开闭原则：通过装饰器扩展功能
  - 依赖倒置：依赖抽象的通知服务

- **DRY 原则**
  - 通用的通知发送函数
  - 通用的任务装饰器

- **KISS 原则**
  - 简洁明了的任务函数
  - 清晰的命名规范

- **YAGNI 原则**
  - 只实现当前需要的功能
  - 避免过度设计

## 配置说明

### 环境变量
无特殊环境变量要求，使用现有配置。

### 可配置参数
- `DEFAULT_CONTRACT_WARNING_DAYS` - 合同到期预警天数（默认30）
- `DEFAULT_LOW_HOURS_THRESHOLD` - 课时不足阈值（默认4.0）
- `DEFAULT_CLASS_REMINDER_HOURS` - 排课提前提醒小时数（默认2）
- `BIRTHDAY_GREETING_HOUR` - 生日祝福发送时间（默认9）

## 使用示例

### 1. 注册默认任务
```python
from app.core.scheduler import register_default_tasks

register_default_tasks()
```

### 2. 手动添加任务
```python
from app.core.scheduler import scheduler
from app.tasks.reminders import check_contract_expiry_reminders

scheduler.add_job(
    func=check_contract_expiry_reminders,
    trigger="cron",
    task_id="custom_task",
    task_name="自定义任务",
    hour=10,
    minute=0
)
```

### 3. 查看任务状态
```python
from app.core.scheduler import scheduler

# 获取所有任务
jobs = scheduler.get_jobs()

# 获取指定任务
job = scheduler.get_job("task_id")

# 打印任务状态
scheduler.print_jobs_status()
```

### 4. 暂停/恢复任务
```python
# 暂停任务
scheduler.pause_job("task_id")

# 恢复任务
scheduler.resume_job("task_id")
```

## 测试建议

### 1. 单元测试
- 测试各个任务函数
- 测试通知发送功能
- 测试统计汇总功能

### 2. 集成测试
- 测试任务调度器启动
- 测试任务执行流程
- 测试企业微信集成

### 3. 性能测试
- 测试大量数据下的任务执行
- 测试并发任务执行

## 监控建议

### 1. 日志监控
- 关注任务执行日志
- 关注错误日志
- 关注执行时长

### 2. 通知监控
- 监控通知发送成功率
- 监控通知失败原因

### 3. 统计监控
- 监控任务执行次数
- 监控任务成功率
- 监控平均执行时长

## 后续优化

### 1. 任务执行日志持久化
- 将任务执行日志保存到数据库
- 实现任务统计功能
- 添加任务执行历史查询

### 2. 任务依赖支持
- 实现任务间的依赖关系
- 支持任务链式执行

### 3. 分布式任务调度
- 使用 Celery 替代 APScheduler
- 支持多服务器部署
- 支持任务队列

### 4. 任务监控面板
- Web界面查看任务状态
- 可视化任务执行历史
- 支持手动触发任务

## 相关文件

- `backend/app/tasks/__init__.py` - 任务模块导出
- `backend/app/tasks/reminders.py` - 到期提醒任务
- `backend/app/tasks/contract_expiry.py` - 合同到期检查
- `backend/app/tasks/statistics.py` - 统计数据汇总
- `backend/app/core/scheduler.py` - 任务调度器
- `backend/app/models/task_log.py` - 任务日志模型
- `backend/app/api/v1/tasks.py` - 任务管理API
- `backend/app/main.py` - 主应用入口

## 变更记录

### 2026-02-14 - 初始实现
- 创建任务模块
- 实现到期提醒任务
- 实现合同到期检查
- 实现统计数据汇总
- 增强任务调度器
- 创建任务日志模型
- 实现任务管理API
- 集成到主应用


<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

### Feb 14, 2026

| ID | Time | T | Title | Read |
|----|------|---|-------|------|
| #3637 | 1:50 PM | 🟣 | Backend project structure scaffolded with 57 Python files | ~243 |

### Feb 16, 2026

| ID | Time | T | Title | Read |
|----|------|---|-------|------|
| #4140 | 5:41 AM | ✅ | Updated tasks module CLAUDE.md with navigation and timestamps | ~148 |
</claude-mem-context>