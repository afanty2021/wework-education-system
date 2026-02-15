<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Logo 和标题 -->
      <div class="login-header">
        <div class="logo">
          <img src="@/assets/logo.png" alt="Logo" />
        </div>
        <h1 class="title">企业微信教务系统</h1>
        <p class="subtitle">教师端</p>
      </div>

      <!-- 登录表单 -->
      <van-form @submit="handleLogin" class="login-form">
        <van-field
          v-model="form.username"
          name="username"
          label="用户名"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请输入用户名' }]"
          left-icon="user-o"
        />
        <van-field
          v-model="form.password"
          type="password"
          name="password"
          label="密码"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请输入密码' }]"
          left-icon="lock"
        />
        <div class="login-actions">
          <van-button round block type="primary" native-type="submit" :loading="loading">
            登录
          </van-button>
        </div>
      </van-form>

      <!-- 分隔线 -->
      <div class="divider">
        <span>或</span>
      </div>

      <!-- 企业微信登录 -->
      <div class="wework-login">
        <van-button round block plain type="primary" @click="handleWeWorkLogin">
          <template #icon>
            <van-icon name="https://res.wx.qq.com/wxdoc/dist/assets/img/logo.4f4cf2d.svg" size="20" />
          </template>
          企业微信一键登录
        </van-button>
      </div>

      <!-- 版权信息 -->
      <div class="copyright">
        <p>登录即表示同意</p>
        <p>
          <a href="#">服务条款</a> 和 <a href="#">隐私政策</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showFail, showSuccess } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 表单数据
const form = reactive({
  username: '',
  password: '',
})

// 加载状态
const loading = ref(false)

/**
 * 处理用户名密码登录
 */
async function handleLogin() {
  loading.value = true
  try {
    const result = await authStore.loginAction({
      username: form.username,
      password: form.password,
    })
    if (result.success) {
      showSuccess('登录成功')
      const redirect = route.query.redirect as string
      router.push(redirect || '/')
    } else {
      showFail(result.error || '登录失败')
    }
  } catch (error) {
    showFail('登录失败，请检查网络')
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 处理企业微信登录
 */
function handleWeWorkLogin() {
  showFail('企业微信登录功能开发中')
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  padding: 40px 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  .logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 16px;

    img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
  }

  .title {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin: 0 0 8px;
  }

  .subtitle {
    font-size: 14px;
    color: #999;
    margin: 0;
  }
}

.login-form {
  margin-bottom: 20px;

  :deep(.van-field) {
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    background: #f5f5f5;
  }
}

.login-actions {
  margin-top: 24px;

  .van-button {
    height: 44px;
    font-size: 16px;
  }
}

.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e5e5e5;
  }

  span {
    padding: 0 16px;
    font-size: 14px;
    color: #999;
  }
}

.wework-login {
  .van-button {
    height: 44px;
    font-size: 16px;
  }
}

.copyright {
  margin-top: 32px;
  text-align: center;
  font-size: 12px;
  color: #999;

  p {
    margin: 4px 0;
  }

  a {
    color: #1989fa;
    text-decoration: none;
  }
}
</style>
