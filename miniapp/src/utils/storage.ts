/**
 * 本地存储工具函数
 */

/**
 * 存储数据
 * @param key 键
 * @param value 值
 */
export function setStorage(key: string, value: unknown): void {
  try {
    uni.setStorageSync(key, JSON.stringify(value))
  } catch (error) {
    console.error('存储数据失败:', error)
  }
}

/**
 * 获取数据
 * @param key 键
 * @param defaultValue 默认值
 * @returns 值
 */
export function getStorage<T>(key: string, defaultValue?: T): T | undefined {
  try {
    const data = uni.getStorageSync(key)
    if (!data) return defaultValue

    if (typeof data === 'string') {
      return JSON.parse(data) as T
    }
    return data as T
  } catch (error) {
    console.error('读取数据失败:', error)
    return defaultValue
  }
}

/**
 * 删除数据
 * @param key 键
 */
export function removeStorage(key: string): void {
  try {
    uni.removeStorageSync(key)
  } catch (error) {
    console.error('删除数据失败:', error)
  }
}

/**
 * 清空所有存储
 */
export function clearStorage(): void {
  try {
    uni.clearStorageSync()
  } catch (error) {
    console.error('清空存储失败:', error)
  }
}

/**
 * 检查键是否存在
 * @param key 键
 * @returns 是否存在
 */
export function hasStorage(key: string): boolean {
  try {
    uni.getStorageInfoSync().keys.includes(key)
    return uni.getStorageInfoSync().keys.includes(key)
  } catch {
    return false
  }
}

/**
 * 获取存储信息
 * @returns 存储信息
 */
export function getStorageInfo(): { currentSize: number; limitSize: number } {
  try {
    const info = uni.getStorageInfoSync()
    return {
      currentSize: info.currentSize,
      limitSize: info.limitSize
    }
  } catch {
    return {
      currentSize: 0,
      limitSize: 0
    }
  }
}

/**
 * 存储认证Token
 * @param token Token
 */
export function setToken(token: string): void {
  setStorage('auth_token', token)
}

/**
 * 获取认证Token
 * @returns Token
 */
export function getToken(): string | null {
  return getStorage<string>('auth_token') || null
}

/**
 * 删除认证Token
 */
export function removeToken(): void {
  removeStorage('auth_token')
}

/**
 * 存储用户信息
 * @param userInfo 用户信息
 */
export function setUserInfo(userInfo: Record<string, unknown>): void {
  setStorage('user_info', userInfo)
}

/**
 * 获取用户信息
 * @returns 用户信息
 */
export function getUserInfo<T = Record<string, unknown>>(): T | null {
  return getStorage<T>('user_info') || null
}

/**
 * 删除用户信息
 */
export function removeUserInfo(): void {
  removeStorage('user_info')
}

/**
 * 存储应用设置
 * @param settings 设置
 */
export function setAppSettings(settings: Record<string, unknown>): void {
  setStorage('app_settings', settings)
}

/**
 * 获取应用设置
 * @returns 应用设置
 */
export function getAppSettings<T = Record<string, unknown>>(): T | null {
  return getStorage<T>('app_settings') || null
}

/**
 * 清除所有应用数据
 */
export function clearAppData(): void {
  clearStorage()
}

/**
 * 存储搜索历史
 * @param key 搜索关键词
 * @param maxCount 最大保存数量
 */
export function addSearchHistory(key: string, maxCount: number = 20): void {
  const history = getSearchHistory<string[]>() || []
  const index = history.indexOf(key)

  // 如果已存在，移除旧位置
  if (index !== -1) {
    history.splice(index, 1)
  }

  // 添加到开头
  history.unshift(key)

  // 限制数量
  if (history.length > maxCount) {
    history.splice(maxCount)
  }

  setStorage('search_history', history)
}

/**
 * 获取搜索历史
 * @returns 搜索历史
 */
export function getSearchHistory<T = string[]>(): T | null {
  return getStorage<T>('search_history') || null
}

/**
 * 清空搜索历史
 */
export function clearSearchHistory(): void {
  removeStorage('search_history')
}

/**
 * 存储浏览历史
 * @param key 页面标识
 * @param data 页面数据
 * @param maxCount 最大保存数量
 */
export function addBrowseHistory(key: string, data: Record<string, unknown>, maxCount: number = 50): void {
  const history = getBrowseHistory<Array<{ key: string; data: Record<string, unknown>; time: number }>>() || []

  // 检查是否已存在
  const index = history.findIndex(item => item.key === key)
  if (index !== -1) {
    history.splice(index, 1)
  }

  // 添加到开头
  history.unshift({
    key,
    data,
    time: Date.now()
  })

  // 限制数量
  if (history.length > maxCount) {
    history.splice(maxCount)
  }

  setStorage('browse_history', history)
}

/**
 * 获取浏览历史
 * @returns 浏览历史
 */
export function getBrowseHistory<T = Array<{ key: string; data: Record<string, unknown>; time: number }>>(): T | null {
  return getStorage<T>('browse_history') || null
}

/**
 * 清空浏览历史
 */
export function clearBrowseHistory(): void {
  removeStorage('browse_history')
}
