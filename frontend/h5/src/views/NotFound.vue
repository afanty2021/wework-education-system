<template>
  <div class="not-found-page">
    <van-icon name="warning-o" size="80" color="#999" />
    <h2>页面不存在</h2>
    <p>您访问的页面不存在或已被移除</p>
    <van-button type="primary" @click="goHome">返回首页</van-button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/')
}
</script>

<style lang="scss" scoped>
.not-found-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  text-align: center;

  h2 {
    font-size: 24px;
    margin: 20px 0 12px;
  }

  p {
    color: #999;
    margin: 0 0 24px;
  }
}
</style>
