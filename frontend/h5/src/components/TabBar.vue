<template>
  <van-tabbar v-model="active" active-color="#667eea" inactive-color="#999">
    <van-tabbar-item name="home" icon="home-o" to="/">
      首页
    </van-tabbar-item>
    <van-tabbar-item name="schedule" icon="calendar-o" to="/schedule">
      课表
    </van-tabbar-item>
    <van-tabbar-item name="attendance" icon="todo-list-o" to="/attendance">
      考勤
    </van-tabbar-item>
    <van-tabbar-item name="notifications" icon="bell-o" to="/notifications">
      消息
      <template #icon>
        <span v-if="unreadCount > 0" class="badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
      </template>
    </van-tabbar-item>
    <van-tabbar-item name="profile" icon="user-o" to="/profile">
      我的
    </van-tabbar-item>
  </van-tabbar>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useNotificationStore } from '@/stores/notification'

const route = useRoute()
const notificationStore = useNotificationStore()

// 当前激活的标签
const active = computed(() => {
  const name = route.name?.toString() || 'home'
  return name
})

// 未读消息数量
const unreadCount = computed(() => notificationStore.unreadCount)
</script>

<style lang="scss" scoped>
.badge {
  position: absolute;
  top: 2px;
  right: 8px;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  background: #f44336;
  color: #fff;
  font-size: 10px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
