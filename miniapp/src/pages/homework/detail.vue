<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useHomeworkStore } from '@/stores/homework'
import type { Homework } from '@/api/homework'

const route = useRoute()
const homeworkStore = useHomeworkStore()

// 页面状态
const loading = ref(true)
const submitting = ref(false)
const homework = ref<Homework | null>(null)
const submissionContent = ref('')

// 作业ID
const homeworkId = computed(() => parseInt(route.query.id as string) || 0)

/**
 * 加载作业详情
 */
async function loadHomeworkDetail() {
  if (!homeworkId.value) {
    uni.showToast({
      title: '参数错误',
      icon: 'error'
    })
    return
  }

  loading.value = true
  try {
    homework.value = await homeworkStore.fetchHomeworkDetail(homeworkId.value)
  } catch (error) {
    console.error('加载作业详情失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 格式化日期
 */
function formatDate(date: string | null): string {
  if (!date) return '无截止日期'
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 获取截止日期状态
 */
function getDueDateStatus(date: string | null): { text: string; color: string } {
  if (!date) return { text: '无截止日期', color: '#909399' }
  const dueDate = new Date(date)
  const now = new Date()
  const diff = dueDate.getTime() - now.getTime()
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

  if (days < 0) {
    return { text: '已过期', color: '#ff4d4f' }
  } else if (days <= 1) {
    return { text: `剩余${days}天`, color: '#faad14' }
  } else {
    return { text: `剩余${days}天`, color: '#52c41a' }
  }
}

/**
 * 提交作业
 */
async function submitHomework() {
  if (!submissionContent.value.trim()) {
    uni.showToast({
      title: '请输入作业内容',
      icon: 'none'
    })
    return
  }

  submitting.value = true
  try {
    await homeworkStore.submitHomework(homeworkId.value, submissionContent.value)
    uni.showToast({
      title: '提交成功',
      icon: 'success'
    })
    // 刷新详情
    await loadHomeworkDetail()
  } catch (error) {
    console.error('提交作业失败:', error)
    uni.showToast({
      title: '提交失败',
      icon: 'error'
    })
  } finally {
    submitting.value = false
  }
}

/**
 * 选择图片
 */
function chooseImage() {
  uni.chooseImage({
    count: 9,
    success: (res) => {
      // TODO: 上传图片到服务器
      uni.showToast({
        title: `选择了${res.tempFilePaths.length}张图片`,
        icon: 'none'
      })
    }
  })
}

onMounted(() => {
  loadHomeworkDetail()
})
</script>

<template>
  <view class="homework-detail-container" v-if="homework">
    <!-- 作业信息 -->
    <view class="homework-info">
      <view class="header">
        <text class="title">{{ homework.title }}</text>
        <view class="status-tag" :class="homework.submission ? 'submitted' : 'pending'">
          {{ homework.submission ? (homework.submission.score !== null ? '已批改' : '已提交') : '待提交' }}
        </view>
      </view>

      <view class="course-name">{{ homework.course_name || `课程ID: ${homework.course_id}` }}</view>
    </view>

    <!-- 作业内容 -->
    <view class="content-card">
      <view class="card-title">作业内容</view>
      <view class="content-text">{{ homework.content }}</view>
    </view>

    <!-- 截止日期 -->
    <view class="info-card">
      <view class="info-row">
        <text class="label">截止时间</text>
        <text class="value" :style="{ color: getDueDateStatus(homework.due_date).color }">
          {{ formatDate(homework.due_date) }}
        </text>
      </view>
      <view class="info-row" v-if="homework.max_score">
        <text class="label">满分</text>
        <text class="value">{{ homework.max_score }}分</text>
      </view>
    </view>

    <!-- 已提交内容 -->
    <view class="submission-card" v-if="homework.submission">
      <view class="card-title">我的提交</view>
      <view class="submission-content">{{ homework.submission.content }}</view>

      <!-- 批改信息 -->
      <view class="grading-info" v-if="homework.submission.score !== null">
        <view class="score">
          <text class="label">得分</text>
          <text class="value">{{ homework.submission.score }}分</text>
        </view>
        <view class="remark" v-if="homework.submission.teacher_remark">
          <text class="label">教师评语</text>
          <text class="value">{{ homework.submission.teacher_remark }}</text>
        </view>
      </view>

      <view class="submit-time">
        提交时间：{{ formatDate(homework.submission.submitted_at) }}
      </view>
    </view>

    <!-- 提交作业表单 -->
    <view class="submit-form" v-else>
      <view class="card-title">提交作业</view>
      <textarea
        class="content-input"
        v-model="submissionContent"
        placeholder="请输入作业内容..."
        :maxlength="-1"
      />

      <view class="attach-area">
        <view class="attach-btn" @click="chooseImage">
          <text class="icon">+</text>
          <text>添加图片</text>
        </view>
      </view>

      <button
        class="submit-btn"
        :disabled="submitting"
        @click="submitHomework"
      >
        {{ submitting ? '提交中...' : '提交作业' }}
      </button>
    </view>
  </view>

  <!-- 加载状态 -->
  <view class="loading-state" v-else-if="loading">
    <text>加载中...</text>
  </view>
</template>

<style lang="scss" scoped>
.homework-detail-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20rpx;
  padding-bottom: 200rpx;
}

.homework-info {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16rpx;

    .title {
      font-size: 36rpx;
      font-weight: 600;
      color: #303133;
      flex: 1;
    }

    .status-tag {
      font-size: 24rpx;
      padding: 8rpx 16rpx;
      border-radius: 8rpx;

      &.pending {
        background-color: #fff2f0;
        color: #ff4d4f;
      }

      &.submitted {
        background-color: #e6f7ff;
        color: #1890ff;
      }
    }
  }

  .course-name {
    font-size: 28rpx;
    color: #909399;
  }
}

.content-card,
.submission-card,
.submit-form {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;

  .card-title {
    font-size: 30rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 20rpx;
  }
}

.content-text {
  font-size: 28rpx;
  color: #606266;
  line-height: 1.8;
}

.info-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;

  .info-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16rpx 0;

    &:not(:last-child) {
      border-bottom: 2rpx solid #f5f5f5;
    }

    .label {
      font-size: 28rpx;
      color: #909399;
    }

    .value {
      font-size: 28rpx;
      color: #303133;
    }
  }
}

.submission-content {
  font-size: 28rpx;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 20rpx;
}

.grading-info {
  background-color: #fafafa;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;

  .score {
    display: flex;
    align-items: center;
    margin-bottom: 12rpx;

    .label {
      font-size: 28rpx;
      color: #909399;
      margin-right: 16rpx;
    }

    .value {
      font-size: 36rpx;
      font-weight: 600;
      color: #52c41a;
    }
  }

  .remark {
    .label {
      font-size: 28rpx;
      color: #909399;
      margin-right: 16rpx;
    }

    .value {
      font-size: 28rpx;
      color: #606266;
    }
  }
}

.submit-time {
  font-size: 24rpx;
  color: #909399;
}

.content-input {
  width: 100%;
  min-height: 200rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #303133;
  background-color: #f5f5f5;
  border-radius: 12rpx;
  box-sizing: border-box;
}

.attach-area {
  margin-top: 20rpx;

  .attach-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 160rpx;
    height: 160rpx;
    background-color: #f5f5f5;
    border-radius: 12rpx;
    border: 2rpx dashed #d9d9d9;

    .icon {
      font-size: 48rpx;
      color: #909399;
      margin-right: 8rpx;
    }

    text {
      font-size: 24rpx;
      color: #909399;
    }
  }
}

.submit-btn {
  margin-top: 32rpx;
  height: 88rpx;
  line-height: 88rpx;
  background-color: #1890ff;
  color: #ffffff;
  font-size: 32rpx;
  border-radius: 44rpx;
  border: none;

  &:disabled {
    opacity: 0.7;
  }
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400rpx;
  font-size: 28rpx;
  color: #909399;
}
</style>
