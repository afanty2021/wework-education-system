<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 获取错误信息
const errorMessage = computed(() => {
  const status = route.query.status || route.query.code || '404'
  const messages: Record<string, string> = {
    '403': '抱歉，您没有权限访问此页面',
    '404': '抱歉，您访问的页面不存在',
    '500': '抱歉，服务器出了点问题',
  }
  return messages[status as string] || '未知错误'
})

// 返回首页
function goHome(): void {
  router.push('/')
}

// 返回上一页
function goBack(): void {
  router.go(-1)
}
</script>

<template>
  <div class="error-page">
    <div class="error-content">
      <div class="error-code">{{ route.query.status || route.query.code || '404' }}</div>
      <div class="error-message">{{ errorMessage }}</div>
      <div class="error-actions">
        <el-button type="primary" @click="goHome">返回首页</el-button>
        <el-button @click="goBack">返回上一页</el-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'ErrorPage',
  setup() {
    const route = useRoute()
    const router = useRouter()

    const errorMessage = computed(() => {
      const status = route.query.status || route.query.code || '404'
      const messages: Record<string, string> = {
        '403': '抱歉，您没有权限访问此页面',
        '404': '抱歉，您访问的页面不存在',
        '500': '抱歉，服务器出了点问题',
      }
      return messages[status as string] || '未知错误'
    })

    function goHome() {
      router.push('/')
    }

    function goBack() {
      router.go(-1)
    }

    return {
      errorMessage,
      goHome,
      goBack,
    }
  },
})
</script>

<style lang="scss" scoped>
.error-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: var(--el-bg-color);
}

.error-content {
  text-align: center;

  .error-code {
    font-size: 120px;
    font-weight: bold;
    color: var(--el-color-primary);
    line-height: 1;
    margin-bottom: 20px;
  }

  .error-message {
    font-size: 18px;
    color: var(--el-text-color-secondary);
    margin-bottom: 30px;
  }

  .error-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
  }
}
</style>
