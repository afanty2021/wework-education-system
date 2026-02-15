<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

// 登录状态
const loading = ref(false)
const errorMessage = ref('')

/**
 * 微信登录
 */
async function onWechatLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    // 获取微信登录凭证
    const loginRes = await uni.login({
      provider: 'weixin',
      success: async (res) => {
        // 获取用户信息
        const userInfoRes = await uni.getUserProfile({
          provider: 'weixin',
          desc: '用于完善用户资料',
          success: (userInfo) => {
            return userInfo
          },
          fail: (err) => {
            console.warn('获取用户信息失败:', err)
            // 用户拒绝授权时仍然可以登录
            return null
          }
        })

        // 执行登录
        try {
          await userStore.wechatLogin(res.code, userInfoRes)
          router.push('/pages/index/index')
        } catch (loginError) {
          errorMessage.value = '登录失败，请稍后重试'
        }
      },
      fail: (err) => {
        console.error('微信登录失败:', err)
        errorMessage.value = '微信登录失败，请检查网络设置'
      }
    })
  } catch (error) {
    console.error('登录过程出错:', error)
    errorMessage.value = '登录过程出错，请稍后重试'
  } finally {
    loading.value = false
  }
}

/**
 * 游客模式
 */
function onGuestMode() {
  router.push('/pages/index/index')
}
</script>

<template>
  <view class="login-container">
    <!-- Logo区域 -->
    <view class="logo-area">
      <image class="logo" src="/static/images/logo.png" mode="aspectFit" />
      <view class="app-name">教务管理系统</view>
      <view class="app-slogan">便捷的家校互动平台</view>
    </view>

    <!-- 登录区域 -->
    <view class="login-area">
      <!-- 错误提示 -->
      <view class="error-tip" v-if="errorMessage">
        {{ errorMessage }}
      </view>

      <!-- 微信登录按钮 -->
      <button
        class="wechat-btn"
        :disabled="loading"
        @click="onWechatLogin"
      >
        <image class="wechat-icon" src="/static/images/wechat.png" mode="aspectFit" />
        <text v-if="loading">登录中...</text>
        <text v-else>微信一键登录</text>
      </button>

      <!-- 游客模式 -->
      <view class="guest-mode" @click="onGuestMode">
        <text>暂不登录，先看看</text>
      </view>
    </view>

    <!-- 协议区域 -->
    <view class="agreement-area">
      <text class="agreement-text">
        登录即表示同意
        <text class="link">《用户服务协议》</text>
        和
        <text class="link">《隐私政策》</text>
      </text>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-color: #ffffff;
  padding: 0 60rpx;
}

.logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 200rpx;
  margin-bottom: 100rpx;

  .logo {
    width: 200rpx;
    height: 200rpx;
    margin-bottom: 32rpx;
  }

  .app-name {
    font-size: 48rpx;
    font-weight: 700;
    color: #303133;
    margin-bottom: 16rpx;
  }

  .app-slogan {
    font-size: 28rpx;
    color: #909399;
  }
}

.login-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;

  .error-tip {
    width: 100%;
    padding: 20rpx;
    margin-bottom: 32rpx;
    background-color: #fff2f0;
    color: #ff4d4f;
    font-size: 28rpx;
    text-align: center;
    border-radius: 8rpx;
  }

  .wechat-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100rpx;
    background-color: #07c160;
    color: #ffffff;
    font-size: 34rpx;
    font-weight: 500;
    border-radius: 50rpx;
    border: none;
    margin-bottom: 32rpx;

    .wechat-icon {
      width: 48rpx;
      height: 48rpx;
      margin-right: 16rpx;
    }

    &:disabled {
      opacity: 0.7;
    }
  }

  .guest-mode {
    padding: 20rpx;
    color: #909399;
    font-size: 28rpx;
  }
}

.agreement-area {
  position: absolute;
  bottom: 60rpx;
  left: 0;
  right: 0;
  padding: 0 40rpx;
  text-align: center;

  .agreement-text {
    font-size: 24rpx;
    color: #909399;

    .link {
      color: #1890ff;
    }
  }
}
</style>
