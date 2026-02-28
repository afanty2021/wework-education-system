/**
 * 企业微信教育系统 - 共享类型定义
 *
 * 本目录包含前后端共用的类型定义
 * 用于确保 API 类型一致性
 */

// ============= 通用类型 =============

/**
 * 分页请求参数
 */
export interface PageParams {
  page?: number
  pageSize?: number
  skip?: number
  limit?: number
}

/**
 * 分页响应
 */
export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

/**
 * API 响应包装
 */
export interface ApiResponse<T> {
  code: number
  message: string
  data?: T
}

/**
 * 基础增删改查响应
 */
export interface CRUDResponse<T> {
  id: number
  item: T
}

// ============= 用户与认证 =============

/**
 * 用户角色
 */
export enum UserRole {
  ADMIN = 'admin',
  TEACHER = 'teacher',
  STUDENT = 'student',
  GUARDIAN = 'guardian',
}

/**
 * 用户信息
 */
export interface User {
  id: number
  username: string
  email?: string
  phone?: string
  role: UserRole
  wework_user_id?: string
  avatar?: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

/**
 * 登录请求
 */
export interface LoginParams {
  code: string // 企业微信授权码
}

/**
 * 登录响应
 */
export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// ============= 学员管理 =============

/**
 * 学员状态
 */
export enum StudentStatus {
  POTENTIAL = 1, // 潜在
  ACTIVE = 2, // 在读
  LOST = 3, // 已流失
}

/**
 * 学员信息
 */
export interface Student {
  id: number
  name: string
  phone?: string
  email?: string
  wechat?: string
  guardian_name?: string
  guardian_phone?: string
  source?: string
  tags: string[]
  status: StudentStatus
  remark?: string
  avatar?: string
  created_at?: string
  updated_at?: string
}

// ============= 课程管理 =============

/**
 * 课程状态
 */
export enum CourseStatus {
  DRAFT = 0,     // 草稿
  PUBLISHED = 1, // 已发布
  ARCHIVED = 2,  // 已归档
}

/**
 * 课程信息
 */
export interface Course {
  id: number
  name: string
  description?: string
  category?: string
  price: number
  duration: number // 课时数
  status: CourseStatus
  cover_image?: string
  teacher_id?: number
  created_at?: string
  updated_at?: string
}

// ============= 合同管理 =============

/**
 * 合同状态
 */
export enum ContractStatus {
  ACTIVE = 1,     // 生效
  COMPLETED = 2, // 完结
  REFUNDED = 3,  // 退费
  EXPIRED = 4,   // 过期
}

/**
 * 合同信息
 */
export interface Contract {
  id: number
  contract_no: string
  student_id: number
  course_id?: number
  total_hours: number
  remaining_hours: number
  unit_price: number
  discount_amount: number
  total_amount: number
  status: ContractStatus
  start_date: string
  end_date?: string
  remark?: string
  created_at?: string
  updated_at?: string
}

// ============= 支付管理 =============

/**
 * 支付状态
 */
export enum PaymentStatus {
  PENDING = 0,   // 待支付
  PAID = 1,      // 已支付
  REFUNDED = 2,  // 已退款
  FAILED = 3,    // 支付失败
}

/**
 * 支付方式
 */
export enum PaymentMethod {
  WECHAT = 'wechat',
  ALIPAY = 'alipay',
  CASH = 'cash',
}

/**
 * 支付记录
 */
export interface Payment {
  id: number
  order_no: string
  student_id: number
  contract_id?: number
  amount: number
  payment_method: PaymentMethod
  status: PaymentStatus
  transaction_id?: string
  paid_at?: string
  created_at?: string
}

// ============= 考勤管理 =============

/**
 * 考勤状态
 */
export enum AttendanceStatus {
  PRESENT = 1,   // 正常
  ABSENT = 2,    // 缺勤
  LATE = 3,      // 迟到
  LEAVE = 4,     // 请假
}

/**
 * 考勤记录
 */
export interface Attendance {
  id: number
  student_id: number
  schedule_id: number
  status: AttendanceStatus
  check_in_time?: string
  check_out_time?: string
  remark?: string
  created_at?: string
}

// ============= 排课管理 =============

/**
 * 排课状态
 */
export enum ScheduleStatus {
  SCHEDULED = 1,  // 已排课
  CANCELLED = 2,  // 已取消
  COMPLETED = 3,  // 已完成
}

/**
 * 排课信息
 */
export interface Schedule {
  id: number
  course_id: number
  classroom_id?: number
  teacher_id: number
  week_day: number // 1-7
  start_time: string // HH:mm
  end_time: string   // HH:mm
  status: ScheduleStatus
  semester?: string
  created_at?: string
}

// ============= 作业管理 =============

/**
 * 作业状态
 */
export enum HomeworkStatus {
  DRAFT = 0,      // 草稿
  PUBLISHED = 1,  // 已发布
  CLOSED = 2,    // 已关闭
}

/**
 * 作业提交状态
 */
export enum HomeworkSubmitStatus {
  PENDING = 0,   // 未提交
  SUBMITTED = 1,  // 已提交
  GRADED = 2,    // 已批改
}

/**
 * 作业信息
 */
export interface Homework {
  id: number
  course_id: number
  title: string
  content: string
  deadline?: string
  status: HomeworkStatus
  created_at?: string
  updated_at?: string
}

/**
 * 作业提交
 */
export interface HomeworkSubmission {
  id: number
  homework_id: number
  student_id: number
  content?: string
  attachment_urls?: string[]
  status: HomeworkSubmitStatus
  score?: number
  teacher_remark?: string
  submitted_at?: string
  graded_at?: string
}

// ============= 通知管理 =============

/**
 * 通知类型
 */
export enum NotificationType {
  SYSTEM = 1,    // 系统通知
  COURSE = 2,   // 课程通知
  HOMEWORK = 3, // 作业通知
  PAYMENT = 4,  // 支付通知
  ATTENDANCE = 5, // 考勤通知
}

/**
 * 通知状态
 */
export enum NotificationStatus {
  UNREAD = 0,  // 未读
  READ = 1,   // 已读
}

/**
 * 通知信息
 */
export interface Notification {
  id: number
  user_id: number
  type: NotificationType
  title: string
  content: string
  link_url?: string
  status: NotificationStatus
  created_at: string
  read_at?: string
}
