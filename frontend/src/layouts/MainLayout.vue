<template>
  <div class="main-layout">
    <!-- محتوای صفحات -->
    <main class="layout-content">
      <RouterView />
    </main>

    <!-- نوار پایین -->
    <nav class="bottom-nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.name"
        :to="{ name: item.name }"
        class="nav-item"
        exact-active-class="nav-item-active"
      >
        <span
          v-if="item.notification"
          class="nav-notification"
        ></span>

        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <template v-if="item.icon === 'home'">
            <path d="m3 10 9-7 9 7" />
            <path d="M5 9v11h14V9" />
            <path d="M9 20v-6h6v6" />
          </template>

          <template v-else-if="item.icon === 'planner'">
            <rect x="4" y="4" width="16" height="16" rx="3" />
            <path d="M8 2v4" />
            <path d="M16 2v4" />
            <path d="M4 9h16" />
            <path d="M8 13h2" />
            <path d="M14 13h2" />
            <path d="M8 17h2" />
          </template>

          <template v-else-if="item.icon === 'rooms'">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </template>

          <template v-else-if="item.icon === 'exams'">
            <rect x="5" y="3" width="14" height="18" rx="2" />
            <path d="M9 7h6" />
            <path d="M9 11h6" />
            <path d="M9 15h4" />
          </template>

          <template v-else-if="item.icon === 'messages'">
            <path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H8l-4 2v-5.2A7.5 7.5 0 1 1 20 11.5Z" />
            <circle cx="8.5" cy="11.5" r=".7" fill="currentColor" stroke="none" />
            <circle cx="12" cy="11.5" r=".7" fill="currentColor" stroke="none" />
            <circle cx="15.5" cy="11.5" r=".7" fill="currentColor" stroke="none" />
          </template>

          <template v-else-if="item.icon === 'profile'">
            <circle cx="12" cy="12" r="9" />
            <circle cx="12" cy="9" r="3" />
            <path d="M6.5 19a6 6 0 0 1 11 0" />
          </template>
        </svg>

        <span class="nav-label">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'

const navItems = [
  {
    name: 'home',
    label: 'خانه',
    icon: 'home'
  },
  {
    name: 'planner',
    label: 'برنامه‌ریز',
    icon: 'planner'
  },
  {
    name: 'rooms',
    label: 'سالن‌ها',
    icon: 'rooms'
  },
  {
    name: 'exams',
    label: 'آزمون‌ها',
    icon: 'exams'
  },
  {
    name: 'messages',
    label: 'پیام‌ها',
    icon: 'messages',
    notification: true
  },
  {
    name: 'profile',
    label: 'پروفایل',
    icon: 'profile'
  }
]
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  position: relative;
}

.layout-content {
  min-height: 100vh;
}

/* =========================
   Bottom Navigation
========================= */

.bottom-nav {
  position: fixed;
  z-index: 1000;

  left: 50%;
  bottom: 10px;
  transform: translateX(-50%);

  width: min(720px, calc(100% - 24px));
  height: 72px;

  display: grid;
  grid-template-columns: repeat(6, 1fr);
  align-items: stretch;

  padding: 7px;

  background: rgba(15, 23, 42, 0.97);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 22px;

  box-shadow:
    0 20px 55px rgba(15, 23, 42, 0.22);

  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* =========================
   Nav Item
========================= */

.nav-item {
  position: relative;

  min-width: 0;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;

  color: #94a3b8;

  text-decoration: none;

  border-radius: 15px;

  transition:
    color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.nav-item:hover {
  color: #e2e8f0;
}

.nav-item:active {
  transform: scale(0.96);
}

/* =========================
   Active Item
========================= */

.nav-item-active {
  color: #ffffff;
  background: rgba(var(--primary-rgb), 0.16);
}

.nav-item-active::after {
  content: '';

  position: absolute;
  left: 50%;
  bottom: 3px;

  width: 18px;
  height: 2px;

  transform: translateX(-50%);

  background: var(--primary-300);
  border-radius: 999px;
}

/* =========================
   Icon
========================= */

.nav-icon {
  width: 21px;
  height: 21px;

  flex-shrink: 0;
}

/* =========================
   Label
========================= */

.nav-label {
  font-size: 10px;
  line-height: 1;
  font-weight: 500;

  white-space: nowrap;
}

/* =========================
   Notification
========================= */

.nav-notification {
  position: absolute;

  top: 9px;
  right: calc(50% - 17px);

  width: 7px;
  height: 7px;

  background: #ef4444;

  border: 2px solid rgba(15, 23, 42, 0.97);
  border-radius: 50%;
}

/* =========================
   Responsive
========================= */

@media (max-width: 640px) {
  .bottom-nav {
    width: calc(100% - 20px);
    bottom: 10px;
    height: 70px;

    padding: 6px;
    border-radius: 20px;
  }

  .nav-icon {
    width: 20px;
    height: 20px;
  }

  .nav-label {
    font-size: 9px;
  }
}
</style>