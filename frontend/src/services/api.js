import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: 'https://dopamine-backend-3vbz.onrender.com/api',
})


// ========================================
// Request Interceptor
// ========================================

api.interceptors.request.use(
  (config) => {
    const auth = useAuthStore()

    const publicEndpoints = [
      '/accounts/register/',
      '/accounts/login/',
      '/accounts/token/refresh/'
    ]

    const isPublicEndpoint = publicEndpoints.some(
      (endpoint) => config.url?.includes(endpoint)
    )

    if (
      auth.accessToken &&
      !isPublicEndpoint
    ) {
      config.headers.Authorization =
        `Bearer ${auth.accessToken}`
    }
    if (config.data instanceof FormData) {
  delete config.headers['Content-Type']
}

    return config
  },

  (error) => {
    return Promise.reject(error)
  }
)


// ========================================
// Refresh State
// ========================================

let isRefreshing = false

let refreshSubscribers = []


const subscribeToRefresh = (callback) => {
  refreshSubscribers.push(callback)
}


const notifyRefreshSuccess = (token) => {
  refreshSubscribers.forEach(
    (callback) => callback(token)
  )

  refreshSubscribers = []
}


const notifyRefreshFailure = (error) => {
  refreshSubscribers.forEach(
    (callback) => callback(null, error)
  )

  refreshSubscribers = []
}


// ========================================
// Response Interceptor
// ========================================

api.interceptors.response.use(
  (response) => {
    return response
  },

  async (error) => {
    const originalRequest = error.config

    // فقط 401
    if (
      error.response?.status !== 401 ||
      !originalRequest
    ) {
      return Promise.reject(error)
    }

    // درخواست refresh خودش نباید دوباره refresh شود
    if (
      originalRequest.url?.includes(
        '/accounts/token/refresh/'
      )
    ) {
      const auth = useAuthStore()

      auth.logout()

      window.location.href = '/login'

      return Promise.reject(error)
    }

    // جلوگیری از retry بی‌نهایت
    if (originalRequest._retry) {
      const auth = useAuthStore()

      auth.logout()

      window.location.href = '/login'

      return Promise.reject(error)
    }

    originalRequest._retry = true

    const auth = useAuthStore()


    // ========================================
    // Refresh Token نداریم
    // ========================================

    if (!auth.refreshToken) {
      auth.logout()

      window.location.href = '/login'

      return Promise.reject(error)
    }


    // ========================================
    // Refresh در حال انجام است
    // ========================================

    if (isRefreshing) {
      return new Promise(
        (resolve, reject) => {

          subscribeToRefresh(
            (newAccessToken, refreshError) => {

              if (refreshError || !newAccessToken) {
                reject(refreshError || error)
                return
              }

              originalRequest.headers.Authorization =
                `Bearer ${newAccessToken}`

              resolve(
                api(originalRequest)
              )
            }
          )
        }
      )
    }


    // ========================================
    // شروع Refresh
    // ========================================

    isRefreshing = true

    try {

      const response = await axios.post(
        'https://dopamine-backend-3vbz.onrender.com/api/accounts/token/refresh/',
        {
          refresh: auth.refreshToken
        }
      )


      const newAccessToken =
        response.data.access

      // اگر Refresh Token Rotation فعال باشد
      // توکن refresh جدید را هم ذخیره می‌کنیم
      if (response.data.refresh) {
        auth.updateRefreshToken(
          response.data.refresh
        )
      }

      auth.updateAccessToken(
        newAccessToken
      )


      notifyRefreshSuccess(
        newAccessToken
      )


      originalRequest.headers.Authorization =
        `Bearer ${newAccessToken}`


      return api(originalRequest)

    } catch (refreshError) {

      notifyRefreshFailure(
        refreshError
      )

      auth.logout()

      window.location.href = '/login'

      return Promise.reject(refreshError)

    } finally {

      isRefreshing = false

    }
  }
)


export default api