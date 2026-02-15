/**
 * 全局类型定义
 */

// 通用分页响应
export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

// 通用请求响应
export interface ApiResponse<T> {
  data: T
  code: number
  message: string
}

// 通用列表响应
export interface ListResponse<T> {
  data: T[]
  count?: number
}

// 通用空响应
export interface EmptyResponse {
  success: boolean
  message?: string
}

// 用户类型
export type UserType = 'student' | 'parent' | 'teacher' | 'admin'

// 角色类型
export type RoleType = 'student' | 'parent' | 'teacher' | 'manager' | 'admin'

// 性别枚举
export enum Gender {
  UNKNOWN = 0,
  MALE = 1,
  FEMALE = 2
}

// 性别文本映射
export const GenderText: Record<Gender, string> = {
  [Gender.UNKNOWN]: '未知',
  [Gender.MALE]: '男',
  [Gender.FEMALE]: '女'
}

// 星期几枚举
export enum WeekDay {
  MONDAY = 1,
  TUESDAY = 2,
  WEDNESDAY = 3,
  THURSDAY = 4,
  FRIDAY = 5,
  SATURDAY = 6,
  SUNDAY = 7
}

// 星期几文本映射
export const WeekDayText: Record<WeekDay | number, string> = {
  1: '周一',
  2: '周二',
  3: '周三',
  4: '周四',
  5: '周五',
  6: '周六',
  7: '周日'
}

export const WeekDayFullText: Record<WeekDay | number, string> = {
  1: '星期一',
  2: '星期二',
  3: '星期三',
  4: '星期四',
  5: '星期五',
  6: '星期六',
  7: '星期日'
}

// 课程状态
export enum ScheduleStatus {
  SCHEDULED = 1,   // 已安排
  COMPLETED = 2,   // 已上课
  CANCELLED = 3,   // 已取消
  RESCHEDULED = 4  // 已调课
}

// 课程状态文本
export const ScheduleStatusText: Record<ScheduleStatus, string> = {
  [ScheduleStatus.SCHEDULED]: '已安排',
  [ScheduleStatus.COMPLETED]: '已上课',
  [ScheduleStatus.CANCELLED]: '已取消',
  [ScheduleStatus.RESCHEDULED]: '已调课'
}

// 课程状态颜色
export const ScheduleStatusColor: Record<ScheduleStatus, string> = {
  [ScheduleStatus.SCHEDULED]: '#1890ff',
  [ScheduleStatus.COMPLETED]: '#52c41a',
  [ScheduleStatus.CANCELLED]: '#ff4d4f',
  [ScheduleStatus.RESCHEDULED]: '#faad14'
}

// 考勤状态
export enum AttendanceStatus {
  PRESENT = 1,  // 出勤
  LEAVE = 2,     // 请假
  ABSENT = 3,    // 缺勤
  LATE = 4       // 迟到
}

// 考勤状态文本
export const AttendanceStatusText: Record<AttendanceStatus, string> = {
  [AttendanceStatus.PRESENT]: '出勤',
  [AttendanceStatus.LEAVE]: '请假',
  [AttendanceStatus.ABSENT]: '缺勤',
  [AttendanceStatus.LATE]: '迟到'
}

// 考勤状态颜色
export const AttendanceStatusColor: Record<AttendanceStatus, string> = {
  [AttendanceStatus.PRESENT]: '#52c41a',
  [AttendanceStatus.LEAVE]: '#1890ff',
  [AttendanceStatus.ABSENT]: '#ff4d4f',
  [AttendanceStatus.LATE]: '#faad14'
}

// 合同状态
export enum ContractStatus {
  ACTIVE = 1,      // 生效
  COMPLETED = 2,   // 完结
  REFUNDED = 3,    // 退费
  EXPIRED = 4      // 过期
}

// 合同状态文本
export const ContractStatusText: Record<ContractStatus, string> = {
  [ContractStatus.ACTIVE]: '生效中',
  [ContractStatus.COMPLETED]: '已完结',
  [ContractStatus.REFUNDED]: '已退费',
  [ContractStatus.EXPIRED]: '已过期'
}

// 作业提交状态
export enum HomeworkSubmitStatus {
  NOT_SUBMITTED = 0,  // 未提交
  SUBMITTED = 1,      // 已提交
  GRADED = 2         // 已批改
}

// 作业提交状态文本
export const HomeworkSubmitStatusText: Record<HomeworkSubmitStatus, string> = {
  [HomeworkSubmitStatus.NOT_SUBMITTED]: '未提交',
  [HomeworkSubmitStatus.SUBMITTED]: '已提交',
  [HomeworkSubmitStatus.GRADED]: '已批改'
}

// 签到方式
export enum CheckMethod {
  MANUAL = 1,   // 手动
  FACE = 2,      // 人脸
  CARD = 3       // 刷卡
}

// 签到方式文本
export const CheckMethodText: Record<CheckMethod, string> = {
  [CheckMethod.MANUAL]: '手动签到',
  [CheckMethod.FACE]: '人脸识别',
  [CheckMethod.CARD]: '刷卡签到'
}

// 消息类型
export enum MessageType {
  SYSTEM = 1,           // 系统通知
  HOMEWORK = 2,          // 作业通知
  SCHEDULE_CHANGE = 3,   // 课表变更
  ATTENDANCE = 4,        // 考勤通知
  CONTRACT = 5           // 合同通知
}

// 消息类型文本
export const MessageTypeText: Record<MessageType, string> = {
  [MessageType.SYSTEM]: '系统通知',
  [MessageType.HOMEWORK]: '作业通知',
  [MessageType.SCHEDULE_CHANGE]: '课表变更',
  [MessageType.ATTENDANCE]: '考勤通知',
  [MessageType.CONTRACT]: '合同通知'
}
