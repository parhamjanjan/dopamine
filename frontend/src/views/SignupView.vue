```vue
<template>
  <main class="signup-shell">

    <!-- فرم -->
    <section class="signup-card">
      <div class="w-full mx-auto">

        <!-- عنوان -->
        <div class="mb-7">
          <span class="eyebrow">ایجاد حساب جدید</span>

          <h2 class="text-3xl font-black text-slate-800 mt-2">
            به جمع ما بپیوندید
          </h2>

          <p class="text-slate-500 mt-2">
            اطلاعات خود را مرحله‌به‌مرحله تکمیل کنید.
          </p>
        </div>


        <!-- مراحل -->
        <div class="steps" id="steps">

          <template v-for="(step, index) in stepTitles" :key="index">

            <div class="step" :class="{
              active: currentStep === index,
              done: currentStep > index
            }">
              <b>{{ index + 1 }}</b>
              <span>{{ step }}</span>
            </div>

            <div v-if="index < stepTitles.length - 1" class="line"></div>

          </template>

        </div>


        <form @submit.prevent="submitForm">

          <!-- ================================================= -->
          <!-- مرحله اول -->
          <!-- ================================================= -->

          <section v-if="currentStep === 0" class="form-step active">

            <h3>اطلاعات اولیه</h3>

            <p class="hint">
              اطلاعات پایه حساب خود را وارد کنید.
            </p>


            <div class="grid md:grid-cols-2 gap-4">

              <label class="field">
                <span>نام</span>

                <input v-model.trim="form.first_name" type="text" required placeholder="مثلاً پرهام">
              </label>


              <label class="field">
                <span>نام خانوادگی</span>

                <input v-model.trim="form.last_name" type="text" required placeholder="مثلاً جانجان">
              </label>

            </div>


            <label class="field">
              <span>شماره تلفن</span>

              <input v-model.trim="form.phone" type="tel" pattern="09[0-9]{9}" placeholder="09xxxxxxxxx" dir="ltr">
            </label>


            <label class="field">
              <span>نام کاربری</span>

              <input v-model.trim="form.username" type="text" required placeholder="نام کاربری دلخواه" dir="ltr">
            </label>

          </section>


          <!-- ================================================= -->
          <!-- مرحله دوم -->
          <!-- ================================================= -->

          <section v-if="currentStep === 1" class="form-step active">

            <h3>اطلاعات امنیتی</h3>

            <p class="hint">
              برای محافظت از حساب، یک رمز عبور قدرتمند انتخاب کنید.
            </p>


            <label class="field">
              <span>رمز عبور</span>

              <input id="password" v-model="form.password" type="password" required minlength="8"
                placeholder="حداقل ۸ کاراکتر" dir="ltr">
            </label>


            <label class="field">
              <span>تکرار رمز عبور</span>

              <input id="confirmPassword" v-model="form.confirm_password" type="password" required
                placeholder="رمز عبور را دوباره وارد کنید" dir="ltr">
            </label>


            <!-- قدرت رمز -->
            <div class="security-box">

              <div>
                <span>قدرت رمز عبور</span>

                <strong :style="{ color: passwordColor }">
                  {{ passwordLabel }}
                </strong>
              </div>


              <div class="strength-track">

                <i :style="{
                  width: passwordWidth,
                  background: passwordColor
                }"></i>

              </div>

            </div>

          </section>


          <!-- ================================================= -->
          <!-- مرحله سوم -->
          <!-- ================================================= -->

          <section v-if="currentStep === 2" class="form-step active">

            <h3>اطلاعات تکمیلی</h3>

            <p class="hint">
              اطلاعات تحصیلی و پروفایل خود را تکمیل کنید.
            </p>


            <!-- نام نمایشی -->



            <!-- تاریخ تولد + جنسیت -->
            <div class="grid md:grid-cols-2 gap-4">

              <div class="field birth-date-field">

                <span>تاریخ تولد</span>

                <div class="date-input-wrapper">

                  <date-picker v-model="form.birth_date" format="jYYYY/jMM/jDD"
                    placeholder="تاریخ تولد خود را انتخاب کنید" :auto-submit="true" color="#1bb1bf" />
                </div>

                <small>
                  تاریخ را به صورت شمسی انتخاب کنید
                </small>

              </div>


              <label class="field">

                <span>جنسیت</span>

                <select v-model="form.gender">

                  <option value="">
                    انتخاب کنید
                  </option>

                  <option value="male">
                    مرد
                  </option>

                  <option value="female">
                    زن
                  </option>

                </select>

              </label>

            </div>


            <!-- پایه + رشته -->
            <div class="grid md:grid-cols-2 gap-4">

              <!-- پایه -->
              <label class="field">

                <span>پایه تحصیلی</span>

                <select v-model="form.grade" required>

                  <option value="">
                    پایه تحصیلی خود را انتخاب کنید
                  </option>

                  <option value="10">
                    دهم
                  </option>

                  <option value="11">
                    یازدهم
                  </option>

                  <option value="12">
                    دوازدهم
                  </option>

                </select>

              </label>


              <!-- رشته -->
              <label class="field">

                <span>رشته تحصیلی</span>

                <select v-model="form.field" required>

                  <option value="">
                    رشته تحصیلی خود را انتخاب کنید
                  </option>

                  <option value="experimental">
                    علوم تجربی
                  </option>

                  <option value="mathematics">
                    ریاضی فیزیک
                  </option>

                  <option value="humanities">
                    علوم انسانی
                  </option>

                </select>

              </label>

            </div>


            <!-- استان + مدرسه -->
            <div class="grid md:grid-cols-2 gap-4">

              <!-- استان -->
              <label class="field">

                <span>استان</span>

                <select v-model="form.province" required>

                  <option value="">
                    استان محل تحصیل را انتخاب کنید
                  </option>

                  <option v-for="province in provinces" :key="province" :value="province">
                    {{ province }}
                  </option>

                </select>

              </label>


              <!-- مدرسه -->
              <label class="field">

                <span>نام مدرسه</span>

                <input v-model.trim="form.school" type="text" required placeholder="مثلاً دبیرستان نمونه دولتی...">

              </label>

            </div>


            <!-- درباره من -->
            <label class="field">

              <span>درباره من</span>

              <textarea v-model.trim="form.bio" rows="3" placeholder="کمی درباره خودتان بنویسید..."></textarea>

            </label>

          </section>


          <!-- ================================================= -->
          <!-- مرحله چهارم -->
          <!-- ================================================= -->

          <section v-if="currentStep === 3" class="form-step active">

            <h3>تم و رابط کاربری</h3>

            <p class="hint">
              ظاهر مورد علاقه خود را برای وبسایت انتخاب کنید.
            </p>


            <div class="theme-grid">

              <!-- روشن -->
              <label class="theme-option">

                <input v-model="form.theme" type="radio" name="theme" value="light">

                <span class="theme-card light-theme">
                  ☀️
                  <b>روشن</b>
                </span>

              </label>


              <!-- تیره -->
              <label class="theme-option">

                <input v-model="form.theme" type="radio" name="theme" value="dark">

                <span class="theme-card dark-theme">
                  🌙
                  <b>تیره</b>
                </span>

              </label>


              <!-- سیستمی -->
              <label class="theme-option">

                <input v-model="form.theme" type="radio" name="theme" value="system">

                <span class="theme-card system-theme">
                  ◐
                  <b>سیستمی</b>
                </span>

              </label>

            </div>


            <!-- رنگ اصلی -->
            <label class="field">

              <span>رنگ اصلی</span>

              <input v-model="form.primary_color" class="color-input" type="color">

            </label>


            <!-- قوانین -->
            <label class="terms">

              <input v-model="form.accept_terms" type="checkbox" required class="accent-violet-600">

              قوانین و شرایط استفاده را می‌پذیرم.

            </label>

          </section>


          <!-- ================================================= -->
          <!-- دکمه‌ها -->
          <!-- ================================================= -->

          <div class="actions">

            <!-- بازگشت -->
            <button v-if="currentStep > 0" type="button" class="secondary-btn" @click="previousStep">
              بازگشت
            </button>


            <!-- ادامه -->
            <button v-if="currentStep < stepTitles.length - 1" type="button" class="primary-btn" @click="nextStep">
              ادامه
            </button>


            <!-- ساخت حساب -->
            <button v-if="currentStep === stepTitles.length - 1" type="submit" class="primary-btn" :disabled="loading">
              <LoaderCircle
              v-if="loading"
              :size="20"
              class="loading-icon"
            />

            <LogIn
              v-else
              :size="20"
            />

            <span>
              {{
                loading
                  ? 'در حال ساخت حساب...'
                  : 'ساخت حساب'
              }}
            </span>


            </button>

          </div>

        </form>


        <!-- ورود -->
        <p class="login-link">

          قبلاً حساب دارید؟

          <RouterLink to="/login">
            وارد شوید
          </RouterLink>

        </p>

      </div>
    </section>


    <!-- ===================================================== -->
    <!-- بخش تصویری -->
    <!-- ===================================================== -->

    <aside class="signup-visual">

      <div class="visual-shade"></div>

      <div class="visual-copy" :style="{
        backgroundImage:
          `url('${visualData[currentStep].bg}')`
      }">
      </div>

    </aside>

  </main>
</template>


<script setup>

import DatePicker from 'vue3-persian-datetime-picker'

import {
  ref,
  reactive,
  computed
} from 'vue'

import {
  RouterLink,
  useRouter
} from 'vue-router'

import api from '../services/api'
import { useAuthStore } from '../stores/auth'

import {
  toGregorian
} from 'jalaali-js'


/* =========================================================
   Router
========================================================= */

const router = useRouter()
const auth = useAuthStore()


/* =========================================================
   وضعیت مرحله فعلی
========================================================= */

const currentStep = ref(0)

const loading = ref(false)


/* =========================================================
   عنوان مراحل
========================================================= */

const stepTitles = [
  'اولیه',
  'امنیتی',
  'تکمیلی',
  'تم'
]


/* =========================================================
   اطلاعات فرم
========================================================= */

const form = reactive({

  /* اطلاعات اولیه */

  first_name: '',
  last_name: '',
  phone: '',
  username: '',


  /* امنیت */

  password: '',
  confirm_password: '',


  /* تکمیلی */

  birth_date: '',
  gender: '',


  /* تحصیلی */

  grade: '',
  field: '',
  province: '',
  school: '',


  /* درباره */

  bio: '',


  /* ظاهر */

  theme: 'light',
  primary_color: '#7055e8',


  /* قوانین */

  accept_terms: false

})


/* =========================================================
   استان‌های ایران
========================================================= */

const provinces = [

  'آذربایجان شرقی',
  'آذربایجان غربی',
  'اردبیل',
  'اصفهان',
  'البرز',
  'ایلام',
  'بوشهر',
  'تهران',
  'چهارمحال و بختیاری',
  'خراسان جنوبی',
  'خراسان رضوی',
  'خراسان شمالی',
  'خوزستان',
  'زنجان',
  'سمنان',
  'سیستان و بلوچستان',
  'فارس',
  'قزوین',
  'قم',
  'کردستان',
  'کرمان',
  'کرمانشاه',
  'کهگیلویه و بویراحمد',
  'گلستان',
  'گیلان',
  'لرستان',
  'مازندران',
  'مرکزی',
  'هرمزگان',
  'همدان',
  'یزد'

]


/* =========================================================
   تصاویر مراحل
========================================================= */

const visualData = [

  {
    bg: '/signup/signup-step-1-primary-info.png'
  },

  {
    bg: '/signup/signup-step-2-security-info.png'
  },

  {
    bg: '/signup/signup-step-3-identity-info.png'
  },

  {
    bg: '/signup/signup-step-4-theme-ui.png'
  }

]


/* =========================================================
   قدرت رمز عبور
========================================================= */

const passwordScore = computed(() => {

  const value = form.password

  let score = 0

  if (value.length >= 8) {
    score++
  }

  if (/[A-Z]/.test(value)) {
    score++
  }

  if (/[0-9]/.test(value)) {
    score++
  }

  if (/[^A-Za-z0-9]/.test(value)) {
    score++
  }

  return score

})


const passwordLabel = computed(() => {

  return [
    'ضعیف',
    'متوسط',
    'خوب',
    'قوی',
    'عالی'
  ][passwordScore.value]

})


const passwordWidth = computed(() => {

  return [
    '20%',
    '40%',
    '60%',
    '80%',
    '100%'
  ][passwordScore.value]

})


const passwordColor = computed(() => {

  return [
    '#ef4444',
    '#f59e0b',
    '#eab308',
    '#22c55e',
    '#16a34a'
  ][passwordScore.value]

})


/* =========================================================
   تبدیل تاریخ شمسی به میلادی
========================================================= */

function convertJalaliToGregorian(jalaliDate) {

  if (!jalaliDate) {
    return ''
  }

  try {

    const parts = String(jalaliDate)
      .trim()
      .split('/')
      .map(Number)

    if (parts.length !== 3) {
      console.error(
        'فرمت تاریخ نامعتبر است:',
        jalaliDate
      )
      return ''
    }

    const [jy, jm, jd] = parts

    if (
      !Number.isInteger(jy) ||
      !Number.isInteger(jm) ||
      !Number.isInteger(jd) ||
      jy < 1 ||
      jm < 1 ||
      jm > 12 ||
      jd < 1 ||
      jd > 31
    ) {
      console.error(
        'مقدار تاریخ نامعتبر است:',
        jalaliDate
      )
      return ''
    }

    const [gy, gm, gd] =
      toGregorian(jy, jm, jd)

    return [
      gy,
      String(gm).padStart(2, '0'),
      String(gd).padStart(2, '0')
    ].join('-')

  } catch (error) {

    console.error(
      'خطا در تبدیل تاریخ:',
      jalaliDate,
      error
    )

    return ''
  }
}

/* =========================================================
   اعتبارسنجی مرحله فعلی
========================================================= */

function validateCurrentStep() {

  const sections =
    document.querySelectorAll('.form-step')

  const section =
    sections[currentStep.value]

  if (!section) {
    return true
  }


  const fields =
    section.querySelectorAll(
      'input, select, textarea'
    )


  for (const field of fields) {

    if (!field.checkValidity()) {

      field.reportValidity()

      return false

    }

  }


  /* بررسی رمز عبور */

  if (currentStep.value === 1) {

    if (
      form.password !==
      form.confirm_password
    ) {

      alert(
        'رمز عبور و تکرار آن یکسان نیستند.'
      )

      return false

    }

  }


  /* بررسی تاریخ */

  if (currentStep.value === 2) {

    if (!form.birth_date) {

      alert(
        'لطفاً تاریخ تولد خود را انتخاب کنید.'
      )

      return false

    }

  }


  return true

}


/* =========================================================
   مرحله بعد
========================================================= */

function nextStep() {

  if (!validateCurrentStep()) {
    return
  }


  if (
    currentStep.value <
    stepTitles.length - 1
  ) {

    currentStep.value++

  }

}


/* =========================================================
   مرحله قبل
========================================================= */

function previousStep() {

  if (currentStep.value > 0) {

    currentStep.value--

  }

}


/* =========================================================
   ساخت Payload برای Django
========================================================= */

function buildPayload() {

  const birthDateJalali =
    form.birth_date
      ? String(form.birth_date)
      : ''

  const birthDateGregorian =
    convertJalaliToGregorian(
      birthDateJalali
    )


  return {

    first_name:
      form.first_name,

    last_name:
      form.last_name,

    phone_number:
      form.phone || null,

    username:
      form.username,

    password:
      form.password,

    password_confirm:
      form.confirm_password,

    birth_date_gregorian:
      birthDateGregorian || null,

    birth_date_jalali:
      birthDateJalali,

    grade:
      form.grade,

    field:
      form.field,

    province:
      form.province,

    school:
      form.school,

    theme:
      form.theme,

    primary_color:
      form.primary_color,

    gender:
      form.gender,

    bio:
      form.bio

  }

}


/* =========================================================
   ثبت فرم
========================================================= */

async function submitForm() {

  if (!validateCurrentStep()) {
    return
  }


  if (loading.value) {
    return
  }


  loading.value = true


  try {

    const payload =
      buildPayload()


    console.log(
      'Registration payload:',
      payload
    )


    /* =====================================================
       ارسال به Django
    ===================================================== */

    const response =
      await api.post(
        '/accounts/register/',
        payload
      )


    /* =====================================================
       دریافت JWT
    ===================================================== */

    const accessToken =
      response.data?.tokens?.access

    const refreshToken =
      response.data?.tokens?.refresh


    if (
      !accessToken ||
      !refreshToken
    ) {

      throw new Error(
        'توکن ورود از سرور دریافت نشد.'
      )

    }


    /* =====================================================
       ذخیره توکن‌ها
    ===================================================== */

    auth.setAuth({
      accessToken,
      refreshToken,
      user: response.data.user || null
    })


    /* =====================================================
       ورود خودکار
    ===================================================== */

    alert(
      'حساب کاربری با موفقیت ساخته شد!'
    )


    await router.push('/')

  } catch (error) {

    console.error(
      'Registration error:',
      error
    )


    /* =====================================================
       خطاهای Validation از Django
    ===================================================== */

    const errors =
      error.response?.data?.errors


    if (errors) {

      const messages = []


      for (
        const [field, fieldErrors]
        of Object.entries(errors)
      ) {

        if (Array.isArray(fieldErrors)) {

          messages.push(
            `${field}: ${fieldErrors.join(' ')}`
          )

        } else {

          messages.push(
            `${field}: ${fieldErrors}`
          )

        }

      }


      alert(
        messages.length
          ? messages.join('\n')
          : 'اطلاعات واردشده صحیح نیست.'
      )

    } else if (
      error.response?.data?.message
    ) {

      alert(
        error.response.data.message
      )

    } else {

      alert(
        'ارتباط با سرور برقرار نشد.'
      )

    }

  } finally {

    loading.value = false

  }

}

</script>


<style src="../assets/signup.css"></style>
```
