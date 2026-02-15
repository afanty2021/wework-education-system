import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import uviewPlus from 'uview-plus'

import App from './App.vue'

/**
 * 创建Vue应用实例
 */
export function createApp() {
  const app = createSSRApp(App)
  const pinia = createPinia()

  // 使用Pinia状态管理
  app.use(pinia)

  // 使用uView UI组件库
  app.use(uviewPlus)

  return {
    app,
    pinia
  }
}
