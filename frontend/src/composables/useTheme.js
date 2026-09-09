import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const DEFAULT_PRIMARY = '#7055e8'

function hexToRgb(hex) {
  if (!hex) {
    return null
  }

  const cleanHex = hex.replace('#', '').trim()

  if (!/^[0-9a-fA-F]{6}$/.test(cleanHex)) {
    return null
  }

  return {
    r: parseInt(cleanHex.slice(0, 2), 16),
    g: parseInt(cleanHex.slice(2, 4), 16),
    b: parseInt(cleanHex.slice(4, 6), 16)
  }
}

function lightenColor(hex, amount = 0.9) {
  const rgb = hexToRgb(hex)

  if (!rgb) {
    return '#f5f3ff'
  }

  const r = Math.round(rgb.r + (255 - rgb.r) * amount)
  const g = Math.round(rgb.g + (255 - rgb.g) * amount)
  const b = Math.round(rgb.b + (255 - rgb.b) * amount)

  return `rgb(${r}, ${g}, ${b})`
}

function darkenColor(hex, amount = 0.15) {
  const rgb = hexToRgb(hex)

  if (!rgb) {
    return '#5b21b6'
  }

  const r = Math.round(rgb.r * (1 - amount))
  const g = Math.round(rgb.g * (1 - amount))
  const b = Math.round(rgb.b * (1 - amount))

  return `rgb(${r}, ${g}, ${b})`
}

function applyColorVariables(color) {
  const root = document.documentElement

  const primary = color || DEFAULT_PRIMARY
  const rgb = hexToRgb(primary)

  root.style.setProperty('--primary', primary)
  root.style.setProperty(
    '--primary-hover',
    darkenColor(primary, 0.15)
  )

  root.style.setProperty(
    '--primary-50',
    lightenColor(primary, 0.95)
  )

  root.style.setProperty(
    '--primary-100',
    lightenColor(primary, 0.88)
  )

  root.style.setProperty(
    '--primary-200',
    lightenColor(primary, 0.76)
  )

  root.style.setProperty(
    '--primary-300',
    lightenColor(primary, 0.55)
  )

  root.style.setProperty(
    '--primary-400',
    lightenColor(primary, 0.30)
  )

  root.style.setProperty('--primary-500', primary)

  if (rgb) {
    root.style.setProperty(
      '--primary-rgb',
      `${rgb.r}, ${rgb.g}, ${rgb.b}`
    )
  }
}

function applyAppearance(theme) {
  const root = document.documentElement

  if (theme === 'dark') {
    root.classList.add('dark')
    return
  }

  if (theme === 'light') {
    root.classList.remove('dark')
    return
  }

  const prefersDark = window.matchMedia(
    '(prefers-color-scheme: dark)'
  ).matches

  root.classList.toggle(
    'dark',
    prefersDark
  )
}

export function useTheme() {
  const auth = useAuthStore()

  const primaryColor = computed(() => {
    const storedUser = localStorage.getItem('user')

    if (storedUser) {
      try {
        const user = JSON.parse(storedUser)

        if (user?.primary_color) {
          return user.primary_color
        }
      } catch {
        // اطلاعات localStorage نامعتبر است
      }
    }

    return auth.user?.primary_color || DEFAULT_PRIMARY
  })

  const theme = computed(() => {
    const storedUser = localStorage.getItem('user')

    if (storedUser) {
      try {
        const user = JSON.parse(storedUser)

        if (user?.theme) {
          return user.theme
        }
      } catch {
        // اطلاعات localStorage نامعتبر است
      }
    }

    return auth.user?.theme || 'light'
  })

  function applyTheme() {
    applyColorVariables(primaryColor.value)
    applyAppearance(theme.value)
  }

  function updateTheme({
    primary_color,
    theme: newTheme
  } = {}) {
    const currentUser = auth.user || {}

    const updatedUser = {
      ...currentUser,

      primary_color:
        primary_color ||
        currentUser.primary_color ||
        DEFAULT_PRIMARY,

      theme:
        newTheme ||
        currentUser.theme ||
        'light'
    }

    auth.user = updatedUser

    localStorage.setItem(
      'user',
      JSON.stringify(updatedUser)
    )

    applyColorVariables(
      updatedUser.primary_color
    )

    applyAppearance(
      updatedUser.theme
    )
  }

  return {
    primaryColor,
    theme,
    applyTheme,
    updateTheme
  }
}