import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken
  },

  actions: {
    setAuth({ accessToken, refreshToken, user = null }) {
      this.accessToken = accessToken
      this.refreshToken = refreshToken
      this.user = user

      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)

      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },

    updateAccessToken(accessToken) {
      this.accessToken = accessToken

      localStorage.setItem(
        'access_token',
        accessToken
      )
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },

    async fetchUser() {
  const { default: api } = await import('../services/api')

  const response = await api.get('/accounts/me/')

  this.user = response.data

  localStorage.setItem(
    'user',
    JSON.stringify(response.data)
  )

  return response.data
}
  }
})