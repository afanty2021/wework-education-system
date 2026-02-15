# 企业微信教务系统 - H5教师端

基于 Vue 3 + Vant 4 的移动端教师端应用。

## 功能特性

- 登录认证：支持用户名密码登录、企业微信扫码登录
- 今日课表：查看今日课程安排
- 周课表：按周查看课表，支持日期选择
- 考勤签到：学员签到、批量签到、考勤统计
- 消息通知：通知列表、通知详情、标记已读
- 个人中心：个人信息、设置、退出登录

## 技术栈

- Vue 3 - 前端框架
- Vue Router - 路由管理
- Pinia - 状态管理
- Vant 4 - 移动端组件库
- Axios - HTTP 客户端
- TypeScript - 类型安全
- Vite - 构建工具
- Sass - CSS 预处理器

## 开发

```bash
# 安装依赖
pnpm install

# 开发模式
pnpm dev

# 构建生产版本
pnpm build

# 预览生产版本
pnpm preview
```

## 项目结构

```
src/
├── api/              # API 接口封装
├── assets/          # 静态资源
├── components/      # 公共组件
├── router/          # 路由配置
├── stores/         # Pinia 状态管理
├── styles/         # 样式文件
├── types/          # TypeScript 类型定义
├── utils/          # 工具函数
├── views/          # 页面组件
├── App.vue         # 根组件
└── main.ts         # 应用入口
```

## 环境变量

```bash
# API 地址
VITE_API_BASE_URL=http://localhost:8000/api/v1

# 企业微信 CorpID
VITE_WEWORK_CORP_ID=
```
