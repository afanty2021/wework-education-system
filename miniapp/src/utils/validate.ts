/**
 * 表单验证工具函数
 */

/**
 * 验证手机号
 * @param phone 手机号
 * @returns 是否有效
 */
export function validatePhone(phone: string): boolean {
  const reg = /^1[3-9]\d{9}$/
  return reg.test(phone)
}

/**
 * 验证邮箱
 * @param email 邮箱
 * @returns 是否有效
 */
export function validateEmail(email: string): boolean {
  const reg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return reg.test(email)
}

/**
 * 验证身份证号
 * @param idCard 身份证号
 * @returns 是否有效
 */
export function validateIdCard(idCard: string): boolean {
  const reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
  return reg.test(idCard)
}

/**
 * 验证姓名
 * @param name 姓名
 * @returns 是否有效
 */
export function validateName(name: string): boolean {
  const reg = /^[\u4e00-\u9fa5]{2,10}$/
  return reg.test(name)
}

/**
 * 验证密码强度
 * @param password 密码
 * @returns 强度等级 (0-4)
 */
export function validatePasswordStrength(password: string): number {
  if (!password || password.length < 6) return 0

  let strength = 0

  // 长度至少8位
  if (password.length >= 8) strength++

  // 包含数字
  if (/\d/.test(password)) strength++

  // 包含小写字母
  if (/[a-z]/.test(password)) strength++

  // 包含大写字母
  if (/[A-Z]/.test(password)) strength++

  // 包含特殊字符
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++

  return Math.min(strength, 4)
}

/**
 * 验证URL
 * @param url URL地址
 * @returns 是否有效
 */
export function validateUrl(url: string): boolean {
  const reg = /^https?:\/\/([\w-]+\.)+[\w-]+(\/[\w-./?%&=]*)?$/
  return reg.test(url)
}

/**
 * 验证微信号
 * @param wechat 微信号
 * @returns 是否有效
 */
export function validateWechat(wechat: string): boolean {
  const reg = /^[a-zA-Z][a-zA-Z0-9_-]{5,19}$/
  return reg.test(wechat)
}

/**
 * 验证金额
 * @param amount 金额
 * @returns 是否有效
 */
export function validateAmount(amount: string | number): boolean {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(num) || num < 0) return false

  const reg = /^\d+(\.\d{1,2})?$/
  return reg.test(String(num))
}

/**
 * 验证课时数
 * @param hours 课时数
 * @returns 是否有效
 */
export function validateHours(hours: string | number): boolean {
  const num = typeof hours === 'string' ? parseFloat(hours) : hours
  if (isNaN(num) || num <= 0) return false
  return num <= 999
}

/**
 * 验证年龄
 * @param age 年龄
 * @returns 是否有效
 */
export function validateAge(age: string | number): boolean {
  const num = typeof age === 'string' ? parseInt(age) : age
  if (isNaN(num)) return false
  return num >= 0 && num <= 150
}

/**
 * 验证年级
 * @param grade 年级
 * @returns 是否有效
 */
export function validateGrade(grade: string | number): boolean {
  const num = typeof grade === 'string' ? parseInt(grade) : grade
  if (isNaN(num)) return false
  return num >= 1 && num <= 12
}

/**
 * 验证邮政编码
 * @param postalCode 邮政编码
 * @returns 是否有效
 */
export function validatePostalCode(postalCode: string): boolean {
  const reg = /^\d{6}$/
  return reg.test(postalCode)
}

/**
 * 验证必填项
 * @param value 值
 * @returns 是否有效
 */
export function validateRequired(value: unknown): boolean {
  if (value === null || value === undefined) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (typeof value === 'number') return true
  if (typeof value === 'boolean') return true
  return false
}

/**
 * 验证字符串长度
 * @param str 字符串
 * @param min 最小长度
 * @param max 最大长度
 * @returns 是否有效
 */
export function validateLength(str: string, min: number, max: number): boolean {
  const len = str.trim().length
  return len >= min && len <= max
}

/**
 * 验证数组长度
 * @param arr 数组
 * @param min 最小长度
 * @param max 最大长度
 * @returns 是否有效
 */
export function validateArrayLength(arr: unknown[], min: number, max: number): boolean {
  return arr.length >= min && arr.length <= max
}

/**
 * 获取验证错误信息
 * @param value 值
 * @param field 字段名
 * @param rules 验证规则
 * @returns 错误信息或null
 */
export function getValidationError(
  value: unknown,
  field: string,
  rules: Record<string, unknown>
): string | null {
  if (rules.required && !validateRequired(value)) {
    return `${field}不能为空`
  }

  if (rules.phone && typeof value === 'string' && !validatePhone(value)) {
    return `请输入正确的${field}`
  }

  if (rules.email && typeof value === 'string' && !validateEmail(value)) {
    return `请输入正确的${field}`
  }

  if (rules.minLength && typeof value === 'string' && value.length < rules.minLength) {
    return `${field}长度不能少于${rules.minLength}个字符`
  }

  if (rules.maxLength && typeof value === 'string' && value.length > rules.maxLength) {
    return `${field}长度不能超过${rules.maxLength}个字符`
  }

  return null
}
