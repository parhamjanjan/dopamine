```vue
<template>
  <main class="auth-shell">

    <!-- =====================================================
         فرم ورود
    ====================================================== -->

    <section class="login-card">

      <div class="login-form-container">

        <!-- عنوان -->

        <div class="mb-8">

          <span class="eyebrow">
            حساب کاربری
          </span>

          <h2 class="text-3xl font-black text-slate-800 mt-2">
            ورود به حساب کاربری
          </h2>

          <p class="text-slate-500 mt-2">
            برای ادامه، وارد حساب خود شوید.
          </p>

        </div>


        <!-- فرم -->

        <form
          class="space-y-5"
          @submit.prevent="submitLogin"
        >

          <!-- نام کاربری -->

          <label class="field">

            <span>
              نام کاربری
            </span>

            <div class="input-wrap">

              <UserRound
                :size="20"
                class="input-icon"
              />

              <input
                v-model.trim="form.username"
                type="text"
                placeholder="نام کاربری خود را وارد کنید"
                autocomplete="username"
                dir="ltr"
                required
              >

            </div>

          </label>


          <!-- رمز عبور -->

          <label class="field">

            <span>
              رمز عبور
            </span>

            <div class="input-wrap">

              <LockKeyhole
                :size="20"
                class="input-icon"
              />

              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="رمز عبور خود را وارد کنید"
                autocomplete="current-password"
                dir="ltr"
                required
              >

              <button
                type="button"
                class="show-pass"
                @click="showPassword = !showPassword"
                :aria-label="
                  showPassword
                    ? 'مخفی کردن رمز عبور'
                    : 'نمایش رمز عبور'
                "
              >

                <EyeOff
                  v-if="showPassword"
                  :size="20"
                />

                <Eye
                  v-else
                  :size="20"
                />

              </button>

            </div>

          </label>


          <!-- گزینه‌ها -->

          <div class="flex items-center justify-between text-sm mb-8">

            <label
              class="remember-me"
            >

              <input
                v-model="rememberMe"
                type="checkbox"
                class="accent-violet-600"
              >

              <span>
                مرا به خاطر بسپار
              </span>

            </label>


            <button
              type="button"
              class="forgot-password"
              @click="forgotPassword"
            >
              رمز عبور را فراموش کردید؟
            </button>

          </div>


          <!-- خطای ورود -->

          <div
            v-if="errorMessage"
            class="login-error"
          >

            <CircleAlert
              :size="19"
            />

            <span>
              {{ errorMessage }}
            </span>

          </div>


          <!-- دکمه ورود -->

          <button
            class="primary-btn"
            type="submit"
            :disabled="loading"
          >

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
                  ? 'در حال ورود...'
                  : 'ورود'
              }}
            </span>

          </button>

        </form>


        <!-- جداکننده -->

        <div class="divider">
          <span>
            یا
          </span>
        </div>


        <!-- ورودهای اجتماعی -->

        <div class="grid grid-cols-3 gap-3">

          <button
            type="button"
            class="social-btn"
            @click="socialLogin('google')"
            aria-label="ورود با گوگل"
          >
            <Chrome :size="21" />
          </button>


          <button
            type="button"
            class="social-btn"
            @click="socialLogin('telegram')"
            aria-label="ورود با تلگرام"
          >
            <Send :size="21" />
          </button>


          <button
            type="button"
            class="social-btn"
            @click="socialLogin('github')"
            aria-label="ورود با گیت‌هاب"
          >
            <Github :size="21" />
          </button>

        </div>


        <!-- ثبت نام -->

        <p class="register-link">

          حساب کاربری ندارید؟

          <RouterLink to="/signup">
            ثبت‌نام کنید
          </RouterLink>

        </p>

      </div>

    </section>


    <!-- =====================================================
         بخش تصویری
    ====================================================== -->

    <section class="login-visual">

      <div class="visual-overlay"></div>

      <div class="visual-content">

        <div class="brand-mark">
          <Sparkles :size="48" />
        </div>

        <h1>
          خوش آمدید!
        </h1>

        <p>
          خوشحالیم که دوباره شما را می‌بینیم.
        </p>

        <div class="floating-heart">
          <Heart
            :size="34"
            fill="currentColor"
          />
        </div>

      </div>

    </section>

  </main>
</template>


<script setup>

import {
  ref,
  reactive
} from 'vue'

import {
  RouterLink,
  useRouter
} from 'vue-router'

import {
  UserRound,
  LockKeyhole,
  Eye,
  EyeOff,
  LogIn,
  LoaderCircle,
  CircleAlert,
  Chrome,
  Send,
  Github,
  Sparkles,
  Heart
} from 'lucide-vue-next'

import api from '../services/api'
import { useAuthStore } from '../stores/auth'


/* =========================================================
   Router و Auth
========================================================= */

const router = useRouter()
const auth = useAuthStore()


/* =========================================================
   فرم
========================================================= */

const form = reactive({

  username: '',
  password: ''

})


/* =========================================================
   وضعیت صفحه
========================================================= */

const loading = ref(false)

const showPassword = ref(false)

const rememberMe = ref(false)

const errorMessage = ref('')


/* =========================================================
   ورود
========================================================= */

async function submitLogin() {

  if (loading.value) {
    return
  }


  errorMessage.value = ''


  if (!form.username || !form.password) {

    errorMessage.value =
      'لطفاً نام کاربری و رمز عبور را وارد کنید.'

    return

  }


  loading.value = true


  try {

    const response =
      await api.post(
        '/accounts/login/',
        {
          username: form.username,
          password: form.password
        }
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
       ذخیره احراز هویت
    ===================================================== */

    auth.setAuth({

      accessToken,

      refreshToken,

      user:
        response.data?.user || null

    })


    /* =====================================================
       انتقال به صفحه اصلی
    ===================================================== */

    await router.push('/')


  } catch (error) {

    console.error(
      'Login error:',
      error
    )


    const errors =
      error.response?.data?.errors


    if (errors) {

      const messages = []


      for (
        const [field, fieldErrors]
        of Object.entries(errors)
      ) {

        if (
          Array.isArray(fieldErrors)
        ) {

          messages.push(
            fieldErrors.join(' ')
          )

        } else {

          messages.push(
            String(fieldErrors)
          )

        }

      }


      errorMessage.value =
        messages.length
          ? messages.join(' ')
          : 'نام کاربری یا رمز عبور صحیح نیست.'


    } else if (
      error.response?.data?.message
    ) {

      errorMessage.value =
        error.response.data.message


    } else if (
      error.response?.status === 401
    ) {

      errorMessage.value =
        'نام کاربری یا رمز عبور اشتباه است.'


    } else {

      errorMessage.value =
        'ارتباط با سرور برقرار نشد.'

    }

  } finally {

    loading.value = false

  }

}


/* =========================================================
   فراموشی رمز عبور
========================================================= */

function forgotPassword() {

  alert(
    'بخش بازیابی رمز عبور هنوز پیاده‌سازی نشده است.'
  )

}


/* =========================================================
   ورود اجتماعی
========================================================= */

function socialLogin(provider) {

  console.log(
    'Social login:',
    provider
  )

  alert(
    'ورود با این سرویس هنوز پیاده‌سازی نشده است.'
  )

}

</script>


<style src="../assets/login.css"></style>

