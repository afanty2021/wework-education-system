# 小程序页面说明

## 页面结构

```
pages/
├── index/          # 首页
│   └── index.vue   # 首页组件
├── schedule/       # 课表模块
│   ├── schedule.vue    # 课表列表页
│   └── detail.vue      # 课表详情页
├── attendance/     # 考勤模块
│   └── attendance.vue  # 考勤记录页
├── homework/       # 作业模块
│   ├── homework.vue    # 作业列表页
│   └── detail.vue      # 作业详情页
├── payment/       # 缴费模块
│   ├── list.vue        # 缴费列表页
│   ├── detail.vue      # 缴费详情页
│   ├── pay.vue         # 在线支付页
│   └── history.vue     # 缴费记录页
├── leave/         # 请假模块
│   ├── list.vue        # 请假列表页
│   ├── apply.vue       # 申请请假页
│   └── detail.vue      # 请假详情页
├── leavechange/   # 调课模块
│   ├── list.vue        # 调课列表页
│   ├── apply.vue       # 申请调课页
│   └── detail.vue      # 调课详情页
├── profile/        # 个人中心
│   └── profile.vue     # 个人中心页
└── login/          # 登录模块
    └── login.vue      # 登录页
```

## 页面功能说明

### 首页 (pages/index/index.vue)
- 展示用户基本信息
- 显示今日课表概览
- 待完成作业快捷入口
- 最近考勤记录
- 快捷功能入口导航

### 课表模块
- **课表列表页** (pages/schedule/schedule.vue)
  - 周视图切换
  - 星期选择器
  - 按日期筛选课程

- **课表详情页** (pages/schedule/detail.vue)
  - 课程详细信息
  - 教师信息
  - 教室信息
  - 设置课程提醒

### 考勤模块
- **考勤记录页** (pages/attendance/attendance.vue)
  - 考勤统计概览
  - 按状态筛选（出勤/请假/缺勤/迟到）
  - 考勤记录列表

### 作业模块
- **作业列表页** (pages/homework/homework.vue)
  - 按状态筛选（全部/待提交/已提交/已批改）
  - 作业列表展示

- **作业详情页** (pages/homework/detail.vue)
  - 作业内容展示
  - 截止日期提示
  - 作业提交功能
  - 批改结果展示

### 个人中心 (pages/profile/profile.vue)
- 用户信息展示
- 统计数据概览
- 快捷功能入口
- 菜单列表（个人信息/绑定管理/消息设置等）
- 退出登录

### 登录模块
- **登录页** (pages/login/login.vue)
  - 微信授权登录
  - 游客模式

### 缴费模块
- **缴费列表页** (pages/payment/list.vue)
  - 缴费统计概览
  - 按状态筛选（全部/待缴费/已缴费/已退款）
  - 缴费列表展示

- **缴费详情页** (pages/payment/detail.vue)
  - 缴费金额和课时信息
  - 支付状态展示
  - 支付方式信息

- **在线支付页** (pages/payment/pay.vue)
  - 支付方式选择（微信/支付宝/现金/银行卡/转账）
  - 支付状态查询
  - 微信支付集成

- **缴费记录页** (pages/payment/history.vue)
  - 历史缴费记录查询
  - 支付凭证查看

### 请假模块
- **请假列表页** (pages/leave/list.vue)
  - 请假统计概览
  - 按状态筛选（全部/待审核/已通过）
  - 请假列表展示

- **申请请假页** (pages/leave/apply.vue)
  - 选择课程
  - 选择请假日期和课时
  - 输入请假原因
  - 表单验证

- **请假详情页** (pages/leave/detail.vue)
  - 请假状态展示
  - 课程和时间信息
  - 请假原因展示
  - 取消请假功能

### 调课模块
- **调课列表页** (pages/leavechange/list.vue)
  - 调课统计概览
  - 按状态筛选（全部/待审核/已通过/已拒绝）
  - 调课列表展示

- **申请调课页** (pages/leavechange/apply.vue)
  - 选择原课程
  - 选择目标日期
  - 输入调课原因
  - 表单验证

- **调课详情页** (pages/leavechange/detail.vue)
  - 调课状态展示
  - 原课程和目标课程信息
  - 调课原因展示
  - 拒绝原因展示（如有）
  - 取消调课功能

## 页面通信

### 页面间传参
- 通过URL query参数传递，如 `/pages/homework/detail?id=123`
- 使用 `useRoute` hook 获取参数

### 状态管理
- 使用Pinia store进行全局状态管理
- `useUserStore`: 用户信息状态
- `useScheduleStore`: 课表状态
- `useAttendanceStore`: 考勤状态
- `useHomeworkStore`: 作业状态
- `usePaymentStore`: 缴费状态
- `useLeaveStore`: 请假状态
- `useLeaveChangeStore`: 调课状态

## 生命周期

### 页面加载
```typescript
onMounted(() => {
  // 页面加载时初始化数据
  initPage()
})
```

### 下拉刷新
```typescript
async function onPullDownRefresh() {
  await initPage()
  uni.stopPullDownRefresh()
}
```

## 样式规范

### 尺寸单位
- 使用rpx作为响应式尺寸单位
- 设计稿宽度为750px

### 颜色规范
- 主色调：#1890ff (蓝色)
- 成功色：#52c41a (绿色)
- 警告色：#faad14 (黄色)
- 错误色：#ff4d4f (红色)
- 文字主色：#303133
- 文字辅助色：#909399

## 最佳实践

1. **数据加载**: 页面初始化时使用 `Promise.all` 并行加载数据
2. **错误处理**: 使用 try-catch 处理异步操作，显示错误提示
3. **加载状态**: 使用loading状态显示加载动画
4. **空状态处理**: 使用EmptyState组件展示空状态
5. **下拉刷新**: 页面支持下拉刷新功能
