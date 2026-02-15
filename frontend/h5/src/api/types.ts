/**
 * API 类型定义
 */

/**
 * 课表状态
 */
export enum ScheduleStatus {
  /** 已安排 */
  SCHEDULED = 1,
  /** 已上课 */
  COMPLETED = 2,
  /** 已取消 */
  CANCELLED = 3,
  /** 已调课 */
  RESCHEDULED = 4,
}

/**
 * 课表循环类型
 */
export enum RecurringType {
  /** 单次 */
  SINGLE = 'single',
  /** 每周 */
  WEEKLY = 'weekly',
  /** 每两周 */
  BIWEEKLY = 'biweekly',
}

/**
 * 考勤状态
 */
export enum AttendanceStatus {
  /** 出勤 */
  PRESENT = 1,
  /** 请假 */
  LEAVE = 2,
  /** 缺勤 */
  ABSENT = 3,
  /** 迟到 */
  LATE = 4,
}

/**
 * 签到方式
 */
export enum CheckMethod {
  /** 手动 */
  MANUAL = 1,
  /** 人脸 */
  FACE = 2,
  /** 刷卡 */
  CARD = 3,
}

/**
 * 通知类型
 */
export enum NotificationType {
  /** 上课提醒 */
  CLASS_REMINDER = 1,
  /** 作业通知 */
  HOMEWORK_NOTICE = 2,
  /** 考勤通知 */
  ATTENDANCE_NOTICE = 3,
  /** 合同通知 */
  CONTRACT_NOTICE = 4,
  /** 系统通知 */
  SYSTEM_NOTICE = 5,
}

/**
 * 通知状态
 */
export enum NotificationStatus {
  /** 待发送 */
  PENDING = 0,
  /** 已发送 */
  SENT = 1,
  /** 发送失败 */
  FAILED = 2,
  /** 已阅读 */
  READ = 3,
}

/**
 * 通知接收者类型
 */
export enum ReceiverType {
  /** 企业微信 */
  WEWORK = 1,
  /** 家长 */
  PARENT = 2,
  /** 小程序 */
  MINIAPP = 3,
}

/**
 * 课表响应
 */
export interface ScheduleResponse {
  id: number
  course_id: number
  course_name?: string
  teacher_id: number
  teacher_name?: string
  classroom_id: number
  classroom_name?: string
  department_id?: number
  department_name?: string
  start_time: string
  end_time: string
  week_day?: number
  recurring_type?: string
  recurring_id?: string
  max_students: number
  enrolled_count: number
  status: number
  notes?: string
  created_by?: number
  created_at: string
  updated_at?: string
}

/**
 * 考勤响应
 */
export interface AttendanceResponse {
  id: number
  schedule_id: number
  schedule_name?: string
  student_id: number
  student_name?: string
  contract_id?: number
  status: number
  check_time?: string
  check_method?: number
  hours_consumed: number
  notes?: string
  created_by?: number
  created_at: string
  updated_at?: string
}

/**
 * 考勤统计
 */
export interface AttendanceStatistics {
  total_count: number
  present_count: number
  leave_count: number
  absent_count: number
  late_count: number
  present_rate: number
  total_hours_consumed: number
}

/**
 * 通知响应
 */
export interface NotificationResponse {
  id: number
  type: number
  receiver_id: string
  receiver_type: number
  title: string
  content?: string
  url?: string
  sent_at?: string
  read_at?: string
  status: number
  error_msg?: string
  created_at: string
  updated_at?: string
}

/**
 * 通知列表响应
 */
export interface NotificationListResponse {
  total: number
  unread_count: number
  items: NotificationResponse[]
}

/**
 * 用户角色
 */
export enum UserRole {
  /** 管理员 */
  ADMIN = 'admin',
  /** 教师 */
  TEACHER = 'teacher',
  /** 学员 */
  STUDENT = 'student',
  /** 家长 */
  PARENT = 'parent',
}

/**
 * 用户信息
 */
export interface UserInfo {
  id: number
  username: string
  name: string
  avatar?: string
  role: UserRole
  wework_id?: string
  email?: string
  phone?: string
}

/**
 * 分页参数
 */
export interface PaginationParams {
  skip?: number
  limit?: number
}

/**
 * 日期范围参数
 */
export interface DateRangeParams {
  start_date?: string
  end_date?: string
}
