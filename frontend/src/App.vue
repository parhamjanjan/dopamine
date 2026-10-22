<template>
  <div id="app-shell" dir="rtl">
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
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
