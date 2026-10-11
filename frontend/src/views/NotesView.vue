
<template>
  <main class="notes-center" :class="{ 'is-dark': isDark }" dir="rtl">
    <!-- Ambient background -->
    <div class="ambient ambient-purple"></div>
    <div class="ambient ambient-cyan"></div>
    <div class="ambient ambient-green"></div>

    <!-- Header -->
    <header class="page-header">
      <div class="header-brand">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
            <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
            <path d="M8 7h8M8 10h6"/>
          </svg>
        </div>

        <div>
          <span class="page-kicker">DOPAMINE / LEARNING CENTER</span>
          <h1>کتابخانهٔ جزوه‌ها</h1>
          <p>یادگیری عمیق‌تر، قدم‌به‌قدم و با تمرکز بیشتر.</p>
        </div>
      </div>

      <div class="header-actions">
        <button
          type="button"
          class="header-button refresh-button"
          :disabled="loading"
          @click="loadNotes"
          aria-label="بروزرسانی جزوه‌ها"
        >
          <svg :class="{ spinning: loading }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20 7v5h-5"/>
            <path d="M4.9 9A7.5 7.5 0 0 1 18 6l2 6"/>
            <path d="M4 17v-5h5"/>
            <path d="M19.1 15A7.5 7.5 0 0 1 6 18l-2-6"/>
          </svg>
          <span>{{ loading ? 'در حال بروزرسانی' : 'بروزرسانی' }}</span>
        </button>

        <RouterLink
          v-if="isAdmin"
          to="/notes/admin/new"
          class="header-button create-button"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          <span>ساخت جزوه</span>
        </RouterLink>
      </div>
    </header>

    <!-- Hero -->
    <section class="learning-hero">
      <div class="hero-grid"></div>
      <div class="hero-glow hero-glow-one"></div>
      <div class="hero-glow hero-glow-two"></div>

      <div class="hero-content">
        <div class="hero-overline">
          <span class="live-dot"></span>
          فضای یادگیری تو
          <span class="overline-divider">/</span>
          LEARNING SPACE
        </div>

        <h2>
          هر صفحه،
          <span class="gradient-text">یک پیشرفت تازه.</span>
        </h2>

        <p>
          جزوه‌هایت را پیدا کن، مطالعه را ادامه بده و هر روز
          یک قدم به هدفت نزدیک‌تر شو.
        </p>

        <div class="hero-pills">
          <span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
              <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
            </svg>
            {{ toPersianNumber(notes.length) }} جزوه
          </span>

          <span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="9"/>
              <path d="M12 7v5l3 2"/>
            </svg>
            مطالعه با برنامه
          </span>
        </div>
      </div>

      <div class="hero-visual" aria-hidden="true">
        <div class="visual-orbit orbit-large"></div>
        <div class="visual-orbit orbit-small"></div>

        <div class="floating-book book-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
            <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
          </svg>
        </div>

        <div class="floating-book book-front">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M5 4h14v17H5z"/>
            <path d="M8 8h8M8 12h8M8 16h5"/>
          </svg>
        </div>

        <div class="visual-star star-one">✦</div>
        <div class="visual-star star-two">✧</div>

        <div class="visual-label">
          <span class="visual-label-dot"></span>
          <span>
            <strong>مسیر پیشرفت</strong>
            <small>هر روز بهتر از دیروز</small>
          </span>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-grid">
      <article class="stat-card stat-purple">
        <div class="stat-top">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
              <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
            </svg>
          </div>
          <span class="stat-label">مجموع جزوه‌ها</span>
        </div>
        <strong class="stat-value">{{ toPersianNumber(notes.length) }}</strong>
        <span class="stat-foot">محتواهای آموزشی کتابخانه</span>
        <div class="stat-decoration decoration-purple"></div>
      </article>

      <article class="stat-card stat-cyan">
        <div class="stat-top">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="9"/>
              <path d="M12 7v5l3 2"/>
            </svg>
          </div>
          <span class="stat-label">در حال مطالعه</span>
        </div>
        <strong class="stat-value">{{ toPersianNumber(inProgressCount) }}</strong>
        <span class="stat-foot">جزوه‌های شروع‌شده و ناتمام</span>
        <div class="stat-decoration decoration-cyan"></div>
      </article>

      <article class="stat-card stat-green">
        <div class="stat-top">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="9"/>
              <path d="m8 12 2.5 2.5L16 9"/>
            </svg>
          </div>
          <span class="stat-label">تکمیل‌شده</span>
        </div>
        <strong class="stat-value">{{ toPersianNumber(completedCount) }}</strong>
        <span class="stat-foot">جزوه‌های به پایان رسیده</span>
        <div class="stat-decoration decoration-green"></div>
      </article>

      <article class="stat-card stat-pink">
        <div class="stat-top">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>
            </svg>
          </div>
          <span class="stat-label">علاقه‌مندی‌ها</span>
        </div>
        <strong class="stat-value">{{ toPersianNumber(bookmarkedCount) }}</strong>
        <span class="stat-foot">جزوه‌های ذخیره‌شده</span>
        <div class="stat-decoration decoration-pink"></div>
      </article>
    </section>

    <!-- Quick filters -->
    <section class="command-strip">
      <div class="command-heading">
        <span class="section-indicator"></span>
        <div>
          <strong>دسترسی سریع</strong>
          <small>کتابخانه را مطابق نیازت مرتب کن.</small>
        </div>
      </div>

      <div class="quick-filters">
        <button
          v-for="filter in quickFilters"
          :key="filter.value"
          type="button"
          class="quick-filter"
          :class="{ active: activeQuickFilter === filter.value }"
          @click="setQuickFilter(filter.value)"
        >
          <svg v-if="filter.value === 'all'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="3" width="7" height="7" rx="2"/>
            <rect x="14" y="3" width="7" height="7" rx="2"/>
            <rect x="3" y="14" width="7" height="7" rx="2"/>
            <rect x="14" y="14" width="7" height="7" rx="2"/>
          </svg>

          <svg v-else-if="filter.value === 'progress'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="9"/>
            <path d="M12 7v5l3 2"/>
          </svg>

          <svg v-else-if="filter.value === 'completed'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="m5 12 4 4L19 6"/>
            <circle cx="12" cy="12" r="9"/>
          </svg>

          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>
          </svg>

          <span>{{ filter.label }}</span>

          <small>{{ filterCount(filter.value) }}</small>
        </button>
      </div>
    </section>

    <!-- Search / Filters -->
    <section class="library-toolbar">
      <div class="toolbar-heading">
        <div>
          <span class="section-kicker">YOUR LIBRARY</span>
          <h2>جزوه‌های آموزشی</h2>
        </div>

        <span class="result-count">
          {{ toPersianNumber(filteredNotes.length) }} نتیجه
        </span>
      </div>

      <div class="toolbar-controls">
        <label class="search-field">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="7"/>
            <path d="m16 16 4 4"/>
          </svg>

          <input
            v-model="search"
            type="search"
            placeholder="جست‌وجو در عنوان، درس، پایه یا توضیحات..."
            aria-label="جست‌وجوی جزوه‌ها"
          />

          <button
            v-if="search"
            type="button"
            class="clear-search"
            aria-label="پاک کردن جست‌وجو"
            @click="search = ''"
          >
            ×
          </button>
        </label>

        <label class="subject-select-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 5h16M7 12h10m-7 7h4"/>
          </svg>

          <select v-model="subjectFilter" aria-label="فیلتر بر اساس درس">
            <option value="">همهٔ درس‌ها</option>
            <option
              v-for="subject in subjects"
              :key="subject"
              :value="subject"
            >
              {{ subject }}
            </option>
          </select>

          <svg class="select-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="m7 10 5 5 5-5"/>
          </svg>
        </label>

        <button
          v-if="hasActiveFilters"
          type="button"
          class="reset-button"
          @click="resetFilters"
        >
          پاک کردن فیلترها
        </button>
      </div>
    </section>

    <!-- Loading -->
    <section v-if="loading" class="state-card">
      <div class="loading-orbit">
        <div class="loading-orbit-inner"></div>
      </div>
      <strong>در حال آماده‌سازی کتابخانه...</strong>
      <p>داریم جزوه‌ها را برایت مرتب می‌کنیم.</p>
      <div class="loading-bars"><span></span><span></span><span></span></div>
    </section>

    <!-- Error -->
    <section v-else-if="error" class="state-card error-card">
      <div class="state-icon error-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M12 9v4m0 4h.01"/>
          <path d="M10.3 3.9 2.5 17.4A2 2 0 0 0 4.2 20h15.6a2 2 0 0 0 1.7-2.6L13.7 3.9a2 2 0 0 0-3.4 0Z"/>
        </svg>
      </div>
      <strong>دریافت جزوه‌ها ناموفق بود</strong>
      <p>{{ error }}</p>
      <button type="button" class="action-button primary-action" @click="loadNotes">
        تلاش دوباره
      </button>
    </section>

    <!-- Notes grid -->
    <section v-else-if="filteredNotes.length" class="notes-grid">
      <article
        v-for="(note, index) in filteredNotes"
        :key="note.id"
        class="note-card"
        :style="{
          '--card-index': index,
          '--cover': safeColor(note.cover_color),
          '--cover-soft': safeColor(note.cover_color)
        }"
      >
        <div class="card-ambient"></div>

        <div class="card-top">
          <div class="card-subject">
            <span class="subject-mark"></span>
            <span>{{ note.subject || 'جزوهٔ آموزشی' }}</span>
          </div>

          <div class="card-top-actions">
            <span
              v-if="isAdmin && note.status === 'draft'"
              class="status-badge draft-badge"
            >
              پیش‌نویس
            </span>

            <button
              type="button"
              class="favorite-button"
              :class="{ favorited: note.is_bookmarked }"
              :disabled="busyBookmarks.includes(note.id)"
              :aria-label="note.is_bookmarked ? 'حذف از علاقه‌مندی‌ها' : 'افزودن به علاقه‌مندی‌ها'"
              :title="note.is_bookmarked ? 'حذف از علاقه‌مندی‌ها' : 'ذخیره جزوه'"
              @click="bookmark(note)"
            >
              <svg viewBox="0 0 24 24" :fill="note.is_bookmarked ? 'currentColor' : 'none'" stroke="currentColor">
                <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Cover -->
        <div class="note-cover">
          <div class="cover-grid"></div>
          <div class="cover-glow"></div>

          <div class="cover-emblem">
            <span v-if="isEmoji(note.cover_icon)">{{ note.cover_icon }}</span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
              <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
              <path d="M8 7h8M8 10h6"/>
            </svg>
          </div>

          <div class="cover-copy">
            <span>{{ note.grade || 'همهٔ پایه‌ها' }}</span>
            <strong>{{ note.title }}</strong>
          </div>

          <div class="cover-decoration cover-decoration-one"></div>
          <div class="cover-decoration cover-decoration-two"></div>

          <span class="cover-index">
            {{ toPersianNumber(index + 1).padStart(2, '۰') }}
          </span>
        </div>

        <!-- Card body -->
        <div class="note-card-body">
          <div class="note-heading">
            <h3>{{ note.title }}</h3>
            <p>{{ note.subtitle || 'برای شروع یک یادگیری تازه آماده‌ای؟' }}</p>
          </div>

          <div class="note-meta">
            <span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/>
                <path d="M12 7v5l3 2"/>
              </svg>
              {{ toPersianNumber(note.estimated_minutes || 10) }} دقیقه
            </span>

            <span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
                <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
              </svg>
              {{ toPersianNumber(Array.isArray(note.blocks) ? note.blocks.length : 0) }} بخش
            </span>
          </div>

          <div v-if="note.tags?.length" class="note-tags">
            <span v-for="tag in note.tags.slice(0, 3)" :key="tag">
              #{{ tag }}
            </span>
            <span v-if="note.tags.length > 3" class="more-tags">
              +{{ toPersianNumber(note.tags.length - 3) }}
            </span>
          </div>

          <div v-else class="note-tags note-tags-empty">
            <span>{{ note.subject || 'مطالعه و یادگیری' }}</span>
          </div>

          <div class="progress-section">
            <div class="progress-heading">
              <span>پیشرفت مطالعه</span>
              <strong>{{ toPersianNumber(progressOf(note)) }}٪</strong>
            </div>

            <div
              class="progress-track"
              role="progressbar"
              :aria-valuenow="progressOf(note)"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`پیشرفت مطالعه ${note.title}`"
            >
              <span :style="{ width: `${progressOf(note)}%` }"></span>
            </div>
          </div>

          <div class="card-footer">
            <RouterLink :to="`/notes/${note.id}`" class="start-button">
              <span>
                {{ progressOf(note) >= 100 ? 'مرور دوباره' : progressOf(note) > 0 ? 'ادامهٔ مطالعه' : 'شروع مطالعه' }}
              </span>

              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M19 12H5m7-7-7 7 7 7"/>
              </svg>
            </RouterLink>

            <RouterLink
              v-if="isAdmin"
              :to="`/notes/admin/${note.id}/edit`"
              class="card-icon-button"
              title="ویرایش جزوه"
              aria-label="ویرایش جزوه"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m15 5 4 4M4 20l4-.8L19 8a2.1 2.1 0 0 0-3-3L5 16l-1 4Z"/>
              </svg>
            </RouterLink>

            <button
              v-if="isAdmin"
              type="button"
              class="card-icon-button delete-button"
              title="حذف جزوه"
              aria-label="حذف جزوه"
              @click="deleteNote(note)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 7h16M10 11v6m4-6v6M5 7l1 14h12l1-14M9 7V4h6v3"/>
              </svg>
            </button>
          </div>
        </div>
      </article>
    </section>

    <!-- Empty state -->
    <section v-else class="state-card empty-card">
      <div class="empty-visual">
        <div class="empty-orbit"></div>
        <div class="empty-book">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z"/>
            <path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20"/>
            <path d="M8 7h8M8 10h6"/>
          </svg>
        </div>
        <span class="empty-spark spark-a">✦</span>
        <span class="empty-spark spark-b">✧</span>
      </div>

      <span class="empty-kicker">NOTHING HERE YET</span>

      <h3>
        {{ emptyTitle }}
      </h3>

      <p>
        {{ emptyDescription }}
      </p>

      <div class="empty-actions">
        <button
          v-if="hasActiveFilters"
          type="button"
          class="action-button secondary-action"
          @click="resetFilters"
        >
          نمایش همهٔ جزوه‌ها
        </button>

        <RouterLink
          v-if="isAdmin && !hasActiveFilters"
          to="/notes/admin/new"
          class="action-button primary-action"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          ساخت اولین جزوه
        </RouterLink>
      </div>
    </section>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast" class="toast-message" role="status">
        <span class="toast-indicator"></span>
        {{ toast }}
      </div>
    </Transition>
  </main>
</template>

<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
  watch
} from 'vue'

import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { notesApi } from '../services/notes'

const auth = useAuthStore()

const isAdmin = computed(() =>
  Boolean(auth.user?.is_staff || auth.user?.is_superuser)
)

const notes = ref([])
const loading = ref(true)
const error = ref('')
const search = ref('')
const subjectFilter = ref('')
const showBookmarks = ref(false)
const toast = ref('')
const isDark = ref(false)
const activeQuickFilter = ref('all')
const busyBookmarks = ref([])

let themeObserver = null
let toastTimer = null

const quickFilters = [
  { value: 'all', label: 'همهٔ جزوه‌ها' },
  { value: 'progress', label: 'در حال مطالعه' },
  { value: 'completed', label: 'تکمیل‌شده‌ها' },
  { value: 'bookmarks', label: 'علاقه‌مندی‌ها' }
]

function progressOf(note) {
  const value = Number(note?.progress_percent) || 0
  return Math.min(100, Math.max(0, value))
}

const subjects = computed(() =>
  [...new Set(notes.value.map(note => note.subject).filter(Boolean))]
    .sort((a, b) => String(a).localeCompare(String(b), 'fa'))
)

const inProgressCount = computed(() =>
  notes.value.filter(note => progressOf(note) > 0 && progressOf(note) < 100).length
)

const completedCount = computed(() =>
  notes.value.filter(note => progressOf(note) >= 100).length
)

const bookmarkedCount = computed(() =>
  notes.value.filter(note => note.is_bookmarked).length
)

const hasActiveFilters = computed(() =>
  Boolean(
    search.value.trim() ||
    subjectFilter.value ||
    activeQuickFilter.value !== 'all'
  )
)

const filteredNotes = computed(() => {
  const query = search.value.trim().toLocaleLowerCase('fa')

  return notes.value.filter(note => {
    const searchable = [
      note.title,
      note.subtitle,
      note.subject,
      note.grade,
      ...(Array.isArray(note.tags) ? note.tags : [])
    ]

    const matchesSearch = !query || searchable.some(value =>
      String(value || '').toLocaleLowerCase('fa').includes(query)
    )

    const matchesSubject =
      !subjectFilter.value || note.subject === subjectFilter.value

    let matchesQuickFilter = true

    if (activeQuickFilter.value === 'progress') {
      matchesQuickFilter =
        progressOf(note) > 0 && progressOf(note) < 100
    } else if (activeQuickFilter.value === 'completed') {
      matchesQuickFilter = progressOf(note) >= 100
    } else if (activeQuickFilter.value === 'bookmarks') {
      matchesQuickFilter = Boolean(note.is_bookmarked)
    }

    return matchesSearch && matchesSubject && matchesQuickFilter
  })
})

const emptyTitle = computed(() => {
  if (search.value.trim() || subjectFilter.value) {
    return 'جزوه‌ای با این مشخصات پیدا نشد'
  }

  if (activeQuickFilter.value === 'progress') {
    return 'هنوز مطالعه‌ای را شروع نکرده‌ای'
  }

  if (activeQuickFilter.value === 'completed') {
    return 'هنوز جزوه‌ای را به پایان نرسانده‌ای'
  }

  if (activeQuickFilter.value === 'bookmarks') {
    return 'هنوز جزوه‌ای ذخیره نکرده‌ای'
  }

  return 'کتابخانه در انتظار اولین جزوه است'
})

const emptyDescription = computed(() => {
  if (hasActiveFilters.value) {
    return 'فیلترها را تغییر بده یا همهٔ جزوه‌ها را ببین تا محتوای موردنظرت را پیدا کنی.'
  }

  return isAdmin.value
    ? 'اولین جزوهٔ آموزشی را بساز تا مسیر یادگیری کاربران آغاز شود.'
    : 'به‌زودی محتوای آموزشی جدید در این بخش نمایش داده می‌شود.'
})

function filterCount(filter) {
  if (filter === 'all') return notes.value.length
  if (filter === 'progress') return inProgressCount.value
  if (filter === 'completed') return completedCount.value
  if (filter === 'bookmarks') return bookmarkedCount.value
  return 0
}

function toPersianNumber(value) {
  return String(value ?? 0).replace(/\d/g, digit =>
    '۰۱۲۳۴۵۶۷۸۹'[Number(digit)]
  )
}

function safeColor(value) {
  return typeof value === 'string' && /^#[0-9a-f]{3}([0-9a-f]{3})?$/i.test(value)
    ? value
    : '#7055e8'
}

function isEmoji(value) {
  if (!value || typeof value !== 'string') return false

  // Supports the existing emoji cover field without adding a dependency.
  return /[^\u0000-\u00ff]/u.test(value) &&
    !/^[a-zA-Z0-9_-]+$/.test(value)
}

function detectDark() {
  const root = document.documentElement
  const body = document.body

  return (
    root.getAttribute('data-theme') === 'dark' ||
    body?.getAttribute('data-theme') === 'dark' ||
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

  const config = {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style']
  }

  themeObserver.observe(document.documentElement, config)

  if (document.body) {
    themeObserver.observe(document.body, config)
  }
}

function showToast(message) {
  toast.value = message

  if (toastTimer) clearTimeout(toastTimer)

  toastTimer = setTimeout(() => {
    toast.value = ''
    toastTimer = null
  }, 2600)
}

async function loadNotes() {
  loading.value = true
  error.value = ''

  try {
    const response = showBookmarks.value
      ? await notesApi.bookmarks()
      : await (isAdmin.value ? notesApi.mine() : notesApi.list())

    const data = response.data
    notes.value = Array.isArray(data)
      ? data
      : Array.isArray(data?.results)
        ? data.results
        : []
  } catch (err) {
    error.value =
      err?.response?.data?.detail ||
      'اتصال به سرور برقرار نشد. آدرس API و وضعیت ورود کاربر را بررسی کن.'
  } finally {
    loading.value = false
  }
}

async function setQuickFilter(filter) {
  activeQuickFilter.value = filter

  const needsBookmarks = filter === 'bookmarks'

  if (showBookmarks.value !== needsBookmarks) {
    showBookmarks.value = needsBookmarks
    await loadNotes()
  }
}

async function bookmark(note) {
  if (busyBookmarks.value.includes(note.id)) return

  busyBookmarks.value = [...busyBookmarks.value, note.id]

  try {
    const response = await notesApi.bookmark(note.id)
    const isBookmarked = Boolean(response.data?.bookmarked)

    // Replace the object to keep Vue's reactive updates predictable.
    notes.value = notes.value.map(item =>
      item.id === note.id
        ? { ...item, is_bookmarked: isBookmarked }
        : item
    )

    showToast(
      isBookmarked
        ? 'جزوه به علاقه‌مندی‌ها اضافه شد.'
        : 'جزوه از علاقه‌مندی‌ها حذف شد.'
    )

    // Keep the bookmark view in sync with the server.
    if (showBookmarks.value && !isBookmarked) {
      notes.value = notes.value.filter(item => item.id !== note.id)
    }
  } catch (err) {
    showToast(
      err?.response?.data?.detail ||
      'برای ذخیرهٔ جزوه باید وارد حساب کاربری شده باشی.'
    )
  } finally {
    busyBookmarks.value = busyBookmarks.value.filter(id => id !== note.id)
  }
}

async function deleteNote(note) {
  const confirmed = window.confirm(
    `جزوهٔ «${note.title}» حذف شود؟ این کار برگشت‌پذیر نیست.`
  )

  if (!confirmed) return

  try {
    await notesApi.remove(note.id)
    notes.value = notes.value.filter(item => item.id !== note.id)
    showToast('جزوه با موفقیت حذف شد.')
  } catch (err) {
    showToast(err?.response?.data?.detail || 'حذف جزوه انجام نشد.')
  }
}

function resetFilters() {
  search.value = ''
  subjectFilter.value = ''
  activeQuickFilter.value = 'all'

  if (showBookmarks.value) {
    showBookmarks.value = false
    loadNotes()
  }
}

watch(isAdmin, () => {
  if (!showBookmarks.value) loadNotes()
})

onMounted(() => {
  observeTheme()
  loadNotes()
})

onBeforeUnmount(() => {
  themeObserver?.disconnect()

  if (toastTimer) {
    clearTimeout(toastTimer)
    toastTimer = null
  }
})
</script>

<style scoped>
.notes-center {
  --nc-bg: #f5f6fb;
  --nc-surface: rgba(255, 255, 255, .84);
  --nc-surface-solid: #fff;
  --nc-surface-muted: #f7f8fc;
  --nc-text: #20243a;
  --nc-text-soft: #555d76;
  --nc-muted: #8b91a7;
  --nc-line: rgba(105, 113, 150, .14);
  --nc-primary: var(--primary, #7055e8);
  --nc-primary-rgb: var(--primary-rgb, 112, 85, 232);
  --nc-shadow: 0 12px 35px rgba(31, 38, 76, .055);
  --nc-ease: cubic-bezier(.2, .75, .25, 1);

  position: relative;
  isolation: isolate;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
  padding: 26px clamp(14px, 3.5vw, 48px) 125px;
  color: var(--nc-text);
  background:
    radial-gradient(ellipse at 82% 0%, rgba(112, 85, 232, .055), transparent 30%),
    var(--nc-bg);
  font-family: inherit;
  transition: background .3s ease, color .3s ease;
}

.notes-center *,
.notes-center *::before,
.notes-center *::after {
  box-sizing: border-box;
}

.notes-center button,
.notes-center input,
.notes-center select {
  font: inherit;
}

.notes-center button,
.notes-center a {
  -webkit-tap-highlight-color: transparent;
}

.notes-center button:focus-visible,
.notes-center a:focus-visible,
.notes-center input:focus-visible,
.notes-center select:focus-visible {
  outline: 3px solid rgba(112, 85, 232, .35);
  outline-offset: 3px;
}

.notes-center.is-dark {
  --nc-bg: #0d111d;
  --nc-surface: rgba(24, 29, 45, .82);
  --nc-surface-solid: #171c2c;
  --nc-surface-muted: rgba(255, 255, 255, .035);
  --nc-text: #f0f1fb;
  --nc-text-soft: #b3bad0;
  --nc-muted: #858da8;
  --nc-line: rgba(177, 184, 220, .13);
  --nc-shadow: 0 15px 42px rgba(0, 0, 0, .16);

  background:
    radial-gradient(ellipse at 80% 0%, rgba(112, 85, 232, .13), transparent 32%),
    radial-gradient(ellipse at 0% 48%, rgba(24, 185, 210, .035), transparent 30%),
    var(--nc-bg);
}

.ambient {
  position: absolute;
  z-index: -1;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  filter: blur(95px);
  opacity: .12;
  pointer-events: none;
  animation: ambientDrift 15s ease-in-out infinite alternate;
}

.ambient-purple {
  top: 340px;
  right: -180px;
  background: #7758ff;
}

.ambient-cyan {
  top: 1080px;
  left: -170px;
  background: #18c4dc;
  animation-delay: -5s;
}

.ambient-green {
  top: 2100px;
  right: 20%;
  background: #13c98b;
  animation-delay: -9s;
}

.page-header {
  width: min(100%, 1500px);
  margin: 0 auto 26px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  animation: enterUp .55s var(--nc-ease) both;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.brand-icon {
  width: 54px;
  height: 54px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border: 1px solid rgba(112, 85, 232, .18);
  border-radius: 17px;
  color: var(--nc-primary);
  background: linear-gradient(145deg, rgba(112, 85, 232, .13), rgba(112, 85, 232, .035));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .2);
}

.brand-icon svg {
  width: 25px;
  height: 25px;
  stroke-width: 1.7;
}

.page-kicker,
.section-kicker {
  display: block;
  color: var(--nc-primary);
  font-size: 9px;
  font-weight: 950;
  letter-spacing: 1.7px;
  direction: ltr;
  text-align: right;
}

.header-brand h1 {
  margin: 5px 0 4px;
  font-size: clamp(22px, 2.7vw, 31px);
  font-weight: 950;
  letter-spacing: -.9px;
  line-height: 1.45;
}

.header-brand p {
  margin: 0;
  color: var(--nc-muted);
  font-size: 11px;
  line-height: 1.8;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.header-button {
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 13px;
  border: 1px solid var(--nc-line);
  border-radius: 12px;
  color: var(--nc-text-soft);
  background: var(--nc-surface);
  text-decoration: none;
  font-size: 10px !important;
  font-weight: 850 !important;
  cursor: pointer;
  transition: transform .25s var(--nc-ease), border-color .25s ease, background .25s ease;
}

.header-button svg {
  width: 16px;
  height: 16px;
  stroke-width: 1.8;
}

.header-button:hover {
  transform: translateY(-2px);
  border-color: rgba(112, 85, 232, .32);
}

.header-button:disabled {
  opacity: .65;
  cursor: wait;
}

.create-button {
  border-color: transparent;
  color: #fff;
  background: linear-gradient(125deg, #8064f5, #6246d6);
  box-shadow: 0 7px 20px rgba(112, 85, 232, .2);
}

.create-button:hover {
  color: #fff;
  box-shadow: 0 10px 25px rgba(112, 85, 232, .26);
}

.spinning {
  animation: spin .9s linear infinite;
}

/* Hero */
.learning-hero {
  position: relative;
  width: min(100%, 1500px);
  min-height: 240px;
  margin: 0 auto 19px;
  padding: clamp(26px, 4vw, 42px);
  overflow: hidden;
  isolation: isolate;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border: 1px solid rgba(255, 255, 255, .09);
  border-radius: 26px;
  color: #fff;
  background:
    linear-gradient(112deg, #17152d 0%, #28204d 51%, #3b2b70 100%);
  box-shadow: 0 22px 55px rgba(46, 32, 96, .14);
  animation: enterUp .65s .06s var(--nc-ease) both;
}

.hero-grid,
.cover-grid {
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255, 255, 255, .035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, .035) 1px, transparent 1px);
  background-size: 31px 31px;
  mask-image: linear-gradient(110deg, transparent, #000 50%, #000);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 650px;
}

.hero-overline {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 9px;
  color: #d5caff;
  font-size: 9px;
  font-weight: 850;
}

.live-dot,
.visual-label-dot,
.subject-mark,
.toast-indicator {
  width: 7px;
  height: 7px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #4cdbb0;
  box-shadow: 0 0 0 4px rgba(76, 219, 176, .12);
}

.overline-divider {
  color: rgba(255, 255, 255, .3);
}

.hero-content h2 {
  margin: 20px 0 11px;
  font-size: clamp(25px, 3.5vw, 40px);
  font-weight: 950;
  line-height: 1.55;
  letter-spacing: -1.4px;
}

.gradient-text {
  display: inline;
  color: #c8b9ff;
  background: linear-gradient(90deg, #c7b9ff, #80e8e4);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-content > p {
  max-width: 530px;
  margin: 0;
  color: #c5c1dc;
  font-size: 12px;
  line-height: 2;
}

.hero-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin-top: 20px;
}

.hero-pills > span {
  min-height: 31px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 11px;
  border: 1px solid rgba(255, 255, 255, .11);
  border-radius: 9px;
  color: #e0dcf3;
  background: rgba(255, 255, 255, .055);
  font-size: 9px;
  font-weight: 750;
}

.hero-pills svg {
  width: 14px;
  height: 14px;
  color: #b9a8ff;
}

.hero-glow {
  position: absolute;
  z-index: -1;
  border-radius: 50%;
  filter: blur(2px);
  pointer-events: none;
}

.hero-glow-one {
  width: 320px;
  height: 320px;
  top: -220px;
  left: 16%;
  background: rgba(145, 112, 255, .23);
}

.hero-glow-two {
  width: 240px;
  height: 240px;
  right: 26%;
  bottom: -205px;
  background: rgba(43, 212, 211, .13);
}

.hero-visual {
  position: relative;
  flex: 0 0 230px;
  height: 190px;
  display: grid;
  place-items: center;
}

.visual-orbit {
  position: absolute;
  left: 50%;
  top: 45%;
  border: 1px solid rgba(206, 191, 255, .19);
  border-radius: 50%;
  transform: translate(-50%, -50%) rotate(-22deg);
}

.orbit-large {
  width: 185px;
  height: 140px;
}

.orbit-small {
  width: 135px;
  height: 185px;
  transform: translate(-50%, -50%) rotate(34deg);
}

.floating-book {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, .17);
  border-radius: 21px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, .22), inset 0 1px 0 rgba(255, 255, 255, .14);
}

.floating-book svg {
  width: 42px;
  height: 42px;
  stroke-width: 1.35;
}

.book-back {
  width: 88px;
  height: 105px;
  top: 23px;
  right: 29px;
  color: #a5dff5;
  background: linear-gradient(145deg, #304e78, #242647);
  transform: rotate(13deg);
  animation: floatBook 5s ease-in-out infinite;
}

.book-front {
  width: 91px;
  height: 110px;
  top: 34px;
  left: 29px;
  color: #e2d8ff;
  background: linear-gradient(145deg, #775ce1, #483b94);
  transform: rotate(-11deg);
  animation: floatBook 5s ease-in-out -2.5s infinite;
}

.visual-star {
  position: absolute;
  color: #d7c9ff;
}

.star-one {
  top: 15px;
  right: 33px;
  font-size: 24px;
  animation: starPulse 3s ease-in-out infinite;
}

.star-two {
  bottom: 36px;
  left: 21px;
  color: #72e6db;
  font-size: 27px;
  animation: starPulse 3s ease-in-out -1.5s infinite;
}

.visual-label {
  position: absolute;
  right: -10px;
  bottom: -2px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 13px;
  border: 1px solid rgba(255, 255, 255, .13);
  border-radius: 14px;
  background: rgba(20, 18, 44, .83);
  box-shadow: 0 12px 30px rgba(0, 0, 0, .15);
  backdrop-filter: blur(15px);
}

.visual-label strong,
.visual-label small {
  display: block;
}

.visual-label strong {
  font-size: 10px;
}

.visual-label small {
  margin-top: 4px;
  color: #aaa5ca;
  font-size: 8px;
}

/* Statistics */
.stats-grid {
  width: min(100%, 1500px);
  margin: 0 auto 30px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 13px;
}

.stat-card {
  position: relative;
  min-width: 0;
  min-height: 137px;
  padding: 17px;
  overflow: hidden;
  border: 1px solid var(--nc-line);
  border-radius: 20px;
  background: var(--nc-surface);
  box-shadow: var(--nc-shadow);
  backdrop-filter: blur(20px);
  animation: enterUp .6s var(--nc-ease) both;
  transition: transform .3s var(--nc-ease), border-color .3s ease;
}

.stat-card:nth-child(2) { animation-delay: .05s; }
.stat-card:nth-child(3) { animation-delay: .1s; }
.stat-card:nth-child(4) { animation-delay: .15s; }

.stat-card:hover {
  transform: translateY(-3px);
}

.stat-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 9px;
}

.stat-icon {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 11px;
}

.stat-icon svg {
  width: 17px;
  height: 17px;
  stroke-width: 1.8;
}

.stat-label {
  color: var(--nc-text-soft);
  font-size: 10px;
  font-weight: 800;
}

.stat-value {
  position: relative;
  z-index: 1;
  display: block;
  margin: 13px 0 5px;
  font-size: 27px;
  font-weight: 950;
  line-height: 1.15;
  letter-spacing: -.7px;
}

.stat-foot {
  position: relative;
  z-index: 1;
  display: block;
  color: var(--nc-muted);
  font-size: 9px;
  line-height: 1.8;
}

.stat-purple .stat-icon {
  color: #896af3;
  background: rgba(137, 106, 243, .12);
}
.stat-purple .stat-value { color: #896af3; }

.stat-cyan .stat-icon {
  color: #159fbe;
  background: rgba(21, 159, 190, .11);
}
.stat-cyan .stat-value { color: #159fbe; }

.stat-green .stat-icon {
  color: #159f80;
  background: rgba(21, 159, 128, .11);
}
.stat-green .stat-value { color: #159f80; }

.stat-pink .stat-icon {
  color: #df689d;
  background: rgba(223, 104, 157, .11);
}
.stat-pink .stat-value { color: #df689d; }

.is-dark .stat-cyan .stat-value { color: #5bd2e7; }
.is-dark .stat-green .stat-value { color: #5bd9b0; }
.is-dark .stat-pink .stat-value { color: #f0a0c2; }

.stat-decoration {
  position: absolute;
  width: 85px;
  height: 85px;
  left: -28px;
  bottom: -39px;
  border: 1px solid currentColor;
  border-radius: 27px;
  transform: rotate(31deg);
  opacity: .08;
  box-shadow: 0 0 0 14px currentColor, 0 0 0 29px currentColor;
  pointer-events: none;
}

.decoration-purple { color: #896af3; }
.decoration-cyan { color: #159fbe; }
.decoration-green { color: #159f80; }
.decoration-pink { color: #df689d; }

/* Quick filters */
.command-strip {
  width: min(100%, 1500px);
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 17px;
  padding: 16px 19px;
  border: 1px solid var(--nc-line);
  border-radius: 19px;
  background: var(--nc-surface);
  box-shadow: var(--nc-shadow);
}

.command-heading {
  display: flex;
  align-items: center;
  gap: 11px;
}

.section-indicator {
  width: 4px;
  height: 34px;
  flex-shrink: 0;
  border-radius: 5px;
  background: linear-gradient(#8d6df5, #39c9d1);
}

.command-heading strong,
.command-heading small {
  display: block;
}

.command-heading strong {
  font-size: 11px;
  font-weight: 950;
}

.command-heading small {
  margin-top: 5px;
  color: var(--nc-muted);
  font-size: 9px;
}

.quick-filters {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
}

.quick-filter {
  min-height: 37px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 0 10px;
  border: 1px solid transparent;
  border-radius: 10px;
  color: var(--nc-text-soft);
  background: var(--nc-surface-muted);
  cursor: pointer;
  transition: color .25s ease, background .25s ease, border-color .25s ease, transform .25s var(--nc-ease);
}

.quick-filter:hover {
  transform: translateY(-1px);
  border-color: var(--nc-line);
}

.quick-filter svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.quick-filter > span {
  font-size: 9px;
  font-weight: 800;
}

.quick-filter > small {
  min-width: 19px;
  height: 19px;
  display: grid;
  place-items: center;
  padding: 0 4px;
  border-radius: 6px;
  color: var(--nc-muted);
  background: rgba(127, 127, 127, .07);
  font-size: 8px;
  font-weight: 850;
}

.quick-filter.active {
  border-color: rgba(var(--nc-primary-rgb), .2);
  color: var(--nc-primary);
  background: rgba(var(--nc-primary-rgb), .085);
}

.quick-filter.active > small {
  color: var(--nc-primary);
  background: rgba(var(--nc-primary-rgb), .11);
}

/* Library toolbar */
.library-toolbar {
  width: min(100%, 1500px);
  margin: 0 auto 17px;
}

.toolbar-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 15px;
}

.toolbar-heading h2 {
  margin: 5px 0 0;
  font-size: 20px;
  font-weight: 950;
  letter-spacing: -.5px;
}

.result-count {
  padding: 7px 10px;
  border: 1px solid var(--nc-line);
  border-radius: 9px;
  color: var(--nc-muted);
  background: var(--nc-surface);
  font-size: 9px;
  font-weight: 800;
  white-space: nowrap;
}

.toolbar-controls {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 9px;
}

.search-field,
.subject-select-wrap {
  min-height: 45px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 13px;
  border: 1px solid var(--nc-line);
  border-radius: 12px;
  color: var(--nc-muted);
  background: var(--nc-surface);
  transition: border-color .25s ease, box-shadow .25s ease;
}

.search-field {
  flex: 1 1 350px;
  min-width: 0;
}

.search-field:focus-within,
.subject-select-wrap:focus-within {
  border-color: rgba(var(--nc-primary-rgb), .45);
  box-shadow: 0 0 0 3px rgba(var(--nc-primary-rgb), .065);
}

.search-field > svg,
.subject-select-wrap > svg {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  stroke-width: 1.8;
}

.search-field input {
  width: 100%;
  min-width: 0;
  height: 43px;
  padding: 0;
  border: 0;
  outline: 0;
  color: var(--nc-text);
  background: transparent;
  font-size: 10px !important;
}

.search-field input::placeholder {
  color: var(--nc-muted);
}

.search-field input:focus-visible {
  outline: none;
}

.clear-search {
  width: 23px;
  height: 23px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 0;
  border-radius: 7px;
  color: var(--nc-muted);
  background: var(--nc-surface-muted);
  font-size: 19px !important;
  cursor: pointer;
}

.subject-select-wrap {
  position: relative;
  flex: 0 1 200px;
}

.subject-select-wrap select {
  width: 100%;
  min-width: 0;
  height: 43px;
  padding: 0 0 0 21px;
  appearance: none;
  border: 0;
  outline: 0;
  color: var(--nc-text);
  background: transparent;
  font-size: 10px !important;
  cursor: pointer;
}

.subject-select-wrap select option {
  color: #20243a;
  background: #fff;
}

.subject-select-wrap .select-chevron {
  position: absolute;
  left: 10px;
  width: 13px;
  height: 13px;
  pointer-events: none;
}

.reset-button {
  min-height: 43px;
  padding: 0 12px;
  border: 1px solid rgba(235, 93, 113, .17);
  border-radius: 11px;
  color: #dc6579;
  background: rgba(235, 93, 113, .06);
  font-size: 9px !important;
  font-weight: 850 !important;
  cursor: pointer;
  transition: background .2s ease;
}

.reset-button:hover {
  background: rgba(235, 93, 113, .12);
}

/* Cards */
.notes-grid {
  width: min(100%, 1500px);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  align-items: stretch;
}

.note-card {
  --card-progress: 0%;
  position: relative;
  min-width: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--nc-line);
  border-radius: 22px;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, .55), rgba(255, 255, 255, .14)),
    var(--nc-surface);
  box-shadow: var(--nc-shadow);
  backdrop-filter: blur(22px);
  animation: cardIn .6s var(--nc-ease) both;
  animation-delay: calc(min(var(--card-index), 8) * 45ms);
  transition:
    transform .35s var(--nc-ease),
    border-color .3s ease,
    box-shadow .35s ease;
}

.is-dark .note-card {
  background:
    linear-gradient(145deg, rgba(35, 40, 61, .75), rgba(17, 22, 36, .68)),
    var(--nc-surface);
}

.note-card:hover {
  transform: translateY(-5px);
  border-color: rgba(var(--nc-primary-rgb), .27);
  box-shadow: 0 19px 44px rgba(31, 38, 76, .09);
}

.is-dark .note-card:hover {
  box-shadow: 0 19px 44px rgba(0, 0, 0, .22);
}

.card-ambient {
  position: absolute;
  z-index: 0;
  top: -110px;
  left: -90px;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  background: var(--cover);
  filter: blur(100px);
  opacity: .08;
  pointer-events: none;
  transition: opacity .35s ease;
}

.note-card:hover .card-ambient {
  opacity: .19;
}

.card-top {
  position: relative;
  z-index: 2;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 15px 15px 12px;
}

.card-subject {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--nc-text-soft);
  font-size: 10px;
  font-weight: 850;
}

.card-subject > span:last-child {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.subject-mark {
  width: 6px;
  height: 6px;
  background: var(--cover);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--cover) 12%, transparent);
}

.card-top-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 7px;
  border-radius: 7px;
  font-size: 8px;
  font-weight: 900;
}

.draft-badge {
  color: #ad791b;
  background: rgba(244, 186, 65, .13);
  border: 1px solid rgba(244, 186, 65, .18);
}

.favorite-button {
  width: 31px;
  height: 31px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border: 1px solid var(--nc-line);
  border-radius: 9px;
  color: var(--nc-muted);
  background: var(--nc-surface-muted);
  cursor: pointer;
  transition: color .25s ease, background .25s ease, transform .25s var(--nc-ease);
}

.favorite-button svg {
  width: 15px;
  height: 15px;
  stroke-width: 1.8;
}

.favorite-button:hover {
  transform: scale(1.06);
  color: #e56b9c;
}

.favorite-button.favorited {
  color: #e56b9c;
  background: rgba(229, 107, 156, .1);
  border-color: rgba(229, 107, 156, .2);
}

.favorite-button:disabled {
  opacity: .5;
  cursor: wait;
}

/* Cover */
.note-cover {
  position: relative;
  isolation: isolate;
  min-height: 164px;
  margin: 0 13px;
  padding: 17px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid rgba(255, 255, 255, .15);
  border-radius: 15px;
  color: #fff;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--cover) 92%, #17142e), color-mix(in srgb, var(--cover) 48%, #17142e));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .14);
}

.note-cover .cover-grid {
  z-index: -2;
  opacity: .75;
  background-size: 23px 23px;
}

.cover-glow {
  position: absolute;
  z-index: -1;
  top: -95px;
  left: -45px;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  background: rgba(255, 255, 255, .15);
  filter: blur(30px);
}

.cover-emblem {
  position: relative;
  z-index: 1;
  width: 43px;
  height: 43px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, .24);
  border-radius: 13px;
  color: #fff;
  background: rgba(255, 255, 255, .12);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .13);
  backdrop-filter: blur(8px);
}

.cover-emblem > span {
  font-size: 23px;
  line-height: 1;
}

.cover-emblem svg {
  width: 24px;
  height: 24px;
  stroke-width: 1.6;
}

.cover-copy {
  position: relative;
  z-index: 1;
  max-width: 88%;
}

.cover-copy > span {
  display: block;
  margin-bottom: 4px;
  color: rgba(255, 255, 255, .75);
  font-size: 8px;
  font-weight: 800;
}

.cover-copy strong {
  display: -webkit-box;
  overflow: hidden;
  color: #fff;
  font-size: 14px;
  font-weight: 950;
  line-height: 1.7;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow-wrap: anywhere;
}

.cover-decoration {
  position: absolute;
  z-index: -1;
  width: 105px;
  height: 105px;
  border: 1px solid rgba(255, 255, 255, .22);
  border-radius: 27px;
  transform: rotate(32deg);
  pointer-events: none;
}

.cover-decoration-one {
  top: 7px;
  right: -29px;
  box-shadow: 0 0 0 14px rgba(255, 255, 255, .045);
}

.cover-decoration-two {
  right: 43px;
  bottom: -78px;
  width: 125px;
  height: 125px;
  opacity: .6;
}

.cover-index {
  position: absolute;
  left: 12px;
  top: 12px;
  color: rgba(255, 255, 255, .45);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 1px;
}

.note-card-body {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.note-heading h3 {
  display: -webkit-box;
  min-height: 28px;
  margin: 0;
  overflow: hidden;
  color: var(--nc-text);
  font-size: 14px;
  font-weight: 950;
  line-height: 1.9;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow-wrap: anywhere;
}

.note-heading p {
  display: -webkit-box;
  min-height: 37px;
  margin: 5px 0 0;
  overflow: hidden;
  color: var(--nc-muted);
  font-size: 10px;
  line-height: 1.9;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.note-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
  padding-top: 11px;
  border-top: 1px solid var(--nc-line);
}

.note-meta > span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--nc-text-soft);
  font-size: 9px;
  font-weight: 750;
}

.note-meta svg {
  width: 13px;
  height: 13px;
  color: var(--nc-muted);
}

.note-tags {
  min-height: 25px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 10px;
}

.note-tags span {
  max-width: 100%;
  padding: 4px 7px;
  overflow: hidden;
  border: 1px solid rgba(var(--nc-primary-rgb), .1);
  border-radius: 6px;
  color: var(--nc-primary);
  background: rgba(var(--nc-primary-rgb), .065);
  font-size: 8px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.note-tags .more-tags {
  color: var(--nc-muted);
  border-color: var(--nc-line);
  background: var(--nc-surface-muted);
}

.note-tags-empty span {
  color: var(--nc-muted);
  border-color: var(--nc-line);
  background: var(--nc-surface-muted);
}

.progress-section {
  margin-top: 15px;
}

.progress-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
  color: var(--nc-muted);
  font-size: 9px;
}

.progress-heading strong {
  color: var(--nc-text-soft);
  font-size: 9px;
  font-weight: 900;
  font-variant-numeric: tabular-nums;
}

.progress-track {
  height: 5px;
  overflow: hidden;
  border-radius: 10px;
  background: rgba(135, 143, 171, .13);
}

.progress-track > span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--cover), #49cdbb);
  transition: width .65s var(--nc-ease);
}

.card-footer {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--nc-line);
}

.start-button {
  min-width: 0;
  min-height: 40px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 7px;
  padding: 0 12px;
  border: 1px solid rgba(var(--nc-primary-rgb), .12);
  border-radius: 10px;
  color: #fff;
  background: linear-gradient(120deg, #8064f2, #6448d8);
  text-decoration: none;
  font-size: 10px;
  font-weight: 900;
  transition: transform .25s var(--nc-ease), box-shadow .25s ease, filter .25s ease;
}

.start-button:hover {
  transform: translateY(-2px);
  filter: brightness(1.06);
  box-shadow: 0 7px 19px rgba(112, 85, 232, .2);
}

.start-button svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  transition: transform .25s ease;
}

.start-button:hover svg {
  transform: translateX(-3px);
}

.card-icon-button {
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border: 1px solid var(--nc-line);
  border-radius: 10px;
  color: var(--nc-text-soft);
  background: var(--nc-surface-muted);
  cursor: pointer;
  transition: color .2s ease, border-color .2s ease, background .2s ease;
}

.card-icon-button svg {
  width: 16px;
  height: 16px;
}

.card-icon-button:hover {
  color: var(--nc-primary);
  border-color: rgba(var(--nc-primary-rgb), .35);
  background: rgba(var(--nc-primary-rgb), .07);
}

.delete-button:hover {
  color: #e45d76;
  border-color: rgba(228, 93, 118, .3);
  background: rgba(228, 93, 118, .07);
}

/* States */
.state-card {
  width: min(100%, 1500px);
  min-height: 290px;
  margin: 0 auto;
  padding: 36px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 9px;
  border: 1px solid var(--nc-line);
  border-radius: 23px;
  background: var(--nc-surface);
  box-shadow: var(--nc-shadow);
  text-align: center;
  animation: enterUp .4s var(--nc-ease) both;
}

.state-card > strong {
  margin-top: 5px;
  color: var(--nc-text);
  font-size: 14px;
  font-weight: 950;
}

.state-card > p {
  max-width: 480px;
  margin: 0;
  color: var(--nc-muted);
  font-size: 10px;
  line-height: 2;
  overflow-wrap: anywhere;
}

.loading-orbit {
  width: 51px;
  height: 51px;
  display: grid;
  place-items: center;
  border: 2px solid rgba(var(--nc-primary-rgb), .13);
  border-top-color: var(--nc-primary);
  border-right-color: #39c8d0;
  border-radius: 50%;
  animation: spin 1.1s linear infinite;
}

.loading-orbit-inner {
  width: 25px;
  height: 25px;
  border: 2px solid rgba(57, 200, 208, .15);
  border-bottom-color: #39c8d0;
  border-radius: 50%;
}

.loading-bars {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 9px;
}

.loading-bars span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--nc-primary);
  animation: loadingPulse .8s ease-in-out infinite alternate;
}

.loading-bars span:nth-child(2) {
  animation-delay: .2s;
}

.loading-bars span:nth-child(3) {
  animation-delay: .4s;
}

.error-icon {
  color: #e45d76 !important;
  background: rgba(228, 93, 118, .09) !important;
}

.error-icon svg {
  width: 25px;
  height: 25px;
}

.error-card > strong {
  color: #e45d76;
}

.action-button {
  min-height: 41px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
  padding: 0 16px;
  border: 1px solid transparent;
  border-radius: 11px;
  text-decoration: none;
  font-size: 10px;
  font-weight: 900;
  cursor: pointer;
  transition: transform .2s ease, filter .2s ease;
}

.action-button:hover {
  transform: translateY(-2px);
}

.action-button svg {
  width: 16px;
  height: 16px;
}

.primary-action {
  color: #fff;
  background: linear-gradient(120deg, #8064f2, #6448d8);
  box-shadow: 0 7px 18px rgba(112, 85, 232, .17);
}

.secondary-action {
  color: var(--nc-primary);
  border-color: rgba(var(--nc-primary-rgb), .2);
  background: rgba(var(--nc-primary-rgb), .07);
}

.empty-visual {
  position: relative;
  width: 112px;
  height: 92px;
  display: grid;
  place-items: center;
  margin-bottom: 3px;
}

.empty-orbit {
  position: absolute;
  inset: 3px 9px;
  border: 1px dashed rgba(var(--nc-primary-rgb), .27);
  border-radius: 50%;
  transform: rotate(-24deg);
  animation: orbitSpin 15s linear infinite;
}

.empty-book {
  width: 59px;
  height: 63px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(var(--nc-primary-rgb), .18);
  border-radius: 17px;
  color: var(--nc-primary);
  background: linear-gradient(145deg, rgba(var(--nc-primary-rgb), .13), rgba(57, 200, 208, .055));
  box-shadow: 0 10px 28px rgba(var(--nc-primary-rgb), .08);
  transform: rotate(-6deg);
}

.empty-book svg {
  width: 31px;
  height: 31px;
  stroke-width: 1.5;
}

.empty-spark {
  position: absolute;
  color: var(--nc-primary);
}

.spark-a {
  top: 4px;
  right: 7px;
  font-size: 20px;
}

.spark-b {
  bottom: 4px;
  left: 8px;
  color: #38bdbf;
  font-size: 23px;
}

.empty-kicker {
  color: var(--nc-primary);
  font-size: 8px;
  font-weight: 950;
  letter-spacing: 2px;
  direction: ltr;
}

.empty-card > h3 {
  margin: 0;
  color: var(--nc-text);
  font-size: 17px;
  font-weight: 950;
}

.empty-card > p {
  max-width: 430px;
}

.empty-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

/* Toast */
.toast-message {
  position: fixed;
  z-index: 1000;
  right: 50%;
  bottom: 94px;
  max-width: min(90vw, 430px);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 13px 17px;
  border: 1px solid rgba(255, 255, 255, .09);
  border-radius: 13px;
  color: #f8f8ff;
  background: #201d39;
  box-shadow: 0 15px 45px rgba(0, 0, 0, .23);
  font-size: 11px;
  line-height: 1.8;
  text-align: right;
  transform: translateX(50%);
  overflow-wrap: anywhere;
}

.toast-indicator {
  background: #47d8ac;
  box-shadow: 0 0 0 4px rgba(71, 216, 172, .12);
}

.toast-enter-active,
.toast-leave-active {
  transition: opacity .25s ease, transform .3s var(--nc-ease);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(50%, 12px);
}

/* Animations */
@keyframes enterUp {
  from { opacity: 0; transform: translateY(13px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(12px) scale(.99); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes ambientDrift {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to { transform: translate3d(-22px, 35px, 0) scale(1.12); }
}

@keyframes floatBook {
  0%, 100% { translate: 0 0; }
  50% { translate: 0 -9px; }
}

@keyframes starPulse {
  0%, 100% { opacity: .6; scale: 1; }
  50% { opacity: 1; scale: 1.15; }
}

@keyframes loadingPulse {
  from { opacity: .25; transform: translateY(0); }
  to { opacity: 1; transform: translateY(-4px); }
}

@keyframes orbitSpin {
  to { transform: rotate(336deg); }
}

/* Responsive */
@media (min-width: 1500px) {
  .notes-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 1100px) {
  .notes-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .command-strip {
    align-items: flex-start;
    flex-direction: column;
  }

  .quick-filters {
    width: 100%;
  }
}

@media (max-width: 700px) {
  .notes-center {
    padding: 19px 13px 115px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 14px;
    margin-bottom: 20px;
  }

  .header-brand {
    align-items: flex-start;
    gap: 11px;
  }

  .brand-icon {
    width: 43px;
    height: 43px;
    border-radius: 13px;
  }

  .brand-icon svg {
    width: 21px;
    height: 21px;
  }

  .page-kicker {
    font-size: 7px;
    letter-spacing: 1.2px;
  }

  .header-brand h1 {
    margin-top: 4px;
    font-size: 22px;
  }

  .header-brand p {
    font-size: 10px;
  }

  .header-actions {
    width: 100%;
  }

  .header-button {
    min-height: 40px;
  }

  .refresh-button {
    flex: 1;
  }

  .create-button {
    flex: 1.15;
  }

  .learning-hero {
    min-height: 0;
    padding: 24px 19px;
    border-radius: 21px;
  }

  .hero-content {
    max-width: 100%;
  }

  .hero-content h2 {
    max-width: 420px;
    margin-top: 17px;
    font-size: clamp(23px, 6vw, 31px);
    line-height: 1.65;
  }

  .hero-content > p {
    max-width: 100%;
    font-size: 10px;
  }

  .hero-visual {
    position: absolute;
    left: -55px;
    top: 4px;
    width: 170px;
    height: 160px;
    opacity: .16;
    pointer-events: none;
  }

  .visual-label {
    display: none;
  }

  .hero-pills {
    gap: 6px;
    margin-top: 15px;
  }

  .hero-pills > span {
    font-size: 8px;
  }

  .stats-grid {
    gap: 9px;
    margin-bottom: 21px;
  }

  .stat-card {
    min-height: 117px;
    padding: 12px;
    border-radius: 16px;
  }

  .stat-icon {
    width: 29px;
    height: 29px;
    border-radius: 9px;
  }

  .stat-icon svg {
    width: 15px;
    height: 15px;
  }

  .stat-label {
    font-size: 9px;
  }

  .stat-value {
    margin: 10px 0 4px;
    font-size: 24px;
  }

  .stat-foot {
    font-size: 8px;
  }

  .command-strip {
    gap: 13px;
    padding: 13px;
    margin-bottom: 25px;
    border-radius: 16px;
  }

  .command-heading small {
    font-size: 8px;
  }

  .quick-filters {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 6px;
  }

  .quick-filter {
    min-width: 0;
    justify-content: flex-start;
    padding: 0 8px;
  }

  .quick-filter > span {
    flex: 1;
    font-size: 9px;
  }

  .toolbar-heading h2 {
    font-size: 17px;
  }

  .toolbar-controls {
    gap: 7px;
  }

  .search-field {
    flex-basis: 100%;
  }

  .subject-select-wrap {
    flex: 1;
  }

  .reset-button {
    flex-shrink: 0;
  }

  .notes-grid {
    gap: 12px;
  }

  .note-card {
    border-radius: 19px;
  }

  .note-cover {
    min-height: 145px;
  }

  .note-card-body {
    padding: 13px;
  }

  .note-heading h3 {
    font-size: 13px;
  }

  .start-button {
    min-height: 39px;
    padding: 0 10px;
    font-size: 9px;
  }

  .card-icon-button {
    width: 35px;
    height: 35px;
  }

  .state-card {
    min-height: 260px;
    padding: 27px 17px;
    border-radius: 19px;
  }

  .state-card > strong {
    font-size: 12px;
  }

  .state-card > p {
    font-size: 9px;
  }
}

@media (max-width: 390px) {
  .notes-center {
    padding-right: 10px;
    padding-left: 10px;
  }

  .header-brand h1 {
    font-size: 20px;
  }

  .hero-content h2 {
    font-size: 22px;
    letter-spacing: -.7px;
  }

  .stats-grid {
    gap: 7px;
  }

  .stat-card {
    padding: 10px;
  }

  .stat-top {
    gap: 6px;
  }

  .stat-label {
    font-size: 8px;
  }

  .stat-value {
    font-size: 22px;
  }

  .quick-filter {
    gap: 5px;
    padding: 0 7px;
  }

  .quick-filter > span {
    font-size: 8px;
  }

  .quick-filter > small {
    min-width: 17px;
    height: 17px;
  }

  .note-cover {
    margin-right: 10px;
    margin-left: 10px;
    padding: 13px;
  }

  .card-top {
    padding: 12px 11px 10px;
  }

  .note-card-body {
    padding: 11px;
  }

  .card-footer {
    gap: 5px;
  }

  .card-icon-button {
    width: 32px;
    height: 35px;
  }
}

@media (hover: none) {
  .note-card:hover,
  .stat-card:hover,
  .header-button:hover,
  .quick-filter:hover,
  .start-button:hover {
    transform: none;
  }

  .note-card:hover {
    box-shadow: var(--nc-shadow);
  }
}

@media (prefers-reduced-motion: reduce) {
  .notes-center *,
  .notes-center *::before,
  .notes-center *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: .01ms !important;
  }
}
</style>
