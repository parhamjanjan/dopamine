```vue
<template>
  <div
    class="exam-taking-page"
    dir="rtl"
    :class="{ 'is-dark': isDark }"
  >
    <!-- =========================
         HEADER
    ========================== -->
    <header class="exam-header">
      <div class="exam-header-main">
        <button
          type="button"
          class="back-button"
          @click="leaveExam"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path d="m15 18-6-6 6-6" />
          </svg>
        </button>

        <div class="exam-header-title">
          <span>
            در حال برگزاری آزمون
          </span>

          <h1>
            {{ attempt?.exam_title || 'آزمون' }}
          </h1>
        </div>
      </div>

      <!-- TIMER -->
      <div
        class="exam-timer"
        :class="{
          warning: remainingSeconds <= 300,
          danger: remainingSeconds <= 60
        }"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <circle
            cx="12"
            cy="12"
            r="9"
          />
          <path d="M12 7v5l3 2" />
        </svg>

        <div>
          <span>
            زمان باقی‌مانده
          </span>

          <strong>
            {{ formatTimer(remainingSeconds) }}
          </strong>
        </div>
      </div>
    </header>


    <!-- =========================
         LOADING
    ========================== -->
    <div
      v-if="loading"
      class="state-screen"
    >
      <div class="loader"></div>

      <h2>
        در حال آماده‌سازی آزمون
      </h2>

      <p>
        اطلاعات آزمون در حال دریافت است...
      </p>
    </div>


    <!-- =========================
         ERROR
    ========================== -->
    <div
      v-else-if="errorMessage"
      class="state-screen error-screen"
    >
      <div class="state-icon">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            d="M12 3 2.8 19a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L12 3Z"
          />
          <path d="M12 9v4" />
          <path d="M12 17h.01" />
        </svg>
      </div>

      <h2>
        ورود به آزمون ممکن نبود
      </h2>

      <p>
        {{ errorMessage }}
      </p>

      <button
        type="button"
        class="retry-button"
        @click="loadAttempt"
      >
        تلاش دوباره
      </button>
    </div>


    <!-- =========================
         EXAM
    ========================== -->
    <main
      v-else-if="attempt"
      class="exam-layout"
    >

      <!-- =========================
           PDF AREA
      ========================== -->
      <section class="pdf-section">

        <div class="pdf-toolbar">

          <div class="pdf-title">

            <div class="pdf-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
              >
                <path d="M5 3h10l4 4v14H5z" />
                <path d="M14 3v5h5" />
                <path d="M8 13h8" />
                <path d="M8 17h6" />
              </svg>
            </div>

            <div>
              <strong>
                دفترچه آزمون
              </strong>

              <span>
                سؤال
                {{ toPersianNumber(currentQuestion) }}
                از
                {{ toPersianNumber(totalQuestions) }}
              </span>
            </div>

          </div>

          <div class="pdf-page-indicator">
            صفحه

            <strong>
              {{ toPersianNumber(currentQuestion) }}
            </strong>

            /

            {{ toPersianNumber(totalQuestions) }}
          </div>

        </div>


        <!-- =========================
             PDF.JS VIEWER
        ========================== -->
        <div
          ref="pdfViewerWrapper"
          class="pdf-viewer-wrapper"
        >

          <div
            v-if="pdfLoading"
            class="pdf-loading"
          >
            <div class="loader"></div>

            <span>
              در حال نمایش صفحه...
            </span>
          </div>


          <div
            v-if="pdfError"
            class="pdf-error"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path
                d="M12 3 2.8 19a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L12 3Z"
              />

              <path d="M12 9v4" />
              <path d="M12 17h.01" />
            </svg>

            <strong>
              نمایش PDF با مشکل مواجه شد
            </strong>

            <span>
              {{ pdfError }}
            </span>

            <button
              type="button"
              @click="renderCurrentPage"
            >
              تلاش دوباره
            </button>
          </div>


          <div
            v-show="!pdfError"
            class="pdf-canvas-container"
          >
            <canvas
              ref="pdfCanvas"
              class="pdf-canvas"
            ></canvas>
          </div>

        </div>

      </section>


      <!-- =========================
           ANSWER PANEL
      ========================== -->
      <aside class="answer-panel">

        <div class="question-header">

          <div>
            <span>
              سؤال
            </span>

            <strong>
              {{ toPersianNumber(currentQuestion) }}
            </strong>
          </div>

          <span class="answer-status">
            {{
              currentAnswer
                ? 'پاسخ داده شده'
                : 'بدون پاسخ'
            }}
          </span>

        </div>


        <!-- OPTIONS -->
        <div class="options">

          <button
            v-for="option in options"
            :key="option.value"
            type="button"
            class="option-button"
            :class="{
              selected:
                currentAnswer === option.value
            }"
            @click="selectAnswer(option.value)"
          >

            <span class="option-number">
              {{ option.label }}
            </span>

            <span class="option-text">
              گزینه {{ option.label }}
            </span>

            <span
              v-if="
                currentAnswer === option.value
              "
              class="option-check"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
              >
                <path d="m5 12 4 4L19 6" />
              </svg>
            </span>

          </button>

        </div>


        <!-- QUESTION NAVIGATION -->
        <div class="question-navigation">

          <button
            type="button"
            class="nav-button"
            :disabled="currentQuestion <= 1"
            @click="previousQuestion"
          >

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path d="m15 18-6-6 6-6" />
            </svg>

            سؤال قبل

          </button>


          <div class="question-counter">

            <strong>
              {{ toPersianNumber(currentQuestion) }}
            </strong>

            <span>
              از
              {{ toPersianNumber(totalQuestions) }}
            </span>

          </div>


          <button
            v-if="currentQuestion < totalQuestions"
            type="button"
            class="nav-button primary"
            @click="nextQuestion"
          >

            سؤال بعد

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path d="m9 18 6-6-6-6" />
            </svg>

          </button>


          <button
            v-else
            type="button"
            class="submit-button"
            :disabled="submitting"
            @click="submitExam"
          >

            <span v-if="!submitting">
              ثبت نهایی آزمون
            </span>

            <span v-else>
              در حال ثبت...
            </span>

          </button>

        </div>


        <!-- PROGRESS -->
        


        <!-- SAVE STATUS -->
        <div
          class="save-status"
          :class="{
            saving: saving,
            saved: saved
          }"
        >

          <span class="save-dot"></span>

          <span v-if="saving">
            در حال ذخیره پاسخ...
          </span>

          <span v-else-if="saved">
            پاسخ‌ها ذخیره شده‌اند
          </span>

          <span v-else>
            پاسخ‌ها به‌صورت خودکار ذخیره می‌شوند
          </span>

        </div>

      </aside>

      <div>

<div class="progress-box">

          <div class="progress-header">

            <span>
              پیشرفت آزمون
            </span>

            <strong>
              {{ toPersianNumber(answeredCount) }}
              /
              {{ toPersianNumber(totalQuestions) }}
            </strong>

          </div>

          <div class="progress-track">

            <div
              class="progress-value"
              :style="{
                width: `${progressPercent}%`
              }"
            ></div>

          </div>

        </div>


        <!-- QUESTION GRID -->
        <div class="question-map">

          <div class="question-map-title">
            مرور سؤالات
          </div>

          <div class="question-map-grid">

            <button
              v-for="question in totalQuestions"
              :key="question"
              type="button"
              class="question-number"
              :class="{
                current:
                  question === currentQuestion,

                answered:
                  Boolean(
                    answers[String(question)]
                  )
              }"
              @click="goToQuestion(question)"
            >
              {{ toPersianNumber(question) }}
            </button>

          </div>

        </div>

      </div>

    </main>


    <!-- =========================
         SUBMIT MODAL
    ========================== -->
    <Transition name="fade">

      <div
        v-if="showSubmitModal"
        class="modal-overlay"
      >

        <div class="submit-modal">

          <div class="modal-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path d="M4 4h16v16H4z" />
              <path d="m8 12 3 3 5-6" />
            </svg>

          </div>

          <h2>
            ثبت نهایی آزمون
          </h2>

          <p>
            شما به

            <strong>
              {{ toPersianNumber(answeredCount) }}
            </strong>

            سؤال از

            <strong>
              {{ toPersianNumber(totalQuestions) }}
            </strong>

            سؤال پاسخ داده‌اید.
          </p>

          <p class="modal-warning">
            پس از ثبت نهایی، امکان تغییر پاسخ‌ها وجود نخواهد داشت.
          </p>

          <div class="modal-actions">

            <button
              type="button"
              class="modal-cancel"
              @click="showSubmitModal = false"
            >
              ادامه آزمون
            </button>

            <button
              type="button"
              class="modal-confirm"
              :disabled="submitting"
              @click="confirmSubmit"
            >
              {{
                submitting
                  ? 'در حال ثبت...'
                  : 'ثبت نهایی'
              }}
            </button>

          </div>

        </div>

      </div>

    </Transition>

  </div>
</template>


<script setup>
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  shallowRef,
} from 'vue'

import {
  useRoute,
  useRouter,
} from 'vue-router'

import api from '../services/api'

import * as pdfjsLib from 'pdfjs-dist'


/* =========================================================
   PDF.JS WORKER
========================================================= */

pdfjsLib.GlobalWorkerOptions.workerSrc =
  new URL(
    'pdfjs-dist/build/pdf.worker.min.mjs',
    import.meta.url
  ).toString()


/* =========================================================
   ROUTER
========================================================= */

const route = useRoute()
const router = useRouter()


/* =========================================================
   STATE
========================================================= */

const loading = ref(false)
const submitting = ref(false)

const errorMessage = ref('')

const attempt = ref(null)

const answers = ref({})

const currentQuestion = ref(1)

const remainingSeconds = ref(0)

const questionsPdfUrl = ref('')

const isDark = ref(false)

const saving = ref(false)
const saved = ref(false)

const showSubmitModal = ref(false)


/* =========================================================
   PDF STATE
========================================================= */

/*
  بسیار مهم:

  PDFDocumentProxy نباید داخل ref معمولی قرار بگیرد.

  Vue در صورت reactive کردن آن می‌تواند با private
  fields داخلی PDF.js تداخل ایجاد کند.

  بنابراین document و loading/render task ها
  به صورت متغیر معمولی نگهداری می‌شوند.
*/

let pdfDocument = null
let pdfLoadingTask = null
let pdfRenderTask = null

const pdfCanvas = ref(null)
const pdfViewerWrapper = ref(null)

const pdfLoading = ref(false)
const pdfError = ref('')

/*
  برای جلوگیری از render های قدیمی که بعد از render جدید
  تمام می‌شوند.
*/
let pdfRenderVersion = 0

/*
  آخرین اندازه‌ای که PDF با آن render شده.
  برای جلوگیری از render اضافه هنگام resize.
*/
let lastRenderWidth = 0
let lastRenderHeight = 0

/*
  ResizeObserver از window resize دقیق‌تر است،
  چون تغییر اندازه خود viewer را هم تشخیص می‌دهد.
*/
let pdfResizeObserver = null

/*
  requestAnimationFrame برای resize rendering
*/
let resizeAnimationFrame = null


/* =========================================================
   OPTIONS
========================================================= */

const options = [
  {
    value: 1,
    label: '۱',
  },
  {
    value: 2,
    label: '۲',
  },
  {
    value: 3,
    label: '۳',
  },
  {
    value: 4,
    label: '۴',
  },
]


/* =========================================================
   API
========================================================= */

function getAccessToken() {
  return (
    localStorage.getItem('access_token') ||
    ''
  )
}


function getApiBaseUrl() {
  return (
    import.meta.env.VITE_API_URL ||
    'http://127.0.0.1:8000/api'
  )
}


function createApi() {
  const token =
    getAccessToken()

  return api.create({
    baseURL:
      getApiBaseUrl(),

    headers: {
      'Content-Type':
        'application/json',

      ...(token
        ? {
            Authorization:
              `Bearer ${token}`,
          }
        : {}),
    },
  })
}


/* =========================================================
   IDS
========================================================= */

const examId = computed(() => {
  return route.params.id
})


const attemptId = computed(() => {
  return (
    route.query.attempt ||
    attempt.value?.id
  )
})


/* =========================================================
   EXAM INFO
========================================================= */

const totalQuestions = computed(() => {
  const attemptTotal =
    Number(
      attempt.value?.exam_total_questions
    )

  if (
    Number.isFinite(attemptTotal) &&
    attemptTotal > 0
  ) {
    return attemptTotal
  }

  const total =
    Number(
      attempt.value?.total_questions
    )

  if (
    Number.isFinite(total) &&
    total > 0
  ) {
    return total
  }

  return 0
})


/* =========================================================
   LOAD EXAM INFO
========================================================= */

async function loadExamInfo() {
  try {
    const apiInstance =
      createApi()

    const response =
      await apiInstance.get(
        `/exams/${examId.value}/`
      )

    const exam =
      response.data || {}

    questionsPdfUrl.value =
      exam.questions_pdf_url || ''

    return exam
  } catch (error) {
    console.error(
      'EXAM INFO ERROR:',
      error
    )

    throw error
  }
}


/* =========================================================
   LOAD ATTEMPT
========================================================= */

async function loadAttempt() {
  loading.value = true
  errorMessage.value = ''

  try {
    const apiInstance =
      createApi()


    /* -----------------------------------------------------
       LOAD ATTEMPT
    ----------------------------------------------------- */

    if (attemptId.value) {
      const response =
        await apiInstance.get(
          `/exams/attempts/${attemptId.value}/`
        )

      attempt.value =
        response.data
    }


    /* -----------------------------------------------------
       LOAD EXAM
    ----------------------------------------------------- */

    const exam =
      await loadExamInfo()


    /* -----------------------------------------------------
       LOAD ANSWERS
    ----------------------------------------------------- */

    answers.value = {
      ...(attempt.value?.answers || {}),
    }


    /* -----------------------------------------------------
       PDF URL
    ----------------------------------------------------- */

    questionsPdfUrl.value =
      exam.questions_pdf_url || ''


    /* -----------------------------------------------------
       TOTAL QUESTIONS
    ----------------------------------------------------- */

    if (
      !attempt.value?.exam_total_questions
    ) {
      attempt.value = {
        ...attempt.value,

        exam_total_questions:
          exam.total_questions || 0,
      }
    }


    /* -----------------------------------------------------
       FIND FIRST UNANSWERED QUESTION
    ----------------------------------------------------- */

    const total =
      Number(
        exam.total_questions
      ) || 0

    if (total > 0) {
      let firstUnanswered = 1

      for (
        let i = 1;
        i <= total;
        i++
      ) {
        const answer =
          answers.value[
            String(i)
          ]

        if (
          !(
            Number(answer) >= 1 &&
            Number(answer) <= 4
          )
        ) {
          firstUnanswered = i
          break
        }

        firstUnanswered = i
      }

      currentQuestion.value =
        firstUnanswered
    }


    /* -----------------------------------------------------
       TIMER
    ----------------------------------------------------- */

    updateRemainingTime()


    /* -----------------------------------------------------
       WAIT FOR DOM
    ----------------------------------------------------- */

    await nextTick()


    /* -----------------------------------------------------
       LOAD PDF
    ----------------------------------------------------- */

    if (questionsPdfUrl.value) {
      await loadPdf()
    }

  } catch (error) {
    console.error(
      'ATTEMPT LOAD ERROR:',
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
        'دریافت اطلاعات آزمون انجام نشد.'
    }

  } finally {
    loading.value = false
  }
}


/* =========================================================
   DESTROY PDF
========================================================= */

async function destroyPdf() {
  pdfRenderVersion++

  /*
    Stop render
  */

  if (pdfRenderTask) {
    try {
      pdfRenderTask.cancel()
    } catch {
      // ignore
    }

    pdfRenderTask = null
  }


  /*
    Destroy loading task
  */

  if (pdfLoadingTask) {
    try {
      await pdfLoadingTask.destroy()
    } catch {
      // ignore
    }

    pdfLoadingTask = null
  }


  /*
    Destroy document
  */

  if (pdfDocument) {
    try {
      await pdfDocument.destroy()
    } catch {
      // ignore
    }

    pdfDocument = null
  }


  lastRenderWidth = 0
  lastRenderHeight = 0
}


/* =========================================================
   LOAD PDF
========================================================= */

async function loadPdf() {
  if (!questionsPdfUrl.value) {
    return
  }

  pdfLoading.value = true
  pdfError.value = ''


  try {
    /*
      PDF قبلی کاملاً آزاد شود.
    */

    await destroyPdf()


    /*
      ایجاد loading task جدید
    */

    pdfLoadingTask =
      pdfjsLib.getDocument({
        url:
          questionsPdfUrl.value,

        /*
          در صورتی که PDF روی دامنه‌ای باشد که
          CORS مناسب دارد.
        */

        withCredentials: false,

        /*
          استفاده از range requests در صورت پشتیبانی سرور.

          این باعث می‌شود PDF های بزرگ سریع‌تر
          و بهینه‌تر دریافت شوند.
        */

        disableRange: false,

        disableStream: false,

        disableAutoFetch: false,

        /*
          کش کردن فونت‌ها برای کاهش مصرف منابع.
        */

        fontExtraProperties: false,

        /*
          استفاده از سیستم رنگ مرورگر.
        */

        useSystemFonts: true,
      })


    /*
      PDFDocumentProxy را reactive نمی‌کنیم.
    */

    const loadedDocument =
      await pdfLoadingTask.promise


    pdfDocument =
      loadedDocument

    pdfLoadingTask = null


    /*
      render اولین صفحه
    */

    await nextTick()

    await renderCurrentPage()

  } catch (error) {
    console.error(
      'PDF LOAD ERROR:',
      error
    )

    /*
      اگر task به علت navigation/destroy لغو شده،
      به عنوان خطای واقعی نمایش داده نشود.
    */

    if (
      error?.name ===
      'AbortException'
    ) {
      return
    }

    pdfError.value =
      getPdfErrorMessage(error)

  } finally {
    pdfLoading.value = false
  }
}


/* =========================================================
   PDF ERROR MESSAGE
========================================================= */

function getPdfErrorMessage(error) {
  if (
    error?.name ===
    'MissingPDFException'
  ) {
    return 'فایل PDF پیدا نشد.'
  }

  if (
    error?.name ===
    'InvalidPDFException'
  ) {
    return 'فایل PDF معتبر نیست یا ناقص دریافت شده است.'
  }

  if (
    error?.name ===
    'UnexpectedResponseException'
  ) {
    return 'سرور فایل PDF را به‌درستی ارسال نکرد.'
  }

  if (
    error?.name ===
    'PasswordException'
  ) {
    return 'این فایل PDF دارای رمز عبور است.'
  }

  if (
    error?.name ===
    'UnknownErrorException'
  ) {
    return 'خطای ناشناخته هنگام پردازش PDF رخ داد.'
  }

  return (
    error?.message ||
    'خطا در بارگذاری فایل PDF.'
  )
}


/* =========================================================
   CALCULATE PDF SCALE
========================================================= */

function calculatePdfScale(
  page,
  containerWidth,
  containerHeight
) {
  const baseViewport =
    page.getViewport({
      scale: 1,
    })


  /*
    فضای داخلی viewer

    padding = 32px
  */

  const availableWidth =
    Math.max(
      1,
      containerWidth - 32
    )


  const availableHeight =
    Math.max(
      1,
      containerHeight - 32
    )


  /*
    Scale برای fit width
  */

  const widthScale =
    availableWidth /
    baseViewport.width


  /*
    Scale برای fit height
  */

  const heightScale =
    availableHeight /
    baseViewport.height


  /*
    برای آزمون، اولویت با عرض است.

    اما اگر صفحه نسبت به viewer بیش از حد
    بلند باشد، ارتفاع نیز در نظر گرفته می‌شود.
  */

  let scale =
    widthScale


  if (
    widthScale *
      baseViewport.height >
    availableHeight * 1.5
  ) {
    scale =
      Math.min(
        widthScale,
        heightScale
      )
  }


  /*
    حداقل scale منطقی
  */

  scale =
    Math.max(
      scale,
      0.1
    )


  /*
    scale بسیار بزرگ می‌تواند Canvas عظیمی بسازد.

    این سقف برای جلوگیری از crash روی PDF های
    بسیار بزرگ است، ولی روی نمایشگرهای معمولی
    تقریباً هیچ‌وقت فعال نمی‌شود.
  */

  scale =
    Math.min(
      scale,
      5
    )


  return {
    scale,
    baseViewport,
  }
}


/* =========================================================
   RENDER CURRENT PAGE
========================================================= */

async function renderCurrentPage() {
  if (!pdfDocument) {
    return
  }

  await nextTick()


  const canvas =
    pdfCanvas.value

  const container =
    pdfViewerWrapper.value


  if (
    !canvas ||
    !container
  ) {
    return
  }


  const pageNumber =
    Number(
      currentQuestion.value
    )


  /*
    بررسی شماره صفحه
  */

  if (
    pageNumber < 1 ||
    pageNumber >
      pdfDocument.numPages
  ) {
    pdfError.value =
      `صفحه ${pageNumber} در PDF وجود ندارد. تعداد صفحات: ${pdfDocument.numPages}`

    return
  }


  /*
    نسخه جدید render

    اگر render قبلی بعداً تمام شود،
    اجازه نمی‌دهیم canvas جدید را خراب کند.
  */

  const renderVersion =
    ++pdfRenderVersion


  pdfError.value = ''
  pdfLoading.value = true


  /*
    Render قبلی را cancel کن.
  */

  if (pdfRenderTask) {
    try {
      pdfRenderTask.cancel()
    } catch {
      // ignore
    }

    pdfRenderTask = null
  }


  try {
    /*
      گرفتن صفحه
    */

    const page =
      await pdfDocument.getPage(
        pageNumber
      )


    /*
      اگر در زمان دریافت صفحه render جدیدی
      شروع شده، این render دیگر معتبر نیست.
    */

    if (
      renderVersion !==
      pdfRenderVersion
    ) {
      return
    }


    /*
      اندازه واقعی viewer
    */

    const rect =
      container.getBoundingClientRect()


    const containerWidth =
      Math.max(
        1,
        Math.floor(
          rect.width
        )
      )


    const containerHeight =
      Math.max(
        1,
        Math.floor(
          rect.height
        )
      )


    /*
      اگر اندازه تغییر نکرده و canvas
      قبلاً render شده، دوباره render نکن.
    */

    if (
      Math.abs(
        containerWidth -
          lastRenderWidth
      ) < 2 &&
      Math.abs(
        containerHeight -
          lastRenderHeight
      ) < 2 &&
      canvas.width > 0 &&
      canvas.height > 0
    ) {
      return
    }


    /*
      محاسبه scale
    */

    const {
      scale,
    } =
      calculatePdfScale(
        page,
        containerWidth,
        containerHeight
      )


    /*
      DPR واقعی نمایشگر

      مثلاً:

      Full HD معمولی → 1
      Retina → 2
      بعضی مانیتورها → 1.25 / 1.5 / 2 / 3
    */

    const devicePixelRatio =
      Math.max(
        1,
        window.devicePixelRatio ||
          1
      )


    /*
      Viewport منطقی

      این اندازه برای CSS است.
    */

    const viewport =
      page.getViewport({
        scale,
      })


    /*
      Canvas واقعی با رزولوشن بالا

      این بخش مهم‌ترین قسمت کیفیت PDF است.
    */

    const outputScale =
      devicePixelRatio


    const outputWidth =
      Math.floor(
        viewport.width *
          outputScale
      )


    const outputHeight =
      Math.floor(
        viewport.height *
          outputScale
      )


    /*
      جلوگیری از Canvas بیش از حد بزرگ

      محدودیت مرورگرها معمولاً به اندازه canvas
      وابسته است.

      اگر PDF فوق‌العاده بزرگ باشد،
      DPR را فقط در همان شرایط کاهش می‌دهیم.
    */

    const MAX_CANVAS_PIXELS =
      26800000


    let finalOutputScale =
      outputScale


    const requestedPixels =
      outputWidth *
      outputHeight


    if (
      requestedPixels >
      MAX_CANVAS_PIXELS
    ) {
      finalOutputScale =
        Math.sqrt(
          MAX_CANVAS_PIXELS /
            (
              viewport.width *
              viewport.height
            )
        )
    }


    /*
      حداقل DPR = 1
    */

    finalOutputScale =
      Math.max(
        1,
        finalOutputScale
      )


    const finalCanvasWidth =
      Math.floor(
        viewport.width *
          finalOutputScale
      )


    const finalCanvasHeight =
      Math.floor(
        viewport.height *
          finalOutputScale
      )


    /*
      Context
    */

    const context =
      canvas.getContext(
        '2d',
        {
          alpha: false,

          /*
            برای PDF خوانی معمولاً
            antialiasing مرورگر بهتر است.
          */

          desynchronized: true,
        }
      )


    if (!context) {
      throw new Error(
        'Canvas 2D context is not available.'
      )
    }


    /*
      Canvas قبلی را پاک می‌کنیم.
    */

    context.setTransform(
      1,
      0,
      0,
      1,
      0,
      0
    )


    context.clearRect(
      0,
      0,
      canvas.width,
      canvas.height
    )


    /*
      اندازه واقعی bitmap
    */

    canvas.width =
      finalCanvasWidth

    canvas.height =
      finalCanvasHeight


    /*
      اندازه CSS

      مرورگر bitmap بزرگ را در اندازه منطقی
      نمایش می‌دهد.
    */

    canvas.style.width =
      `${viewport.width}px`

    canvas.style.height =
      `${viewport.height}px`


    /*
      Scale مخصوص HiDPI

      به جای تغییر viewport، bitmap را با
      رزولوشن بالاتر render می‌کنیم.
    */

    const renderViewport =
      page.getViewport({
        scale,
      })


    const renderContext = {
      canvasContext:
        context,

      viewport:
        renderViewport,

      transform:
        finalOutputScale !== 1
          ? [
              finalOutputScale,
              0,
              0,
              finalOutputScale,
              0,
              0,
            ]
          : null,

      /*
        background سفید

        مخصوصاً برای PDF های دارای transparency
        نتیجه تمیزتری می‌دهد.
      */

      background:
        '#ffffff',
    }


    /*
      Render
    */

    pdfRenderTask =
      page.render(
        renderContext
      )


    await pdfRenderTask.promise


    /*
      اگر render قدیمی بود، نتیجه را معتبر
      حساب نکن.
    */

    if (
      renderVersion !==
      pdfRenderVersion
    ) {
      return
    }


    /*
      اندازه آخرین render
    */

    lastRenderWidth =
      containerWidth

    lastRenderHeight =
      containerHeight


    pdfRenderTask = null

  } catch (error) {
    /*
      اگر render لغو شده، خطا نیست.
    */

    if (
      error?.name ===
      'RenderingCancelledException' ||
      error?.name ===
      'AbortException'
    ) {
      return
    }


    /*
      ممکن است PDF هنگام navigation
      destroy شده باشد.
    */

    if (
      renderVersion !==
      pdfRenderVersion
    ) {
      return
    }


    console.error(
      'PDF RENDER ERROR:',
      error
    )


    pdfError.value =
      getPdfErrorMessage(error)

  } finally {
    /*
      فقط render فعلی loading را خاموش کند.
    */

    if (
      renderVersion ===
      pdfRenderVersion
    ) {
      pdfLoading.value = false
    }
  }
}


/* =========================================================
   FORCE RENDER
========================================================= */

async function forceRenderCurrentPage() {
  lastRenderWidth = 0
  lastRenderHeight = 0

  await renderCurrentPage()
}


/* =========================================================
   CURRENT ANSWER
========================================================= */

const currentAnswer = computed(() => {
  return (
    answers.value[
      String(
        currentQuestion.value
      )
    ] || null
  )
})


/* =========================================================
   ANSWER COUNT
========================================================= */

const answeredCount = computed(() => {
  return Object.keys(
    answers.value
  ).filter(
    key => {
      const value =
        Number(
          answers.value[key]
        )

      return (
        value >= 1 &&
        value <= 4
      )
    }
  ).length
})


/* =========================================================
   PROGRESS
========================================================= */

const progressPercent = computed(() => {
  if (
    !totalQuestions.value
  ) {
    return 0
  }

  return Math.round(
    (
      answeredCount.value /
      totalQuestions.value
    ) *
    100
  )
})


/* =========================================================
   SELECT ANSWER
========================================================= */

async function selectAnswer(value) {
  answers.value = {
    ...answers.value,

    [String(
      currentQuestion.value
    )]:
      value,
  }

  await saveAnswers()
}


/* =========================================================
   SAVE ANSWERS
========================================================= */

async function saveAnswers() {
  if (!attemptId.value) {
    return
  }


  /*
    اگر یک save قبلی در حال انجام است،
    همچنان request جدید ارسال می‌شود تا
    آخرین state ثبت شود.

    در صورت نیاز می‌توان debounce اضافه کرد،
    ولی برای آزمون ثبت فوری پاسخ امن‌تر است.
  */

  saving.value = true
  saved.value = false


  try {
    const apiInstance =
      createApi()

    await apiInstance.patch(
      `/exams/attempts/${attemptId.value}/answers/`,
      {
        answers:
          answers.value,
      }
    )

    saved.value = true

  } catch (error) {
    console.error(
      'SAVE ANSWERS ERROR:',
      error
    )

  } finally {
    saving.value = false
  }
}


/* =========================================================
   GO TO QUESTION
========================================================= */

async function goToQuestion(
  question
) {
  const questionNumber =
    Number(question)


  if (
    questionNumber < 1 ||
    questionNumber >
      totalQuestions.value
  ) {
    return
  }


  /*
    اگر همان سؤال فعلی است،
    در صورت وجود canvas نیازی به render نیست.
  */

  const changed =
    currentQuestion.value !==
    questionNumber


  currentQuestion.value =
    questionNumber


  await nextTick()


  /*
    اگر PDF هنوز load نشده، چیزی render نمی‌کنیم.
  */

  if (!pdfDocument) {
    return
  }


  /*
    برای سؤال جدید حتماً render انجام شود.
  */

  if (changed) {
    lastRenderWidth = 0
    lastRenderHeight = 0
  }


  await renderCurrentPage()
}


/* =========================================================
   NEXT QUESTION
========================================================= */

async function nextQuestion() {
  if (
    currentQuestion.value >=
    totalQuestions.value
  ) {
    return
  }

  await goToQuestion(
    currentQuestion.value + 1
  )
}


/* =========================================================
   PREVIOUS QUESTION
========================================================= */

async function previousQuestion() {
  if (
    currentQuestion.value <= 1
  ) {
    return
  }

  await goToQuestion(
    currentQuestion.value - 1
  )
}


/* =========================================================
   TIMER
========================================================= */

let timerInterval = null


function updateRemainingTime() {
  if (
    !attempt.value?.expires_at
  ) {
    remainingSeconds.value = 0
    return
  }


  const expires =
    new Date(
      attempt.value.expires_at
    ).getTime()


  const now =
    Date.now()


  remainingSeconds.value =
    Math.max(
      0,
      Math.floor(
        (
          expires -
          now
        ) / 1000
      )
    )
}


function startTimer() {
  stopTimer()

  updateRemainingTime()


  timerInterval =
    window.setInterval(
      async () => {
        updateRemainingTime()


        if (
          remainingSeconds.value <= 0
        ) {
          stopTimer()

          await handleTimeExpired()
        }
      },
      1000
    )
}


function stopTimer() {
  if (timerInterval) {
    window.clearInterval(
      timerInterval
    )

    timerInterval = null
  }
}


/* =========================================================
   TIME EXPIRED
========================================================= */

async function handleTimeExpired() {
  try {
    /*
      آخرین پاسخ‌ها را ذخیره کن.
    */

    await saveAnswers()


    /*
      سپس submit
    */

    await submitExamNow()

  } catch (error) {
    console.error(
      'AUTO SUBMIT ERROR:',
      error
    )


    /*
      اگر submitExamNow خودش alert نشان داده،
      alert اضافه نکن.
    */

    if (
      !error?.response
    ) {
      alert(
        'زمان آزمون به پایان رسید، اما ثبت نهایی با مشکل مواجه شد.'
      )
    }
  }
}


/* =========================================================
   FORMAT TIMER
========================================================= */

function formatTimer(seconds) {
  const value =
    Math.max(
      0,
      Number(seconds) || 0
    )


  const hours =
    Math.floor(
      value / 3600
    )


  const minutes =
    Math.floor(
      (
        value % 3600
      ) / 60
    )


  const secs =
    value % 60


  const h =
    String(hours)
      .padStart(
        2,
        '0'
      )


  const m =
    String(minutes)
      .padStart(
        2,
        '0'
      )


  const s =
    String(secs)
      .padStart(
        2,
        '0'
      )


  return (
    `${toPersianNumber(h)}:` +
    `${toPersianNumber(m)}:` +
    `${toPersianNumber(s)}`
  )
}


/* =========================================================
   SUBMIT
========================================================= */

async function submitExam() {
  if (submitting.value) {
    return
  }

  showSubmitModal.value =
    true
}


/* =========================================================
   CONFIRM SUBMIT
========================================================= */

async function confirmSubmit() {
  if (submitting.value) {
    return
  }

  await submitExamNow()
}


/* =========================================================
   SUBMIT EXAM NOW
========================================================= */

async function submitExamNow() {
  if (!attemptId.value) {
    throw new Error(
      'Attempt ID not found'
    )
  }


  submitting.value = true


  try {
    const apiInstance =
      createApi()


    const response =
      await apiInstance.post(
        `/exams/attempts/${attemptId.value}/submit/`,
        {
          answers:
            answers.value,
        }
      )


    stopTimer()


    showSubmitModal.value =
      false


    await router.push({
      name: 'ExamResult',

      params: {
        id:
          attemptId.value,
      },
    })


    return response.data

  } catch (error) {
    console.error(
      'SUBMIT EXAM ERROR:',
      error
    )


    alert(
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      'ثبت نهایی آزمون انجام نشد.'
    )


    throw error

  } finally {
    submitting.value = false
  }
}


/* =========================================================
   LEAVE
========================================================= */

async function leaveExam() {
  const confirmed =
    window.confirm(
      'آیا مطمئن هستید می‌خواهید از آزمون خارج شوید؟ پاسخ‌های ذخیره‌شده باقی می‌مانند.'
    )


  if (!confirmed) {
    return
  }


  await saveAnswers()


  await router.push({
    name: 'ExamResult',
  })
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
   THEME
========================================================= */

function detectDark() {
  const root =
    document.documentElement

  const body =
    document.body


  const dataTheme =
    root.getAttribute(
      'data-theme'
    ) ||
    body?.getAttribute(
      'data-theme'
    )


  return (
    dataTheme === 'dark' ||

    root.classList.contains(
      'dark'
    ) ||

    body?.classList.contains(
      'dark'
    ) ||

    root.classList.contains(
      'dark-mode'
    ) ||

    body?.classList.contains(
      'dark-mode'
    )
  )
}


let themeObserver = null


function observeTheme() {
  isDark.value =
    detectDark()


  themeObserver =
    new MutationObserver(
      () => {
        isDark.value =
          detectDark()
      }
    )


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
}


/* =========================================================
   KEYBOARD
========================================================= */

function handleKeyboard(event) {
  const target =
    event.target


  /*
    داخل input ها، keyboard navigation
    آزمون اجرا نشود.
  */

  if (
    target instanceof
      HTMLInputElement ||
    target instanceof
      HTMLTextAreaElement ||
    target instanceof
      HTMLSelectElement
  ) {
    return
  }


  /*
    جلوگیری از رفتار پیش‌فرض مرورگر
    برای Arrow keys
  */

  if (
    event.key ===
    'ArrowRight'
  ) {
    event.preventDefault()

    nextQuestion()
  }


  if (
    event.key ===
    'ArrowLeft'
  ) {
    event.preventDefault()

    previousQuestion()
  }
}


/* =========================================================
   WINDOW RESIZE
========================================================= */

function handleResize() {
  /*
    render مستقیم روی هر resize باعث
    render های زیاد می‌شود.

    requestAnimationFrame بهتر است.
  */

  if (
    resizeAnimationFrame
  ) {
    cancelAnimationFrame(
      resizeAnimationFrame
    )
  }


  resizeAnimationFrame =
    requestAnimationFrame(
      async () => {
        resizeAnimationFrame =
          null

        if (!pdfDocument) {
          return
        }


        lastRenderWidth = 0
        lastRenderHeight = 0


        await renderCurrentPage()
      }
    )
}


/* =========================================================
   PDF RESIZE OBSERVER
========================================================= */

function setupPdfResizeObserver() {
  if (
    typeof ResizeObserver ===
    'undefined'
  ) {
    return
  }


  if (
    !pdfViewerWrapper.value
  ) {
    return
  }


  pdfResizeObserver =
    new ResizeObserver(
      () => {
        handleResize()
      }
    )


  pdfResizeObserver.observe(
    pdfViewerWrapper.value
  )
}


/* =========================================================
   CLEANUP PDF RESIZE OBSERVER
========================================================= */

function destroyPdfResizeObserver() {
  if (
    pdfResizeObserver
  ) {
    try {
      pdfResizeObserver.disconnect()
    } catch {
      // ignore
    }

    pdfResizeObserver = null
  }
}


/* =========================================================
   PAGE VISIBILITY
========================================================= */

function handleVisibilityChange() {
  /*
    وقتی tab دوباره visible شد،
    PDF را در صورت نیاز مجدداً render می‌کنیم.

    این کار مخصوصاً برای لپ‌تاپ و مرورگرهایی که
    tab background را suspend می‌کنند مفید است.
  */

  if (
    document.visibilityState ===
    'visible'
  ) {
    if (pdfDocument) {
      lastRenderWidth = 0
      lastRenderHeight = 0

      handleResize()
    }
  }
}


/* =========================================================
   MOUNT
========================================================= */

onMounted(
  async () => {
    /*
      Theme
    */

    observeTheme()


    /*
      Load exam
    */

    await loadAttempt()


    /*
      Start timer
    */

    if (
      attempt.value &&
      attempt.value.status ===
        'in_progress'
    ) {
      startTimer()
    }


    /*
      DOM آماده شود
    */

    await nextTick()


    /*
      PDF resize observer
    */

    setupPdfResizeObserver()


    /*
      Keyboard
    */

    window.addEventListener(
      'keydown',
      handleKeyboard,
      {
        passive: false,
      }
    )


    /*
      Window resize
    */

    window.addEventListener(
      'resize',
      handleResize,
      {
        passive: true,
      }
    )


    /*
      Visibility
    */

    document.addEventListener(
      'visibilitychange',
      handleVisibilityChange
    )


    /*
      اگر PDF در loadAttempt هنوز
      آماده نشده بود، دوباره render کنیم.
    */

    if (
      pdfDocument &&
      pdfCanvas.value
    ) {
      await forceRenderCurrentPage()
    }
  }
)


/* =========================================================
   UNMOUNT
========================================================= */

onBeforeUnmount(
  async () => {
    /*
      Timer
    */

    stopTimer()


    /*
      Resize animation
    */

    if (
      resizeAnimationFrame
    ) {
      cancelAnimationFrame(
        resizeAnimationFrame
      )

      resizeAnimationFrame =
        null
    }


    /*
      ResizeObserver
    */

    destroyPdfResizeObserver()


    /*
      Visibility
    */

    document.removeEventListener(
      'visibilitychange',
      handleVisibilityChange
    )


    /*
      PDF
    */

    await destroyPdf()


    /*
      Theme observer
    */

    themeObserver?.disconnect()

    themeObserver = null


    /*
      Keyboard
    */

    window.removeEventListener(
      'keydown',
      handleKeyboard
    )


    /*
      Window resize
    */

    window.removeEventListener(
      'resize',
      handleResize
    )
  }
)
</script>

<style scoped>

* {
  box-sizing: border-box;
}


.exam-taking-page {
  min-height: 100vh;

  background:
    radial-gradient(
      circle at top right,
      color-mix(
        in srgb,
        var(--primary-color, #6366f1) 8%,
        transparent
      ),
      transparent 32%
    ),
    #f5f7fb;

  color: #18212f;

  --primary:
    var(--primary-color, #6366f1);

  --surface:
    #ffffff;

  --surface-soft:
    #f8fafc;

  --border:
    #e5e7eb;

  --text:
    #18212f;

  --muted:
    #64748b;

  --danger:
    #ef4444;

  --success:
    #10b981;

  transition:
    background .25s ease,
    color .25s ease;
}


/* =========================
   DARK
========================= */

.exam-taking-page.is-dark {

  background:
    radial-gradient(
      circle at top right,
      color-mix(
        in srgb,
        var(--primary-color, #6366f1) 12%,
        transparent
      ),
      transparent 35%
    ),
    #0b1120;

  --surface:
    #111827;

  --surface-soft:
    #172033;

  --border:
    #273449;

  --text:
    #f1f5f9;

  --muted:
    #94a3b8;
}


/* =========================
   HEADER
========================= */

.exam-header {

  height: 82px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 20px;

  padding:
    0 28px;

  background:
    color-mix(
      in srgb,
      var(--surface) 94%,
      transparent
    );

  border-bottom:
    1px solid var(--border);

  position: sticky;

  top: 0;

  z-index: 50;

  backdrop-filter:
    blur(18px);
}


.exam-header-main {

  display: flex;

  align-items: center;

  gap: 15px;

  min-width: 0;
}


.back-button {

  width: 42px;

  height: 42px;

  border:
    1px solid var(--border);

  border-radius: 12px;

  background:
    var(--surface);

  color:
    var(--text);

  display: flex;

  align-items: center;

  justify-content: center;

  cursor: pointer;
}


.back-button svg {

  width: 20px;

  height: 20px;
}


.exam-header-title span {

  display: block;

  font-size: 12px;

  color:
    var(--muted);

  margin-bottom: 3px;
}


.exam-header-title h1 {

  margin: 0;

  font-size: 18px;

  color:
    var(--text);
}


/* =========================
   TIMER
========================= */

.exam-timer {

  display: flex;

  align-items: center;

  gap: 11px;

  min-width: 155px;

  padding:
    10px 14px;

  border:
    1px solid
    color-mix(
      in srgb,
      var(--primary) 20%,
      var(--border)
    );

  border-radius: 14px;

  background:
    color-mix(
      in srgb,
      var(--primary) 7%,
      var(--surface)
    );
}


.exam-timer svg {

  width: 25px;

  height: 25px;

  color:
    var(--primary);
}


.exam-timer span {

  display: block;

  font-size: 11px;

  color:
    var(--muted);
}


.exam-timer strong {

  display: block;

  direction: ltr;

  font-size: 17px;

  color:
    var(--text);
}


.exam-timer.warning strong {

  color:
    #f59e0b;
}


.exam-timer.danger {

  border-color:
    rgba(
      239,
      68,
      68,
      .3
    );
}


.exam-timer.danger strong {

  color:
    var(--danger);
}


/* =========================
   LAYOUT
========================= */

.exam-layout {

  width:
    min(
      1500px,
      calc(100% - 32px)
    );

  margin:
    18px auto;

  display: grid;

  grid-template-columns:
    minmax(0, 1fr)
    370px;

  gap: 18px;

  align-items: start;
}


/* =========================
   PDF
========================= */

.pdf-section {
  min-height: 100%;
  min-width: 0;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius: 20px;

  overflow: hidden;

  box-shadow:
    0 10px 35px
    rgba(
      15,
      23,
      42,
      .06
    );
}


.pdf-toolbar {

  min-height: 68px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 15px;

  padding:
    12px 18px;

  border-bottom:
    1px solid var(--border);
}


.pdf-title {

  display: flex;

  align-items: center;

  gap: 11px;
}


.pdf-icon {

  width: 42px;

  height: 42px;

  border-radius: 12px;

  background:
    color-mix(
      in srgb,
      var(--primary) 10%,
      var(--surface)
    );

  color:
    var(--primary);

  display: flex;

  align-items: center;

  justify-content: center;
}


.pdf-icon svg {

  width: 21px;

  height: 21px;
}


.pdf-title strong {

  display: block;

  color:
    var(--text);

  font-size: 14px;
}


.pdf-title span {

  display: block;

  margin-top: 3px;

  color:
    var(--muted);

  font-size: 11px;
}


.pdf-page-indicator {

  padding:
    7px 11px;

  border-radius: 9px;

  background:
    var(--surface-soft);

  color:
    var(--muted);

  font-size: 12px;
}


.pdf-page-indicator strong {

  color:
    var(--primary);
}


/* =========================
   PDF VIEWER
========================= */

.pdf-viewer-wrapper {
  
  background:
    #e8ebf0;

  overflow:
    auto;

  position:
    relative;

  
  justify-content:
    center;

  display: grid;
  place-items: center;
  height: 300px;
  padding:
    16px;
}


.exam-taking-page.is-dark
.pdf-viewer-wrapper {

  background:
    #0f172a;
}


.pdf-canvas-container {

  width:
    max-content;

  display:
    flex;

  justify-content:
    center;

  align-items:
    flex-start;

  background:
    white;

  box-shadow:
    0 5px 30px
    rgba(
      0,
      0,
      0,
      .14
    );
}


.pdf-canvas {

  display:
    block;

  background:
    white;

  max-width:
    none;
}


/* =========================
   PDF LOADING
========================= */

.pdf-loading {

  position:
    absolute;

  inset:
    0;

  z-index:
    10;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  justify-content:
    center;

  gap:
    12px;

  background:
    color-mix(
      in srgb,
      var(--surface) 82%,
      transparent
    );

  backdrop-filter:
    blur(4px);

  color:
    var(--muted);
}


.pdf-loading .loader {

  width:
    38px;

  height:
    38px;
}


/* =========================
   PDF ERROR
========================= */

.pdf-error {

  position:
    absolute;

  inset:
    0;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  justify-content:
    center;

  gap:
    10px;

  padding:
    30px;

  text-align:
    center;

  color:
    var(--muted);
}


.pdf-error svg {

  width:
    50px;

  height:
    50px;

  color:
    var(--danger);
}


.pdf-error strong {

  color:
    var(--text);

  font-size:
    15px;
}


.pdf-error span {

  max-width:
    500px;

  font-size:
    12px;

  line-height:
    1.8;
}


.pdf-error button {

  margin-top:
    10px;

  border:
    0;

  border-radius:
    10px;

  padding:
    9px 16px;

  background:
    var(--primary);

  color:
    white;

  cursor:
    pointer;
}


/* =========================
   ANSWER PANEL
========================= */

.answer-panel {

  position:
    sticky;

  top:
    100px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    20px;

  padding:
    17px;

  box-shadow:
    0 10px 35px
    rgba(
      15,
      23,
      42,
      .06
    );
}


.question-header {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  padding-bottom:
    15px;

  border-bottom:
    1px solid var(--border);
}


.question-header > div {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;
}


.question-header span {

  color:
    var(--muted);

  font-size:
    12px;
}


.question-header strong {

  font-size:
    25px;

  color:
    var(--primary);
}


.answer-status {

  padding:
    6px 9px;

  border-radius:
    8px;

  background:
    var(--surface-soft);
}


/* =========================
   OPTIONS
========================= */

.options {

  display:
    grid;

  gap:
    9px;

  margin-top:
    16px;
}


.option-button {

  position:
    relative;

  min-height:
    56px;

  border:
    1px solid var(--border);

  border-radius:
    13px;

  background:
    var(--surface);

  color:
    var(--text);

  display:
    flex;

  align-items:
    center;

  gap:
    11px;

  padding:
    8px 10px;

  cursor:
    pointer;

  text-align:
    right;

  transition:
    .18s ease;
}


.option-button:hover {

  border-color:
    color-mix(
      in srgb,
      var(--primary) 45%,
      var(--border)
    );

  transform:
    translateY(-1px);
}


.option-button.selected {

  border-color:
    var(--primary);

  background:
    color-mix(
      in srgb,
      var(--primary) 9%,
      var(--surface)
    );
}


.option-number {

  width:
    38px;

  height:
    38px;

  flex:
    0 0 38px;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  border-radius:
    10px;

  background:
    var(--surface-soft);

  color:
    var(--text);

  font-weight:
    700;
}


.option-button.selected
.option-number {

  background:
    var(--primary);

  color:
    white;
}


.option-text {

  font-size:
    13px;

  font-weight:
    600;
}


.option-check {

  margin-right:
    auto;

  width:
    24px;

  height:
    24px;

  color:
    var(--primary);
}


.option-check svg {

  width:
    100%;

  height:
    100%;
}


/* =========================
   NAVIGATION
========================= */

.question-navigation {

  display:
    grid;

  grid-template-columns:
    1fr
    auto
    1fr;

  gap:
    8px;

  margin-top:
    18px;
}


.nav-button,
.submit-button {

  min-height:
    43px;

  border-radius:
    11px;

  border:
    1px solid var(--border);

  background:
    var(--surface-soft);

  color:
    var(--text);

  font-size:
    12px;

  font-weight:
    700;

  cursor:
    pointer;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    5px;
}


.nav-button svg {

  width:
    17px;

  height:
    17px;
}


.nav-button:disabled {

  opacity:
    .4;

  cursor:
    not-allowed;
}


.nav-button.primary {

  border-color:
    var(--primary);

  background:
    var(--primary);

  color:
    white;
}


.submit-button {

  border:
    0;

  background:
    var(--primary);

  color:
    white;
}


.submit-button:disabled {

  opacity:
    .6;

  cursor:
    not-allowed;
}


.question-counter {

  min-width:
    65px;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  justify-content:
    center;
}


.question-counter strong {

  color:
    var(--primary);

  font-size:
    16px;
}


.question-counter span {

  color:
    var(--muted);

  font-size:
    9px;
}


/* =========================
   PROGRESS
========================= */

.progress-box {

  margin-top:
    18px;

  padding:
    13px;

  border-radius:
    13px;

  background:
    var(--surface-soft);
}


.progress-header {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  font-size:
    11px;

  color:
    var(--muted);
}


.progress-header strong {

  color:
    var(--primary);
}


.progress-track {

  height:
    6px;

  margin-top:
    9px;

  border-radius:
    999px;

  overflow:
    hidden;

  background:
    var(--border);
}


.progress-value {

  height:
    100%;

  border-radius:
    inherit;

  background:
    var(--primary);

  transition:
    width .25s ease;
}


/* =========================
   QUESTION MAP
========================= */

.question-map {

  margin-top:
    18px;
}


.question-map-title {

  font-size:
    12px;

  font-weight:
    700;

  color:
    var(--text);

  margin-bottom:
    10px;
}

.question-map-grid {

  display:
    grid;

  grid-template-columns:
    repeat(15, 1fr);

  gap:
    5px;

  max-height:
    190px;

  overflow-y:
    auto;

  padding:
    2px;
}


.question-number {

  aspect-ratio:
    1;

  border:
    1px solid var(--border);

  border-radius:
    8px;

  background:
    var(--surface);

  color:
    var(--muted);

  cursor:
    pointer;

  font-size:
    10px;
}


.question-number:hover {

  border-color:
    var(--primary);
}


.question-number.answered {

  background:
    color-mix(
      in srgb,
      var(--primary) 11%,
      var(--surface)
    );

  color:
    var(--primary);
}


.question-number.current {

  background:
    var(--primary);

  color:
    white;

  border-color:
    var(--primary);

  font-weight:
    700;
}


/* =========================
   SAVE STATUS
========================= */

.save-status {

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    7px;

  margin-top:
    14px;

  font-size:
    10px;

  color:
    var(--muted);
}


.save-dot {

  width:
    6px;

  height:
    6px;

  border-radius:
    50%;

  background:
    var(--muted);
}


.save-status.saving .save-dot {

  background:
    #f59e0b;

  animation:
    pulse 1s infinite;
}


.save-status.saved .save-dot {

  background:
    var(--success);
}


@keyframes pulse {

  50% {
    opacity:
      .3;
  }
}


/* =========================
   STATE
========================= */

.state-screen {

  min-height:
    calc(100vh - 82px);

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  flex-direction:
    column;

  gap:
    10px;

  color:
    var(--muted);
}


.state-screen h2 {

  margin:
    5px 0 0;

  color:
    var(--text);

  font-size:
    19px;
}


.state-screen p {

  margin:
    0;

  font-size:
    13px;
}


.loader {

  width:
    42px;

  height:
    42px;

  border:
    3px solid var(--border);

  border-top-color:
    var(--primary);

  border-radius:
    50%;

  animation:
    spin .8s linear infinite;
}


@keyframes spin {

  to {
    transform:
      rotate(360deg);
  }
}


.state-icon {

  width:
    60px;

  height:
    60px;

  border-radius:
    17px;

  background:
    color-mix(
      in srgb,
      var(--primary) 10%,
      var(--surface)
    );

  color:
    var(--primary);

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;
}


.state-icon svg {

  width:
    30px;

  height:
    30px;
}


.retry-button {

  margin-top:
    10px;

  padding:
    10px 18px;

  border:
    0;

  border-radius:
    10px;

  background:
    var(--primary);

  color:
    white;

  cursor:
    pointer;
}


/* =========================
   MODAL
========================= */

.modal-overlay {

  position:
    fixed;

  inset:
    0;

  z-index:
    100;

  background:
    rgba(
      2,
      6,
      23,
      .58
    );

  backdrop-filter:
    blur(7px);

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  padding:
    20px;
}


.submit-modal {

  width:
    min(
      430px,
      100%
    );

  padding:
    27px;

  border-radius:
    22px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  text-align:
    center;

  box-shadow:
    0 25px 80px
    rgba(
      0,
      0,
      0,
      .2
    );
}


.modal-icon {

  width:
    58px;

  height:
    58px;

  margin:
    0 auto 15px;

  border-radius:
    17px;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  background:
    color-mix(
      in srgb,
      var(--primary) 10%,
      var(--surface)
    );

  color:
    var(--primary);
}


.modal-icon svg {

  width:
    28px;

  height:
    28px;
}


.submit-modal h2 {

  margin:
    0;

  color:
    var(--text);

  font-size:
    20px;
}


.submit-modal p {

  color:
    var(--muted);

  font-size:
    13px;

  line-height:
    1.9;
}


.submit-modal p strong {

  color:
    var(--primary);
}


.modal-warning {

  color:
    #f59e0b !important;
}


.modal-actions {

  display:
    grid;

  grid-template-columns:
    1fr 1fr;

  gap:
    9px;

  margin-top:
    20px;
}


.modal-cancel,
.modal-confirm {

  height:
    45px;

  border-radius:
    11px;

  font-weight:
    700;

  cursor:
    pointer;
}


.modal-cancel {

  border:
    1px solid var(--border);

  background:
    var(--surface-soft);

  color:
    var(--text);
}


.modal-confirm {

  border:
    0;

  background:
    var(--primary);

  color:
    white;
}


.modal-confirm:disabled {

  opacity:
    .6;

  cursor:
    not-allowed;
}


.fade-enter-active,
.fade-leave-active {

  transition:
    opacity .2s ease;
}


.fade-enter-from,
.fade-leave-to {

  opacity:
    0;
}


/* =========================
   RESPONSIVE
========================= */

@media (
  max-width: 1000px
) {

  .exam-layout {

    grid-template-columns:
      1fr;
  }


  .answer-panel {

    position:
      static;
  }


  .pdf-viewer-wrapper {

    height:
      75vh;
  }
}


@media (
  max-width: 600px
) {

  .exam-header {

    height:
      auto;

    min-height:
      70px;

    padding:
      10px 12px;
  }


  .exam-header-title h1 {

    font-size:
      14px;
  }


  .exam-timer {

    min-width:
      auto;

    padding:
      8px;
  }


  .exam-timer span {

    display:
      none;
  }


  .exam-timer strong {

    font-size:
      14px;
  }


  .exam-layout {

    width:
      calc(100% - 16px);

    margin:
      8px auto;
  }


  .pdf-viewer-wrapper {

    height:
      65vh;

    min-height:
      400px;
  }


  .question-navigation {

    grid-template-columns:
      1fr 1fr;
  }


  .question-counter {

    display:
      none;
  }
}

</style>
```
