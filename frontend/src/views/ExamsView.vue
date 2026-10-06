<template>
  <div class="exams-page-wrapper" dir="rtl">
    <section
      class="exams-page"
      :class="{ 'is-dark': isDark }"
    >
      <!-- Ambient visual layer -->
      <div class="aurora-field" aria-hidden="true">
        <span class="aurora-orb orb-one"></span>
        <span class="aurora-orb orb-two"></span>
        <span class="aurora-orb orb-three"></span>
        <span class="aurora-orb orb-four"></span>
        <span class="aurora-grid"></span>
        <span class="aurora-noise"></span>
      </div>

      <!-- Floating command button -->
      <button
        class="command-fab"
        type="button"
        title="فرمان‌های سریع"
        aria-label="باز کردن فرمان‌های سریع"
        @click="showCommandPalette = true"
      >
        <span class="fab-ring"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M12 4v16M4 12h16"/>
          <circle cx="12" cy="12" r="8"/>
        </svg>
        <kbd>⌘K</kbd>
      </button>

      <!-- =========================
           HERO
      ========================== -->
      <header class="page-header">
        <div class="hero-scanline" aria-hidden="true"></div>

        <div class="header-main">
          <div class="header-icon-shell">
            <div class="header-icon">
              <span class="icon-glow"></span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 4.5A2.5 2.5 0 0 1 7.5 2H20v17H7.5A2.5 2.5 0 0 0 5 21.5v-17Z"/>
                <path d="M5 4.5V21.5"/>
                <path d="M9 7h7"/>
                <path d="M9 11h7"/>
                <path d="M9 15h4"/>
              </svg>
            </div>
            <span class="orbit-dot orbit-dot-one"></span>
            <span class="orbit-dot orbit-dot-two"></span>
          </div>

          <div class="header-copy">
            <div class="hero-eyebrow">
              <span class="live-dot"></span>
              <span>مرکز ارزیابی هوشمند</span>
              <b>۲۴/۷</b>
            </div>

            <h1>
              آزمون‌های
              <span class="gradient-word">دوپامین</span>
            </h1>

            <p>
              یک فضای مدرن برای پیدا کردن آزمون مناسب، سنجش آمادگی
              و دنبال کردن مسیر پیشرفت تحصیلی تو.
            </p>

            <div class="hero-meta">
              <span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="m5 12 4 4L19 6"/>
                </svg>
                {{ toPersianNumber(exams.length) }} آزمون ثبت شده
              </span>
              <span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="9"/>
                  <path d="M12 7v5l3 2"/>
                </svg>
                بروزرسانی زنده وضعیت
              </span>
            </div>
          </div>
        </div>

        <div class="header-actions">
          <button
            type="button"
            class="refresh-button"
            :class="{ spinning: loading }"
            :disabled="loading"
            @click="loadExams"
          >
            <span class="refresh-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M20 11a8.1 8.1 0 0 0-14.7-4.7L4 8"/>
                <path d="M4 4v4h4"/>
                <path d="M4 13a8.1 8.1 0 0 0 14.7 4.7L20 16"/>
                <path d="M20 20v-4h-4"/>
              </svg>
            </span>
            <span>{{ loading ? 'در حال بروزرسانی' : 'بروزرسانی' }}</span>
          </button>

          <button
            type="button"
            class="help-button"
            aria-label="راهنمای میانبرها"
            @click="showKeyboardHelp = true"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="9"/>
              <path d="M9.7 9a2.3 2.3 0 1 1 3.9 1.6c-1.1.8-1.6 1.2-1.6 2.4"/>
              <path d="M12 16.5h.01"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- =========================
           COMMAND STRIP
      ========================== -->
      <section class="command-strip">
        <div class="command-strip-left">
          <span class="command-kicker">دسترسی سریع</span>

          <button
            v-for="filter in quickFilters"
            :key="filter.value"
            type="button"
            class="quick-filter"
            :class="{ active: activeQuickFilter === filter.value }"
            @click="setQuickFilter(filter.value)"
          >
            <span class="quick-filter-icon">
              <svg v-if="filter.icon === 'spark'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m12 2 1.7 6.3L20 10l-6.3 1.7L12 18l-1.7-6.3L4 10l6.3-1.7L12 2Z"/>
                <path d="m19 16 .7 2.3L22 19l-2.3.7L19 22l-.7-2.3L16 19l2.3-.7L19 16Z"/>
              </svg>
              <svg v-else-if="filter.icon === 'play'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m9 6 9 6-9 6V6Z"/>
              </svg>
              <svg v-else-if="filter.icon === 'clock'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/>
                <path d="M12 7v5l3 2"/>
              </svg>
              <svg v-else-if="filter.icon === 'heart'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m12 20-1.5-1.35C5.4 14.1 2 11.05 2 7.25A4.25 4.25 0 0 1 6.25 3c1.8 0 3.5.85 4.55 2.2A5.58 5.58 0 0 1 15.35 3 4.25 4.25 0 0 1 19.6 7.25c0 3.8-3.4 6.85-8.5 11.4L12 20Z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m5 12 4 4L19 6"/>
              </svg>
            </span>
            <span>{{ filter.label }}</span>
          </button>
        </div>

        <button
          type="button"
          class="shortcut-hint"
          @click="showCommandPalette = true"
        >
          <kbd>Ctrl</kbd>
          <span>+</span>
          <kbd>K</kbd>
          <span>فرمان‌های سریع</span>
        </button>
      </section>

      <!-- =========================
           STATS
      ========================== -->
      <section class="stats-grid">
        <div class="stat-card stat-total">
          <div class="stat-card-glow"></div>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="5" y="3" width="14" height="18" rx="2"/>
              <path d="M8 7h8M8 11h8M8 15h5"/>
            </svg>
          </div>
          <div class="stat-copy">
            <span>کل آزمون‌ها</span>
            <strong>{{ toPersianNumber(exams.length) }}</strong>
            <small>در مرکز آزمون</small>
          </div>
          <div class="stat-mini-chart">
            <i></i><i></i><i></i><i></i><i></i><i></i><i></i>
          </div>
        </div>

        <div class="stat-card stat-upcoming">
          <div class="stat-card-glow"></div>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="9"/>
              <path d="M12 7v5l3 2"/>
            </svg>
          </div>
          <div class="stat-copy">
            <span>آزمون‌های پیش‌رو</span>
            <strong>{{ toPersianNumber(upcomingCount) }}</strong>
            <small v-if="upcomingSoonest">
              {{ getRelativeTime(upcomingSoonest.start_at) }}
            </small>
            <small v-else>فعلاً آزمونی نزدیک نیست</small>
          </div>
          <span class="stat-pulse"></span>
        </div>

        <div class="stat-card stat-running">
          <div class="stat-card-glow"></div>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 12h14"/>
              <path d="m13 6 6 6-6 6"/>
            </svg>
          </div>
          <div class="stat-copy">
            <span>همین حالا</span>
            <strong>{{ toPersianNumber(runningCount) }}</strong>
            <small>{{ toPersianNumber(availableCount) }} آزمون قابل شرکت</small>
          </div>
          <span class="live-indicator"><i></i> زنده</span>
        </div>

        <div class="stat-card stat-completed">
          <div class="stat-card-glow"></div>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 4h16v16H4z"/>
              <path d="m8 12 3 3 5-6"/>
            </svg>
          </div>
          <div class="stat-copy">
            <span>شرکت کرده‌اید</span>
            <strong>{{ toPersianNumber(attemptedCount) }}</strong>
            <small>{{ toPersianNumber(completionRate) }}٪ پوشش آزمون‌ها</small>
          </div>
          <div class="completion-ring" :style="{ '--value': completionRate + '%' }">
            <span>{{ toPersianNumber(completionRate) }}٪</span>
          </div>
        </div>
      </section>

      <!-- =========================
           SEARCH / DISCOVERY
      ========================== -->
      <section
        v-if="!loading && !errorMessage"
        class="discovery-panel"
      >
        <div class="discovery-top">
          <div class="discovery-title">
            <span class="section-overline">جست‌وجوی سریع</span>
            <h2>آزمون مناسب خودت را پیدا کن</h2>
            <p>عنوان، درس، برگزارکننده یا هر بخشی از اطلاعات آزمون را جست‌وجو کن.</p>
          </div>

          <div class="view-switcher">
            <button
              type="button"
              :class="{ active: viewMode === 'grid' }"
              aria-label="نمای شبکه‌ای"
              @click="viewMode = 'grid'"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="4" y="4" width="6" height="6" rx="1"/>
                <rect x="14" y="4" width="6" height="6" rx="1"/>
                <rect x="4" y="14" width="6" height="6" rx="1"/>
                <rect x="14" y="14" width="6" height="6" rx="1"/>
              </svg>
            </button>
            <button
              type="button"
              :class="{ active: viewMode === 'list' }"
              aria-label="نمای فهرستی"
              @click="viewMode = 'list'"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M8 6h12M8 12h12M8 18h12"/>
                <circle cx="4" cy="6" r="1"/>
                <circle cx="4" cy="12" r="1"/>
                <circle cx="4" cy="18" r="1"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="discovery-controls">
          <label class="search-box">
            <span class="search-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="7"/>
                <path d="m20 20-4-4"/>
              </svg>
            </span>
            <input
              v-model="searchQuery"
              class="exam-search-input"
              type="search"
              placeholder="مثلاً: ریاضی، قلمچی، آزمون جامع..."
              autocomplete="off"
            />
            <button
              v-if="searchQuery"
              type="button"
              class="clear-search"
              aria-label="پاک کردن جست‌وجو"
              @click="clearSearch"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m7 7 10 10M17 7 7 17"/>
              </svg>
            </button>
            <kbd>/</kbd>
          </label>

          <div class="sort-box">
            <span class="sort-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M8 6h12M8 12h8M8 18h4"/>
                <path d="m4 4 2 2 2-2M4 10l2 2 2-2M4 16l2 2 2-2"/>
              </svg>
            </span>
            <select v-model="sortMode" aria-label="مرتب‌سازی">
              <option
                v-for="option in sortOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <button
            type="button"
            class="filter-toggle"
            :class="{ active: showFilters }"
            @click="showFilters = !showFilters"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 6h16M7 12h10M10 18h4"/>
              <circle cx="7" cy="6" r="1.5"/>
              <circle cx="17" cy="12" r="1.5"/>
              <circle cx="12" cy="18" r="1.5"/>
            </svg>
            <span>فیلتر پیشرفته</span>
            <i :class="{ on: showFilters }"></i>
          </button>
        </div>

        <Transition name="filter-expand">
          <div v-if="showFilters" class="advanced-filters">
            <div class="advanced-filter-group">
              <span>وضعیت</span>
              <div class="filter-pills">
                <button
                  type="button"
                  :class="{ active: selectedStatus === 'all' }"
                  @click="selectedStatus = 'all'"
                >همه</button>
                <button
                  type="button"
                  :class="{ active: selectedStatus === 'not_started' }"
                  @click="selectedStatus = 'not_started'"
                >پیش‌رو</button>
                <button
                  type="button"
                  :class="{ active: selectedStatus === 'running' }"
                  @click="selectedStatus = 'running'"
                >در حال برگزاری</button>
                <button
                  type="button"
                  :class="{ active: selectedStatus === 'ended' }"
                  @click="selectedStatus = 'ended'"
                >پایان‌یافته</button>
              </div>
            </div>

            <label class="availability-toggle">
              <span>
                <strong>فقط آزمون‌های قابل شرکت</strong>
                <small>آزمون‌هایی که همین حالا امکان شروع دارند</small>
              </span>
              <input v-model="onlyAvailable" type="checkbox" />
              <i></i>
            </label>

            <button type="button" class="reset-filters" @click="resetFilters">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 12a8 8 0 1 0 2.3-5.6"/>
                <path d="M4 4v5h5"/>
              </svg>
              پاک کردن فیلترها
            </button>
          </div>
        </Transition>
      </section>

      <!-- =========================
           CATEGORIES
      ========================== -->
      <section
        v-if="!loading && !errorMessage"
        class="filters-section"
      >
        <div class="section-heading">
          <div>
            <span>دسته‌بندی</span>
            <strong>برگزارکننده آزمون</strong>
          </div>
          <span class="result-count">
            {{ toPersianNumber(visibleExamCount) }} نتیجه
          </span>
        </div>

        <div class="category-tabs">
          <button
            type="button"
            class="category-tab all-tab"
            :class="{ active: selectedCategory === 'all' }"
            @click="selectedCategory = 'all'"
          >
            <span class="tab-symbol">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </span>
            <span>همه آزمون‌ها</span>
            <small>{{ toPersianNumber(exams.length) }}</small>
          </button>

          <button
            v-for="category in categories"
            :key="category.value"
            type="button"
            class="category-tab"
            :class="[
              getCategoryTabClass(category.value),
              { active: selectedCategory === category.value }
            ]"
            @click="selectedCategory = category.value"
          >
            <span class="tab-symbol">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 5h16v14H4z"/>
                <path d="M8 9h8M8 13h5"/>
              </svg>
            </span>
            <span>{{ category.label }}</span>
            <small>{{ toPersianNumber(category.count) }}</small>
          </button>
        </div>
      </section>

      <!-- =========================
           RESULT SUMMARY
      ========================== -->
      <div
        v-if="!loading && !errorMessage && filteredExams.length"
        class="results-toolbar"
      >
        <div>
          <span class="results-dot"></span>
          <strong>{{ toPersianNumber(filteredExams.length) }} آزمون</strong>
          <span>مطابق انتخاب‌های تو</span>
        </div>

        <div class="results-toolbar-actions">
          <span v-if="normalizedSearch">
            جست‌وجو: «{{ searchQuery }}»
          </span>
          <button
            v-if="normalizedSearch || selectedCategory !== 'all' || selectedStatus !== 'all' || onlyAvailable"
            type="button"
            @click="resetFilters"
          >
            پاک کردن
          </button>
        </div>
      </div>

      <!-- =========================
           LOADING
      ========================== -->
      <div v-if="loading" class="state-card loading-state">
        <div class="loading-orbit">
          <span></span>
          <span></span>
          <span></span>
          <div>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>
              <path d="m5.6 5.6 2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>
            </svg>
          </div>
        </div>
        <div class="state-content">
          <span class="state-kicker">SYNCING</span>
          <h3>در حال آماده‌سازی مرکز آزمون</h3>
          <p>آخرین اطلاعات آزمون‌ها در حال دریافت و مرتب‌سازی است...</p>
          <div class="loading-lines">
            <i></i><i></i><i></i>
          </div>
        </div>
      </div>

      <!-- =========================
           ERROR
      ========================== -->
      <div v-else-if="errorMessage" class="state-card error-state">
        <div class="state-visual error">
          <span></span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 3 2.8 19a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L12 3Z"/>
            <path d="M12 9v4M12 17h.01"/>
          </svg>
        </div>
        <div class="state-content">
          <span class="state-kicker">CONNECTION ERROR</span>
          <h3>دریافت آزمون‌ها ناموفق بود</h3>
          <p>{{ errorMessage }}</p>
          <button type="button" class="state-button" @click="loadExams">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 11a8 8 0 0 0-14.7-4.7L4 8"/>
              <path d="M4 4v4h4"/>
              <path d="M4 13a8 8 0 0 0 14.7 4.7L20 16"/>
              <path d="M20 20v-4h-4"/>
            </svg>
            تلاش دوباره
          </button>
        </div>
      </div>

      <!-- =========================
           EMPTY
      ========================== -->
      <div
        v-else-if="filteredExams.length === 0"
        class="state-card empty-state"
      >
        <div class="empty-illustration">
          <span class="empty-orbit"></span>
          <div class="empty-paper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="5" y="3" width="14" height="18" rx="2"/>
              <path d="M8 8h8M8 12h8M8 16h5"/>
            </svg>
          </div>
          <span class="empty-spark spark-a">✦</span>
          <span class="empty-spark spark-b">✧</span>
        </div>
        <div class="state-content">
          <span class="state-kicker">NO MATCHES</span>
          <h3>چیزی با این مشخصات پیدا نشد</h3>
          <p>فیلترها یا عبارت جست‌وجو را تغییر بده تا آزمون‌های بیشتری ببینی.</p>
          <button type="button" class="state-button secondary" @click="resetFilters">
            نمایش همه آزمون‌ها
          </button>
        </div>
      </div>

      <!-- =========================
           EXAM GRID
      ========================== -->
      <section
        v-else
        class="exam-grid"
        :class="{
          'list-view': viewMode === 'list'
        }"
      >
        <article
          v-for="exam in filteredExams"
          :key="exam.id"
          :class="[
            'exam-card',
            'accent-' + getExamAccent(exam),
            {
              'is-running': getExamState(exam) === 'running',
              'is-ended': getExamState(exam) === 'ended',
              'is-favorite': isFavorite(exam),
              'is-expanded': isExpanded(exam),
              'is-hovered': hoveredExamId === exam.id
            }
          ]"
          :style="getCardStyle(exam)"
          tabindex="0"
          @mouseenter="hoveredExamId = exam.id"
          @mouseleave="hoveredExamId = null"
          @keydown="handleCardKeydown($event, exam)"
        >
          <div class="card-ambient"></div>
          <div class="card-noise"></div>
          <div class="card-progress-line"></div>

          <!-- Card header -->
          <div class="card-top">
            <div class="provider-badge" :class="getCategoryClass(exam.category)">
              <span></span>
              {{ getCategoryLabel(exam) }}
            </div>

            <div class="card-top-actions">
              <button
                type="button"
                class="favorite-button"
                :class="{ active: isFavorite(exam) }"
                :aria-label="isFavorite(exam) ? 'حذف از نشان‌شده‌ها' : 'نشان کردن آزمون'"
                @click.stop="toggleFavorite(exam)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="m12 20-1.5-1.35C5.4 14.1 2 11.05 2 7.25A4.25 4.25 0 0 1 6.25 3c1.8 0 3.5.85 4.55 2.2A5.58 5.58 0 0 1 15.35 3 4.25 4.25 0 0 1 19.6 7.25c0 3.8-3.4 6.85-8.5 11.4L12 20Z"/>
                </svg>
              </button>

              <div class="status-badge" :class="getStatusClass(exam)">
                <i></i>
                {{ getStatusLabel(exam) }}
              </div>
            </div>
          </div>

          <!-- Card title -->
          <div class="exam-heading">
            <h2>{{ exam.title }}</h2>
            <p v-if="exam.description">{{ exam.description }}</p>
          </div>

          <!-- Countdown -->
          <div
            class="exam-live-panel"
            :class="`state-${getExamState(exam)}`"
          >
            <div class="live-panel-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/>
                <path d="M12 7v5l3 2"/>
              </svg>
            </div>
            <div class="live-panel-copy">
              <span>
                {{
                  getExamState(exam) === 'running'
                    ? 'زمان باقی‌مانده'
                    : getExamState(exam) === 'not_started'
                      ? 'تا شروع آزمون'
                      : 'وضعیت زمانی'
                }}
              </span>
              <strong>{{ getTimeRemaining(exam) }}</strong>
            </div>
            <div
              v-if="getExamState(exam) !== 'ended'"
              class="mini-progress"
              :style="{ '--progress': getProgressPercent(exam) + '%' }"
            >
              <span></span>
            </div>
          </div>

          <!-- Date -->
          <div class="exam-date">
            <div class="date-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="17" rx="2"/>
                <path d="M8 2v4M16 2v4M3 10h18"/>
              </svg>
            </div>
            <div class="date-content">
              <span>تاریخ و زمان برگزاری</span>
              <strong>{{ formatFullDate(exam.start_at) }}</strong>
              <div class="date-time">
                <span>{{ formatTime(exam.start_at) }}</span>
                <b>←</b>
                <span>{{ formatTime(exam.end_at) }}</span>
              </div>
            </div>
            <div class="date-relative">
              {{ getRelativeTime(exam.start_at) }}
            </div>
          </div>

          <!-- Information grid -->
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
                <strong>{{ formatDuration(exam.duration_minutes) }}</strong>
              </div>
            </div>

            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M6 4h12M6 9h12M6 14h7M6 19h5"/>
                </svg>
              </span>
              <div>
                <small>تعداد سؤال</small>
                <strong>{{ toPersianNumber(exam.total_questions) }} سؤال</strong>
              </div>
            </div>

            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <rect x="4" y="3" width="16" height="18" rx="2"/>
                  <path d="M8 8h8M8 12h8M8 16h4"/>
                </svg>
              </span>
              <div>
                <small>دفترچه‌ها</small>
                <strong>
                  {{ toPersianNumber(exam.booklet_count || exam.booklets?.length || 0) }}
                  دفترچه
                </strong>
              </div>
            </div>

            <div class="exam-info">
              <span class="info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="m5 12 4 4L19 6"/>
                </svg>
              </span>
              <div>
                <small>وضعیت</small>
                <strong>{{ getStatusLabel(exam) }}</strong>
              </div>
            </div>
          </div>

          <!-- Booklets -->
          <div v-if="exam.booklets?.length" class="booklets">
            <div class="booklets-header">
              <div>
                <span>ساختار آزمون</span>
                <strong>دفترچه‌ها و دروس</strong>
              </div>
              <small>
                {{ toPersianNumber(exam.booklets.length) }} دفترچه
              </small>
            </div>

            <div class="booklets-list">
              <div
                v-for="booklet in sortedBooklets(exam.booklets)"
                :key="booklet.id"
                class="booklet"
              >
                <div class="booklet-number">{{ toPersianNumber(booklet.order) }}</div>
                <div class="booklet-main">
                  <div class="booklet-title">
                    <strong>{{ booklet.title || `دفترچه ${booklet.order}` }}</strong>
                    <span>{{ booklet.subject }}</span>
                  </div>
                  <small>
                    سؤال {{ toPersianNumber(booklet.start_question) }}
                    تا {{ toPersianNumber(booklet.end_question) }}
                    <b>•</b>
                    {{ toPersianNumber(booklet.question_count) }} سؤال
                  </small>
                </div>
                <svg class="booklet-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="m9 18 6-6-6-6"/>
                </svg>
              </div>
            </div>
          </div>

          <div v-else class="no-booklets">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 5h16v14H4zM8 9h8M8 13h5"/>
            </svg>
            <span>اطلاعات دفترچه‌های این آزمون ثبت نشده است.</span>
          </div>

          <!-- Active / result -->
          <Transition name="soft">
            <div v-if="isInProgress(exam)" class="attempt-banner">
              <div class="attempt-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="9"/>
                  <path d="M12 7v5l3 2"/>
                </svg>
              </div>
              <div>
                <strong>آزمون نیمه‌تمام داری</strong>
                <span>از همان‌جایی که متوقف شدی ادامه بده.</span>
              </div>
              <b>ادامه</b>
            </div>
          </Transition>

          <Transition name="soft">
            <div v-if="hasResult(exam)" class="result-banner">
              <div class="result-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M4 19V5M4 19h16M7 15l3-4 3 2 5-7"/>
                </svg>
              </div>
              <div>
                <strong>کارنامه آماده است</strong>
                <span>نتیجه و عملکرد خود را مشاهده کن.</span>
              </div>
              <span class="result-arrow">↗</span>
            </div>
          </Transition>

          <!-- Expand -->
          <Transition name="expand">
            <div v-if="isExpanded(exam)" class="card-expanded-panel">
              <div>
                <span>شناسه آزمون</span>
                <strong>#{{ toPersianNumber(exam.id) }}</strong>
              </div>
              <div>
                <span>شروع نسبی</span>
                <strong>{{ getRelativeTime(exam.start_at) }}</strong>
              </div>
              <div>
                <span>نوع دسترسی</span>
                <strong>{{ canStartExam(exam) ? 'قابل شرکت' : 'محدود' }}</strong>
              </div>
            </div>
          </Transition>

          <!-- Footer -->
<footer class="exam-footer">
  <!-- وضعیت آزمون -->
  <div class="footer-message">
    <span class="footer-status-dot"></span>
    <span class="footer-message-text">
      {{ getFooterText(exam) }}
    </span>
  </div>

  <!-- عملیات -->
  <div class="footer-actions">

    <!-- جزئیات -->
    <button
      type="button"
      class="footer-action details-button"
      @click.stop="openExamDetails(exam)"
    >
      <span class="action-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="9"/>
          <path d="M12 11v5M12 8h.01"/>
        </svg>
      </span>

      <span class="action-label">جزئیات</span>
    </button>

    <!-- کارنامه -->
    <button
      v-if="hasResult(exam)"
      type="button"
      class="footer-action result-button"
      @click.stop="viewResult(exam)"
    >
      <span class="action-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M4 19V5M4 19h16M7 15l3-4 3 2 5-7"/>
        </svg>
      </span>

      <span class="action-label">مشاهده کارنامه</span>
    </button>

    <!-- شروع / ادامه -->
    <button
      v-if="canStartExam(exam)"
      type="button"
      class="start-button"
      @click.stop="startExam(exam)"
    >
      <span style="
    display: flex;
    direction: ltr;
    align-items: center;
" class="start-button-content">
        <span>
          {{ isInProgress(exam) ? 'ادامه آزمون' : 'شروع آزمون' }}
        </span>

        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="m9 18 6-6-6-6"/>
        </svg>
      </span>
    </button>

    <!-- وضعیت غیرفعال -->
    <button
      v-else
      type="button"
      class="disabled-button"
      disabled
    >
      <span>{{ getActionText(exam) }}</span>
    </button>

    <!-- Expand -->
    <button
      type="button"
      class="expand-button"
      :class="{ 'is-expanded': isExpanded(exam) }"
      :aria-label="
        isExpanded(exam)
          ? 'بستن اطلاعات بیشتر'
          : 'اطلاعات بیشتر'
      "
      @click.stop="toggleExpanded(exam)"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path
          :d="
            isExpanded(exam)
              ? 'm6 15 6-6 6 6'
              : 'm6 9 6 6 6-6'
          "
        />
      </svg>
    </button>

  </div>
</footer>
          <span class="card-corner corner-one"></span>
          <span class="card-corner corner-two"></span>
        </article>
      </section>

      <!-- =========================
           FOOT NOTE
      ========================== -->
      <section
        v-if="!loading && !errorMessage && exams.length"
        class="bottom-insight"
      >
        <div class="insight-orb">
          <span></span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M9 18h6M10 21h4"/>
            <path d="M8.2 14.5A7 7 0 1 1 16 14.2c-.8.7-1.2 1.5-1.5 2.8h-5c-.3-1.2-.7-2-1.3-2.5Z"/>
          </svg>
        </div>
        <div>
          <span>نکته هوشمند</span>
          <strong>
            آزمون‌هایی که به زمان شروع نزدیک‌ترند را در اولویت قرار بده.
          </strong>
        </div>
        <button type="button" @click="sortMode = 'soonest'">
          مرتب‌سازی بر اساس نزدیک‌ترین
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="m9 18 6-6-6-6"/>
          </svg>
        </button>
      </section>

      <!-- =========================
           SCROLL TOP
      ========================== -->
      <Transition name="float">
        <button
          v-if="showScrollTop"
          type="button"
          class="scroll-top"
          aria-label="بازگشت به بالا"
          @click="scrollToTop"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="m6 15 6-6 6 6"/>
          </svg>
        </button>
      </Transition>

      <!-- =========================
           EXAM DETAIL MODAL
      ========================== -->
      <Transition name="modal">
        <div
          v-if="selectedExam"
          class="modal-overlay"
          @click.self="closeExamDetails"
        >
          <div class="exam-modal">
            <div class="modal-backdrop-art" aria-hidden="true">
              <span></span><span></span><span></span>
            </div>

            <button
              type="button"
              class="modal-close"
              aria-label="بستن"
              @click="closeExamDetails"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m6 6 12 12M18 6 6 18"/>
              </svg>
            </button>

            <div class="modal-top">
              <div class="provider-badge" :class="getCategoryClass(selectedExam.category)">
                <span></span>
                {{ getCategoryLabel(selectedExam) }}
              </div>
              <div class="status-badge" :class="getStatusClass(selectedExam)">
                <i></i>
                {{ getStatusLabel(selectedExam) }}
              </div>
            </div>

            <div class="modal-hero-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 4.5A2.5 2.5 0 0 1 7.5 2H20v17H7.5A2.5 2.5 0 0 0 5 21.5v-17Z"/>
                <path d="M9 7h7M9 11h7M9 15h4"/>
              </svg>
            </div>

            <div class="modal-heading">
              <span>جزئیات آزمون</span>
              <h2>{{ selectedExam.title }}</h2>
              <p v-if="selectedExam.description" class="modal-description">
                {{ selectedExam.description }}
              </p>
            </div>

            <div class="modal-countdown">
              <div>
                <span>وضعیت زمانی</span>
                <strong>{{ getTimeRemaining(selectedExam) }}</strong>
              </div>
              <div class="modal-countdown-progress">
                <span :style="{ width: getProgressPercent(selectedExam) + '%' }"></span>
              </div>
            </div>

            <div class="modal-date-grid">
              <div>
                <span>شروع آزمون</span>
                <strong>{{ formatFullDate(selectedExam.start_at) }}</strong>
                <small>{{ formatTime(selectedExam.start_at) }}</small>
              </div>
              <div>
                <span>پایان آزمون</span>
                <strong>{{ formatFullDate(selectedExam.end_at) }}</strong>
                <small>{{ formatTime(selectedExam.end_at) }}</small>
              </div>
            </div>

            <div class="modal-stats">
              <div>
                <span>مدت آزمون</span>
                <strong>{{ formatDuration(selectedExam.duration_minutes) }}</strong>
              </div>
              <div>
                <span>تعداد سؤال</span>
                <strong>{{ toPersianNumber(selectedExam.total_questions) }}</strong>
              </div>
              <div>
                <span>دفترچه</span>
                <strong>{{ toPersianNumber(selectedExam.booklets?.length || selectedExam.booklet_count || 0) }}</strong>
              </div>
            </div>

            <div v-if="selectedExam.booklets?.length" class="modal-booklets">
              <div class="modal-section-header">
                <div>
                  <span>ساختار آزمون</span>
                  <strong>دفترچه‌ها و دروس</strong>
                </div>
                <span>{{ toPersianNumber(selectedExam.booklets.length) }} دفترچه</span>
              </div>

              <div
                v-for="booklet in sortedBooklets(selectedExam.booklets)"
                :key="booklet.id"
                class="modal-booklet"
              >
                <div class="modal-booklet-number">{{ toPersianNumber(booklet.order) }}</div>
                <section>
                  <strong>{{ booklet.title || `دفترچه ${booklet.order}` }}</strong>
                  <span>{{ booklet.subject }}</span>
                  <small>
                    {{ toPersianNumber(booklet.question_count) }} سؤال
                    <b>•</b>
                    {{ toPersianNumber(booklet.start_question) }}
                    تا
                    {{ toPersianNumber(booklet.end_question) }}
                  </small>
                </section>
              </div>
            </div>

            <div v-else class="modal-no-booklets">
              اطلاعات دفترچه‌های این آزمون ثبت نشده است.
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
                {{ isInProgress(selectedExam) ? 'ادامه آزمون' : 'شروع آزمون' }}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="m9 18 6-6-6-6"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- =========================
           COMMAND PALETTE
      ========================== -->
      <Transition name="command">
        <div
          v-if="showCommandPalette"
          class="command-overlay"
          @click.self="showCommandPalette = false"
        >
          <div class="command-palette">
            <div class="command-header">
              <div class="command-search-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="11" cy="11" r="7"/>
                  <path d="m20 20-4-4"/>
                </svg>
              </div>
              <div>
                <span>مرکز فرمان دوپامین</span>
                <strong>یک کار را انتخاب کن</strong>
              </div>
              <button type="button" @click="showCommandPalette = false">Esc</button>
            </div>

            <div class="command-list">
              <button type="button" @click="selectFromCommand('search')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="11" cy="11" r="7"/>
                    <path d="m20 20-4-4"/>
                  </svg>
                </span>
                <span><strong>جست‌وجوی آزمون</strong><small>پیدا کردن آزمون با عنوان یا درس</small></span>
                <kbd>/</kbd>
              </button>

              <button type="button" @click="selectFromCommand('available')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="m9 6 9 6-9 6V6Z"/>
                  </svg>
                </span>
                <span><strong>آزمون‌های قابل شرکت</strong><small>فقط آزمون‌های فعال را نشان بده</small></span>
              </button>

              <button type="button" @click="selectFromCommand('upcoming')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="9"/>
                    <path d="M12 7v5l3 2"/>
                  </svg>
                </span>
                <span><strong>آزمون‌های پیش‌رو</strong><small>نزدیک‌ترین آزمون‌ها را ببین</small></span>
              </button>

              <button type="button" @click="selectFromCommand('attempted')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="m5 12 4 4L19 6"/>
                  </svg>
                </span>
                <span><strong>آزمون‌های شرکت‌کرده</strong><small>سوابق آزمون‌های خودت</small></span>
              </button>

              <button type="button" @click="selectFromCommand('favorites')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="m12 20-1.5-1.35C5.4 14.1 2 11.05 2 7.25A4.25 4.25 0 0 1 6.25 3c1.8 0 3.5.85 4.55 2.2A5.58 5.58 0 0 1 15.35 3 4.25 4.25 0 0 1 19.6 7.25c0 3.8-3.4 6.85-8.5 11.4L12 20Z"/>
                  </svg>
                </span>
                <span><strong>آزمون‌های نشان‌شده</strong><small>{{ toPersianNumber(favoriteCount) }} آزمون ذخیره شده</small></span>
              </button>

              <button type="button" @click="selectFromCommand('refresh')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M20 11a8.1 8.1 0 0 0-14.7-4.7L4 8M4 4v4h4"/>
                    <path d="M4 13a8.1 8.1 0 0 0 14.7 4.7L20 16M20 20v-4h-4"/>
                  </svg>
                </span>
                <span><strong>بروزرسانی آزمون‌ها</strong><small>دریافت آخرین اطلاعات</small></span>
                <kbd>R</kbd>
              </button>

              <button type="button" @click="selectFromCommand('top')">
                <span class="command-list-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="m6 15 6-6 6 6"/>
                  </svg>
                </span>
                <span><strong>بازگشت به بالا</strong><small>رفتن به ابتدای صفحه</small></span>
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- =========================
           KEYBOARD HELP
      ========================== -->
      <Transition name="command">
        <div
          v-if="showKeyboardHelp"
          class="command-overlay"
          @click.self="showKeyboardHelp = false"
        >
          <div class="keyboard-modal">
            <button
              type="button"
              class="modal-close"
              @click="showKeyboardHelp = false"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m6 6 12 12M18 6 6 18"/>
              </svg>
            </button>
            <span class="state-kicker">POWER USER</span>
            <h2>میانبرهای صفحه</h2>
            <p>با چند کلید ساده سریع‌تر در مرکز آزمون حرکت کن.</p>
            <div class="shortcut-grid">
              <div><kbd>/</kbd><span>تمرکز روی جست‌وجو</span></div>
              <div><kbd>Ctrl K</kbd><span>باز کردن فرمان‌های سریع</span></div>
              <div><kbd>R</kbd><span>بروزرسانی آزمون‌ها</span></div>
              <div><kbd>Esc</kbd><span>بستن پنجره باز</span></div>
              <div><kbd>Enter</kbd><span>باز کردن جزئیات کارت</span></div>
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
   PREMIUM UI STATE
========================================================= */

const searchQuery = ref('')
const sortMode = ref('smart')
const viewMode = ref('grid')
const showFilters = ref(false)
const selectedStatus = ref('all')
const onlyAvailable = ref(false)
const favorites = ref(new Set())
const expandedCards = ref(new Set())
const activeQuickFilter = ref('all')
const hoveredExamId = ref(null)
const showScrollTop = ref(false)
const showCommandPalette = ref(false)
const showKeyboardHelp = ref(false)
const currentTime = ref(Date.now())

const sortOptions = [
  { value: 'smart', label: 'هوشمند' },
  { value: 'newest', label: 'جدیدترین' },
  { value: 'soonest', label: 'نزدیک‌ترین' },
  { value: 'questions', label: 'تعداد سؤال' },
  { value: 'duration', label: 'مدت آزمون' },
]

const quickFilters = [
  { value: 'all', label: 'همه', icon: 'spark' },
  { value: 'available', label: 'قابل شرکت', icon: 'play' },
  { value: 'upcoming', label: 'پیش‌رو', icon: 'clock' },
  { value: 'attempted', label: 'شرکت کرده‌ام', icon: 'check' },
  { value: 'favorites', label: 'نشان‌شده‌ها', icon: 'heart' },
]

const normalizedSearch = computed(() =>
  String(searchQuery.value || '').trim().toLocaleLowerCase('fa-IR')
)

const visibleExamCount = computed(() => filteredExams.value.length)

const favoriteCount = computed(() => favorites.value.size)

const completionRate = computed(() => {
  if (!exams.value.length) return 0
  return Math.round((attemptedCount.value / exams.value.length) * 100)
})

const availableCount = computed(() =>
  exams.value.filter(exam => canStartExam(exam)).length
)

const upcomingSoonest = computed(() => {
  const upcoming = exams.value
    .filter(exam => getExamState(exam) === 'not_started')
    .sort((a, b) =>
      (parseDate(a.start_at)?.getTime() || Infinity) -
      (parseDate(b.start_at)?.getTime() || Infinity)
    )
  return upcoming[0] || null
})

const filteredAndSortedExams = computed(() => {
  let list = [...exams.value]

  if (selectedCategory.value !== 'all') {
    list = list.filter(exam =>
      String(exam.category) === String(selectedCategory.value)
    )
  }

  if (selectedStatus.value !== 'all') {
    list = list.filter(exam => getExamState(exam) === selectedStatus.value)
  }

  if (onlyAvailable.value) {
    list = list.filter(exam => canStartExam(exam))
  }

  if (activeQuickFilter.value === 'available') {
    list = list.filter(exam => canStartExam(exam))
  } else if (activeQuickFilter.value === 'upcoming') {
    list = list.filter(exam => getExamState(exam) === 'not_started')
  } else if (activeQuickFilter.value === 'attempted') {
    list = list.filter(exam => hasAttempt(exam))
  } else if (activeQuickFilter.value === 'favorites') {
    list = list.filter(exam => favorites.value.has(exam.id))
  }

  if (normalizedSearch.value) {
    list = list.filter(exam => {
      const haystack = [
        exam.title,
        exam.description,
        exam.category_label,
        getCategoryLabel(exam),
        ...(Array.isArray(exam.booklets)
          ? exam.booklets.flatMap(booklet => [
              booklet.title,
              booklet.subject,
            ])
          : []),
      ]
        .filter(Boolean)
        .join(' ')
        .toLocaleLowerCase('fa-IR')

      return haystack.includes(normalizedSearch.value)
    })
  }

  return list.sort((a, b) => {
    const aTime = parseDate(a.start_at)?.getTime() || 0
    const bTime = parseDate(b.start_at)?.getTime() || 0

    if (sortMode.value === 'newest') {
      return bTime - aTime
    }

    if (sortMode.value === 'soonest') {
      const now = Date.now()
      const ad = aTime >= now ? aTime : Infinity
      const bd = bTime >= now ? bTime : Infinity
      return ad - bd
    }

    if (sortMode.value === 'questions') {
      return Number(b.total_questions || 0) - Number(a.total_questions || 0)
    }

    if (sortMode.value === 'duration') {
      return Number(b.duration_minutes || 0) - Number(a.duration_minutes || 0)
    }

    const rank = exam => {
      const state = getExamState(exam)
      if (isInProgress(exam)) return 0
      if (state === 'running') return 1
      if (state === 'not_started') return 2
      if (hasResult(exam)) return 3
      return 4
    }

    return rank(a) - rank(b) || bTime - aTime
  })
})

/* Keep the legacy computed name consumed by the page, but use the richer pipeline. */
const filteredExams = computed(() => filteredAndSortedExams.value)

function toggleFavorite(exam) {
  const next = new Set(favorites.value)
  if (next.has(exam.id)) {
    next.delete(exam.id)
  } else {
    next.add(exam.id)
  }
  favorites.value = next
  localStorage.setItem(
    'dopamine_exam_favorites',
    JSON.stringify([...next])
  )
}

function isFavorite(exam) {
  return favorites.value.has(exam.id)
}

function toggleExpanded(exam) {
  const next = new Set(expandedCards.value)
  if (next.has(exam.id)) {
    next.delete(exam.id)
  } else {
    next.add(exam.id)
  }
  expandedCards.value = next
}

function isExpanded(exam) {
  return expandedCards.value.has(exam.id)
}

function setQuickFilter(value) {
  activeQuickFilter.value = value
  if (value !== 'all') {
    showFilters.value = true
  }
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  selectedStatus.value = 'all'
  onlyAvailable.value = false
  activeQuickFilter.value = 'all'
  sortMode.value = 'smart'
}

function clearSearch() {
  searchQuery.value = ''
}

function getRelativeTime(value) {
  const date = parseDate(value)
  if (!date) return '—'

  const diff = date.getTime() - currentTime.value
  const minutes = Math.round(Math.abs(diff) / 60000)

  if (minutes < 1) return 'همین حالا'

  const units = [
    [525600, 'سال'],
    [43200, 'ماه'],
    [10080, 'هفته'],
    [1440, 'روز'],
    [60, 'ساعت'],
    [1, 'دقیقه'],
  ]

  for (const [size, label] of units) {
    if (minutes >= size) {
      const amount = Math.floor(minutes / size)
      return diff > 0
        ? `${toPersianNumber(amount)} ${label} دیگر`
        : `${toPersianNumber(amount)} ${label} پیش`
    }
  }

  return 'همین حالا'
}

function getProgressPercent(exam) {
  const start = parseDate(exam.start_at)?.getTime()
  const end = parseDate(exam.end_at)?.getTime()
  if (!start || !end || end <= start) return 0

  const now = currentTime.value
  if (now <= start) return 0
  if (now >= end) return 100

  return Math.round(((now - start) / (end - start)) * 100)
}

function getTimeRemaining(exam) {
  const state = getExamState(exam)
  if (state === 'not_started') return getRelativeTime(exam.start_at)
  if (state === 'running') return `${getRelativeTime(exam.end_at)} تا پایان`
  return 'پایان یافته'
}

function getExamAccent(exam) {
  const category = String(exam?.category || '').toLowerCase()
  if (category.includes('maz') || category.includes('ماز')) return 'maz'
  if (
    category.includes('kanoon') ||
    category.includes('ghalam') ||
    category.includes('قلم')
  ) return 'kanoon'
  if (
    category.includes('kheilisabz') ||
    category.includes('khilisabz') ||
    category.includes('سبز')
  ) return 'kheilisabz'
  if (category.includes('dopamine') || category.includes('دوپامین')) return 'dopamine'
  return 'other'
}

function getCardStyle(exam) {
  const progress = getProgressPercent(exam)
  return {
    '--exam-progress': `${progress}%`,
    '--card-index': String(Math.max(0, filteredExams.value.indexOf(exam))),
  }
}

function handleCardKeydown(event, exam) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault()
    openExamDetails(exam)
  }
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleGlobalKeydown(event) {
  const tag = event.target?.tagName?.toLowerCase()
  const typing = ['input', 'textarea', 'select'].includes(tag)

  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    showCommandPalette.value = !showCommandPalette.value
    return
  }

  if (event.key === 'Escape') {
    showCommandPalette.value = false
    showKeyboardHelp.value = false
    if (selectedExam.value) closeExamDetails()
    return
  }

  if (!typing && event.key === '/') {
    event.preventDefault()
    document.querySelector('.exam-search-input')?.focus()
  }

  if (!typing && event.key.toLowerCase() === 'r') {
    loadExams()
  }
}

function handleScroll() {
  showScrollTop.value = window.scrollY > 520
}

function focusSearch() {
  showCommandPalette.value = false
  nextTick(() => document.querySelector('.exam-search-input')?.focus())
}

function selectFromCommand(action) {
  showCommandPalette.value = false

  if (action === 'search') {
    focusSearch()
  } else if (action === 'available') {
    setQuickFilter('available')
  } else if (action === 'upcoming') {
    setQuickFilter('upcoming')
  } else if (action === 'attempted') {
    setQuickFilter('attempted')
  } else if (action === 'favorites') {
    setQuickFilter('favorites')
  } else if (action === 'refresh') {
    loadExams()
  } else if (action === 'top') {
    scrollToTop()
  }
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

    try {
      const savedFavorites = JSON.parse(
        localStorage.getItem('dopamine_exam_favorites') || '[]'
      )
      if (Array.isArray(savedFavorites)) {
        favorites.value = new Set(savedFavorites)
      }
    } catch {
      favorites.value = new Set()
    }

    window.addEventListener('keydown', handleGlobalKeydown)
    window.addEventListener('scroll', handleScroll, { passive: true })

    await loadExams()

    await nextTick()

    clockTimer =
      window.setInterval(() => {
        currentTime.value = Date.now()
        refreshExamStates()
      }, 30000)

    currentTime.value = Date.now()
    handleScroll()

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

    window.removeEventListener('keydown', handleGlobalKeydown)
    window.removeEventListener('scroll', handleScroll)

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
   DOPAMINE EXAMS — NEBULA / QUANTUM UI
   Visual system: aurora glass + editorial dashboard + motion
========================================================= */

.exams-page-wrapper {
  --font-ui: Vazirmatn, Vazir, IRANSans, Tahoma, sans-serif;
  --bg: #f5f7fb;
  --bg-deep: #edf1f8;
  --surface: rgba(255, 255, 255, 0.78);
  --surface-solid: #ffffff;
  --surface-soft: rgba(248, 250, 255, 0.82);
  --surface-muted: rgba(242, 245, 251, 0.86);
  --text: #151827;
  --text-soft: #5e6578;
  --text-muted: #8d94a7;
  --line: rgba(20, 27, 52, 0.08);
  --line-strong: rgba(20, 27, 52, 0.14);
  --primary: #7357ff;
  --primary-2: #a855f7;
  --cyan: #16b7d8;
  --green: #22b573;
  --amber: #f4a83a;
  --red: #ee5b72;
  --blue: #4b82ff;
  --shadow-xs: 0 2px 10px rgba(25, 31, 55, 0.04);
  --shadow-sm: 0 10px 30px rgba(34, 41, 70, 0.07);
  --shadow-md: 0 22px 55px rgba(36, 42, 77, 0.11);
  --shadow-lg: 0 35px 90px rgba(29, 36, 74, 0.16);
  --radius-xs: 10px;
  --radius-sm: 14px;
  --radius-md: 20px;
  --radius-lg: 28px;
  --radius-xl: 36px;
  --ease: cubic-bezier(.22, .8, .24, 1);
  --ease-bounce: cubic-bezier(.2, 1.35, .35, 1);
  --page-width: 1480px;
  position: relative;
  width: 100%;
  min-height: 100%;
  overflow: hidden;
  font-family: var(--font-ui);
  color: var(--text);
}

.exams-page {
  position: relative;
  isolation: isolate;
  min-height: 100vh;
  padding: 30px clamp(16px, 3vw, 46px) 90px;
  background:
    radial-gradient(circle at 12% 5%, rgba(115, 87, 255, .12), transparent 26%),
    radial-gradient(circle at 88% 8%, rgba(22, 183, 216, .10), transparent 24%),
    linear-gradient(145deg, var(--bg), var(--bg-deep));
  transition:
    background .5s var(--ease),
    color .5s var(--ease);
}

.exams-page.is-dark {
  --bg: #090b13;
  --bg-deep: #0e1220;
  --surface: rgba(20, 24, 38, .72);
  --surface-solid: #151a29;
  --surface-soft: rgba(22, 27, 43, .78);
  --surface-muted: rgba(25, 30, 46, .86);
  --text: #f5f6ff;
  --text-soft: #aeb4c9;
  --text-muted: #747c95;
  --line: rgba(255, 255, 255, .075);
  --line-strong: rgba(255, 255, 255, .13);
  --shadow-xs: 0 2px 10px rgba(0, 0, 0, .2);
  --shadow-sm: 0 12px 35px rgba(0, 0, 0, .22);
  --shadow-md: 0 26px 65px rgba(0, 0, 0, .30);
  --shadow-lg: 0 40px 100px rgba(0, 0, 0, .42);
  background:
    radial-gradient(circle at 14% 5%, rgba(115, 87, 255, .17), transparent 28%),
    radial-gradient(circle at 86% 10%, rgba(22, 183, 216, .13), transparent 25%),
    linear-gradient(145deg, var(--bg), var(--bg-deep));
}

.exams-page *,
.exams-page *::before,
.exams-page *::after {
  box-sizing: border-box;
}

.exams-page button,
.exams-page input,
.exams-page select {
  font: inherit;
}

.exams-page button {
  border: 0;
}

.exams-page button:focus-visible,
.exams-page input:focus-visible,
.exams-page select:focus-visible,
.exams-page article:focus-visible {
  outline: 3px solid rgba(115, 87, 255, .35);
  outline-offset: 3px;
}

/* =========================================================
   AURORA BACKGROUND
========================================================= */

.aurora-field {
  position: absolute;
  z-index: -2;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.aurora-orb {
  position: absolute;
  display: block;
  width: 420px;
  height: 420px;
  border-radius: 999px;
  filter: blur(75px);
  opacity: .26;
  animation: orbFloat 15s ease-in-out infinite alternate;
}

.orb-one {
  top: -180px;
  right: 5%;
  background: rgba(115, 87, 255, .30);
}

.orb-two {
  top: 35%;
  left: -220px;
  background: rgba(22, 183, 216, .20);
  animation-delay: -4s;
  animation-duration: 18s;
}

.orb-three {
  right: 18%;
  bottom: -240px;
  background: rgba(168, 85, 247, .18);
  animation-delay: -8s;
  animation-duration: 20s;
}

.orb-four {
  left: 42%;
  top: 52%;
  width: 260px;
  height: 260px;
  background: rgba(75, 130, 255, .12);
  animation-delay: -12s;
}

.aurora-grid {
  position: absolute;
  inset: 0;
  opacity: .42;
  background-image:
    linear-gradient(rgba(100, 110, 145, .035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(100, 110, 145, .035) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: linear-gradient(to bottom, black, transparent 80%);
}

.aurora-noise {
  position: absolute;
  inset: 0;
  opacity: .028;
  background-image:
    radial-gradient(circle at 25% 20%, #fff 0 1px, transparent 1px),
    radial-gradient(circle at 75% 80%, #fff 0 1px, transparent 1px);
  background-size: 5px 5px, 7px 7px;
}

@keyframes orbFloat {
  0% {
    transform: translate3d(-2%, -1%, 0) scale(1);
  }
  50% {
    transform: translate3d(3%, 2%, 0) scale(1.08);
  }
  100% {
    transform: translate3d(-1%, 4%, 0) scale(.96);
  }
}

/* =========================================================
   COMMAND FAB
========================================================= */

.command-fab {
  position: fixed;
  z-index: 80;
  left: 22px;
  bottom: 24px;
  display: grid;
  place-items: center;
  width: 58px;
  height: 58px;
  padding: 0;
  border: 1px solid rgba(255, 255, 255, .45);
  border-radius: 19px;
  color: #fff;
  cursor: pointer;
  background:
    linear-gradient(145deg, rgba(115, 87, 255, .96), rgba(168, 85, 247, .88));
  box-shadow:
    0 18px 45px rgba(83, 64, 190, .30),
    inset 0 1px 0 rgba(255, 255, 255, .35);
  backdrop-filter: blur(18px);
  transition:
    transform .35s var(--ease-bounce),
    box-shadow .35s var(--ease),
    border-color .35s var(--ease);
}

.command-fab:hover {
  transform: translateY(-5px) rotate(-2deg);
  box-shadow:
    0 25px 60px rgba(83, 64, 190, .42),
    inset 0 1px 0 rgba(255, 255, 255, .42);
}

.command-fab:active {
  transform: translateY(-1px) scale(.96);
}

.command-fab svg {
  width: 23px;
  height: 23px;
  position: relative;
  z-index: 2;
}

.command-fab kbd {
  position: absolute;
  left: -7px;
  top: -7px;
  min-width: 25px;
  height: 20px;
  display: grid;
  place-items: center;
  padding: 0 5px;
  border: 1px solid rgba(255, 255, 255, .4);
  border-radius: 7px;
  color: rgba(255, 255, 255, .95);
  background: rgba(16, 13, 38, .58);
  font-size: 8px;
  line-height: 1;
}

.fab-ring {
  position: absolute;
  inset: -5px;
  border: 1px solid rgba(115, 87, 255, .22);
  border-radius: 23px;
  animation: fabRing 2.8s ease-out infinite;
}

@keyframes fabRing {
  0% {
    transform: scale(.88);
    opacity: .7;
  }
  75% {
    transform: scale(1.22);
    opacity: 0;
  }
  100% {
    transform: scale(1.22);
    opacity: 0;
  }
}

/* =========================================================
   HERO HEADER
========================================================= */

.page-header {
  position: relative;
  width: min(100%, var(--page-width));
  min-height: 220px;
  margin: 0 auto 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 34px;
  padding: clamp(25px, 4vw, 48px);
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: var(--radius-xl);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, .72), rgba(255, 255, 255, .34)),
    var(--surface);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(28px) saturate(125%);
}

.is-dark .page-header {
  background:
    linear-gradient(135deg, rgba(35, 40, 61, .70), rgba(15, 19, 31, .50)),
    var(--surface);
}

.page-header::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 75% 20%, rgba(115, 87, 255, .14), transparent 25%),
    radial-gradient(circle at 95% 100%, rgba(22, 183, 216, .10), transparent 22%);
}

.page-header::after {
  content: "";
  position: absolute;
  top: 0;
  right: 8%;
  left: 8%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .85), transparent);
  opacity: .65;
}

.hero-scanline {
  position: absolute;
  top: -40%;
  right: -15%;
  width: 60%;
  height: 180%;
  pointer-events: none;
  transform: rotate(16deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .10), transparent);
  animation: scanline 8s ease-in-out infinite;
}

@keyframes scanline {
  0% {
    transform: translateX(80%) rotate(16deg);
  }
  48%,
  100% {
    transform: translateX(-100%) rotate(16deg);
  }
}

.header-main {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 24px;
  min-width: 0;
}

.header-icon-shell {
  position: relative;
  flex: 0 0 auto;
  width: 92px;
  height: 92px;
  display: grid;
  place-items: center;
}

.header-icon {
  position: relative;
  z-index: 2;
  width: 72px;
  height: 72px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, .45);
  border-radius: 24px;
  color: #fff;
  background:
    linear-gradient(145deg, rgba(115, 87, 255, .98), rgba(168, 85, 247, .80));
  box-shadow:
    0 18px 42px rgba(102, 75, 222, .30),
    inset 0 1px 0 rgba(255, 255, 255, .40);
  transform: rotate(-3deg);
  animation: iconBreath 5s ease-in-out infinite;
}

.header-icon::after {
  content: "";
  position: absolute;
  inset: 5px;
  border: 1px solid rgba(255, 255, 255, .22);
  border-radius: 19px;
}

.header-icon svg {
  position: relative;
  z-index: 3;
  width: 34px;
  height: 34px;
  stroke-width: 1.5;
}

.icon-glow {
  position: absolute;
  inset: -16px;
  border-radius: 34px;
  background: rgba(115, 87, 255, .20);
  filter: blur(22px);
  animation: iconGlow 3s ease-in-out infinite alternate;
}

.orbit-dot {
  position: absolute;
  z-index: 3;
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: #fff;
  box-shadow: 0 0 15px rgba(255, 255, 255, .9);
}

.orbit-dot-one {
  top: 4px;
  right: 12px;
  animation: dotOrbit 5s linear infinite;
}

.orbit-dot-two {
  bottom: 10px;
  left: 8px;
  opacity: .65;
  animation: dotOrbit 7s linear reverse infinite;
}

@keyframes iconBreath {
  0%,
  100% {
    transform: rotate(-3deg) translateY(0);
  }
  50% {
    transform: rotate(1deg) translateY(-4px);
  }
}

@keyframes iconGlow {
  from {
    opacity: .45;
    transform: scale(.92);
  }
  to {
    opacity: .85;
    transform: scale(1.12);
  }
}

@keyframes dotOrbit {
  from {
    transform: rotate(0deg) translateX(36px) rotate(0deg);
  }
  to {
    transform: rotate(360deg) translateX(36px) rotate(-360deg);
  }
}

.header-copy {
  min-width: 0;
}

.hero-eyebrow {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .04em;
}

.hero-eyebrow b {
  padding: 4px 8px;
  border: 1px solid rgba(34, 181, 115, .18);
  border-radius: 999px;
  color: var(--green);
  background: rgba(34, 181, 115, .07);
  font-size: 9px;
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: var(--green);
  box-shadow: 0 0 0 4px rgba(34, 181, 115, .10);
  animation: livePulse 1.8s ease-in-out infinite;
}

@keyframes livePulse {
  0%,
  100% {
    box-shadow: 0 0 0 3px rgba(34, 181, 115, .08);
  }
  50% {
    box-shadow: 0 0 0 7px rgba(34, 181, 115, .02);
  }
}

.header-copy h1 {
  margin: 0;
  color: var(--text);
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 950;
  letter-spacing: -.055em;
  line-height: 1.05;
}

.gradient-word {
  color: transparent;
  background: linear-gradient(110deg, #6c4dff, #a855f7 48%, #19aeca);
  -webkit-background-clip: text;
  background-clip: text;
}

.header-copy p {
  max-width: 650px;
  margin: 12px 0 0;
  color: var(--text-soft);
  font-size: 13px;
  line-height: 2;
}

.hero-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 16px;
  margin-top: 14px;
}

.hero-meta span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 700;
}

.hero-meta svg {
  width: 13px;
  height: 13px;
  color: var(--primary);
  stroke-width: 2;
}

.header-actions {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 9px;
  flex: 0 0 auto;
}

.refresh-button,
.help-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-height: 46px;
  border: 1px solid var(--line);
  border-radius: 15px;
  color: var(--text);
  background: rgba(255, 255, 255, .55);
  box-shadow: var(--shadow-xs);
  cursor: pointer;
  transition:
    transform .3s var(--ease-bounce),
    border-color .3s var(--ease),
    box-shadow .3s var(--ease),
    background .3s var(--ease);
}

.is-dark .refresh-button,
.is-dark .help-button {
  background: rgba(255, 255, 255, .045);
}

.refresh-button {
  padding: 0 15px;
  font-size: 11px;
  font-weight: 850;
}

.refresh-button:hover,
.help-button:hover {
  transform: translateY(-3px);
  border-color: rgba(115, 87, 255, .25);
  box-shadow: 0 14px 30px rgba(49, 54, 94, .10);
  background: rgba(255, 255, 255, .78);
}

.is-dark .refresh-button:hover,
.is-dark .help-button:hover {
  background: rgba(255, 255, 255, .08);
}

.refresh-button:disabled {
  cursor: wait;
  opacity: .75;
}

.refresh-icon {
  display: grid;
  place-items: center;
}

.refresh-icon svg {
  width: 17px;
  height: 17px;
  color: var(--primary);
  stroke-width: 2;
}

.refresh-button.spinning .refresh-icon svg {
  animation: spin 1s linear infinite;
}

.help-button {
  width: 46px;
  padding: 0;
}

.help-button svg {
  width: 18px;
  height: 18px;
  color: var(--text-soft);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* =========================================================
   COMMAND STRIP
========================================================= */

.command-strip {
  width: min(100%, var(--page-width));
  min-height: 66px;
  margin: 0 auto 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 9px 12px;
  border: 1px solid var(--line);
  border-radius: 19px;
  background: var(--surface);
  box-shadow: var(--shadow-xs);
  backdrop-filter: blur(22px);
}

.command-strip-left {
  display: flex;
  align-items: center;
  gap: 7px;
  min-width: 0;
  overflow-x: auto;
  scrollbar-width: none;
}

.command-strip-left::-webkit-scrollbar {
  display: none;
}

.command-kicker {
  flex: 0 0 auto;
  padding: 0 8px;
  color: var(--text-muted);
  font-size: 9px;
  font-weight: 900;
  white-space: nowrap;
}

.quick-filter {
  position: relative;
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 42px;
  padding: 0 12px;
  border: 1px solid transparent;
  border-radius: 13px;
  color: var(--text-soft);
  background: transparent;
  cursor: pointer;
  transition:
    color .25s var(--ease),
    background .25s var(--ease),
    transform .25s var(--ease),
    border-color .25s var(--ease);
}

.quick-filter:hover {
  color: var(--text);
  transform: translateY(-1px);
  background: rgba(115, 87, 255, .05);
}

.quick-filter.active {
  color: var(--primary);
  border-color: rgba(115, 87, 255, .12);
  background: rgba(115, 87, 255, .08);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .4);
}

.quick-filter-icon {
  display: grid;
  place-items: center;
}

.quick-filter-icon svg {
  width: 15px;
  height: 15px;
  stroke-width: 1.8;
}

.quick-filter span:last-child {
  font-size: 10px;
  font-weight: 800;
  white-space: nowrap;
}

.shortcut-hint {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 8px;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  font-size: 9px;
}

.shortcut-hint:hover {
  color: var(--primary);
}

.shortcut-hint kbd {
  display: grid;
  place-items: center;
  min-width: 20px;
  height: 20px;
  padding: 0 4px;
  border: 1px solid var(--line-strong);
  border-bottom-width: 2px;
  border-radius: 5px;
  color: var(--text-soft);
  background: var(--surface-solid);
  font-size: 8px;
  font-weight: 800;
}

/* =========================================================
   STATS
========================================================= */

.stats-grid {
  width: min(100%, var(--page-width));
  margin: 0 auto 18px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.stat-card {
  position: relative;
  min-height: 124px;
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 18px;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(22px);
  transition:
    transform .4s var(--ease-bounce),
    box-shadow .4s var(--ease),
    border-color .4s var(--ease);
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: rgba(115, 87, 255, .16);
  box-shadow: var(--shadow-md);
}

.stat-card-glow {
  position: absolute;
  width: 150px;
  height: 150px;
  left: -50px;
  top: -70px;
  border-radius: 999px;
  background: rgba(115, 87, 255, .08);
  filter: blur(25px);
  pointer-events: none;
  transition: transform .6s var(--ease);
}

.stat-card:hover .stat-card-glow {
  transform: translate(30px, 20px) scale(1.2);
}

.stat-icon {
  position: relative;
  flex: 0 0 auto;
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 15px;
  color: var(--primary);
  background: rgba(115, 87, 255, .09);
  border: 1px solid rgba(115, 87, 255, .10);
}

.stat-icon svg {
  width: 22px;
  height: 22px;
  stroke-width: 1.65;
}

.stat-upcoming .stat-icon {
  color: var(--amber);
  background: rgba(244, 168, 58, .10);
  border-color: rgba(244, 168, 58, .13);
}

.stat-running .stat-icon {
  color: var(--green);
  background: rgba(34, 181, 115, .10);
  border-color: rgba(34, 181, 115, .13);
}

.stat-completed .stat-icon {
  color: var(--blue);
  background: rgba(75, 130, 255, .10);
  border-color: rgba(75, 130, 255, .13);
}

.stat-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.stat-copy span {
  color: var(--text-muted);
  font-size: 9px;
  font-weight: 800;
}

.stat-copy strong {
  color: var(--text);
  font-size: 24px;
  font-weight: 950;
  line-height: 1.1;
  letter-spacing: -.04em;
}

.stat-copy small {
  color: var(--text-muted);
  font-size: 8px;
  font-weight: 700;
  white-space: nowrap;
}

.stat-mini-chart {
  position: absolute;
  left: 14px;
  bottom: 13px;
  display: flex;
  align-items: flex-end;
  gap: 3px;
  opacity: .6;
}

.stat-mini-chart i {
  width: 3px;
  height: 10px;
  border-radius: 5px;
  background: linear-gradient(to top, var(--primary), rgba(115, 87, 255, .08));
  animation: chartBounce 2s ease-in-out infinite alternate;
}

.stat-mini-chart i:nth-child(2) {
  height: 16px;
  animation-delay: -.2s;
}

.stat-mini-chart i:nth-child(3) {
  height: 11px;
  animation-delay: -.5s;
}

.stat-mini-chart i:nth-child(4) {
  height: 22px;
  animation-delay: -.8s;
}

.stat-mini-chart i:nth-child(5) {
  height: 14px;
  animation-delay: -1.1s;
}

.stat-mini-chart i:nth-child(6) {
  height: 27px;
  animation-delay: -1.4s;
}

.stat-mini-chart i:nth-child(7) {
  height: 19px;
  animation-delay: -1.7s;
}

@keyframes chartBounce {
  to {
    transform: scaleY(.55);
  }
}

.stat-pulse {
  position: absolute;
  left: 15px;
  top: 16px;
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: var(--green);
  box-shadow: 0 0 0 0 rgba(34, 181, 115, .25);
  animation: livePulse 1.7s infinite;
}

.live-indicator {
  position: absolute;
  left: 14px;
  bottom: 15px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--green);
  font-size: 8px;
  font-weight: 900;
}

.live-indicator i {
  width: 5px;
  height: 5px;
  border-radius: 999px;
  background: currentColor;
}

.completion-ring {
  position: absolute;
  left: 13px;
  top: 14px;
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background:
    radial-gradient(circle at center, var(--surface-solid) 55%, transparent 57%),
    conic-gradient(var(--blue) var(--value), rgba(75, 130, 255, .08) 0);
}

.completion-ring span {
  color: var(--blue);
  font-size: 7px;
  font-weight: 950;
}

/* =========================================================
   DISCOVERY
========================================================= */

.discovery-panel {
  width: min(100%, var(--page-width));
  margin: 0 auto 16px;
  padding: 24px;
  border: 1px solid var(--line);
  border-radius: 25px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(24px);
}

.discovery-top {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.discovery-title {
  min-width: 0;
}

.section-overline {
  display: block;
  margin-bottom: 5px;
  color: var(--primary);
  font-size: 9px;
  font-weight: 950;
  letter-spacing: .08em;
}

.discovery-title h2 {
  margin: 0;
  color: var(--text);
  font-size: 20px;
  font-weight: 950;
  letter-spacing: -.035em;
}

.discovery-title p {
  margin: 6px 0 0;
  color: var(--text-muted);
  font-size: 10px;
  line-height: 1.8;
}

.view-switcher {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 4px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: var(--surface-muted);
}

.view-switcher button {
  width: 34px;
  height: 32px;
  display: grid;
  place-items: center;
  border-radius: 9px;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  transition: .25s var(--ease);
}

.view-switcher button:hover {
  color: var(--text);
}

.view-switcher button.active {
  color: var(--primary);
  background: var(--surface-solid);
  box-shadow: var(--shadow-xs);
}

.view-switcher svg {
  width: 16px;
  height: 16px;
  stroke-width: 1.7;
}

.discovery-controls {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  gap: 8px;
}

.search-box {
  position: relative;
  min-width: 0;
  height: 54px;
  display: flex;
  align-items: center;
  border: 1px solid var(--line);
  border-radius: 15px;
  background: var(--surface-muted);
  transition:
    border-color .25s var(--ease),
    box-shadow .25s var(--ease),
    background .25s var(--ease);
}

.search-box:focus-within {
  border-color: rgba(115, 87, 255, .35);
  background: var(--surface-solid);
  box-shadow:
    0 0 0 4px rgba(115, 87, 255, .06),
    var(--shadow-xs);
}

.search-icon {
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  width: 52px;
  color: var(--text-muted);
}

.search-icon svg {
  width: 19px;
  height: 19px;
}

.exam-search-input {
  width: 100%;
  min-width: 0;
  height: 100%;
  padding: 0 4px;
  border: 0;
  outline: 0;
  color: var(--text);
  background: transparent;
  font-size: 11px;
  font-weight: 650;
}

.exam-search-input::placeholder {
  color: var(--text-muted);
}

.exam-search-input::-webkit-search-cancel-button {
  display: none;
}

.clear-search {
  width: 30px;
  height: 30px;
  margin-left: 8px;
  display: grid;
  place-items: center;
  border-radius: 9px;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
}

.clear-search:hover {
  color: var(--red);
  background: rgba(238, 91, 114, .08);
}

.clear-search svg {
  width: 15px;
  height: 15px;
}

.search-box > kbd {
  flex: 0 0 auto;
  margin-left: 10px;
  display: grid;
  place-items: center;
  width: 25px;
  height: 24px;
  border: 1px solid var(--line);
  border-bottom-width: 2px;
  border-radius: 7px;
  color: var(--text-muted);
  background: var(--surface-solid);
  font-size: 9px;
}

.sort-box {
  height: 54px;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 142px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 15px;
  color: var(--text-soft);
  background: var(--surface-muted);
}

.sort-icon {
  display: grid;
  place-items: center;
  color: var(--primary);
}

.sort-icon svg {
  width: 17px;
  height: 17px;
}

.sort-box select {
  width: 100%;
  border: 0;
  outline: 0;
  color: var(--text);
  background: transparent;
  cursor: pointer;
  font-size: 10px;
  font-weight: 800;
}

.filter-toggle {
  position: relative;
  height: 54px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 15px;
  border: 1px solid var(--line);
  border-radius: 15px;
  color: var(--text-soft);
  background: var(--surface-muted);
  cursor: pointer;
  transition: .3s var(--ease);
}

.filter-toggle:hover,
.filter-toggle.active {
  color: var(--primary);
  border-color: rgba(115, 87, 255, .18);
  background: rgba(115, 87, 255, .06);
}

.filter-toggle svg {
  width: 17px;
  height: 17px;
}

.filter-toggle span {
  font-size: 10px;
  font-weight: 800;
}

.filter-toggle i {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: transparent;
}

.filter-toggle i.on {
  background: var(--primary);
  box-shadow: 0 0 0 4px rgba(115, 87, 255, .08);
}

/* =========================================================
   ADVANCED FILTERS
========================================================= */

.advanced-filters {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 18px;
  margin-top: 12px;
  padding-top: 15px;
  border-top: 1px dashed var(--line);
}

.advanced-filter-group {
  min-width: 0;
}

.advanced-filter-group > span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-muted);
  font-size: 9px;
  font-weight: 800;
}

.filter-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.filter-pills button {
  min-height: 32px;
  padding: 0 11px;
  border: 1px solid var(--line);
  border-radius: 9px;
  color: var(--text-soft);
  background: var(--surface-muted);
  cursor: pointer;
  font-size: 9px;
  font-weight: 800;
  transition: .25s var(--ease);
}

.filter-pills button:hover,
.filter-pills button.active {
  color: var(--primary);
  border-color: rgba(115, 87, 255, .18);
  background: rgba(115, 87, 255, .07);
}

.availability-toggle {
  min-width: 220px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.availability-toggle span {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.availability-toggle strong {
  color: var(--text);
  font-size: 9px;
  font-weight: 850;
}

.availability-toggle small {
  color: var(--text-muted);
  font-size: 8px;
}

.availability-toggle input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.availability-toggle i {
  position: relative;
  flex: 0 0 auto;
  width: 43px;
  height: 24px;
  border-radius: 999px;
  background: rgba(130, 139, 160, .18);
  transition: .3s var(--ease);
}

.availability-toggle i::after {
  content: "";
  position: absolute;
  top: 3px;
  right: 3px;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, .16);
  transition: .3s var(--ease-bounce);
}

.availability-toggle input:checked + i {
  background: var(--primary);
}

.availability-toggle input:checked + i::after {
  transform: translateX(-19px);
}

.reset-filters {
  min-height: 34px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0 10px;
  border-radius: 9px;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  font-size: 9px;
  font-weight: 800;
}

.reset-filters:hover {
  color: var(--red);
  background: rgba(238, 91, 114, .06);
}

.reset-filters svg {
  width: 14px;
  height: 14px;
}

.filter-expand-enter-active,
.filter-expand-leave-active {
  transition:
    opacity .28s var(--ease),
    transform .28s var(--ease);
}

.filter-expand-enter-from,
.filter-expand-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* =========================================================
   CATEGORY TABS
========================================================= */

.filters-section {
  width: min(100%, var(--page-width));
  margin: 0 auto 18px;
  padding: 22px 24px;
  border: 1px solid var(--line);
  border-radius: 24px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(22px);
}

.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.section-heading > div {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.section-heading span:first-child {
  color: var(--text-muted);
  font-size: 9px;
  font-weight: 800;
}

.section-heading strong {
  color: var(--text);
  font-size: 16px;
  font-weight: 950;
}

.result-count {
  color: var(--primary);
  font-size: 9px;
  font-weight: 900;
}

.category-tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 2px;
  scrollbar-width: thin;
}

.category-tabs::-webkit-scrollbar {
  height: 4px;
}

.category-tabs::-webkit-scrollbar-thumb {
  border-radius: 99px;
  background: rgba(115, 87, 255, .14);
}

.category-tab {
  position: relative;
  flex: 0 0 auto;
  min-height: 47px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 13px;
  color: var(--text-soft);
  background: var(--surface-muted);
  cursor: pointer;
  overflow: hidden;
  transition:
    color .3s var(--ease),
    background .3s var(--ease),
    border-color .3s var(--ease),
    transform .3s var(--ease-bounce),
    box-shadow .3s var(--ease);
}

.category-tab::after {
  content: "";
  position: absolute;
  right: -35%;
  top: -100%;
  width: 70%;
  height: 250%;
  transform: rotate(18deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .24), transparent);
  opacity: 0;
  transition: .4s var(--ease);
}

.category-tab:hover {
  transform: translateY(-2px);
  color: var(--text);
  border-color: rgba(115, 87, 255, .15);
  box-shadow: var(--shadow-xs);
}

.category-tab:hover::after {
  right: 130%;
  opacity: 1;
}

.category-tab.active {
  color: var(--primary);
  border-color: rgba(115, 87, 255, .20);
  background: rgba(115, 87, 255, .08);
  box-shadow:
    0 8px 22px rgba(115, 87, 255, .08),
    inset 0 1px 0 rgba(255, 255, 255, .55);
}

.tab-symbol {
  width: 27px;
  height: 27px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: rgba(115, 87, 255, .08);
}

.tab-symbol svg {
  width: 14px;
  height: 14px;
  stroke-width: 1.7;
}

.category-tab small {
  min-width: 20px;
  height: 20px;
  display: grid;
  place-items: center;
  padding: 0 5px;
  border-radius: 7px;
  color: var(--text-muted);
  background: rgba(0, 0, 0, .035);
  font-size: 8px;
  font-weight: 900;
}

.is-dark .category-tab small {
  background: rgba(255, 255, 255, .05);
}

.category-tab > span:not(.tab-symbol) {
  font-size: 10px;
  font-weight: 850;
  white-space: nowrap;
}

.tab-maz.active {
  color: #e05b74;
  border-color: rgba(224, 91, 116, .18);
  background: rgba(224, 91, 116, .07);
}

.tab-kanoon.active {
  color: #397de8;
  border-color: rgba(57, 125, 232, .18);
  background: rgba(57, 125, 232, .07);
}

.tab-kheilisabz.active {
  color: #19a978;
  border-color: rgba(25, 169, 120, .18);
  background: rgba(25, 169, 120, .07);
}

.tab-dopamine.active {
  color: #9a5cf6;
  border-color: rgba(154, 92, 246, .18);
  background: rgba(154, 92, 246, .07);
}

.tab-other.active {
  color: var(--primary);
}

/* =========================================================
   RESULTS TOOLBAR
========================================================= */

.results-toolbar {
  width: min(100%, var(--page-width));
  min-height: 42px;
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 0 4px;
}

.results-toolbar > div:first-child {
  display: flex;
  align-items: center;
  gap: 6px;
}

.results-toolbar strong {
  color: var(--text);
  font-size: 10px;
  font-weight: 950;
}

.results-toolbar span:not(.results-dot) {
  color: var(--text-muted);
  font-size: 9px;
}

.results-dot {
  width: 6px;
  height: 6px;
  border-radius: 99px;
  background: var(--primary);
  box-shadow: 0 0 0 4px rgba(115, 87, 255, .08);
}

.results-toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.results-toolbar-actions button {
  padding: 6px 8px;
  border-radius: 7px;
  color: var(--red);
  background: rgba(238, 91, 114, .06);
  cursor: pointer;
  font-size: 8px;
  font-weight: 850;
}

/* =========================================================
   EXAM GRID
========================================================= */

.exam-grid {
  width: min(100%, var(--page-width));
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  align-items: start;
}

.exam-grid.list-view {
  grid-template-columns: 1fr;
}

.exam-card {
  --card-progress: 0%;
  position: relative;
  min-width: 0;
  padding: 20px;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 27px;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, .72), rgba(255, 255, 255, .43)),
    var(--surface);
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(24px) saturate(125%);
  cursor: default;
  animation: cardIn .65s var(--ease) both;
  animation-delay: calc(var(--card-index) * 55ms);
  transition:
    transform .45s var(--ease-bounce),
    box-shadow .45s var(--ease),
    border-color .35s var(--ease),
    background .35s var(--ease);
}

.is-dark .exam-card {
  background:
    linear-gradient(145deg, rgba(31, 37, 56, .76), rgba(17, 21, 34, .62)),
    var(--surface);
}

@keyframes cardIn {
  from {
    opacity: 0;
    transform: translateY(22px) scale(.985);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.exam-card:hover,
.exam-card.is-hovered {
  transform: translateY(-8px);
  border-color: rgba(115, 87, 255, .19);
  box-shadow:
    0 30px 75px rgba(35, 42, 76, .13),
    0 0 0 1px rgba(115, 87, 255, .025);
}

.is-dark .exam-card:hover,
.is-dark .exam-card.is-hovered {
  box-shadow:
    0 30px 80px rgba(0, 0, 0, .36),
    0 0 0 1px rgba(115, 87, 255, .06);
}

.exam-card::before {
  content: "";
  position: absolute;
  z-index: 0;
  top: 0;
  right: 8%;
  left: 8%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .75), transparent);
  opacity: .65;
}

.card-ambient {
  position: absolute;
  z-index: 0;
  width: 260px;
  height: 260px;
  right: -120px;
  top: -150px;
  border-radius: 999px;
  background: rgba(115, 87, 255, .10);
  filter: blur(25px);
  transition:
    transform .8s var(--ease),
    opacity .5s var(--ease);
  pointer-events: none;
}

.exam-card:hover .card-ambient {
  transform: translate(-55px, 65px) scale(1.25);
  opacity: .9;
}

.card-noise {
  position: absolute;
  z-index: 0;
  inset: 0;
  pointer-events: none;
  opacity: .02;
  background-image: radial-gradient(currentColor .7px, transparent .7px);
  background-size: 6px 6px;
}

.card-progress-line {
  position: absolute;
  z-index: 3;
  right: 0;
  bottom: 0;
  left: 0;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent 0,
    transparent calc(100% - var(--card-progress)),
    rgba(115, 87, 255, .0) calc(100% - var(--card-progress)),
    rgba(115, 87, 255, .85) calc(100% - var(--card-progress)),
    rgba(168, 85, 247, .85) 100%
  );
  opacity: .45;
}

.exam-card > *:not(.card-ambient):not(.card-noise):not(.card-progress-line):not(.card-corner) {
  position: relative;
  z-index: 2;
}

.card-corner {
  position: absolute;
  z-index: 1;
  width: 16px;
  height: 16px;
  border-color: rgba(115, 87, 255, .16);
  pointer-events: none;
  transition: .4s var(--ease);
}

.corner-one {
  top: 13px;
  left: 13px;
  border-top: 1px solid;
  border-left: 1px solid;
  border-top-left-radius: 6px;
}

.corner-two {
  right: 13px;
  bottom: 13px;
  border-right: 1px solid;
  border-bottom: 1px solid;
  border-bottom-right-radius: 6px;
}

.exam-card:hover .card-corner {
  width: 24px;
  height: 24px;
  border-color: rgba(115, 87, 255, .28);
}

/* =========================================================
   CARD TOP
========================================================= */

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 18px;
}

.card-top-actions {
  display: flex;
  align-items: center;
  gap: 7px;
}

.provider-badge,
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 27px;
  padding: 0 9px;
  border: 1px solid var(--line);
  border-radius: 999px;
  font-size: 8px;
  font-weight: 900;
  white-space: nowrap;
}

.provider-badge span {
  width: 5px;
  height: 5px;
  border-radius: 999px;
  background: currentColor;
  box-shadow: 0 0 0 3px color-mix(in srgb, currentColor 12%, transparent);
}

.provider-maz {
  color: #df5873;
  background: rgba(223, 88, 115, .07);
  border-color: rgba(223, 88, 115, .13);
}

.provider-kanoon {
  color: #3d7fe8;
  background: rgba(61, 127, 232, .07);
  border-color: rgba(61, 127, 232, .13);
}

.provider-kheilisabz {
  color: #1aa977;
  background: rgba(26, 169, 119, .07);
  border-color: rgba(26, 169, 119, .13);
}

.provider-dopamine {
  color: #9857f5;
  background: rgba(152, 87, 245, .07);
  border-color: rgba(152, 87, 245, .13);
}

.provider-other {
  color: var(--primary);
  background: rgba(115, 87, 255, .07);
  border-color: rgba(115, 87, 255, .13);
}

.status-badge i {
  width: 5px;
  height: 5px;
  border-radius: 999px;
  background: currentColor;
}

.status-not_started {
  color: #b7791f;
  background: rgba(244, 168, 58, .07);
  border-color: rgba(244, 168, 58, .13);
}

.status-running {
  color: var(--green);
  background: rgba(34, 181, 115, .07);
  border-color: rgba(34, 181, 115, .13);
}

.status-running i {
  animation: livePulseSmall 1.5s infinite;
}

.status-ended {
  color: var(--text-muted);
  background: rgba(130, 139, 160, .07);
  border-color: var(--line);
}

.status-inactive {
  color: var(--red);
  background: rgba(238, 91, 114, .07);
  border-color: rgba(238, 91, 114, .13);
}

@keyframes livePulseSmall {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(34, 181, 115, .20);
  }
  50% {
    box-shadow: 0 0 0 5px rgba(34, 181, 115, .01);
  }
}

.favorite-button {
  width: 29px;
  height: 29px;
  display: grid;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 9px;
  color: var(--text-muted);
  background: var(--surface-muted);
  cursor: pointer;
  transition:
    transform .3s var(--ease-bounce),
    color .3s var(--ease),
    background .3s var(--ease),
    border-color .3s var(--ease);
}

.favorite-button:hover {
  color: var(--red);
  transform: translateY(-2px) scale(1.04);
  background: rgba(238, 91, 114, .07);
  border-color: rgba(238, 91, 114, .15);
}

.favorite-button.active {
  color: var(--red);
  background: rgba(238, 91, 114, .09);
  border-color: rgba(238, 91, 114, .16);
}

.favorite-button.active svg {
  fill: currentColor;
}

.favorite-button svg {
  width: 14px;
  height: 14px;
  stroke-width: 1.7;
}

/* =========================================================
   CARD HEADING
========================================================= */

.exam-heading {
  position: relative;
  margin-bottom: 15px;
  padding-left: 2px;
}

.exam-index {
  display: inline-flex;
  align-items: center;
  gap: 1px;
  margin-bottom: 7px;
  color: var(--text-muted);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 8px;
  font-weight: 800;
  direction: ltr;
  opacity: .75;
}

.exam-index span {
  color: var(--primary);
}

.exam-heading h2 {
  margin: 0;
  color: var(--text);
  font-size: 19px;
  font-weight: 950;
  letter-spacing: -.04em;
  line-height: 1.45;
}

.exam-heading p {
  display: -webkit-box;
  overflow: hidden;
  margin: 6px 0 0;
  color: var(--text-muted);
  font-size: 9px;
  line-height: 1.9;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

/* =========================================================
   LIVE PANEL
========================================================= */

.exam-live-panel {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 62px;
  margin-bottom: 11px;
  padding: 10px 12px;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(255, 255, 255, .34);
}

.is-dark .exam-live-panel {
  background: rgba(255, 255, 255, .025);
}

.exam-live-panel::after {
  content: "";
  position: absolute;
  top: -80%;
  left: -20%;
  width: 35%;
  height: 260%;
  transform: rotate(18deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .17), transparent);
  animation: liveSweep 6s ease-in-out infinite;
}

@keyframes liveSweep {
  0%,
  55% {
    transform: translateX(0) rotate(18deg);
  }
  100% {
    transform: translateX(430%) rotate(18deg);
  }
}

.live-panel-icon {
  flex: 0 0 auto;
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  border-radius: 11px;
  color: var(--primary);
  background: rgba(115, 87, 255, .08);
}

.live-panel-icon svg {
  width: 17px;
  height: 17px;
}

.live-panel-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.live-panel-copy span {
  color: var(--text-muted);
  font-size: 8px;
  font-weight: 750;
}

.live-panel-copy strong {
  overflow: hidden;
  color: var(--text);
  font-size: 11px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.state-running .live-panel-icon {
  color: var(--green);
  background: rgba(34, 181, 115, .09);
}

.state-running {
  border-color: rgba(34, 181, 115, .15);
  background: rgba(34, 181, 115, .025);
}

.state-not_started .live-panel-icon {
  color: var(--amber);
  background: rgba(244, 168, 58, .09);
}

.state-not_started {
  border-color: rgba(244, 168, 58, .14);
}

.state-ended {
  opacity: .82;
}

.mini-progress {
  position: relative;
  flex: 1 1 auto;
  max-width: 90px;
  height: 4px;
  margin-right: auto;
  overflow: hidden;
  border-radius: 99px;
  background: rgba(115, 87, 255, .08);
}

.mini-progress span {
  position: absolute;
  inset: 0 auto 0 0;
  width: var(--progress);
  border-radius: inherit;
  background: linear-gradient(90deg, var(--primary), var(--primary-2));
  transition: width .5s var(--ease);
}

/* =========================================================
   DATE
========================================================= */

.exam-date {
  position: relative;
  display: flex;
  align-items: center;
  gap: 11px;
  min-height: 75px;
  margin-bottom: 12px;
  padding: 11px 12px;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 17px;
  background:
    linear-gradient(120deg, rgba(115, 87, 255, .045), transparent 50%),
    var(--surface-muted);
}

.exam-date::before {
  content: "";
  position: absolute;
  right: -30%;
  top: -80%;
  width: 60%;
  height: 250%;
  transform: rotate(20deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .18), transparent);
  opacity: 0;
  transition: .5s var(--ease);
}

.exam-card:hover .exam-date::before {
  right: 130%;
  opacity: 1;
}

.date-icon {
  flex: 0 0 auto;
  width: 39px;
  height: 39px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  color: var(--primary);
  background: rgba(115, 87, 255, .08);
}

.date-icon svg {
  width: 18px;
  height: 18px;
}

.date-content {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.date-content > span {
  color: var(--text-muted);
  font-size: 8px;
  font-weight: 750;
}

.date-content > strong {
  overflow: hidden;
  color: var(--text);
  font-size: 10px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.date-time {
  display: flex;
  align-items: center;
  gap: 5px;
  direction: ltr;
}

.date-time span {
  color: var(--primary);
  font-size: 9px;
  font-weight: 900;
}

.date-time b {
  color: var(--text-muted);
  font-size: 8px;
}

.date-relative {
  margin-right: auto;
  align-self: flex-start;
  padding: 5px 7px;
  border: 1px solid var(--line);
  border-radius: 7px;
  color: var(--text-muted);
  background: var(--surface-solid);
  font-size: 7px;
  font-weight: 850;
  white-space: nowrap;
}

/* =========================================================
   INFO GRID
========================================================= */

.exam-info-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 7px;
  margin-bottom: 13px;
}

.exam-info {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 7px;
  min-height: 58px;
  padding: 8px;
  border: 1px solid var(--line);
  border-radius: 13px;
  background: rgba(255, 255, 255, .24);
  transition:
    transform .3s var(--ease-bounce),
    background .3s var(--ease),
    border-color .3s var(--ease);
}

.is-dark .exam-info {
  background: rgba(255, 255, 255, .018);
}

.exam-info:hover {
  transform: translateY(-2px);
  border-color: rgba(115, 87, 255, .13);
  background: rgba(115, 87, 255, .045);
}

.info-icon {
  flex: 0 0 auto;
  width: 27px;
  height: 27px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  color: var(--primary);
  background: rgba(115, 87, 255, .065);
}

.info-icon svg {
  width: 13px;
  height: 13px;
  stroke-width: 1.7;
}

.exam-info > div {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.exam-info small {
  color: var(--text-muted);
  font-size: 7px;
  font-weight: 700;
  white-space: nowrap;
}

.exam-info strong {
  overflow: hidden;
  color: var(--text);
  font-size: 8px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* =========================================================
   BOOKLETS
========================================================= */

.booklets {
  margin-bottom: 13px;
  padding: 13px;
  border: 1px solid var(--line);
  border-radius: 17px;
  background: rgba(255, 255, 255, .18);
}

.is-dark .booklets {
  background: rgba(255, 255, 255, .015);
}

.booklets-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 9px;
}

.booklets-header > div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.booklets-header span {
  color: var(--text-muted);
  font-size: 7px;
  font-weight: 750;
}

.booklets-header strong {
  color: var(--text);
  font-size: 9px;
  font-weight: 900;
}

.booklets-header > small {
  color: var(--primary);
  font-size: 7px;
  font-weight: 900;
}

.booklets-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.booklet {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px;
  border: 1px solid transparent;
  border-radius: 11px;
  transition:
    transform .3s var(--ease-bounce),
    border-color .3s var(--ease),
    background .3s var(--ease);
}

.booklet:hover {
  transform: translateX(-4px);
  border-color: var(--line);
  background: rgba(255, 255, 255, .42);
}

.is-dark .booklet:hover {
  background: rgba(255, 255, 255, .035);
}

.booklet-number {
  flex: 0 0 auto;
  width: 27px;
  height: 27px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  color: var(--primary);
  background: rgba(115, 87, 255, .08);
  font-size: 8px;
  font-weight: 950;
}

.booklet-main {
  min-width: 0;
  flex: 1;
}

.booklet-title {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
}

.booklet-title strong {
  overflow: hidden;
  color: var(--text);
  font-size: 8px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.booklet-title span {
  flex: 0 0 auto;
  max-width: 90px;
  overflow: hidden;
  padding: 2px 5px;
  border-radius: 5px;
  color: var(--text-muted);
  background: rgba(130, 139, 160, .07);
  font-size: 6px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.booklet-main > small {
  display: block;
  margin-top: 2px;
  color: var(--text-muted);
  font-size: 7px;
}

.booklet-main > small b {
  margin: 0 3px;
  color: var(--line-strong);
}

.booklet-arrow {
  flex: 0 0 auto;
  width: 13px;
  height: 13px;
  color: var(--text-muted);
  transition: .25s var(--ease);
}

.booklet:hover .booklet-arrow {
  color: var(--primary);
  transform: translateX(-3px);
}

.no-booklets {
  min-height: 42px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 13px;
  padding: 0 10px;
  border: 1px dashed var(--line-strong);
  border-radius: 12px;
  color: var(--text-muted);
  background: rgba(130, 139, 160, .025);
  font-size: 8px;
  font-weight: 700;
}

.no-booklets svg {
  width: 15px;
  height: 15px;
  color: var(--text-muted);
}

/* =========================================================
   ATTEMPT / RESULT BANNERS
========================================================= */

.attempt-banner,
.result-banner {
  position: relative;
  display: flex;
  align-items: center;
  gap: 9px;
  min-height: 55px;
  margin-bottom: 11px;
  padding: 8px 10px;
  overflow: hidden;
  border: 1px solid;
  border-radius: 15px;
}

.attempt-banner {
  border-color: rgba(244, 168, 58, .16);
  background: rgba(244, 168, 58, .055);
}

.result-banner {
  border-color: rgba(34, 181, 115, .16);
  background: rgba(34, 181, 115, .055);
}

.attempt-banner::after,
.result-banner::after {
  content: "";
  position: absolute;
  top: -100%;
  left: -25%;
  width: 30%;
  height: 300%;
  transform: rotate(18deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .18), transparent);
  animation: bannerShine 5s ease-in-out infinite;
}

@keyframes bannerShine {
  0%,
  60% {
    transform: translateX(0) rotate(18deg);
  }
  100% {
    transform: translateX(520%) rotate(18deg);
  }
}

.attempt-icon,
.result-icon {
  flex: 0 0 auto;
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 10px;
}

.attempt-icon {
  color: var(--amber);
  background: rgba(244, 168, 58, .09);
}

.result-icon {
  color: var(--green);
  background: rgba(34, 181, 115, .09);
}

.attempt-icon svg,
.result-icon svg {
  width: 17px;
  height: 17px;
}

.attempt-banner > div:nth-child(2),
.result-banner > div:nth-child(2) {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.attempt-banner strong,
.result-banner strong {
  color: var(--text);
  font-size: 8px;
  font-weight: 900;
}

.attempt-banner span,
.result-banner span {
  color: var(--text-muted);
  font-size: 7px;
}

.attempt-banner > b {
  margin-right: auto;
  color: var(--amber);
  font-size: 8px;
}

.result-arrow {
  margin-right: auto;
  color: var(--green) !important;
  font-size: 15px !important;
  font-weight: 900;
}

/* =========================================================
   EXPANDED PANEL
========================================================= */

.card-expanded-panel {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin: -2px 0 11px;
  padding: 8px;
  border: 1px solid var(--line);
  border-radius: 13px;
  background: rgba(115, 87, 255, .035);
}

.card-expanded-panel > div {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 7px;
  border-radius: 9px;
  background: rgba(255, 255, 255, .25);
}

.is-dark .card-expanded-panel > div {
  background: rgba(255, 255, 255, .02);
}

.card-expanded-panel span {
  color: var(--text-muted);
  font-size: 6px;
  font-weight: 700;
}

.card-expanded-panel strong {
  overflow: hidden;
  color: var(--text);
  font-size: 8px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.expand-enter-active,
.expand-leave-active {
  overflow: hidden;
  transition:
    max-height .35s var(--ease),
    opacity .25s var(--ease),
    transform .35s var(--ease);
  max-height: 100px;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-6px);
}

/* =========================================================
   CARD FOOTER
========================================================= */
.exam-footer {
  position:relative;
  z-index:2;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-top:auto;
  padding-top:17px;
  border-top:1px solid var(--exam-border);
}

.footer-message {color:var(--exam-text-muted);font-size:9px;font-weight:750;line-height:1.7}
.footer-actions {display:flex;align-items:center;gap:7px}

.footer-actions button {
  min-height:38px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:6px;
  padding:0 12px;
  border-radius:11px;
  font-family:inherit;
  font-size:9px;
  font-weight:900;
  cursor:pointer;
  transition:transform .22s ease,box-shadow .22s ease,background .22s ease;
}

.footer-actions button:hover:not(:disabled) {transform:translateY(-3px)}
.footer-actions svg {width:15px;height:15px;stroke-width:1.9}

.result-button {
  color:var(--exam-primary);
  background:rgba(var(--exam-primary-rgb),.075);
  border:1px solid rgba(var(--exam-primary-rgb),.13);
}
.result-button:hover {background:rgba(var(--exam-primary-rgb),.13);box-shadow:0 8px 20px rgba(var(--exam-primary-rgb),.10)}

.start-button {
  position:relative;
  overflow:hidden;
  color:#fff;
  border:0;
  background:linear-gradient(135deg,var(--exam-primary),color-mix(in srgb,var(--exam-primary) 62%,#7c3aed));
  box-shadow:0 9px 24px rgba(var(--exam-primary-rgb),.25);
}

.start-button::before {
  content:"";
  position:absolute;
  top:0;
  bottom:0;
  width:45%;
  left:-60%;
  transform:skewX(-20deg);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.32),transparent);
  transition:left .6s ease;
}
.start-button:hover::before {left:125%}
.start-button:hover {box-shadow:0 13px 30px rgba(var(--exam-primary-rgb),.34)}

.disabled-button {
  color:var(--exam-text-muted);
  background:var(--exam-surface-2);
  border:1px solid var(--exam-border);
  cursor:not-allowed !important;
}


.footer-status-dot {
  flex: 0 0 auto;
  width: 5px;
  height: 5px;
  border-radius: 999px;
  background: var(--primary);
  box-shadow: 0 0 0 3px rgba(115, 87, 255, .07);
}

.is-running .footer-status-dot {
  background: var(--green);
  box-shadow: 0 0 0 3px rgba(34, 181, 115, .08);
  animation: livePulse 1.7s infinite;
}

.details-button,
.expand-button {
  min-height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 0 9px;
  border: 1px solid var(--line);
  border-radius: 10px;
  font-size: 8px;
  font-weight: 900;
  cursor: pointer;
  transition:
    transform .3s var(--ease-bounce),
    box-shadow .3s var(--ease),
    color .3s var(--ease),
    background .3s var(--ease),
    border-color .3s var(--ease);
}

.details-button {
  color: var(--text-soft);
  background: var(--surface-muted);
}

.details-button:hover {
  transform: translateY(-2px);
  color: var(--text);
  border-color: var(--line-strong);
}

.result-button {
  color: var(--green);
  background: rgba(34, 181, 115, .065);
  border-color: rgba(34, 181, 115, .13);
}

.result-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 9px 22px rgba(34, 181, 115, .10);
}

.start-button {
  position: relative;
  min-width: 104px;
  overflow: hidden;
  color: #fff;
  border-color: rgba(255, 255, 255, .22);
  background: linear-gradient(120deg, #6d4df8, #a855f7);
  box-shadow: 0 10px 24px rgba(111, 78, 231, .20);
}

.start-button::before {
  content: "";
  position: absolute;
  top: -80%;
  right: -30%;
  width: 35%;
  height: 260%;
  transform: rotate(18deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .30), transparent);
  transition: right .5s var(--ease);
}

.start-button:hover::before {
  right: 130%;
}

.start-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 32px rgba(111, 78, 231, .30);
}

.start-button:active {
  transform: translateY(-1px) scale(.98);
}

.start-button span,
.start-button svg {
  position: relative;
  z-index: 2;
}

.start-button svg {
  width: 13px;
  height: 13px;
}

.disabled-button {
  color: var(--text-muted);
  background: rgba(130, 139, 160, .06);
  cursor: not-allowed;
}

.expand-button {
  width: 34px;
  padding: 0;
  color: var(--text-muted);
  background: transparent;
}

.expand-button:hover {
  color: var(--primary);
  background: rgba(115, 87, 255, .06);
}

.expand-button svg {
  width: 14px;
  height: 14px;
}

.soft-enter-active,
.soft-leave-active {
  transition:
    opacity .25s var(--ease),
    transform .3s var(--ease-bounce);
}

.soft-enter-from,
.soft-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* =========================================================
   LIST VIEW
========================================================= */

.exam-grid.list-view .exam-card {
  display: grid;
  grid-template-columns: minmax(250px, 1.1fr) minmax(250px, .9fr);
  column-gap: 20px;
  padding: 22px;
}

.exam-grid.list-view .exam-card > .card-top {
  grid-column: 1 / -1;
}

.exam-grid.list-view .exam-card > .exam-heading {
  grid-column: 1;
  grid-row: 2 / span 2;
  align-self: center;
  padding-left: 5px;
}

.exam-grid.list-view .exam-card > .exam-live-panel {
  grid-column: 2;
  grid-row: 2;
}

.exam-grid.list-view .exam-card > .exam-date {
  grid-column: 2;
  grid-row: 3;
}

.exam-grid.list-view .exam-card > .exam-info-grid {
  grid-column: 1 / -1;
  grid-row: 4;
}

.exam-grid.list-view .exam-card > .booklets,
.exam-grid.list-view .exam-card > .no-booklets,
.exam-grid.list-view .exam-card > .attempt-banner,
.exam-grid.list-view .exam-card > .result-banner,
.exam-grid.list-view .exam-card > .card-expanded-panel {
  grid-column: 1 / -1;
}

.exam-grid.list-view .exam-card > .exam-footer {
  grid-column: 1 / -1;
}

.exam-grid.list-view .exam-info-grid {
  grid-template-columns: repeat(4, 1fr);
}

/* =========================================================
   BOTTOM INSIGHT
========================================================= */

.bottom-insight {
  width: min(100%, var(--page-width));
  min-height: 82px;
  margin: 22px auto 0;
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 12px 15px;
  border: 1px solid rgba(115, 87, 255, .12);
  border-radius: 19px;
  background:
    linear-gradient(105deg, rgba(115, 87, 255, .065), rgba(22, 183, 216, .035)),
    var(--surface);
  box-shadow: var(--shadow-xs);
}

.insight-orb {
  position: relative;
  flex: 0 0 auto;
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 15px;
  color: var(--primary);
  background: rgba(115, 87, 255, .08);
}

.insight-orb span {
  position: absolute;
  inset: 5px;
  border: 1px dashed rgba(115, 87, 255, .20);
  border-radius: 11px;
  animation: spin 10s linear infinite;
}

.insight-orb svg {
  position: relative;
  width: 21px;
  height: 21px;
}

.bottom-insight > div:nth-child(2) {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.bottom-insight > div:nth-child(2) span {
  color: var(--primary);
  font-size: 8px;
  font-weight: 900;
}

.bottom-insight > div:nth-child(2) strong {
  color: var(--text);
  font-size: 10px;
  font-weight: 850;
}

.bottom-insight > button {
  margin-right: auto;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 8px 10px;
  border: 1px solid var(--line);
  border-radius: 9px;
  color: var(--primary);
  background: var(--surface-solid);
  cursor: pointer;
  font-size: 8px;
  font-weight: 850;
  transition: .3s var(--ease-bounce);
}

.bottom-insight > button:hover {
  transform: translateX(-3px);
  box-shadow: var(--shadow-xs);
}

.bottom-insight > button svg {
  width: 12px;
  height: 12px;
}

/* =========================================================
   STATES
========================================================= */

.state-card {
  width: min(100%, 900px);
  min-height: 360px;
  margin: 24px auto 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 28px;
  padding: 45px;
  border: 1px solid var(--line);
  border-radius: 29px;
  background: var(--surface);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(24px);
  text-align: right;
}

.state-content {
  max-width: 460px;
}

.state-kicker {
  display: block;
  margin-bottom: 8px;
  color: var(--primary);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 8px;
  font-weight: 950;
  letter-spacing: .12em;
}

.state-content h3 {
  margin: 0;
  color: var(--text);
  font-size: 22px;
  font-weight: 950;
  letter-spacing: -.035em;
}

.state-content p {
  margin: 8px 0 0;
  color: var(--text-muted);
  font-size: 10px;
  line-height: 2;
}

.loading-orbit {
  position: relative;
  flex: 0 0 auto;
  width: 130px;
  height: 130px;
  display: grid;
  place-items: center;
}

.loading-orbit > div {
  width: 62px;
  height: 62px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(115, 87, 255, .16);
  border-radius: 22px;
  color: var(--primary);
  background: rgba(115, 87, 255, .07);
  box-shadow: 0 20px 50px rgba(115, 87, 255, .12);
}

.loading-orbit > div svg {
  width: 28px;
  height: 28px;
  animation: spin 2s linear infinite;
}

.loading-orbit > span {
  position: absolute;
  border: 1px solid rgba(115, 87, 255, .18);
  border-radius: 999px;
}

.loading-orbit > span:nth-child(1) {
  inset: 5px;
  animation: orbitPulse 2.2s ease-in-out infinite;
}

.loading-orbit > span:nth-child(2) {
  inset: 20px;
  border-color: rgba(22, 183, 216, .15);
  animation: orbitPulse 2.2s ease-in-out infinite -.7s;
}

.loading-orbit > span:nth-child(3) {
  inset: 34px;
  border-color: rgba(168, 85, 247, .15);
  animation: orbitPulse 2.2s ease-in-out infinite -1.3s;
}

@keyframes orbitPulse {
  0%,
  100% {
    transform: scale(.92);
    opacity: .35;
  }
  50% {
    transform: scale(1.08);
    opacity: .9;
  }
}

.loading-lines {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 16px;
}

.loading-lines i {
  display: block;
  height: 5px;
  border-radius: 99px;
  background: linear-gradient(90deg, rgba(115, 87, 255, .12), rgba(115, 87, 255, .04));
  animation: loadingLine 1.4s ease-in-out infinite;
}

.loading-lines i:nth-child(1) {
  width: 100%;
}

.loading-lines i:nth-child(2) {
  width: 82%;
  animation-delay: -.15s;
}

.loading-lines i:nth-child(3) {
  width: 61%;
  animation-delay: -.3s;
}

@keyframes loadingLine {
  0%,
  100% {
    opacity: .4;
    transform: scaleX(.92);
    transform-origin: right;
  }
  50% {
    opacity: 1;
    transform: scaleX(1);
  }
}

.state-visual {
  position: relative;
  flex: 0 0 auto;
  width: 120px;
  height: 120px;
  display: grid;
  place-items: center;
  border-radius: 35px;
  background: rgba(115, 87, 255, .07);
}

.state-visual::before {
  content: "";
  position: absolute;
  inset: 12px;
  border: 1px dashed rgba(115, 87, 255, .18);
  border-radius: 28px;
  animation: spin 14s linear infinite;
}

.state-visual svg {
  position: relative;
  width: 42px;
  height: 42px;
  color: var(--primary);
  stroke-width: 1.4;
}

.state-visual.error {
  background: rgba(238, 91, 114, .07);
}

.state-visual.error::before {
  border-color: rgba(238, 91, 114, .16);
}

.state-visual.error svg {
  color: var(--red);
}

.state-button {
  margin-top: 16px;
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 14px;
  border: 1px solid rgba(115, 87, 255, .15);
  border-radius: 11px;
  color: #fff;
  background: linear-gradient(120deg, #6d4df8, #a855f7);
  box-shadow: 0 10px 25px rgba(109, 77, 248, .18);
  cursor: pointer;
  font-size: 9px;
  font-weight: 900;
  transition: .3s var(--ease-bounce);
}

.state-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 34px rgba(109, 77, 248, .25);
}

.state-button.secondary {
  color: var(--primary);
  background: rgba(115, 87, 255, .07);
  box-shadow: none;
}

.state-button svg {
  width: 14px;
  height: 14px;
}

.empty-illustration {
  position: relative;
  flex: 0 0 auto;
  width: 150px;
  height: 150px;
  display: grid;
  place-items: center;
}

.empty-orbit {
  position: absolute;
  inset: 10px;
  border: 1px dashed rgba(115, 87, 255, .18);
  border-radius: 999px;
  animation: spin 12s linear infinite;
}

.empty-paper {
  position: relative;
  width: 74px;
  height: 90px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(115, 87, 255, .15);
  border-radius: 17px;
  color: var(--primary);
  background: var(--surface-solid);
  box-shadow: 0 18px 40px rgba(38, 43, 80, .12);
  transform: rotate(-5deg);
}

.empty-paper svg {
  width: 33px;
  height: 33px;
}

.empty-spark {
  position: absolute;
  color: var(--primary);
  font-size: 16px;
  animation: sparkFloat 3s ease-in-out infinite alternate;
}

.spark-a {
  top: 18px;
  right: 8px;
}

.spark-b {
  bottom: 19px;
  left: 8px;
  animation-delay: -1.3s;
}

@keyframes sparkFloat {
  to {
    transform: translateY(-7px) rotate(10deg);
    opacity: .45;
  }
}

/* =========================================================
   SCROLL TOP
========================================================= */

.scroll-top {
  position: fixed;
  z-index: 70;
  right: 22px;
  bottom: 24px;
  width: 43px;
  height: 43px;
  display: grid;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 13px;
  color: var(--text);
  background: var(--surface);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(18px);
  cursor: pointer;
  transition: .3s var(--ease-bounce);
}

.scroll-top:hover {
  color: var(--primary);
  transform: translateY(-4px);
}

.scroll-top svg {
  width: 17px;
  height: 17px;
}

.float-enter-active,
.float-leave-active {
  transition:
    opacity .25s var(--ease),
    transform .35s var(--ease-bounce);
}

.float-enter-from,
.float-leave-to {
  opacity: 0;
  transform: translateY(15px) scale(.8);
}

/* =========================================================
   MODAL
========================================================= */

.modal-overlay,
.command-overlay {
  position: fixed;
  z-index: 200;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(9, 12, 22, .58);
  backdrop-filter: blur(18px) saturate(120%);
}

.exam-modal {
  position: relative;
  width: min(100%, 700px);
  max-height: min(900px, calc(100vh - 30px));
  overflow: auto;
  padding: 27px;
  border: 1px solid rgba(255, 255, 255, .15);
  border-radius: 31px;
  color: var(--text);
  background:
    radial-gradient(circle at 100% 0, rgba(115, 87, 255, .11), transparent 30%),
    radial-gradient(circle at 0 80%, rgba(22, 183, 216, .06), transparent 28%),
    var(--surface-solid);
  box-shadow:
    0 45px 120px rgba(0, 0, 0, .28),
    inset 0 1px 0 rgba(255, 255, 255, .32);
  scrollbar-width: thin;
}

.exam-modal::-webkit-scrollbar {
  width: 5px;
}

.exam-modal::-webkit-scrollbar-thumb {
  border-radius: 99px;
  background: rgba(115, 87, 255, .18);
}

.modal-backdrop-art {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.modal-backdrop-art span {
  position: absolute;
  border-radius: 999px;
  border: 1px solid rgba(115, 87, 255, .08);
}

.modal-backdrop-art span:nth-child(1) {
  width: 230px;
  height: 230px;
  right: -100px;
  top: -100px;
}

.modal-backdrop-art span:nth-child(2) {
  width: 350px;
  height: 350px;
  right: -160px;
  top: -160px;
}

.modal-backdrop-art span:nth-child(3) {
  width: 150px;
  height: 150px;
  left: -70px;
  bottom: -50px;
  border-color: rgba(22, 183, 216, .08);
}

.modal-close {
  position: absolute;
  z-index: 4;
  top: 17px;
  left: 17px;
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 11px;
  color: var(--text-muted);
  background: var(--surface-muted);
  cursor: pointer;
  transition: .3s var(--ease-bounce);
}

.modal-close:hover {
  color: var(--red);
  border-color: rgba(238, 91, 114, .16);
  background: rgba(238, 91, 114, .07);
  transform: rotate(5deg) scale(1.05);
}

.modal-close svg {
  width: 15px;
  height: 15px;
}

.modal-top {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 18px;
}

.modal-hero-icon {
  position: relative;
  z-index: 2;
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  margin-bottom: 13px;
  border: 1px solid rgba(115, 87, 255, .14);
  border-radius: 17px;
  color: var(--primary);
  background: rgba(115, 87, 255, .07);
  box-shadow: 0 15px 35px rgba(115, 87, 255, .08);
}

.modal-hero-icon svg {
  width: 27px;
  height: 27px;
}

.modal-heading {
  position: relative;
  z-index: 2;
}

.modal-heading > span {
  color: var(--text-muted);
  font-size: 8px;
  font-weight: 800;
}

.modal-heading h2 {
  margin: 5px 0 0;
  color: var(--text);
  font-size: 25px;
  font-weight: 950;
  letter-spacing: -.045em;
  line-height: 1.35;
}

.modal-description {
  max-width: 620px;
  margin: 7px 0 0;
  color: var(--text-muted);
  font-size: 9px;
  line-height: 1.9;
}

.modal-countdown {
  position: relative;
  z-index: 2;
  margin: 17px 0 10px;
  padding: 13px;
  border: 1px solid var(--line);
  border-radius: 15px;
  background: var(--surface-muted);
}

.modal-countdown > div:first-child {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.modal-countdown span {
  color: var(--text-muted);
  font-size: 8px;
  font-weight: 750;
}

.modal-countdown strong {
  color: var(--primary);
  font-size: 10px;
  font-weight: 950;
}

.modal-countdown-progress {
  position: relative;
  height: 4px;
  margin-top: 9px;
  overflow: hidden;
  border-radius: 99px;
  background: rgba(115, 87, 255, .08);
}

.modal-countdown-progress span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--primary), var(--primary-2), var(--cyan));
  transition: width .5s var(--ease);
}

.modal-date-grid {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 10px;
}

.modal-date-grid > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: var(--surface-muted);
}

.modal-date-grid span {
  color: var(--text-muted);
  font-size: 7px;
  font-weight: 750;
}

.modal-date-grid strong {
  color: var(--text);
  font-size: 9px;
  font-weight: 900;
}

.modal-date-grid small {
  color: var(--primary);
  font-size: 9px;
  font-weight: 950;
}

.modal-stats {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 7px;
  margin-top: 8px;
}

.modal-stats > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 11px;
  border: 1px solid var(--line);
  border-radius: 13px;
  background: rgba(115, 87, 255, .025);
}

.modal-stats span {
  color: var(--text-muted);
  font-size: 7px;
}

.modal-stats strong {
  color: var(--text);
  font-size: 10px;
  font-weight: 950;
}

.modal-booklets {
  position: relative;
  z-index: 2;
  margin-top: 12px;
  padding: 13px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface-muted);
}

.modal-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 9px;
}

.modal-section-header > div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.modal-section-header > div span {
  color: var(--text-muted);
  font-size: 7px;
}

.modal-section-header > div strong {
  color: var(--text);
  font-size: 9px;
  font-weight: 900;
}

.modal-section-header > span {
  color: var(--primary);
  font-size: 7px;
  font-weight: 900;
}

.modal-booklet {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px;
  border-radius: 10px;
  transition: .25s var(--ease);
}

.modal-booklet:hover {
  background: rgba(115, 87, 255, .05);
}

.modal-booklet-number {
  flex: 0 0 auto;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  color: var(--primary);
  background: rgba(115, 87, 255, .08);
  font-size: 8px;
  font-weight: 950;
}

.modal-booklet section {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.modal-booklet section strong {
  color: var(--text);
  font-size: 8px;
  font-weight: 900;
}

.modal-booklet section span {
  color: var(--text-soft);
  font-size: 7px;
  font-weight: 700;
}

.modal-booklet section small {
  color: var(--text-muted);
  font-size: 6px;
}

.modal-booklet section small b {
  margin: 0 3px;
}

.modal-no-booklets {
  position: relative;
  z-index: 2;
  margin-top: 11px;
  padding: 12px;
  border: 1px dashed var(--line-strong);
  border-radius: 12px;
  color: var(--text-muted);
  font-size: 8px;
}

.modal-actions {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 7px;
  margin-top: 16px;
}

.modal-secondary,
.modal-result,
.modal-primary {
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 0 15px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 9px;
  font-weight: 900;
  transition: .3s var(--ease-bounce);
}

.modal-secondary {
  color: var(--text-soft);
  border: 1px solid var(--line);
  background: var(--surface-muted);
}

.modal-result {
  color: var(--green);
  border: 1px solid rgba(34, 181, 115, .14);
  background: rgba(34, 181, 115, .07);
}

.modal-primary {
  color: #fff;
  border: 1px solid rgba(255, 255, 255, .2);
  background: linear-gradient(120deg, #6d4df8, #a855f7);
  box-shadow: 0 12px 28px rgba(109, 77, 248, .20);
}

.modal-secondary:hover,
.modal-result:hover,
.modal-primary:hover {
  transform: translateY(-3px);
}

.modal-primary svg {
  width: 14px;
  height: 14px;
}

/* =========================================================
   COMMAND PALETTE
========================================================= */

.command-overlay {
  z-index: 250;
}

.command-palette {
  width: min(100%, 610px);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, .14);
  border-radius: 24px;
  background: var(--surface-solid);
  box-shadow: 0 45px 120px rgba(0, 0, 0, .30);
}

.command-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  border-bottom: 1px solid var(--line);
  background:
    linear-gradient(100deg, rgba(115, 87, 255, .055), transparent);
}

.command-search-icon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 11px;
  color: var(--primary);
  background: rgba(115, 87, 255, .08);
}

.command-search-icon svg {
  width: 18px;
  height: 18px;
}

.command-header > div:nth-child(2) {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.command-header > div:nth-child(2) span {
  color: var(--text-muted);
  font-size: 7px;
  font-weight: 800;
}

.command-header > div:nth-child(2) strong {
  color: var(--text);
  font-size: 10px;
  font-weight: 950;
}

.command-header > button {
  margin-right: auto;
  padding: 5px 7px;
  border: 1px solid var(--line);
  border-radius: 7px;
  color: var(--text-muted);
  background: var(--surface-muted);
  cursor: pointer;
  font-size: 8px;
  font-weight: 800;
}

.command-list {
  display: flex;
  flex-direction: column;
  padding: 8px;
}

.command-list > button {
  min-height: 58px;
  display: grid;
  grid-template-columns: 37px minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 7px;
  border-radius: 13px;
  color: var(--text);
  background: transparent;
  text-align: right;
  cursor: pointer;
  transition: .25s var(--ease);
}

.command-list > button:hover {
  background: rgba(115, 87, 255, .055);
}

.command-list-icon {
  width: 37px;
  height: 37px;
  display: grid;
  place-items: center;
  border-radius: 11px;
  color: var(--primary);
  background: rgba(115, 87, 255, .07);
}

.command-list-icon svg {
  width: 17px;
  height: 17px;
}

.command-list > button > span:nth-child(2) {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.command-list strong {
  font-size: 9px;
  font-weight: 900;
}

.command-list small {
  color: var(--text-muted);
  font-size: 7px;
}

.command-list kbd {
  min-width: 28px;
  height: 24px;
  display: grid;
  place-items: center;
  padding: 0 6px;
  border: 1px solid var(--line);
  border-bottom-width: 2px;
  border-radius: 7px;
  color: var(--text-muted);
  background: var(--surface-muted);
  font-size: 8px;
}

/* =========================================================
   KEYBOARD MODAL
========================================================= */

.keyboard-modal {
  position: relative;
  width: min(100%, 500px);
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, .12);
  border-radius: 27px;
  background: var(--surface-solid);
  box-shadow: 0 45px 120px rgba(0, 0, 0, .30);
}

.keyboard-modal h2 {
  margin: 0;
  color: var(--text);
  font-size: 23px;
  font-weight: 950;
}

.keyboard-modal > p {
  margin: 6px 0 20px;
  color: var(--text-muted);
  font-size: 9px;
}

.shortcut-grid {
  display: grid;
  gap: 7px;
}

.shortcut-grid > div {
  min-height: 47px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px;
  border: 1px solid var(--line);
  border-radius: 11px;
  background: var(--surface-muted);
}

.shortcut-grid kbd {
  min-width: 55px;
  height: 29px;
  display: grid;
  place-items: center;
  padding: 0 7px;
  border: 1px solid var(--line-strong);
  border-bottom-width: 2px;
  border-radius: 8px;
  color: var(--primary);
  background: var(--surface-solid);
  font-size: 8px;
  font-weight: 900;
}

.shortcut-grid span {
  color: var(--text-soft);
  font-size: 9px;
  font-weight: 750;
}

/* =========================================================
   MODAL TRANSITIONS
========================================================= */

.modal-enter-active,
.modal-leave-active,
.command-enter-active,
.command-leave-active {
  transition:
    opacity .3s var(--ease),
    backdrop-filter .3s var(--ease);
}

.modal-enter-active .exam-modal,
.modal-leave-active .exam-modal,
.command-enter-active .command-palette,
.command-leave-active .command-palette,
.command-enter-active .keyboard-modal,
.command-leave-active .keyboard-modal {
  transition:
    transform .4s var(--ease-bounce),
    opacity .3s var(--ease);
}

.modal-enter-from,
.modal-leave-to,
.command-enter-from,
.command-leave-to {
  opacity: 0;
}

.modal-enter-from .exam-modal,
.modal-leave-to .exam-modal {
  opacity: 0;
  transform: translateY(28px) scale(.96);
}

.command-enter-from .command-palette,
.command-leave-to .command-palette,
.command-enter-from .keyboard-modal,
.command-leave-to .keyboard-modal {
  opacity: 0;
  transform: translateY(18px) scale(.96);
}

/* =========================================================
   ACCENTS
========================================================= */

.accent-maz .card-ambient {
  background: rgba(223, 88, 115, .10);
}

.accent-kanoon .card-ambient {
  background: rgba(61, 127, 232, .10);
}

.accent-kheilisabz .card-ambient {
  background: rgba(26, 169, 119, .10);
}

.accent-dopamine .card-ambient {
  background: rgba(152, 87, 245, .11);
}

.accent-maz .card-progress-line {
  background:
    linear-gradient(90deg, transparent, rgba(223, 88, 115, .7), rgba(245, 124, 148, .75));
}

.accent-kanoon .card-progress-line {
  background:
    linear-gradient(90deg, transparent, rgba(61, 127, 232, .7), rgba(92, 155, 255, .75));
}

.accent-kheilisabz .card-progress-line {
  background:
    linear-gradient(90deg, transparent, rgba(26, 169, 119, .7), rgba(55, 205, 152, .75));
}

.accent-dopamine .card-progress-line {
  background:
    linear-gradient(90deg, transparent, rgba(152, 87, 245, .7), rgba(195, 133, 255, .75));
}

.is-running .card-ambient {
  animation: runningAmbient 4s ease-in-out infinite alternate;
}

@keyframes runningAmbient {
  from {
    opacity: .55;
    transform: scale(.95);
  }
  to {
    opacity: 1;
    transform: scale(1.15);
  }
}

.is-ended {
  opacity: .88;
}

.is-ended:hover {
  opacity: 1;
}

/* =========================================================
   RESPONSIVE — LARGE
========================================================= */

@media (max-width: 1250px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .exam-grid {
    grid-template-columns: 1fr;
  }

  .exam-grid.list-view .exam-card {
    grid-template-columns: 1fr;
  }

  .exam-grid.list-view .exam-card > .exam-heading,
  .exam-grid.list-view .exam-card > .exam-live-panel,
  .exam-grid.list-view .exam-card > .exam-date {
    grid-column: 1;
    grid-row: auto;
  }

  .exam-grid.list-view .exam-card > .exam-heading {
    padding-left: 0;
  }

  .exam-grid.list-view .exam-card > .exam-info-grid,
  .exam-grid.list-view .exam-card > .booklets,
  .exam-grid.list-view .exam-card > .no-booklets,
  .exam-grid.list-view .exam-card > .attempt-banner,
  .exam-grid.list-view .exam-card > .result-banner,
  .exam-grid.list-view .exam-card > .card-expanded-panel,
  .exam-grid.list-view .exam-card > .exam-footer {
    grid-column: 1;
    grid-row: auto;
  }
}

@media (max-width: 900px) {
  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .refresh-button {
    flex: 1;
  }

  .discovery-controls {
    grid-template-columns: 1fr 1fr;
  }

  .search-box {
    grid-column: 1 / -1;
  }

  .advanced-filters {
    grid-template-columns: 1fr;
  }

  .availability-toggle {
    min-width: 0;
  }
}

/* =========================================================
   RESPONSIVE — TABLET
========================================================= */

@media (max-width: 700px) {
  .exams-page {
    padding: 12px 10px 80px;
  }

  .command-fab {
    left: 12px;
    bottom: 14px;
    width: 50px;
    height: 50px;
    border-radius: 16px;
  }

  .command-fab kbd {
    display: none;
  }

  .page-header {
    min-height: 0;
    margin-bottom: 10px;
    padding: 22px 18px;
    border-radius: 24px;
  }

  .header-main {
    width: 100%;
    gap: 14px;
  }

  .header-icon-shell {
    width: 62px;
    height: 62px;
  }

  .header-icon {
    width: 54px;
    height: 54px;
    border-radius: 18px;
  }

  .header-icon svg {
    width: 27px;
    height: 27px;
  }

  .header-copy h1 {
    font-size: 27px;
  }

  .header-copy p {
    font-size: 9px;
    line-height: 1.9;
  }

  .hero-meta {
    margin-top: 9px;
  }

  .hero-meta span {
    font-size: 8px;
  }

  .header-actions {
    gap: 7px;
  }

  .refresh-button {
    min-height: 41px;
  }

  .help-button {
    width: 41px;
    min-height: 41px;
  }

  .command-strip {
    min-height: 58px;
    padding: 7px;
    border-radius: 16px;
  }

  .shortcut-hint {
    display: none;
  }

  .command-kicker {
    display: none;
  }

  .quick-filter {
    min-height: 40px;
    padding: 0 10px;
  }

  .stats-grid {
    gap: 8px;
    margin-bottom: 10px;
  }

  .stat-card {
    min-height: 102px;
    padding: 13px;
    border-radius: 17px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
  }

  .stat-icon svg {
    width: 18px;
    height: 18px;
  }

  .stat-copy strong {
    font-size: 19px;
  }

  .discovery-panel,
  .filters-section {
    padding: 16px;
    border-radius: 20px;
  }

  .discovery-top {
    align-items: flex-start;
  }

  .discovery-title h2 {
    font-size: 17px;
  }

  .discovery-title p {
    font-size: 8px;
  }

  .view-switcher {
    display: none;
  }

  .discovery-controls {
    grid-template-columns: 1fr 1fr;
  }

  .sort-box,
  .filter-toggle {
    min-width: 0;
  }

  .filter-toggle span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .filters-section {
    margin-bottom: 10px;
  }

  .section-heading strong {
    font-size: 14px;
  }

  .category-tab {
    min-height: 43px;
  }

  .results-toolbar {
    padding: 0 2px;
  }

  .exam-card {
    padding: 15px;
    border-radius: 21px;
  }

  .exam-heading h2 {
    font-size: 17px;
  }

  .exam-info-grid {
    grid-template-columns: 1fr 1fr;
  }

  .exam-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .footer-message {
    width: 100%;
  }

  .footer-actions {
    width: 100%;
  }

  .footer-actions > button:not(.expand-button) {
    flex: 1;
  }

  .expand-button {
    flex: 0 0 34px !important;
  }

  .bottom-insight {
    align-items: flex-start;
    flex-wrap: wrap;
    padding: 12px;
  }

  .bottom-insight > button {
    width: 100%;
    justify-content: center;
    margin-right: 0;
  }

  .state-card {
    flex-direction: column;
    min-height: 340px;
    padding: 30px 18px;
    text-align: center;
  }

  .state-content {
    max-width: 100%;
  }

  .state-content h3 {
    font-size: 19px;
  }

  .exam-modal {
    max-height: calc(100vh - 20px);
    padding: 20px;
    border-radius: 23px;
  }

  .modal-heading h2 {
    font-size: 20px;
  }

  .modal-actions {
    flex-wrap: wrap;
  }

  .modal-actions > button {
    flex: 1;
  }
}

/* =========================================================
   RESPONSIVE — PHONE
========================================================= */

@media (max-width: 430px) {
  .exams-page {
    padding-right: 7px;
    padding-left: 7px;
  }

  .page-header {
    padding: 18px 14px;
  }

  .header-main {
    align-items: flex-start;
  }

  .header-icon-shell {
    width: 51px;
    height: 51px;
  }

  .header-icon {
    width: 45px;
    height: 45px;
    border-radius: 14px;
  }

  .header-icon svg {
    width: 22px;
    height: 22px;
  }

  .header-copy h1 {
    font-size: 23px;
  }

  .header-copy p {
    margin-top: 7px;
    font-size: 8px;
  }

  .hero-meta {
    display: none;
  }

  .hero-eyebrow {
    font-size: 8px;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .stat-card {
    gap: 8px;
    min-height: 91px;
    padding: 10px;
  }

  .stat-card .stat-icon {
    width: 34px;
    height: 34px;
  }

  .stat-copy span {
    font-size: 7px;
  }

  .stat-copy strong {
    font-size: 16px;
  }

  .stat-copy small {
    font-size: 6px;
  }

  .completion-ring {
    left: 8px;
    top: 8px;
    width: 30px;
    height: 30px;
  }

  .completion-ring span {
    font-size: 6px;
  }

  .stat-mini-chart,
  .live-indicator {
    display: none;
  }

  .discovery-controls {
    grid-template-columns: 1fr;
  }

  .search-box {
    grid-column: auto;
  }

  .sort-box,
  .filter-toggle {
    width: 100%;
  }

  .exam-live-panel {
    min-height: 57px;
  }

  .mini-progress {
    max-width: 55px;
  }

  .date-relative {
    display: none;
  }

  .exam-info {
    min-height: 54px;
  }

  .exam-info strong {
    font-size: 7px;
  }

  .booklet-title span {
    display: none;
  }

  .footer-actions {
    gap: 4px;
  }

  .details-button,
  .result-button,
  .start-button,
  .disabled-button,
  .expand-button {
    min-height: 36px;
    padding-right: 7px;
    padding-left: 7px;
    font-size: 7px;
  }

  .start-button {
    min-width: 0;
  }

  .exam-modal {
    padding: 17px;
  }

  .modal-top {
    margin-left: 35px;
  }

  .modal-date-grid,
  .modal-stats {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }

  .modal-actions > button {
    width: 100%;
  }

  .command-palette,
  .keyboard-modal {
    border-radius: 20px;
  }

  .command-list > button {
    min-height: 54px;
  }

  .shortcut-grid kbd {
    min-width: 48px;
  }
}

/* =========================================================
   ACCESSIBILITY
========================================================= */

@media (prefers-reduced-motion: reduce) {
  .exams-page *,
  .exams-page *::before,
  .exams-page *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: .01ms !important;
  }
}

@media (prefers-contrast: more) {
  .exams-page {
    --line: rgba(20, 27, 52, .18);
    --line-strong: rgba(20, 27, 52, .28);
  }

  .is-dark {
    --line: rgba(255, 255, 255, .18);
    --line-strong: rgba(255, 255, 255, .28);
  }

  .exam-card,
  .stat-card,
  .filters-section,
  .discovery-panel {
    border-width: 1.5px;
  }
}

/* =========================================================
   PRINT
========================================================= */

@media print {
  .exams-page {
    padding: 0;
    background: #fff;
  }

  .aurora-field,
  .command-fab,
  .header-actions,
  .command-strip,
  .discovery-panel,
  .bottom-insight,
  .scroll-top,
  .modal-overlay,
  .command-overlay {
    display: none !important;
  }

  .page-header,
  .stats-grid,
  .filters-section,
  .exam-grid {
    width: 100%;
  }

  .page-header,
  .stat-card,
  .filters-section,
  .exam-card {
    box-shadow: none;
    break-inside: avoid;
  }

  .exam-grid {
    grid-template-columns: 1fr 1fr;
  }
}
/* =========================================================
   MICRO-INTERACTIONS / FINE GRAINED STATES
========================================================= */

.exam-card.is-favorite {
  border-color: rgba(238, 91, 114, .10);
}

.exam-card.is-favorite .card-ambient {
  background: rgba(238, 91, 114, .06);
}

.exam-card.is-expanded {
  box-shadow: 0 24px 65px rgba(115, 87, 255, .12);
}

.exam-card:focus-within .card-corner {
  border-color: rgba(115, 87, 255, .28);
}

.exam-card:focus-within {
  border-color: rgba(115, 87, 255, .20);
}

.exam-card .provider-badge,
.exam-card .status-badge,
.exam-card .favorite-button,
.exam-card .details-button,
.exam-card .result-button,
.exam-card .start-button,
.exam-card .disabled-button,
.exam-card .expand-button {
  will-change: transform;
}

.exam-card .exam-heading h2 {
  transition: color .25s var(--ease);
}

.exam-card:hover .exam-heading h2 {
  color: color-mix(in srgb, var(--text) 86%, var(--primary));
}

.exam-card .info-icon {
  transition:
    transform .35s var(--ease-bounce),
    box-shadow .35s var(--ease);
}

.exam-info:hover .info-icon {
  transform: rotate(-5deg) scale(1.06);
  box-shadow: 0 7px 18px rgba(115, 87, 255, .08);
}

.exam-card .provider-badge span {
  transition: transform .3s var(--ease-bounce);
}

.exam-card:hover .provider-badge span {
  transform: scale(1.35);
}

.exam-card .status-badge i {
  transition: transform .3s var(--ease-bounce);
}

.exam-card:hover .status-badge i {
  transform: scale(1.4);
}

.exam-card .date-icon {
  transition:
    transform .4s var(--ease-bounce),
    box-shadow .4s var(--ease);
}

.exam-card:hover .date-icon {
  transform: rotate(-4deg) translateY(-2px);
  box-shadow: 0 9px 22px rgba(115, 87, 255, .10);
}

.exam-card .booklet-number {
  transition:
    transform .3s var(--ease-bounce),
    background .3s var(--ease);
}

.booklet:hover .booklet-number {
  transform: scale(1.07);
  background: rgba(115, 87, 255, .12);
}

.exam-card .footer-status-dot {
  transition: transform .3s var(--ease-bounce);
}

.exam-card:hover .footer-status-dot {
  transform: scale(1.25);
}

.is-dark .exam-card .exam-date {
  background:
    linear-gradient(120deg, rgba(115, 87, 255, .065), transparent 55%),
    rgba(255, 255, 255, .025);
}

.is-dark .exam-card .exam-live-panel {
  background: rgba(255, 255, 255, .022);
}

.is-dark .exam-card .exam-info {
  background: rgba(255, 255, 255, .015);
}

.is-dark .exam-card .booklets {
  background: rgba(255, 255, 255, .012);
}

.is-dark .search-box,
.is-dark .sort-box,
.is-dark .filter-toggle,
.is-dark .view-switcher {
  background: rgba(255, 255, 255, .025);
}

.is-dark .search-box:focus-within {
  background: rgba(255, 255, 255, .045);
}

.is-dark .category-tab {
  background: rgba(255, 255, 255, .025);
}

.is-dark .category-tab.active {
  background: rgba(115, 87, 255, .11);
}

.is-dark .stat-card {
  background:
    linear-gradient(145deg, rgba(30, 35, 54, .75), rgba(16, 20, 32, .66)),
    var(--surface);
}

.is-dark .stat-card:hover {
  border-color: rgba(115, 87, 255, .22);
}

.is-dark .bottom-insight {
  background:
    linear-gradient(105deg, rgba(115, 87, 255, .10), rgba(22, 183, 216, .045)),
    var(--surface);
}

.is-dark .state-card {
  background:
    linear-gradient(145deg, rgba(27, 32, 49, .76), rgba(15, 19, 31, .68)),
    var(--surface);
}

.is-dark .exam-modal,
.is-dark .command-palette,
.is-dark .keyboard-modal {
  box-shadow:
    0 45px 120px rgba(0, 0, 0, .52),
    inset 0 1px 0 rgba(255, 255, 255, .04);
}

.is-dark .modal-close,
.is-dark .command-header > button,
.is-dark .shortcut-grid kbd {
  background: rgba(255, 255, 255, .035);
}

.is-dark .modal-date-grid > div,
.is-dark .modal-stats > div,
.is-dark .modal-booklets {
  background: rgba(255, 255, 255, .025);
}

.is-dark .command-list > button:hover {
  background: rgba(115, 87, 255, .08);
}

@media (hover: none) {
  .exam-card:hover {
    transform: none;
    box-shadow: var(--shadow-sm);
  }

  .stat-card:hover {
    transform: none;
    box-shadow: var(--shadow-sm);
  }

  .quick-filter:hover,
  .category-tab:hover,
  .bottom-insight > button:hover {
    transform: none;
  }

  .start-button:hover,
  .details-button:hover,
  .result-button:hover,
  .expand-button:hover {
    transform: none;
  }

  .exam-card:hover .card-ambient {
    transform: none;
  }
}

@media (max-width: 560px) {
  .command-strip-left {
    width: 100%;
  }

  .quick-filter {
    padding-right: 8px;
    padding-left: 8px;
  }

  .quick-filter-icon {
    width: 18px;
  }

  .quick-filter span:last-child {
    font-size: 8px;
  }

  .exam-card {
    animation-delay: 0ms;
  }

  .card-top {
    margin-bottom: 13px;
  }

  .card-top-actions {
    gap: 4px;
  }

  .provider-badge,
  .status-badge {
    min-height: 24px;
    padding-right: 7px;
    padding-left: 7px;
    font-size: 7px;
  }

  .favorite-button {
    width: 27px;
    height: 27px;
  }

  .exam-heading {
    margin-bottom: 12px;
  }

  .exam-heading h2 {
    font-size: 16px;
  }

  .exam-heading p {
    font-size: 8px;
  }

  .exam-live-panel {
    gap: 7px;
    padding: 8px;
  }

  .live-panel-icon {
    width: 32px;
    height: 32px;
  }

  .live-panel-copy strong {
    font-size: 9px;
  }

  .exam-date {
    min-height: 68px;
    padding: 9px;
  }

  .date-icon {
    width: 34px;
    height: 34px;
  }

  .date-content > strong {
    font-size: 8px;
  }

  .exam-info-grid {
    gap: 5px;
  }

  .exam-info {
    gap: 5px;
    padding: 6px;
  }

  .info-icon {
    width: 24px;
    height: 24px;
  }

  .exam-info small {
    font-size: 6px;
  }

  .exam-info strong {
    font-size: 7px;
  }

  .booklets {
    padding: 9px;
  }

  .attempt-banner,
  .result-banner {
    min-height: 50px;
  }

  .attempt-banner strong,
  .result-banner strong {
    font-size: 7px;
  }

  .attempt-banner span,
  .result-banner span {
    font-size: 6px;
  }

  .bottom-insight > div:nth-child(2) strong {
    font-size: 8px;
    line-height: 1.8;
  }
}


.exam-footer svg {
  width: 18px;
  height: 18px;
  flex: 0 0 18px;
  display: block;
  stroke-width: 1.8;
}

</style>
