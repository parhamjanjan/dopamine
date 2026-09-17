```vue
<template>
  <div class="exams-page-wrapper mb-12" dir="rtl">
    <section
      class="exams-page"
      :class="{ 'is-dark': isDark }"
    >

      <!-- =========================
           TOP BAR
      ========================== -->
      <header class="page-header">

        <div class="header-main">

          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 4.5A2.5 2.5 0 0 1 7.5 2H20v17H7.5A2.5 2.5 0 0 0 5 21.5v-17Z"/>
              <path d="M5 4.5V21.5"/>
              <path d="M9 7h7"/>
              <path d="M9 11h7"/>
              <path d="M9 15h4"/>
            </svg>
          </div>

          <div class="header-copy">
            <span class="eyebrow">مرکز ارزیابی</span>

            <h1>
              آزمون‌های دوپامین
            </h1>

            <p>
              آزمون‌های پیش‌رو را ببینید و عملکرد خود را به چالش بکشید.
            </p>
          </div>

        </div>

        <button
          type="button"
          class="refresh-button"
          :disabled="loading"
          @click="loadExams"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            :class="{ spinning: loading }"
          >
            <path d="M20 11a8.1 8.1 0 0 0-14.9-3.8L3 10"/>
            <path d="M3 5v5h5"/>
            <path d="M4 13a8.1 8.1 0 0 0 14.9 3.8L21 14"/>
            <path d="M21 19v-5h-5"/>
          </svg>

          <span>به‌روزرسانی</span>
        </button>

      </header>


      <!-- =========================
           STATS
      ========================== -->
      <section
        v-if="!loading && !errorMessage && exams.length"
        class="stats-grid"
      >

        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="4" width="18" height="17" rx="2"/>
              <path d="M8 2v4"/>
              <path d="M16 2v4"/>
              <path d="M3 10h18"/>
            </svg>
          </div>

          <div>
            <span>کل آزمون‌ها</span>
            <strong>{{ toPersianNumber(exams.length) }}</strong>
          </div>
        </div>


        <div class="stat-card">
          <div class="stat-icon upcoming">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="9"/>
              <path d="M12 7v5l3 2"/>
            </svg>
          </div>

          <div>
            <span>پیش‌رو</span>
            <strong>{{ toPersianNumber(upcomingCount) }}</strong>
          </div>
        </div>


        <div class="stat-card">
          <div class="stat-icon running">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 12h14"/>
              <path d="m13 6 6 6-6 6"/>
            </svg>
          </div>

          <div>
            <span>در حال برگزاری</span>
            <strong>{{ toPersianNumber(runningCount) }}</strong>
          </div>
        </div>


        <div class="stat-card">
          <div class="stat-icon completed">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 4h16v16H4z"/>
              <path d="m8 12 3 3 5-6"/>
            </svg>
          </div>

          <div>
            <span>شرکت کرده‌اید</span>
            <strong>{{ toPersianNumber(attemptedCount) }}</strong>
          </div>
        </div>

      </section>


      <!-- =========================
           FILTER
      ========================== -->
      <section
        v-if="!loading && !errorMessage"
        class="filters-section"
      >

        <div class="section-heading">
          <div>
            <span>دسته‌بندی آزمون‌ها</span>
            <strong>انتخاب آزمون</strong>
          </div>

          <span class="result-count">
            {{ toPersianNumber(filteredExams.length) }}
            آزمون
          </span>
        </div>


        <div class="category-tabs">

          <button
            type="button"
            class="category-tab"
            :class="{ active: selectedCategory === 'all' }"
            @click="selectedCategory = 'all'"
          >
            <span class="tab-symbol">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 6h16"/>
                <path d="M4 12h16"/>
                <path d="M4 18h16"/>
              </svg>
            </span>

            <span>همه</span>

            <small>
              {{ toPersianNumber(exams.length) }}
            </small>
          </button>


          <button
            v-for="category in categories"
            :key="category.value"
            type="button"
            class="category-tab"
            :class="[
              getCategoryTabClass(category.value),
              {
                active:
                  selectedCategory === category.value
              }
            ]"
            @click="selectedCategory = category.value"
          >

            <span class="tab-symbol">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 5h16v14H4z"/>
                <path d="M8 9h8"/>
                <path d="M8 13h5"/>
              </svg>
            </span>

            <span>
              {{ category.label }}
            </span>

            <small>
              {{ toPersianNumber(category.count) }}
            </small>

          </button>

        </div>

      </section>


      <!-- =========================
           LOADING
      ========================== -->
      <div
        v-if="loading"
        class="state-card"
      >

        <div class="loading-animation">
          <span></span>
          <span></span>
          <span></span>
        </div>

        <h3>در حال دریافت آزمون‌ها</h3>

        <p>
          اطلاعات آزمون‌ها در حال دریافت است...
        </p>

      </div>


      <!-- =========================
           ERROR
      ========================== -->
      <div
        v-else-if="errorMessage"
        class="state-card error-state"
      >

        <div class="state-icon error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 3 2.8 19a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L12 3Z"/>
            <path d="M12 9v4"/>
            <path d="M12 17h.01"/>
          </svg>
        </div>

        <h3>دریافت آزمون‌ها ناموفق بود</h3>

        <p>
          {{ errorMessage }}
        </p>

        <button
          type="button"
          class="state-button"
          @click="loadExams"
        >
          تلاش دوباره
        </button>

      </div>


      <!-- =========================
           EMPTY
      ========================== -->
      <div
        v-else-if="filteredExams.length === 0"
        class="state-card"
      >

        <div class="state-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="4" y="3" width="16" height="18" rx="2.5"/>
            <path d="M8 8h8"/>
            <path d="M8 12h8"/>
            <path d="M8 16h5"/>
          </svg>
        </div>

        <h3>آزمونی برای نمایش وجود ندارد</h3>

        <p>
          در این دسته‌بندی هنوز آزمونی ثبت نشده است.
        </p>

      </div>


      <!-- =========================
           EXAMS
      ========================== -->
      <section
        v-else
        class="exam-grid"
      >

        <article
          v-for="exam in filteredExams"
          :key="exam.id"
          class="exam-card"
          :class="{
            'is-running': getExamState(exam) === 'running',
            'is-ended': getExamState(exam) === 'ended'
          }"
        >

          <!-- CARD TOP -->
          <div class="card-top">

            <div
              class="provider-badge"
              :class="getCategoryClass(exam.category)"
            >
              <span></span>
              {{ getCategoryLabel(exam) }}
            </div>

            <div
              class="status-badge"
              :class="getStatusClass(exam)"
            >
              <i></i>
              {{ getStatusLabel(exam) }}
            </div>

          </div>


          <!-- TITLE -->
          <div class="exam-heading">

            <h2>
              {{ exam.title }}
            </h2>

            <p v-if="exam.description">
              {{ exam.description }}
            </p>

          </div>


          <!-- DATE -->
          <div class="exam-date">

            <div class="date-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="17" rx="2"/>
                <path d="M8 2v4"/>
                <path d="M16 2v4"/>
                <path d="M3 10h18"/>
              </svg>
            </div>

            <div class="date-content">

              <span>تاریخ و زمان برگزاری</span>

              <strong>
                {{ formatFullDate(exam.start_at) }}
              </strong>

              <div class="date-time">
                <span>
                  {{ formatTime(exam.start_at) }}
                </span>

                <b>←</b>

                <span>
                  {{ formatTime(exam.end_at) }}
                </span>
              </div>

            </div>

          </div>


          <!-- INFO -->
          <div class="exam-info-grid">

            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="9"/>
                  <path d="M12 7v5l3 2"/>
                </svg>
              </span>

              <div>
                <small>مدت آزمون</small>
                <strong>
                  {{ formatDuration(exam.duration_minutes) }}
                </strong>
              </div>
            </div>


            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M6 4h12"/>
                  <path d="M6 9h12"/>
                  <path d="M6 14h7"/>
                  <path d="M6 19h5"/>
                </svg>
              </span>

              <div>
                <small>تعداد سؤال</small>
                <strong>
                  {{ toPersianNumber(exam.total_questions) }}
                  سؤال
                </strong>
              </div>
            </div>


            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <rect x="4" y="3" width="16" height="18" rx="2"/>
                  <path d="M8 8h8"/>
                  <path d="M8 12h8"/>
                  <path d="M8 16h4"/>
                </svg>
              </span>

              <div>
                <small>دفترچه‌ها</small>
                <strong>
                  {{
                    toPersianNumber(
                      exam.booklet_count ||
                      exam.booklets?.length ||
                      0
                    )
                  }}
                  دفترچه
                </strong>
              </div>
            </div>


            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="9"/>
                  <path d="M8 12h8"/>
                  <path d="M12 8v8"/>
                </svg>
              </span>

              <div>
                <small>وضعیت</small>
                <strong>
                  {{ getStatusLabel(exam) }}
                </strong>
              </div>
            </div>

          </div>


          <!-- BOOKLETS -->
          <div
            v-if="exam.booklets?.length"
            class="booklets"
          >

            <div class="booklets-header">
              <div>
                <span>ساختار آزمون</span>
                <strong>دفترچه‌ها و دروس</strong>
              </div>

              <small>
                {{ toPersianNumber(exam.booklets.length) }}
                دفترچه
              </small>
            </div>


            <div class="booklets-list">

              <div
                v-for="booklet in sortedBooklets(exam.booklets)"
                :key="booklet.id"
                class="booklet"
              >

                <div class="booklet-number">
                  {{ toPersianNumber(booklet.order) }}
                </div>

                <div class="booklet-main">

                  <div class="booklet-title">
                    <strong>
                      {{
                        booklet.title ||
                        `دفترچه ${booklet.order}`
                      }}
                    </strong>

                    <span>
                      {{ booklet.subject }}
                    </span>
                  </div>

                  <small>
                    سؤال
                    {{ toPersianNumber(booklet.start_question) }}
                    تا
                    {{ toPersianNumber(booklet.end_question) }}
                    <b>•</b>
                    {{ toPersianNumber(booklet.question_count) }}
                    سؤال
                  </small>

                </div>

              </div>

            </div>

          </div>


          <!-- NO BOOKLETS -->
          <div
            v-else
            class="no-booklets"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 5h16v14H4z"/>
              <path d="M8 9h8"/>
              <path d="M8 13h5"/>
            </svg>

            <span>
              اطلاعات دفترچه‌های این آزمون ثبت نشده است.
            </span>
          </div>


          <!-- ACTIVE -->
          <div
            v-if="isInProgress(exam)"
            class="attempt-banner"
          >

            <div class="attempt-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/>
                <path d="M12 7v5l3 2"/>
              </svg>
            </div>

            <div>
              <strong>آزمون شما نیمه‌تمام است</strong>
              <span>می‌توانید از همین‌جا ادامه دهید.</span>
            </div>

          </div>


          <!-- RESULT -->
          <div
            v-if="hasResult(exam)"
            class="result-banner"
          >

            <div class="result-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 19V5"/>
                <path d="M4 19h16"/>
                <path d="m7 15 3-4 3 2 5-7"/>
              </svg>
            </div>

            <div>
              <strong>کارنامه آزمون آماده است</strong>
              <span>نتیجه و عملکرد خود را مشاهده کنید.</span>
            </div>

          </div>


          <!-- FOOTER -->
          <footer class="exam-footer">

            <div class="footer-message">
              {{ getFooterText(exam) }}
            </div>

            <div class="footer-actions">

              <button
                v-if="hasResult(exam)"
                type="button"
                class="result-button"
                @click="viewResult(exam)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M4 19V5"/>
                  <path d="M4 19h16"/>
                  <path d="m7 15 3-4 3 2 5-7"/>
                </svg>

                مشاهده کارنامه
              </button>


              <button
                v-if="canStartExam(exam)"
                type="button"
                class="start-button"
                @click="startExam(exam)"
              >

                <span>
                  {{
                    isInProgress(exam)
                      ? 'ادامه آزمون'
                      : 'شروع آزمون'
                  }}
                </span>

                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="m15 18-6-6 6-6"/>
                </svg>

              </button>


              <button
                v-else
                type="button"
                class="disabled-button"
                disabled
              >
                {{ getActionText(exam) }}
              </button>

            </div>

          </footer>

        </article>

      </section>


      <!-- =========================
           MODAL
      ========================== -->
      <Transition name="modal">

        <div
          v-if="selectedExam"
          class="modal-overlay"
          @click.self="closeExamDetails"
        >

          <div class="exam-modal">

            <button
              type="button"
              class="modal-close"
              @click="closeExamDetails"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m6 6 12 12"/>
                <path d="m18 6-12 12"/>
              </svg>
            </button>


            <div class="modal-top">

              <div
                class="provider-badge"
                :class="getCategoryClass(selectedExam.category)"
              >
                <span></span>
                {{ getCategoryLabel(selectedExam) }}
              </div>

              <div
                class="status-badge"
                :class="getStatusClass(selectedExam)"
              >
                <i></i>
                {{ getStatusLabel(selectedExam) }}
              </div>

            </div>


            <h2>
              {{ selectedExam.title }}
            </h2>

            <p
              v-if="selectedExam.description"
              class="modal-description"
            >
              {{ selectedExam.description }}
            </p>


            <div class="modal-date-grid">

              <div>
                <span>شروع آزمون</span>
                <strong>
                  {{ formatFullDate(selectedExam.start_at) }}
                </strong>
                <small>
                  {{ formatTime(selectedExam.start_at) }}
                </small>
              </div>

              <div>
                <span>پایان آزمون</span>
                <strong>
                  {{ formatFullDate(selectedExam.end_at) }}
                </strong>
                <small>
                  {{ formatTime(selectedExam.end_at) }}
                </small>
              </div>

            </div>


            <div
              v-if="selectedExam.booklets?.length"
              class="modal-booklets"
            >

              <div class="modal-section-header">
                <strong>دفترچه‌های آزمون</strong>

                <span>
                  {{ toPersianNumber(selectedExam.booklets.length) }}
                  دفترچه
                </span>
              </div>

              <div
                v-for="booklet in sortedBooklets(selectedExam.booklets)"
                :key="booklet.id"
                class="modal-booklet"
              >

                <div>
                  {{ toPersianNumber(booklet.order) }}
                </div>

                <section>
                  <strong>
                    {{
                      booklet.title ||
                      `دفترچه ${booklet.order}`
                    }}
                  </strong>

                  <span>
                    {{ booklet.subject }}
                  </span>

                  <small>
                    {{ toPersianNumber(booklet.question_count) }}
                    سؤال
                  </small>
                </section>

              </div>

            </div>


            <div class="modal-stats">

              <div>
                <span>مدت آزمون</span>
                <strong>
                  {{ formatDuration(selectedExam.duration_minutes) }}
                </strong>
              </div>

              <div>
                <span>تعداد سؤال</span>
                <strong>
                  {{ toPersianNumber(selectedExam.total_questions) }}
                </strong>
              </div>

            </div>


            <div class="modal-actions">

              <button
                type="button"
                class="modal-secondary"
                @click="closeExamDetails"
              >
                بستن
              </button>

              <button
                v-if="hasResult(selectedExam)"
                type="button"
                class="modal-result"
                @click="viewResult(selectedExam)"
              >
                مشاهده کارنامه
              </button>

              <button
                v-if="canStartExam(selectedExam)"
                type="button"
                class="modal-primary"
                @click="startExam(selectedExam)"
              >
                {{
                  isInProgress(selectedExam)
                    ? 'ادامه آزمون'
                    : 'شروع آزمون'
                }}
              </button>

            </div>

          </div>

        </div>

      </Transition>

    </section>
  </div>
</template>


<script setup>

import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
} from 'vue'

import {
  useRouter,
} from 'vue-router'

import api from '../services/api'


/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()


/* =========================================================
   STATE
========================================================= */

const exams = ref([])
const loading = ref(false)
const errorMessage = ref('')
const selectedCategory = ref('all')
const selectedExam = ref(null)
const isDark = ref(false)


/* =========================================================
   THEME
========================================================= */

let themeObserver = null

function detectDark() {

  const root = document.documentElement
  const body = document.body

  const dataTheme =
    root.getAttribute('data-theme') ||
    body?.getAttribute('data-theme')

  return (
    dataTheme === 'dark' ||
    root.classList.contains('dark') ||
    body?.classList.contains('dark') ||
    root.classList.contains('dark-mode') ||
    body?.classList.contains('dark-mode')
  )
}


function observeTheme() {

  isDark.value = detectDark()

  themeObserver = new MutationObserver(() => {
    isDark.value = detectDark()
  })

  themeObserver.observe(
    document.documentElement,
    {
      attributes: true,
      attributeFilter: [
        'class',
        'data-theme',
        'style',
      ],
    }
  )

  if (document.body) {

    themeObserver.observe(
      document.body,
      {
        attributes: true,
        attributeFilter: [
          'class',
          'data-theme',
          'style',
        ],
      }
    )

  }
}


/* =========================================================
   API
========================================================= */

function getAccessToken() {

  return (
    localStorage.getItem('access_token') ||
    ''
  )

}



/* =========================================================
   LOAD
========================================================= */

async function loadExams() {

  if (loading.value) {
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {


    const response =
      await api.get('/exams/')

    const data = response.data

    if (Array.isArray(data)) {

      exams.value = data

    } else if (Array.isArray(data.results)) {

      exams.value = data.results

    } else if (Array.isArray(data.exams)) {

      exams.value = data.exams

    } else {

      exams.value = []

    }

    exams.value.sort(
      (a, b) => {

        const aTime =
          parseDate(a.start_at)?.getTime() || 0

        const bTime =
          parseDate(b.start_at)?.getTime() || 0

        return bTime - aTime
      }
    )

  } catch (error) {

    console.error(
      'EXAMS LOAD ERROR:',
      error
    )

    if (
      error?.response?.status === 401
    ) {

      errorMessage.value =
        'نشست شما منقضی شده است. دوباره وارد حساب کاربری شوید.'

    } else {

      errorMessage.value =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        'در دریافت فهرست آزمون‌ها مشکلی پیش آمد.'

    }

  } finally {

    loading.value = false

  }

}


/* =========================================================
   CATEGORIES
========================================================= */

const categories = computed(() => {

  const map = new Map()

  for (const exam of exams.value) {

    const value =
      exam.category ?? ''

    if (!value) {
      continue
    }

    const label =
      exam.category_label ||
      getCategoryLabel(exam)

    if (!map.has(value)) {

      map.set(
        value,
        {
          value,
          label,
          count: 0,
        }
      )

    }

    map.get(value).count += 1

  }

  return Array.from(
    map.values()
  )

})


/* =========================================================
   FILTERED
========================================================= */

const filteredExams = computed(() => {

  let list = [
    ...exams.value
  ]

  if (
    selectedCategory.value !== 'all'
  ) {

    list = list.filter(
      exam =>
        String(exam.category) ===
        String(selectedCategory.value)
    )

  }

  return list.sort(
    (a, b) => {

      const aTime =
        parseDate(a.start_at)?.getTime() || 0

      const bTime =
        parseDate(b.start_at)?.getTime() || 0

      return bTime - aTime

    }
  )

})


/* =========================================================
   SUMMARY
========================================================= */

const upcomingCount = computed(() =>
  exams.value.filter(
    exam =>
      getExamState(exam) === 'not_started'
  ).length
)


const runningCount = computed(() =>
  exams.value.filter(
    exam =>
      getExamState(exam) === 'running'
  ).length
)


const attemptedCount = computed(() =>
  exams.value.filter(
    exam =>
      hasAttempt(exam)
  ).length
)


/* =========================================================
   CATEGORY
========================================================= */

function getCategoryLabel(examOrCategory) {

  if (
    typeof examOrCategory === 'object'
  ) {

    if (
      examOrCategory.category_label
    ) {

      return examOrCategory.category_label

    }

    examOrCategory =
      examOrCategory.category

  }

  const value =
    String(examOrCategory ?? '')
      .trim()
      .toLowerCase()

  const labels = {

    maz: 'ماز',
    kanoon: 'قلمچی',
    ghalamchi: 'قلمچی',
    kalamchi: 'قلمچی',
    kheilisabz: 'خیلی سبز',
    khilisabz: 'خیلی سبز',
    dopamine: 'دوپامین',
    other: 'سایر',

    'ماز': 'ماز',
    'قلمچی': 'قلمچی',
    'خیلی سبز': 'خیلی سبز',
    'دوپامین': 'دوپامین',
    'سایر': 'سایر',

  }

  return (
    labels[value] ||
    examOrCategory ||
    'آزمون'
  )

}


function getCategoryClass(category) {

  const value =
    String(category ?? '')
      .trim()
      .toLowerCase()

  if (
    value.includes('maz') ||
    value.includes('ماز')
  ) {
    return 'provider-maz'
  }

  if (
    value.includes('kanoon') ||
    value.includes('ghalam') ||
    value.includes('قلم')
  ) {
    return 'provider-kanoon'
  }

  if (
    value.includes('kheilisabz') ||
    value.includes('khilisabz') ||
    value.includes('سبز')
  ) {
    return 'provider-kheilisabz'
  }

  if (
    value.includes('dopamine') ||
    value.includes('دوپامین')
  ) {
    return 'provider-dopamine'
  }

  return 'provider-other'
}


function getCategoryTabClass(category) {

  const value =
    String(category ?? '')
      .trim()
      .toLowerCase()

  if (
    value.includes('maz') ||
    value.includes('ماز')
  ) {
    return 'tab-maz'
  }

  if (
    value.includes('kanoon') ||
    value.includes('ghalam') ||
    value.includes('قلم')
  ) {
    return 'tab-kanoon'
  }

  if (
    value.includes('kheilisabz') ||
    value.includes('khilisabz') ||
    value.includes('سبز')
  ) {
    return 'tab-kheilisabz'
  }

  if (
    value.includes('dopamine') ||
    value.includes('دوپامین')
  ) {
    return 'tab-dopamine'
  }

  return 'tab-other'
}


/* =========================================================
   DATE
========================================================= */

function parseDate(value) {

  if (!value) {
    return null
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(date.getTime())
  ) {
    return null
  }

  return date
}


function formatFullDate(value) {

  const date =
    parseDate(value)

  if (!date) {
    return '—'
  }

  return date.toLocaleDateString(
    'fa-IR-u-ca-persian',
    {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }
  )
}


function formatTime(value) {

  const date =
    parseDate(value)

  if (!date) {
    return '—'
  }

  return date.toLocaleTimeString(
    'fa-IR',
    {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }
  )
}


/* =========================================================
   DURATION
========================================================= */

function formatDuration(minutes) {

  const value =
    Number(minutes)

  if (
    !Number.isFinite(value) ||
    value <= 0
  ) {
    return '—'
  }

  const hours =
    Math.floor(value / 60)

  const remaining =
    value % 60

  if (!hours) {
    return `${toPersianNumber(remaining)} دقیقه`
  }

  if (!remaining) {
    return `${toPersianNumber(hours)} ساعت`
  }

  return (
    `${toPersianNumber(hours)} ساعت و ` +
    `${toPersianNumber(remaining)} دقیقه`
  )
}


/* =========================================================
   STATUS
========================================================= */

function getExamState(exam) {

  const backendStatus =
    exam.status

  if (backendStatus) {

    const value =
      String(backendStatus).toLowerCase()

    if (
      [
        'not_started',
        'upcoming',
        'scheduled',
      ].includes(value)
    ) {
      return 'not_started'
    }

    if (
      [
        'running',
        'active',
        'ongoing',
        'available',
      ].includes(value)
    ) {
      return 'running'
    }

    if (
      [
        'ended',
        'finished',
        'expired',
      ].includes(value)
    ) {
      return 'ended'
    }

    if (value === 'inactive') {
      return 'inactive'
    }

  }

  const now =
    Date.now()

  const start =
    parseDate(exam.start_at)

  const end =
    parseDate(exam.end_at)

  if (
    start &&
    now < start.getTime()
  ) {
    return 'not_started'
  }

  if (
    end &&
    now >= end.getTime()
  ) {
    return 'ended'
  }

  return 'running'
}


function getStatusLabel(exam) {

  const state =
    getExamState(exam)

  if (state === 'not_started') {
    return 'شروع نشده'
  }

  if (state === 'ended') {
    return 'پایان یافته'
  }

  if (state === 'inactive') {
    return 'غیرفعال'
  }

  return 'در حال برگزاری'
}


function getStatusClass(exam) {

  return `status-${getExamState(exam)}`

}


/* =========================================================
   ATTEMPT
========================================================= */

function hasAttempt(exam) {

  return Boolean(
    exam.has_attempt
  )

}


function isInProgress(exam) {

  return (
    exam.attempt_status ===
    'in_progress'
  )

}


function hasResult(exam) {

  if (
    exam.result_available
  ) {
    return true
  }

  return [
    'submitted',
    'expired',
  ].includes(
    exam.attempt_status
  )
}


/* =========================================================
   ACTION
========================================================= */

function canStartExam(exam) {

  if (
    isInProgress(exam)
  ) {
    return true
  }

  if (
    exam.can_start === false
  ) {
    return false
  }

  return (
    getExamState(exam) === 'running' &&
    !hasResult(exam)
  )
}


function getActionText(exam) {

  if (
    isInProgress(exam)
  ) {
    return 'ادامه آزمون'
  }

  const state =
    getExamState(exam)

  if (
    state === 'not_started'
  ) {
    return 'منتظر شروع'
  }

  if (
    state === 'ended'
  ) {
    return 'پایان یافته'
  }

  if (
    hasResult(exam)
  ) {
    return 'شرکت کرده‌اید'
  }

  return 'شروع آزمون'
}


function getFooterText(exam) {

  if (
    isInProgress(exam)
  ) {
    return 'آزمون نیمه‌تمام'
  }

  if (
    hasResult(exam)
  ) {
    return 'کارنامه شما آماده مشاهده است'
  }

  const state =
    getExamState(exam)

  if (
    state === 'not_started'
  ) {
    return `شروع در ${formatTime(exam.start_at)}`
  }

  if (
    state === 'ended'
  ) {
    return 'زمان شرکت در آزمون به پایان رسیده است'
  }

  return 'آزمون اکنون قابل انجام است'
}


/* =========================================================
   BOOKLETS
========================================================= */

function sortedBooklets(booklets) {

  if (!Array.isArray(booklets)) {
    return []
  }

  return [
    ...booklets
  ].sort(
    (a, b) =>
      Number(a.order || 0) -
      Number(b.order || 0)
  )

}


/* =========================================================
   START
========================================================= */

async function startExam(exam) {

  if (
    !canStartExam(exam)
  ) {
    return
  }

  if (
    isInProgress(exam) &&
    exam.attempt_id
  ) {

    await router.push({
      name: 'ExamTaking',
      params: {
        id: exam.id,
      },
      query: {
        attempt:
          exam.attempt_id,
      },
    })

    return
  }

  try {

    
    const response =
      await api.post(
        `/exams/${exam.id}/start/`
      )

    const data =
      response.data || {}

    const attemptId =
      data.id ??
      data.attempt_id ??
      data.attempt?.id

    if (
      attemptId
    ) {

      await router.push({
        name: 'ExamTaking',
        params: {
          id: exam.id,
        },
        query: {
          attempt:
            attemptId,
        },
      })

      return

    }

    await router.push({
      name: 'ExamTaking',
      params: {
        id: exam.id,
      },
    })

  } catch (error) {

    console.error(
      'EXAM START ERROR:',
      error
    )

    const detail =
      error?.response?.data?.detail ||
      error?.response?.data?.message

    alert(
      detail ||
      'شروع آزمون انجام نشد. دوباره تلاش کنید.'
    )

  }

}


/* =========================================================
   RESULT
========================================================= */

async function viewResult(exam) {

  const attemptId =
    exam.attempt_id

  if (!attemptId) {

    alert(
      'کارنامه این آزمون پیدا نشد.'
    )

    return
  }

  try {

    await router.push({
      name: 'ExamResult',
      params: {
        id: attemptId,
      },
    })

  } catch (error) {

    console.error(
      'RESULT ROUTE ERROR:',
      error
    )

  }

}


/* =========================================================
   MODAL
========================================================= */

function openExamDetails(exam) {

  selectedExam.value =
    exam

}


function closeExamDetails() {

  selectedExam.value =
    null

}


/* =========================================================
   PERSIAN NUMBERS
========================================================= */

function toPersianNumber(value) {

  if (
    value === null ||
    value === undefined
  ) {
    return '۰'
  }

  return String(value)
    .replace(
      /\d/g,
      digit =>
        '۰۱۲۳۴۵۶۷۸۹'[
          Number(digit)
        ]
    )
}


/* =========================================================
   CLOCK
========================================================= */

let clockTimer = null

function refreshExamStates() {

  exams.value = [
    ...exams.value
  ]

}


/* =========================================================
   MOUNT
========================================================= */

onMounted(
  async () => {

    observeTheme()

    await loadExams()

    await nextTick()

    clockTimer =
      window.setInterval(
        refreshExamStates,
        30000
      )

  }
)


/* =========================================================
   UNMOUNT
========================================================= */

onBeforeUnmount(
  () => {

    themeObserver?.disconnect()

    themeObserver =
      null

    if (clockTimer) {

      window.clearInterval(
        clockTimer
      )

      clockTimer =
        null
    }

  }
)

</script>


<style scoped>

/* =========================================================
   DOPAMINE EXAMS — DESIGN SYSTEM
   Primary-driven + Dark Mode
========================================================= */

.exams-page-wrapper {
  --exam-primary: var(--primary, #6366f1);

  --exam-primary-rgb: var(
    --primary-rgb,
    99, 102, 241
  );

  --exam-bg: #f6f7fb;
  --exam-surface: #ffffff;
  --exam-surface-2: #f8f9fc;

  --exam-text: #171923;
  --exam-text-soft: #626979;
  --exam-text-muted: #8b92a3;

  --exam-border: #e8eaf0;
  --exam-border-strong: #dfe2ea;

  --exam-shadow:
    0 10px 30px rgba(20, 24, 40, 0.06);

  --exam-shadow-hover:
    0 18px 45px rgba(20, 24, 40, 0.11);

  width: 100%;
  min-height: 100%;
  color: var(--exam-text);
}


/* =========================================================
   DARK MODE
========================================================= */

.exams-page.is-dark {
  --exam-bg: #0c0e13;
  --exam-surface: #14171e;
  --exam-surface-2: #1a1e27;

  --exam-text: #f1f3f7;
  --exam-text-soft: #b0b6c4;
  --exam-text-muted: #7f8797;

  --exam-border: #272c36;
  --exam-border-strong: #343a47;

  --exam-shadow:
    0 14px 35px rgba(0, 0, 0, 0.28);

  --exam-shadow-hover:
    0 20px 50px rgba(0, 0, 0, 0.42);
}


/* =========================================================
   MAIN
========================================================= */

.exams-page {
  min-height: 100vh;
  padding: 30px;
  background:
    radial-gradient(
      circle at 85% 0%,
      rgba(var(--exam-primary-rgb), 0.08),
      transparent 32%
    ),
    var(--exam-bg);

  transition:
    background 0.3s ease,
    color 0.3s ease;
}


/* =========================================================
   HEADER
========================================================= */

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 17px;
}

.header-icon {
  width: 58px;
  height: 58px;
  flex: 0 0 58px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 18px;

  color: var(--exam-primary);

  background:
    linear-gradient(
      145deg,
      rgba(var(--exam-primary-rgb), 0.16),
      rgba(var(--exam-primary-rgb), 0.06)
    );

  border: 1px solid
    rgba(var(--exam-primary-rgb), 0.15);

  box-shadow:
    0 8px 25px
    rgba(var(--exam-primary-rgb), 0.10);
}

.header-icon svg {
  width: 28px;
  height: 28px;
  stroke-width: 1.7;
}

.header-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.eyebrow {
  color: var(--exam-primary);
  font-size: 12px;
  font-weight: 800;
}

.header-copy h1 {
  margin: 0;
  font-size: clamp(24px, 3vw, 32px);
  font-weight: 900;
  letter-spacing: -0.5px;
}

.header-copy p {
  margin: 0;
  color: var(--exam-text-soft);
  font-size: 13px;
}


/* =========================================================
   REFRESH
========================================================= */

.refresh-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  height: 45px;
  padding: 0 17px;

  border: 1px solid var(--exam-border);
  border-radius: 13px;

  color: var(--exam-text-soft);
  background: var(--exam-surface);

  font-family: inherit;
  font-size: 13px;
  font-weight: 700;

  cursor: pointer;

  box-shadow: var(--exam-shadow);

  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.refresh-button:hover:not(:disabled) {
  color: var(--exam-primary);

  border-color:
    rgba(var(--exam-primary-rgb), 0.28);

  transform: translateY(-2px);

  box-shadow:
    0 12px 30px
    rgba(var(--exam-primary-rgb), 0.10);
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-button svg {
  width: 18px;
  height: 18px;
  stroke-width: 1.8;
}

.refresh-button .spinning {
  animation: exam-spin 0.9s linear infinite;
}

@keyframes exam-spin {
  to {
    transform: rotate(360deg);
  }
}


/* =========================================================
   STATS
========================================================= */

.stats-grid {
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 14px;
  margin-bottom: 28px;
}

.stat-card {
  position: relative;

  display: flex;
  align-items: center;
  gap: 13px;

  min-height: 86px;
  padding: 16px;

  background: var(--exam-surface);

  border: 1px solid var(--exam-border);
  border-radius: 18px;

  box-shadow: var(--exam-shadow);

  overflow: hidden;

  transition:
    transform 0.22s ease,
    border-color 0.22s ease,
    box-shadow 0.22s ease;
}

.stat-card::after {
  content: "";

  position: absolute;
  inset-inline-end: -25px;
  bottom: -35px;

  width: 90px;
  height: 90px;

  border-radius: 50%;

  background:
    rgba(var(--exam-primary-rgb), 0.05);

  pointer-events: none;
}

.stat-card:hover {
  transform: translateY(-3px);

  border-color:
    rgba(var(--exam-primary-rgb), 0.18);

  box-shadow: var(--exam-shadow-hover);
}

.stat-icon {
  width: 46px;
  height: 46px;

  flex: 0 0 46px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 14px;

  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.10);
}

.stat-icon svg {
  width: 21px;
  height: 21px;
  stroke-width: 1.8;
}

.stat-icon.upcoming {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.11);
}

.stat-icon.running {
  color: #10b981;
  background: rgba(16, 185, 129, 0.11);
}

.stat-icon.completed {
  color: var(--exam-primary);
  background:
    rgba(var(--exam-primary-rgb), 0.10);
}

.stat-card span {
  display: block;

  color: var(--exam-text-muted);

  font-size: 12px;
  font-weight: 700;

  margin-bottom: 5px;
}

.stat-card strong {
  display: block;

  color: var(--exam-text);

  font-size: 22px;
  font-weight: 900;
}


/* =========================================================
   FILTER
========================================================= */

.filters-section {
  margin-bottom: 25px;
}

.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;

  gap: 15px;

  margin-bottom: 14px;
}

.section-heading > div {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.section-heading span:not(.result-count) {
  color: var(--exam-text-muted);
  font-size: 11px;
  font-weight: 700;
}

.section-heading strong {
  color: var(--exam-text);
  font-size: 18px;
  font-weight: 900;
}

.result-count {
  padding: 6px 11px;

  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.08);

  border-radius: 9px;

  font-size: 11px;
  font-weight: 800;
}

.category-tabs {
  display: flex;
  align-items: center;
  gap: 9px;

  overflow-x: auto;

  padding: 5px;

  background: var(--exam-surface);

  border: 1px solid var(--exam-border);
  border-radius: 17px;

  box-shadow: var(--exam-shadow);

  scrollbar-width: none;
}

.category-tabs::-webkit-scrollbar {
  display: none;
}

.category-tab {
  position: relative;

  display: inline-flex;
  align-items: center;
  gap: 8px;

  min-height: 42px;

  padding: 0 13px;

  flex: 0 0 auto;

  border: 1px solid transparent;
  border-radius: 12px;

  color: var(--exam-text-soft);
  background: transparent;

  font-family: inherit;
  font-size: 12px;
  font-weight: 800;

  cursor: pointer;

  transition:
    color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.category-tab:hover {
  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.06);
}

.category-tab.active {
  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.10);

  border-color:
    rgba(var(--exam-primary-rgb), 0.14);

  box-shadow:
    inset 0 0 0 1px
    rgba(var(--exam-primary-rgb), 0.025);
}

.tab-symbol {
  width: 25px;
  height: 25px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 8px;

  background:
    rgba(var(--exam-primary-rgb), 0.08);
}

.tab-symbol svg {
  width: 14px;
  height: 14px;
  stroke-width: 1.8;
}

.category-tab small {
  min-width: 21px;
  height: 21px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  padding: 0 5px;

  border-radius: 7px;

  color: var(--exam-text-muted);
  background: var(--exam-surface-2);

  font-size: 10px;
}


/* =========================================================
   EXAM GRID
========================================================= */

.exam-grid {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 18px;
}


/* =========================================================
   EXAM CARD
========================================================= */

.exam-card {
  position: relative;

  display: flex;
  flex-direction: column;

  min-width: 0;

  padding: 21px;

  background:
    linear-gradient(
      180deg,
      var(--exam-surface),
      var(--exam-surface)
    );

  border: 1px solid var(--exam-border);
  border-radius: 22px;

  box-shadow: var(--exam-shadow);

  overflow: hidden;

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.exam-card::before {
  content: "";

  position: absolute;

  inset-inline-start: 0;
  top: 0;

  width: 100%;
  height: 3px;

  background:
    linear-gradient(
      90deg,
      transparent,
      var(--exam-primary),
      transparent
    );

  opacity: 0;

  transition: opacity 0.25s ease;
}

.exam-card:hover {
  transform: translateY(-4px);

  box-shadow: var(--exam-shadow-hover);

  border-color:
    rgba(var(--exam-primary-rgb), 0.18);
}

.exam-card:hover::before {
  opacity: 1;
}

.exam-card.is-running {
  border-color:
    rgba(16, 185, 129, 0.22);
}

.exam-card.is-running::before {
  background:
    linear-gradient(
      90deg,
      transparent,
      #10b981,
      transparent
    );

  opacity: 0.8;
}

.exam-card.is-ended {
  opacity: 0.82;
}


/* =========================================================
   CARD TOP
========================================================= */

.card-top,
.modal-top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 10px;

  margin-bottom: 17px;
}

.provider-badge,
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;

  min-height: 28px;

  padding: 0 9px;

  border-radius: 9px;

  font-size: 10px;
  font-weight: 850;
}

.provider-badge span {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: currentColor;
}

.provider-other {
  color: var(--exam-primary);
  background:
    rgba(var(--exam-primary-rgb), 0.09);
}

.provider-dopamine {
  color: var(--exam-primary);
  background:
    rgba(var(--exam-primary-rgb), 0.09);
}

.provider-maz {
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.10);
}

.provider-kanoon {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.10);
}

.provider-kheilisabz {
  color: #10b981;
  background: rgba(16, 185, 129, 0.10);
}


/* =========================================================
   STATUS
========================================================= */

.status-badge {
  border: 1px solid transparent;
}

.status-badge i {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: currentColor;
}

.status-not_started {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.10);
}

.status-running {
  color: #10b981;
  background: rgba(16, 185, 129, 0.10);
}

.status-ended {
  color: var(--exam-text-muted);
  background:
    rgba(127, 135, 151, 0.10);
}

.status-inactive {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.10);
}


/* =========================================================
   HEADING
========================================================= */

.exam-heading {
  margin-bottom: 17px;
}

.exam-heading h2 {
  margin: 0;

  color: var(--exam-text);

  font-size: 19px;
  line-height: 1.65;

  font-weight: 900;

  letter-spacing: -0.2px;
}

.exam-heading p {
  margin: 6px 0 0;

  color: var(--exam-text-soft);

  font-size: 12px;
  line-height: 1.8;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;

  overflow: hidden;
}


/* =========================================================
   DATE
========================================================= */

.exam-date {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 13px;

  margin-bottom: 14px;

  border:
    1px solid
    rgba(var(--exam-primary-rgb), 0.10);

  border-radius: 15px;

  background:
    linear-gradient(
      135deg,
      rgba(var(--exam-primary-rgb), 0.075),
      rgba(var(--exam-primary-rgb), 0.025)
    );
}

.date-icon {
  width: 40px;
  height: 40px;

  flex: 0 0 40px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--exam-primary);

  border-radius: 11px;

  background:
    rgba(var(--exam-primary-rgb), 0.10);
}

.date-icon svg {
  width: 19px;
  height: 19px;
  stroke-width: 1.8;
}

.date-content {
  min-width: 0;
}

.date-content > span {
  display: block;

  margin-bottom: 3px;

  color: var(--exam-text-muted);

  font-size: 10px;
  font-weight: 700;
}

.date-content > strong {
  display: block;

  color: var(--exam-text);

  font-size: 12px;
  font-weight: 850;
}

.date-time {
  display: flex;
  align-items: center;
  gap: 7px;

  margin-top: 4px;

  color: var(--exam-primary);

  font-size: 11px;
  font-weight: 800;
}

.date-time b {
  opacity: 0.55;
}


/* =========================================================
   INFO GRID
========================================================= */

.exam-info-grid {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 8px;

  margin-bottom: 15px;
}

.exam-info {
  display: flex;
  align-items: center;
  gap: 9px;

  min-width: 0;

  padding: 10px;

  background: var(--exam-surface-2);

  border: 1px solid var(--exam-border);

  border-radius: 12px;
}

.info-icon {
  width: 30px;
  height: 30px;

  flex: 0 0 30px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--exam-primary);

  border-radius: 9px;

  background:
    rgba(var(--exam-primary-rgb), 0.08);
}

.info-icon svg {
  width: 15px;
  height: 15px;
  stroke-width: 1.8;
}

.exam-info > div {
  min-width: 0;
}

.exam-info small {
  display: block;

  color: var(--exam-text-muted);

  font-size: 9px;
  font-weight: 700;

  margin-bottom: 2px;
}

.exam-info strong {
  display: block;

  color: var(--exam-text);

  font-size: 11px;
  font-weight: 850;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}


/* =========================================================
   BOOKLETS
========================================================= */

.booklets {
  padding-top: 16px;

  border-top:
    1px solid var(--exam-border);
}

.booklets-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 10px;

  margin-bottom: 10px;
}

.booklets-header > div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.booklets-header span {
  color: var(--exam-text-muted);
  font-size: 9px;
  font-weight: 700;
}

.booklets-header strong {
  color: var(--exam-text);
  font-size: 12px;
  font-weight: 900;
}

.booklets-header small {
  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.08);

  padding: 5px 8px;

  border-radius: 8px;

  font-size: 9px;
  font-weight: 800;
}

.booklets-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.booklet {
  display: flex;
  align-items: center;
  gap: 9px;

  padding: 9px;

  border:
    1px solid var(--exam-border);

  border-radius: 12px;

  background: var(--exam-surface-2);

  transition:
    border-color 0.2s ease,
    transform 0.2s ease;
}

.booklet:hover {
  transform: translateX(-2px);

  border-color:
    rgba(var(--exam-primary-rgb), 0.18);
}

.booklet-number {
  width: 30px;
  height: 30px;

  flex: 0 0 30px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.09);

  border-radius: 9px;

  font-size: 11px;
  font-weight: 900;
}

.booklet-main {
  min-width: 0;
  flex: 1;
}

.booklet-title {
  display: flex;
  align-items: center;
  gap: 7px;

  min-width: 0;
}

.booklet-title strong {
  color: var(--exam-text);

  font-size: 11px;
  font-weight: 850;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.booklet-title span {
  flex: 0 0 auto;

  padding: 3px 6px;

  color: var(--exam-text-muted);

  background:
    rgba(127, 135, 151, 0.08);

  border-radius: 5px;

  font-size: 8px;
  font-weight: 700;
}

.booklet-main > small {
  display: block;

  margin-top: 3px;

  color: var(--exam-text-muted);

  font-size: 8px;
}

.booklet-main > small b {
  margin: 0 3px;
}


/* =========================================================
   NO BOOKLETS
========================================================= */

.no-booklets {
  display: flex;
  align-items: center;
  gap: 8px;

  padding: 12px;

  border-radius: 12px;

  color: var(--exam-text-muted);

  background: var(--exam-surface-2);

  border: 1px dashed var(--exam-border-strong);

  font-size: 10px;
}

.no-booklets svg {
  width: 17px;
  height: 17px;

  flex: 0 0 17px;

  color: var(--exam-primary);
}


/* =========================================================
   BANNERS
========================================================= */

.attempt-banner,
.result-banner {
  display: flex;
  align-items: center;
  gap: 10px;

  margin-top: 13px;
  padding: 11px;

  border-radius: 13px;
}

.attempt-banner {
  color: #d97706;

  background: rgba(245, 158, 11, 0.08);

  border:
    1px solid rgba(245, 158, 11, 0.14);
}

.result-banner {
  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.075);

  border:
    1px solid
    rgba(var(--exam-primary-rgb), 0.13);
}

.attempt-icon,
.result-icon {
  width: 33px;
  height: 33px;

  flex: 0 0 33px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 9px;

  background: currentColor;
  color: inherit;
}

.attempt-icon svg,
.result-icon svg {
  width: 17px;
  height: 17px;

  stroke: var(--exam-surface);

  stroke-width: 1.9;
}

.attempt-banner > div:last-child,
.result-banner > div:last-child {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.attempt-banner strong,
.result-banner strong {
  font-size: 10px;
  font-weight: 900;
}

.attempt-banner span,
.result-banner span {
  font-size: 9px;
  opacity: 0.75;
}


/* =========================================================
   FOOTER
========================================================= */

.exam-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 12px;

  margin-top: auto;
  padding-top: 17px;

  border-top:
    1px solid var(--exam-border);
}

.footer-message {
  color: var(--exam-text-muted);

  font-size: 10px;
  font-weight: 700;

  line-height: 1.6;
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: 7px;
}

.footer-actions button {
  min-height: 37px;

  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;

  padding: 0 11px;

  border-radius: 10px;

  font-family: inherit;

  font-size: 10px;
  font-weight: 850;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.footer-actions button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.footer-actions svg {
  width: 15px;
  height: 15px;
  stroke-width: 1.9;
}

.result-button {
  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.08);

  border:
    1px solid
    rgba(var(--exam-primary-rgb), 0.14);
}

.result-button:hover {
  background:
    rgba(var(--exam-primary-rgb), 0.13);
}

.start-button {
  color: #fff;

  border: 0;

  background:
    linear-gradient(
      135deg,
      var(--exam-primary),
      color-mix(
        in srgb,
        var(--exam-primary) 78%,
        #000
      )
    );

  box-shadow:
    0 7px 18px
    rgba(var(--exam-primary-rgb), 0.24);
}

.start-button:hover {
  box-shadow:
    0 10px 25px
    rgba(var(--exam-primary-rgb), 0.32);
}

.disabled-button {
  color: var(--exam-text-muted);

  background: var(--exam-surface-2);

  border: 1px solid var(--exam-border);

  cursor: not-allowed !important;
}


/* =========================================================
   STATE
========================================================= */

.state-card {
  min-height: 260px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  padding: 30px;

  text-align: center;

  background: var(--exam-surface);

  border:
    1px solid var(--exam-border);

  border-radius: 22px;

  box-shadow: var(--exam-shadow);
}

.state-card h3 {
  margin: 15px 0 5px;

  color: var(--exam-text);

  font-size: 16px;
  font-weight: 900;
}

.state-card p {
  margin: 0;

  max-width: 430px;

  color: var(--exam-text-muted);

  font-size: 11px;
  line-height: 1.8;
}

.loading-animation {
  display: flex;
  align-items: center;
  gap: 6px;
}

.loading-animation span {
  width: 8px;
  height: 8px;

  border-radius: 50%;

  background: var(--exam-primary);

  animation: exam-loading 1.2s infinite ease-in-out;
}

.loading-animation span:nth-child(2) {
  animation-delay: 0.15s;
}

.loading-animation span:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes exam-loading {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.35;
  }

  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

.state-icon {
  width: 58px;
  height: 58px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--exam-primary);

  border-radius: 17px;

  background:
    rgba(var(--exam-primary-rgb), 0.09);
}

.state-icon.error {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.09);
}

.state-icon svg {
  width: 27px;
  height: 27px;
  stroke-width: 1.7;
}

.state-button {
  margin-top: 17px;

  min-height: 40px;

  padding: 0 17px;

  color: #fff;

  border: 0;
  border-radius: 11px;

  background: var(--exam-primary);

  font-family: inherit;

  font-size: 11px;
  font-weight: 850;

  cursor: pointer;

  box-shadow:
    0 7px 18px
    rgba(var(--exam-primary-rgb), 0.22);

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.state-button:hover {
  transform: translateY(-2px);

  box-shadow:
    0 10px 25px
    rgba(var(--exam-primary-rgb), 0.30);
}


/* =========================================================
   MODAL
========================================================= */

.modal-overlay {
  position: fixed;
  inset: 0;

  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background:
    rgba(7, 9, 14, 0.58);

  backdrop-filter: blur(8px);
}

.exam-modal {
  position: relative;

  width: min(620px, 100%);

  max-height: calc(100vh - 40px);

  overflow-y: auto;

  padding: 25px;

  background: var(--exam-surface);

  border:
    1px solid var(--exam-border);

  border-radius: 24px;

  box-shadow:
    0 30px 80px rgba(0, 0, 0, 0.28);

  scrollbar-width: thin;
}

.modal-close {
  position: absolute;

  top: 18px;
  inset-inline-start: 18px;

  width: 34px;
  height: 34px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--exam-text-muted);

  background: var(--exam-surface-2);

  border:
    1px solid var(--exam-border);

  border-radius: 10px;

  cursor: pointer;

  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.modal-close:hover {
  color: #ef4444;
  transform: rotate(5deg);
}

.modal-close svg {
  width: 17px;
  height: 17px;
}

.exam-modal h2 {
  margin: 0 0 7px;

  padding-inline-start: 40px;

  color: var(--exam-text);

  font-size: 22px;
  font-weight: 900;
  line-height: 1.6;
}

.modal-description {
  margin: 0 0 20px;

  color: var(--exam-text-soft);

  font-size: 11px;
  line-height: 1.9;
}

.modal-date-grid {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 10px;

  margin-bottom: 18px;
}

.modal-date-grid > div {
  display: flex;
  flex-direction: column;
  gap: 4px;

  padding: 13px;

  background: var(--exam-surface-2);

  border:
    1px solid var(--exam-border);

  border-radius: 13px;
}

.modal-date-grid span {
  color: var(--exam-text-muted);

  font-size: 9px;
  font-weight: 700;
}

.modal-date-grid strong {
  color: var(--exam-text);

  font-size: 11px;
  font-weight: 850;
}

.modal-date-grid small {
  color: var(--exam-primary);

  font-size: 10px;
  font-weight: 850;
}


/* =========================================================
   MODAL BOOKLETS
========================================================= */

.modal-booklets {
  padding-top: 17px;

  border-top:
    1px solid var(--exam-border);
}

.modal-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 10px;
}

.modal-section-header strong {
  color: var(--exam-text);

  font-size: 12px;
  font-weight: 900;
}

.modal-section-header span {
  color: var(--exam-primary);

  font-size: 9px;
  font-weight: 800;
}

.modal-booklet {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 10px;

  margin-bottom: 7px;

  border:
    1px solid var(--exam-border);

  border-radius: 12px;

  background: var(--exam-surface-2);
}

.modal-booklet > div {
  width: 31px;
  height: 31px;

  flex: 0 0 31px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.09);

  border-radius: 9px;

  font-size: 10px;
  font-weight: 900;
}

.modal-booklet section {
  display: flex;
  flex-direction: column;
  gap: 2px;

  min-width: 0;
}

.modal-booklet section strong {
  color: var(--exam-text);

  font-size: 10px;
  font-weight: 850;
}

.modal-booklet section span,
.modal-booklet section small {
  color: var(--exam-text-muted);

  font-size: 8px;
}


/* =========================================================
   MODAL STATS
========================================================= */

.modal-stats {
  display: grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap: 10px;

  margin-top: 18px;
}

.modal-stats > div {
  padding: 13px;

  text-align: center;

  background:
    rgba(var(--exam-primary-rgb), 0.055);

  border:
    1px solid
    rgba(var(--exam-primary-rgb), 0.10);

  border-radius: 13px;
}

.modal-stats span {
  display: block;

  margin-bottom: 4px;

  color: var(--exam-text-muted);

  font-size: 9px;
  font-weight: 700;
}

.modal-stats strong {
  color: var(--exam-primary);

  font-size: 14px;
  font-weight: 900;
}


/* =========================================================
   MODAL ACTIONS
========================================================= */

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;

  gap: 8px;

  margin-top: 20px;
}

.modal-actions button {
  min-height: 40px;

  padding: 0 14px;

  border-radius: 11px;

  font-family: inherit;

  font-size: 10px;
  font-weight: 850;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.modal-actions button:hover {
  transform: translateY(-2px);
}

.modal-secondary {
  color: var(--exam-text-soft);

  background: var(--exam-surface-2);

  border:
    1px solid var(--exam-border);
}

.modal-result {
  color: var(--exam-primary);

  background:
    rgba(var(--exam-primary-rgb), 0.08);

  border:
    1px solid
    rgba(var(--exam-primary-rgb), 0.13);
}

.modal-primary {
  color: #fff;

  background: var(--exam-primary);

  border: 0;

  box-shadow:
    0 7px 18px
    rgba(var(--exam-primary-rgb), 0.23);
}


/* =========================================================
   MODAL TRANSITION
========================================================= */

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;
}

.modal-enter-active .exam-modal,
.modal-leave-active .exam-modal {
  transition:
    transform 0.25s ease,
    opacity 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .exam-modal,
.modal-leave-to .exam-modal {
  opacity: 0;
  transform: translateY(15px) scale(0.98);
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1100px) {

  .stats-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .exam-grid {
    grid-template-columns:
      1fr;
  }

}


@media (max-width: 700px) {

  .exams-page {
    padding: 18px 14px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-main {
    width: 100%;
  }

  .refresh-button {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));

    gap: 9px;
  }

  .stat-card {
    min-height: 76px;
    padding: 12px;
    border-radius: 15px;
  }

  .stat-icon {
    width: 38px;
    height: 38px;
    flex-basis: 38px;
  }

  .stat-icon svg {
    width: 18px;
    height: 18px;
  }

  .stat-card strong {
    font-size: 18px;
  }

  .exam-card {
    padding: 16px;
    border-radius: 18px;
  }

  .exam-heading h2 {
    font-size: 17px;
  }

  .exam-footer {
    align-items: stretch;
    flex-direction: column;
  }

  .footer-actions {
    width: 100%;
  }

  .footer-actions button {
    flex: 1;
  }

  .modal-overlay {
    padding: 10px;
  }

  .exam-modal {
    max-height: calc(100vh - 20px);
    padding: 19px;
    border-radius: 20px;
  }

}


@media (max-width: 430px) {

  .header-icon {
    width: 48px;
    height: 48px;
    flex-basis: 48px;
    border-radius: 14px;
  }

  .header-icon svg {
    width: 23px;
    height: 23px;
  }

  .header-copy h1 {
    font-size: 22px;
  }

  .header-copy p {
    font-size: 11px;
  }

  .stats-grid {
    grid-template-columns:
      1fr 1fr;
  }

  .stat-card {
    gap: 8px;
  }

  .stat-card > div:last-child span {
    font-size: 9px;
  }

  .stat-card strong {
    font-size: 17px;
  }

  .exam-info-grid {
    grid-template-columns:
      1fr 1fr;
  }

  .modal-date-grid {
    grid-template-columns:
      1fr;
  }

  .modal-actions {
    flex-direction: column;
  }

  .modal-actions button {
    width: 100%;
  }

}

</style>