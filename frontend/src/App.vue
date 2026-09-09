<template>
  <div dir="rtl">
    <RouterView />

   
  </div>
   
</template>
<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useTheme } from './composables/useTheme'

const auth = useAuthStore()
const { applyTheme } = useTheme()

onMounted(async () => {
  if (auth.accessToken) {
    try {
      await auth.fetchUser()
    } catch (error) {
      console.error('خطا در دریافت اطلاعات کاربر:', error)
    }
  }

  applyTheme()
})
</script>