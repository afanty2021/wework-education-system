/**
 * 日期格式化工具函数
 */

/**
 * 格式化日期为指定格式
 * @param date 日期对象或日期字符串
 * @param format 格式化模板
 * @returns 格式化后的日期字符串
 */
export function formatDate(
  date: Date | string,
  format: string = 'YYYY-MM-DD'
): string {
  const d = typeof date === 'string' ? new Date(date) : date

  const year = d.getFullYear()
  const month = d.getMonth() + 1
  const day = d.getDate()
  const hour = d.getHours()
  const minute = d.getMinutes()
  const second = d.getSeconds()
  const week = d.getDay()

  const formatMap: Record<string, string | number> = {
    'YYYY': year,
    'MM': String(month).padStart(2, '0'),
    'M': month,
    'DD': String(day).padStart(2, '0'),
    'D': day,
    'HH': String(hour).padStart(2, '0'),
    'H': hour,
    'mm': String(minute).padStart(2, '0'),
    'm': minute,
    'ss': String(second).padStart(2, '0'),
    's': second,
    'W': week
  }

  return format.replace(/YYYY|MM|M|DD|D|HH|H|mm|m|ss|s|W/g, (match) => {
    return String(formatMap[match])
  })
}

/**
 * 格式化时间为 HH:mm 格式
 * @param date 日期对象或日期字符串
 * @returns 时间字符串
 */
export function formatTime(date: Date | string): string {
  return formatDate(date, 'HH:mm')
}

/**
 * 格式化为完整日期时间
 * @param date 日期对象或日期字符串
 * @returns 完整日期时间字符串
 */
export function formatDateTime(date: Date | string): string {
  return formatDate(date, 'YYYY-MM-DD HH:mm')
}

/**
 * 格式化为中文日期
 * @param date 日期对象或日期字符串
 * @returns 中文日期字符串
 */
export function formatDateCN(date: Date | string): string {
  return formatDate(date, 'YYYY年M月D日')
}

/**
 * 格式化为中文日期时间
 * @param date 日期对象或日期字符串
 * @returns 中文日期时间字符串
 */
export function formatDateTimeCN(date: Date | string): string {
  return formatDate(date, 'YYYY年M月D日 HH:mm')
}

/**
 * 格式化为简短日期（用于列表显示）
 * @param date 日期对象或日期字符串
 * @returns 简短日期字符串
 */
export function formatShortDate(date: Date | string): string {
  return formatDate(date, 'M月D日')
}

/**
 * 格式化为相对时间
 * @param date 日期对象或日期字符串
 * @returns 相对时间字符串
 */
export function formatRelativeTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diff = now.getTime() - d.getTime()

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}

/**
 * 获取今天是星期几
 * @returns 星期几 (1-7)
 */
export function getTodayWeekday(): number {
  const weekday = new Date().getDay()
  return weekday === 0 ? 7 : weekday
}

/**
 * 格式化星期几
 * @param weekday 星期几 (1-7)
 * @param short 是否简写
 * @returns 星期几文本
 */
export function formatWeekday(weekday: number, short: boolean = true): string {
  const weekDaysCN = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const weekDaysFull = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']

  if (weekday < 1 || weekday > 7) {
    return '未知'
  }

  return short ? weekDaysCN[weekday - 1] : weekDaysFull[weekday - 1]
}

/**
 * 计算两个日期相差天数
 * @param date1 日期1
 * @param date2 日期2
 * @returns 相差天数
 */
export function getDaysDiff(date1: Date | string, date2: Date | string): number {
  const d1 = typeof date1 === 'string' ? new Date(date1) : date1
  const d2 = typeof date2 === 'string' ? new Date(date2) : date2

  const diff = d2.getTime() - d1.getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

/**
 * 获取某日期是当月第几周
 * @param date 日期
 * @returns 周数
 */
export function getWeekOfMonth(date: Date | string): number {
  const d = typeof date === 'string' ? new Date(date) : date
  const firstDay = new Date(d.getFullYear(), d.getMonth(), 1)
  const firstWeekday = firstDay.getDay() || 7
  return Math.ceil((d.getDate() + firstWeekday - 1) / 7)
}

/**
 * 获取某周的开始日期
 * @param date 日期
 * @returns 周开始日期
 */
export function getWeekStart(date: Date | string): Date {
  const d = typeof date === 'string' ? new Date(date) : date
  const day = d.getDay() || 7
  const weekStart = new Date(d)
  weekStart.setDate(d.getDate() - day + 1)
  return weekStart
}

/**
 * 获取某周的结束日期
 * @param date 日期
 * @returns 周结束日期
 */
export function getWeekEnd(date: Date | string): Date {
  const d = typeof date === 'string' ? new Date(date) : date
  const day = d.getDay() || 7
  const weekEnd = new Date(d)
  weekEnd.setDate(d.getDate() + (7 - day))
  return weekEnd
}

/**
 * 格式化截止日期（用于作业等）
 * @param dueDate 截止日期
 * @returns 截止日期文本
 */
export function formatDueDate(dueDate: Date | string | null): string {
  if (!dueDate) return '无截止日期'

  const d = typeof dueDate === 'string' ? new Date(dueDate) : dueDate
  const now = new Date()
  const diff = d.getTime() - now.getTime()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

  if (days < 0) {
    return '已过期'
  } else if (days === 0) {
    return '今天截止'
  } else if (days === 1) {
    return '明天截止'
  } else if (days <= 7) {
    return `${days}天后截止`
  } else {
    return formatDate(d, 'M月D日截止')
  }
}

/**
 * 获取剩余时间描述
 * @param targetDate 目标日期
 * @returns 剩余时间描述
 */
export function getTimeRemaining(targetDate: Date | string): string {
  const d = typeof targetDate === 'string' ? new Date(targetDate) : targetDate
  const now = new Date()
  const diff = d.getTime() - now.getTime()

  if (diff <= 0) return '已结束'

  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))

  if (days > 0) {
    return `${days}天${hours}小时`
  } else if (hours > 0) {
    return `${hours}小时${minutes}分钟`
  } else {
    return `${minutes}分钟`
  }
}
