<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLeaveStore } from '@/stores/leave'
import { useScheduleStore } from '@/stores/schedule'
import type { Schedule } from '@/api/schedule'

const leaveStore = useLeaveStore()
const scheduleStore = useScheduleStore()

// 页面状态
const loading = ref(false)
const selectedSchedule = ref<Schedule | null>(null)
const leaveDate = ref('')
const leaveHours = ref(1)
const reason = ref('')

// 表单验证
const formError = ref('')

/**
 * 初始化
 */
async function init() {
  try {
    // 获取今日课表作为可选课程
    await scheduleStore.fetchTodaySchedules()
  } catch (error) {
    console.error('加载课表失败:', error)
  }
}

/**
 * 选择课程
 */
function selectSchedule(schedule: Schedule) {
  selectedSchedule.value = schedule
  // 自动填充日期
  leaveDate.value = schedule.start_time.split('T')[0]
}

/**
 * 选择日期
 */
function onDateChange(e: any) {
  leaveDate.value = e.detail.value
}

/**
 * 选择课时
 */
function onHoursChange(e: any) {
  leaveHours.value = parseInt(e.detail.value)
}

/**
 * 输入原因
 */
function onReasonInput(e: any) {
  reason.value = e.detail.value
}

/**
 * 提交请假申请
 */
async function submitLeave() {
  // 验证表单
  if (!selectedSchedule.value) {
    formError.value = '请选择课程'
    uni.showToast({
      title: '请选择课程',
      icon: 'none'
    })
    return
  }

  if (!leaveDate.value) {
    formError.value = '请选择请假日期'
    uni.showToast({
      title: '请选择请假日期',
      icon: 'none'
    })
    return
  }

  if (!reason.value.trim()) {
    formError.value = '请输入请假原因'
    uni.showToast({
      title: '请输入请假原因',
      icon: 'none'
    })
    return
  }

  loading.value = true
  formError.value = ''

  try {
    await leaveStore.applyLeave({
      schedule_id: selectedSchedule.value.id,
      student_id: 1, // TODO: 从用户信息获取
      leave_date: leaveDate.value,
      reason: reason.value,
      hours: leaveHours.value
    })

    uni.showToast({
      title: '申请成功',
      icon: 'success'
    })

    // 返回列表页
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)

  } catch (error) {
    console.error('申请请假失败:', error)
    uni.showToast({
      title: '申请失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 返回上一页
 */
function goBack() {
  uni.navigateBack()
}

onMounted(() => {
  init()
})
</script>

<template>
  <view class="leave-apply-container">
    <!-- 课程选择 -->
    <view class="section-card">
      <view class="section-title">选择课程</view>
      <view class="schedule-list" v-if="scheduleStore.todaySchedules.length > 0">
        <view
          v-for="schedule in scheduleStore.todaySchedules"
          :key="schedule.id"
          :class="['schedule-item', { active: selectedSchedule?.id === schedule.id }]"
          @click="selectSchedule(schedule)"
        >
          <view class="schedule-info">
            <view class="course-name">{{ schedule.course_name || '课程' }}</view>
            <view class="schedule-time">
              {{ schedule.start_time.split('T')[1]?.slice(0, 5) }} -
              {{ schedule.end_time.split('T')[1]?.slice(0, 5) }}
            </view>
          </view>
          <view :class="['radio', { checked: selectedSchedule?.id === schedule.id }]">
            <text v-if="selectedSchedule?.id === schedule.id">&#10003;</text>
          </view>
        </view>
      </view>
      <view v-else class="empty-tip">
        今日暂无课程
      </view>
    </view>

    <!-- 请假日期 -->
    <view class="section-card">
      <view class="section-title">请假日期</view>
      <picker mode="date" :value="leaveDate" @change="onDateChange">
        <view class="picker-trigger">
          <text v-if="leaveDate">{{ leaveDate }}</text>
          <text v-else class="placeholder">请选择请假日期</text>
        </view>
      </picker>
    </view>

    <!-- 请假课时 -->
    <view class="section-card">
      <view class="section-title">请假课时</view>
      <picker mode="selector" :range="[1, 2, 3, 4]" @change="onHoursChange">
        <view class="picker-trigger">
          <text>{{ leaveHours }}课时</text>
        </view>
      </picker>
    </view>

    <!-- 请假原因 -->
    <view class="section-card">
      <view class="section-title">请假原因</view>
      <textarea
        class="reason-input"
        placeholder="请输入请假原因"
        :value="reason"
        @input="onReasonInput"
        maxlength="500"
      />
    </view>

    <!-- 错误提示 -->
    <view class="error-tip" v-if="formError">
      {{ formError }}
    </view>

    <!-- 提交按钮 -->
    <view class="submit-area">
      <view class="submit-btn" :class="{ disabled: loading }" @click="submitLeave">
        {{ loading ? '提交中...' : '提交申请' }}
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.leave-apply-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20rpx;
  padding-bottom: 120rpx;
}

.section-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;

  .section-title {
    font-size: 28rpx;
    font-weight: 600;
    color: #303133;
    margin-bottom: 16rpx;
  }
}

.schedule-list {
  display: flex;
  flex-direction: column;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  border: 2rpx solid #f0f0f0;
  border-radius: 12rpx;
  margin-bottom: 12rpx;

  &.active {
    border-color: #1890ff;
    background-color: #f0f7ff;
  }

  .schedule-info {
    .course-name {
      font-size: 28rpx;
      color: #303133;
      margin-bottom: 8rpx;
    }

    .schedule-time {
      font-size: 24rpx;
      color: #909399;
    }
  }

  .radio {
    width: 40rpx;
    height: 40rpx;
    border-radius: 50%;
    border: 2rpx solid #d9d9d9;
    display: flex;
    justify-content: center;
    align-items: center;

    &.checked {
      border-color: #1890ff;
      background-color: #1890ff;
      color: #ffffff;
      font-size: 24rpx;
    }
  }
}

.empty-tip {
  padding: 40rpx;
  text-align: center;
  color: #909399;
  font-size: 26rpx;
}

.picker-trigger {
  padding: 20rpx;
  background-color: #f5f7fa;
  border-radius: 8rpx;
  font-size: 28rpx;
  color: #303133;

  .placeholder {
    color: #c0c4cc;
  }
}

.reason-input {
  width: 100%;
  min-height: 200rpx;
  padding: 20rpx;
  background-color: #f5f7fa;
  border-radius: 8rpx;
  font-size: 28rpx;
  color: #303133;
  box-sizing: border-box;
}

.error-tip {
  padding: 20rpx;
  color: #ff4d4f;
  font-size: 24rpx;
  text-align: center;
}

.submit-area {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20rpx;
  background-color: #ffffff;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);

  .submit-btn {
    width: 100%;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    color: #ffffff;
    background-color: #1890ff;
    border-radius: 16rpx;

    &.disabled {
      background-color: #ccc;
    }
  }
}
</style>
