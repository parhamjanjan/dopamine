```vue
<template>
  <div class="main-layout" :class="{ 'layout-dark': isDark }">
    <!-- Main content -->
    <main class="layout-content">
      <RouterView />
    </main>

    <!-- Open navigation button -->
    <Transition name="nav-reveal">
      <button
        v-if="!isNavVisible"
        type="button"
        class="nav-toggle-open"
        :class="{ 'is-dark': isDark }"
        @click="isNavVisible = true"
        aria-label="باز کردن نوار ناوبری"
        title="باز کردن منو"
      >
        <span class="toggle-open-glow"></span>

        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="toggle-icon"
        >
          <path d="m6 14 6-6 6 6" />
        </svg>
      </button>
    </Transition>

    <!-- Premium bottom navigation -->
    <Transition name="nav-slide">
      <nav
        v-if="isNavVisible"
        class="bottom-nav"
        :class="{ 'is-dark': isDark }"
        aria-label="ناوبری اصلی"
        dir="rtl"
      >
        <!-- Ambient light effects -->
        <div class="nav-ambient nav-ambient-one"></div>
        <div class="nav-ambient nav-ambient-two"></div>
        <div class="nav-top-highlight"></div>

        <!-- Animated active indicator -->
        <div
          class="nav-active-indicator"
          :style="activeIndicatorStyle"
          aria-hidden="true"
        >
          <div class="indicator-glow"></div>
          <div class="indicator-core"></div>
        </div>

        <!-- Navigation items -->
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="{ name: item.name }"
          class="nav-item"
          active-class="nav-item-active"
          exact-active-class="nav-item-exact-active"
          :aria-label="item.label"
          :title="item.label"
        >
          <span
            v-if="item.notification"
            class="nav-notification"
            aria-label="اعلان جدید"
          ></span>

          <span class="nav-item-inner">
            <span class="nav-icon-wrap">
              <svg
                class="nav-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <!-- Home -->
                <template v-if="item.icon === 'home'">
                  <path d="m3 10 9-7 9 7" />
                  <path d="M5 9v11h14V9" />
                  <path d="M9 20v-6h6v6" />
                </template>

                <!-- Notes -->
                <template v-else-if="item.icon === 'notes'">
                  <path
                    d="M6.5 3.5H14l4.5 4.5V19a2 2 0 0 1-2 2H6.5a2 2 0 0 1-2-2V5.5a2 2 0 0 1 2-2Z"
                  />
                  <path d="M14 3.5V8h4.5" />
                  <path d="M8 12h8" />
                  <path d="M8 16h8" />
                </template>

                <!-- Study rooms -->
                <template v-else-if="item.icon === 'rooms'">
                  <circle cx="9" cy="7" r="4" />
                  <path
                    d="M2.5 21v-2a6.5 6.5 0 0 1 13 0v2"
                  />
                  <path d="M16 4a4 4 0 0 1 0 7.5" />
                  <path d="M18 15a5.5 5.5 0 0 1 3.5 5v1" />
                </template>

                <!-- Exams -->
                <template v-else-if="item.icon === 'exams'">
                  <rect x="5" y="3" width="14" height="18" rx="2.5" />
                  <path d="M9 7h6" />
                  <path d="M9 11h6" />
                  <path d="M9 15h3" />
                  <path d="m14 16 1.5 1.5L19 14" />
                </template>

                <!-- Planner -->
                <template v-else-if="item.icon === 'planner'">
                  <rect x="3.5" y="5" width="17" height="16" rx="3" />
                  <path d="M8 3v4" />
                  <path d="M16 3v4" />
                  <path d="M3.5 10h17" />
                  <path d="m8 14 1.5 1.5L12 13" />
                  <path d="M14 15h3" />
                  <path d="M8 18h2" />
                </template>

                <!-- Profile -->
                <template v-else-if="item.icon === 'profile'">
                  <circle cx="12" cy="12" r="9" />
                  <circle cx="12" cy="9" r="3" />
                  <path d="M6.5 19a6 6 0 0 1 11 0" />
                </template>
              </svg>

              <span class="icon-orbit"></span>
            </span>

            <span class="nav-label">
              {{ item.label }}
            </span>
          </span>
        </RouterLink>

        <!-- Close navigation -->
        <button
          type="button"
          class="nav-toggle-close"
          @click="isNavVisible = false"
          aria-label="جمع کردن نوار ناوبری"
          title="جمع کردن منو"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="m7 10 5 5 5-5" />
          </svg>
        </button>
      </nav>
    </Transition>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount
} from 'vue'

import {
  RouterLink,
  RouterView,
  useRoute
} from 'vue-router'

const route = useRoute()

const isNavVisible = ref(true)
const isDark = ref(false)

let themeObserver = null

const navItems = [
  { name: 'home', label: 'خانه', icon: 'home' },
  { name: 'notes', label: 'جزوه‌ها', icon: 'notes' },
  { name: 'rooms', label: 'سالن‌ها', icon: 'rooms' },
  { name: 'exams', label: 'آزمون‌ها', icon: 'exams' },
  { name: 'planner', label: 'برنامه‌ریز', icon: 'planner' },
  { name: 'profile', label: 'پروفایل', icon: 'profile' }
]

/*
|--------------------------------------------------------------------------
| Theme detection
| سازگار با سیستم تم سراسری پروژه دوپامین
|--------------------------------------------------------------------------
*/

function detectDarkTheme() {
  const root = document.documentElement
  const body = document.body

  const dataTheme =
    root.getAttribute('data-theme') ||
    body?.getAttribute('data-theme')

  if (dataTheme === 'dark') return true
  if (dataTheme === 'light') return false

  if (
    root.classList.contains('dark') ||
    body?.classList.contains('dark') ||
    root.classList.contains('dark-mode') ||
    body?.classList.contains('dark-mode')
  ) {
    return true
  }

  return false
}

function syncTheme() {
  isDark.value = detectDarkTheme()
}

function initThemeWatcher() {
  syncTheme()

  if (typeof MutationObserver === 'undefined') return

  themeObserver = new MutationObserver(() => {
    syncTheme()
  })

  const options = {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style']
  }

  themeObserver.observe(document.documentElement, options)
  themeObserver.observe(document.body, options)
}

/*
|--------------------------------------------------------------------------
| Active item indicator
|--------------------------------------------------------------------------
| هر آیتم یک ستون مساوی دارد. نشانگر زیر آیتم فعال قرار می‌گیرد.
*/

const activeIndicatorStyle = computed(() => {
  const index = navItems.findIndex(
    item => item.name === route.name
  )

  if (index < 0) {
    return {
      opacity: '0',
      '--active-index': '0'
    }
  }

  return {
    opacity: '1',
    '--active-index': String(index)
  }
})

onMounted(() => {
  initThemeWatcher()
})

onBeforeUnmount(() => {
  themeObserver?.disconnect()
  themeObserver = null
})
</script>

<style scoped>
/* =========================================================
   LAYOUT
========================================================= */

.main-layout {
  --nav-accent: var(--primary-color, #8065f6);
  --nav-accent-rgb: var(--primary-rgb, 128, 101, 246);
  --nav-height: 88px;

  min-height: 100vh;
  min-height: 100dvh;
  position: relative;
}

.layout-content {
  min-height: 100vh;
  min-height: 100dvh;

  /*
   * از قرار گرفتن محتوای صفحه زیر نوار جلوگیری می‌کند.
   */
  padding-bottom: calc(
    var(--nav-height) + 35px + env(safe-area-inset-bottom, 0px)
  );
}

/* =========================================================
   BOTTOM NAVIGATION — LIGHT THEME
========================================================= */

.bottom-nav {
  --surface: rgba(255, 255, 255, 0.91);
  --surface-inner: rgba(255, 255, 255, 0.55);
  --nav-border: rgba(113, 97, 166, 0.17);

  --text-primary: #38334b;
  --text-secondary: #858096;

  --active-bg: rgba(var(--nav-accent-rgb), 0.105);
  --active-text: var(--nav-accent);

  --highlight: rgba(255, 255, 255, 0.95);
  --shadow-color: rgba(47, 35, 89, 0.15);

  position: fixed;
  z-index: 1000;

  left: 8px;
  right: 8px;

  bottom: max(8px, env(safe-area-inset-bottom, 0px));

  height: var(--nav-height);

  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  align-items: stretch;

  padding: 9px 8px 7px;

  isolation: isolate;
  overflow: visible;

  border: 1px solid var(--nav-border);
  border-radius: 27px;

  background: var(--surface);
  color: var(--text-primary);

  box-shadow:
    0 18px 55px var(--shadow-color),
    0 5px 15px rgba(30, 25, 60, 0.045),
    inset 0 1px 0 var(--highlight),
    inset 0 -1px 0 rgba(125, 105, 175, 0.055);

  backdrop-filter: blur(30px) saturate(175%);
  -webkit-backdrop-filter: blur(30px) saturate(175%);

  transition:
    background 0.35s ease,
    border-color 0.35s ease,
    box-shadow 0.35s ease,
    color 0.35s ease;

  direction: rtl;
}

/* =========================================================
   DARK THEME
========================================================= */

.bottom-nav.is-dark {
  --surface: rgba(18, 17, 31, 0.94);
  --surface-inner: rgba(255, 255, 255, 0.035);
  --nav-border: rgba(193, 174, 255, 0.15);

  --text-primary: #f4f0ff;
  --text-secondary: #9690ac;

  --active-bg: rgba(var(--nav-accent-rgb), 0.19);
  --active-text: #e3d9ff;

  --highlight: rgba(255, 255, 255, 0.1);
  --shadow-color: rgba(0, 0, 0, 0.43);

  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.045),
      transparent 48%
    ),
    var(--surface);

  box-shadow:
    0 20px 65px var(--shadow-color),
    0 0 30px rgba(var(--nav-accent-rgb), 0.075),
    inset 0 1px 0 var(--highlight),
    inset 0 -1px 0 rgba(255, 255, 255, 0.025);
}

/* =========================================================
   AMBIENT LIGHTS
========================================================= */

.nav-ambient {
  position: absolute;
  z-index: -1;

  pointer-events: none;

  border-radius: 50%;
  filter: blur(27px);

  opacity: 0.38;

  transition: opacity 0.35s ease;
}

.nav-ambient-one {
  width: 190px;
  height: 70px;

  right: 3%;
  top: -30px;

  background: rgba(var(--nav-accent-rgb), 0.19);
}

.nav-ambient-two {
  width: 170px;
  height: 65px;

  left: 5%;
  bottom: -25px;

  background: rgba(71, 164, 255, 0.13);
}

.bottom-nav.is-dark .nav-ambient {
  opacity: 0.72;
}

.nav-top-highlight {
  position: absolute;
  top: 0;
  left: 12%;
  right: 12%;

  height: 1px;

  pointer-events: none;

  background: linear-gradient(
    90deg,
    transparent,
    rgba(var(--nav-accent-rgb), 0.4),
    rgba(255, 255, 255, 0.8),
    rgba(var(--nav-accent-rgb), 0.4),
    transparent
  );

  opacity: 0.75;
}

/* =========================================================
   ACTIVE INDICATOR
========================================================= */

.nav-active-indicator {
  position: absolute;

  top: 7px;

  right: calc(
    8px + (100% - 16px) / 6 * var(--active-index)
  );

  width: calc((100% - 16px) / 6);
  height: calc(100% - 14px);

  pointer-events: none;

  transition:
    right 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.2s ease;

  will-change: right;
}

.nav-active-indicator::before {
  content: '';

  position: absolute;
  inset: 0 3px;

  border-radius: 20px;

  background:
    linear-gradient(
      145deg,
      rgba(var(--nav-accent-rgb), 0.15),
      rgba(var(--nav-accent-rgb), 0.045)
    );

  border: 1px solid rgba(var(--nav-accent-rgb), 0.12);

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.32),
    0 3px 12px rgba(var(--nav-accent-rgb), 0.045);

  transition:
    background 0.35s ease,
    border-color 0.35s ease,
    box-shadow 0.35s ease;
}

.bottom-nav.is-dark .nav-active-indicator::before {
  background:
    linear-gradient(
      145deg,
      rgba(var(--nav-accent-rgb), 0.23),
      rgba(var(--nav-accent-rgb), 0.075)
    );

  border-color: rgba(var(--nav-accent-rgb), 0.22);

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.07),
    0 0 24px rgba(var(--nav-accent-rgb), 0.09);
}

.indicator-glow {
  position: absolute;

  top: -4px;
  left: 24%;
  right: 24%;

  height: 13px;

  border-radius: 50%;

  background: var(--nav-accent);

  filter: blur(12px);
  opacity: 0.23;
}

.indicator-core {
  position: absolute;

  top: -1px;
  left: 50%;

  width: 24px;
  height: 3px;

  transform: translateX(-50%);

  border-radius: 999px;

  background: var(--nav-accent);

  box-shadow:
    0 0 8px rgba(var(--nav-accent-rgb), 0.48),
    0 0 18px rgba(var(--nav-accent-rgb), 0.23);
}

/* =========================================================
   NAV ITEMS
========================================================= */

.nav-item {
  position: relative;
  z-index: 2;

  min-width: 0;
  min-height: 0;

  display: flex;
  align-items: stretch;
  justify-content: center;

  padding: 0 1px;

  border-radius: 20px;

  color: var(--text-secondary);
  text-decoration: none;

  -webkit-tap-highlight-color: transparent;

  transition:
    color 0.28s ease,
    transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-item-inner {
  width: 100%;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 5px;

  min-width: 0;

  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-icon-wrap {
  position: relative;

  width: 33px;
  height: 33px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  border-radius: 12px;

  transition:
    background 0.3s ease,
    box-shadow 0.3s ease,
    transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-icon {
  position: relative;
  z-index: 1;

  display: block;

  width: 23px;
  height: 23px;

  overflow: visible;

  transition:
    transform 0.32s cubic-bezier(0.22, 1, 0.36, 1),
    filter 0.3s ease;
}

.nav-label {
  display: block;

  max-width: 100%;

  font-family: inherit;
  font-size: 10px;
  line-height: 1.25;
  font-weight: 550;

  white-space: nowrap;

  color: inherit;

  transition:
    color 0.25s ease,
    letter-spacing 0.25s ease,
    transform 0.25s ease;
}

.nav-item:hover {
  color: var(--text-primary);
}

.nav-item:hover .nav-icon {
  transform: translateY(-2px) scale(1.06);
}

.nav-item:active {
  transform: scale(0.94);
}

.nav-item:focus-visible {
  outline: 2px solid var(--nav-accent);
  outline-offset: -3px;
}

/* =========================================================
   ACTIVE ITEM
========================================================= */

.nav-item-active,
.nav-item-exact-active {
  color: var(--active-text);
}

.nav-item-active .nav-icon-wrap,
.nav-item-exact-active .nav-icon-wrap {
  background:
    linear-gradient(
      145deg,
      rgba(var(--nav-accent-rgb), 0.12),
      rgba(var(--nav-accent-rgb), 0.035)
    );

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.35),
    0 3px 12px rgba(var(--nav-accent-rgb), 0.055);
}

.bottom-nav.is-dark .nav-item-active .nav-icon-wrap,
.bottom-nav.is-dark .nav-item-exact-active .nav-icon-wrap {
  background: rgba(var(--nav-accent-rgb), 0.15);

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.055),
    0 0 16px rgba(var(--nav-accent-rgb), 0.07);
}

.nav-item-active .nav-icon,
.nav-item-exact-active .nav-icon {
  filter: drop-shadow(
    0 2px 5px rgba(var(--nav-accent-rgb), 0.17)
  );
}

.nav-item-active .nav-label,
.nav-item-exact-active .nav-label {
  font-weight: 750;
}

.nav-item-active .nav-item-inner,
.nav-item-exact-active .nav-item-inner {
  transform: translateY(-1px);
}

/* Small decorative orbit around active icon */

.icon-orbit {
  position: absolute;

  inset: -3px;

  border: 1px solid rgba(var(--nav-accent-rgb), 0.0);
  border-radius: 14px;

  pointer-events: none;

  transition:
    inset 0.3s ease,
    border-color 0.3s ease,
    opacity 0.3s ease;

  opacity: 0;
}

.nav-item-active .icon-orbit,
.nav-item-exact-active .icon-orbit {
  inset: -2px;

  border-color: rgba(var(--nav-accent-rgb), 0.18);
  opacity: 1;
}

/* =========================================================
   NOTIFICATION
========================================================= */

.nav-notification {
  position: absolute;
  z-index: 5;

  top: 12px;
  right: calc(50% - 17px);

  width: 8px;
  height: 8px;

  border-radius: 50%;

  background: #ff5577;

  border: 2px solid var(--surface);

  box-shadow:
    0 0 0 2px rgba(255, 85, 119, 0.12),
    0 0 10px rgba(255, 85, 119, 0.4);

  animation: notification-pulse 2.2s ease-in-out infinite;
}

/* =========================================================
   CLOSE BUTTON
========================================================= */

.nav-toggle-close {
  position: absolute;
  z-index: 6;

  top: -13px;
  left: 50%;

  width: 27px;
  height: 27px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  transform: translateX(-50%);

  border: 1px solid var(--nav-border);
  border-radius: 50%;

  color: var(--text-secondary);
  background: var(--surface);

  box-shadow:
    0 4px 14px var(--shadow-color),
    inset 0 1px 0 var(--highlight);

  cursor: pointer;

  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);

  transition:
    color 0.25s ease,
    background 0.25s ease,
    box-shadow 0.25s ease,
    transform 0.25s ease;
}

.nav-toggle-close svg {
  width: 14px;
  height: 14px;

  transition: transform 0.3s ease;
}

.nav-toggle-close:hover {
  color: var(--nav-accent);

  box-shadow:
    0 5px 18px var(--shadow-color),
    0 0 15px rgba(var(--nav-accent-rgb), 0.1);
}

.nav-toggle-close:hover svg {
  transform: translateY(1px);
}

.nav-toggle-close:active {
  transform: translateX(-50%) scale(0.9);
}

.nav-toggle-close:focus-visible,
.nav-toggle-open:focus-visible {
  outline: 2px solid var(--nav-accent);
  outline-offset: 3px;
}

/* =========================================================
   OPEN BUTTON
========================================================= */

.nav-toggle-open {
  --surface: rgba(255, 255, 255, 0.92);
  --nav-border: rgba(113, 97, 166, 0.2);
  --text-primary: #6350a6;
  --shadow-color: rgba(47, 35, 89, 0.2);

  position: fixed;
  z-index: 1000;

  left: 50%;
  bottom: max(15px, env(safe-area-inset-bottom, 0px));

  width: 47px;
  height: 47px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0;

  transform: translateX(-50%);

  overflow: hidden;

  color: var(--text-primary);

  background:
    linear-gradient(
      145deg,
      rgba(255, 255, 255, 0.96),
      rgba(246, 242, 255, 0.9)
    );

  border: 1px solid var(--nav-border);
  border-radius: 17px;

  box-shadow:
    0 9px 30px var(--shadow-color),
    0 0 22px rgba(var(--nav-accent-rgb), 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.95);

  cursor: pointer;

  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);

  transition:
    color 0.3s ease,
    background 0.3s ease,
    box-shadow 0.3s ease,
    border-color 0.3s ease,
    transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-toggle-open.is-dark {
  --surface: rgba(24, 22, 40, 0.96);
  --nav-border: rgba(193, 174, 255, 0.19);
  --text-primary: #e3d9ff;
  --shadow-color: rgba(0, 0, 0, 0.4);

  background:
    linear-gradient(
      145deg,
      rgba(40, 35, 63, 0.98),
      rgba(20, 19, 34, 0.96)
    );

  box-shadow:
    0 10px 32px var(--shadow-color),
    0 0 25px rgba(var(--nav-accent-rgb), 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.09);
}

.nav-toggle-open:hover {
  transform: translateX(-50%) translateY(-3px);

  box-shadow:
    0 13px 34px var(--shadow-color),
    0 0 26px rgba(var(--nav-accent-rgb), 0.2);
}

.nav-toggle-open:active {
  transform: translateX(-50%) scale(0.93);
}

.nav-toggle-open .toggle-icon {
  position: relative;
  z-index: 1;

  width: 21px;
  height: 21px;
}

.toggle-open-glow {
  position: absolute;

  inset: -15px;

  border-radius: 50%;

  background: rgba(var(--nav-accent-rgb), 0.15);
  filter: blur(13px);

  pointer-events: none;
}

/* =========================================================
   TRANSITIONS
========================================================= */

.nav-slide-enter-active,
.nav-slide-leave-active {
  transition:
    opacity 0.32s ease,
    transform 0.42s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-slide-enter-from,
.nav-slide-leave-to {
  opacity: 0;
  transform: translateY(35px) scale(0.97);
}

.nav-reveal-enter-active,
.nav-reveal-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-reveal-enter-from,
.nav-reveal-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(15px) scale(0.86);
}

/* =========================================================
   KEYFRAMES
========================================================= */

@keyframes notification-pulse {
  0%, 100% {
    box-shadow:
      0 0 0 2px rgba(255, 85, 119, 0.1),
      0 0 8px rgba(255, 85, 119, 0.28);
  }

  50% {
    box-shadow:
      0 0 0 4px rgba(255, 85, 119, 0.045),
      0 0 13px rgba(255, 85, 119, 0.5);
  }
}

/* =========================================================
   RESPONSIVE
========================================================= */

@media (min-width: 900px) {
  .bottom-nav {
    left: 12px;
    right: 12px;

    height: 91px;

    border-radius: 29px;

    padding: 9px 10px 7px;
  }

  .nav-active-indicator {
    right: calc(
      10px + (100% - 20px) / 6 * var(--active-index)
    );

    width: calc((100% - 20px) / 6);
  }

  .nav-icon-wrap {
    width: 37px;
    height: 37px;
  }

  .nav-icon {
    width: 24px;
    height: 24px;
  }

  .nav-label {
    font-size: 11px;
  }

  .nav-item-inner {
    gap: 4px;
  }
}

@media (max-width: 480px) {
  .main-layout {
    --nav-height: 79px;
  }

  .bottom-nav {
    left: 5px;
    right: 5px;

    bottom: max(5px, env(safe-area-inset-bottom, 0px));

    height: var(--nav-height);

    padding: 7px 5px 5px;

    border-radius: 23px;
  }

  .nav-active-indicator {
    top: 6px;
    height: calc(100% - 12px);

    right: calc(
      5px + (100% - 10px) / 6 * var(--active-index)
    );

    width: calc((100% - 10px) / 6);
  }

  .nav-active-indicator::before {
    inset: 0 2px;
    border-radius: 17px;
  }

  .nav-icon-wrap {
    width: 29px;
    height: 29px;

    border-radius: 10px;
  }

  .nav-icon {
    width: 21px;
    height: 21px;
  }

  .nav-item-inner {
    gap: 4px;
  }

  .nav-label {
    font-size: 9px;
    font-weight: 550;
  }

  .nav-item-active .nav-label,
  .nav-item-exact-active .nav-label {
    font-weight: 750;
  }

  .nav-toggle-close {
    width: 24px;
    height: 24px;
    top: -11px;
  }

  .nav-toggle-close svg {
    width: 12px;
    height: 12px;
  }

  .nav-notification {
    top: 10px;
    right: calc(50% - 15px);
  }
}

/* Very narrow screens */

@media (max-width: 350px) {
  .bottom-nav {
    left: 3px;
    right: 3px;
    padding-left: 3px;
    padding-right: 3px;
  }

  .nav-label {
    font-size: 8px;
  }

  .nav-icon-wrap {
    width: 27px;
    height: 27px;
  }

  .nav-icon {
    width: 20px;
    height: 20px;
  }
}

/* =========================================================
   ACCESSIBILITY
========================================================= */

@media (prefers-reduced-motion: reduce) {
  .bottom-nav,
  .bottom-nav *,
  .nav-toggle-open,
  .nav-slide-enter-active,
  .nav-slide-leave-active,
  .nav-reveal-enter-active,
  .nav-reveal-leave-active {
    animation: none !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
```