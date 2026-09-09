<template>
  <div class="home-page" :class="{ 'home-dark': isDark }">
    <main class="page-wrapper">

      <!-- =========================
           HEADER
      ========================== -->
      <header class="home-header">
        <div>
          <div class="date-row">
            <span>{{ todayWeekday }}</span>
            <span class="date-dot">•</span>
            <span>{{ todayDate }}</span>
          </div>

          <h1>
            صبح بخیر، {{ firstName }}
          </h1>

          <p>
            برنامه امروزت آماده است. موفق باشی.
          </p>
        </div>

        <RouterLink
          to="/messages"
          class="notification-button"
          aria-label="پیام‌ها"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <path
              d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"
            />
            <path d="M10 21h4" />
          </svg>

          <span class="notification-dot"></span>
        </RouterLink>
      </header>


      <!-- =========================
           LOADING
      ========================== -->
      <div
        v-if="loading"
        class="loading-card"
      >
        <div class="loading-spinner"></div>
        <span>در حال دریافت برنامه‌ات...</span>
      </div>


      <!-- =========================
           ERROR
      ========================== -->
      <div
        v-else-if="error"
        class="error-card"
      >
        <strong>دریافت اطلاعات انجام نشد</strong>

        <span>
          {{ error }}
        </span>

        <button
          type="button"
          @click="loadHomeData"
        >
          تلاش دوباره
        </button>
      </div>


      <template v-else>

        <!-- =========================
             OVERVIEW
        ========================== -->
        <section class="overview-card">

          <div class="overview-glow overview-glow-left"></div>
          <div class="overview-glow overview-glow-right"></div>

          <div class="overview-content">

            <div class="overview-main">

              <div class="status-pill">
                <span></span>
                وضعیت مطالعه امروز
              </div>

              <h2>
                روی برنامه بمان،
                <br class="desktop-break" />
                نتیجه خودش می‌آید.
              </h2>

              <p>
                امروز {{ totalTodayTasks }} تسک برایت برنامه‌ریزی شده که
                {{ completedTodayTasks }} مورد آن را انجام داده‌ای.
                <template v-if="remainingTodayTasks > 0">
                  فقط {{ remainingTodayTasks }} مرحله دیگر تا تکمیل برنامه امروز باقی مانده است.
                </template>

                <template v-else-if="totalTodayTasks > 0">
                  برنامه امروزت کامل شده است. عالی پیش رفتی.
                </template>

                <template v-else>
                  برای امروز هنوز تسکی برنامه‌ریزی نشده است.
                </template>
              </p>

              <div class="overview-actions">

                <RouterLink
                  to="/planner"
                  class="overview-primary-button"
                >
                  ادامه مطالعه
                </RouterLink>

                <RouterLink
                  to="/rooms"
                  class="overview-secondary-button"
                >
                  سالن‌های مطالعه
                </RouterLink>

              </div>

            </div>


            <!-- Progress -->
            <div class="progress-wrapper">

              <svg
                class="progress-circle"
                viewBox="0 0 120 120"
              >
                <circle
                  class="progress-track"
                  cx="60"
                  cy="60"
                  r="48"
                />

                <circle
                  class="progress-value"
                  cx="60"
                  cy="60"
                  r="48"
                  :style="{
                    strokeDashoffset: progressOffset
                  }"
                />
              </svg>

              <div class="progress-center">
                <strong>{{ dailyProgress }}٪</strong>

                <span>
                  تکمیل برنامه
                </span>
              </div>

            </div>

          </div>
        </section>


        <!-- =========================
             STATISTICS
        ========================== -->
        <section class="stats-grid">

          <!-- Streak -->
          <article class="stat-card">
            <div class="stat-label">
              روزهای متوالی
            </div>

            <div class="stat-value">
              {{ streakDays }}
            </div>

            <div
              class="stat-footer"
              :class="{ success: streakDays > 0 }"
            >
              {{ streakDays > 0 ? 'ادامه بده' : 'هنوز شروع نشده' }}
            </div>
          </article>


          <!-- Monthly study -->
          <article class="stat-card">
            <div class="stat-label">
              ساعت مطالعه
            </div>

            <div class="stat-value">
              {{ monthlyStudyHours }}
            </div>

            <div class="stat-footer">
              این ماه
            </div>
          </article>


          <!-- Completed -->
          <article class="stat-card">
            <div class="stat-label">
              تسک‌های تکمیل‌شده
            </div>

            <div class="stat-value">
              {{ completedTaskCount }}
            </div>

            <div class="stat-footer success">
              {{ productivity }}٪ بهره‌وری
            </div>
          </article>


          <!-- Today's study -->
          <article class="stat-card">
            <div class="stat-label">
              مطالعه امروز
            </div>

            <div class="stat-value">
              {{ todayStudyHours }}
            </div>

            <div class="stat-footer primary">
              ساعت مطالعه
            </div>
          </article>

        </section>


        <!-- =========================
             TASKS
        ========================== -->
        <section class="tasks-grid">

          <!-- =====================
               TODAY
          ====================== -->
          <article class="tasks-card">

            <div class="tasks-card-header">

              <div>
                <h3>
                  برنامه امروز
                </h3>

                <p>
                  {{ completedTodayTasks }}
                  مورد از
                  {{ totalTodayTasks }}
                  مورد تکمیل شده
                </p>
              </div>

              <span class="completion-badge">
                {{ dailyProgress }}٪ تکمیل
              </span>

            </div>


            <div
              v-if="todayTasks.length"
              class="task-list"
            >

              <button
                v-for="task in todayTasks"
                :key="task.id"
                type="button"
                class="task-row"
                :class="{ completed: task.completed }"
                :disabled="updatingTaskId === task.id"
                @click="toggleTask(task)"
              >

                <span
                  class="task-checkbox"
                  :class="{ checked: task.completed }"
                >

                  <svg
                    v-if="task.completed"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.5"
                  >
                    <path d="m5 12 4 4L19 6" />
                  </svg>

                </span>


                <span class="task-info">

                  <strong>
                    {{ task.title }}
                  </strong>

                  <span>
                    {{ getCategoryName(task.category) }}
                    <template v-if="task.studyTime">
                      • {{ formatStudyTime(task.studyTime) }}
                    </template>
                  </span>

                </span>


                <span
                  v-if="task.startTime"
                  class="task-time"
                >
                  {{ formatTime(task.startTime) }}
                </span>

                <span
                  v-else
                  class="task-time"
                >
                  —
                </span>

              </button>

            </div>


            <div
              v-else
              class="empty-tasks"
            >
              <span class="empty-icon">✓</span>

              <strong>
                برای امروز تسکی نداری
              </strong>

              <span>
                می‌توانی برنامه امروزت را از Planner بسازی.
              </span>
            </div>


            <button
              type="button"
              class="add-task-button"
              @click="goToPlanner"
            >
              <span>+</span>
              افزودن تسک
            </button>

          </article>


          <!-- =====================
               TOMORROW
          ====================== -->
          <article class="tasks-card">

            <div class="tasks-card-header">

              <div>
                <h3>
                  برنامه فردا
                </h3>

                <p>
                  {{ tomorrowTasks.length }}
                  فعالیت برنامه‌ریزی شده
                </p>
              </div>

              <span class="tomorrow-badge">
                فردا
              </span>

            </div>


            <div
              v-if="tomorrowTasks.length"
              class="task-list"
            >

              <div
                v-for="task in tomorrowTasks"
                :key="task.id"
                class="task-row tomorrow-task"
              >

                <span class="task-checkbox empty"></span>

                <span class="task-info">

                  <strong>
                    {{ task.title }}
                  </strong>

                  <span>
                    {{ getCategoryName(task.category) }}
                    <template v-if="task.studyTime">
                      • {{ formatStudyTime(task.studyTime) }}
                    </template>
                  </span>

                </span>


                <span
                  v-if="task.startTime"
                  class="task-time"
                >
                  {{ formatTime(task.startTime) }}
                </span>

                <span
                  v-else
                  class="task-time"
                >
                  —
                </span>

              </div>

            </div>


            <div
              v-else
              class="empty-tasks"
            >
              <span class="empty-icon tomorrow-empty">
                +
              </span>

              <strong>
                برای فردا برنامه‌ای نداری
              </strong>

              <span>
                می‌توانی از Planner فعالیت‌های فردا را اضافه کنی.
              </span>
            </div>


            <button
              type="button"
              class="add-task-button"
              @click="goToPlanner"
            >
              <span>+</span>
              برنامه‌ریزی فردا
            </button>

          </article>

        </section>

      </template>


      <!-- Toast -->
      <Transition name="toast">
        <div
          v-if="toast.visible"
          class="toast"
          :class="{ error: toast.type === 'error' }"
        >
          {{ toast.message }}
        </div>
      </Transition>

    </main>
  </div>
</template>


<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref
} from 'vue'

import {
  RouterLink,
  useRouter
} from 'vue-router'

import {
  getTasks as apiGetTasks,
  getLists as apiGetLists,
  updateTask as apiUpdateTask
} from '../services/planner'

import { useAuthStore } from '../stores/auth'


/* =========================================
   Stores
========================================= */

const auth = useAuthStore()
const router = useRouter()


/* =========================================
   State
========================================= */

const tasks = ref([])
const lists = ref([])

const loading = ref(true)
const error = ref('')

const updatingTaskId = ref(null)


/* =========================================
   User
========================================= */

const firstName = computed(() => {
  return (
    auth.user?.first_name ||
    auth.user?.username ||
    'پرهام'
  )
})


/* =========================================
   Date Helpers
========================================= */

function todayISO() {
  return new Date().toISOString().split('T')[0]
}

function addDaysISO(days) {
  const date = new Date()

  date.setDate(
    date.getDate() + days
  )

  return date.toISOString().split('T')[0]
}

const today = todayISO()
const tomorrow = addDaysISO(1)


const todayWeekday = new Intl.DateTimeFormat(
  'fa-IR',
  {
    weekday: 'long'
  }
).format(new Date())


const todayDate = new Intl.DateTimeFormat(
  'fa-IR',
  {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }
).format(new Date())


/* =========================================
   Normalize Task
   دقیقاً مطابق ساختار Planner فعلی
========================================= */

function normalizeTask(raw) {
  const plannerList = raw?.planner_list ?? null

  return {
    id: raw.id,

    title: raw.title || '',

    description: raw.description || '',

    completed: !!raw.completed,

    important: !!raw.important,

    category:
      plannerList !== null &&
      plannerList !== undefined
        ? String(plannerList)
        : String(raw.category || ''),

    plannerList,

    dueDate: raw.due_date || '',

    startTime: raw.start_time
      ? String(raw.start_time).slice(0, 5)
      : null,

    endTime: raw.end_time
      ? String(raw.end_time).slice(0, 5)
      : null,

    reminder: raw.reminder || 'none',

    timeCategory: raw.time_category || '',

    studyTime:
      parseFloat(raw.study_time) || 0,

    createdAt: raw.created_at,

    updatedAt: raw.updated_at
  }
}


/* =========================================
   Normalize List
========================================= */

function normalizeList(raw) {
  return {
    ...raw,

    id: String(raw.id),

    name: raw.name || '',

    color: raw.color || '#8b5cf6'
  }
}


/* =========================================
   Load Data
========================================= */

async function loadHomeData() {
  loading.value = true
  error.value = ''

  try {
    const [
      rawTasks,
      rawLists
    ] = await Promise.all([
      apiGetTasks(),
      apiGetLists()
    ])

    tasks.value = (
      Array.isArray(rawTasks)
        ? rawTasks
        : []
    ).map(normalizeTask)

    lists.value = (
      Array.isArray(rawLists)
        ? rawLists
        : []
    ).map(normalizeList)

  } catch (err) {

    console.error(
      'خطا در دریافت اطلاعات Home:',
      err
    )

    error.value =
      'اطلاعات برنامه از سرور دریافت نشد.'

  } finally {
    loading.value = false
  }
}


/* =========================================
   Today's Tasks
========================================= */

const todayTasks = computed(() => {
  return tasks.value
    .filter(task => task.dueDate === today)
    .sort((a, b) => {

      if (!a.startTime && !b.startTime) {
        return 0
      }

      if (!a.startTime) {
        return 1
      }

      if (!b.startTime) {
        return -1
      }

      return a.startTime.localeCompare(
        b.startTime
      )
    })
})


/* =========================================
   Tomorrow's Tasks
========================================= */

const tomorrowTasks = computed(() => {
  return tasks.value
    .filter(task => task.dueDate === tomorrow)
    .sort((a, b) => {

      if (!a.startTime && !b.startTime) {
        return 0
      }

      if (!a.startTime) {
        return 1
      }

      if (!b.startTime) {
        return -1
      }

      return a.startTime.localeCompare(
        b.startTime
      )
    })
})


/* =========================================
   Today's Statistics
========================================= */

const totalTodayTasks = computed(() => {
  return todayTasks.value.length
})


const completedTodayTasks = computed(() => {
  return todayTasks.value.filter(
    task => task.completed
  ).length
})


const remainingTodayTasks = computed(() => {
  return Math.max(
    totalTodayTasks.value -
    completedTodayTasks.value,
    0
  )
})


const dailyProgress = computed(() => {

  if (!totalTodayTasks.value) {
    return 0
  }

  return Math.round(
    (
      completedTodayTasks.value /
      totalTodayTasks.value
    ) * 100
  )
})


/* =========================================
   Progress Circle
========================================= */

const circumference = 2 * Math.PI * 48

const progressOffset = computed(() => {
  return (
    circumference -
    (
      circumference *
      dailyProgress.value
    ) / 100
  )
})


/* =========================================
   Study Time
========================================= */

const todayStudyHours = computed(() => {

  const total = todayTasks.value
    .filter(task => task.completed)
    .reduce(
      (sum, task) =>
        sum + (Number(task.studyTime) || 0),
      0
    )

  return formatHoursNumber(total)
})


const monthlyStudyHours = computed(() => {

  const now = new Date()

  const year = now.getFullYear()
  const month = now.getMonth()

  const total = tasks.value
    .filter(task => {

      if (
        !task.completed ||
        !task.dueDate
      ) {
        return false
      }

      const date = new Date(
        `${task.dueDate}T00:00:00`
      )

      return (
        date.getFullYear() === year &&
        date.getMonth() === month
      )
    })
    .reduce(
      (sum, task) =>
        sum + (Number(task.studyTime) || 0),
      0
    )

  return formatHoursNumber(total)
})


function formatHoursNumber(hours) {

  const value = Number(hours) || 0

  if (value === 0) {
    return '۰'
  }

  if (Number.isInteger(value)) {
    return toPersianNumber(value)
  }

  return toPersianNumber(
    value.toFixed(1)
  )
}


/* =========================================
   Global Task Statistics
========================================= */

const completedTaskCount = computed(() => {
  return tasks.value.filter(
    task => task.completed
  ).length
})


const productivity = computed(() => {

  if (!tasks.value.length) {
    return 0
  }

  return Math.round(
    (
      completedTaskCount.value /
      tasks.value.length
    ) * 100
  )
})


/* =========================================
   Streak
   بر اساس تاریخ dueDate تسک‌های تکمیل‌شده
========================================= */

const streakDays = computed(() => {

  const completedDates = new Set(
    tasks.value
      .filter(
        task =>
          task.completed &&
          task.dueDate
      )
      .map(task => task.dueDate)
  )

  if (!completedDates.size) {
    return 0
  }

  let cursor = new Date()

  /*
    اگر امروز مطالعه‌ای ثبت نشده،
    از دیروز شروع می‌کنیم.
  */
  const todayKey = cursor
    .toISOString()
    .split('T')[0]

  if (!completedDates.has(todayKey)) {
    cursor.setDate(
      cursor.getDate() - 1
    )
  }

  let streak = 0

  while (true) {

    const key = cursor
      .toISOString()
      .split('T')[0]

    if (!completedDates.has(key)) {
      break
    }

    streak++

    cursor.setDate(
      cursor.getDate() - 1
    )
  }

  return streak
})


/* =========================================
   Category
========================================= */

function getCategoryName(id) {

  if (!id || id === 'general') {
    return 'عمومی'
  }

  const list = lists.value.find(
    item => String(item.id) === String(id)
  )

  return list?.name || 'عمومی'
}


/* =========================================
   Time Formatting
========================================= */

function formatTime(time) {

  if (!time) {
    return ''
  }

  const [hours, minutes] =
    String(time)
      .slice(0, 5)
      .split(':')

  if (
    hours === undefined ||
    minutes === undefined
  ) {
    return time
  }

  return toPersianNumber(
    `${hours}:${minutes}`
  )
}


function formatStudyTime(hours) {

  const value =
    Number(hours) || 0

  if (value < 1) {

    return `${toPersianNumber(
      Math.round(value * 60)
    )} دقیقه`
  }

  if (
    Number.isInteger(value)
  ) {

    return `${toPersianNumber(
      value
    )} ساعت`
  }

  const wholeHours =
    Math.floor(value)

  const minutes =
    Math.round(
      (value - wholeHours) * 60
    )

  if (!wholeHours) {
    return `${toPersianNumber(
      minutes
    )} دقیقه`
  }

  if (!minutes) {
    return `${toPersianNumber(
      wholeHours
    )} ساعت`
  }

  return `${toPersianNumber(
    wholeHours
  )} ساعت و ${toPersianNumber(
    minutes
  )} دقیقه`
}


/* =========================================
   Persian Number
========================================= */

function toPersianNumber(value) {

  return String(value)
    .replace(
      /\d/g,
      digit =>
        '۰۱۲۳۴۵۶۷۸۹'[
          Number(digit)
        ]
    )
}


/* =========================================
   API Task Payload
   دقیقاً مطابق Planner
========================================= */

function toApiTask(task) {

  const listId =
    task.category
      ? Number(task.category)
      : null

  return {

    title: task.title,

    description:
      task.description || '',

    completed:
      !!task.completed,

    important:
      !!task.important,

    category:
      task.category || '',

    due_date:
      task.dueDate || null,

    start_time:
      task.startTime || null,

    end_time:
      task.endTime || null,

    reminder:
      task.reminder || 'none',

    time_category:
      task.timeCategory || '',

    study_time:
      Number(task.studyTime) || 0,

    planner_list:
      Number.isFinite(listId)
        ? listId
        : null
  }
}


/* =========================================
   Toggle Task
========================================= */

async function toggleTask(task) {

  if (
    updatingTaskId.value !== null
  ) {
    return
  }

  const oldTask = {
    ...task
  }

  const nextTask = {
    ...task,

    completed:
      !task.completed
  }

  /*
    اول UI را سریع تغییر می‌دهیم
    تا تجربه کاربری روان باشد.
  */
  const index =
    tasks.value.findIndex(
      item =>
        String(item.id) ===
        String(task.id)
    )

  if (index < 0) {
    return
  }

  tasks.value[index] = nextTask

  updatingTaskId.value =
    task.id

  try {

    const saved =
      await apiUpdateTask(
        nextTask.id,
        toApiTask(nextTask)
      )

    /*
      پاسخ واقعی Backend را دوباره
      normalize می‌کنیم.
    */
    tasks.value[index] =
      normalizeTask(saved)

    showToast(
      tasks.value[index].completed
        ? 'تسک انجام شد ✓'
        : 'تسک به حالت انجام‌نشده برگشت'
    )

  } catch (err) {

    console.error(
      'خطا در تغییر وضعیت Task:',
      err
    )

    /*
      اگر Backend خطا داد،
      وضعیت قبلی برمی‌گردد.
    */
    tasks.value[index] =
      oldTask

    showToast(
      'ذخیره وضعیت تسک انجام نشد.',
      'error'
    )

  } finally {

    updatingTaskId.value =
      null
  }
}


/* =========================================
   Navigation
========================================= */

function goToPlanner() {
  router.push('/planner')
}


/* =========================================
   Toast
========================================= */

const toast = ref({
  visible: false,
  message: '',
  type: 'success'
})

let toastTimer = null

function showToast(
  message,
  type = 'success'
) {

  toast.value = {
    visible: true,
    message,
    type
  }

  clearTimeout(toastTimer)

  toastTimer = setTimeout(() => {

    toast.value.visible = false

  }, 2200)
}


/* =========================================
   Theme
   هماهنگ با سیستم تم سراسری پروژه
========================================= */
const isDark = ref(false)
let themeObserver = null

function detectDarkTheme() {
  const root = document.documentElement
  const body = document.body

  const dataTheme =
    root.getAttribute('data-theme') ||
    body?.getAttribute('data-theme')

  if (dataTheme === 'dark') return true
  if (dataTheme === 'light') return false

  if (root.classList.contains('dark')) return true
  if (body?.classList.contains('dark')) return true
  if (root.classList.contains('dark-mode')) return true
  if (body?.classList.contains('dark-mode')) return true

  return false
}

function syncTheme() {
  isDark.value = detectDarkTheme()
}

function initThemeWatcher() {
  syncTheme()

  themeObserver = new MutationObserver(() => {
    syncTheme()
  })

  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style']
  })

  if (document.body) {
    themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'data-theme', 'style']
    })
  }
}

/* =========================================
   Initial Load
========================================= */

onMounted(() => {
  initThemeWatcher()
  loadHomeData()
})

onBeforeUnmount(() => {
  themeObserver?.disconnect()
  themeObserver = null
})
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');


/* =========================================
   BASE
========================================= */

.home-page {
  min-height: 100vh;

  background:
    linear-gradient(
      180deg,
      #f8fafc 0%,
      #f8fafc 65%,
      var(--primary-50) 100%
    );

  color: #0f172a;

  font-family:
    Vazirmatn,
    sans-serif;

  --home-card: #ffffff;
  --home-border: #e5e7eb;
  --home-text: #0f172a;
  --home-muted: #64748b;
  --home-soft: #f8fafc;
  --home-dark: #0f172a;

  --home-shadow:
    0 1px 2px rgba(15, 23, 42, .03),
    0 8px 30px rgba(15, 23, 42, .04);
}


/* =========================================
   DARK MODE
========================================= */

:global(.dark) .home-page {
  background:
    linear-gradient(
      180deg,
      #0b1120 0%,
      #0b1120 65%,
      #111827 100%
    );

  --home-card: #111827;
  --home-border: rgba(148, 163, 184, .16);
  --home-text: #f8fafc;
  --home-muted: #94a3b8;
  --home-soft: #172033;
  --home-dark: #020617;

  --home-shadow:
    0 1px 2px rgba(0, 0, 0, .25),
    0 12px 35px rgba(0, 0, 0, .18);
}


/* =========================================
   WRAPPER
========================================= */

.page-wrapper {
  width: min(1280px, 100%);

  margin:
    0 auto;

  padding:
    24px
    16px
    128px;
}


/* =========================================
   HEADER
========================================= */

.home-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 20px;

  margin-bottom: 24px;
}

.date-row {
  display: flex;

  align-items: center;

  gap: 8px;

  color:
    var(--home-muted);

  font-size: 13px;

  font-weight: 500;

  margin-bottom: 7px;
}

.date-dot {
  opacity: .65;
}

.home-header h1 {
  margin: 0;

  color:
    var(--home-text);

  font-size:
    clamp(24px, 3vw, 30px);

  line-height: 1.45;

  font-weight: 800;
}

.home-header p {
  margin:
    5px 0 0;

  color:
    var(--home-muted);

  font-size: 14px;

  line-height: 1.8;
}


/* =========================================
   NOTIFICATION
========================================= */

.notification-button {
  position: relative;

  width: 44px;
  height: 44px;

  flex: 0 0 44px;

  display: flex;

  align-items: center;

  justify-content: center;

  background:
    var(--home-card);

  color:
    var(--home-text);

  border:
    1px solid var(--home-border);

  border-radius: 12px;

  box-shadow:
    var(--home-shadow);

  text-decoration: none;

  transition:
    transform .2s ease,
    border-color .2s ease,
    box-shadow .2s ease;
}

.notification-button:hover {
  transform:
    translateY(-1px);

  border-color:
    var(--primary-200);

  box-shadow:
    0 8px 25px
    rgba(
      var(--primary-rgb),
      .10
    );
}

.notification-button svg {
  width: 21px;
  height: 21px;
}

.notification-dot {
  position: absolute;

  top: 9px;
  right: 9px;

  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #ef4444;

  border:
    2px solid
    var(--home-card);
}


/* =========================================
   LOADING / ERROR
========================================= */

.loading-card,
.error-card {
  display: flex;

  align-items: center;

  justify-content: center;

  flex-direction: column;

  gap: 10px;

  min-height: 180px;

  margin-bottom: 24px;

  background:
    var(--home-card);

  border:
    1px solid var(--home-border);

  border-radius: 20px;

  box-shadow:
    var(--home-shadow);

  color:
    var(--home-muted);

  font-size: 13px;
}

.loading-spinner {
  width: 28px;
  height: 28px;

  border:
    3px solid
    var(--primary-100);

  border-top-color:
    var(--primary);

  border-radius: 50%;

  animation:
    spin .8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-card strong {
  color:
    var(--home-text);

  font-size: 15px;
}

.error-card button {
  margin-top: 5px;

  padding:
    9px 14px;

  border: 0;

  border-radius: 9px;

  background:
    var(--primary);

  color: white;

  font-family: inherit;

  font-size: 12px;

  font-weight: 600;

  cursor: pointer;
}


/* =========================================
   OVERVIEW
========================================= */

.overview-card {
  position: relative;

  overflow: hidden;

  margin-bottom: 24px;

  padding: 32px;

  background:
    #0f172a;

  color: white;

  border-radius: 24px;

  box-shadow:
    0 15px 45px
    rgba(15, 23, 42, .16);
}

.overview-glow {
  position: absolute;

  pointer-events: none;

  border-radius: 999px;

  filter: blur(55px);
}

.overview-glow-left {
  width: 260px;
  height: 260px;

  left: -110px;
  top: -130px;

  background:
    rgba(
      var(--primary-rgb),
      .23
    );
}

.overview-glow-right {
  width: 280px;
  height: 280px;

  right: -130px;
  bottom: -170px;

  background:
    rgba(
      var(--primary-rgb),
      .20
    );
}

.overview-content {
  position: relative;

  z-index: 1;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 40px;
}

.overview-main {
  min-width: 0;

  max-width: 700px;
}

.status-pill {
  display: inline-flex;

  align-items: center;

  gap: 8px;

  padding:
    7px 11px;

  background:
    rgba(255,255,255,.07);

  border:
    1px solid
    rgba(255,255,255,.08);

  border-radius: 999px;

  color: #cbd5e1;

  font-size: 12px;

  font-weight: 500;
}

.status-pill span {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #34d399;

  box-shadow:
    0 0 0 4px
    rgba(52,211,153,.10);
}

.overview-card h2 {
  margin:
    17px 0 10px;

  font-size:
    clamp(25px, 4vw, 36px);

  line-height: 1.6;

  font-weight: 800;

  letter-spacing:
    -.5px;
}

.overview-card p {
  max-width: 650px;

  margin: 0;

  color: #94a3b8;

  font-size: 14px;

  line-height: 2;
}

.overview-actions {
  display: flex;

  align-items: center;

  gap: 10px;

  margin-top: 22px;
}

.overview-primary-button,
.overview-secondary-button {
  display: inline-flex;

  align-items: center;

  justify-content: center;

  min-height: 42px;

  padding:
    10px 16px;

  border-radius: 10px;

  font-family: inherit;

  font-size: 13px;

  font-weight: 600;

  text-decoration: none;

  transition:
    transform .2s ease,
    background .2s ease;
}

.overview-primary-button {
  background: white;

  color: #0f172a;
}

.overview-primary-button:hover {
  background: #f8fafc;

  transform:
    translateY(-1px);
}

.overview-secondary-button {
  background:
    rgba(255,255,255,.07);

  color: #e2e8f0;

  border:
    1px solid
    rgba(255,255,255,.10);
}

.overview-secondary-button:hover {
  background:
    rgba(255,255,255,.12);

  transform:
    translateY(-1px);
}


/* =========================================
   PROGRESS
========================================= */

.progress-wrapper {
  position: relative;

  width: 144px;
  height: 144px;

  flex: 0 0 144px;

  display: flex;

  align-items: center;

  justify-content: center;
}

.progress-circle {
  width: 144px;
  height: 144px;

  transform:
    rotate(-90deg);
}

.progress-track,
.progress-value {
  fill: none;

  stroke-width: 7;
}

.progress-track {
  stroke:
    rgba(255,255,255,.10);
}

.progress-value {
  stroke:
    var(--primary-300);

  stroke-linecap: round;

  stroke-dasharray:
    301.59;

  transition:
    stroke-dashoffset .4s ease;
}

.progress-center {
  position: absolute;

  inset: 0;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;
}

.progress-center strong {
  font-size: 25px;

  line-height: 1.3;

  font-weight: 800;
}

.progress-center span {
  margin-top: 2px;

  color: #94a3b8;

  font-size: 10px;
}


/* =========================================
   STATS
========================================= */

.stats-grid {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 16px;

  margin-bottom: 24px;
}

.stat-card {
  background:
    var(--home-card);

  border:
    1px solid
    var(--home-border);

  border-radius: 20px;

  padding:
    19px 20px;

  box-shadow:
    var(--home-shadow);

  transition:
    transform .2s ease,
    border-color .2s ease,
    box-shadow .2s ease;
}

.stat-card:hover {
  transform:
    translateY(-1px);

  border-color:
    var(--primary-200);

  box-shadow:
    0 12px 30px
    rgba(
      var(--primary-rgb),
      .08
    );
}

.stat-label {
  color:
    var(--home-muted);

  font-size: 12px;

  font-weight: 500;
}

.stat-value {
  margin-top: 8px;

  color:
    var(--home-text);

  font-size: 26px;

  line-height: 1.3;

  font-weight: 800;
}

.stat-footer {
  margin-top: 5px;

  color:
    var(--home-muted);

  font-size: 11px;
}

.stat-footer.success {
  color: #10b981;
}

.stat-footer.primary {
  color:
    var(--primary);
}


/* =========================================
   TASKS
========================================= */

.tasks-grid {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 16px;
}

.tasks-card {
  overflow: hidden;

  background:
    var(--home-card);

  border:
    1px solid
    var(--home-border);

  border-radius: 20px;

  box-shadow:
    var(--home-shadow);
}

.tasks-card-header {
  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  gap: 15px;

  padding:
    20px 20px 15px;
}

.tasks-card-header h3 {
  margin: 0;

  color:
    var(--home-text);

  font-size: 16px;

  font-weight: 800;
}

.tasks-card-header p {
  margin:
    4px 0 0;

  color:
    var(--home-muted);

  font-size: 11px;
}

.completion-badge,
.tomorrow-badge {
  flex-shrink: 0;

  padding:
    6px 9px;

  border-radius: 999px;

  font-size: 10px;

  font-weight: 600;
}

.completion-badge {
  color:
    var(--primary);

  background:
    var(--primary-50);
}

.tomorrow-badge {
  color:
    var(--home-muted);

  background:
    var(--home-soft);

  border:
    1px solid
    var(--home-border);
}


/* =========================================
   TASK LIST
========================================= */

.task-list {
  border-top:
    1px solid
    var(--home-border);
}

.task-row {
  width: 100%;

  display: flex;

  align-items: center;

  gap: 12px;

  padding:
    14px 20px;

  background: transparent;

  border: 0;

  border-bottom:
    1px solid
    var(--home-border);

  color: inherit;

  font-family: inherit;

  text-align: right;

  cursor: pointer;

  transition:
    background .15s ease;

  appearance: none;
}

.task-row:hover:not(:disabled) {
  background:
    var(--home-soft);
}

.task-row:last-child {
  border-bottom: 0;
}

.task-row:disabled {
  cursor: wait;

  opacity: .7;
}

.task-checkbox {
  width: 20px;
  height: 20px;

  flex: 0 0 20px;

  display: flex;

  align-items: center;

  justify-content: center;

  border:
    1.5px solid
    #cbd5e1;

  border-radius: 6px;

  color: white;

  transition:
    background .2s ease,
    border-color .2s ease;
}

.task-checkbox.checked {
  background:
    var(--primary);

  border-color:
    var(--primary);
}

.task-checkbox svg {
  width: 13px;
  height: 13px;
}

.task-checkbox.empty {
  cursor: default;
}

.task-info {
  min-width: 0;

  flex: 1;

  display: flex;

  flex-direction: column;

  gap: 3px;
}

.task-info strong {
  overflow: hidden;

  color:
    var(--home-text);

  font-size: 13px;

  font-weight: 600;

  white-space: nowrap;

  text-overflow: ellipsis;
}

.task-info span {
  color:
    var(--home-muted);

  font-size: 10px;
}

.task-time {
  flex: 0 0 auto;

  color:
    var(--home-muted);

  font-size: 11px;

  font-weight: 500;
}

.task-row.completed
.task-info strong {
  color:
    var(--home-muted);

  text-decoration:
    line-through;
}


/* =========================================
   EMPTY
========================================= */

.empty-tasks {
  min-height: 180px;

  padding:
    25px 20px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  text-align: center;

  gap: 6px;

  color:
    var(--home-muted);
}

.empty-tasks strong {
  color:
    var(--home-text);

  font-size: 13px;
}

.empty-tasks > span:last-child {
  font-size: 11px;
}

.empty-icon {
  width: 38px;
  height: 38px;

  display: flex;

  align-items: center;

  justify-content: center;

  margin-bottom: 4px;

  border-radius: 50%;

  background:
    var(--primary-50);

  color:
    var(--primary);

  font-size: 18px;

  font-weight: 700;
}

.tomorrow-empty {
  font-size: 22px;
}


/* =========================================
   ADD TASK
========================================= */

.add-task-button {
  width: 100%;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 6px;

  padding:
    13px 20px;

  background:
    var(--home-soft);

  border: 0;

  color:
    var(--primary);

  font-family: inherit;

  font-size: 12px;

  font-weight: 600;

  cursor: pointer;

  transition:
    background .15s ease;
}

.add-task-button:hover {
  background:
    var(--primary-50);
}

.add-task-button span {
  font-size: 17px;

  line-height: 1;
}


/* =========================================
   TOAST
========================================= */

.toast {
  position: fixed;

  left: 50%;

  bottom: 95px;

  transform:
    translateX(-50%);

  z-index: 100;

  padding:
    11px 17px;

  background:
    var(--home-dark);

  color: white;

  border:
    1px solid
    rgba(255,255,255,.08);

  border-radius: 10px;

  box-shadow:
    0 15px 40px
    rgba(15,23,42,.25);

  font-size: 12px;

  font-weight: 500;

  white-space: nowrap;
}

.toast.error {
  background: #991b1b;
}

.toast-enter-active,
.toast-leave-active {
  transition:
    opacity .2s ease,
    transform .2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;

  transform:
    translateX(-50%)
    translateY(8px);
}


/* =========================================
   DARK MODE
   این بخش با کلاس داخلی کامپوننت کار می‌کند؛
   بنابراین مستقل از scoped/global selector های پروژه است.
========================================= */
.home-page.home-dark {
  --home-card: #111827;
  --home-border: #263244;
  --home-text: #f8fafc;
  --home-muted: #a8b3c4;
  --home-soft: #172033;
  --home-dark: #020617;

  background:
    radial-gradient(
      circle at 8% 0%,
      rgba(var(--primary-rgb), .08),
      transparent 30%
    ),
    radial-gradient(
      circle at 92% 8%,
      rgba(var(--primary-rgb), .055),
      transparent 28%
    ),
    linear-gradient(
      180deg,
      #070d18 0%,
      #0b1120 62%,
      #101827 100%
    );

  color: var(--home-text);
}

.home-page.home-dark .notification-button,
.home-page.home-dark .loading-card,
.home-page.home-dark .error-card,
.home-page.home-dark .stat-card,
.home-page.home-dark .tasks-card {
  background: var(--home-card);
  border-color: var(--home-border);
  color: var(--home-text);
}

.home-page.home-dark .notification-button:hover,
.home-page.home-dark .stat-card:hover {
  border-color: var(--primary);
  box-shadow: 0 12px 30px rgba(var(--primary-rgb), .12);
}

.home-page.home-dark .overview-card {
  background:
    radial-gradient(
      circle at 8% 15%,
      rgba(var(--primary-rgb), .14),
      transparent 34%
    ),
    linear-gradient(135deg, #0b1220 0%, #111827 100%);
  box-shadow:
    0 18px 50px rgba(0, 0, 0, .32),
    inset 0 1px 0 rgba(255,255,255,.035);
}

.home-page.home-dark .overview-card p,
.home-page.home-dark .progress-center span {
  color: #a8b3c4;
}

.home-page.home-dark .overview-primary-button {
  background: var(--primary);
  color: #ffffff;
  box-shadow: 0 8px 24px rgba(var(--primary-rgb), .22);
}

.home-page.home-dark .overview-primary-button:hover {
  background: var(--primary-600, var(--primary));
}

.home-page.home-dark .overview-secondary-button {
  background: rgba(255,255,255,.055);
  color: #e5e7eb;
  border-color: rgba(255,255,255,.12);
}

.home-page.home-dark .progress-track {
  stroke: rgba(255,255,255,.09);
}

.home-page.home-dark .progress-value {
  stroke: var(--primary);
}

.home-page.home-dark .task-row {
  border-color: var(--home-border);
  color: var(--home-text);
}

.home-page.home-dark .task-row:hover:not(:disabled) {
  background: #182235;
}

.home-page.home-dark .task-checkbox {
  border-color: #526176;
  background: transparent;
}

.home-page.home-dark .task-checkbox.checked {
  background: var(--primary);
  border-color: var(--primary);
}

.home-page.home-dark .completion-badge {
  background: rgba(var(--primary-rgb), .14);
  color: var(--primary-300, var(--primary));
}

.home-page.home-dark .tomorrow-badge {
  background: #172033;
  border-color: var(--home-border);
  color: #a8b3c4;
}

.home-page.home-dark .add-task-button {
  background: #172033;
  color: var(--primary);
}

.home-page.home-dark .add-task-button:hover {
  background: rgba(var(--primary-rgb), .13);
}

.home-page.home-dark .empty-icon {
  background: rgba(var(--primary-rgb), .13);
  color: var(--primary);
}

.home-page.home-dark .toast {
  background: #020617;
  border-color: #263244;
  box-shadow: 0 18px 45px rgba(0,0,0,.4);
}

.home-page.home-dark .toast.error {
  background: #7f1d1d;
}

.home-page.home-dark .error-card button {
  color: #ffffff;
}

.home-page.home-dark :focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 1023px) {

  .stats-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .tasks-grid {
    grid-template-columns:
      1fr;
  }
}


@media (max-width: 700px) {

  .page-wrapper {
    padding:
      20px
      14px
      120px;
  }

  .home-header {
    margin-bottom: 20px;
  }

  .home-header h1 {
    font-size: 23px;
  }

  .home-header p {
    font-size: 12px;
  }

  .overview-card {
    padding: 22px;

    border-radius: 20px;
  }

  .overview-content {
    align-items: flex-start;

    flex-direction: column;

    gap: 25px;
  }

  .overview-card h2 {
    font-size: 25px;
  }

  .overview-card p {
    font-size: 12px;
  }

  .desktop-break {
    display: none;
  }

  .progress-wrapper {
    align-self: center;
  }
}


@media (max-width: 480px) {

  .stats-grid {
    gap: 10px;
  }

  .stat-card {
    padding: 15px;

    border-radius: 16px;
  }

  .stat-value {
    font-size: 22px;
  }

  .stat-label {
    font-size: 11px;
  }

  .overview-actions {
    flex-direction: column;

    align-items: stretch;
  }

  .overview-primary-button,
  .overview-secondary-button {
    width: 100%;
  }

  .task-row {
    padding:
      13px 14px;
  }

  .tasks-card-header {
    padding:
      17px 14px 13px;
  }
}
</style>