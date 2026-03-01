<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import SvgIcon from '@/components/SvgIcon.vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 登录方式
const loginType = ref<'wework' | 'password'>('wework')

// 企业微信登录相关
const weworkQrcodeUrl = ref('')
const weworkAuthUrl = ref('')
const weworkLoading = ref(true)

// 账号密码登录表单
const formData = ref({
  username: '',
  password: '',
  remember: false,
})

const formRef = ref()
const loading = ref(false)

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在2-20个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在6-20个字符', trigger: 'blur' },
  ],
}

// 获取企业微信登录二维码
async function getWeWorkQrcode(): Promise<void> {
  try {
    weworkLoading.value = true
    const response = await axios.get('/api/v1/auth/wework/url')
    weworkAuthUrl.value = response.data.auth_url

    // 使用公共二维码生成服务将 URL 转为二维码
    weworkQrcodeUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(response.data.auth_url)}`

    // 轮询检查是否有回调（通过检查 URL 参数或 token）
    startPolling()
  } catch (error) {
    console.error('获取登录二维码失败:', error)
    ElMessage.error('获取登录二维码失败，请稍后重试')
    weworkLoading.value = false
  } finally {
    weworkLoading.value = false
  }
}

// 轮询检查登录状态
let pollTimer: ReturnType<typeof setInterval> | null = null
function startPolling(): void {
  stopPolling()
  pollTimer = setInterval(async () => {
    // 检查 URL 参数中是否有 code（企业微信回调）
    const urlParams = new URLSearchParams(window.location.search)
    const code = urlParams.get('code')
    const state = urlParams.get('state')

    if (code) {
      try {
        await handleWeworkCallback(code, state)
      } catch (error) {
        console.error('登录失败:', error)
      }
    }
  }, 2000)
}

function stopPolling(): void {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

// 处理企业微信回调
async function handleWeworkCallback(code: string, state: string | null): Promise<void> {
  try {
    const response = await axios.post('/api/v1/auth/wework', { code })
    userStore.setToken(response.data.access_token)
    await userStore.fetchUserInfo()

    ElMessage.success('登录成功')
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)

    // 清除 URL 参数
    window.history.replaceState({}, document.title, window.location.pathname)
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.detail || '登录失败，请重试')
  }
}

// 账号密码登录
async function handlePasswordLogin(): Promise<void> {
  // 跳过表单验证，直接尝试登录
  if (!formData.value.username || !formData.value.password) {
    ElMessage.error('请输入用户名和密码')
    return
  }

  try {
    loading.value = true

    // 调用后端账号密码登录接口
    const response = await axios.post('/api/v1/auth/login', {
      username: formData.value.username,
      password: formData.value.password,
    })
    userStore.setToken(response.data.access_token)
    await userStore.fetchUserInfo()

    ElMessage.success('登录成功')
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '登录失败')
  } finally {
    loading.value = false
  }
}

// 切换登录方式
function switchLoginType(type: 'wework' | 'password'): void {
  loginType.value = type
  if (type === 'wework') {
    getWeWorkQrcode()
  } else {
    stopPolling()
  }
}

// 重置表单
function resetForm(): void {
  formRef.value?.resetFields()
}

onMounted(() => {
  // 如果已登录，跳转到首页
  if (userStore.isLoggedIn) {
    router.push('/')
  } else {
    // 检查是否有回调参数
    const urlParams = new URLSearchParams(window.location.search)
    const code = urlParams.get('code')
    if (code) {
      handleWeworkCallback(code, urlParams.get('state'))
    } else {
      // 默认显示企业微信登录
      switchLoginType('wework')
    }
  }
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧Logo区域 -->
      <div class="login-left">
        <div class="logo-area">
          <SvgIcon name="education" size="80" color="#fff" />
          <h1 class="system-title">教务管理系统</h1>
          <p class="system-subtitle">Enterprise Education Management System</p>
        </div>
      </div>

      <!-- 右侧登录区域 -->
      <div class="login-right">
        <div class="login-form-container">
          <!-- 登录方式切换 -->
          <div class="login-type-switch">
            <span
              :class="{ active: loginType === 'wework' }"
              @click="switchLoginType('wework')"
            >
              企业微信
            </span>
            <span class="divider">|</span>
            <span
              :class="{ active: loginType === 'password' }"
              @click="switchLoginType('password')"
            >
              账号密码
            </span>
          </div>

          <!-- 企业微信登录 -->
          <transition name="fade">
            <div v-if="loginType === 'wework'" class="wework-login">
              <div class="qrcode-area">
                <div v-if="weworkQrcodeUrl && !weworkLoading" class="qrcode">
                  <img :src="weworkQrcodeUrl" alt="企业微信登录二维码" />
                </div>
                <div v-else class="qrcode-loading">
                  <el-icon :size="48" class="is-loading">
                    <Loading />
                  </el-icon>
                  <p>加载中...</p>
                </div>
              </div>
              <p class="login-tip">请使用企业微信扫码登录</p>
            </div>
          </transition>

          <!-- 账号密码登录 -->
          <transition name="fade">
            <el-form
              v-if="loginType === 'password'"
              ref="formRef"
              :model="formData"
              :rules="rules"
              class="login-form"
              size="large"
            >
              <el-form-item prop="username">
                <el-input
                  v-model="formData.username"
                  placeholder="请输入用户名"
                  prefix-icon="User"
                  clearable
                />
              </el-form-item>

              <el-form-item prop="password">
                <el-input
                  v-model="formData.password"
                  type="password"
                  placeholder="请输入密码"
                  prefix-icon="Lock"
                  show-password
                />
              </el-form-item>

              <el-form-item>
                <div class="form-options">
                  <el-checkbox v-model="formData.remember">记住我</el-checkbox>
                  <el-link type="primary" :underline="false">忘记密码?</el-link>
                </div>
              </el-form-item>

              <el-form-item>
                <el-button
                  type="primary"
                  :loading="loading"
                  class="login-btn"
                  @click="handlePasswordLogin"
                >
                  登 录
                </el-button>
              </el-form-item>

              <el-form-item>
                <el-button class="reset-btn" @click="resetForm">重 置</el-button>
              </el-form-item>
            </el-form>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  display: flex;
  width: 900px;
  height: 540px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.login-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 450px;
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;

  .logo-area {
    text-align: center;
  }

  .system-title {
    margin-top: 24px;
    font-size: 28px;
    font-weight: 600;
    letter-spacing: 2px;
  }

  .system-subtitle {
    margin-top: 8px;
    font-size: 14px;
    opacity: 0.8;
    letter-spacing: 4px;
  }
}

.login-right {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.login-form-container {
  width: 100%;
  max-width: 320px;
}

.login-type-switch {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 32px;
  font-size: 16px;
  color: #999;

  span {
    cursor: pointer;
    transition: color 0.3s;

    &.active {
      color: #667eea;
      font-weight: 600;
    }

    &:hover:not(.divider) {
      color: #667eea;
    }
  }

  .divider {
    margin: 0 16px;
    color: #ddd;
    cursor: default;
  }
}

.wework-login {
  text-align: center;

  .qrcode-area {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 200px;
    height: 200px;
    margin: 0 auto 24px;
    background: #f5f7fa;
    border-radius: 8px;

    .qrcode {
      img {
        width: 180px;
        height: 180px;
      }
    }

    .qrcode-loading {
      display: flex;
      flex-direction: column;
      align-items: center;
      color: #999;
    }
  }

  .login-tip {
    font-size: 14px;
    color: #666;
  }
}

.login-form {
  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }

  .login-btn {
    width: 100%;
    height: 44px;
    font-size: 16px;
    letter-spacing: 4px;
  }

  .reset-btn {
    width: 100%;
    height: 44px;
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 响应式
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
    width: 90%;
    height: auto;
  }

  .login-left {
    width: 100%;
    padding: 30px;
  }

  .login-right {
    padding: 30px;
  }
}
</style>
