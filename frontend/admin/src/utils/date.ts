/**
 * 日期工具函数
 */
import dayjs, { type Dayjs } from 'dayjs'

/**
 * 格式化日期
 */
export function formatDate(
  date: Date | string | Dayjs | null | undefined,
  format: string = 'YYYY-MM-DD'
): string {
  if (!date) return ''
  return dayjs(date).format(format)
}

/**
 * 解析日期
 */
export function parseDate(date: string | Date): Date {
  return dayjs(date).toDate()
}

/**
 * 获取相对时间
 */
export function fromNow(date: Date | string | Dayjs | null | undefined): string {
  if (!date) return ''
  return dayjs(date).fromNow()
}

/**
 * 判断是否今天
 */
export function isToday(date: Date | string | Dayjs | null | undefined): boolean {
  if (!date) return false
  return dayjs(date).isSame(dayjs(), 'day')
}

/**
 * 判断是否过期
 */
export function isExpired(date: Date | string | Dayjs | null | undefined): boolean {
  if (!date) return false
  return dayjs(date).isBefore(dayjs())
}
