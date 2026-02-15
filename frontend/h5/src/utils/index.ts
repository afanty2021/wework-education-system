/**
 * 工具函数
 */
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'

/**
 * 格式化日期
 */
export function formatDate(date: string | Date, format: string = 'YYYY-MM-DD'): string {
  return dayjs(date).format(format)
}

/**
 * 格式化时间
 */
export function formatTime(date: string | Date, format: string = 'HH:mm'): string {
  return dayjs(date).format(format)
}

/**
 * 格式化日期时间
 */
export function formatDateTime(date: string | Date, format: string = 'YYYY-MM-DD HH:mm'): string {
  return dayjs(date).format(format)
}

/**
 * 相对时间（如：3分钟前）
 */
export function fromNow(date: string | Date): string {
  return dayjs(date).locale('zh-cn').fromNow()
}

/**
 * 判断是否为今天
 */
export function isToday(date: string | Date): boolean {
  return dayjs(date).isSame(dayjs(), 'day')
}

/**
 * 判断是否为昨天
 */
export function isYesterday(date: string | Date): boolean {
  return dayjs(date).isSame(dayjs().subtract(1, 'day'), 'day')
}

/**
 * 获取星期几
 */
export function getWeekday(date: string | Date): string {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekdays[dayjs(date).day()]
}

/**
 * 获取星期几（完整）
 */
export function getWeekdayFull(date: string | Date): string {
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  return weekdays[dayjs(date).day()]
}

/**
 * 获取年龄
 */
export function getAge(birthday: string | Date): number {
  const birth = dayjs(birthday)
  const now = dayjs()
  let age = now.year() - birth.year()
  if (now.month() < birth.month() || (now.month() === birth.month() && now.date() < birth.date())) {
    age--
  }
  return age
}

/**
 * 格式化手机号
 */
export function formatPhone(phone: string): string {
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

/**
 * 格式化金额
 */
export function formatMoney(amount: number | string, decimals: number = 2): string {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount
  return '¥' + num.toFixed(decimals)
}

/**
 * 格式化数字（千分位）
 */
export function formatNumber(num: number | string): string {
  const n = typeof num === 'string' ? parseFloat(num) : num
  return n.toLocaleString('zh-CN')
}

/**
 * 节流函数
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastTime = 0
  return function (this: any, ...args: Parameters<T>) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}

/**
 * 防抖函数
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout> | null = null
  return function (this: any, ...args: Parameters<T>) {
    if (timer) {
      clearTimeout(timer)
    }
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * 深拷贝
 */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj))
}

/**
 * 判断对象是否为空
 */
export function isEmpty(obj: object): boolean {
  if (obj === null || obj === undefined) {
    return true
  }
  return Object.keys(obj).length === 0
}

/**
 * 获取数据类型
 */
export function getType(value: any): string {
  return Object.prototype.toString.call(value).slice(8, -1)
}

/**
 * 存储到本地
 */
export function setStorage(key: string, value: any): void {
  localStorage.setItem(key, JSON.stringify(value))
}

/**
 * 从本地读取
 */
export function getStorage<T>(key: string, defaultValue?: T): T | undefined {
  const item = localStorage.getItem(key)
  if (item) {
    try {
      return JSON.parse(item) as T
    } catch {
      return defaultValue
    }
  }
  return defaultValue
}

/**
 * 从本地删除
 */
export function removeStorage(key: string): void {
  localStorage.removeItem(key)
}

/**
 * 获取 URL 参数
 */
export function getUrlParam(name: string): string | null {
  const url = new URL(window.location.href)
  return url.searchParams.get(name)
}

/**
 * 设置 URL 参数
 */
export function setUrlParam(name: string, value: string): void {
  const url = new URL(window.location.href)
  url.searchParams.set(name, value)
  window.history.replaceState({}, '', url)
}

/**
 * 复制到剪贴板
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    return false
  }
}

/**
 * 下载文件
 */
export function downloadFile(url: string, filename: string): void {
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
}

/**
 * 微信环境判断
 */
export function isWeChat(): boolean {
  return /MicroMessenger/i.test(navigator.userAgent)
}

/**
 * 移动端判断
 */
export function isMobile(): boolean {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  )
}

/**
 * 企业微信判断
 */
export function isWeWork(): boolean {
  return /wxwork/i.test(navigator.userAgent)
}
