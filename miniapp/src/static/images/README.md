# 静态图片资源

此目录用于存放小程序的静态图片资源。

## 目录结构

```
static/
├── images/
│   ├── logo.png          # 应用Logo
│   ├── default-avatar.png # 默认头像
│   └── empty.png         # 空状态图片
└── tabbar/
    ├── home.png              # 首页图标（未选中）
    ├── home_active.png      # 首页图标（选中）
    ├── schedule.png         # 课表图标（未选中）
    ├── schedule_active.png  # 课表图标（选中）
    ├── attendance.png       # 考勤图标（未选中）
    ├── attendance_active.png# 考勤图标（选中）
    ├── homework.png         # 作业图标（未选中）
    ├── homework_active.png  # 作业图标（选中）
    ├── profile.png          # 个人中心图标（未选中）
    ├── profile_active.png   # 个人中心图标（选中）
    └── scan.png            # 中间扫码按钮
```

## 图片规格

| 位置 | 尺寸 | 格式 |
|------|------|------|
| TabBar图标 | 48x48px | PNG |
| Logo | 200x200px | PNG |
| 默认头像 | 120x120px | PNG |
| 空状态图片 | 300x300px | PNG |

## 注意事项

1. TabBar图片需要同时提供选中状态和未选中状态
2. 图片命名使用小写字母和下划线
3. 建议使用PNG格式保持透明背景
4. 图片文件大小控制在200KB以内
