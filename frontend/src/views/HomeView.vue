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


<style src="../assets/home.css" scoped></style>