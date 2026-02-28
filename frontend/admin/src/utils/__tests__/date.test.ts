/**
 * 日期工具函数测试
 */
import { describe, it, expect } from 'vitest'
import { formatDate, parseDate } from '../date'

describe('日期工具', () => {
  it('formatDate should format date correctly', () => {
    const date = new Date('2024-01-15T10:30:00')
    expect(formatDate(date)).toBe('2024-01-15')
    expect(formatDate(date, 'YYYY-MM-DD HH:mm')).toBe('2024-01-15 10:30')
  })

  it('parseDate should parse date string correctly', () => {
    const result = parseDate('2024-01-15')
    expect(result.getFullYear()).toBe(2024)
    expect(result.getMonth()).toBe(0)
    expect(result.getDate()).toBe(15)
  })
})
