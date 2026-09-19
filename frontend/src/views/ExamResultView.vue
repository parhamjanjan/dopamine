<template>
  <div
    class="exam-result-page"
    :class="{ 'is-dark': isDark }"
    dir="rtl"
    @mousemove="handleMouseMove"
    :style="mouseStyle"
  >
    <!-- Background grid only -->
    <div class="bg-layer" aria-hidden="true">
      <div class="bg-grid"></div>
      <div class="bg-glow"></div>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="page-state">
      <div class="loading-orb">
        <span></span><span></span><span></span>
      </div>
      <h2>در حال آماده‌سازی کارنامه</h2>
      <p>نتایج و تحلیل عملکرد شما در حال دریافت است...</p>
    </div>

    <!-- ERROR -->
    <div v-else-if="errorMessage" class="page-state error-state">
      <div class="state-icon error">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M12 3 2.8 19a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L12 3Z"/>
          <path d="M12 9v4"/><path d="M12 17h.01"/>
        </svg>
      </div>
      <h2>دریافت کارنامه ناموفق بود</h2>
      <p>{{ errorMessage }}</p>
      <button type="button" class="retry-button" @click="loadResult">تلاش دوباره</button>
    </div>

    <!-- MAIN -->
    <main v-else-if="result" class="result-container">

      <!-- HERO -->
      <section class="hero-card">
        <button type="button" class="back-button" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="m15 18-6-6 6-6" />
          </svg>
        </button>

        <div class="hero-aurora"></div>
        <div class="hero-grid"></div>

        <div class="hero-content">
          <div class="hero-user">
            <div class="avatar-wrap">
              <img
                v-if="result.user?.profile_image"
                :src="result.user.profile_image"
                alt="تصویر کاربر"
                class="avatar-image"
              />
              <div v-else class="avatar-fallback">{{ userInitials }}</div>
              <div class="avatar-status"></div>
            </div>

            <div class="hero-user-info">
              <span class="hero-eyebrow">کارنامه آزمون</span>
              <h1>{{ result.exam?.title || 'آزمون' }}</h1>
              <p>{{ result.user?.full_name || result.user?.username || 'دانش‌آموز' }}</p>
            </div>
          </div>

          <div class="hero-score">
            <div class="score-ring">
              <svg viewBox="0 0 120 120" class="score-svg">
                <defs>
                  <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff" />
                    <stop offset="100%" stop-color="#b8b9ff" />
                  </linearGradient>
                </defs>
                <circle cx="60" cy="60" r="50" class="score-track" />
                <circle
                  cx="60" cy="60" r="50"
                  class="score-progress"
                  :stroke-dasharray="scoreDash"
                  stroke-dashoffset="0"
                />
              </svg>
              <div class="score-center">
                <strong>{{ formatPercent(result.summary?.percentage) }}</strong>
                <span>درصد</span>
              </div>
            </div>
            <div class="score-caption">درصد با نمره منفی</div>
          </div>
        </div>

        <div class="hero-bottom">
          <div class="hero-meta">
            <span class="hero-meta-dot"></span>
            <span>{{ result.is_final ? 'کارنامه نهایی' : 'کارنامه اولیه' }}</span>
          </div>
          <div class="hero-meta">
            <span>{{ formatDate(result.exam?.start_at) }}</span>
            <span class="meta-separator">•</span>
            <span>{{ formatTime(result.exam?.start_at) }}</span>
          </div>
        </div>
      </section>

      <!-- RESULT PULSE -->
      <section class="result-pulse" aria-label="نمایش سریع عملکرد">
        <div class="pulse-main">
          <div class="pulse-orbit" aria-hidden="true">
            <span class="orbit orbit-one"></span>
            <span class="orbit orbit-two"></span>
            <span class="orbit-dot"></span>
          </div>
          <div class="pulse-copy">
            <span class="pulse-kicker">نمایش هوشمند عملکرد</span>
            <strong>{{ performanceSignal.title }}</strong>
            <p>{{ performanceSignal.description }}</p>
          </div>
        </div>
        <div class="pulse-stats">
          <div><span>صدک</span><strong>{{ formatPercent(percentile) }}٪</strong></div>
          <div><span>رتبه</span><strong>{{ formatRank(result.ranking?.national_rank) }}</strong></div>
          <div><span>دقت</span><strong>{{ formatPercent(answerAccuracy) }}٪</strong></div>
          <div><span>فاصله تا ۷۵٪</span><strong>{{ formatPercent(targetGap) }}٪</strong></div>
        </div>
      </section>

      <!-- TABS -->
      <nav class="result-tabs">
        <button
          type="button" class="result-tab"
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
          type="button" class="result-tab"
          :class="{ active: activeTab === 'booklets' }"
          @click="activeTab = 'booklets'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 4.5A2.5 2.5 0 0 1 7.5 2H20v17H7.5A2.5 2.5 0 0 0 5 21.5v-17Z"/>
              <path d="M5 4.5V21.5"/><path d="M9 7h7"/>
              <path d="M9 11h7"/><path d="M9 15h4"/>
            </svg>
          </span>
          <span>دفترچه‌ها</span>
          <small>{{ toPersianNumber(result.booklets?.length || 0) }}</small>
        </button>

        <button
          type="button" class="result-tab"
          :class="{ active: activeTab === 'analytics' }"
          @click="activeTab = 'analytics'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 19V5"/><path d="M4 19h16"/>
              <path d="m7 15 3-4 3 2 5-7"/>
            </svg>
          </span>
          <span>تحلیل و نمودارها</span>
        </button>

        <button
          type="button" class="result-tab review-tab"
          :class="{ active: activeTab === 'review' }"
          @click="activeTab = 'review'"
        >
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M4 4h16v16H4z"/><path d="M8 8h8"/>
              <path d="M8 12h8"/><path d="M8 16h5"/>
            </svg>
          </span>
          <span>مرور شخصی‌سازی‌شده</span>
          <small>{{ toPersianNumber(result.personalized_review?.length || 0) }}</small>
        </button>
      </nav>

      <!-- TAB: OVERVIEW -->
      <section v-if="activeTab === 'overview'" class="tab-content">

        <!-- Performance Signal -->
        <section class="signal-panel" :class="`signal-${performanceSignal.key}`">
          <div class="signal-radar">
            <span class="radar-ring r1"></span>
            <span class="radar-ring r2"></span>
            <span class="radar-ring r3"></span>
            <span class="radar-sweep"></span>
            <span class="radar-dot"></span>
          </div>

          <div class="signal-content">
            <span class="signal-label">سیگنال عملکرد</span>
            <h3 class="signal-title">{{ performanceSignal.title }}</h3>
            <p class="signal-desc">{{ performanceSignal.description }}</p>

            <div class="signal-bars">
              <span
                v-for="(bar, i) in 5"
                :key="i"
                class="signal-bar"
                :class="{ active: i < performanceSignal.strength }"
              ></span>
            </div>
          </div>

          <div class="signal-meta">
            <div class="signal-percent">
              <strong>{{ formatPercent(result.summary?.percentage) }}٪</strong>
              <span>درصد</span>
            </div>
            <div class="signal-rank">
              <strong>{{ formatRank(result.ranking?.national_rank) }}</strong>
              <span>رتبه</span>
            </div>
          </div>
        </section>

        <!-- Summary stats -->
        <div class="summary-grid">
          <div class="metric-card score-metric">
            <div class="metric-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 3v18"/><path d="M5 8h14"/><path d="M5 16h14"/>
              </svg>
            </div>
            <div class="metric-content">
              <span>درصد نهایی</span>
              <strong>{{ formatPercent(result.summary?.percentage) }}٪</strong>
              <small>با نمره منفی</small>
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
              <strong>{{ toPersianNumber(result.summary?.correct_count || 0) }}</strong>
              <small>سؤال</small>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon wrong">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m7 7 10 10"/><path d="m17 7-10 10"/>
              </svg>
            </div>
            <div class="metric-content">
              <span>پاسخ غلط</span>
              <strong>{{ toPersianNumber(result.summary?.wrong_count || 0) }}</strong>
              <small>سؤال</small>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon unanswered">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>
              </svg>
            </div>
            <div class="metric-content">
              <span>نزده</span>
              <strong>{{ toPersianNumber(result.summary?.unanswered_count || 0) }}</strong>
              <small>سؤال</small>
            </div>
          </div>
        </div>

        <!-- SMART INSIGHTS -->
        <section class="smart-insights">
          <div class="smart-insight accent-purple">
            <span class="smart-insight-icon">◈</span>
            <div><span>صدک عملکرد</span><strong>{{ formatPercent(percentile) }}٪</strong><small>بالاتر از {{ formatPercent(percentile) }}٪ شرکت‌کننده‌ها</small></div>
          </div>
          <div class="smart-insight accent-cyan">
            <span class="smart-insight-icon">✓</span>
            <div><span>دقت پاسخ‌ها</span><strong>{{ formatPercent(answerAccuracy) }}٪</strong><small>از پاسخ‌های داده‌شده</small></div>
          </div>
          <div class="smart-insight accent-orange">
            <span class="smart-insight-icon">!</span>
            <div><span>فرصت رشد</span><strong>{{ toPersianNumber(unansweredCount) }}</strong><small>سؤال نزده برای بررسی</small></div>
          </div>
          <div class="smart-insight accent-pink">
            <span class="smart-insight-icon">↑</span>
            <div><span>فاصله تا هدف</span><strong>{{ formatPercent(targetGap) }}٪</strong><small>تا هدف ۷۵٪ عملکرد</small></div>
          </div>
        </section>

        <!-- PERFORMANCE DNA -->
        <section class="performance-dna">
          <div class="dna-heading">
            <div>
              <span>DNA کارنامه</span>
              <h2>این نتیجه دقیقاً چه چیزی درباره عملکردت می‌گوید؟</h2>
            </div>
            <div class="dna-live"><i></i>تحلیل زنده</div>
          </div>

          <div class="dna-grid">
            <article class="dna-card dna-purple">
              <div class="dna-icon">↗</div>
              <div class="dna-copy"><span>قدرت حل سؤال</span><strong>{{ formatPercent(answerAccuracy) }}٪</strong><p>از سؤال‌هایی که جواب دادی، این درصد درست بوده.</p></div>
              <div class="dna-meter"><i :style="{ width: clampPercent(answerAccuracy) + '%' }"></i></div>
            </article>
            <article class="dna-card dna-cyan">
              <div class="dna-icon">◌</div>
              <div class="dna-copy"><span>کنترل ریسک</span><strong>{{ formatPercent(riskControl) }}٪</strong><p>{{ riskControlText }}</p></div>
              <div class="dna-meter"><i :style="{ width: clampPercent(riskControl) + '%' }"></i></div>
            </article>
            <article class="dna-card dna-orange">
              <div class="dna-icon">✦</div>
              <div class="dna-copy"><span>پتانسیل رشد</span><strong>{{ formatPercent(growthPotential) }}٪</strong><p>{{ growthPotentialText }}</p></div>
              <div class="dna-meter"><i :style="{ width: clampPercent(growthPotential) + '%' }"></i></div>
            </article>
          </div>
        </section>

        <!-- Performance Peak -->
        <section class="panel peak-panel">
          <div class="panel-heading">
            <div>
              <span>قله عملکرد</span>
              <h2>جایگاه شما در رقابت</h2>
            </div>
            <div class="peak-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m3 20 5-9 4 5 5-11 4 15"/>
                <path d="M3 20h18"/>
              </svg>
            </div>
          </div>

          <div class="peak-chart">
            <div class="peak-top-label">
              <span class="peak-badge">🏆 بالاترین</span>
              <span class="peak-badge-label">۱۰۰٪</span>
            </div>

            <div class="peak-track-wrap">
              <div class="peak-track"></div>
              <div class="peak-fill" :style="{ width: peakPosition + '%' }"></div>

              <div class="peak-marker" :style="{ right: peakPosition + '%' }">
                <div class="peak-marker-pulse"></div>
                <div class="peak-marker-dot">
                  <span>{{ formatPercent(result.summary?.percentage) }}٪</span>
                </div>
                <div class="peak-marker-arrow"></div>
              </div>

              <div class="peak-tick" style="right: 0%"><span>۰</span></div>
              <div class="peak-tick" style="right: 25%"><span>۲۵</span></div>
              <div class="peak-tick" style="right: 50%"><span>۵۰</span></div>
              <div class="peak-tick" style="right: 75%"><span>۷۵</span></div>
              <div class="peak-tick" style="right: 100%"><span>۱۰۰</span></div>
            </div>

            <div class="peak-bottom">
              <div class="peak-stat">
                <span>میانگین کشور</span>
                <strong>{{ formatPercent(nationalAverage) }}٪</strong>
                <div class="peak-stat-bar">
                  <div class="peak-stat-fill" :style="{ width: clampPercent(nationalAverage) + '%' }"></div>
                </div>
              </div>
              <div class="peak-stat">
                <span>بهترین دفترچه</span>
                <strong>{{ bestBooklet?.title || '—' }}</strong>
                <small v-if="bestBooklet">{{ formatPercent(bestBooklet.percentage) }}٪</small>
              </div>
              <div class="peak-stat">
                <span>ضعیف‌ترین دفترچه</span>
                <strong>{{ weakestBooklet?.title || '—' }}</strong>
                <small v-if="weakestBooklet">{{ formatPercent(weakestBooklet.percentage) }}٪</small>
              </div>
            </div>
          </div>
        </section>

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
                <strong>{{ formatRank(result.ranking?.national_rank) }}</strong>
                <small>از {{ toPersianNumber(result.ranking?.national_participants || 0) }} شرکت‌کننده</small>
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
                  <template v-if="result.ranking?.province">— {{ result.ranking.province }}</template>
                </span>
                <strong>{{ formatRank(result.ranking?.provincial_rank) }}</strong>
                <small>از {{ toPersianNumber(result.ranking?.provincial_participants || 0) }} شرکت‌کننده</small>
              </div>
            </div>
          </div>
        </section>

        <!-- League -->
        <section class="league-panel" :class="`league-${performanceLeague.key}`">
          <div class="league-bg-grid"></div>
          <div class="league-particles">
            <span v-for="n in 12" :key="n" :class="`particle particle-${n}`"></span>
          </div>

          <div class="league-head">
            <div>
              <span class="league-kicker">مسیر پیشرفت</span>
              <h2>لیگ عملکرد شما</h2>
              <p>جایگاهت بر اساس رتبه این آزمون در یک لیگ رقابتی نمایش داده می‌شود.</p>
            </div>
            <div class="league-season">
              <span class="season-dot"></span>
              <span>فصل جاری</span>
            </div>
          </div>

          <div class="league-main">
            <div class="league-emblem">
              <div class="emblem-aura"></div>
              <div class="emblem-ring ring-outer"></div>
              <div class="emblem-ring ring-mid"></div>
              <div class="emblem-ring ring-inner"></div>
              <div class="emblem-core">
                <svg
                  viewBox="0 0 64 64"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  v-html="performanceLeague.svgPath"
                ></svg>
              </div>
              <div class="emblem-shine"></div>
            </div>

            <div class="league-copy">
              <div class="league-title-row">
                <div>
                  <span class="league-label">لیگ فعلی</span>
                  <h3>{{ performanceLeague.title }}</h3>
                </div>
                <div class="league-rank-chip">
                  <span>رتبه</span>
                  <strong>{{ formatRank(result.ranking?.national_rank) }}</strong>
                </div>
              </div>

              <div class="league-progress-wrap">
                <div class="league-progress-labels">
                  <span>{{ performanceLeague.fromText }}</span>
                  <strong>{{ toPersianNumber(performanceLeague.progress) }}٪</strong>
                  <span>{{ performanceLeague.toText }}</span>
                </div>
                <div class="league-progress">
                  <div class="league-progress-fill" :style="{ width: performanceLeague.progress + '%' }"></div>
                  <i :style="{ right: `calc(${performanceLeague.progress}% - 7px)` }"></i>
                </div>
              </div>

              <!-- Distance to next league -->
              <div class="league-distance" v-if="performanceLeague.ranksToNext > 0">
                <div class="distance-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 19V5"/>
                    <path d="m5 12 7-7 7 7"/>
                  </svg>
                </div>
                <div class="distance-copy">
                  <span>تا لیگ بعدی</span>
                  <strong>
                    {{ toPersianNumber(performanceLeague.ranksToNext) }}
                    رتبه فاصله داری
                  </strong>
                </div>
                <div class="distance-target">{{ performanceLeague.nextTitle }}</div>
              </div>

              <div class="league-distance complete" v-else>
                <div class="distance-icon crown">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="m3 6 4 4 5-7 5 7 4-4-2 13H5L3 6Z"/>
                    <path d="M5 19h14"/>
                  </svg>
                </div>
                <div class="distance-copy">
                  <span>وضعیت</span>
                  <strong>به بالاترین لیگ رسیده‌ای 🎉</strong>
                </div>
              </div>

              <div class="league-foot">
                <div class="league-stat">
                  <span>شرکت‌کنندگان</span>
                  <strong>{{ toPersianNumber(result.ranking?.national_participants || 0) }}</strong>
                </div>
                <div class="league-stat">
                  <span>سطح لیگ</span>
                  <strong>{{ toPersianNumber(performanceLeague.level) }} / ۶</strong>
                </div>
                <div class="league-stat highlight">
                  <span>وضعیت</span>
                  <strong>{{ performanceLeague.caption }}</strong>
                </div>
              </div>
            </div>
          </div>

          <div class="league-track">
            <div
              v-for="tier in leagueTiers"
              :key="tier.key"
              class="tier"
              :class="{ active: tier.key === performanceLeague.key, passed: isTierPassed(tier.key) }"
            >
              <span class="tier-badge">
                <svg
                  viewBox="0 0 64 64"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  v-html="tier.svgPath"
                ></svg>
              </span>
              <span class="tier-name">{{ tier.title }}</span>
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
                <strong>{{ formatPercent(result.summary?.percentage) }}٪</strong>
              </div>
              <div class="progress-track">
                <div
                  class="progress-fill negative"
                  :style="{ width: clampPercent(result.summary?.percentage) + '%' }"
                ></div>
              </div>
              <small>معیار اصلی رتبه‌بندی</small>
            </div>

            <div class="raw-item">
              <div class="raw-label">
                <span>درصد خام</span>
                <strong>{{ formatPercent(result.summary?.raw_percentage) }}٪</strong>
              </div>
              <div class="progress-track">
                <div
                  class="progress-fill raw"
                  :style="{ width: clampPercent(result.summary?.raw_percentage) + '%' }"
                ></div>
              </div>
              <small>بدون اعمال نمره منفی</small>
            </div>
          </div>
        </section>

        <!-- Previous attempt -->
        <section v-if="result.previous_attempt" class="panel previous-panel">
          <div class="panel-heading">
            <div>
              <span>مقایسه با آزمون قبلی</span>
              <h2>{{ result.previous_attempt.exam_title }}</h2>
            </div>
            <div class="change-badge" :class="changeClass(result.previous_attempt.score_change)">
              {{ signedPercent(result.previous_attempt.score_change) }}
            </div>
          </div>

          <div class="previous-content">
            <div class="previous-score">
              <span>آزمون قبلی</span>
              <strong>{{ formatPercent(result.previous_attempt.score) }}٪</strong>
            </div>
            <div class="change-arrow">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
              </svg>
            </div>
            <div class="previous-score current">
              <span>این آزمون</span>
              <strong>{{ formatPercent(result.summary?.percentage) }}٪</strong>
            </div>
          </div>

          <div class="previous-details">
            <div>
              <span>تغییر درصد</span>
              <strong :class="changeTextClass(result.previous_attempt.score_change)">
                {{ signedPercent(result.previous_attempt.score_change) }}٪
              </strong>
            </div>
            <div>
              <span>تغییر درصد خام</span>
              <strong :class="changeTextClass(result.previous_attempt.raw_score_change)">
                {{ signedPercent(result.previous_attempt.raw_score_change) }}٪
              </strong>
            </div>
            <div>
              <span>درست قبلی</span>
              <strong>{{ toPersianNumber(result.previous_attempt.correct || 0) }}</strong>
            </div>
            <div>
              <span>غلط قبلی</span>
              <strong>{{ toPersianNumber(result.previous_attempt.wrong || 0) }}</strong>
            </div>
          </div>
        </section>
      </section>

      <!-- TAB: BOOKLETS -->
      <section v-if="activeTab === 'booklets'" class="tab-content">
        <div class="section-intro">
          <div>
            <span>تحلیل تفکیکی</span>
            <h2>عملکرد در دفترچه‌ها</h2>
            <p>عملکرد هر دفترچه را جداگانه بررسی کن و نقاط قوت و ضعف خودت را پیدا کن.</p>
          </div>
          <div class="booklet-total">
            <strong>{{ toPersianNumber(result.booklets?.length || 0) }}</strong>
            <span>دفترچه</span>
          </div>
        </div>

        <section class="booklet-spotlight">
          <div class="spotlight-main">
            <span class="spotlight-kicker">نقشه عملکرد دفترچه‌ها</span>
            <h2>از کجا امتیاز می‌گیری و کجا جا برای جهش داری؟</h2>
            <p>دفترچه‌ها بر اساس فاصله از میانگین کشور، دقت پاسخ و درصد نهایی قابل مقایسه‌اند.</p>
          </div>
          <div class="spotlight-podium">
            <div class="podium-item second">
              <span>میانگین</span><strong>{{ formatPercent(bookletAverage) }}٪</strong>
            </div>
            <div class="podium-item first">
              <span>قوی‌ترین</span><strong>{{ bestBooklet?.title || '—' }}</strong><small v-if="bestBooklet">{{ formatPercent(bestBooklet.percentage) }}٪</small>
            </div>
            <div class="podium-item third">
              <span>نیازمند توجه</span><strong>{{ weakestBooklet?.title || '—' }}</strong><small v-if="weakestBooklet">{{ formatPercent(weakestBooklet.percentage) }}٪</small>
            </div>
          </div>
        </section>

        <div class="booklet-toolbar">
          <div class="booklet-toolbar-copy"><span>مرتب‌سازی</span><strong>{{ bookletSort === 'score' ? 'از بهترین به ضعیف‌ترین' : 'به ترتیب دفترچه' }}</strong></div>
          <div class="booklet-sort-buttons">
            <button type="button" :class="{ active: bookletSort === 'order' }" @click="bookletSort = 'order'">ترتیب آزمون</button>
            <button type="button" :class="{ active: bookletSort === 'score' }" @click="bookletSort = 'score'">بیشترین درصد</button>
          </div>
        </div>

        <div class="booklet-cards">
          <article v-for="(booklet, bookletIndex) in sortedBooklets" :key="booklet.id" class="booklet-card" :style="{ '--booklet-score': clampPercent(booklet.percentage) + '%' }">
            <div class="booklet-card-top">
              <div class="booklet-number">{{ toPersianNumber(booklet.order) }}</div>
              <div class="booklet-title-wrap">
                <span>{{ booklet.subject || 'درس' }}</span>
                <h3>{{ booklet.title }}</h3>
              </div>
              <div class="booklet-rank-badge">#{{ toPersianNumber(bookletIndex + 1) }}</div>
              <div class="decile-badge">
                <span>دهک</span>
                <strong>{{ toPersianNumber(booklet.decile || 0) }}</strong>
              </div>
            </div>

            <div class="booklet-score-row">
              <div class="booklet-score-orb"><span>{{ formatPercent(booklet.percentage) }}٪</span></div>
              <div class="booklet-score">
                <strong>{{ formatPercent(booklet.percentage) }}٪</strong>
                <span>درصد با نمره منفی</span>
              </div>
              <div class="booklet-raw">
                <span>خام</span>
                <strong>{{ formatPercent(booklet.raw_percentage) }}٪</strong>
              </div>
            </div>

            <div class="booklet-bar">
              <div class="booklet-bar-fill" :style="{ width: positivePercent(booklet.percentage) + '%' }"></div>
              <span class="booklet-bar-label">{{ bookletGapText(booklet) }}</span>
            </div>

            <div class="answer-breakdown">
              <div class="answer-stat correct">
                <span class="answer-dot"></span>
                <span>درست</span>
                <strong>{{ toPersianNumber(booklet.correct) }}</strong>
              </div>
              <div class="answer-stat wrong">
                <span class="answer-dot"></span>
                <span>غلط</span>
                <strong>{{ toPersianNumber(booklet.wrong) }}</strong>
              </div>
              <div class="answer-stat unanswered">
                <span class="answer-dot"></span>
                <span>نزده</span>
                <strong>{{ toPersianNumber(booklet.unanswered) }}</strong>
              </div>
            </div>

            <div class="booklet-ranks">
              <div>
                <span>رتبه کشوری</span>
                <strong>{{ formatRank(booklet.national_rank) }}</strong>
                <small>از {{ toPersianNumber(booklet.national_participants) }}</small>
              </div>
              <div>
                <span>رتبه استانی</span>
                <strong>{{ formatRank(booklet.provincial_rank) }}</strong>
                <small>از {{ toPersianNumber(booklet.provincial_participants) }}</small>
              </div>
            </div>

            <div class="booklet-average">
              <div class="average-line">
                <span>میانگین کشور</span>
                <strong>{{ formatPercent(booklet.country_average) }}٪</strong>
              </div>
              <div class="average-track">
                <div class="average-user-marker" :style="{ right: markerPosition(booklet.percentage) }"></div>
                <div class="average-country-marker" :style="{ right: markerPosition(booklet.country_average) }"></div>
              </div>
              <div class="average-line province-line">
                <span>میانگین استان</span>
                <strong>{{ formatPercent(booklet.province_average) }}٪</strong>
              </div>
            </div>

            <div class="performance-message">
              <div class="performance-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 3v18"/><path d="M5 8h14"/><path d="M5 16h14"/>
                </svg>
              </div>
              <div>
                <strong>{{ booklet.performance_title }}</strong>
                <p>{{ booklet.performance_message }}</p>
              </div>
            </div>

            <div class="booklet-range">
              <span>سؤالات {{ toPersianNumber(booklet.start_question) }} تا {{ toPersianNumber(booklet.end_question) }}</span>
              <span>{{ toPersianNumber(booklet.question_count) }} سؤال</span>
            </div>
          </article>
        </div>
      </section>

      <!-- TAB: ANALYTICS -->
      <section v-if="activeTab === 'analytics'" class="tab-content">
        <div class="section-intro analytics-intro">
          <div>
            <span>اتاق کنترل عملکرد</span>
            <h2>نمودارها، بدون شلوغی اضافه</h2>
            <p>دو نمای واضح برای تحلیل نتیجه: مقایسه با میانگین‌ها و مسیر عملکرد.</p>
          </div>
          <div class="analytics-badge">
            <span class="analytics-live-dot"></span>
            تحلیل زنده
          </div>
        </div>

        <section class="panel chart-panel chartjs-panel">
          <div class="panel-heading">
            <div>
              <span>مقایسه هوشمند</span>
              <h2>تو در برابر میانگین‌ها</h2>
            </div>
            <div class="chart-mini-note">بر اساس درصد با نمره منفی</div>
          </div>
          <div v-if="bookletComparison.length" class="chartjs-wrap comparison-chartjs-wrap">
            <canvas ref="comparisonChartCanvas"></canvas>
          </div>
          <div v-else class="empty-chart">اطلاعات کافی برای نمایش نمودار وجود ندارد.</div>
        </section>

        <section class="panel chart-panel chartjs-panel">
          <div class="panel-heading">
            <div>
              <span>مسیر رشد</span>
              <h2>روند عملکردت در آزمون‌ها</h2>
            </div>
            <div v-if="previousChange !== null" class="trend-chip" :class="changeClass(previousChange)">
              {{ signedPercent(previousChange) }}٪
            </div>
          </div>
          <div v-if="progressData.length" class="chartjs-wrap progress-chartjs-wrap">
            <canvas ref="progressChartCanvas"></canvas>
          </div>
          <div v-else class="empty-chart">هنوز اطلاعات کافی برای نمایش روند وجود ندارد.</div>

          <div class="progress-summary">
            <div>
              <span>اولین عملکرد</span>
              <strong>{{ formatPercent(firstProgressScore) }}٪</strong>
            </div>
            <div>
              <span>آخرین عملکرد</span>
              <strong>{{ formatPercent(lastProgressScore) }}٪</strong>
            </div>
            <div>
              <span>تعداد آزمون‌ها</span>
              <strong>{{ toPersianNumber(progressData.length) }}</strong>
            </div>
          </div>
        </section>

        <section class="insights-grid">
          <div class="insight-card">
            <div class="insight-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m5 12 4 4L19 6"/></svg></div>
            <span>بهترین دفترچه</span>
            <strong>{{ bestBooklet?.title || '—' }}</strong>
            <small v-if="bestBooklet">{{ formatPercent(bestBooklet.percentage) }}٪</small>
          </div>
          <div class="insight-card">
            <div class="insight-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 3v18"/><path d="M5 8h14"/><path d="M5 16h14"/></svg></div>
            <span>نیازمند توجه</span>
            <strong>{{ weakestBooklet?.title || '—' }}</strong>
            <small v-if="weakestBooklet">{{ formatPercent(weakestBooklet.percentage) }}٪</small>
          </div>
          <div class="insight-card">
            <div class="insight-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="9"/><path d="M8 12h8"/></svg></div>
            <span>مجموع نزده‌ها</span>
            <strong>{{ toPersianNumber(result.summary?.unanswered_count || 0) }}</strong>
            <small>سؤال</small>
          </div>
        </section>
      </section>

      <!-- TAB: REVIEW -->
      <section v-if="activeTab === 'review'" class="tab-content">
        <div class="review-hero">
          <div class="review-hero-copy">
            <span class="review-kicker">مرور شخصی‌سازی‌شده</span>
            <h2>اشتباهاتت را به نقطه قوت تبدیل کن</h2>
            <p>صفحه هر سؤال را از دفترچه اصلی ببین، پاسخ خودت را با پاسخ صحیح مقایسه کن و مرور هدفمند داشته باش.</p>

            <div class="review-progress-row">
              <div class="review-progress-track">
                <div class="review-progress-fill" :style="{ width: reviewProgress + '%' }"></div>
              </div>
              <strong>{{ formatPercent(reviewProgress) }}٪ مرور انجام شد</strong>
            </div>
          </div>

          <div class="review-donut">
            <div class="review-donut-ring" :style="{ '--review-progress': `${reviewProgress}%` }">
              <div class="review-donut-center">
                <strong>{{ toPersianNumber(reviewCounts.correct) }}</strong>
                <span>درست</span>
              </div>
            </div>
          </div>
        </div>

        <div class="review-dashboard">
          <div class="review-stat-card total">
            <div class="review-stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="4" y="3" width="16" height="18" rx="2"/>
                <path d="M8 8h8"/><path d="M8 12h5"/>
              </svg>
            </div>
            <div>
              <span>کل سؤال‌ها</span>
              <strong>{{ toPersianNumber(result.personalized_review?.length || 0) }}</strong>
            </div>
          </div>
          <div class="review-stat-card correct">
            <div class="review-stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m5 12 4 4L19 6"/></svg>
            </div>
            <div>
              <span>پاسخ درست</span>
              <strong>{{ toPersianNumber(reviewCounts.correct) }}</strong>
            </div>
          </div>
          <div class="review-stat-card wrong">
            <div class="review-stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m7 7 10 10"/><path d="m17 7-10 10"/>
              </svg>
            </div>
            <div>
              <span>نیازمند مرور</span>
              <strong>{{ toPersianNumber(reviewCounts.wrong + reviewCounts.unanswered) }}</strong>
            </div>
          </div>
          <div class="review-stat-card unanswered">
            <div class="review-stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>
              </svg>
            </div>
            <div>
              <span>نزده</span>
              <strong>{{ toPersianNumber(reviewCounts.unanswered) }}</strong>
            </div>
          </div>
        </div>

        <div class="review-toolbar">
          <div class="review-toolbar-copy">
            <span>فیلتر مرور</span>
            <strong>{{ toPersianNumber(filteredReview.length) }} سؤال نمایش داده می‌شود</strong>
          </div>
          <div class="review-search">
            <span>⌕</span>
            <input v-model.trim="reviewSearch" type="search" placeholder="جستجو بر اساس شماره، درس یا دفترچه..." aria-label="جستجوی سؤال" />
            <button v-if="reviewSearch" type="button" @click="reviewSearch = ''">×</button>
          </div>
          <div class="review-filters">
            <button type="button" :class="{ active: reviewFilter === 'all' }" @click="setReviewFilter('all')">
              همه <span>{{ toPersianNumber(result.personalized_review?.length || 0) }}</span>
            </button>
            <button type="button" :class="{ active: reviewFilter === 'wrong' }" @click="setReviewFilter('wrong')">
              غلط <span>{{ toPersianNumber(reviewCounts.wrong) }}</span>
            </button>
            <button type="button" :class="{ active: reviewFilter === 'correct' }" @click="setReviewFilter('correct')">
              درست <span>{{ toPersianNumber(reviewCounts.correct) }}</span>
            </button>
            <button type="button" :class="{ active: reviewFilter === 'unanswered' }" @click="setReviewFilter('unanswered')">
              نزده <span>{{ toPersianNumber(reviewCounts.unanswered) }}</span>
            </button>
          </div>
        </div>

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
                <strong>{{ toPersianNumber(question.question_number) }}</strong>
              </div>
              <div class="question-context">
                <strong>{{ question.booklet_title || 'دفترچه' }}</strong>
                <span>{{ question.subject || '—' }}</span>
              </div>
              <div class="question-status" :class="question.status">
                <span class="status-dot"></span>
                {{ question.status === 'correct' ? 'درست' : question.status === 'wrong' ? 'غلط' : 'نزده' }}
              </div>
            </div>

            <div class="question-paper">
              <div class="question-paper-heading">
                <div>
                  <span>صورت سؤال</span>
                  <strong>صفحه {{ toPersianNumber(question.question_number) }}</strong>
                </div>
                <a
                  class="paper-open-link"
                  :href="questionPdfUrl(question.question_number)"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  مشاهده PDF
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M14 5h5v5"/><path d="M19 5 10 14"/>
                    <path d="M19 13v5a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>
                  </svg>
                </a>
              </div>

              <div class="question-pdf-frame">
                <div v-if="questionPdfLoading && !renderedQuestionPages.has(Number(question.question_number))" class="question-pdf-state">
                  <span class="pdf-loader"></span>
                  <span>در حال آماده‌سازی صفحه سؤال...</span>
                </div>
                <div v-if="questionPdfError" class="question-pdf-state error">
                  <strong>نمایش PDF ممکن نیست</strong>
                  <span>{{ questionPdfError }}</span>
                </div>
                <canvas
                  :ref="el => setQuestionCanvasRef(question.question_number, el)"
                  class="question-pdf-canvas"
                  :data-question="question.question_number"
                  :aria-label="`صفحه ${question.question_number} از PDF آزمون`"
                ></canvas>
              </div>
            </div>

            <div class="answer-comparison">
              <div class="answer-comparison-heading">
                <div>
                  <span>تحلیل پاسخ</span>
                  <strong>انتخاب شما در برابر پاسخ صحیح</strong>
                </div>
                <div class="answer-result-pill" :class="question.status">
                  {{ question.status === 'correct' ? 'پاسخ صحیح' : question.status === 'wrong' ? 'نیازمند مرور' : 'بدون پاسخ' }}
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
                    'selected-wrong': option.selected && !option.correct
                  }"
                >
                  <div class="option-number">{{ toPersianNumber(option.value) }}</div>
                  <div class="option-content">
                    <span>گزینه {{ toPersianNumber(option.value) }}</span>
                    <small v-if="option.selected">پاسخ شما</small>
                    <small v-if="option.correct" class="correct-label">پاسخ صحیح</small>
                  </div>
                  <div class="option-mark">
                    <svg v-if="option.correct" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="m5 12 4 4L19 6"/>
                    </svg>
                    <svg v-else-if="option.selected" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="m7 7 10 10"/><path d="m17 7-10 10"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <div class="question-answer-summary">
              <div>
                <span>پاسخ شما</span>
                <strong :class="{ empty: question.user_answer === null || question.user_answer === undefined }">
                  {{ question.user_answer ? `گزینه ${toPersianNumber(question.user_answer)}` : 'نزده' }}
                </strong>
              </div>
              <div>
                <span>پاسخ صحیح</span>
                <strong>
                  {{ question.correct_answer ? `گزینه ${toPersianNumber(question.correct_answer)}` : 'نامشخص' }}
                </strong>
              </div>
            </div>
          </article>

          <div v-if="filteredReview.length === 0" class="empty-review">
            <div class="empty-review-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 4h16v16H4z"/><path d="M8 8h8"/>
                <path d="M8 12h8"/><path d="M8 16h5"/>
              </svg>
            </div>
            <h3>سؤالی در این دسته وجود ندارد</h3>
            <p>فیلتر دیگری را امتحان کن.</p>
          </div>
        </div>
      </section>

      <button v-show="showScrollTop" type="button" class="scroll-top-button" aria-label="بازگشت به بالا" @click="scrollToTop">↑</button>

      <footer class="result-footer">
        <div>
          <strong>کارنامه دوپامین</strong>
          <span>تحلیل کن، یاد بگیر، بهتر شو.</span>
        </div>
        <button type="button" @click="goBack">
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
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  shallowRef,
  watch,
} from 'vue'

import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'
import Chart from 'chart.js/auto'

import * as pdfjsLib from 'pdfjs-dist'
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url'

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker

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
const bookletSort = ref('order')
const reviewSearch = ref('')
const showScrollTop = ref(false)

let themeObserver = null

/* =========================================================
   MOUSE
========================================================= */
const mx = ref(0)
const my = ref(0)

const mouseStyle = computed(() => ({
  '--mx': mx.value + 'px',
  '--my': my.value + 'px',
}))

function handleMouseMove(e) {
  mx.value = e.clientX
  my.value = e.clientY
}

/* =========================================================
   CHART.JS
========================================================= */
const comparisonChartCanvas = ref(null)
const progressChartCanvas = ref(null)
let comparisonChart = null
let progressChart = null

function destroyCharts() {
  comparisonChart?.destroy()
  progressChart?.destroy()
  comparisonChart = null
  progressChart = null
}

function chartPalette() {
  return {
    text: isDark.value ? '#aab4c6' : '#667085',
    grid: isDark.value ? 'rgba(145,151,255,.10)' : 'rgba(91,92,240,.08)',
    user: isDark.value ? '#9294ff' : '#5b5de6',
    country: isDark.value ? '#35cdb0' : '#18a88b',
    province: isDark.value ? '#f0bb54' : '#e3a62f',
    surface: isDark.value ? '#121824' : '#ffffff',
  }
}

async function initCharts() {
  if (activeTab.value !== 'analytics') return
  await nextTick()
  destroyCharts()

  const palette = chartPalette()
  const font = { family: 'Vazirmatn, IRANSans, Tahoma, sans-serif' }

  if (comparisonChartCanvas.value && bookletComparison.value.length) {
    comparisonChart = new Chart(comparisonChartCanvas.value, {
      type: 'bar',
      data: {
        labels: bookletComparison.value.map(item => truncate(item.booklet_title || 'دفترچه', 16)),
        datasets: [
          {
            label: 'شما',
            data: bookletComparison.value.map(item => Number(item.user_percentage || 0)),
            backgroundColor: palette.user,
            borderRadius: 8,
            borderSkipped: false,
            maxBarThickness: 24,
          },
          {
            label: 'میانگین کشور',
            data: bookletComparison.value.map(item => Number(item.country_average || 0)),
            backgroundColor: palette.country,
            borderRadius: 8,
            borderSkipped: false,
            maxBarThickness: 24,
          },
          {
            label: 'میانگین استان',
            data: bookletComparison.value.map(item => Number(item.province_average || 0)),
            backgroundColor: palette.province,
            borderRadius: 8,
            borderSkipped: false,
            maxBarThickness: 24,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 900, easing: 'easeOutQuart' },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            position: 'top',
            rtl: true,
            labels: {
              color: palette.text,
              font: { ...font, size: 11 },
              usePointStyle: true,
              pointStyle: 'circle',
              padding: 18,
            },
          },
          tooltip: {
            rtl: true,
            titleFont: { ...font, weight: '700' },
            bodyFont: { ...font },
            callbacks: {
              label: ctx => ` ${ctx.dataset.label}: ${formatPercent(ctx.raw)}٪`,
            },
          },
        },
        scales: {
          x: {
            ticks: { color: palette.text, font: { ...font, size: 10 } },
            grid: { display: false },
            border: { display: false },
          },
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              color: palette.text,
              font: { ...font, size: 9 },
              callback: value => `${value}٪`,
            },
            grid: { color: palette.grid },
            border: { display: false },
          },
        },
      },
    })
  }

  if (progressChartCanvas.value && progressData.value.length) {
    const gradient = progressChartCanvas.value.getContext('2d')?.createLinearGradient(0, 0, 0, 320)
    if (gradient) {
      gradient.addColorStop(0, isDark.value ? 'rgba(133,135,255,.28)' : 'rgba(101,103,241,.22)')
      gradient.addColorStop(1, 'rgba(101,103,241,0)')
    }

    progressChart = new Chart(progressChartCanvas.value, {
      type: 'line',
      data: {
        labels: progressData.value.map((item, index) => truncate(item.exam_title || `آزمون ${index + 1}`, 14)),
        datasets: [{
          label: 'درصد عملکرد',
          data: progressData.value.map(item => Number(item.percentage || 0)),
          borderColor: palette.user,
          backgroundColor: gradient || 'rgba(101,103,241,.12)',
          fill: true,
          tension: 0.38,
          borderWidth: 3,
          pointRadius: 4,
          pointHoverRadius: 7,
          pointBackgroundColor: palette.surface,
          pointBorderColor: palette.user,
          pointBorderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 1100, easing: 'easeOutQuart' },
        plugins: {
          legend: { display: false },
          tooltip: {
            rtl: true,
            titleFont: { ...font, weight: '700' },
            bodyFont: { ...font },
            callbacks: {
              label: ctx => ` درصد: ${formatPercent(ctx.raw)}٪`,
            },
          },
        },
        scales: {
          x: {
            ticks: { color: palette.text, font: { ...font, size: 10 }, maxRotation: 0 },
            grid: { display: false },
            border: { display: false },
          },
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              color: palette.text,
              font: { ...font, size: 9 },
              callback: value => `${value}٪`,
            },
            grid: { color: palette.grid },
            border: { display: false },
          },
        },
      },
    })
  }
}

/* =========================================================
   QUESTION PDF
========================================================= */
const questionPdfDocument = shallowRef(null)
const questionPdfLoading = ref(false)
const questionPdfError = ref('')

const questionCanvasRefs = new Map()
const questionRenderTasks = new Map()
const renderedQuestionPages = new Set()

let questionPdfLoadPromise = null

/* =========================================================
   THEME
========================================================= */
function detectDark() {
  const root = document.documentElement
  const body = document.body
  const dataTheme = root.getAttribute('data-theme') || body?.getAttribute('data-theme')

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
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style'],
  })
  if (document.body) {
    themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'data-theme', 'style'],
    })
  }
}

/* =========================================================
   LOAD RESULT
========================================================= */
async function loadResult() {
  loading.value = true
  errorMessage.value = ''

  try {
    const attemptId = route.params.id
    if (!attemptId) throw new Error('شناسه کارنامه پیدا نشد.')

    const response = await api.get(`/exams/attempts/${attemptId}/result/`)
    result.value = response.data
  } catch (error) {
    console.error('EXAM RESULT LOAD ERROR:', error)

    if (error?.response?.status === 401) {
      errorMessage.value = 'نشست شما منقضی شده است. دوباره وارد حساب کاربری شوید.'
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
const userInitials = computed(() => {
  const user = result.value?.user
  if (!user) return 'د'

  const first = user.first_name?.trim()?.charAt(0)
  const last = user.last_name?.trim()?.charAt(0)

  if (first || last) return `${first || ''}${last || ''}`
  return user.username?.charAt(0) || 'د'
})

/* =========================================================
   PERFORMANCE SIGNAL — سیگنال عملکرد
========================================================= */
const performanceSignal = computed(() => {
  const percentage = Number(result.value?.summary?.percentage || 0)
  const rank = Number(result.value?.ranking?.national_rank || 0)
  const total = Number(result.value?.ranking?.national_participants || 0)

  // محاسبه percentile (هر چه بالاتر بهتر)
  let percentile = 50
  if (rank && total) {
    percentile = ((total - rank + 1) / total) * 100
  }

  // ترکیب درصد و percentile
  const combinedScore = (percentage * 0.5) + (percentile * 0.5)

  // تعیین سطح
  if (combinedScore >= 90) {
    return {
      key: 'very-high',
      title: 'بسیار قوی',
      emoji: '📡',
      description: 'عملکردت در سطح نخبه‌های آزمون قرار داره؛ همین مسیر رو ادامه بده.',
      strength: 5,
    }
  }
  if (combinedScore >= 75) {
    return {
      key: 'rising',
      title: 'رو به رشد',
      emoji: '🔵',
      description: 'عملکردت بالاتر از میانگینه و مسیر خوبی رو داری طی می‌کنی.',
      strength: 4,
    }
  }
  if (combinedScore >= 55) {
    return {
      key: 'strong',
      title: 'قوی',
      emoji: '🟢',
      description: 'عملکردت متعادل و قابل قبوله؛ با کمی تلاش می‌تونی بالاتر بری.',
      strength: 3,
    }
  }
  if (combinedScore >= 35) {
    return {
      key: 'stable',
      title: 'پایدار',
      emoji: '🟡',
      description: 'عملکردت در محدوده متوسطه؛ روی نقاط ضعفت تمرکز کن.',
      strength: 2,
    }
  }
  if (combinedScore >= 20) {
    return {
      key: 'challenging',
      title: 'چالش‌برانگیز',
      emoji: '🟠',
      description: 'این آزمون سخت بوده برات؛ با مرور هدفمند می‌تونی بهتر بشی.',
      strength: 1,
    }
  }
  return {
    key: 'critical',
    title: 'نیاز به توجه',
    emoji: '🔴',
    description: 'نیاز به برنامه‌ریزی جدی داری؛ از همین امروز شروع کن.',
    strength: 1,
  }
})

/* =========================================================
   PEAK POSITION — موقعیت روی قله
========================================================= */
const peakPosition = computed(() => {
  return clampPercent(result.value?.summary?.percentage)
})

const nationalAverage = computed(() => {
  if (!sortedBooklets.value.length) return 0
  const sum = sortedBooklets.value.reduce(
    (acc, b) => acc + Number(b.country_average || 0),
    0
  )
  return sum / sortedBooklets.value.length
})

/* =========================================================
   LEAGUE TIERS — آیکون‌های کامل 64x64
========================================================= */
const leagueTiers = [
  {
    key: 'bronze',
    title: 'برنز',
    // مدال برنز
    svgPath: `
      <circle cx="32" cy="26" r="16" />
      <circle cx="32" cy="26" r="10" />
      <path d="M22 44v8M42 44v8M22 56h20" />
      <path d="m32 22 2 4h4l-3 3 1 4-4-2-4 2 1-4-3-3h4l2-4Z" fill="currentColor" opacity="0.4"/>
    `,
  },
  {
    key: 'silver',
    title: 'نقره‌ای',
    // سپر با ستاره
    svgPath: `
      <path d="M32 4 54 14v18c0 14-10 24-22 28C20 56 10 46 10 32V14L32 4Z" />
      <path d="M32 4 54 14v18c0 14-10 24-22 28V4Z" opacity="0.35" fill="currentColor"/>
      <path d="m32 18 3 7h7l-6 5 2 8-6-4-6 4 2-8-6-5h7l3-7Z" fill="currentColor" opacity="0.5"/>
    `,
  },
  {
    key: 'gold',
    title: 'طلایی',
    // جام قهرمانی
    svgPath: `
      <path d="M18 12h28v12c0 12-6 20-14 24-8-4-14-12-14-24V12Z" />
      <path d="M18 18H8c0 12 5 18 12 18M46 18h10c0 12-5 18-12 18" />
      <path d="M32 48v8M20 60h24" />
      <path d="m32 22 2.5 5h5.5l-4.5 3.5 1.5 5.5-5-3-5 3 1.5-5.5L24 27h5.5L32 22Z" fill="currentColor" opacity="0.55"/>
    `,
  },
  {
    key: 'platinum',
    title: 'پلاتینیوم',
    // کریستال شش‌ضلعی
    svgPath: `
      <path d="M32 4 54 18v28L32 60 10 46V18L32 4Z" />
      <path d="M32 4v56M10 18l44 28M54 18 10 46" opacity="0.4"/>
      <circle cx="32" cy="32" r="9" />
      <circle cx="32" cy="32" r="4" fill="currentColor"/>
      <path d="M32 4 54 18 32 32 10 18 32 4Z" fill="currentColor" opacity="0.2"/>
    `,
  },
  {
    key: 'diamond',
    title: 'الماس',
    // الماس تراش‌خورده
    svgPath: `
      <path d="M32 2 60 22 32 62 4 22 32 2Z" />
      <path d="M4 22h56M32 62V22M18 22 32 2l14 20" opacity="0.5"/>
      <path d="M22 32 32 26l10 6-10 12-10-12Z" fill="currentColor" opacity="0.55"/>
      <path d="M22 32h20M32 26v18" opacity="0.4"/>
    `,
  },
  {
    key: 'elite',
    title: 'نخبه',
    // تاج نخبه
    svgPath: `
      <path d="M8 22 18 32 32 8l14 24 10-10-4 30H12L8 22Z" />
      <path d="M12 52h40" stroke-width="2.5"/>
      <path d="M20 52v6M44 52v6" stroke-width="2"/>
      <circle cx="32" cy="40" r="4" fill="currentColor"/>
      <circle cx="32" cy="40" r="7" opacity="0.4"/>
      <path d="M32 30v-4M24 36l-3-3M40 36l3-3" opacity="0.7"/>
    `,
  },
]

const leagueOrder = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'elite']

const performanceLeague = computed(() => {
  const rank = Math.max(0, Number(result.value?.ranking?.national_rank || 0))
  const total = Math.max(rank, Number(result.value?.ranking?.national_participants || 0))

  if (!rank || !total) {
    return {
      key: 'bronze',
      title: 'لیگ برنز',
      level: 1,
      progress: 0,
      fromText: 'شروع',
      toText: 'رتبه‌های بالاتر',
      caption: 'در حال ثبت',
      svgPath: leagueTiers[0].svgPath,
      ranksToNext: 0,
      nextTitle: '',
    }
  }

  const percentile = Math.max(0, Math.min(100, ((total - rank + 1) / total) * 100))
  let tierIndex = 0
  if (percentile >= 99) tierIndex = 5
  else if (percentile >= 95) tierIndex = 4
  else if (percentile >= 85) tierIndex = 3
  else if (percentile >= 65) tierIndex = 2
  else if (percentile >= 35) tierIndex = 1

  const tier = leagueTiers[tierIndex]
  const thresholds = [0, 35, 65, 85, 95, 99]
  const start = thresholds[tierIndex]
  const end = tierIndex === 5 ? 100 : thresholds[tierIndex + 1]
  const progress = Math.round(Math.max(0, Math.min(100, ((percentile - start) / Math.max(1, end - start)) * 100)))

  // محاسبه فاصله تا لیگ بعدی
  let ranksToNext = 0
  let nextTitle = ''
  if (tierIndex < 5) {
    const nextThreshold = thresholds[tierIndex + 1]
    // rank لازم برای رسیدن به nextThreshold
    const targetRank = Math.ceil(total * (1 - nextThreshold / 100))
    ranksToNext = Math.max(0, rank - targetRank)
    nextTitle = leagueTiers[tierIndex + 1].title
  }

  return {
    key: tier.key,
    title: `لیگ ${tier.title}`,
    level: tierIndex + 1,
    progress,
    fromText: tierIndex === 0 ? 'آغاز مسیر' : `ورود به ${tier.title}`,
    toText: tierIndex === 5 ? 'اوج جدول' : `لیگ ${leagueTiers[tierIndex + 1].title}`,
    caption: percentile >= 99 ? 'نخبه جدول' : `جزو ${Math.max(1, Math.round(100 - percentile))}٪ برتر`,
    svgPath: tier.svgPath,
    ranksToNext,
    nextTitle,
  }
})

function isTierPassed(tierKey) {
  const currentIdx = leagueOrder.indexOf(performanceLeague.value.key)
  const tierIdx = leagueOrder.indexOf(tierKey)
  return tierIdx < currentIdx
}

/* =========================================================
   BOOKLETS
========================================================= */
const sortedBooklets = computed(() => {
  const list = Array.isArray(result.value?.booklets) ? [...result.value.booklets] : []
  if (bookletSort.value === 'score') {
    return list.sort((a, b) => Number(b.percentage || 0) - Number(a.percentage || 0))
  }
  return list.sort((a, b) => Number(a.order || 0) - Number(b.order || 0))
})

const bookletComparison = computed(() => {
  const data = result.value?.charts?.booklet_comparison
  if (Array.isArray(data)) return data

  return sortedBooklets.value.map(booklet => ({
    booklet_id: booklet.id,
    booklet_title: booklet.title,
    user_percentage: booklet.percentage,
    user_raw_percentage: booklet.raw_percentage,
    country_average: booklet.country_average,
    province_average: booklet.province_average,
  }))
})

const bestBooklet = computed(() => {
  if (!sortedBooklets.value.length) return null
  return [...sortedBooklets.value].sort((a, b) => Number(b.percentage || 0) - Number(a.percentage || 0))[0]
})

const weakestBooklet = computed(() => {
  if (!sortedBooklets.value.length) return null
  return [...sortedBooklets.value].sort((a, b) => Number(a.percentage || 0) - Number(b.percentage || 0))[0]
})

/* =========================================================
   PROGRESS
========================================================= */
const progressData = computed(() => {
  const data = result.value?.charts?.progress || result.value?.progress || []
  if (!Array.isArray(data)) return []
  return data
})

const firstProgressScore = computed(() => {
  if (!progressData.value.length) return 0
  return Number(progressData.value[0].percentage || 0)
})

const lastProgressScore = computed(() => {
  if (!progressData.value.length) return 0
  return Number(progressData.value[progressData.value.length - 1].percentage || 0)
})

const previousChange = computed(() => {
  const value = result.value?.previous_attempt?.score_change
  if (value === null || value === undefined) return null
  return Number(value)
})

/* =========================================================
   SMART METRICS
========================================================= */
const percentile = computed(() => {
  const rank = Number(result.value?.ranking?.national_rank || 0)
  const total = Number(result.value?.ranking?.national_participants || 0)
  if (!rank || !total) return 0
  return Math.max(0, Math.min(100, ((total - rank + 1) / total) * 100))
})

const answeredCount = computed(() => {
  const correct = Number(result.value?.summary?.correct_count || 0)
  const wrong = Number(result.value?.summary?.wrong_count || 0)
  return correct + wrong
})

const unansweredCount = computed(() => Number(result.value?.summary?.unanswered_count || 0))

const answerAccuracy = computed(() => {
  if (!answeredCount.value) return 0
  return (Number(result.value?.summary?.correct_count || 0) / answeredCount.value) * 100
})

const targetGap = computed(() => {
  const score = Number(result.value?.summary?.percentage || 0)
  return Math.max(0, 75 - score)
})

const riskControl = computed(() => {
  const answered = answeredCount.value
  if (!answered) return 0
  const wrong = Number(result.value?.summary?.wrong_count || 0)
  return Math.max(0, Math.min(100, 100 - (wrong / answered) * 100))
})

const riskControlText = computed(() => {
  const wrong = Number(result.value?.summary?.wrong_count || 0)
  if (!answeredCount.value) return 'هنوز پاسخ ثبت‌شده‌ای برای تحلیل وجود ندارد.'
  if (wrong === 0) return 'هیچ پاسخ غلطی ثبت نشده؛ کنترل ریسک فوق‌العاده بوده.'
  return `${toPersianNumber(wrong)} پاسخ غلط داشته‌ای؛ مرور خطاها بیشترین اثر را دارد.`
})

const growthPotential = computed(() => {
  const unanswered = unansweredCount.value
  const score = Number(result.value?.summary?.percentage || 0)
  const unansweredBoost = Math.min(55, unanswered * 4)
  const targetBoost = Math.min(45, Math.max(0, 75 - score))
  return Math.max(0, Math.min(100, unansweredBoost + targetBoost))
})

const growthPotentialText = computed(() => {
  if (unansweredCount.value > 0) return `${toPersianNumber(unansweredCount.value)} سؤال بدون پاسخ، بزرگ‌ترین فضای رشد فوری توست.`
  if (targetGap.value > 0) return `تا هدف ۷۵٪ هنوز ${formatPercent(targetGap.value)}٪ فاصله داری.`
  return 'به هدف ۷۵٪ رسیده‌ای؛ حالا هدف بعدی را بالاتر بگذار.'
})

const bookletAverage = computed(() => {
  if (!sortedBooklets.value.length) return 0
  return sortedBooklets.value.reduce((sum, booklet) => sum + Number(booklet.percentage || 0), 0) / sortedBooklets.value.length
})

function bookletGap(booklet) {
  const value = Number(booklet?.percentage || 0) - Number(booklet?.country_average || 0)
  return Number.isFinite(value) ? value : 0
}

function bookletGapText(booklet) {
  const gap = bookletGap(booklet)
  if (gap > 0) return `${signedPercent(gap)}٪ بالاتر از میانگین کشور`
  if (gap < 0) return `${signedPercent(gap)}٪ پایین‌تر از میانگین کشور`
  return 'برابر با میانگین کشور'
}

/* =========================================================
   SCORE RING
========================================================= */
const scoreDash = computed(() => {
  const radius = 50
  const circumference = 2 * Math.PI * radius
  const percentage = clampPercent(result.value?.summary?.percentage)
  const visible = circumference * (percentage / 100)
  return `${visible} ${circumference}`
})

/* =========================================================
   REVIEW
========================================================= */
const reviewCounts = computed(() => {
  const review = Array.isArray(result.value?.personalized_review) ? result.value.personalized_review : []
  return {
    correct: review.filter(item => item.status === 'correct').length,
    wrong: review.filter(item => item.status === 'wrong').length,
    unanswered: review.filter(item => item.status === 'unanswered').length,
  }
})

const filteredReview = computed(() => {
  const review = Array.isArray(result.value?.personalized_review) ? result.value.personalized_review : []
  const query = reviewSearch.value.toLocaleLowerCase('fa-IR').trim()
  return review.filter(item => {
    const matchesFilter = reviewFilter.value === 'all' || item.status === reviewFilter.value
    if (!matchesFilter) return false
    if (!query) return true
    const haystack = [item.question_number, item.booklet_title, item.subject, item.status].filter(Boolean).join(' ').toLocaleLowerCase('fa-IR')
    return haystack.includes(query)
  })
})

function setReviewFilter(filter) {
  reviewFilter.value = filter
}

const reviewProgress = computed(() => {
  const total = Number(result.value?.personalized_review?.length || 0)
  if (!total) return 0
  return Math.round((reviewCounts.value.correct / total) * 100)
})

/* =========================================================
   PDF HELPERS
========================================================= */
function questionPdfUrl(questionNumber) {
  const number = Number(questionNumber)
  if (!Number.isInteger(number) || number < 1) {
    return result.value.exam.question_pdf_url
  }
  return `${result.value.exam.question_pdf_url}#page=${number}`
}

function setQuestionCanvasRef(questionNumber, element) {
  const number = Number(questionNumber)
  if (!Number.isInteger(number) || number < 1) return

  if (element) {
    questionCanvasRefs.set(number, element)
  } else {
    questionCanvasRefs.delete(number)
  }
}

async function loadQuestionPdf() {
  if (questionPdfDocument.value) return questionPdfDocument.value
  if (questionPdfLoadPromise) return questionPdfLoadPromise

  questionPdfLoading.value = true
  questionPdfError.value = ''

  questionPdfLoadPromise = pdfjsLib
    .getDocument({
      url: result.value.exam.question_pdf_url,
      withCredentials: false,
    })
    .promise
    .then(pdf => {
      questionPdfDocument.value = pdf
      return pdf
    })
    .catch(error => {
      console.error('QUESTION PDF LOAD ERROR:', error)
      questionPdfError.value = 'فایل PDF آزمون بارگذاری نشد. آدرس PDF یا تنظیمات CORS سرور را بررسی کنید.'
      throw error
    })
    .finally(() => {
      questionPdfLoading.value = false
      questionPdfLoadPromise = null
    })

  return questionPdfLoadPromise
}

async function renderQuestionPage(questionNumber, force = false) {
  const number = Number(questionNumber)
  const canvas = questionCanvasRefs.get(number)

  if (!Number.isInteger(number) || number < 1 || !canvas) return

  if (!force && renderedQuestionPages.has(number)) {
    const ctx = canvas.getContext('2d')
    if (canvas.width > 0 && canvas.height > 0 && ctx) return
    renderedQuestionPages.delete(number)
  }

  const previousTask = questionRenderTasks.get(number)
  if (previousTask) {
    try { previousTask.cancel() } catch { /* ignore */ }
  }

  try {
    const pdf = await loadQuestionPdf()

    if (number > pdf.numPages) {
      throw new Error(`PDF فقط ${pdf.numPages} صفحه دارد؛ صفحه ${number} وجود ندارد.`)
    }

    const page = await pdf.getPage(number)
    const container = canvas.parentElement
    if (!container) return

    const baseViewport = page.getViewport({ scale: 1 })
    const availableWidth = Math.max(280, container.clientWidth - 2)
    const scale = Math.min(1.75, availableWidth / baseViewport.width)
    const viewport = page.getViewport({ scale })
    const outputScale = Math.min(window.devicePixelRatio || 1, 2)

    canvas.width = Math.floor(viewport.width * outputScale)
    canvas.height = Math.floor(viewport.height * outputScale)
    canvas.style.width = `${Math.floor(viewport.width)}px`
    canvas.style.height = `${Math.floor(viewport.height)}px`

    const context = canvas.getContext('2d', { alpha: false })
    if (!context) throw new Error('Canvas 2D context is unavailable.')

    context.setTransform(outputScale, 0, 0, outputScale, 0, 0)
    context.fillStyle = '#ffffff'
    context.fillRect(0, 0, viewport.width, viewport.height)

    const renderTask = page.render({
      canvasContext: context,
      viewport,
    })

    questionRenderTasks.set(number, renderTask)
    await renderTask.promise
    renderedQuestionPages.add(number)
  } catch (error) {
    if (error?.name === 'RenderingCancelledException') return
    console.error(`QUESTION PDF PAGE ${number} RENDER ERROR:`, error)
    questionPdfError.value = 'نمایش صفحه این سؤال با خطا مواجه شد.'
  } finally {
    questionRenderTasks.delete(number)
  }
}

function resetQuestionRendering() {
  for (const task of questionRenderTasks.values()) {
    try { task.cancel() } catch { /* already completed */ }
  }
  questionRenderTasks.clear()
  renderedQuestionPages.clear()
  questionPdfError.value = ''
}

async function renderFilteredQuestionPages() {
  if (activeTab.value !== 'review') return
  await nextTick()
  if (!filteredReview.value.length) return

  try {
    await loadQuestionPdf()
  } catch {
    return
  }

  for (const question of filteredReview.value) {
    const number = Number(question.question_number)
    const canvas = questionCanvasRefs.get(number)
    if (canvas) {
      canvas.width = 0
      canvas.height = 0
      renderedQuestionPages.delete(number)
    }
  }

  await nextTick()

  for (const question of filteredReview.value) {
    await renderQuestionPage(question.question_number, true)
  }
}

/* =========================================================
   FORMATTERS
========================================================= */
function toPersianNumber(value) {
  if (value === null || value === undefined) return '۰'
  return String(value).replace(/\d/g, digit => '۰۱۲۳۴۵۶۷۸۹'[Number(digit)])
}

function formatPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '۰'
  return number.toFixed(1).replace(/\.0$/, '').replace(/-/g, '−')
}

function clampPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return 0
  return Math.max(0, Math.min(100, number))
}

function positivePercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return 0
  return Math.max(0, Math.min(100, number))
}

function signedPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '۰'
  const absolute = Math.abs(number)
  const formatted = formatPercent(absolute)
  if (number > 0) return `+${formatted}`
  if (number < 0) return `−${formatted}`
  return '۰'
}

function formatRank(value) {
  if (value === null || value === undefined || value === '') return '—'
  return toPersianNumber(value)
}

function formatDate(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleDateString('fa-IR-u-ca-persian', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

function formatTime(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleTimeString('fa-IR', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  })
}

function truncate(value, length) {
  if (!value) return ''
  const text = String(value)
  if (text.length <= length) return text
  return text.slice(0, length) + '…'
}

function markerPosition(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '0%'
  return `${Math.max(0, Math.min(100, number))}%`
}

function changeClass(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return 'neutral'
  if (number > 0) return 'positive'
  if (number < 0) return 'negative'
  return 'neutral'
}

function changeTextClass(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return ''
  if (number > 0) return 'text-positive'
  if (number < 0) return 'text-negative'
  return ''
}

async function shareResult() {
  const title = result.value?.exam?.title || 'کارنامه آزمون'
  const text = `کارنامه ${title} — درصد: ${formatPercent(result.value?.summary?.percentage)}٪`
  try {
    if (navigator.share) {
      await navigator.share({ title, text, url: window.location.href })
    } else if (navigator.clipboard) {
      await navigator.clipboard.writeText(window.location.href)
      window.alert('لینک کارنامه کپی شد.')
    }
  } catch (error) {
    if (error?.name !== 'AbortError') console.error('SHARE ERROR:', error)
  }
}

function printResult() {
  window.print()
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleScroll() {
  showScrollTop.value = window.scrollY > 700
}

async function goBack() {
  try {
    await router.push({ name: 'exams' })
  } catch {
    router.back()
  }
}

/* =========================================================
   WATCHERS
========================================================= */
watch(
  () => activeTab.value,
  async value => {
    if (value === 'review') {
      resetQuestionRendering()
      await renderFilteredQuestionPages()
    } else if (value === 'analytics') {
      await initCharts()
    } else {
      destroyCharts()
    }
  }
)

watch(
  () => reviewFilter.value,
  async () => {
    if (activeTab.value === 'review') {
      resetQuestionRendering()
      await renderFilteredQuestionPages()
    }
  }
)

/* =========================================================
   MOUNT / UNMOUNT
========================================================= */
onMounted(async () => {
  observeTheme()
  window.addEventListener('scroll', handleScroll, { passive: true })
  await loadResult()

  if (activeTab.value === 'review') {
    await renderFilteredQuestionPages()
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
  themeObserver?.disconnect()
  themeObserver = null
  destroyCharts()

  for (const task of questionRenderTasks.values()) {
    try { task.cancel() } catch { /* ignore */ }
  }

  questionRenderTasks.clear()
  questionCanvasRefs.clear()
  renderedQuestionPages.clear()

  if (questionPdfDocument.value) {
    questionPdfDocument.value.destroy()
    questionPdfDocument.value = null
  }
})
</script>

<style scoped>
/* =========================================================
   DOPAMINE • EXAM RESULT — PREMIUM
========================================================= */

.exam-result-page {
  --bg: #f4f6fc;
  --surface: rgba(255, 255, 255, .9);
  --surface-solid: #ffffff;
  --surface-soft: #f8f9fd;
  --text: #14172a;
  --text-soft: #5e6781;
  --text-faint: #98a2b3;
  --border: rgba(91, 92, 240, .10);
  --border-strong: rgba(91, 92, 240, .2);

  --primary: #6567f1;
  --primary-dark: #4d4fd8;
  --primary-light: #8c8eff;
  --primary-soft: rgba(101, 103, 241, .10);

  --success: #18a88b;
  --success-soft: rgba(24, 168, 139, .10);
  --danger: #e35d68;
  --danger-soft: rgba(227, 93, 104, .10);
  --warning: #e3a62f;
  --warning-soft: rgba(227, 166, 47, .11);
  --orange: #f0862f;
  --orange-soft: rgba(240, 134, 47, .11);

  --shadow-sm: 0 8px 28px rgba(32, 35, 70, .06);
  --shadow: 0 18px 55px rgba(32, 35, 70, .09);
  --shadow-lg: 0 30px 90px rgba(53, 56, 145, .16);

  --mx: 50vw;
  --my: 50vh;

  position: relative;
  isolation: isolate;
  min-height: 100vh;
  overflow: hidden;
  padding: 30px 20px 70px;
  color: var(--text);
  background: linear-gradient(180deg, #f6f7fd 0%, var(--bg) 40%, #eef0f9 100%);
  transition: background .4s ease, color .35s ease;
}

.exam-result-page.is-dark {
  --bg: #080b13;
  --surface: rgba(18, 24, 36, .85);
  --surface-solid: #121824;
  --surface-soft: #0e1520;
  --text: #f4f6fb;
  --text-soft: #aab4c6;
  --text-faint: #6d7789;
  --border: rgba(145, 151, 255, .12);
  --border-strong: rgba(145, 151, 255, .24);

  --primary: #8587ff;
  --primary-dark: #6f71f5;
  --primary-light: #a6a7ff;
  --primary-soft: rgba(133,135,255,.13);

  --success: #2ac7a6;
  --danger: #ff7180;
  --warning: #efb84e;
  --orange: #ff9a4a;
  --orange-soft: rgba(255, 154, 74, .14);

  --shadow-sm: 0 10px 32px rgba(0,0,0,.18);
  --shadow: 0 20px 60px rgba(0,0,0,.26);
  --shadow-lg: 0 35px 100px rgba(0,0,0,.4);

  background: linear-gradient(180deg, #0a0e18 0%, #080b13 100%);
}

.exam-result-page *,
.exam-result-page *::before,
.exam-result-page *::after {
  box-sizing: border-box;
}

.exam-result-page button,
.exam-result-page a {
  -webkit-tap-highlight-color: transparent;
}

.exam-result-page button:focus-visible,
.exam-result-page a:focus-visible {
  outline: 3px solid rgba(101,103,241,.3);
  outline-offset: 3px;
}

/* =========================================================
   SIMPLE BACKGROUND (grid + spotlight)
========================================================= */

.bg-layer {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(101, 103, 241, .05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(101, 103, 241, .05) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: radial-gradient(circle at var(--mx) var(--my), black 0%, transparent 65%);
  -webkit-mask-image: radial-gradient(circle at var(--mx) var(--my), black 0%, transparent 65%);
}

.is-dark .bg-grid {
  background-image:
    linear-gradient(rgba(133, 135, 255, .07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(133, 135, 255, .07) 1px, transparent 1px);
}

.bg-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    700px circle at var(--mx) var(--my),
    rgba(101, 103, 241, .07),
    transparent 45%
  );
}

.is-dark .bg-glow {
  background: radial-gradient(
    700px circle at var(--mx) var(--my),
    rgba(133, 135, 255, .09),
    transparent 45%
  );
}

/* =========================================================
   LOADING / ERROR
========================================================= */

.page-state {
  min-height: calc(100vh - 100px);
  display: grid;
  place-items: center;
  align-content: center;
  gap: 9px;
  text-align: center;
  animation: pageReveal .65s ease both;
}

.page-state h2 {
  margin: 14px 0 0;
  font-size: clamp(21px, 3vw, 29px);
  letter-spacing: -.04em;
}

.page-state p {
  max-width: 520px;
  margin: 0;
  color: var(--text-soft);
  font-size: 12px;
  line-height: 2;
}

.loading-orb {
  position: relative;
  width: 74px;
  height: 74px;
  display: grid;
  place-items: center;
}

.loading-orb::before {
  content: "";
  position: absolute;
  inset: 0;
  border: 1px solid var(--border-strong);
  border-radius: 50%;
  box-shadow: 0 0 0 12px var(--primary-soft), 0 18px 50px rgba(101,103,241,.16);
  animation: orbPulse 1.8s ease-in-out infinite;
}

.loading-orb::after {
  content: "";
  width: 22px;
  height: 22px;
  border: 3px solid rgba(255,255,255,.18);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin .75s linear infinite;
}

.loading-orb span {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--primary);
  box-shadow: 0 0 16px var(--primary);
  animation: orbit 1.8s linear infinite;
}

.loading-orb span:nth-child(2) { animation-delay: -.6s; }
.loading-orb span:nth-child(3) { animation-delay: -1.2s; }

.state-icon {
  width: 72px;
  height: 72px;
  display: grid;
  place-items: center;
  border-radius: 24px;
  color: var(--danger);
  background: var(--danger-soft);
  box-shadow: var(--shadow);
}

.state-icon svg { width: 32px; height: 32px; }

.retry-button {
  margin-top: 12px;
  padding: 11px 18px;
  border: 1px solid var(--border-strong);
  border-radius: 13px;
  color: #fff;
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  font-weight: 850;
  box-shadow: 0 10px 25px rgba(101,103,241,.2);
  transition: transform .22s ease, box-shadow .22s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 34px rgba(101,103,241,.28);
}

/* =========================================================
   MAIN CONTAINER
========================================================= */

.result-container {
  width: min(1180px, 100%);
  margin-inline: auto;
  animation: pageReveal .7s cubic-bezier(.2,.8,.2,1) both;
}

.hero-card,
.panel,
.metric-card,
.booklet-card,
.review-hero,
.review-stat-card,
.review-toolbar,
.question-card,
.result-tabs,
.insight-card,
.signal-panel {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* =========================================================
   HERO
========================================================= */

.hero-card {
  position: relative;
  overflow: hidden;
  padding: 34px;
  border: 1px solid rgba(255,255,255,.16);
  border-radius: 36px;
  color: #fff;
  background:
    radial-gradient(circle at 12% 20%, rgba(255,255,255,.18), transparent 18rem),
    radial-gradient(circle at 88% 82%, rgba(170,150,255,.24), transparent 20rem),
    linear-gradient(135deg, #2b2da0 0%, #5557e8 45%, #7779ff 100%);
  box-shadow: var(--shadow-lg);
}

.hero-card::before {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgba(255,255,255,.09);
  pointer-events: none;
}

.hero-aurora {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 40% at 20% 10%, rgba(180, 200, 255, .35), transparent),
    radial-gradient(ellipse 50% 50% at 80% 90%, rgba(180, 140, 255, .3), transparent);
  filter: blur(20px);
  opacity: .7;
  animation: auroraShift 12s ease-in-out infinite alternate;
  pointer-events: none;
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.04) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 30px;
}

.back-button {
  position: relative;
  z-index: 3;
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  margin-bottom: 24px;
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 15px;
  color: #fff;
  background: rgba(255,255,255,.1);
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 8px 20px rgba(0,0,0,.12);
  transition: transform .25s ease, background .25s ease;
}

.back-button:hover {
  transform: translateX(4px);
  background: rgba(255,255,255,.18);
}

.back-button svg { width: 20px; height: 20px; }

.hero-user {
  display: flex;
  align-items: center;
  gap: 18px;
  min-width: 0;
}

.avatar-wrap {
  position: relative;
  width: 78px;
  height: 78px;
  flex: 0 0 78px;
  padding: 3px;
  border-radius: 26px;
  background: linear-gradient(145deg, rgba(255,255,255,.85), rgba(255,255,255,.2));
  box-shadow: 0 14px 35px rgba(22,24,100,.25);
  animation: avatarIn .8s cubic-bezier(.2,.8,.2,1) both;
}

.avatar-image,
.avatar-fallback {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  border-radius: 23px;
  object-fit: cover;
  background: rgba(255,255,255,.16);
}

.avatar-fallback { font-size: 25px; font-weight: 950; }

.avatar-status {
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 16px;
  height: 16px;
  border: 3px solid #5557e8;
  border-radius: 50%;
  background: #36d6b1;
  box-shadow: 0 0 0 5px rgba(54,214,177,.12), 0 0 18px rgba(54,214,177,.5);
  animation: statusPulse 2s ease-in-out infinite;
}

.hero-user-info { min-width: 0; }

.hero-eyebrow,
.review-kicker {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: rgba(255,255,255,.75);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: .04em;
}

.hero-eyebrow::before,
.review-kicker::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #b8b9ff;
  box-shadow: 0 0 0 5px rgba(255,255,255,.07), 0 0 14px #b8b9ff;
}

.hero-user-info h1 {
  max-width: 650px;
  margin: 7px 0 4px;
  overflow: hidden;
  font-size: clamp(22px, 4vw, 36px);
  line-height: 1.25;
  letter-spacing: -.045em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero-user-info p {
  margin: 0;
  color: rgba(255,255,255,.7);
  font-size: 12px;
}

.hero-score {
  position: relative;
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: scoreIn .8s cubic-bezier(.2,.8,.2,1) .12s both;
}

.score-ring {
  position: relative;
  width: 158px;
  height: 158px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  filter: drop-shadow(0 18px 32px rgba(15,17,85,.25));
}

.score-ring::before {
  content: "";
  position: absolute;
  inset: 10px;
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 50%;
  box-shadow: inset 0 0 30px rgba(255,255,255,.08);
}

.score-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
  overflow: visible;
}

.score-track {
  fill: none;
  stroke: rgba(255,255,255,.15);
  stroke-width: 8;
}

.score-progress {
  fill: none;
  stroke: url(#scoreGrad);
  stroke-width: 8;
  stroke-linecap: round;
  filter: drop-shadow(0 0 10px rgba(255,255,255,.55));
  transition: stroke-dasharray 1.2s cubic-bezier(.2,.8,.2,1);
}

.score-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-center strong {
  font-size: 34px;
  line-height: 1;
  font-weight: 950;
  letter-spacing: -.04em;
  text-shadow: 0 2px 12px rgba(0,0,0,.15);
}

.score-center span {
  margin-top: 7px;
  color: rgba(255,255,255,.72);
  font-size: 11px;
}

.score-caption {
  margin-top: 9px;
  color: rgba(255,255,255,.65);
  font-size: 10px;
}

.hero-bottom {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-top: 28px;
  padding-top: 18px;
  border-top: 1px solid rgba(255,255,255,.14);
  color: rgba(255,255,255,.72);
  font-size: 10px;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hero-meta-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #52dfbe;
  box-shadow: 0 0 12px rgba(82,223,190,.85);
}

.meta-separator { opacity: .4; }

/* =========================================================
   TABS
========================================================= */

.result-tabs {
  position: sticky;
  top: 14px;
  z-index: 20;
  display: flex;
  gap: 7px;
  overflow-x: auto;
  margin: 20px 0;
  padding: 7px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: color-mix(in srgb, var(--surface-solid) 85%, transparent);
  box-shadow: var(--shadow-sm);
  scrollbar-width: none;
}

.result-tabs::-webkit-scrollbar { display: none; }

.result-tab {
  position: relative;
  flex: 1 0 auto;
  min-width: max-content;
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 11px 17px;
  border: 0;
  border-radius: 16px;
  color: var(--text-soft);
  background: transparent;
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  font-weight: 750;
  transition: color .22s ease, background .22s ease, transform .22s ease;
}

.result-tab:hover {
  color: var(--text);
  background: var(--surface-soft);
  transform: translateY(-1px);
}

.result-tab.active {
  color: var(--primary);
  background: var(--primary-soft);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.5), 0 8px 22px rgba(101,103,241,.12);
}

.tab-icon {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border-radius: 10px;
  background: rgba(101,103,241,.08);
  transition: transform .3s cubic-bezier(.2,.8,.2,1);
}

.result-tab:hover .tab-icon,
.result-tab.active .tab-icon {
  transform: translateY(-2px) scale(1.08);
}

.result-tab.active .tab-icon {
  background: rgba(101,103,241,.16);
  box-shadow: 0 0 0 5px rgba(101,103,241,.05);
}

.tab-icon svg { width: 17px; height: 17px; }

.result-tab small {
  min-width: 20px;
  padding: 3px 6px;
  border-radius: 7px;
  color: var(--primary);
  background: var(--primary-soft);
  font-size: 9px;
  font-weight: 900;
}

/* =========================================================
   TAB CONTENT
========================================================= */

.tab-content {
  animation: tabIn .5s cubic-bezier(.2,.8,.2,1) both;
}

.tab-content > * {
  animation: itemIn .55s cubic-bezier(.2,.8,.2,1) both;
}

.tab-content > *:nth-child(2) { animation-delay: .05s; }
.tab-content > *:nth-child(3) { animation-delay: .1s; }
.tab-content > *:nth-child(4) { animation-delay: .15s; }

/* =========================================================
   PERFORMANCE SIGNAL
========================================================= */

.signal-panel {
  position: relative;
  display: grid;
  grid-template-columns: 130px 1fr auto;
  align-items: center;
  gap: 26px;
  overflow: hidden;
  margin-top: 15px;
  padding: 26px;
  border: 1px solid var(--border);
  border-radius: 28px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

/* رنگ‌های سیگنال */
.signal-very-high {
  background: linear-gradient(135deg,
    color-mix(in srgb, var(--primary-soft) 80%, var(--surface)) 0%,
    var(--surface) 70%);
  border-color: rgba(101,103,241,.24);
}
.signal-very-high .signal-radar::before { background: rgba(101,103,241,.5); }
.signal-very-high .signal-title { color: var(--primary); }
.signal-very-high .signal-bar.active { background: var(--primary); box-shadow: 0 0 12px var(--primary); }

.signal-rising {
  background: linear-gradient(135deg,
    rgba(101, 103, 241, .06) 0%, var(--surface) 70%);
  border-color: rgba(101,103,241,.2);
}
.signal-rising .signal-radar::before { background: rgba(101,103,241,.4); }
.signal-rising .signal-title { color: var(--primary); }
.signal-rising .signal-bar.active { background: var(--primary); box-shadow: 0 0 12px var(--primary); }

.signal-strong {
  background: linear-gradient(135deg, var(--success-soft) 0%, var(--surface) 70%);
  border-color: rgba(24,168,139,.22);
}
.signal-strong .signal-radar::before { background: rgba(24,168,139,.45); }
.signal-strong .signal-title { color: var(--success); }
.signal-strong .signal-bar.active { background: var(--success); box-shadow: 0 0 12px var(--success); }

.signal-stable {
  background: linear-gradient(135deg, var(--warning-soft) 0%, var(--surface) 70%);
  border-color: rgba(227,166,47,.22);
}
.signal-stable .signal-radar::before { background: rgba(227,166,47,.45); }
.signal-stable .signal-title { color: var(--warning); }
.signal-stable .signal-bar.active { background: var(--warning); box-shadow: 0 0 12px var(--warning); }

.signal-challenging {
  background: linear-gradient(135deg, var(--orange-soft) 0%, var(--surface) 70%);
  border-color: rgba(240,134,47,.22);
}
.signal-challenging .signal-radar::before { background: rgba(240,134,47,.45); }
.signal-challenging .signal-title { color: var(--orange); }
.signal-challenging .signal-bar.active { background: var(--orange); box-shadow: 0 0 12px var(--orange); }

.signal-critical {
  background: linear-gradient(135deg, var(--danger-soft) 0%, var(--surface) 70%);
  border-color: rgba(227,93,104,.22);
}
.signal-critical .signal-radar::before { background: rgba(227,93,104,.45); }
.signal-critical .signal-title { color: var(--danger); }
.signal-critical .signal-bar.active { background: var(--danger); box-shadow: 0 0 12px var(--danger); }

/* Radar */
.signal-radar {
  position: relative;
  width: 120px;
  height: 120px;
  display: grid;
  place-items: center;
  border-radius: 50%;
}

.signal-radar::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  animation: radarCore 2s ease-in-out infinite;
}

.radar-ring {
  position: absolute;
  border: 1px solid currentColor;
  border-radius: 50%;
  opacity: .22;
}

.r1 { inset: 0; animation: radarRing 3s ease-out infinite; }
.r2 { inset: 20px; animation: radarRing 3s ease-out .5s infinite; }
.r3 { inset: 40px; animation: radarRing 3s ease-out 1s infinite; }

.radar-sweep {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    transparent 0deg,
    currentColor 30deg,
    transparent 60deg
  );
  opacity: .28;
  animation: radarSweep 3s linear infinite;
}

.radar-dot {
  position: relative;
  z-index: 2;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 20px currentColor;
}

.signal-content { position: relative; z-index: 1; }

.signal-label {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
  font-weight: 850;
  letter-spacing: .12em;
}

.signal-title {
  margin: 6px 0 6px;
  font-size: clamp(24px, 3vw, 34px);
  font-weight: 1000;
  letter-spacing: -.045em;
}

.signal-desc {
  margin: 0;
  max-width: 520px;
  color: var(--text-soft);
  font-size: 11px;
  line-height: 1.9;
}

.signal-bars {
  display: flex;
  gap: 5px;
  margin-top: 14px;
}

.signal-bar {
  width: 26px;
  height: 5px;
  border-radius: 99px;
  background: var(--border);
  transition: .3s ease;
}

.signal-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-inline-start: 24px;
  border-inline-start: 1px solid var(--border);
}

.signal-percent strong,
.signal-rank strong {
  display: block;
  font-size: 24px;
  font-weight: 1000;
  line-height: 1;
  letter-spacing: -.04em;
}

.signal-percent span,
.signal-rank span {
  display: block;
  margin-top: 4px;
  color: var(--text-faint);
  font-size: 9px;
}

.signal-percent strong { color: var(--primary); }

/* =========================================================
   SUMMARY METRICS
========================================================= */

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-top: 15px;
}

.metric-card {
  position: relative;
  min-width: 0;
  min-height: 128px;
  display: flex;
  align-items: center;
  gap: 14px;
  overflow: hidden;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s ease, border-color .3s ease;
}

.metric-card::after {
  content: "";
  position: absolute;
  width: 110px;
  height: 110px;
  left: -60px;
  bottom: -65px;
  border-radius: 50%;
  background: var(--primary-soft);
  filter: blur(3px);
  transition: transform .5s ease;
}

.metric-card:hover {
  transform: translateY(-6px);
  border-color: var(--border-strong);
  box-shadow: var(--shadow);
}

.metric-card:hover::after { transform: scale(1.3); }

.metric-icon {
  width: 54px;
  height: 54px;
  flex: 0 0 54px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(101,103,241,.08);
  border-radius: 18px;
  color: var(--primary);
  background: var(--primary-soft);
  box-shadow: 0 8px 20px rgba(101,103,241,.08);
}

.metric-icon.correct { color: var(--success); background: var(--success-soft); }
.metric-icon.wrong { color: var(--danger); background: var(--danger-soft); }
.metric-icon.unanswered { color: var(--warning); background: var(--warning-soft); }

.metric-icon svg { width: 25px; height: 25px; }

.metric-content { min-width: 0; }

.metric-content span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
  font-weight: 700;
}

.metric-content strong {
  display: block;
  margin-top: 4px;
  font-size: 27px;
  line-height: 1;
  font-weight: 950;
  letter-spacing: -.04em;
}

.metric-content small {
  display: block;
  margin-top: 6px;
  color: var(--text-faint);
  font-size: 9px;
}

/* =========================================================
   PANELS
========================================================= */

.panel {
  position: relative;
  overflow: hidden;
  margin-top: 15px;
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: 26px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: border-color .3s ease, box-shadow .3s ease, transform .3s ease;
}

.panel::before {
  content: "";
  position: absolute;
  top: 0;
  right: 8%;
  width: 130px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary), transparent);
  opacity: .5;
}

.panel:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow);
}

.panel-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 20px;
}

.panel-heading > div:first-child > span,
.section-intro > div:first-child > span {
  display: block;
  color: var(--primary);
  font-size: 9px;
  font-weight: 850;
  letter-spacing: .05em;
}

.panel-heading h2,
.section-intro h2 {
  margin: 5px 0 0;
  font-size: clamp(18px, 2.5vw, 23px);
  line-height: 1.35;
  letter-spacing: -.035em;
}

.section-intro {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin: 6px 2px 18px;
}

.section-intro p {
  max-width: 680px;
  margin: 7px 0 0;
  color: var(--text-soft);
  font-size: 11px;
  line-height: 1.9;
}

/* =========================================================
   PEAK PANEL — قله عملکرد
========================================================= */

.peak-icon {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 15px;
  color: var(--primary);
  background: var(--primary-soft);
}

.peak-icon svg { width: 22px; height: 22px; }

.peak-chart {
  padding: 10px 4px 4px;
}

.peak-top-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}

.peak-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 11px;
  border-radius: 10px;
  color: var(--warning);
  background: var(--warning-soft);
  font-size: 10px;
  font-weight: 900;
}

.peak-badge-label {
  color: var(--text-faint);
  font-size: 10px;
  font-weight: 850;
}

.peak-track-wrap {
  position: relative;
  height: 92px;
  padding: 0 22px;
}

.peak-track {
  position: absolute;
  top: 50%;
  right: 22px;
  left: 22px;
  height: 10px;
  transform: translateY(-50%);
  border-radius: 99px;
  background: linear-gradient(90deg,
    rgba(227,93,104,.18) 0%,
    rgba(240,134,47,.18) 25%,
    rgba(227,166,47,.18) 50%,
    rgba(24,168,139,.18) 75%,
    rgba(101,103,241,.18) 100%);
  box-shadow: inset 0 1px 2px rgba(0,0,0,.05);
}

.peak-fill {
  position: absolute;
  top: 50%;
  right: 22px;
  height: 10px;
  transform: translateY(-50%);
  border-radius: 99px;
  background: linear-gradient(90deg,
    #e35d68 0%,
    #f0862f 25%,
    #e3a62f 50%,
    #18a88b 75%,
    #6567f1 100%);
  background-size: 100% 100%;
  box-shadow: 0 0 22px rgba(101,103,241,.3);
  max-width: calc(100% - 44px);
  animation: peakFill 1.4s cubic-bezier(.2,.8,.2,1) both;
}

.peak-marker {
  position: absolute;
  top: 50%;
  transform: translate(50%, -50%);
  z-index: 3;
  animation: peakMarker 1.6s cubic-bezier(.2,.8,.2,1) both;
}

.peak-marker-pulse {
  position: absolute;
  top: 50%;
  right: 50%;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary);
  opacity: .2;
  transform: translate(50%, -50%);
  animation: peakPulse 2s ease-out infinite;
}

.peak-marker-dot {
  position: relative;
  display: grid;
  place-items: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(145deg, var(--primary-dark), var(--primary));
  color: #fff;
  border: 4px solid var(--surface-solid);
  box-shadow: 0 10px 28px rgba(101,103,241,.4), 0 0 0 4px rgba(101,103,241,.15);
}

.peak-marker-dot span {
  font-size: 13px;
  font-weight: 1000;
  letter-spacing: -.03em;
}

.peak-marker-arrow {
  position: absolute;
  top: calc(50% + 34px);
  right: 50%;
  width: 0;
  height: 0;
  border-inline: 7px solid transparent;
  border-top: 8px solid var(--primary);
  transform: translateX(50%);
}

.peak-tick {
  position: absolute;
  top: 50%;
  height: 16px;
  border-inline-start: 1px dashed var(--border-strong);
  transform: translate(50%, -50%);
  opacity: .6;
}

.peak-tick span {
  position: absolute;
  top: -26px;
  right: 50%;
  transform: translateX(50%);
  color: var(--text-faint);
  font-size: 9px;
  font-weight: 850;
  white-space: nowrap;
}

.peak-bottom {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.peak-stat {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: var(--surface-soft);
  transition: border-color .25s ease, transform .25s ease;
}

.peak-stat:hover {
  border-color: var(--border-strong);
  transform: translateY(-2px);
}

.peak-stat > span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
  font-weight: 750;
}

.peak-stat > strong {
  display: block;
  margin-top: 5px;
  overflow: hidden;
  font-size: 13px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.peak-stat > small {
  display: block;
  margin-top: 4px;
  color: var(--primary);
  font-size: 10px;
  font-weight: 850;
}

.peak-stat-bar {
  height: 4px;
  margin-top: 8px;
  border-radius: 99px;
  overflow: hidden;
  background: rgba(100,116,139,.1);
}

.peak-stat-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--success), #53d4b8);
  box-shadow: 0 0 10px rgba(24,168,139,.3);
  transform-origin: right;
  animation: barGrow 1s cubic-bezier(.2,.8,.2,1) both;
}

/* =========================================================
   RANKING
========================================================= */

.ranking-crown {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 15px;
  color: var(--warning);
  background: var(--warning-soft);
  box-shadow: 0 0 0 7px rgba(227,166,47,.04);
  animation: crownFloat 3s ease-in-out infinite;
}

.ranking-crown svg { width: 22px; height: 22px; }

.ranking-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 13px;
}

.rank-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 15px;
  overflow: hidden;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 21px;
  background: linear-gradient(135deg, var(--surface-soft), var(--surface));
  transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s ease;
}

.rank-card::after {
  content: "";
  position: absolute;
  width: 130px;
  height: 130px;
  left: -75px;
  bottom: -75px;
  border-radius: 50%;
  background: var(--primary-soft);
  filter: blur(3px);
}

.rank-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-sm);
}

.rank-card-icon {
  position: relative;
  z-index: 1;
  width: 50px;
  height: 50px;
  flex: 0 0 50px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  color: var(--primary);
  background: var(--primary-soft);
  transition: transform .35s cubic-bezier(.2,.8,.2,1);
}

.rank-card:hover .rank-card-icon {
  transform: scale(1.08) rotate(-5deg);
}

.rank-card.province .rank-card-icon {
  color: var(--success);
  background: var(--success-soft);
}

.rank-card-icon svg { width: 22px; height: 22px; }

.rank-card-copy {
  position: relative;
  z-index: 1;
  min-width: 0;
}

.rank-card-copy span {
  display: block;
  color: var(--text-soft);
  font-size: 9px;
}

.rank-card-copy strong {
  display: block;
  margin-top: 3px;
  font-size: 27px;
  line-height: 1;
  font-weight: 950;
}

.rank-card-copy small {
  display: block;
  margin-top: 6px;
  color: var(--text-faint);
  font-size: 9px;
}

/* =========================================================
   LEAGUE — با افکت کامل
========================================================= */

.league-panel {
  --league-color: #8b5cf6;
  --league-soft: rgba(139,92,246,.22);
  --league-glow: rgba(139,92,246,.55);

  position: relative;
  overflow: hidden;
  margin-top: 15px;
  padding: 32px;
  border: 1px solid rgba(124,92,255,.2);
  border-radius: 30px;
  background:
    radial-gradient(circle at 78% 18%, var(--league-soft), transparent 30%),
    radial-gradient(circle at 14% 90%, rgba(44,211,188,.08), transparent 28%),
    var(--surface);
  box-shadow: 0 24px 80px rgba(28,25,55,.12), inset 0 1px 0 rgba(255,255,255,.09);
}

.is-dark .league-panel {
  box-shadow: 0 28px 90px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.06);
}

.league-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--league-color), #2bd3b0, var(--league-color), transparent);
  background-size: 200% 100%;
  animation: leagueBorderGlow 3s linear infinite;
  pointer-events: none;
}

/* رنگ‌های هر لیگ */
.league-bronze { --league-color: #c48354; --league-soft: rgba(196,131,84,.22); --league-glow: rgba(196,131,84,.6); }
.league-silver { --league-color: #c7d2e0; --league-soft: rgba(199,210,224,.25); --league-glow: rgba(199,210,224,.65); }
.league-gold { --league-color: #ffcb47; --league-soft: rgba(255,203,71,.25); --league-glow: rgba(255,203,71,.7); }
.league-platinum { --league-color: #7de8e0; --league-soft: rgba(125,232,224,.22); --league-glow: rgba(125,232,224,.6); }
.league-diamond { --league-color: #7dc4ff; --league-soft: rgba(125,196,255,.25); --league-glow: rgba(125,196,255,.7); }
.league-elite { --league-color: #c79bff; --league-soft: rgba(199,155,255,.28); --league-glow: rgba(199,155,255,.75); }

.league-bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(124,92,255,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124,92,255,.04) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(ellipse at center, black 20%, transparent 80%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 20%, transparent 80%);
  pointer-events: none;
}

.league-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--league-color);
  box-shadow: 0 0 10px var(--league-color);
  opacity: .6;
}

.particle-1 { top: 15%; left: 12%; animation: particleFloat 5s ease-in-out infinite; }
.particle-2 { top: 25%; left: 28%; animation: particleFloat 7s ease-in-out .5s infinite; }
.particle-3 { top: 40%; left: 8%; animation: particleFloat 6s ease-in-out 1s infinite; }
.particle-4 { top: 55%; left: 42%; animation: particleFloat 8s ease-in-out 1.5s infinite; }
.particle-5 { top: 70%; left: 18%; animation: particleFloat 5.5s ease-in-out 2s infinite; }
.particle-6 { top: 80%; left: 55%; animation: particleFloat 7.5s ease-in-out .8s infinite; }
.particle-7 { top: 12%; right: 20%; animation: particleFloat 6.5s ease-in-out 1.2s infinite; }
.particle-8 { top: 35%; right: 8%; animation: particleFloat 8.5s ease-in-out .3s infinite; }
.particle-9 { top: 50%; right: 30%; animation: particleFloat 5.2s ease-in-out 1.8s infinite; }
.particle-10 { top: 68%; right: 15%; animation: particleFloat 7.2s ease-in-out .6s infinite; }
.particle-11 { top: 85%; right: 42%; animation: particleFloat 6.8s ease-in-out 2.2s infinite; }
.particle-12 { top: 22%; left: 50%; animation: particleFloat 5.8s ease-in-out 1.4s infinite; }

.league-head,
.league-main,
.league-track {
  position: relative;
  z-index: 2;
}

.league-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.league-kicker {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: var(--league-color);
  font-size: 9px;
  font-weight: 950;
  letter-spacing: .1em;
}

.league-kicker::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 5px var(--league-soft), 0 0 16px currentColor;
  animation: statusPulse 2s infinite;
}

.league-head h2 {
  margin: 6px 0 5px;
  font-size: clamp(20px, 2.2vw, 30px);
  font-weight: 950;
  letter-spacing: -.045em;
}

.league-head p {
  max-width: 650px;
  margin: 0;
  color: var(--text-faint);
  font-size: 11px;
  line-height: 1.9;
}

.league-season {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 13px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--text-soft);
  background: rgba(255,255,255,.05);
  font-size: 9px;
  font-weight: 850;
  white-space: nowrap;
}

.season-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2bd3b0;
  box-shadow: 0 0 0 5px rgba(43,211,176,.1), 0 0 18px rgba(43,211,176,.6);
  animation: seasonPulse 1.8s infinite;
}

.league-main {
  display: grid;
  grid-template-columns: 240px minmax(0,1fr);
  align-items: center;
  gap: 36px;
  margin-top: 30px;
}

/* ============ EMBLEM ============ */
.league-emblem {
  position: relative;
  width: 200px;
  height: 200px;
  margin-inline: auto;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: var(--league-color);
  animation: emblemFloat 5s ease-in-out infinite;
}

.emblem-aura {
  position: absolute;
  inset: -20px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--league-soft) 0%, transparent 65%);
  filter: blur(14px);
  animation: auraPulse 3s ease-in-out infinite;
}

.emblem-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid var(--league-color);
}

.ring-outer {
  inset: 0;
  border-style: dashed;
  opacity: .35;
  animation: emblemSpin 18s linear infinite;
}

.ring-mid {
  inset: 16px;
  opacity: .55;
  animation: emblemSpinReverse 12s linear infinite;
  box-shadow: 0 0 20px var(--league-soft), inset 0 0 20px var(--league-soft);
}

.ring-inner {
  inset: 32px;
  border-style: dotted;
  opacity: .4;
  animation: emblemSpin 9s linear infinite;
}

.emblem-core {
  position: relative;
  z-index: 3;
  width: 110px;
  height: 110px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background:
    radial-gradient(circle at 30% 30%, rgba(255,255,255,.25), transparent 50%),
    linear-gradient(145deg, var(--league-soft), rgba(0,0,0,.05));
  border: 2px solid var(--league-color);
  box-shadow:
    0 0 40px var(--league-glow),
    0 0 80px var(--league-soft),
    inset 0 0 30px var(--league-soft),
    inset 0 2px 4px rgba(255,255,255,.15);
  animation: coreGlow 3s ease-in-out infinite;
}

.emblem-core svg {
  width: 62px;
  height: 62px;
  stroke-width: 1.7;
  filter: drop-shadow(0 0 10px var(--league-color)) drop-shadow(0 0 22px var(--league-glow));
  animation: emblemIcon 2.5s ease-in-out infinite;
}

.emblem-shine {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(
    135deg,
    transparent 35%,
    rgba(255,255,255,.35) 45%,
    transparent 55%
  );
  pointer-events: none;
  overflow: hidden;
  mix-blend-mode: overlay;
}

/* ============ COPY ============ */
.league-copy { min-width: 0; }

.league-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.league-label {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
  font-weight: 800;
}

.league-title-row h3 {
  margin: 4px 0 0;
  font-size: clamp(26px, 3vw, 40px);
  font-weight: 1000;
  letter-spacing: -.055em;
  background: linear-gradient(110deg, var(--text) 0%, var(--league-color) 50%, var(--text) 100%);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: titleGradient 5s ease-in-out infinite;
}

.league-rank-chip {
  min-width: 82px;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 17px;
  text-align: center;
  background: rgba(255,255,255,.05);
  box-shadow: var(--shadow-sm);
}

.league-rank-chip span,
.league-rank-chip strong { display: block; }

.league-rank-chip span {
  color: var(--text-faint);
  font-size: 8px;
}

.league-rank-chip strong {
  margin-top: 2px;
  color: var(--league-color);
  font-size: 23px;
  font-weight: 1000;
}

.league-progress-wrap { margin-top: 26px; }

.league-progress-labels {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 10px;
  color: var(--text-faint);
  font-size: 8px;
}

.league-progress-labels strong {
  color: var(--text);
  font-size: 13px;
}

.league-progress-labels span:last-child { text-align: left; }

.league-progress {
  position: relative;
  height: 10px;
  margin-top: 10px;
  overflow: visible;
  border-radius: 999px;
  background: rgba(127,127,160,.12);
  box-shadow: inset 0 1px 3px rgba(0,0,0,.1);
}

.league-progress-fill {
  height: 100%;
  border-radius: inherit;
  transform-origin: right center;
  background: linear-gradient(90deg, var(--league-color), #2bd3b0, var(--league-color));
  background-size: 180% 100%;
  box-shadow: 0 0 22px var(--league-glow);
  animation: leagueBar 1.5s cubic-bezier(.16,1,.3,1) both, gradientMove 3s linear infinite;
}

.league-progress i {
  position: absolute;
  top: 50%;
  width: 14px;
  height: 14px;
  transform: translateY(-50%);
  border: 3px solid var(--surface);
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 0 2px var(--league-color), 0 0 22px var(--league-glow);
  animation: progressKnob 1.5s cubic-bezier(.16,1,.3,1) both;
}

/* Distance to next league */
.league-distance {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 18px;
  padding: 12px 14px;
  border: 1px dashed var(--league-color);
  border-radius: 15px;
  background: var(--league-soft);
  opacity: .95;
}

.distance-icon {
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  display: grid;
  place-items: center;
  border-radius: 11px;
  color: var(--league-color);
  background: rgba(255,255,255,.15);
  animation: distanceBounce 2s ease-in-out infinite;
}

.distance-icon.crown {
  color: var(--warning);
  background: var(--warning-soft);
}

.distance-icon svg { width: 18px; height: 18px; }

.distance-copy {
  flex: 1;
  min-width: 0;
}

.distance-copy span {
  display: block;
  color: var(--text-soft);
  font-size: 9px;
  font-weight: 750;
}

.distance-copy strong {
  display: block;
  margin-top: 3px;
  color: var(--league-color);
  font-size: 13px;
  font-weight: 950;
}

.distance-target {
  padding: 5px 11px;
  border-radius: 9px;
  color: var(--league-color);
  background: rgba(255,255,255,.15);
  font-size: 10px;
  font-weight: 900;
  white-space: nowrap;
}

.league-foot {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 9px;
  margin-top: 20px;
}

.league-stat {
  min-width: 0;
  padding: 12px 13px;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: rgba(255,255,255,.04);
  transition: border-color .25s ease, background .25s ease;
}

.league-stat:hover {
  border-color: var(--border-strong);
  background: var(--league-soft);
}

.league-stat span,
.league-stat strong { display: block; }

.league-stat span {
  color: var(--text-faint);
  font-size: 8px;
}

.league-stat strong {
  margin-top: 4px;
  overflow: hidden;
  color: var(--text);
  font-size: 11px;
  font-weight: 950;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.league-stat.highlight strong { color: var(--league-color); }

/* ============ TIER TRACK ============ */
.league-track {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin-top: 30px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
}

.tier {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 0;
  padding: 12px 8px;
  border: 1px solid transparent;
  border-radius: 15px;
  color: var(--text-faint);
  background: rgba(127,127,160,.05);
  font-size: 9px;
  font-weight: 850;
  transition: all .4s cubic-bezier(.2,.8,.2,1);
}

.tier:hover {
  transform: translateY(-4px);
  background: var(--league-soft);
  color: var(--text-soft);
}

.tier-badge {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: rgba(127,127,160,.1);
  color: var(--text-faint);
  transition: all .4s cubic-bezier(.2,.8,.2,1);
}

.tier-badge svg {
  width: 26px;
  height: 26px;
}

.tier-name { white-space: nowrap; }

.tier.passed {
  color: var(--text-soft);
  background: rgba(127,127,160,.08);
}

.tier.passed .tier-badge {
  color: var(--text-faint);
  background: rgba(127,127,160,.15);
}

.tier.active {
  color: var(--league-color);
  border-color: var(--league-color);
  background: var(--league-soft);
  box-shadow: 0 12px 32px var(--league-glow);
  transform: translateY(-5px);
}

.tier.active .tier-badge {
  color: var(--league-color);
  background: rgba(255,255,255,.2);
  box-shadow: 0 0 22px var(--league-glow), inset 0 0 12px var(--league-soft);
  animation: tierBadgePulse 2s ease-in-out infinite;
}

.tier.active::after {
  content: '';
  position: absolute;
  left: 20%;
  right: 20%;
  bottom: -22px;
  height: 2px;
  border-radius: 999px;
  background: var(--league-color);
  box-shadow: 0 0 14px var(--league-color);
}

/* =========================================================
   RAW SCORE
========================================================= */

.raw-comparison {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.raw-item {
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: 19px;
  background: var(--surface-soft);
}

.raw-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.raw-label span { color: var(--text-soft); font-size: 10px; }

.raw-label strong {
  color: var(--primary);
  font-size: 22px;
  font-weight: 950;
}

.progress-track,
.average-track,
.review-progress-track {
  overflow: hidden;
  border-radius: 99px;
  background: rgba(100,116,139,.1);
}

.raw-item .progress-track {
  height: 9px;
  margin-top: 14px;
}

.progress-fill {
  height: 100%;
  min-width: 0;
  border-radius: inherit;
  transform-origin: right center;
  animation: barGrow .9s cubic-bezier(.2,.8,.2,1) both;
}

.progress-fill.negative {
  background: linear-gradient(90deg, var(--primary-dark), var(--primary-light));
  box-shadow: 0 0 18px rgba(101,103,241,.3);
}

.progress-fill.raw {
  background: linear-gradient(90deg, #13a989, #53d4b8);
  box-shadow: 0 0 18px rgba(24,168,139,.25);
}

.raw-item small {
  display: block;
  margin-top: 8px;
  color: var(--text-faint);
  font-size: 9px;
}

/* Previous */
.previous-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 25px;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 21px;
  background: var(--surface-soft);
}

.previous-score span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.previous-score strong {
  display: block;
  margin-top: 6px;
  font-size: 30px;
  font-weight: 950;
}

.previous-score.current strong { color: var(--primary); }

.change-arrow {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: var(--primary);
  background: var(--primary-soft);
  animation: arrowPulse 2.5s ease-in-out infinite;
}

.change-arrow svg { width: 19px; height: 19px; }

.change-badge,
.trend-chip {
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 900;
}

.change-badge.positive,
.trend-chip.positive { color: var(--success); background: var(--success-soft); }

.change-badge.negative,
.trend-chip.negative { color: var(--danger); background: var(--danger-soft); }

.change-badge.neutral,
.trend-chip.neutral { color: var(--text-soft); background: var(--surface-soft); }

.previous-details {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  margin-top: 16px;
  padding: 5px 0;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface);
}

.previous-details > div {
  padding: 12px 15px;
  border-left: 1px solid var(--border);
}

.previous-details > div:last-child { border-left: 0; }

.previous-details span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.previous-details strong {
  display: block;
  margin-top: 4px;
  font-size: 14px;
}

.text-positive { color: var(--success); }
.text-negative { color: var(--danger); }

/* =========================================================
   BOOKLETS
========================================================= */

.booklet-total {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 13px;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

.booklet-total strong {
  color: var(--primary);
  font-size: 20px;
  font-weight: 950;
}

.booklet-total span {
  color: var(--text-faint);
  font-size: 9px;
}

.booklet-cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(0,1fr));
  gap: 16px;
}

.booklet-card {
  position: relative;
  overflow: hidden;
  padding: 22px;
  border: 1px solid var(--border);
  border-radius: 26px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease, border-color .35s ease;
}

.booklet-card::before {
  content: "";
  position: absolute;
  top: -110px;
  left: -110px;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: var(--primary-soft);
  filter: blur(12px);
  opacity: .55;
  transition: transform .5s ease;
}

.booklet-card:hover {
  transform: translateY(-7px);
  border-color: var(--border-strong);
  box-shadow: var(--shadow);
}

.booklet-card:hover::before { transform: scale(1.2); }

.booklet-card-top,
.booklet-score-row,
.booklet-ranks,
.booklet-range,
.average-line {
  position: relative;
  z-index: 1;
}

.booklet-card-top {
  display: flex;
  align-items: center;
  gap: 12px;
}

.booklet-number {
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  color: #fff;
  background: linear-gradient(145deg, var(--primary-dark), var(--primary-light));
  box-shadow: 0 9px 22px rgba(101,103,241,.28);
  font-size: 13px;
  font-weight: 950;
}

.booklet-title-wrap {
  min-width: 0;
  flex: 1;
}

.booklet-title-wrap > span {
  display: block;
  color: var(--primary);
  font-size: 9px;
  font-weight: 800;
}

.booklet-title-wrap h3 {
  overflow: hidden;
  margin: 4px 0 0;
  font-size: 14px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.decile-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface-soft);
}

.decile-badge span {
  color: var(--text-faint);
  font-size: 8px;
}

.decile-badge strong {
  color: var(--primary);
  font-size: 13px;
}

.booklet-score-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 15px;
  margin-top: 22px;
}

.booklet-score strong {
  display: block;
  color: var(--primary);
  font-size: 30px;
  line-height: 1;
  font-weight: 950;
  letter-spacing: -.04em;
}

.booklet-score span {
  display: block;
  margin-top: 6px;
  color: var(--text-faint);
  font-size: 9px;
}

.booklet-raw { text-align: left; }

.booklet-raw span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.booklet-raw strong {
  display: block;
  margin-top: 4px;
  font-size: 16px;
}

.booklet-bar {
  position: relative;
  z-index: 1;
  height: 7px;
  margin-top: 14px;
  overflow: hidden;
  border-radius: 99px;
  background: rgba(100,116,139,.1);
}

.booklet-bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--primary-dark), var(--primary-light));
  box-shadow: 0 0 16px rgba(101,103,241,.28);
  transform-origin: right;
  animation: barGrow 1s cubic-bezier(.2,.8,.2,1) both;
}

.answer-breakdown {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 16px;
}

.answer-stat {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: 13px;
  background: var(--surface-soft);
  font-size: 9px;
}

.answer-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: 50%;
}

.answer-stat.correct .answer-dot { background: var(--success); box-shadow: 0 0 10px rgba(24,168,139,.5); }
.answer-stat.wrong .answer-dot { background: var(--danger); box-shadow: 0 0 10px rgba(227,93,104,.5); }
.answer-stat.unanswered .answer-dot { background: var(--warning); box-shadow: 0 0 10px rgba(227,166,47,.5); }

.answer-stat span { color: var(--text-soft); }

.answer-stat strong {
  margin-right: auto;
  font-weight: 900;
}

.booklet-ranks {
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 10px;
  margin-top: 13px;
}

.booklet-ranks > div {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: var(--surface-soft);
}

.booklet-ranks span,
.booklet-ranks small {
  display: block;
  color: var(--text-faint);
  font-size: 8px;
}

.booklet-ranks strong {
  display: block;
  margin: 3px 0;
  font-size: 16px;
}

.booklet-average {
  position: relative;
  z-index: 1;
  margin-top: 13px;
  padding: 13px;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: var(--surface-soft);
}

.average-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.average-line span {
  color: var(--text-faint);
  font-size: 9px;
}

.average-line strong { font-size: 11px; }

.average-track {
  position: relative;
  height: 8px;
  margin: 9px 0;
  overflow: visible;
}

.average-user-marker,
.average-country-marker {
  position: absolute;
  top: 50%;
  width: 12px;
  height: 12px;
  border: 2px solid var(--surface-solid);
  border-radius: 50%;
  transform: translate(50%, -50%);
  box-shadow: 0 3px 10px rgba(0,0,0,.18);
}

.average-user-marker {
  z-index: 2;
  background: var(--primary);
}

.average-country-marker {
  z-index: 1;
  background: var(--success);
}

.performance-message {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 11px;
  margin-top: 13px;
  padding: 13px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: linear-gradient(135deg, var(--primary-soft), transparent);
}

.performance-icon {
  width: 38px;
  height: 38px;
  flex: 0 0 38px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  color: var(--primary);
  background: var(--primary-soft);
}

.performance-icon svg { width: 18px; height: 18px; }

.performance-message strong { font-size: 10px; }

.performance-message p {
  margin: 4px 0 0;
  color: var(--text-soft);
  font-size: 9px;
  line-height: 1.85;
}

.booklet-range {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 13px;
  padding-top: 12px;
  border-top: 1px dashed var(--border-strong);
  color: var(--text-faint);
  font-size: 8px;
}

/* =========================================================
   ANALYTICS
========================================================= */

.analytics-intro { align-items: center; }

.analytics-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 13px;
  border: 1px solid var(--border);
  border-radius: 13px;
  color: var(--text-soft);
  background: var(--surface);
  font-size: 9px;
  font-weight: 800;
}

.analytics-live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 0 4px var(--success-soft);
  animation: statusPulse 2s infinite;
}

.chart-mini-note { color: var(--text-faint); font-size: 9px; }

.chartjs-panel { overflow: visible; }

.chartjs-wrap {
  position: relative;
  width: 100%;
  padding: 12px 4px 4px;
}

.comparison-chartjs-wrap { height: 360px; }
.progress-chartjs-wrap { height: 350px; }

.chartjs-wrap canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

.empty-chart {
  min-height: 230px;
  display: grid;
  place-items: center;
  padding: 20px;
  border: 1px dashed var(--border-strong);
  border-radius: 19px;
  color: var(--text-faint);
  font-size: 10px;
  background: var(--surface-soft);
}

.progress-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 15px;
}

.progress-summary > div {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: var(--surface-soft);
}

.progress-summary span {
  display: block;
  color: var(--text-faint);
  font-size: 8px;
}

.progress-summary strong {
  display: block;
  margin-top: 4px;
  font-size: 17px;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-top: 15px;
}

.insight-card {
  position: relative;
  overflow: hidden;
  min-height: 145px;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s ease;
}

.insight-card::after {
  content: "";
  position: absolute;
  width: 110px;
  height: 110px;
  left: -65px;
  bottom: -60px;
  border-radius: 50%;
  background: var(--primary-soft);
  transition: transform .5s ease;
}

.insight-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow);
}

.insight-card:hover::after { transform: scale(1.25); }

.insight-icon {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  margin-bottom: 18px;
  border-radius: 14px;
  color: var(--primary);
  background: var(--primary-soft);
}

.insight-icon svg { width: 20px; height: 20px; }

.insight-card > span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.insight-card > strong {
  display: block;
  overflow: hidden;
  margin-top: 4px;
  font-size: 14px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.insight-card > small {
  display: block;
  margin-top: 5px;
  color: var(--primary);
  font-size: 10px;
  font-weight: 850;
}

/* =========================================================
   REVIEW
========================================================= */

.review-hero {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 170px;
  align-items: center;
  gap: 25px;
  overflow: hidden;
  padding: 28px;
  border: 1px solid var(--border);
  border-radius: 28px;
  background:
    radial-gradient(circle at 100% 0%, rgba(101,103,241,.13), transparent 20rem),
    var(--surface);
  box-shadow: var(--shadow);
}

.review-hero::before {
  content: "";
  position: absolute;
  top: 0;
  right: 8%;
  width: 200px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--primary-light), transparent);
}

.review-hero-copy { position: relative; z-index: 1; }

.review-kicker { color: var(--primary); }

.review-kicker::before {
  background: var(--primary);
  box-shadow: 0 0 0 5px var(--primary-soft), 0 0 14px var(--primary);
}

.review-hero h2 {
  margin: 8px 0 7px;
  font-size: clamp(22px, 3vw, 31px);
  line-height: 1.35;
  letter-spacing: -.045em;
}

.review-hero p {
  max-width: 700px;
  margin: 0;
  color: var(--text-soft);
  font-size: 11px;
  line-height: 2;
}

.review-progress-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.review-progress-track {
  width: min(390px, 55vw);
  height: 8px;
}

.review-progress-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--primary-dark), var(--primary-light));
  box-shadow: 0 0 16px rgba(101,103,241,.35);
  animation: barGrow 1s cubic-bezier(.2,.8,.2,1) both;
  transition: width .5s ease;
}

.review-progress-row strong {
  white-space: nowrap;
  color: var(--text-soft);
  font-size: 9px;
}

.review-donut {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  width: 160px;
  height: 160px;
  justify-self: center;
}

.review-donut::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  box-shadow: 0 0 50px rgba(101,103,241,.15);
  animation: orbPulse 2.5s ease-in-out infinite;
}

.review-donut-ring {
  position: relative;
  display: grid;
  place-items: center;
  width: 148px;
  height: 148px;
  border-radius: 50%;
  background: conic-gradient(
    var(--primary) var(--review-progress),
    var(--border) var(--review-progress)
  );
  box-shadow: 0 15px 40px rgba(101,103,241,.18);
}

.review-donut-ring::before {
  content: "";
  position: absolute;
  inset: 12px;
  border-radius: 50%;
  background: var(--surface-solid);
  box-shadow: inset 0 0 30px rgba(101,103,241,.06);
}

.review-donut-center {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.review-donut-center strong {
  font-size: 30px;
  line-height: 1;
  font-weight: 950;
}

.review-donut-center span {
  margin-top: 4px;
  color: var(--text-faint);
  font-size: 9px;
}

.review-dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin: 15px 0;
}

.review-stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  padding: 17px;
  border: 1px solid var(--border);
  border-radius: 19px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: transform .25s ease, box-shadow .25s ease;
}

.review-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}

.review-stat-icon {
  width: 44px;
  height: 44px;
  flex: 0 0 44px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  color: var(--primary);
  background: var(--primary-soft);
}

.review-stat-card.correct .review-stat-icon { color: var(--success); background: var(--success-soft); }
.review-stat-card.wrong .review-stat-icon { color: var(--danger); background: var(--danger-soft); }
.review-stat-card.unanswered .review-stat-icon { color: var(--warning); background: var(--warning-soft); }

.review-stat-icon svg { width: 21px; height: 21px; }

.review-stat-card span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.review-stat-card strong {
  display: block;
  margin-top: 3px;
  font-size: 22px;
  font-weight: 950;
}

.review-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: 19px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

.review-toolbar-copy { padding: 0 8px; }

.review-toolbar-copy span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.review-toolbar-copy strong {
  display: block;
  margin-top: 3px;
  font-size: 11px;
}

.review-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  padding: 4px;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: var(--surface-soft);
}

.review-filters button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 11px;
  border: 0;
  border-radius: 11px;
  color: var(--text-soft);
  background: transparent;
  cursor: pointer;
  font: inherit;
  font-size: 9px;
  font-weight: 800;
  transition: .25s ease;
}

.review-filters button span {
  min-width: 18px;
  padding: 2px 5px;
  border-radius: 6px;
  color: var(--text-faint);
  background: var(--surface);
  font-size: 8px;
}

.review-filters button:hover { color: var(--text); }

.review-filters button.active {
  color: var(--primary);
  background: var(--surface);
  box-shadow: 0 6px 18px rgba(31,41,55,.08);
}

.review-filters button.active span {
  color: var(--primary);
  background: var(--primary-soft);
}

.review-list { display: grid; gap: 16px; }

.question-card {
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 25px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}

.question-card:hover {
  transform: translateY(-3px);
  border-color: var(--border-strong);
  box-shadow: var(--shadow);
}

.question-top {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border-bottom: 1px solid var(--border);
}

.question-number {
  min-width: 58px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 10px;
  border-radius: 14px;
  color: var(--primary);
  background: var(--primary-soft);
}

.question-number span { font-size: 8px; }

.question-number strong {
  margin-top: 2px;
  font-size: 17px;
  line-height: 1;
}

.question-context { min-width: 0; }

.question-context strong {
  display: block;
  overflow: hidden;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.question-context span {
  display: block;
  margin-top: 4px;
  color: var(--text-faint);
  font-size: 9px;
}

.question-status {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 11px;
  border-radius: 11px;
  font-size: 9px;
  font-weight: 900;
}

.question-status.correct { color: var(--success); background: var(--success-soft); }
.question-status.wrong { color: var(--danger); background: var(--danger-soft); }
.question-status.unanswered { color: var(--warning); background: var(--warning-soft); }

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 4px color-mix(in srgb, currentColor 10%, transparent);
}

.question-paper {
  margin: 16px;
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--surface-soft);
}

.question-paper-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.question-paper-heading > div:first-child span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.question-paper-heading > div:first-child strong {
  display: block;
  margin-top: 3px;
  font-size: 11px;
}

.paper-open-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 11px;
  border: 1px solid var(--border);
  border-radius: 11px;
  color: var(--primary);
  background: var(--surface);
  font-size: 9px;
  font-weight: 850;
  text-decoration: none;
  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}

.paper-open-link:hover {
  transform: translateY(-1px);
  border-color: var(--primary);
  box-shadow: 0 8px 20px rgba(101,103,241,.15);
}

.paper-open-link svg { width: 14px; height: 14px; }

.question-pdf-frame {
  position: relative;
  width: 100%;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: #fff;
  box-shadow: 0 12px 35px rgba(15,23,42,.08);
}

.question-pdf-canvas {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 0 auto;
  background: #fff;
}

.question-pdf-state {
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 260px;
  padding: 24px;
  text-align: center;
  color: var(--text-soft);
  background: rgba(248,250,252,.94);
  backdrop-filter: blur(7px);
  font-size: 10px;
}

.exam-result-page.is-dark .question-pdf-state { background: rgba(16,22,32,.94); }

.question-pdf-state.error { color: var(--danger); }
.question-pdf-state.error strong { font-size: 12px; }

.pdf-loader {
  width: 28px;
  height: 28px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin .75s linear infinite;
}

.answer-comparison {
  margin: 16px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--surface-soft);
}

.answer-comparison-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.answer-comparison-heading span {
  display: block;
  color: var(--text-faint);
  font-size: 9px;
}

.answer-comparison-heading strong {
  display: block;
  margin-top: 3px;
  font-size: 12px;
}

.answer-result-pill {
  padding: 7px 11px;
  border-radius: 11px;
  font-size: 9px;
  font-weight: 900;
}

.answer-result-pill.correct { color: var(--success); background: var(--success-soft); }
.answer-result-pill.wrong { color: var(--danger); background: var(--danger-soft); }
.answer-result-pill.unanswered { color: var(--warning); background: var(--warning-soft); }

.answer-comparison .options-grid { margin-top: 13px; }

.options-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 9px;
}

.option-card {
  position: relative;
  min-height: 62px;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: var(--surface);
  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}

.option-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-strong);
  box-shadow: var(--shadow-sm);
}

.option-card.selected {
  border-color: rgba(101,103,241,.3);
  background: var(--primary-soft);
}

.option-card.correct {
  border-color: rgba(24,168,139,.35);
  background: var(--success-soft);
}

.option-card.selected-wrong {
  border-color: rgba(227,93,104,.35);
  background: var(--danger-soft);
}

.option-number {
  width: 30px;
  height: 30px;
  flex: 0 0 30px;
  display: grid;
  place-items: center;
  border-radius: 10px;
  color: var(--text-soft);
  background: var(--surface-soft);
  font-size: 10px;
  font-weight: 900;
}

.option-content { min-width: 0; }

.option-content span {
  display: block;
  color: var(--text);
  font-size: 9px;
  font-weight: 800;
}

.option-content small {
  display: block;
  margin-top: 3px;
  color: var(--primary);
  font-size: 8px;
}

.option-content .correct-label { color: var(--success); }

.option-mark {
  width: 22px;
  height: 22px;
  flex: 0 0 22px;
  display: grid;
  place-items: center;
  margin-right: auto;
}

.option-mark svg {
  width: 17px;
  height: 17px;
  color: var(--success);
}

.option-card.selected-wrong .option-mark svg { color: var(--danger); }

.question-answer-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin: 0 16px 16px;
}

.question-answer-summary > div {
  padding: 13px;
  border: 1px solid var(--border);
  border-radius: 15px;
  background: var(--surface-soft);
}

.question-answer-summary span {
  display: block;
  color: var(--text-faint);
  font-size: 8px;
}

.question-answer-summary strong {
  display: block;
  margin-top: 4px;
  font-size: 12px;
}

.question-answer-summary strong.empty { color: var(--warning); }

.empty-review {
  padding: 55px 20px;
  border: 1px dashed var(--border-strong);
  border-radius: 23px;
  text-align: center;
  background: var(--surface-soft);
}

.empty-review-icon {
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  margin: 0 auto 13px;
  border-radius: 19px;
  color: var(--primary);
  background: var(--primary-soft);
}

.empty-review-icon svg { width: 25px; height: 25px; }

.empty-review h3 { margin: 0; font-size: 15px; }

.empty-review p {
  margin: 6px 0 0;
  color: var(--text-faint);
  font-size: 10px;
}

/* =========================================================
   FOOTER
========================================================= */

.result-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-top: 28px;
  padding: 22px 5px;
}

.result-footer strong { display: block; font-size: 14px; }

.result-footer span {
  display: block;
  margin-top: 4px;
  color: var(--text-faint);
  font-size: 9px;
}

.result-footer button {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--primary);
  background: var(--surface);
  cursor: pointer;
  font: inherit;
  font-size: 10px;
  font-weight: 800;
  box-shadow: var(--shadow-sm);
  transition: transform .2s ease, box-shadow .2s ease;
}

.result-footer button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.result-footer button svg { width: 16px; height: 16px; }

/* =========================================================
   ANIMATIONS
========================================================= */

@keyframes pageReveal {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes itemIn {
  from { opacity: 0; transform: translateY(12px) scale(.985); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes tabIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes avatarIn {
  from { opacity: 0; transform: scale(.72) rotate(-6deg); }
  to { opacity: 1; transform: scale(1) rotate(0); }
}

@keyframes scoreIn {
  from { opacity: 0; transform: scale(.76) rotate(8deg); }
  to { opacity: 1; transform: scale(1) rotate(0); }
}

@keyframes statusPulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(54,214,177,.1), 0 0 14px rgba(54,214,177,.4); }
  50% { box-shadow: 0 0 0 8px rgba(54,214,177,.03), 0 0 26px rgba(54,214,177,.65); }
}

@keyframes crownFloat {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-4px) rotate(2deg); }
}

@keyframes orbPulse {
  0%, 100% { transform: scale(.96); opacity: .75; }
  50% { transform: scale(1.04); opacity: 1; }
}

@keyframes orbit {
  from { transform: rotate(0deg) translateX(31px) rotate(0deg); }
  to { transform: rotate(360deg) translateX(31px) rotate(-360deg); }
}

@keyframes spin { to { transform: rotate(360deg); } }

@keyframes barGrow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

@keyframes auroraShift {
  0% { transform: translate(0,0) scale(1); opacity: .65; }
  50% { transform: translate(3%,-2%) scale(1.1); opacity: .85; }
  100% { transform: translate(-2%,2%) scale(1.05); opacity: .7; }
}

/* Signal */
@keyframes radarSweep { to { transform: rotate(360deg); } }

@keyframes radarRing {
  0% { transform: scale(.4); opacity: .6; }
  100% { transform: scale(1.3); opacity: 0; }
}

@keyframes radarCore {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: .7; }
}

/* Peak */
@keyframes peakFill { from { width: 0; } }

@keyframes peakMarker {
  0% { opacity: 0; transform: translate(50%, -50%) scale(0); }
  70% { transform: translate(50%, -50%) scale(1.15); }
  100% { opacity: 1; transform: translate(50%, -50%) scale(1); }
}

@keyframes peakPulse {
  0% { transform: translate(50%, -50%) scale(.6); opacity: .5; }
  100% { transform: translate(50%, -50%) scale(1.8); opacity: 0; }
}

/* League */
@keyframes leagueBorderGlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

@keyframes particleFloat {
  0%, 100% { transform: translate(0,0); opacity: .3; }
  50% { transform: translate(15px,-20px); opacity: .9; }
}

@keyframes seasonPulse {
  50% { box-shadow: 0 0 0 8px rgba(43,211,176,.03), 0 0 25px rgba(43,211,176,.8); }
}

@keyframes emblemFloat {
  0%,100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-10px) rotate(1.5deg); }
}

@keyframes auraPulse {
  0%,100% { transform: scale(1); opacity: .85; }
  50% { transform: scale(1.15); opacity: 1; }
}

@keyframes emblemSpin { to { transform: rotate(360deg); } }
@keyframes emblemSpinReverse { to { transform: rotate(-360deg); } }

@keyframes coreGlow {
  0%,100% {
    box-shadow:
      0 0 40px var(--league-glow),
      0 0 80px var(--league-soft),
      inset 0 0 30px var(--league-soft),
      inset 0 2px 4px rgba(255,255,255,.15);
  }
  50% {
    box-shadow:
      0 0 60px var(--league-glow),
      0 0 120px var(--league-soft),
      inset 0 0 45px var(--league-soft),
      inset 0 2px 4px rgba(255,255,255,.2);
  }
}

@keyframes emblemIcon {
  0%,100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-3px) scale(1.06); }
}


@keyframes titleGradient {
  0%,100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes leagueBar { from { width: 0 !important; } }

@keyframes gradientMove { to { background-position: 180% 0; } }

@keyframes progressKnob {
  from { opacity: 0; transform: translateY(-50%) scale(.4); }
  to { opacity: 1; transform: translateY(-50%) scale(1); }
}

@keyframes arrowPulse {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.08); box-shadow: 0 0 0 6px rgba(101,103,241,.08); }
}

@keyframes tierBadgePulse {
  0%,100% { box-shadow: 0 0 22px var(--league-glow), inset 0 0 12px var(--league-soft); }
  50% { box-shadow: 0 0 34px var(--league-glow), inset 0 0 18px var(--league-soft); }
}

@keyframes distanceBounce {
  0%,100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* =========================================================
   PREMIUM UX ADDITIONS
========================================================= */
.quick-actions {
  position: relative;
  margin: 16px 0 20px;
  padding: 15px 17px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: color-mix(in srgb, var(--surface) 88%, transparent);
  box-shadow: 0 14px 40px rgba(30, 34, 70, .07);
  backdrop-filter: blur(18px);
  overflow: hidden;
}
.quick-actions::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 5px;
  background: linear-gradient(180deg, #7c5cff, #16c7b7, #ffb454);
}
.quick-actions-copy { display:flex; flex-direction:column; gap:4px; }
.quick-actions-copy span { font-size:11px; color:var(--muted); font-weight:800; }
.quick-actions-copy strong { font-size:13px; color:var(--text); }
.quick-actions-buttons { display:flex; flex-wrap:wrap; gap:8px; }
.quick-action {
  border:1px solid var(--border); background:var(--surface-soft); color:var(--text);
  border-radius:13px; padding:9px 12px; display:flex; align-items:center; gap:7px;
  font:inherit; font-size:11px; font-weight:800; cursor:pointer; transition:.25s ease;
}
.quick-action:hover { transform:translateY(-2px); border-color:rgba(101,103,241,.35); box-shadow:0 10px 24px rgba(70,60,150,.10); }
.quick-action-icon { width:25px; height:25px; display:grid; place-items:center; border-radius:8px; background:linear-gradient(135deg,#7367ff,#4f46c8); color:#fff; font-size:15px; }

.smart-insights { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:16px 0 20px; }
.smart-insight {
  position:relative; display:flex; align-items:center; gap:12px; padding:15px; border:1px solid var(--border);
  border-radius:20px; background:var(--surface); box-shadow:0 12px 35px rgba(30,34,70,.055); overflow:hidden;
  transition:transform .28s ease, box-shadow .28s ease;
}
.smart-insight:hover { transform:translateY(-4px); box-shadow:0 18px 42px rgba(30,34,70,.10); }
.smart-insight::after { content:''; position:absolute; width:90px; height:90px; border-radius:50%; left:-34px; bottom:-48px; background:var(--insight-glow); filter:blur(12px); opacity:.35; }
.smart-insight-icon { width:38px; height:38px; flex:0 0 38px; display:grid; place-items:center; border-radius:13px; color:#fff; font-weight:950; background:var(--insight-color); box-shadow:0 8px 22px var(--insight-shadow); }
.smart-insight div { min-width:0; display:flex; flex-direction:column; gap:2px; }
.smart-insight span:not(.smart-insight-icon) { font-size:10px; color:var(--muted); font-weight:800; }
.smart-insight strong { font-size:21px; line-height:1.1; color:var(--text); }
.smart-insight small { color:var(--muted); font-size:9px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.accent-purple { --insight-color:#6f63ff; --insight-shadow:rgba(111,99,255,.24); --insight-glow:#8d82ff; }
.accent-cyan { --insight-color:#11b8b0; --insight-shadow:rgba(17,184,176,.22); --insight-glow:#42ddd5; }
.accent-orange { --insight-color:#f39a35; --insight-shadow:rgba(243,154,53,.22); --insight-glow:#ffc16e; }
.accent-pink { --insight-color:#df5e9b; --insight-shadow:rgba(223,94,155,.22); --insight-glow:#ff91c0; }

.booklet-toolbar { display:flex; align-items:center; justify-content:space-between; gap:12px; margin:0 0 14px; padding:11px 13px; border:1px solid var(--border); border-radius:17px; background:var(--surface-soft); }
.booklet-toolbar-copy { display:flex; flex-direction:column; gap:2px; }
.booklet-toolbar-copy span { font-size:9px; color:var(--muted); font-weight:800; }
.booklet-toolbar-copy strong { font-size:11px; color:var(--text); }
.booklet-sort-buttons { display:flex; gap:6px; }
.booklet-sort-buttons button { border:1px solid var(--border); background:transparent; color:var(--muted); padding:7px 10px; border-radius:10px; font:inherit; font-size:10px; font-weight:800; cursor:pointer; transition:.2s ease; }
.booklet-sort-buttons button.active { color:#fff; border-color:transparent; background:linear-gradient(135deg,#6f63ff,#5147cf); box-shadow:0 7px 18px rgba(81,71,207,.2); }

.review-search { flex:1; min-width:220px; display:flex; align-items:center; gap:7px; height:40px; padding:0 10px; border:1px solid var(--border); border-radius:12px; background:var(--surface); }
.review-search > span { color:var(--muted); font-size:18px; }
.review-search input { flex:1; min-width:0; border:0; outline:0; background:transparent; color:var(--text); font:inherit; font-size:11px; }
.review-search button { border:0; background:transparent; color:var(--muted); cursor:pointer; font-size:18px; }

.scroll-top-button { position:fixed; z-index:50; right:22px; bottom:22px; width:46px; height:46px; border:1px solid rgba(255,255,255,.25); border-radius:15px; color:#fff; background:linear-gradient(135deg,#6f63ff,#4136bd); box-shadow:0 14px 35px rgba(64,52,180,.30); cursor:pointer; font-size:20px; animation:floatUp .3s ease both; }
@keyframes floatUp { from { opacity:0; transform:translateY(10px) scale(.85); } to { opacity:1; transform:none; } }

@media (max-width:1050px) { .smart-insights { grid-template-columns:repeat(2,1fr); } }
@media (max-width:850px) { .quick-actions { align-items:flex-start; flex-direction:column; } .quick-actions-buttons { width:100%; } .quick-action { flex:1; justify-content:center; } }
@media (max-width:650px) { .smart-insights { grid-template-columns:1fr; } .booklet-toolbar { align-items:flex-start; flex-direction:column; } .booklet-sort-buttons { width:100%; } .booklet-sort-buttons button { flex:1; } .review-search { width:100%; } .scroll-top-button { right:14px; bottom:14px; } }

@media print {
  .bg-layer, .result-tabs, .quick-actions, .scroll-top-button, .result-footer, .back-button, .review-toolbar, .paper-open-link { display:none !important; }
  .exam-result-page { padding:0 !important; background:#fff !important; color:#111 !important; }
  .tab-content { display:block !important; }
  .hero-card, .panel, .league-panel, .smart-insight, .booklet-card, .question-card, .review-hero { break-inside:avoid; box-shadow:none !important; }
  .is-dark { background:#fff !important; }
}

/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1050px) {
  .summary-grid { grid-template-columns: repeat(2, 1fr); }
  .booklet-cards { grid-template-columns: 1fr; }
  .review-dashboard { grid-template-columns: repeat(2, 1fr); }
  .signal-panel { grid-template-columns: 110px 1fr auto; gap: 20px; }
}

@media (max-width: 850px) {
  .exam-result-page { padding: 18px 12px 50px; }

  .hero-card { padding: 24px; border-radius: 27px; }
  .hero-content { flex-direction: column; align-items: flex-start; }
  .hero-score { align-self: center; }
  .hero-bottom { flex-direction: column; gap: 9px; }

  .signal-panel {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 22px;
  }
  .signal-radar { margin-inline: auto; }
  .signal-meta {
    flex-direction: row;
    justify-content: center;
    gap: 30px;
    padding-inline-start: 0;
    padding-top: 16px;
    border-inline-start: 0;
    border-top: 1px solid var(--border);
  }

  .ranking-grid,
  .raw-comparison { grid-template-columns: 1fr; }

  .previous-content { gap: 18px; }
  .previous-details { grid-template-columns: repeat(2, 1fr); }
  .previous-details > div:nth-child(2) { border-left: 0; }

  .insights-grid { grid-template-columns: 1fr; }

  .review-hero { grid-template-columns: 1fr; }
  .review-donut { justify-self: center; }

  .review-toolbar {
    align-items: flex-start;
    flex-direction: column;
  }
  .review-toolbar,
  .review-filters { width: 100%; }

  .league-main {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .league-copy { width: 100%; }
  .league-title-row { text-align: right; }
  .league-foot { text-align: right; }

  .analytics-intro { align-items: flex-start; }
  .comparison-chartjs-wrap,
  .progress-chartjs-wrap { height: 290px; }

  .peak-bottom { grid-template-columns: 1fr; }
}

@media (max-width: 650px) {
  .result-tabs { top: 8px; margin: 13px 0; }
  .result-tab { min-height: 46px; padding-inline: 12px; }
  .result-tab span:not(.tab-icon) { font-size: 9px; }

  .summary-grid,
  .review-dashboard { grid-template-columns: 1fr; }

  .section-intro {
    align-items: flex-start;
    flex-direction: column;
  }

  .previous-details { grid-template-columns: 1fr 1fr; }
  .previous-details > div { border-left: 0; }

  .review-progress-row {
    align-items: flex-start;
    flex-direction: column;
  }
  .review-progress-track { width: 100%; }

  .question-paper { margin: 10px; padding: 10px; }
  .question-paper-heading,
  .answer-comparison-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .question-top { grid-template-columns: auto 1fr; }
  .question-status {
    grid-column: 1 / -1;
    justify-self: start;
  }

  .options-grid { grid-template-columns: repeat(2, 1fr); }
  .question-answer-summary { grid-template-columns: 1fr; }

  .result-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .league-panel { padding: 22px; border-radius: 24px; }
  .league-head { align-items: flex-start; flex-direction: column; }
  .league-season { align-self: flex-start; }

  .league-emblem { width: 170px; height: 170px; }
  .emblem-core { width: 92px; height: 92px; }
  .emblem-core svg { width: 54px; height: 54px; }

  .league-main { gap: 20px; }
  .league-title-row { gap: 10px; }
  .league-title-row h3 { font-size: 28px; }

  .league-foot { grid-template-columns: 1fr; }
  .league-track { grid-template-columns: repeat(3, 1fr); }
  .tier.active::after { display: none; }

  .league-distance { flex-wrap: wrap; }

  .peak-track-wrap { padding: 0 10px; }
  .peak-marker-dot { width: 52px; height: 52px; }
  .peak-marker-dot span { font-size: 11px; }
}

@media (max-width: 430px) {
  .hero-card { padding: 20px; }
  .hero-user { gap: 11px; }

  .avatar-wrap {
    width: 66px;
    height: 66px;
    flex-basis: 66px;
  }

  .hero-user-info h1 {
    max-width: calc(100vw - 125px);
    font-size: 20px;
  }

  .score-ring { width: 142px; height: 142px; }
  .score-center strong { font-size: 29px; }

  .panel { padding: 18px; border-radius: 21px; }
  .booklet-card { padding: 17px; }

  .answer-breakdown,
  .booklet-ranks { grid-template-columns: 1fr; }

  .options-grid { grid-template-columns: 1fr; }

  .review-hero { padding: 20px; }
  .review-filters {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
  .review-filters button { justify-content: center; }
}

@media (prefers-reduced-motion: reduce) {
  .exam-result-page *,
  .exam-result-page *::before,
  .exam-result-page *::after {
    animation-duration: .001ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: .001ms !important;
  }
}

/* =========================================================
   2026 VISUAL REFRESH — Aurora / Midnight / Glass
========================================================= */
:root {
  --primary: #6557ff;
  --primary-strong: #4b3fe5;
  --primary-soft: rgba(101,87,255,.10);
  --accent-cyan: #18c7c0;
  --accent-mint: #54e3b5;
  --accent-gold: #f5b84b;
  --danger: #ef6b86;
  --text: #111526;
  --muted: #737b91;
  --text-faint: #a0a7b8;
  --surface: rgba(255,255,255,.82);
  --surface-solid: #ffffff;
  --surface-soft: #f4f6fb;
  --border: rgba(32,39,67,.09);
  --shadow-sm: 0 10px 30px rgba(24,31,61,.06);
  --shadow: 0 24px 70px rgba(34,39,84,.10);
}

.exam-result-page {
  --aurora-1: rgba(101,87,255,.17);
  --aurora-2: rgba(24,199,192,.13);
  --aurora-3: rgba(245,184,75,.09);
  position: relative;
  isolation: isolate;
  background:
    radial-gradient(circle at 8% 0%, var(--aurora-1), transparent 28rem),
    radial-gradient(circle at 92% 8%, var(--aurora-2), transparent 25rem),
    linear-gradient(180deg,#f8f9fd 0%,#f3f5fa 48%,#f8f9fd 100%);
}

.exam-result-page.is-dark {
  --text: #f4f6ff;
  --muted: #98a0b8;
  --text-faint: #737c96;
  --surface: rgba(17,23,39,.78);
  --surface-solid: #111727;
  --surface-soft: #0e1422;
  --border: rgba(255,255,255,.085);
  --shadow-sm: 0 14px 38px rgba(0,0,0,.22);
  --shadow: 0 30px 90px rgba(0,0,0,.32);
  --aurora-1: rgba(101,87,255,.20);
  --aurora-2: rgba(24,199,192,.11);
  --aurora-3: rgba(245,184,75,.07);
  background:
    radial-gradient(circle at 10% 0%,var(--aurora-1),transparent 30rem),
    radial-gradient(circle at 90% 4%,var(--aurora-2),transparent 26rem),
    linear-gradient(180deg,#080b14 0%,#0b0f1b 50%,#080b14 100%);
}

.bg-grid {
  opacity: .25;
  background-image:
    linear-gradient(rgba(101,87,255,.055) 1px,transparent 1px),
    linear-gradient(90deg,rgba(101,87,255,.055) 1px,transparent 1px);
  background-size: 42px 42px;
}

.bg-glow {
  width: 55vw;
  height: 55vw;
  max-width: 720px;
  max-height: 720px;
  background: radial-gradient(circle,rgba(101,87,255,.12),rgba(24,199,192,.045) 42%,transparent 70%);
  filter: blur(16px);
}

.hero-card {
  border: 1px solid rgba(255,255,255,.15);
  background:
    radial-gradient(circle at 78% 12%,rgba(24,199,192,.24),transparent 19rem),
    radial-gradient(circle at 15% 90%,rgba(245,184,75,.15),transparent 22rem),
    linear-gradient(135deg,#11152b 0%,#211c52 46%,#3c2c83 100%);
  box-shadow: 0 35px 100px rgba(58,43,154,.22), inset 0 1px 0 rgba(255,255,255,.12);
}

.hero-aurora {
  opacity: .9;
  background:
    radial-gradient(circle at 18% 55%,rgba(84,227,181,.23),transparent 18rem),
    radial-gradient(circle at 82% 40%,rgba(111,96,255,.30),transparent 20rem);
  filter: blur(4px);
}

.hero-card::after {
  content:'';
  position:absolute;
  inset:0;
  pointer-events:none;
  border-radius:inherit;
  background: linear-gradient(120deg,transparent 25%,rgba(255,255,255,.055) 48%,transparent 70%);
  transform: translateX(-100%);
  animation: heroSheen 7s ease-in-out infinite;
}
@keyframes heroSheen { 0%,65%{transform:translateX(-100%)} 82%,100%{transform:translateX(100%)} }

.score-ring {
  filter: drop-shadow(0 0 24px rgba(84,227,181,.18));
}
.score-progress { stroke: #54e3b5 !important; }
.score-track { stroke: rgba(255,255,255,.15) !important; }

.result-pulse {
  position: relative;
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 16px;
  align-items: center;
  margin: 18px 0;
  padding: 17px 18px;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: linear-gradient(120deg,rgba(255,255,255,.78),rgba(246,247,253,.72));
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(18px);
}
.exam-result-page.is-dark .result-pulse { background:linear-gradient(120deg,rgba(17,23,39,.82),rgba(13,18,31,.72)); }
.result-pulse::before {
  content:''; position:absolute; width:280px; height:280px; left:-120px; top:-160px;
  border-radius:50%; background:rgba(101,87,255,.10); filter:blur(15px);
}
.pulse-main { display:flex; align-items:center; gap:14px; min-width:0; }
.pulse-orbit { position:relative; width:58px; height:58px; flex:0 0 58px; display:grid; place-items:center; }
.orbit { position:absolute; border:1px solid rgba(101,87,255,.25); border-radius:50%; }
.orbit-one { inset:2px; animation:orbitSpin 9s linear infinite; }
.orbit-two { inset:9px; border-color:rgba(24,199,192,.34); animation:orbitSpin 6s linear reverse infinite; }
.orbit-dot { width:12px; height:12px; border-radius:50%; background:linear-gradient(135deg,#6557ff,#54e3b5); box-shadow:0 0 0 6px rgba(101,87,255,.08),0 0 24px rgba(84,227,181,.45); }
@keyframes orbitSpin { to{transform:rotate(360deg)} }
.pulse-copy { min-width:0; }
.pulse-kicker { display:block; margin-bottom:2px; color:var(--muted); font-size:9px; font-weight:900; letter-spacing:.05em; }
.pulse-copy strong { display:block; color:var(--text); font-size:17px; }
.pulse-copy p { margin:4px 0 0; color:var(--muted); font-size:10px; line-height:1.8; }
.pulse-stats { display:grid; grid-template-columns:repeat(4,1fr); border-radius:17px; overflow:hidden; border:1px solid var(--border); background:rgba(127,136,170,.045); }
.pulse-stats div { padding:10px 9px; text-align:center; border-inline-start:1px solid var(--border); }
.pulse-stats div:first-child { border-inline-start:0; }
.pulse-stats span { display:block; color:var(--muted); font-size:8px; font-weight:800; }
.pulse-stats strong { display:block; margin-top:3px; color:var(--text); font-size:15px; font-weight:950; }

.summary-grid { gap:12px; }
.metric-card {
  position:relative; overflow:hidden; border-radius:22px; border:1px solid var(--border);
  background:linear-gradient(145deg,var(--surface),rgba(255,255,255,.48));
  box-shadow:var(--shadow-sm); backdrop-filter:blur(14px);
  transition:transform .3s ease,box-shadow .3s ease,border-color .3s ease;
}
.exam-result-page.is-dark .metric-card { background:linear-gradient(145deg,rgba(17,23,39,.88),rgba(12,17,29,.7)); }
.metric-card:hover { transform:translateY(-5px); box-shadow:0 22px 55px rgba(35,40,88,.12); border-color:rgba(101,87,255,.22); }
.metric-card::after { content:''; position:absolute; width:90px; height:90px; left:-45px; bottom:-50px; border-radius:50%; background:rgba(101,87,255,.10); filter:blur(8px); }
.metric-icon { box-shadow:0 10px 24px rgba(101,87,255,.14); }

.smart-insights { gap:12px; }
.smart-insight { border-radius:22px; background:linear-gradient(145deg,var(--surface),rgba(255,255,255,.5)); backdrop-filter:blur(16px); }
.exam-result-page.is-dark .smart-insight { background:linear-gradient(145deg,rgba(17,23,39,.88),rgba(12,17,29,.7)); }
.smart-insight strong { font-variant-numeric:tabular-nums; }

.performance-dna {
  position:relative; margin:18px 0; padding:20px; border:1px solid var(--border); border-radius:28px;
  background:linear-gradient(145deg,rgba(255,255,255,.75),rgba(246,247,252,.62)); box-shadow:var(--shadow-sm); overflow:hidden;
}
.exam-result-page.is-dark .performance-dna { background:linear-gradient(145deg,rgba(17,23,39,.82),rgba(11,16,28,.72)); }
.performance-dna::before { content:''; position:absolute; width:300px; height:180px; left:-100px; bottom:-120px; border-radius:50%; background:rgba(101,87,255,.10); filter:blur(30px); }
.dna-heading { position:relative; display:flex; justify-content:space-between; align-items:center; gap:15px; margin-bottom:14px; }
.dna-heading span { color:var(--primary); font-size:9px; font-weight:950; }
.dna-heading h2 { margin:3px 0 0; color:var(--text); font-size:17px; }
.dna-live { display:flex; align-items:center; gap:7px; color:var(--muted); font-size:9px; font-weight:850; }
.dna-live i { width:7px; height:7px; border-radius:50%; background:var(--accent-mint); box-shadow:0 0 0 5px rgba(84,227,181,.10),0 0 16px rgba(84,227,181,.55); animation:livePulse 1.8s ease-in-out infinite; }
@keyframes livePulse { 50%{transform:scale(.7);opacity:.6} }
.dna-grid { position:relative; display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
.dna-card { position:relative; min-height:130px; padding:15px; overflow:hidden; border:1px solid var(--border); border-radius:20px; background:rgba(255,255,255,.55); }
.exam-result-page.is-dark .dna-card { background:rgba(255,255,255,.025); }
.dna-card::before { content:''; position:absolute; width:120px; height:120px; left:-65px; top:-65px; border-radius:50%; background:var(--dna-color); opacity:.09; filter:blur(5px); }
.dna-purple { --dna-color:#6557ff; } .dna-cyan { --dna-color:#18c7c0; } .dna-orange { --dna-color:#f5b84b; }
.dna-icon { width:34px; height:34px; display:grid; place-items:center; margin-bottom:10px; border-radius:11px; color:var(--dna-color); background:color-mix(in srgb,var(--dna-color) 10%,transparent); font-weight:950; }
.dna-copy span { color:var(--muted); font-size:9px; font-weight:850; }
.dna-copy strong { display:block; margin-top:2px; color:var(--text); font-size:22px; }
.dna-copy p { margin:4px 0 0; color:var(--muted); font-size:9px; line-height:1.7; min-height:30px; }
.dna-meter { position:absolute; right:15px; left:15px; bottom:13px; height:5px; overflow:hidden; border-radius:99px; background:rgba(125,132,159,.12); }
.dna-meter i { display:block; height:100%; border-radius:inherit; background:linear-gradient(90deg,var(--dna-color),color-mix(in srgb,var(--dna-color) 45%,white)); box-shadow:0 0 15px color-mix(in srgb,var(--dna-color) 35%,transparent); }

.panel,.league-panel,.booklet-card,.review-hero,.review-toolbar,.question-card {
  backdrop-filter:blur(16px);
}
.panel { border-radius:28px; box-shadow:var(--shadow-sm); }
.section-intro { margin-bottom:17px; }
.section-intro h2 { letter-spacing:-.03em; }

.booklet-spotlight {
  position:relative; display:grid; grid-template-columns:1.05fr 1.4fr; gap:16px; align-items:stretch; margin-bottom:14px;
  padding:17px; overflow:hidden; border:1px solid rgba(101,87,255,.15); border-radius:25px;
  background:
    radial-gradient(circle at 85% 15%,rgba(24,199,192,.13),transparent 13rem),
    radial-gradient(circle at 12% 80%,rgba(101,87,255,.11),transparent 14rem),
    linear-gradient(145deg,rgba(255,255,255,.82),rgba(246,247,253,.68));
  box-shadow:var(--shadow-sm);
}
.exam-result-page.is-dark .booklet-spotlight { background:radial-gradient(circle at 85% 15%,rgba(24,199,192,.12),transparent 13rem),linear-gradient(145deg,rgba(17,23,39,.88),rgba(11,16,28,.76)); }
.spotlight-main { display:flex; flex-direction:column; justify-content:center; }
.spotlight-kicker { color:var(--primary); font-size:9px; font-weight:950; }
.spotlight-main h2 { margin:4px 0 5px; color:var(--text); font-size:18px; letter-spacing:-.025em; }
.spotlight-main p { margin:0; color:var(--muted); font-size:10px; line-height:1.8; max-width:460px; }
.spotlight-podium { display:grid; grid-template-columns:.8fr 1.25fr 1fr; gap:8px; align-items:stretch; }
.podium-item { min-width:0; display:flex; flex-direction:column; justify-content:center; padding:13px; border:1px solid var(--border); border-radius:17px; background:rgba(255,255,255,.5); }
.exam-result-page.is-dark .podium-item { background:rgba(255,255,255,.025); }
.podium-item span { color:var(--muted); font-size:8px; font-weight:850; }
.podium-item strong { margin-top:5px; overflow:hidden; color:var(--text); font-size:13px; text-overflow:ellipsis; white-space:nowrap; }
.podium-item small { margin-top:3px; color:var(--primary); font-size:10px; font-weight:950; }
.podium-item.first { border-color:rgba(245,184,75,.34); box-shadow:inset 0 1px 0 rgba(245,184,75,.18); }
.podium-item.first strong { font-size:14px; }

.booklet-toolbar { border-radius:18px; background:rgba(255,255,255,.54); backdrop-filter:blur(14px); }
.exam-result-page.is-dark .booklet-toolbar { background:rgba(255,255,255,.025); }
.booklet-sort-buttons button.active { background:linear-gradient(135deg,#6557ff,#4b3fe5); box-shadow:0 10px 25px rgba(75,63,229,.24); }
.booklet-cards { gap:14px; }
.booklet-card {
  position:relative; overflow:hidden; border-radius:27px; border:1px solid var(--border);
  background:linear-gradient(150deg,rgba(255,255,255,.84),rgba(247,248,252,.68));
  box-shadow:var(--shadow-sm); transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s ease,border-color .35s ease;
}
.exam-result-page.is-dark .booklet-card { background:linear-gradient(150deg,rgba(17,23,39,.9),rgba(11,16,28,.74)); }
.booklet-card::before { content:''; position:absolute; width:210px; height:210px; top:-130px; left:-110px; border-radius:50%; background:conic-gradient(from 90deg,rgba(101,87,255,.16),rgba(24,199,192,.10),transparent 70%); filter:blur(3px); }
.booklet-card::after { content:''; position:absolute; right:0; top:0; width:4px; height:100%; background:linear-gradient(180deg,#6557ff,#18c7c0,#54e3b5); opacity:.55; }
.booklet-card:hover { transform:translateY(-7px); box-shadow:0 28px 65px rgba(30,35,80,.14); border-color:rgba(101,87,255,.22); }
.booklet-card-top { position:relative; z-index:1; }
.booklet-number { background:linear-gradient(135deg,#6557ff,#4b3fe5) !important; box-shadow:0 10px 22px rgba(75,63,229,.25); }
.booklet-rank-badge { min-width:31px; height:31px; display:grid; place-items:center; border:1px solid var(--border); border-radius:10px; color:var(--primary); background:rgba(101,87,255,.06); font-size:9px; font-weight:950; }
.decile-badge { border-color:rgba(245,184,75,.22) !important; background:rgba(245,184,75,.07) !important; }
.booklet-score-row { position:relative; z-index:1; }
.booklet-score-orb { position:relative; width:68px; height:68px; flex:0 0 68px; display:grid; place-items:center; border-radius:50%; background:conic-gradient(#6557ff var(--booklet-score),rgba(101,87,255,.08) 0); box-shadow:0 8px 25px rgba(101,87,255,.13); }
.booklet-score-orb::before { content:''; position:absolute; width:56px; height:56px; border-radius:50%; background:var(--surface-solid); }
.exam-result-page.is-dark .booklet-score-orb::before { background:#111727; }
.booklet-score-orb span { position:relative; z-index:1; color:var(--text); font-size:12px; font-weight:950; }
.booklet-bar { position:relative; z-index:1; }
.booklet-bar-fill { background:linear-gradient(90deg,#6557ff 0%,#18c7c0 58%,#54e3b5 100%) !important; box-shadow:0 0 16px rgba(24,199,192,.18); }
.booklet-bar-label { color:var(--muted); font-size:8px; font-weight:850; }
.answer-stat { border-radius:14px; background:rgba(127,136,170,.045); }
.booklet-average { border-radius:18px; background:rgba(127,136,170,.045); padding:10px; }
.average-track { background:linear-gradient(90deg,rgba(101,87,255,.08),rgba(24,199,192,.10)) !important; }
.average-user-marker { box-shadow:0 0 0 4px rgba(101,87,255,.12),0 0 16px rgba(101,87,255,.45); }
.average-country-marker { box-shadow:0 0 0 4px rgba(24,199,192,.10),0 0 16px rgba(24,199,192,.40); }

.analytics-chart-card {
  border-radius:28px !important;
  background:linear-gradient(145deg,rgba(255,255,255,.82),rgba(247,248,252,.66)) !important;
}
.exam-result-page.is-dark .analytics-chart-card { background:linear-gradient(145deg,rgba(17,23,39,.88),rgba(11,16,28,.72)) !important; }
.chartjs-wrap,.comparison-chartjs-wrap,.progress-chartjs-wrap { border-radius:22px !important; }

.result-tabs {
  border:1px solid var(--border) !important;
  background:rgba(255,255,255,.68) !important;
  box-shadow:0 18px 55px rgba(28,34,73,.08) !important;
  backdrop-filter:blur(20px);
}
.exam-result-page.is-dark .result-tabs { background:rgba(13,18,31,.78) !important; }
.result-tab.active { color:#fff !important; background:linear-gradient(135deg,#6557ff,#4b3fe5) !important; box-shadow:0 12px 28px rgba(75,63,229,.23); }
.result-tab:hover:not(.active) { background:rgba(101,87,255,.06); color:var(--primary); }

.ranking-panel,.peak-panel { background:linear-gradient(145deg,rgba(255,255,255,.82),rgba(247,248,252,.65)) !important; }
.exam-result-page.is-dark .ranking-panel,.exam-result-page.is-dark .peak-panel { background:linear-gradient(145deg,rgba(17,23,39,.88),rgba(11,16,28,.72)) !important; }
.rank-card { border-radius:21px !important; background:rgba(127,136,170,.045) !important; }

.league-panel {
  border:1px solid rgba(101,87,255,.20) !important;
  box-shadow:0 30px 90px rgba(57,45,161,.16) !important;
}
.league-season { border-color:rgba(84,227,181,.24) !important; background:rgba(84,227,181,.07) !important; }

.scroll-top-button { background:linear-gradient(135deg,#6557ff,#18c7c0); box-shadow:0 18px 40px rgba(75,63,229,.28); border:0; }

@media (max-width: 900px) {
  .result-pulse { grid-template-columns:1fr; }
  .dna-grid { grid-template-columns:1fr; }
  .booklet-spotlight { grid-template-columns:1fr; }
}
@media (max-width: 650px) {
  .result-pulse { padding:14px; border-radius:20px; }
  .pulse-stats { grid-template-columns:repeat(2,1fr); }
  .pulse-stats div:nth-child(3) { border-inline-start:0; border-top:1px solid var(--border); }
  .pulse-stats div:nth-child(4) { border-top:1px solid var(--border); }
  .dna-heading { align-items:flex-start; flex-direction:column; }
  .spotlight-podium { grid-template-columns:1fr; }
  .booklet-score-orb { position:relative; width:60px; height:60px; flex-basis:60px; }
  .booklet-score-orb::before { width:50px; height:50px; }
}
</style>