<template>
  <div
    class="exam-result-page"
    :class="{ 'is-dark': isDark }"
    dir="rtl"
  >
    <!-- =====================================================
         LOADING
    ====================================================== -->

    <div v-if="loading" class="page-state">
      <div class="loading-orb">
        <span></span>
        <span></span>
        <span></span>
      </div>

      <h2>در حال آماده‌سازی کارنامه</h2>
      <p>
        نتایج و تحلیل عملکرد شما در حال دریافت است...
      </p>
    </div>


    <!-- =====================================================
         ERROR
    ====================================================== -->

    <div
      v-else-if="errorMessage"
      class="page-state error-state"
    >
      <div class="state-icon error">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M12 3 2.8 19a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L12 3Z"/>
          <path d="M12 9v4"/>
          <path d="M12 17h.01"/>
        </svg>
      </div>

      <h2>دریافت کارنامه ناموفق بود</h2>

      <p>{{ errorMessage }}</p>

      <button
        type="button"
        class="retry-button"
        @click="loadResult"
      >
        تلاش دوباره
      </button>
    </div>


    <!-- =====================================================
         MAIN
    ====================================================== -->

    <main
      v-else-if="result"
      class="result-container"
    >

      <!-- ===================================================
           HERO
      ==================================================== -->

      <section class="hero-card">

        <div class="hero-glow glow-one"></div>
        <div class="hero-glow glow-two"></div>

        <div class="hero-content">

          <div class="hero-user">

            <div class="avatar-wrap">

              <img
                v-if="result.user?.profile_image"
                :src="result.user.profile_image"
                alt="تصویر کاربر"
                class="avatar-image"
              />

              <div
                v-else
                class="avatar-fallback"
              >
                {{ userInitials }}
              </div>

              <div class="avatar-status"></div>

            </div>


            <div class="hero-user-info">

              <span class="hero-eyebrow">
                کارنامه آزمون
              </span>

              <h1>
                {{ result.exam?.title || 'آزمون' }}
              </h1>

              <p>
                {{ result.user?.full_name || result.user?.username || 'دانش‌آموز' }}
              </p>

            </div>

          </div>


          <div class="hero-score">

            <div class="score-ring">

              <svg
                viewBox="0 0 120 120"
                class="score-svg"
              >
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  class="score-track"
                />

                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  class="score-progress"
                  :stroke-dasharray="scoreDash"
                  stroke-dashoffset="0"
                />
              </svg>

              <div class="score-center">

                <strong>
                  {{ formatPercent(result.summary?.percentage) }}
                </strong>

                <span>
                  درصد
                </span>

              </div>

            </div>

            <div class="score-caption">
              درصد با نمره منفی
            </div>

          </div>

        </div>


        <div class="hero-bottom">

          <div class="hero-meta">

            <span class="hero-meta-dot"></span>

            <span>
              {{
                result.is_final
                  ? 'کارنامه نهایی'
                  : 'کارنامه اولیه'
              }}
            </span>

          </div>

          <div class="hero-meta">

            <span>
              {{ formatDate(result.exam?.start_at) }}
            </span>

            <span class="meta-separator">•</span>

            <span>
              {{ formatTime(result.exam?.start_at) }}
            </span>

          </div>

        </div>

      </section>


      <!-- ===================================================
           TABS
      ==================================================== -->

      <nav class="result-tabs">

        <button
          type="button"
          class="result-tab"
          :class="{ active: activeTab === 'overview' }"
          @click="activeTab = 'overview'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </span>

          <span>خلاصه کارنامه</span>
        </button>


        <button
          type="button"
          class="result-tab"
          :class="{ active: activeTab === 'booklets' }"
          @click="activeTab = 'booklets'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 4.5A2.5 2.5 0 0 1 7.5 2H20v17H7.5A2.5 2.5 0 0 0 5 21.5v-17Z"/>
              <path d="M5 4.5V21.5"/>
              <path d="M9 7h7"/>
              <path d="M9 11h7"/>
              <path d="M9 15h4"/>
            </svg>
          </span>

          <span>دفترچه‌ها</span>

          <small>
            {{ toPersianNumber(result.booklets?.length || 0) }}
          </small>
        </button>


        <button
          type="button"
          class="result-tab"
          :class="{ active: activeTab === 'analytics' }"
          @click="activeTab = 'analytics'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 19V5"/>
              <path d="M4 19h16"/>
              <path d="m7 15 3-4 3 2 5-7"/>
            </svg>
          </span>

          <span>تحلیل و نمودارها</span>
        </button>


        <button
          type="button"
          class="result-tab review-tab"
          :class="{ active: activeTab === 'review' }"
          @click="activeTab = 'review'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 4h16v16H4z"/>
              <path d="M8 8h8"/>
              <path d="M8 12h8"/>
              <path d="M8 16h5"/>
            </svg>
          </span>

          <span>مرور شخصی‌سازی‌شده</span>

          <small>
            {{ toPersianNumber(result.personalized_review?.length || 0) }}
          </small>
        </button>

      </nav>


      <!-- ===================================================
           TAB: OVERVIEW
      ==================================================== -->

      <section
        v-if="activeTab === 'overview'"
        class="tab-content"
      >

        <!-- Summary stats -->

        <div class="summary-grid">

          <div class="metric-card score-metric">

            <div class="metric-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 3v18"/>
                <path d="M5 8h14"/>
                <path d="M5 16h14"/>
              </svg>
            </div>

            <div class="metric-content">

              <span>درصد نهایی</span>

              <strong>
                {{ formatPercent(result.summary?.percentage) }}٪
              </strong>

              <small>
                با نمره منفی
              </small>

            </div>

          </div>


          <div class="metric-card">

            <div class="metric-icon correct">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m5 12 4 4L19 6"/>
              </svg>
            </div>

            <div class="metric-content">

              <span>پاسخ درست</span>

              <strong>
                {{ toPersianNumber(result.summary?.correct_count || 0) }}
              </strong>

              <small>
                سؤال
              </small>

            </div>

          </div>


          <div class="metric-card">

            <div class="metric-icon wrong">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m7 7 10 10"/>
                <path d="m17 7-10 10"/>
              </svg>
            </div>

            <div class="metric-content">

              <span>پاسخ غلط</span>

              <strong>
                {{ toPersianNumber(result.summary?.wrong_count || 0) }}
              </strong>

              <small>
                سؤال
              </small>

            </div>

          </div>


          <div class="metric-card">

            <div class="metric-icon unanswered">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/>
                <path d="M8 12h8"/>
              </svg>
            </div>

            <div class="metric-content">

              <span>نزده</span>

              <strong>
                {{ toPersianNumber(result.summary?.unanswered_count || 0) }}
              </strong>

              <small>
                سؤال
              </small>

            </div>

          </div>

        </div>


        <!-- Ranking -->

        <section class="panel ranking-panel">

          <div class="panel-heading">

            <div>
              <span>جایگاه شما</span>
              <h2>رتبه‌بندی</h2>
            </div>

            <div class="ranking-crown">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m3 6 4 4 5-7 5 7 4-4-2 13H5L3 6Z"/>
                <path d="M5 19h14"/>
              </svg>
            </div>

          </div>


          <div class="ranking-grid">

            <div class="rank-card national">

              <div class="rank-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="9"/>
                  <path d="M3 12h18"/>
                  <path d="M12 3c2.5 2.5 2.5 15.5 0 18"/>
                  <path d="M12 3c-2.5 2.5-2.5 15.5 0 18"/>
                </svg>
              </div>

              <div class="rank-card-copy">

                <span>رتبه کشوری</span>

                <strong>
                  {{ formatRank(result.ranking?.national_rank) }}
                </strong>

                <small>
                  از
                  {{ toPersianNumber(result.ranking?.national_participants || 0) }}
                  شرکت‌کننده
                </small>

              </div>

            </div>


            <div class="rank-card province">

              <div class="rank-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Z"/>
                  <circle cx="12" cy="9" r="2.5"/>
                </svg>
              </div>

              <div class="rank-card-copy">

                <span>
                  رتبه استانی
                  <template v-if="result.ranking?.province">
                    — {{ result.ranking.province }}
                  </template>
                </span>

                <strong>
                  {{ formatRank(result.ranking?.provincial_rank) }}
                </strong>

                <small>
                  از
                  {{ toPersianNumber(result.ranking?.provincial_participants || 0) }}
                  شرکت‌کننده
                </small>

              </div>

            </div>

          </div>

        </section>


        <!-- Raw score -->

        <section class="panel raw-score-panel">

          <div class="panel-heading">

            <div>
              <span>دو نگاه به عملکرد</span>
              <h2>درصد خام و درصد با نمره منفی</h2>
            </div>

          </div>


          <div class="raw-comparison">

            <div class="raw-item">

              <div class="raw-label">
                <span>درصد با نمره منفی</span>

                <strong>
                  {{ formatPercent(result.summary?.percentage) }}٪
                </strong>
              </div>

              <div class="progress-track">

                <div
                  class="progress-fill negative"
                  :style="{
                    width: clampPercent(result.summary?.percentage) + '%'
                  }"
                ></div>

              </div>

              <small>
                معیار اصلی رتبه‌بندی
              </small>

            </div>


            <div class="raw-item">

              <div class="raw-label">
                <span>درصد خام</span>

                <strong>
                  {{ formatPercent(result.summary?.raw_percentage) }}٪
                </strong>
              </div>

              <div class="progress-track">

                <div
                  class="progress-fill raw"
                  :style="{
                    width: clampPercent(result.summary?.raw_percentage) + '%'
                  }"
                ></div>

              </div>

              <small>
                بدون اعمال نمره منفی
              </small>

            </div>

          </div>

        </section>


        <!-- Previous attempt -->

        <section
          v-if="result.previous_attempt"
          class="panel previous-panel"
        >

          <div class="panel-heading">

            <div>
              <span>مقایسه با آزمون قبلی</span>
              <h2>
                {{ result.previous_attempt.exam_title }}
              </h2>
            </div>

            <div
              class="change-badge"
              :class="changeClass(result.previous_attempt.score_change)"
            >
              {{ signedPercent(result.previous_attempt.score_change) }}
            </div>

          </div>


          <div class="previous-content">

            <div class="previous-score">

              <span>آزمون قبلی</span>

              <strong>
                {{ formatPercent(result.previous_attempt.score) }}٪
              </strong>

            </div>


            <div class="change-arrow">

              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 12h14"/>
                <path d="m13 6 6 6-6 6"/>
              </svg>

            </div>


            <div class="previous-score current">

              <span>این آزمون</span>

              <strong>
                {{ formatPercent(result.summary?.percentage) }}٪
              </strong>

            </div>

          </div>


          <div class="previous-details">

            <div>
              <span>تغییر درصد</span>
              <strong
                :class="changeTextClass(result.previous_attempt.score_change)"
              >
                {{ signedPercent(result.previous_attempt.score_change) }}٪
              </strong>
            </div>

            <div>
              <span>تغییر درصد خام</span>
              <strong
                :class="changeTextClass(result.previous_attempt.raw_score_change)"
              >
                {{ signedPercent(result.previous_attempt.raw_score_change) }}٪
              </strong>
            </div>

            <div>
              <span>درست قبلی</span>
              <strong>
                {{ toPersianNumber(result.previous_attempt.correct || 0) }}
              </strong>
            </div>

            <div>
              <span>غلط قبلی</span>
              <strong>
                {{ toPersianNumber(result.previous_attempt.wrong || 0) }}
              </strong>
            </div>

          </div>

        </section>

      </section>


      <!-- ===================================================
           TAB: BOOKLETS
      ==================================================== -->

      <section
        v-if="activeTab === 'booklets'"
        class="tab-content"
      >

        <div class="section-intro">

          <div>
            <span>تحلیل تفکیکی</span>
            <h2>عملکرد در دفترچه‌ها</h2>
            <p>
              عملکرد هر دفترچه را جداگانه بررسی کن و نقاط قوت و ضعف خودت را پیدا کن.
            </p>
          </div>

          <div class="booklet-total">

            <strong>
              {{ toPersianNumber(result.booklets?.length || 0) }}
            </strong>

            <span>
              دفترچه
            </span>

          </div>

        </div>


        <div class="booklet-cards">

          <article
            v-for="booklet in sortedBooklets"
            :key="booklet.id"
            class="booklet-card"
          >

            <div class="booklet-card-top">

              <div class="booklet-number">
                {{ toPersianNumber(booklet.order) }}
              </div>

              <div class="booklet-title-wrap">

                <span>
                  {{ booklet.subject || 'درس' }}
                </span>

                <h3>
                  {{ booklet.title }}
                </h3>

              </div>

              <div class="decile-badge">
                <span>دهک</span>
                <strong>
                  {{ toPersianNumber(booklet.decile || 0) }}
                </strong>
              </div>

            </div>


            <div class="booklet-score-row">

              <div class="booklet-score">

                <strong>
                  {{ formatPercent(booklet.percentage) }}٪
                </strong>

                <span>
                  درصد با نمره منفی
                </span>

              </div>

              <div class="booklet-raw">

                <span>خام</span>

                <strong>
                  {{ formatPercent(booklet.raw_percentage) }}٪
                </strong>

              </div>

            </div>


            <div class="booklet-bar">

              <div
                class="booklet-bar-fill"
                :style="{
                  width: positivePercent(booklet.percentage) + '%'
                }"
              ></div>

            </div>


            <div class="answer-breakdown">

              <div class="answer-stat correct">

                <span class="answer-dot"></span>

                <span>درست</span>

                <strong>
                  {{ toPersianNumber(booklet.correct) }}
                </strong>

              </div>


              <div class="answer-stat wrong">

                <span class="answer-dot"></span>

                <span>غلط</span>

                <strong>
                  {{ toPersianNumber(booklet.wrong) }}
                </strong>

              </div>


              <div class="answer-stat unanswered">

                <span class="answer-dot"></span>

                <span>نزده</span>

                <strong>
                  {{ toPersianNumber(booklet.unanswered) }}
                </strong>

              </div>

            </div>


            <div class="booklet-ranks">

              <div>

                <span>رتبه کشوری</span>

                <strong>
                  {{ formatRank(booklet.national_rank) }}
                </strong>

                <small>
                  از {{ toPersianNumber(booklet.national_participants) }}
                </small>

              </div>


              <div>

                <span>رتبه استانی</span>

                <strong>
                  {{ formatRank(booklet.provincial_rank) }}
                </strong>

                <small>
                  از {{ toPersianNumber(booklet.provincial_participants) }}
                </small>

              </div>

            </div>


            <div class="booklet-average">

              <div class="average-line">

                <span>
                  میانگین کشور
                </span>

                <strong>
                  {{ formatPercent(booklet.country_average) }}٪
                </strong>

              </div>

              <div class="average-track">

                <div
                  class="average-user-marker"
                  :style="{
                    right: markerPosition(booklet.percentage)
                  }"
                ></div>

                <div
                  class="average-country-marker"
                  :style="{
                    right: markerPosition(booklet.country_average)
                  }"
                ></div>

              </div>

              <div class="average-line province-line">

                <span>
                  میانگین استان
                </span>

                <strong>
                  {{ formatPercent(booklet.province_average) }}٪
                </strong>

              </div>

            </div>


            <div class="performance-message">

              <div class="performance-icon">

                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 3v18"/>
                  <path d="M5 8h14"/>
                  <path d="M5 16h14"/>
                </svg>

              </div>

              <div>

                <strong>
                  {{ booklet.performance_title }}
                </strong>

                <p>
                  {{ booklet.performance_message }}
                </p>

              </div>

            </div>


            <div class="booklet-range">

              <span>
                سؤالات
                {{ toPersianNumber(booklet.start_question) }}
                تا
                {{ toPersianNumber(booklet.end_question) }}
              </span>

              <span>
                {{ toPersianNumber(booklet.question_count) }}
                سؤال
              </span>

            </div>

          </article>

        </div>

      </section>


      <!-- ===================================================
           TAB: ANALYTICS
      ==================================================== -->

      <section
        v-if="activeTab === 'analytics'"
        class="tab-content"
      >

        <div class="section-intro">

          <div>
            <span>داشبورد تحلیلی</span>
            <h2>تصویر کامل عملکرد</h2>
            <p>
              عملکردت را هم بین دفترچه‌ها و هم در طول آزمون‌های مختلف بررسی کن.
            </p>
          </div>

        </div>


        <!-- Booklet comparison -->

        <section class="panel chart-panel">

          <div class="panel-heading">

            <div>
              <span>مقایسه دفترچه‌ها</span>
              <h2>درصد شما در برابر میانگین‌ها</h2>
            </div>

            <div class="chart-legend">

              <span>
                <i class="legend-user"></i>
                شما
              </span>

              <span>
                <i class="legend-country"></i>
                کشور
              </span>

              <span>
                <i class="legend-province"></i>
                استان
              </span>

            </div>

          </div>


          <div class="comparison-chart">

            <div
              v-for="item in bookletComparison"
              :key="item.booklet_id"
              class="comparison-column"
            >

              <div class="comparison-values">

                <span class="value-user">
                  {{ formatPercent(item.user_percentage) }}
                </span>

                <span class="value-country">
                  {{ formatPercent(item.country_average) }}
                </span>

              </div>


              <div class="bars">

                <div
                  class="chart-bar country"
                  :style="{
                    height: chartHeight(item.country_average)
                  }"
                ></div>

                <div
                  class="chart-bar province"
                  :style="{
                    height: chartHeight(item.province_average)
                  }"
                ></div>

                <div
                  class="chart-bar user"
                  :style="{
                    height: chartHeight(item.user_percentage)
                  }"
                ></div>

              </div>


              <div class="column-label">

                <strong>
                  {{ item.booklet_title }}
                </strong>

              </div>

            </div>

          </div>

        </section>


        <!-- Progress -->

        <section class="panel chart-panel progress-panel">

          <div class="panel-heading">

            <div>
              <span>روند عملکرد</span>
              <h2>پیشرفت شما در آزمون‌ها</h2>
            </div>

            <div
              v-if="previousChange !== null"
              class="trend-chip"
              :class="changeClass(previousChange)"
            >
              {{ signedPercent(previousChange) }}٪
            </div>

          </div>


          <div
            v-if="progressData.length"
            class="line-chart"
          >

            <div class="line-chart-y">

              <span>۱۰۰</span>
              <span>۷۵</span>
              <span>۵۰</span>
              <span>۲۵</span>
              <span>۰</span>

            </div>


            <div class="line-chart-main">

              <div class="grid-lines">

                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>

              </div>


              <svg
                class="progress-svg"
                viewBox="0 0 800 300"
                preserveAspectRatio="none"
              >

                <defs>

                  <linearGradient
                    id="progressGradient"
                    x1="0"
                    x2="0"
                    y1="0"
                    y2="1"
                  >
                    <stop
                      offset="0%"
                      stop-opacity=".28"
                    />

                    <stop
                      offset="100%"
                      stop-opacity="0"
                    />
                  </linearGradient>

                </defs>


                <path
                  v-if="progressAreaPath"
                  :d="progressAreaPath"
                  class="progress-area"
                />

                <path
                  v-if="progressLinePath"
                  :d="progressLinePath"
                  class="progress-line"
                />


                <circle
                  v-for="point in progressPoints"
                  :key="point.index"
                  :cx="point.x"
                  :cy="point.y"
                  r="6"
                  class="progress-point"
                />

              </svg>


              <div class="progress-labels">

                <div
                  v-for="point in progressPoints"
                  :key="'label-' + point.index"
                  class="progress-label"
                  :style="{
                    left: point.left
                  }"
                >
                  {{ truncate(point.title, 18) }}
                </div>

              </div>

            </div>

          </div>


          <div
            v-else
            class="empty-chart"
          >
            <span>هنوز اطلاعات کافی برای نمایش روند وجود ندارد.</span>
          </div>


          <div class="progress-summary">

            <div>

              <span>اولین عملکرد</span>

              <strong>
                {{ formatPercent(firstProgressScore) }}٪
              </strong>

            </div>


            <div>

              <span>آخرین عملکرد</span>

              <strong>
                {{ formatPercent(lastProgressScore) }}٪
              </strong>

            </div>


            <div>

              <span>تعداد آزمون‌ها</span>

              <strong>
                {{ toPersianNumber(progressData.length) }}
              </strong>

            </div>

          </div>

        </section>


        <!-- Quick insights -->

        <section class="insights-grid">

          <div class="insight-card">

            <div class="insight-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m5 12 4 4L19 6"/>
              </svg>
            </div>

            <span>بهترین دفترچه</span>

            <strong>
              {{ bestBooklet?.title || '—' }}
            </strong>

            <small v-if="bestBooklet">
              {{ formatPercent(bestBooklet.percentage) }}٪
            </small>

          </div>


          <div class="insight-card">

            <div class="insight-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 3v18"/>
                <path d="M5 8h14"/>
                <path d="M5 16h14"/>
              </svg>
            </div>

            <span>نیازمند توجه</span>

            <strong>
              {{ weakestBooklet?.title || '—' }}
            </strong>

            <small v-if="weakestBooklet">
              {{ formatPercent(weakestBooklet.percentage) }}٪
            </small>

          </div>


          <div class="insight-card">

            <div class="insight-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/>
                <path d="M8 12h8"/>
              </svg>
            </div>

            <span>مجموع نزده‌ها</span>

            <strong>
              {{ toPersianNumber(result.summary?.unanswered_count || 0) }}
            </strong>

            <small>
              سؤال
            </small>

          </div>

        </section>

      </section>


      <!-- ===================================================
           TAB: PERSONALIZED REVIEW
      ==================================================== -->

      <section
        v-if="activeTab === 'review'"
        class="tab-content"
      >

        <div class="review-header">

          <div>

            <span>
              مرور شخصی‌سازی‌شده
            </span>

            <h2>
              سؤال‌ها را دوباره بررسی کن
            </h2>

            <p>
              پاسخ انتخابی شما و پاسخ صحیح هر سؤال را کنار هم ببین و اشتباهاتت را مرور کن.
            </p>

          </div>


          <div class="review-summary">

            <div class="review-mini correct">
              <strong>
                {{ toPersianNumber(reviewCounts.correct) }}
              </strong>
              <span>درست</span>
            </div>

            <div class="review-mini wrong">
              <strong>
                {{ toPersianNumber(reviewCounts.wrong) }}
              </strong>
              <span>غلط</span>
            </div>

            <div class="review-mini unanswered">
              <strong>
                {{ toPersianNumber(reviewCounts.unanswered) }}
              </strong>
              <span>نزده</span>
            </div>

          </div>

        </div>


        <!-- Review filters -->

        <div class="review-filters">

          <button
            type="button"
            :class="{ active: reviewFilter === 'all' }"
            @click="reviewFilter = 'all'"
          >
            همه
            <span>
              {{ toPersianNumber(result.personalized_review?.length || 0) }}
            </span>
          </button>


          <button
            type="button"
            :class="{ active: reviewFilter === 'wrong' }"
            @click="reviewFilter = 'wrong'"
          >
            غلط
            <span>
              {{ toPersianNumber(reviewCounts.wrong) }}
            </span>
          </button>


          <button
            type="button"
            :class="{ active: reviewFilter === 'correct' }"
            @click="reviewFilter = 'correct'"
          >
            درست
            <span>
              {{ toPersianNumber(reviewCounts.correct) }}
            </span>
          </button>


          <button
            type="button"
            :class="{ active: reviewFilter === 'unanswered' }"
            @click="reviewFilter = 'unanswered'"
          >
            نزده
            <span>
              {{ toPersianNumber(reviewCounts.unanswered) }}
            </span>
          </button>

        </div>


        <!-- Review list -->

        <div class="review-list">

          <article
            v-for="question in filteredReview"
            :key="question.question_number"
            class="question-card"
            :class="question.status"
          >

            <div class="question-top">

              <div class="question-number">

                <span>سؤال</span>

                <strong>
                  {{ toPersianNumber(question.question_number) }}
                </strong>

              </div>


              <div class="question-context">

                <strong>
                  {{ question.booklet_title || 'دفترچه' }}
                </strong>

                <span>
                  {{ question.subject || '—' }}
                </span>

              </div>


              <div
                class="question-status"
                :class="question.status"
              >

                <span class="status-dot"></span>

                {{
                  question.status === 'correct'
                    ? 'درست'
                    : question.status === 'wrong'
                      ? 'غلط'
                      : 'نزده'
                }}

              </div>

            </div>


            <div class="options-grid">

              <div
                v-for="option in question.options"
                :key="option.value"
                class="option-card"
                :class="{
                  selected: option.selected,
                  correct: option.correct,
                  'selected-wrong':
                    option.selected && !option.correct
                }"
              >

                <div class="option-number">
                  {{ toPersianNumber(option.value) }}
                </div>

                <div class="option-content">

                  <span>
                    گزینه {{ toPersianNumber(option.value) }}
                  </span>


                  <small v-if="option.selected">
                    پاسخ شما
                  </small>


                  <small
                    v-if="option.correct"
                    class="correct-label"
                  >
                    پاسخ صحیح
                  </small>

                </div>


                <div class="option-mark">

                  <svg
                    v-if="option.correct"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path d="m5 12 4 4L19 6"/>
                  </svg>


                  <svg
                    v-else-if="option.selected"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path d="m7 7 10 10"/>
                    <path d="m17 7-10 10"/>
                  </svg>

                </div>

              </div>

            </div>


            <div class="question-answer-summary">

              <div>

                <span>پاسخ شما</span>

                <strong
                  :class="{
                    empty: question.user_answer === null ||
                      question.user_answer === undefined
                  }"
                >
                  {{
                    question.user_answer
                      ? `گزینه ${toPersianNumber(question.user_answer)}`
                      : 'نزده'
                  }}
                </strong>

              </div>


              <div>

                <span>پاسخ صحیح</span>

                <strong>
                  {{
                    question.correct_answer
                      ? `گزینه ${toPersianNumber(question.correct_answer)}`
                      : 'نامشخص'
                  }}
                </strong>

              </div>

            </div>

          </article>


          <div
            v-if="filteredReview.length === 0"
            class="empty-review"
          >

            <div class="empty-review-icon">

              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 4h16v16H4z"/>
                <path d="M8 8h8"/>
                <path d="M8 12h8"/>
                <path d="M8 16h5"/>
              </svg>

            </div>

            <h3>
              سؤالی در این دسته وجود ندارد
            </h3>

            <p>
              فیلتر دیگری را امتحان کن.
            </p>

          </div>

        </div>

      </section>


      <!-- ===================================================
           FOOTER
      ==================================================== -->

      <footer class="result-footer">

        <div>

          <strong>
            کارنامه دوپامین
          </strong>

          <span>
            تحلیل کن، یاد بگیر، بهتر شو.
          </span>

        </div>


        <button
          type="button"
          @click="goBack"
        >
          بازگشت به آزمون‌ها

          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="m9 18 6-6-6-6"/>
          </svg>

        </button>

      </footer>

    </main>
  </div>
</template>


<script setup>

import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
} from 'vue'

import {
  useRoute,
  useRouter,
} from 'vue-router'

import api from '../services/api'


/* =========================================================
   ROUTER
========================================================= */

const route = useRoute()
const router = useRouter()


/* =========================================================
   STATE
========================================================= */

const result = ref(null)

const loading = ref(false)

const errorMessage = ref('')

const activeTab = ref('overview')

const reviewFilter = ref('all')

const isDark = ref(false)

let themeObserver = null


/* =========================================================
   THEME
========================================================= */

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

  themeObserver =
    new MutationObserver(() => {
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
   LOAD RESULT
========================================================= */

async function loadResult() {

  loading.value = true
  errorMessage.value = ''

  try {

    const attemptId =
      route.params.id

    if (!attemptId) {

      throw new Error(
        'شناسه کارنامه پیدا نشد.'
      )

    }

    const response =
      await api.get(
        `/exams/attempts/${attemptId}/result/`
      )

    result.value =
      response.data

  } catch (error) {

    console.error(
      'EXAM RESULT LOAD ERROR:',
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
        error?.message ||
        'دریافت کارنامه با مشکل مواجه شد.'

    }

  } finally {

    loading.value = false

  }

}


/* =========================================================
   USER
========================================================= */

const userInitials =
  computed(() => {

    const user =
      result.value?.user

    if (!user) {
      return 'د'
    }

    const first =
      user.first_name?.trim()?.charAt(0)

    const last =
      user.last_name?.trim()?.charAt(0)

    if (first || last) {
      return `${first || ''}${last || ''}`
    }

    return (
      user.username?.charAt(0) ||
      'د'
    )

  })


/* =========================================================
   BOOKLETS
========================================================= */

const sortedBooklets =
  computed(() => {

    const list =
      Array.isArray(result.value?.booklets)
        ? [...result.value.booklets]
        : []

    return list.sort(
      (a, b) =>
        Number(a.order || 0) -
        Number(b.order || 0)
    )

  })


const bookletComparison =
  computed(() => {

    const data =
      result.value?.charts?.booklet_comparison

    if (Array.isArray(data)) {
      return data
    }

    return sortedBooklets.value.map(
      booklet => ({
        booklet_id: booklet.id,
        booklet_title: booklet.title,
        user_percentage: booklet.percentage,
        user_raw_percentage: booklet.raw_percentage,
        country_average:
          booklet.country_average,
        province_average:
          booklet.province_average,
      })
    )

  })


/* =========================================================
   BEST / WEAKEST
========================================================= */

const bestBooklet =
  computed(() => {

    if (!sortedBooklets.value.length) {
      return null
    }

    return [...sortedBooklets.value]
      .sort(
        (a, b) =>
          Number(b.percentage || 0) -
          Number(a.percentage || 0)
      )[0]

  })


const weakestBooklet =
  computed(() => {

    if (!sortedBooklets.value.length) {
      return null
    }

    return [...sortedBooklets.value]
      .sort(
        (a, b) =>
          Number(a.percentage || 0) -
          Number(b.percentage || 0)
      )[0]

  })


/* =========================================================
   PROGRESS
========================================================= */

const progressData =
  computed(() => {

    const data =
      result.value?.charts?.progress ||
      result.value?.progress ||
      []

    if (!Array.isArray(data)) {
      return []
    }

    return data

  })


const firstProgressScore =
  computed(() => {

    if (!progressData.value.length) {
      return 0
    }

    return Number(
      progressData.value[0].percentage || 0
    )

  })


const lastProgressScore =
  computed(() => {

    if (!progressData.value.length) {
      return 0
    }

    return Number(
      progressData.value[
        progressData.value.length - 1
      ].percentage || 0
    )

  })


const previousChange =
  computed(() => {

    const value =
      result.value?.previous_attempt?.score_change

    if (
      value === null ||
      value === undefined
    ) {
      return null
    }

    return Number(value)

  })


/* =========================================================
   PROGRESS SVG
========================================================= */

const progressPoints =
  computed(() => {

    const data =
      progressData.value

    if (!data.length) {
      return []
    }

    const width = 800
    const height = 300

    const horizontalPadding = 15
    const verticalPadding = 20

    const usableWidth =
      width -
      horizontalPadding * 2

    const usableHeight =
      height -
      verticalPadding * 2

    const max =
      Math.max(
        100,
        ...data.map(
          item =>
            Number(item.percentage || 0)
        )
      )

    const min = 0

    return data.map(
      (item, index) => {

        const value =
          Number(item.percentage || 0)

        const x =
          data.length === 1
            ? width / 2
            : horizontalPadding +
              (
                index /
                (data.length - 1)
              ) *
              usableWidth

        const normalized =
          (value - min) /
          (max - min || 1)

        const y =
          height -
          verticalPadding -
          normalized *
          usableHeight

        const left =
          `${(
            x / width
          ) * 100}%`

        return {
          index,
          x,
          y,
          left,
          value,
          title:
            item.exam_title ||
            `آزمون ${index + 1}`,
        }

      }
    )

  })


const progressLinePath =
  computed(() => {

    const points =
      progressPoints.value

    if (!points.length) {
      return ''
    }

    return points
      .map(
        (point, index) =>
          `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`
      )
      .join(' ')

  })


const progressAreaPath =
  computed(() => {

    const points =
      progressPoints.value

    if (!points.length) {
      return ''
    }

    const baseY = 300 - 20

    const first =
      points[0]

    const last =
      points[points.length - 1]

    const line =
      points
        .map(
          (point, index) =>
            `${index === 0 ? 'L' : 'L'} ${point.x} ${point.y}`
        )
        .join(' ')

    return `
      M ${first.x} ${baseY}
      ${line}
      L ${last.x} ${baseY}
      Z
    `

  })


/* =========================================================
   SCORE RING
========================================================= */

const scoreDash =
  computed(() => {

    const radius = 50

    const circumference =
      2 * Math.PI * radius

    const percentage =
      clampPercent(
        result.value?.summary?.percentage
      )

    const visible =
      circumference *
      (percentage / 100)

    return `${visible} ${circumference}`

  })


/* =========================================================
   REVIEW
========================================================= */

const reviewCounts =
  computed(() => {

    const review =
      Array.isArray(
        result.value?.personalized_review
      )
        ? result.value.personalized_review
        : []

    return {
      correct:
        review.filter(
          item =>
            item.status === 'correct'
        ).length,

      wrong:
        review.filter(
          item =>
            item.status === 'wrong'
        ).length,

      unanswered:
        review.filter(
          item =>
            item.status === 'unanswered'
        ).length,
    }

  })


const filteredReview =
  computed(() => {

    const review =
      Array.isArray(
        result.value?.personalized_review
      )
        ? result.value.personalized_review
        : []

    if (
      reviewFilter.value === 'all'
    ) {
      return review
    }

    return review.filter(
      item =>
        item.status ===
        reviewFilter.value
    )

  })


/* =========================================================
   FORMATTERS
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


function formatPercent(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return '۰'
  }

  return number
    .toFixed(1)
    .replace(
      /\.0$/,
      ''
    )
    .replace(
      /-/g,
      '−'
    )

}


function clampPercent(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return 0
  }

  return Math.max(
    0,
    Math.min(
      100,
      number
    )
  )

}


function positivePercent(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return 0
  }

  return Math.max(
    0,
    Math.min(
      100,
      number
    )
  )

}


function signedPercent(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return '۰'
  }

  const absolute =
    Math.abs(number)

  const formatted =
    formatPercent(absolute)

  if (number > 0) {
    return `+${formatted}`
  }

  if (number < 0) {
    return `−${formatted}`
  }

  return '۰'

}


function formatRank(value) {

  if (
    value === null ||
    value === undefined ||
    value === ''
  ) {
    return '—'
  }

  return toPersianNumber(value)

}


function formatDate(value) {

  if (!value) {
    return '—'
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return '—'
  }

  return date.toLocaleDateString(
    'fa-IR-u-ca-persian',
    {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }
  )

}


function formatTime(value) {

  if (!value) {
    return '—'
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
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


function truncate(value, length) {

  if (!value) {
    return ''
  }

  const text =
    String(value)

  if (
    text.length <= length
  ) {
    return text
  }

  return (
    text.slice(0, length) +
    '…'
  )

}


/* =========================================================
   CHART HELPERS
========================================================= */

function chartHeight(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return '0%'
  }

  return `${Math.max(
    4,
    Math.min(
      100,
      number
    )
  )}%`

}


function markerPosition(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return '0%'
  }

  return `${Math.max(
    0,
    Math.min(
      100,
      number
    )
  )}%`

}


/* =========================================================
   CHANGE HELPERS
========================================================= */

function changeClass(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return 'neutral'
  }

  if (number > 0) {
    return 'positive'
  }

  if (number < 0) {
    return 'negative'
  }

  return 'neutral'

}


function changeTextClass(value) {

  const number =
    Number(value)

  if (
    !Number.isFinite(number)
  ) {
    return ''
  }

  if (number > 0) {
    return 'text-positive'
  }

  if (number < 0) {
    return 'text-negative'
  }

  return ''

}


/* =========================================================
   GO BACK
========================================================= */

async function goBack() {

  try {

    await router.push({
      name: 'Exams',
    })

  } catch {

    router.back()

  }

}


/* =========================================================
   MOUNT
========================================================= */

onMounted(
  async () => {

    observeTheme()

    await loadResult()

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

  }
)

</script>


<style scoped>

/* =========================================================
   ROOT
========================================================= */

.exam-result-page {

  --bg:
    #f4f7fb;

  --surface:
    #ffffff;

  --surface-soft:
    #f8fafc;

  --text:
    #172033;

  --text-soft:
    #68748a;

  --text-faint:
    #98a2b3;

  --border:
    #e7ebf2;

  --primary:
    #5b5cf0;

  --primary-dark:
    #4546d8;

  --primary-soft:
    rgba(91, 92, 240, .10);

  --success:
    #16a085;

  --success-soft:
    rgba(22, 160, 133, .11);

  --danger:
    #e05252;

  --danger-soft:
    rgba(224, 82, 82, .10);

  --warning:
    #e3a52f;

  --warning-soft:
    rgba(227, 165, 47, .12);

  --shadow:
    0 15px 45px rgba(31, 41, 55, .07);

  min-height:
    100vh;

  background:
    var(--bg);

  color:
    var(--text);

  padding:
    28px 20px 70px;

  transition:
    background .25s ease,
    color .25s ease;

}


/* =========================================================
   DARK
========================================================= */

.exam-result-page.is-dark {

  --bg:
    #0c1018;

  --surface:
    #151b26;

  --surface-soft:
    #101620;

  --text:
    #f1f5f9;

  --text-soft:
    #aab4c4;

  --text-faint:
    #737f91;

  --border:
    #252e3c;

  --primary:
    #7778ff;

  --primary-dark:
    #6465f2;

  --primary-soft:
    rgba(119, 120, 255, .13);

  --success:
    #28c7a7;

  --success-soft:
    rgba(40, 199, 167, .12);

  --danger:
    #ff6c6c;

  --danger-soft:
    rgba(255, 108, 108, .12);

  --warning:
    #f0b746;

  --warning-soft:
    rgba(240, 183, 70, .12);

  --shadow:
    0 18px 55px rgba(0, 0, 0, .25);

}


/* =========================================================
   CONTAINER
========================================================= */

.result-container {

  width:
    min(1280px, 100%);

  margin:
    0 auto;

}


/* =========================================================
   STATE
========================================================= */

.page-state {

  width:
    min(600px, 100%);

  min-height:
    65vh;

  margin:
    auto;

  display:
    flex;

  flex-direction:
    column;

  justify-content:
    center;

  align-items:
    center;

  text-align:
    center;

}

.page-state h2 {

  margin:
    20px 0 8px;

  font-size:
    24px;

}

.page-state p {

  margin:
    0;

  color:
    var(--text-soft);

}

.loading-orb {

  display:
    flex;

  gap:
    8px;

}

.loading-orb span {

  width:
    10px;

  height:
    10px;

  border-radius:
    50%;

  background:
    var(--primary);

  animation:
    loadingBounce 1s infinite ease-in-out;

}

.loading-orb span:nth-child(2) {
  animation-delay:
    .12s;
}

.loading-orb span:nth-child(3) {
  animation-delay:
    .24s;
}

@keyframes loadingBounce {

  0%,
  80%,
  100% {
    transform:
      translateY(0);
    opacity:
      .35;
  }

  40% {
    transform:
      translateY(-8px);
    opacity:
      1;
  }

}

.state-icon {

  width:
    70px;

  height:
    70px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    22px;

  background:
    var(--primary-soft);

}

.state-icon svg {

  width:
    34px;

  height:
    34px;

}

.state-icon.error {

  color:
    var(--danger);

  background:
    var(--danger-soft);

}

.retry-button {

  border:
    0;

  margin-top:
    24px;

  padding:
    12px 24px;

  border-radius:
    14px;

  background:
    var(--primary);

  color:
    #fff;

  cursor:
    pointer;

  font:
    inherit;

}


/* =========================================================
   HERO
========================================================= */

.hero-card {

  position:
    relative;

  overflow:
    hidden;

  border-radius:
    30px;

  padding:
    32px;

  color:
    #fff;

  background:
    linear-gradient(
      135deg,
      #3435aa 0%,
      #5556e9 48%,
      #7677ff 100%
    );

  box-shadow:
    0 25px 65px rgba(77, 78, 220, .25);

}

.hero-glow {

  position:
    absolute;

  border-radius:
    50%;

  pointer-events:
    none;

  filter:
    blur(4px);

  background:
    rgba(255,255,255,.09);

}

.glow-one {

  width:
    330px;

  height:
    330px;

  top:
    -180px;

  left:
    -80px;

}

.glow-two {

  width:
    400px;

  height:
    400px;

  right:
    -230px;

  bottom:
    -240px;

}

.hero-content {

  position:
    relative;

  z-index:
    1;

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    30px;

}

.hero-user {

  display:
    flex;

  align-items:
    center;

  gap:
    18px;

}

.avatar-wrap {

  position:
    relative;

  width:
    82px;

  height:
    82px;

  flex:
    0 0 82px;

}

.avatar-image,
.avatar-fallback {

  width:
    100%;

  height:
    100%;

  border-radius:
    26px;

  object-fit:
    cover;

  border:
    3px solid rgba(255,255,255,.35);

  background:
    rgba(255,255,255,.12);

}

.avatar-fallback {

  display:
    grid;

  place-items:
    center;

  font-size:
    26px;

  font-weight:
    900;

}

.avatar-status {

  position:
    absolute;

  width:
    16px;

  height:
    16px;

  border:
    3px solid #5556e9;

  background:
    #35d39b;

  border-radius:
    50%;

  right:
    -1px;

  bottom:
    -1px;

}

.hero-user-info {

  min-width:
    0;

}

.hero-eyebrow {

  display:
    block;

  font-size:
    13px;

  opacity:
    .75;

  margin-bottom:
    7px;

}

.hero-user-info h1 {

  margin:
    0;

  font-size:
    clamp(22px, 3vw, 34px);

  line-height:
    1.35;

  font-weight:
    900;

}

.hero-user-info p {

  margin:
    8px 0 0;

  font-size:
    14px;

  opacity:
    .75;

}

.hero-score {

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

}

.score-ring {

  position:
    relative;

  width:
    142px;

  height:
    142px;

}

.score-svg {

  width:
    100%;

  height:
    100%;

  transform:
    rotate(-90deg);

}

.score-track {

  fill:
    none;

  stroke:
    rgba(255,255,255,.15);

  stroke-width:
    8;

}

.score-progress {

  fill:
    none;

  stroke:
    #fff;

  stroke-width:
    8;

  stroke-linecap:
    round;

  transition:
    stroke-dasharray .7s ease;

}

.score-center {

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

}

.score-center strong {

  font-size:
    29px;

  line-height:
    1;

  font-weight:
    950;

}

.score-center span {

  font-size:
    12px;

  margin-top:
    6px;

  opacity:
    .72;

}

.score-caption {

  margin-top:
    7px;

  font-size:
    12px;

  opacity:
    .75;

}

.hero-bottom {

  position:
    relative;

  z-index:
    1;

  display:
    flex;

  justify-content:
    space-between;

  gap:
    15px;

  margin-top:
    30px;

  padding-top:
    20px;

  border-top:
    1px solid rgba(255,255,255,.14);

  font-size:
    13px;

  opacity:
    .8;

}

.hero-meta {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

}

.hero-meta-dot {

  width:
    8px;

  height:
    8px;

  border-radius:
    50%;

  background:
    #45dfa8;

  box-shadow:
    0 0 0 5px rgba(69,223,168,.12);

}

.meta-separator {

  opacity:
    .5;

}


/* =========================================================
   TABS
========================================================= */

.result-tabs {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  overflow-x:
    auto;

  margin:
    20px 0;

  padding:
    7px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    19px;

  box-shadow:
    var(--shadow);

  scrollbar-width:
    none;

}

.result-tabs::-webkit-scrollbar {
  display:
    none;
}

.result-tab {

  flex:
    1 0 auto;

  min-width:
    max-content;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    9px;

  border:
    0;

  padding:
    13px 17px;

  border-radius:
    13px;

  background:
    transparent;

  color:
    var(--text-soft);

  cursor:
    pointer;

  font:
    inherit;

  font-size:
    13px;

  transition:
    .2s ease;

}

.result-tab:hover {

  color:
    var(--text);

  background:
    var(--surface-soft);

}

.result-tab.active {

  color:
    #fff;

  background:
    var(--primary);

  box-shadow:
    0 7px 20px rgba(91,92,240,.22);

}

.tab-icon {

  display:
    grid;

  place-items:
    center;

}

.tab-icon svg {

  width:
    19px;

  height:
    19px;

}

.result-tab small {

  min-width:
    23px;

  padding:
    2px 6px;

  border-radius:
    8px;

  background:
    var(--primary-soft);

  color:
    var(--primary);

  font-size:
    10px;

}

.result-tab.active small {

  color:
    #fff;

  background:
    rgba(255,255,255,.18);

}


/* =========================================================
   TAB CONTENT
========================================================= */

.tab-content {

  animation:
    tabIn .3s ease;

}

@keyframes tabIn {

  from {
    opacity:
      0;

    transform:
      translateY(8px);
  }

  to {
    opacity:
      1;

    transform:
      translateY(0);
  }

}


/* =========================================================
   SUMMARY
========================================================= */

.summary-grid {

  display:
    grid;

  grid-template-columns:
    repeat(4, 1fr);

  gap:
    14px;

}

.metric-card {

  display:
    flex;

  align-items:
    center;

  gap:
    15px;

  min-height:
    125px;

  padding:
    20px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    22px;

  box-shadow:
    var(--shadow);

}

.metric-icon {

  width:
    50px;

  height:
    50px;

  flex:
    0 0 50px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    16px;

  background:
    var(--primary-soft);

  color:
    var(--primary);

}

.metric-icon svg {

  width:
    24px;

  height:
    24px;

}

.metric-icon.correct {

  color:
    var(--success);

  background:
    var(--success-soft);

}

.metric-icon.wrong {

  color:
    var(--danger);

  background:
    var(--danger-soft);

}

.metric-icon.unanswered {

  color:
    var(--warning);

  background:
    var(--warning-soft);

}

.metric-content {

  min-width:
    0;

}

.metric-content span {

  display:
    block;

  color:
    var(--text-soft);

  font-size:
    12px;

}

.metric-content strong {

  display:
    block;

  margin-top:
    5px;

  font-size:
    26px;

  font-weight:
    950;

}

.metric-content small {

  color:
    var(--text-faint);

  font-size:
    10px;

}


/* =========================================================
   PANEL
========================================================= */

.panel {

  margin-top:
    16px;

  padding:
    25px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    24px;

  box-shadow:
    var(--shadow);

}

.panel-heading {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    20px;

  margin-bottom:
    22px;

}

.panel-heading > div:first-child span {

  color:
    var(--primary);

  font-size:
    11px;

  font-weight:
    700;

}

.panel-heading h2 {

  margin:
    5px 0 0;

  font-size:
    20px;

}

.ranking-crown {

  width:
    50px;

  height:
    50px;

  display:
    grid;

  place-items:
    center;

  color:
    var(--warning);

  background:
    var(--warning-soft);

  border-radius:
    16px;

}

.ranking-crown svg {

  width:
    25px;

  height:
    25px;

}


/* =========================================================
   RANKING
========================================================= */

.ranking-grid {

  display:
    grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap:
    15px;

}

.rank-card {

  display:
    flex;

  align-items:
    center;

  gap:
    16px;

  padding:
    20px;

  border-radius:
    19px;

  border:
    1px solid var(--border);

  background:
    var(--surface-soft);

}

.rank-card.national {

  background:
    linear-gradient(
      135deg,
      var(--primary-soft),
      transparent
    );

}

.rank-card.province {

  background:
    linear-gradient(
      135deg,
      var(--success-soft),
      transparent
    );

}

.rank-card-icon {

  width:
    52px;

  height:
    52px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    16px;

  color:
    var(--primary);

  background:
    var(--surface);

}

.province .rank-card-icon {

  color:
    var(--success);

}

.rank-card-icon svg {

  width:
    25px;

  height:
    25px;

}

.rank-card-copy span {

  display:
    block;

  color:
    var(--text-soft);

  font-size:
    12px;

}

.rank-card-copy strong {

  display:
    inline-block;

  margin-top:
    4px;

  font-size:
    29px;

  font-weight:
    950;

}

.rank-card-copy small {

  color:
    var(--text-faint);

  font-size:
    11px;

  margin-right:
    7px;

}


/* =========================================================
   RAW SCORE
========================================================= */

.raw-comparison {

  display:
    grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap:
    25px;

}

.raw-label {

  display:
    flex;

  justify-content:
    space-between;

  align-items:
    center;

  margin-bottom:
    9px;

}

.raw-label span {

  color:
    var(--text-soft);

  font-size:
    13px;

}

.raw-label strong {

  font-size:
    20px;

}

.progress-track {

  height:
    9px;

  border-radius:
    99px;

  overflow:
    hidden;

  background:
    var(--border);

}

.progress-fill {

  height:
    100%;

  border-radius:
    inherit;

}

.progress-fill.negative {

  background:
    linear-gradient(
      90deg,
      #4546d8,
      #7778ff
    );

}

.progress-fill.raw {

  background:
    linear-gradient(
      90deg,
      #13a884,
      #45d8b7
    );

}

.raw-item > small {

  display:
    block;

  margin-top:
    8px;

  color:
    var(--text-faint);

  font-size:
    10px;

}


/* =========================================================
   PREVIOUS
========================================================= */

.change-badge,
.trend-chip {

  padding:
    7px 12px;

  border-radius:
    11px;

  font-size:
    12px;

  font-weight:
    800;

}

.change-badge.positive,
.trend-chip.positive {

  color:
    var(--success);

  background:
    var(--success-soft);

}

.change-badge.negative,
.trend-chip.negative {

  color:
    var(--danger);

  background:
    var(--danger-soft);

}

.change-badge.neutral,
.trend-chip.neutral {

  color:
    var(--text-soft);

  background:
    var(--surface-soft);

}

.previous-content {

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    45px;

  padding:
    20px;

}

.previous-score {

  text-align:
    center;

}

.previous-score span {

  display:
    block;

  color:
    var(--text-soft);

  font-size:
    12px;

}

.previous-score strong {

  display:
    block;

  margin-top:
    5px;

  font-size:
    31px;

  color:
    var(--text);

}

.previous-score.current strong {

  color:
    var(--primary);

}

.change-arrow {

  width:
    45px;

  height:
    45px;

  display:
    grid;

  place-items:
    center;

  color:
    var(--primary);

  background:
    var(--primary-soft);

  border-radius:
    50%;

}

.change-arrow svg {

  width:
    22px;

  height:
    22px;

}

.previous-details {

  display:
    grid;

  grid-template-columns:
    repeat(4, 1fr);

  border-top:
    1px solid var(--border);

  padding-top:
    18px;

}

.previous-details > div {

  text-align:
    center;

  padding:
    0 15px;

  border-left:
    1px solid var(--border);

}

.previous-details > div:last-child {

  border-left:
    0;

}

.previous-details span {

  display:
    block;

  color:
    var(--text-faint);

  font-size:
    11px;

}

.previous-details strong {

  display:
    block;

  margin-top:
    5px;

  font-size:
    17px;

}

.text-positive {

  color:
    var(--success);

}

.text-negative {

  color:
    var(--danger);

}


/* =========================================================
   SECTION INTRO
========================================================= */

.section-intro {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    20px;

  margin:
    5px 0 20px;

}

.section-intro span,
.review-header > div:first-child > span {

  color:
    var(--primary);

  font-size:
    11px;

  font-weight:
    800;

}

.section-intro h2,
.review-header h2 {

  margin:
    5px 0;

  font-size:
    26px;

}

.section-intro p,
.review-header p {

  margin:
    0;

  color:
    var(--text-soft);

  font-size:
    13px;

}

.booklet-total {

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  padding:
    15px 20px;

  border-radius:
    18px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

}

.booklet-total strong {

  font-size:
    25px;

}

.booklet-total span {

  color:
    var(--text-soft);

}


/* =========================================================
   BOOKLETS
========================================================= */

.booklet-cards {

  display:
    grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap:
    16px;

}

.booklet-card {

  padding:
    22px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    24px;

  box-shadow:
    var(--shadow);

  transition:
    transform .2s ease,
    box-shadow .2s ease;

}

.booklet-card:hover {

  transform:
    translateY(-3px);

  box-shadow:
    0 20px 50px rgba(31,41,55,.10);

}

.booklet-card-top {

  display:
    flex;

  align-items:
    center;

  gap:
    13px;

}

.booklet-number {

  width:
    44px;

  height:
    44px;

  display:
    grid;

  place-items:
    center;

  flex:
    0 0 44px;

  border-radius:
    14px;

  color:
    #fff;

  background:
    linear-gradient(
      135deg,
      var(--primary),
      #8586ff
    );

  font-weight:
    900;

}

.booklet-title-wrap {

  min-width:
    0;

  flex:
    1;

}

.booklet-title-wrap span {

  color:
    var(--text-faint);

  font-size:
    10px;

}

.booklet-title-wrap h3 {

  margin:
    3px 0 0;

  font-size:
    16px;

  overflow:
    hidden;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;

}

.decile-badge {

  display:
    flex;

  align-items:
    center;

  gap:
    6px;

  padding:
    7px 10px;

  border-radius:
    12px;

  background:
    var(--warning-soft);

  color:
    var(--warning);

}

.decile-badge span {

  font-size:
    10px;

}

.decile-badge strong {

  font-size:
    16px;

}

.booklet-score-row {

  display:
    flex;

  justify-content:
    space-between;

  align-items:
    end;

  margin-top:
    25px;

}

.booklet-score strong {

  display:
    block;

  font-size:
    35px;

  font-weight:
    950;

}

.booklet-score span {

  color:
    var(--text-faint);

  font-size:
    10px;

}

.booklet-raw {

  text-align:
    left;

}

.booklet-raw span {

  color:
    var(--text-faint);

  font-size:
    10px;

}

.booklet-raw strong {

  display:
    block;

  margin-top:
    3px;

  font-size:
    17px;

}

.booklet-bar {

  height:
    8px;

  margin:
    15px 0;

  overflow:
    hidden;

  border-radius:
    99px;

  background:
    var(--border);

}

.booklet-bar-fill {

  height:
    100%;

  border-radius:
    inherit;

  background:
    linear-gradient(
      90deg,
      var(--primary),
      #8889ff
    );

}

.answer-breakdown {

  display:
    grid;

  grid-template-columns:
    repeat(3, 1fr);

  gap:
    8px;

}

.answer-stat {

  display:
    flex;

  align-items:
    center;

  gap:
    6px;

  padding:
    10px;

  border-radius:
    13px;

  background:
    var(--surface-soft);

}

.answer-dot {

  width:
    7px;

  height:
    7px;

  border-radius:
    50%;

  background:
    currentColor;

}

.answer-stat span:not(.answer-dot) {

  color:
    var(--text-soft);

  font-size:
    10px;

}

.answer-stat strong {

  margin-right:
    auto;

  font-size:
    14px;

}

.answer-stat.correct {

  color:
    var(--success);

}

.answer-stat.wrong {

  color:
    var(--danger);

}

.answer-stat.unanswered {

  color:
    var(--warning);

}

.booklet-ranks {

  display:
    grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap:
    10px;

  margin-top:
    13px;

}

.booklet-ranks > div {

  padding:
    13px;

  border-radius:
    14px;

  background:
    var(--surface-soft);

}

.booklet-ranks span {

  display:
    block;

  color:
    var(--text-faint);

  font-size:
    10px;

}

.booklet-ranks strong {

  display:
    inline-block;

  margin-top:
    3px;

  font-size:
    19px;

}

.booklet-ranks small {

  color:
    var(--text-faint);

  font-size:
    9px;

  margin-right:
    4px;

}

.booklet-average {

  margin-top:
    14px;

  padding:
    14px;

  border:
    1px solid var(--border);

  border-radius:
    15px;

}

.average-line {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

}

.average-line span {

  color:
    var(--text-soft);

  font-size:
    10px;

}

.average-line strong {

  font-size:
    13px;

}

.average-track {

  position:
    relative;

  height:
    8px;

  margin:
    13px 0;

  border-radius:
    99px;

  background:
    var(--border);

}

.average-user-marker,
.average-country-marker {

  position:
    absolute;

  top:
    50%;

  width:
    13px;

  height:
    13px;

  transform:
    translate(50%, -50%);

  border:
    3px solid var(--surface);

  border-radius:
    50%;

}

.average-user-marker {

  background:
    var(--primary);

  z-index:
    2;

}

.average-country-marker {

  background:
    var(--warning);

  z-index:
    1;

}

.province-line {

  margin-top:
    5px;

}

.performance-message {

  display:
    flex;

  gap:
    12px;

  margin-top:
    14px;

  padding:
    15px;

  border-radius:
    17px;

  background:
    var(--primary-soft);

}

.performance-icon {

  width:
    38px;

  height:
    38px;

  flex:
    0 0 38px;

  display:
    grid;

  place-items:
    center;

  color:
    var(--primary);

  background:
    var(--surface);

  border-radius:
    12px;

}

.performance-icon svg {

  width:
    19px;

  height:
    19px;

}

.performance-message strong {

  display:
    block;

  font-size:
    13px;

}

.performance-message p {

  margin:
    5px 0 0;

  color:
    var(--text-soft);

  font-size:
    11px;

  line-height:
    1.9;

}

.booklet-range {

  display:
    flex;

  justify-content:
    space-between;

  gap:
    10px;

  margin-top:
    15px;

  color:
    var(--text-faint);

  font-size:
    10px;

}


/* =========================================================
   CHARTS
========================================================= */

.chart-panel {

  overflow:
    hidden;

}

.chart-legend {

  display:
    flex;

  gap:
    14px;

  color:
    var(--text-soft);

  font-size:
    10px;

}

.chart-legend span {

  display:
    flex;

  align-items:
    center;

  gap:
    5px;

}

.chart-legend i {

  width:
    8px;

  height:
    8px;

  border-radius:
    50%;

}

.legend-user {

  background:
    var(--primary);

}

.legend-country {

  background:
    var(--warning);

}

.legend-province {

  background:
    var(--success);

}

.comparison-chart {

  min-height:
    320px;

  display:
    flex;

  align-items:
    end;

  justify-content:
    space-around;

  gap:
    15px;

  padding:
    30px 15px 0;

  border-bottom:
    1px solid var(--border);

}

.comparison-column {

  width:
    100%;

  max-width:
    130px;

  height:
    280px;

  display:
    flex;

  flex-direction:
    column;

  justify-content:
    end;

}

.comparison-values {

  display:
    flex;

  justify-content:
    center;

  gap:
    8px;

  margin-bottom:
    5px;

  font-size:
    9px;

}

.value-user {

  color:
    var(--primary);

  font-weight:
    900;

}

.value-country {

  color:
    var(--warning);

}

.bars {

  height:
    225px;

  display:
    flex;

  align-items:
    end;

  justify-content:
    center;

  gap:
    5px;

  border-bottom:
    1px solid var(--border);

}

.chart-bar {

  width:
    20px;

  min-height:
    3px;

  border-radius:
    7px 7px 0 0;

  transition:
    height .5s ease;

}

.chart-bar.user {

  background:
    linear-gradient(
      180deg,
      #7778ff,
      #5051e4
    );

}

.chart-bar.country {

  background:
    var(--warning);

  opacity:
    .65;

}

.chart-bar.province {

  background:
    var(--success);

  opacity:
    .65;

}

.column-label {

  min-height:
    42px;

  display:
    grid;

  place-items:
    center;

  text-align:
    center;

  padding-top:
    10px;

}

.column-label strong {

  max-width:
    100%;

  overflow:
    hidden;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;

  font-size:
    10px;

  color:
    var(--text-soft);

}


/* =========================================================
   LINE CHART
========================================================= */

.line-chart {

  display:
    flex;

  gap:
    12px;

}

.line-chart-y {

  width:
    35px;

  display:
    flex;

  flex-direction:
    column;

  justify-content:
    space-between;

  height:
    300px;

  color:
    var(--text-faint);

  font-size:
    9px;

  text-align:
    left;

}

.line-chart-main {

  position:
    relative;

  flex:
    1;

  height:
    300px;

}

.grid-lines {

  position:
    absolute;

  inset:
    0;

  display:
    flex;

  flex-direction:
    column;

  justify-content:
    space-between;

}

.grid-lines span {

  width:
    100%;

  height:
    1px;

  background:
    var(--border);

}

.progress-svg {

  position:
    absolute;

  inset:
    0;

  width:
    100%;

  height:
    100%;

  overflow:
    visible;

}

.progress-area {

  fill:
    url(#progressGradient);

}

.progress-line {

  fill:
    none;

  stroke:
    var(--primary);

  stroke-width:
    4;

  stroke-linecap:
    round;

  stroke-linejoin:
    round;

}

.progress-point {

  fill:
    var(--surface);

  stroke:
    var(--primary);

  stroke-width:
    4;

}

.progress-labels {

  position:
    absolute;

  left:
    0;

  right:
    0;

  bottom:
    -30px;

  height:
    20px;

}

.progress-label {

  position:
    absolute;

  transform:
    translateX(-50%);

  width:
    90px;

  overflow:
    hidden;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;

  text-align:
    center;

  color:
    var(--text-faint);

  font-size:
    8px;

}

.empty-chart {

  min-height:
    260px;

  display:
    grid;

  place-items:
    center;

  color:
    var(--text-faint);

}

.progress-summary {

  display:
    grid;

  grid-template-columns:
    repeat(3, 1fr);

  margin-top:
    55px;

  padding-top:
    20px;

  border-top:
    1px solid var(--border);

}

.progress-summary > div {

  text-align:
    center;

  border-left:
    1px solid var(--border);

}

.progress-summary > div:last-child {

  border-left:
    0;

}

.progress-summary span {

  display:
    block;

  color:
    var(--text-faint);

  font-size:
    10px;

}

.progress-summary strong {

  display:
    block;

  margin-top:
    4px;

  font-size:
    19px;

}


/* =========================================================
   INSIGHTS
========================================================= */

.insights-grid {

  display:
    grid;

  grid-template-columns:
    repeat(3, 1fr);

  gap:
    15px;

  margin-top:
    16px;

}

.insight-card {

  padding:
    21px;

  border:
    1px solid var(--border);

  background:
    var(--surface);

  border-radius:
    21px;

  box-shadow:
    var(--shadow);

}

.insight-icon {

  width:
    43px;

  height:
    43px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    14px;

  color:
    var(--primary);

  background:
    var(--primary-soft);

}

.insight-icon svg {

  width:
    21px;

  height:
    21px;

}

.insight-card > span {

  display:
    block;

  margin-top:
    15px;

  color:
    var(--text-faint);

  font-size:
    10px;

}

.insight-card > strong {

  display:
    block;

  margin-top:
    5px;

  font-size:
    16px;

}

.insight-card > small {

  display:
    block;

  margin-top:
    5px;

  color:
    var(--primary);

  font-weight:
    800;

}


/* =========================================================
   REVIEW
========================================================= */

.review-header {

  display:
    flex;

  justify-content:
    space-between;

  align-items:
    end;

  gap:
    20px;

  margin:
    5px 0 20px;

}

.review-summary {

  display:
    flex;

  gap:
    8px;

}

.review-mini {

  min-width:
    65px;

  padding:
    10px;

  text-align:
    center;

  border-radius:
    13px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

}

.review-mini strong {

  display:
    block;

  font-size:
    18px;

}

.review-mini span {

  color:
    var(--text-faint);

  font-size:
    9px;

}

.review-mini.correct strong {

  color:
    var(--success);

}

.review-mini.wrong strong {

  color:
    var(--danger);

}

.review-mini.unanswered strong {

  color:
    var(--warning);

}

.review-filters {

  display:
    flex;

  gap:
    8px;

  overflow-x:
    auto;

  margin-bottom:
    15px;

  scrollbar-width:
    none;

}

.review-filters::-webkit-scrollbar {
  display:
    none;
}

.review-filters button {

  display:
    flex;

  align-items:
    center;

  gap:
    7px;

  padding:
    10px 14px;

  border:
    1px solid var(--border);

  border-radius:
    13px;

  background:
    var(--surface);

  color:
    var(--text-soft);

  cursor:
    pointer;

  font:
    inherit;

  font-size:
    11px;

  white-space:
    nowrap;

}

.review-filters button span {

  padding:
    2px 6px;

  border-radius:
    7px;

  background:
    var(--surface-soft);

}

.review-filters button.active {

  color:
    #fff;

  background:
    var(--primary);

  border-color:
    var(--primary);

}

.review-filters button.active span {

  background:
    rgba(255,255,255,.18);

}

.review-list {

  display:
    flex;

  flex-direction:
    column;

  gap:
    13px;

}

.question-card {

  padding:
    20px;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    22px;

  box-shadow:
    var(--shadow);

  overflow:
    hidden;

}

.question-card.correct {

  border-right:
    4px solid var(--success);

}

.question-card.wrong {

  border-right:
    4px solid var(--danger);

}

.question-card.unanswered {

  border-right:
    4px solid var(--warning);

}

.question-top {

  display:
    flex;

  align-items:
    center;

  gap:
    13px;

  padding-bottom:
    17px;

  border-bottom:
    1px solid var(--border);

}

.question-number {

  display:
    flex;

  align-items:
    center;

  gap:
    7px;

}

.question-number span {

  color:
    var(--text-faint);

  font-size:
    10px;

}

.question-number strong {

  font-size:
    21px;

}

.question-context {

  flex:
    1;

  min-width:
    0;

}

.question-context strong {

  display:
    block;

  overflow:
    hidden;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;

  font-size:
    13px;

}

.question-context span {

  display:
    block;

  margin-top:
    3px;

  color:
    var(--text-faint);

  font-size:
    10px;

}

.question-status {

  display:
    flex;

  align-items:
    center;

  gap:
    6px;

  padding:
    7px 10px;

  border-radius:
    11px;

  font-size:
    10px;

}

.question-status.correct {

  color:
    var(--success);

  background:
    var(--success-soft);

}

.question-status.wrong {

  color:
    var(--danger);

  background:
    var(--danger-soft);

}

.question-status.unanswered {

  color:
    var(--warning);

  background:
    var(--warning-soft);

}

.status-dot {

  width:
    6px;

  height:
    6px;

  border-radius:
    50%;

  background:
    currentColor;

}

.options-grid {

  display:
    grid;

  grid-template-columns:
    repeat(4, 1fr);

  gap:
    10px;

  margin-top:
    17px;

}

.option-card {

  position:
    relative;

  min-height:
    72px;

  display:
    flex;

  align-items:
    center;

  gap:
    10px;

  padding:
    10px;

  border:
    1px solid var(--border);

  border-radius:
    15px;

  background:
    var(--surface-soft);

  transition:
    .2s ease;

}

.option-card.selected {

  border-color:
    var(--primary);

  background:
    var(--primary-soft);

}

.option-card.correct {

  border-color:
    var(--success);

  background:
    var(--success-soft);

}

.option-card.selected-wrong {

  border-color:
    var(--danger);

  background:
    var(--danger-soft);

}

.option-number {

  width:
    32px;

  height:
    32px;

  flex:
    0 0 32px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    10px;

  background:
    var(--surface);

  color:
    var(--text-soft);

  font-weight:
    900;

}

.option-content {

  min-width:
    0;

}

.option-content span {

  display:
    block;

  color:
    var(--text-soft);

  font-size:
    10px;

}

.option-content small {

  display:
    block;

  margin-top:
    4px;

  color:
    var(--primary);

  font-size:
    9px;

  font-weight:
    800;

}

.option-content small.correct-label {

  color:
    var(--success);

}

.option-mark {

  margin-right:
    auto;

}

.option-mark svg {

  width:
    19px;

  height:
    19px;

}

.option-card.correct .option-mark {

  color:
    var(--success);

}

.option-card.selected-wrong .option-mark {

  color:
    var(--danger);

}

.question-answer-summary {

  display:
    grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap:
    10px;

  margin-top:
    15px;

}

.question-answer-summary > div {

  display:
    flex;

  justify-content:
    space-between;

  align-items:
    center;

  padding:
    12px 14px;

  border-radius:
    13px;

  background:
    var(--surface-soft);

}

.question-answer-summary span {

  color:
    var(--text-faint);

  font-size:
    10px;

}

.question-answer-summary strong {

  font-size:
    12px;

}

.question-answer-summary strong.empty {

  color:
    var(--warning);

}

.empty-review {

  padding:
    60px 20px;

  text-align:
    center;

  background:
    var(--surface);

  border:
    1px solid var(--border);

  border-radius:
    22px;

}

.empty-review-icon {

  width:
    60px;

  height:
    60px;

  margin:
    0 auto;

  display:
    grid;

  place-items:
    center;

  color:
    var(--text-faint);

  background:
    var(--surface-soft);

  border-radius:
    18px;

}

.empty-review-icon svg {

  width:
    28px;

  height:
    28px;

}

.empty-review h3 {

  margin:
    16px 0 5px;

}

.empty-review p {

  margin:
    0;

  color:
    var(--text-faint);

  font-size:
    12px;

}


/* =========================================================
   FOOTER
========================================================= */

.result-footer {

  display:
    flex;

  justify-content:
    space-between;

  align-items:
    center;

  gap:
    20px;

  margin-top:
    25px;

  padding:
    20px 5px;

}

.result-footer strong {

  display:
    block;

  font-size:
    14px;

}

.result-footer span {

  display:
    block;

  margin-top:
    4px;

  color:
    var(--text-faint);

  font-size:
    10px;

}

.result-footer button {

  display:
    flex;

  align-items:
    center;

  gap:
    7px;

  border:
    0;

  background:
    transparent;

  color:
    var(--primary);

  cursor:
    pointer;

  font:
    inherit;

  font-size:
    11px;

}

.result-footer button svg {

  width:
    17px;

  height:
    17px;

}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1050px) {

  .summary-grid {

    grid-template-columns:
      repeat(2, 1fr);

  }

  .booklet-cards {

    grid-template-columns:
      1fr;

  }

}


@media (max-width: 800px) {

  .exam-result-page {

    padding:
      15px 12px 50px;

  }

  .hero-card {

    padding:
      23px;

    border-radius:
      24px;

  }

  .hero-content {

    flex-direction:
      column;

    align-items:
      flex-start;

  }

  .hero-score {

    align-self:
      center;

  }

  .hero-bottom {

    flex-direction:
      column;

  }

  .ranking-grid,
  .raw-comparison {

    grid-template-columns:
      1fr;

  }

  .previous-content {

    gap:
      18px;

  }

  .previous-details {

    grid-template-columns:
      repeat(2, 1fr);

    gap:
      15px;

  }

  .previous-details > div {

    border-left:
      0;

  }

  .insights-grid {

    grid-template-columns:
      1fr;

  }

  .review-header {

    flex-direction:
      column;

    align-items:
      flex-start;

  }

}


@media (max-width: 600px) {

  .summary-grid {

    grid-template-columns:
      1fr;

  }

  .metric-card {

    min-height:
      100px;

  }

  .panel {

    padding:
      18px;

    border-radius:
      19px;

  }

  .section-intro h2,
  .review-header h2 {

    font-size:
      21px;

  }

  .booklet-card {

    padding:
      17px;

  }

  .answer-breakdown {

    grid-template-columns:
      1fr;

  }

  .booklet-ranks {

    grid-template-columns:
      1fr;

  }

  .comparison-chart {

    overflow-x:
      auto;

    justify-content:
      flex-start;

    min-width:
      650px;

  }

  .chart-panel {

    overflow-x:
      auto;

  }

  .line-chart {

    min-width:
      650px;

  }

  .options-grid {

    grid-template-columns:
      repeat(2, 1fr);

  }

  .question-top {

    flex-wrap:
      wrap;

  }

  .question-context {

    order:
      3;

    flex-basis:
      100%;

  }

  .question-answer-summary {

    grid-template-columns:
      1fr;

  }

  .result-footer {

    flex-direction:
      column;

    align-items:
      flex-start;

  }

}


@media (max-width: 390px) {

  .avatar-wrap {

    width:
      65px;

    height:
      65px;

    flex-basis:
      65px;

  }

  .hero-user {

    gap:
      11px;

  }

  .hero-user-info h1 {

    font-size:
      19px;

  }

  .options-grid {

    grid-template-columns:
      1fr;

  }

}

</style>