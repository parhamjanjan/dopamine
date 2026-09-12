<template>
  <div
    class="profile-page"
    :class="{ 'profile-dark': isDark }"
  >
    <div class="page-wrapper">

      <!-- ========================================================= -->
      <!-- HEADER -->
      <!-- ========================================================= -->

      <header class="profile-header">

        <div class="profile-header-content">

          <span class="header-eyebrow">
            حساب کاربری
          </span>

          <h1>
            پروفایل من
          </h1>

          <p>
            اطلاعات حساب و مشخصات شخصی خود را مدیریت کنید.
          </p>

        </div>

        <div class="header-badge">

          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.7"
            aria-hidden="true"
          >
            <circle
              cx="12"
              cy="8"
              r="4"
            />

            <path
              d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"
            />
          </svg>

        </div>

      </header>


      <!-- ========================================================= -->
      <!-- PROFILE OVERVIEW -->
      <!-- ========================================================= -->

      <section class="profile-overview">

        <div class="profile-glow profile-glow-one"></div>

        <div class="profile-glow profile-glow-two"></div>

        <div class="profile-overview-content">

          <!-- AVATAR -->

          <div class="avatar-wrapper">

            <div class="profile-avatar">

              <img
                v-if="profileImage"
                :src="profileImage"
                alt="تصویر پروفایل"
              />

              <span v-else>
                {{ avatarLetter }}
              </span>

            </div>

            <button
              type="button"
              class="avatar-edit-button"
              aria-label="تغییر تصویر پروفایل"
              @click="openFilePicker"
            >

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                aria-hidden="true"
              >
                <path d="M12 20h9" />

                <path
                  d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"
                />
              </svg>

            </button>

            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              hidden
              @change="handleImageChange"
            />

          </div>


          <!-- IDENTITY -->

          <div class="profile-identity">

            <div class="profile-name-row">

              <h2>
                {{ fullName }}
              </h2>

              <span
                class="verified-badge"
                title="حساب فعال"
              >

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path d="m5 12 4 4L19 6" />
                </svg>

              </span>

            </div>

            <span class="profile-username">
              @{{ auth.user?.username || 'username' }}
            </span>

            <span
              v-if="auth.user?.school"
              class="school-badge"
            >
              {{ auth.user.school }}
            </span>

          </div>


          <!-- QUICK STATS -->

          <div class="profile-quick-stats">

            <div class="quick-stat">

              <strong>
                {{ gradeLabel }}
              </strong>

              <span>
                پایه
              </span>

            </div>

            <div class="quick-stat">

              <strong>
                {{ fieldLabel }}
              </strong>

              <span>
                رشته
              </span>

            </div>

            <div class="quick-stat">

              <strong>
                {{ auth.user?.province || 'ثبت نشده' }}
              </strong>

              <span>
                استان
              </span>

            </div>

          </div>

        </div>

      </section>


      <!-- ========================================================= -->
      <!-- TABS -->
      <!-- ========================================================= -->

      <nav
        class="profile-tabs"
        role="tablist"
        aria-label="بخش‌های پروفایل"
      >

        <button
          type="button"
          role="tab"
          class="profile-tab"
          :class="{ active: activeTab === 'overview' }"
          :aria-selected="activeTab === 'overview'"
          @click="setActiveTab('overview')"
        >

          <span class="tab-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              aria-hidden="true"
            >
              <rect
                x="3"
                y="3"
                width="7"
                height="7"
                rx="1.5"
              />

              <rect
                x="14"
                y="3"
                width="7"
                height="7"
                rx="1.5"
              />

              <rect
                x="3"
                y="14"
                width="7"
                height="7"
                rx="1.5"
              />

              <rect
                x="14"
                y="14"
                width="7"
                height="7"
                rx="1.5"
              />
            </svg>

          </span>

          <span>
            نمای کلی
          </span>

        </button>


        <button
          type="button"
          role="tab"
          class="profile-tab"
          :class="{ active: activeTab === 'personal' }"
          :aria-selected="activeTab === 'personal'"
          @click="setActiveTab('personal')"
        >

          <span class="tab-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="8"
                r="4"
              />

              <path
                d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"
              />
            </svg>

          </span>

          <span>
            اطلاعات شخصی
          </span>

        </button>


        <button
          type="button"
          role="tab"
          class="profile-tab"
          :class="{ active: activeTab === 'academic' }"
          :aria-selected="activeTab === 'academic'"
          @click="setActiveTab('academic')"
        >

          <span class="tab-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              aria-hidden="true"
            >
              <path d="M3 10 12 5l9 5-9 5-9-5Z" />

              <path
                d="M7 12.5V17c2.7 2.2 7.3 2.2 10 0v-4.5"
              />

              <path d="M21 10v6" />

            </svg>

          </span>

          <span>
            تحصیلات
          </span>

        </button>


        <button
          type="button"
          role="tab"
          class="profile-tab"
          :class="{ active: activeTab === 'security' }"
          :aria-selected="activeTab === 'security'"
          @click="setActiveTab('security')"
        >

          <span class="tab-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              aria-hidden="true"
            >
              <rect
                x="4"
                y="10"
                width="16"
                height="10"
                rx="2"
              />

              <path
                d="M8 10V7a4 4 0 0 1 8 0v3"
              />

              <circle
                cx="12"
                cy="15"
                r="1"
              />

            </svg>

          </span>

          <span>
            امنیت و حساب
          </span>

        </button>

      </nav>


      <!-- ========================================================= -->
      <!-- TAB CONTENT -->
      <!-- ========================================================= -->

      <main class="profile-tab-content">

        <Transition
          name="tab"
          mode="out-in"
        >

          <!-- ===================================================== -->
          <!-- OVERVIEW TAB -->
          <!-- ===================================================== -->

          <section
            v-if="activeTab === 'overview'"
            key="overview"
            class="tab-panel"
          >

            <div class="overview-grid">

              <!-- ABOUT -->

              <section class="profile-card about-card">

                <div class="section-header">

                  <div class="section-heading">

                    <div class="section-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                        aria-hidden="true"
                      >
                        <circle
                          cx="12"
                          cy="12"
                          r="9"
                        />

                        <path d="M12 10v6" />

                        <path d="M12 7h.01" />

                      </svg>

                    </div>

                    <div>

                      <h3>
                        درباره من
                      </h3>

                      <span>
                        معرفی کوتاه
                      </span>

                    </div>

                  </div>

                  <button
                    type="button"
                    class="edit-button"
                    @click="openEditModal"
                  >
                    ویرایش
                  </button>

                </div>


                <div class="bio-content">

                  <p v-if="auth.user?.bio">
                    {{ auth.user.bio }}
                  </p>

                  <div
                    v-else
                    class="empty-state"
                  >

                    <span class="empty-state-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M12 3v18" />
                        <path d="M3 12h18" />
                      </svg>

                    </span>

                    <strong>
                      هنوز چیزی درباره خودتان ننوشته‌اید
                    </strong>

                    <span>
                      یک معرفی کوتاه به پروفایل خود اضافه کنید.
                    </span>

                  </div>

                </div>

              </section>


              <!-- PROFILE SUMMARY -->

              <section class="profile-card summary-card">

                <div class="section-header">

                  <div class="section-heading">

                    <div class="section-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M4 19V5" />

                        <path d="M4 19h16" />

                        <path d="m7 15 3-4 3 2 5-6" />

                      </svg>

                    </div>

                    <div>

                      <h3>
                        خلاصه حساب
                      </h3>

                      <span>
                        وضعیت اطلاعات پروفایل
                      </span>

                    </div>

                  </div>

                </div>


                <div class="summary-list">

                  <div class="summary-row">

                    <span>
                      نام کاربری
                    </span>

                    <strong dir="ltr">
                      @{{ auth.user?.username || 'ثبت نشده' }}
                    </strong>

                  </div>


                  <div class="summary-row">

                    <span>
                      شماره تلفن
                    </span>

                    <strong dir="ltr">
                      {{ auth.user?.phone_number || 'ثبت نشده' }}
                    </strong>

                  </div>


                  <div class="summary-row">

                    <span>
                      وضعیت حساب
                    </span>

                    <strong class="status-active">

                      <span></span>

                      فعال

                    </strong>

                  </div>


                  <div class="summary-row">

                    <span>
                      تکمیل اطلاعات
                    </span>

                    <strong>
                      {{ profileCompletion }}٪
                    </strong>

                  </div>

                </div>


                <div class="completion-wrapper">

                  <div class="completion-header">

                    <span>
                      میزان تکمیل پروفایل
                    </span>

                    <strong>
                      {{ profileCompletion }}٪
                    </strong>

                  </div>

                  <div class="completion-track">

                    <div
                      class="completion-value"
                      :style="{ width: `${profileCompletion}%` }"
                    ></div>

                  </div>

                </div>

              </section>


              <!-- QUICK INFORMATION -->

              <section class="profile-card overview-info-card">

                <div class="section-header">

                  <div class="section-heading">

                    <div class="section-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M4 6h16" />

                        <path d="M4 12h16" />

                        <path d="M4 18h16" />

                      </svg>

                    </div>

                    <div>

                      <h3>
                        اطلاعات سریع
                      </h3>

                      <span>
                        مهم‌ترین مشخصات حساب
                      </span>

                    </div>

                  </div>

                </div>


                <div class="quick-info-grid">

                  <button
                    type="button"
                    class="quick-info-item"
                    @click="setActiveTab('personal')"
                  >

                    <span class="quick-info-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <circle
                          cx="12"
                          cy="8"
                          r="4"
                        />

                        <path
                          d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"
                        />

                      </svg>

                    </span>

                    <span class="quick-info-content">

                      <small>
                        اطلاعات شخصی
                      </small>

                      <strong>
                        {{ fullName }}
                      </strong>

                    </span>

                    <span class="quick-info-arrow">
                      ←
                    </span>

                  </button>


                  <button
                    type="button"
                    class="quick-info-item"
                    @click="setActiveTab('academic')"
                  >

                    <span class="quick-info-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M3 10 12 5l9 5-9 5-9-5Z" />

                        <path
                          d="M7 12.5V17c2.7 2.2 7.3 2.2 10 0v-4.5"
                        />

                      </svg>

                    </span>

                    <span class="quick-info-content">

                      <small>
                        وضعیت تحصیلی
                      </small>

                      <strong>
                        {{ gradeLabel }} · {{ fieldLabel }}
                      </strong>

                    </span>

                    <span class="quick-info-arrow">
                      ←
                    </span>

                  </button>

                </div>

              </section>


              <!-- PROFILE ACTIONS -->

              <section class="profile-card overview-actions-card">

                <div class="section-header">

                  <div class="section-heading">

                    <div class="section-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M12 3v12" />

                        <path d="M7 8 12 3l5 5" />

                        <path d="M5 12v7h14v-7" />

                      </svg>

                    </div>

                    <div>

                      <h3>
                        دسترسی سریع
                      </h3>

                      <span>
                        مدیریت بخش‌های حساب
                      </span>

                    </div>

                  </div>

                </div>


                <div class="overview-action-grid">

                  <button
                    type="button"
                    class="overview-action"
                    @click="openEditModal"
                  >

                    <span class="overview-action-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M12 20h9" />

                        <path
                          d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"
                        />

                      </svg>

                    </span>

                    <span>
                      ویرایش پروفایل
                    </span>

                  </button>


                  <button
                    type="button"
                    class="overview-action"
                    @click="openAcademicModal"
                  >

                    <span class="overview-action-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M3 10 12 5l9 5-9 5-9-5Z" />

                        <path
                          d="M7 12.5V17c2.7 2.2 7.3 2.2 10 0v-4.5"
                        />

                      </svg>

                    </span>

                    <span>
                      ویرایش تحصیلات
                    </span>

                  </button>


                  <button
                    type="button"
                    class="overview-action"
                    @click="openPasswordModal"
                  >

                    <span class="overview-action-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <rect
                          x="4"
                          y="10"
                          width="16"
                          height="10"
                          rx="2"
                        />

                        <path
                          d="M8 10V7a4 4 0 0 1 8 0v3"
                        />

                      </svg>

                    </span>

                    <span>
                      تغییر رمز عبور
                    </span>

                  </button>

                </div>

              </section>

            </div>

          </section>


          <!-- ===================================================== -->
          <!-- PERSONAL TAB -->
          <!-- ===================================================== -->

          <section
            v-else-if="activeTab === 'personal'"
            key="personal"
            class="tab-panel"
          >

            <section class="profile-card">

              <div class="section-header">

                <div class="section-heading">

                  <div class="section-icon">

                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.8"
                    >
                      <circle
                        cx="12"
                        cy="8"
                        r="4"
                      />

                      <path
                        d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"
                      />

                    </svg>

                  </div>

                  <div>

                    <h3>
                      اطلاعات شخصی
                    </h3>

                    <span>
                      مشخصات و اطلاعات پایه حساب
                    </span>

                  </div>

                </div>


                <button
                  type="button"
                  class="edit-button"
                  @click="openEditModal"
                >
                  ویرایش اطلاعات
                </button>

              </div>


              <div class="personal-profile-banner">

                <div class="personal-banner-avatar">

                  <img
                    v-if="profileImage"
                    :src="profileImage"
                    alt="تصویر پروفایل"
                  />

                  <span v-else>
                    {{ avatarLetter }}
                  </span>

                </div>


                <div class="personal-banner-content">

                  <strong>
                    {{ fullName }}
                  </strong>

                  <span>
                    @{{ auth.user?.username || 'username' }}
                  </span>

                </div>


                <button
                  type="button"
                  class="secondary-outline-button"
                  @click="openFilePicker"
                >
                  تغییر تصویر
                </button>

              </div>


              <div class="info-grid personal-info-grid">

                <div class="info-item">

                  <span>
                    نام و نام خانوادگی
                  </span>

                  <strong>
                    {{ fullName }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    نام کاربری
                  </span>

                  <strong dir="ltr">
                    {{ auth.user?.username || 'ثبت نشده' }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    شماره تلفن
                  </span>

                  <strong dir="ltr">
                    {{ auth.user?.phone_number || 'ثبت نشده' }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    جنسیت
                  </span>

                  <strong>
                    {{ genderLabel }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    تاریخ تولد
                  </span>

                  <strong>
                    {{ birthDateLabel }}
                  </strong>

                </div>

              </div>


              <div class="profile-card-divider"></div>


              <div class="bio-section">

                <div class="bio-section-heading">

                  <strong>
                    درباره من
                  </strong>

                  <span>
                    معرفی کوتاه شما
                  </span>

                </div>


                <div class="bio-content">

                  <p v-if="auth.user?.bio">
                    {{ auth.user.bio }}
                  </p>

                  <p
                    v-else
                    class="empty-text"
                  >
                    هنوز توضیحی برای پروفایل خود ثبت نکرده‌اید.
                  </p>

                </div>

              </div>

            </section>

          </section>


          <!-- ===================================================== -->
          <!-- ACADEMIC TAB -->
          <!-- ===================================================== -->

          <section
            v-else-if="activeTab === 'academic'"
            key="academic"
            class="tab-panel"
          >

            <section class="profile-card">

              <div class="section-header">

                <div class="section-heading">

                  <div class="section-icon">

                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.8"
                    >
                      <path d="M3 10 12 5l9 5-9 5-9-5Z" />

                      <path
                        d="M7 12.5V17c2.7 2.2 7.3 2.2 10 0v-4.5"
                      />

                      <path d="M21 10v6" />

                    </svg>

                  </div>

                  <div>

                    <h3>
                      اطلاعات تحصیلی
                    </h3>

                    <span>
                      وضعیت آموزشی و مشخصات مدرسه
                    </span>

                  </div>

                </div>


                <button
                  type="button"
                  class="edit-button"
                  @click="openAcademicModal"
                >
                  ویرایش اطلاعات
                </button>

              </div>


              <div class="academic-highlight">

                <div class="academic-highlight-icon">

                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.7"
                  >
                    <path d="M3 10 12 5l9 5-9 5-9-5Z" />

                    <path
                      d="M7 12.5V17c2.7 2.2 7.3 2.2 10 0v-4.5"
                    />

                  </svg>

                </div>


                <div class="academic-highlight-content">

                  <span>
                    وضعیت فعلی
                  </span>

                  <strong>
                    {{ gradeLabel }} · رشته {{ fieldLabel }}
                  </strong>

                  <small>
                    {{ auth.user?.school || 'مدرسه ثبت نشده' }}
                  </small>

                </div>

              </div>


              <div class="academic-grid">

                <div class="info-item">

                  <span>
                    پایه تحصیلی
                  </span>

                  <strong>
                    {{ gradeLabel }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    رشته
                  </span>

                  <strong>
                    {{ fieldLabel }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    مدرسه
                  </span>

                  <strong>
                    {{ auth.user?.school || 'ثبت نشده' }}
                  </strong>

                </div>


                <div class="info-item">

                  <span>
                    استان
                  </span>

                  <strong>
                    {{ auth.user?.province || 'ثبت نشده' }}
                  </strong>

                </div>

              </div>

            </section>

          </section>


          <!-- ===================================================== -->
          <!-- SECURITY TAB -->
          <!-- ===================================================== -->

          <section
            v-else-if="activeTab === 'security'"
            key="security"
            class="tab-panel"
          >

            <div class="security-grid">

              <!-- SECURITY INTRO -->

              <section class="profile-card security-intro-card">

                <div class="security-visual">

                  <div class="security-visual-icon">

                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.7"
                    >
                      <rect
                        x="4"
                        y="10"
                        width="16"
                        height="10"
                        rx="2"
                      />

                      <path
                        d="M8 10V7a4 4 0 0 1 8 0v3"
                      />

                      <path d="M12 14v3" />

                    </svg>

                  </div>

                </div>


                <div class="security-intro-content">

                  <span class="security-label">
                    امنیت حساب
                  </span>

                  <h3>
                    حساب شما تحت کنترل شماست
                  </h3>

                  <p>
                    برای حفظ امنیت حساب، رمز عبور خود را به‌صورت دوره‌ای
                    تغییر دهید و اطلاعات حساب خود را به‌روز نگه دارید.
                  </p>

                  <button
                    type="button"
                    class="primary-button"
                    @click="openPasswordModal"
                  >
                    تغییر رمز عبور
                  </button>

                </div>

              </section>


              <!-- ACCOUNT ACTIONS -->

              <section class="profile-card actions-card">

                <div class="section-header">

                  <div class="section-heading">

                    <div class="section-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M12 3v12" />

                        <path d="M7 8 12 3l5 5" />

                        <path d="M5 12v7h14v-7" />

                      </svg>

                    </div>

                    <div>

                      <h3>
                        عملیات حساب
                      </h3>

                      <span>
                        مدیریت حساب کاربری
                      </span>

                    </div>

                  </div>

                </div>


                <div class="actions-list">

                  <!-- EDIT PROFILE -->

                  <button
                    type="button"
                    class="action-item"
                    @click="openEditModal"
                  >

                    <span class="action-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M12 20h9" />

                        <path
                          d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"
                        />

                      </svg>

                    </span>


                    <span class="action-content">

                      <strong>
                        ویرایش پروفایل
                      </strong>

                      <small>
                        اطلاعات شخصی پروفایل خود را ویرایش کنید.
                      </small>

                    </span>


                    <span class="action-arrow">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="m9 18 6-6-6-6" />
                      </svg>

                    </span>

                  </button>


                  <!-- CHANGE PASSWORD -->

                  <button
                    type="button"
                    class="action-item"
                    @click="openPasswordModal"
                  >

                    <span class="action-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <rect
                          x="4"
                          y="10"
                          width="16"
                          height="10"
                          rx="2"
                        />

                        <path
                          d="M8 10V7a4 4 0 0 1 8 0v3"
                        />

                        <circle
                          cx="12"
                          cy="15"
                          r="1"
                        />

                      </svg>

                    </span>


                    <span class="action-content">

                      <strong>
                        تغییر رمز عبور
                      </strong>

                      <small>
                        رمز عبور حساب خود را تغییر دهید.
                      </small>

                    </span>


                    <span class="action-arrow">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="m9 18 6-6-6-6" />
                      </svg>

                    </span>

                  </button>


                  <!-- LOGOUT -->

                  <button
                    type="button"
                    class="action-item action-danger"
                    @click="logout"
                  >

                    <span class="action-icon">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="M10 17l5-5-5-5" />

                        <path d="M15 12H3" />

                        <path d="M21 3v18" />

                      </svg>

                    </span>


                    <span class="action-content">

                      <strong>
                        خروج از حساب
                      </strong>

                      <small>
                        از حساب کاربری خود خارج شوید.
                      </small>

                    </span>


                    <span class="action-arrow">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path d="m9 18 6-6-6-6" />
                      </svg>

                    </span>

                  </button>

                </div>

              </section>

            </div>

          </section>

        </Transition>

      </main>

    </div>


    <!-- ========================================================= -->
    <!-- EDIT PERSONAL MODAL -->
    <!-- ========================================================= -->

    <Transition name="modal">

      <div
        v-if="showEditModal"
        class="modal-backdrop"
        @click.self="closeEditModal"
      >

        <section
          class="edit-modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="edit-modal-title"
        >

          <div class="modal-header">

            <div>

              <span class="modal-eyebrow">
                اطلاعات شخصی
              </span>

              <h2 id="edit-modal-title">
                ویرایش پروفایل
              </h2>

              <p>
                اطلاعات شخصی خود را به‌روزرسانی کنید.
              </p>

            </div>


            <button
              type="button"
              class="modal-close"
              aria-label="بستن"
              @click="closeEditModal"
            >

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
              >
                <path d="M18 6 6 18" />
                <path d="m6 6 12 12" />
              </svg>

            </button>

          </div>


          <form
            class="edit-form"
            @submit.prevent="saveProfile"
          >

            <div class="form-grid">

              <label class="form-field">

                <span>
                  نام
                </span>

                <input
                  v-model="editForm.first_name"
                  type="text"
                  maxlength="100"
                  placeholder="نام"
                />

              </label>


              <label class="form-field">

                <span>
                  نام خانوادگی
                </span>

                <input
                  v-model="editForm.last_name"
                  type="text"
                  maxlength="100"
                  placeholder="نام خانوادگی"
                />

              </label>


              <label class="form-field">

                <span>
                  شماره تلفن
                </span>

                <input
                  v-model="editForm.phone_number"
                  type="tel"
                  maxlength="20"
                  placeholder="شماره تلفن"
                />

              </label>


              <label class="form-field">

                <span>
                  جنسیت
                </span>

                <select v-model="editForm.gender">

                  <option value="">
                    انتخاب جنسیت
                  </option>

                  <option value="male">
                    مرد
                  </option>

                  <option value="female">
                    زن
                  </option>

                </select>

              </label>


              <label class="form-field form-field-full">

                <span>
                  درباره من
                </span>

                <textarea
                  v-model="editForm.bio"
                  maxlength="500"
                  rows="4"
                  placeholder="کمی درباره خودتان بنویسید..."
                ></textarea>

              </label>

            </div>


            <div class="modal-actions">

              <button
                type="button"
                class="modal-cancel"
                :disabled="isSavingProfile"
                @click="closeEditModal"
              >
                انصراف
              </button>


              <button
                type="submit"
                class="modal-save"
                :disabled="isSavingProfile"
              >

                <span
                  v-if="isSavingProfile"
                  class="button-spinner"
                ></span>

                <span v-if="isSavingProfile">
                  در حال ذخیره...
                </span>

                <span v-else>
                  ذخیره تغییرات
                </span>

              </button>

            </div>

          </form>

        </section>

      </div>

    </Transition>


    <!-- ========================================================= -->
    <!-- ACADEMIC MODAL -->
    <!-- ========================================================= -->

    <Transition name="modal">

      <div
        v-if="showAcademicModal"
        class="modal-backdrop"
        @click.self="closeAcademicModal"
      >

        <section
          class="edit-modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="academic-modal-title"
        >

          <div class="modal-header">

            <div>

              <span class="modal-eyebrow">
                اطلاعات آموزشی
              </span>

              <h2 id="academic-modal-title">
                ویرایش اطلاعات تحصیلی
              </h2>

              <p>
                مشخصات تحصیلی خود را به‌روزرسانی کنید.
              </p>

            </div>


            <button
              type="button"
              class="modal-close"
              aria-label="بستن"
              @click="closeAcademicModal"
            >

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
              >
                <path d="M18 6 6 18" />
                <path d="m6 6 12 12" />
              </svg>

            </button>

          </div>


          <form
            class="edit-form"
            @submit.prevent="saveAcademic"
          >

            <div class="form-grid">

              <label class="form-field">

                <span>
                  پایه تحصیلی
                </span>

                <select v-model="academicForm.grade">

                  <option value="">
                    انتخاب پایه
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


              <label class="form-field">

                <span>
                  رشته
                </span>

                <select v-model="academicForm.field">

                  <option value="">
                    انتخاب رشته
                  </option>

                  <option value="experimental">
                    تجربی
                  </option>

                  <option value="mathematics">
                    ریاضی
                  </option>

                  <option value="humanities">
                    انسانی
                  </option>

                </select>

              </label>


              <label class="form-field">

                <span>
                  استان
                </span>

                <select v-model="academicForm.province">

                  <option value="">
                    انتخاب استان
                  </option>

                  <option
                    v-for="province in iranProvinces"
                    :key="province"
                    :value="province"
                  >
                    {{ province }}
                  </option>

                </select>

              </label>


              <label class="form-field">

                <span>
                  مدرسه
                </span>

                <input
                  v-model="academicForm.school"
                  type="text"
                  maxlength="200"
                  placeholder="نام مدرسه"
                />

              </label>

            </div>


            <div class="modal-actions">

              <button
                type="button"
                class="modal-cancel"
                :disabled="isSavingAcademic"
                @click="closeAcademicModal"
              >
                انصراف
              </button>


              <button
                type="submit"
                class="modal-save"
                :disabled="isSavingAcademic"
              >

                <span
                  v-if="isSavingAcademic"
                  class="button-spinner"
                ></span>

                <span v-if="isSavingAcademic">
                  در حال ذخیره...
                </span>

                <span v-else>
                  ذخیره تغییرات
                </span>

              </button>

            </div>

          </form>

        </section>

      </div>

    </Transition>


    <!-- ========================================================= -->
    <!-- PASSWORD MODAL -->
    <!-- ========================================================= -->

    <Transition name="modal">

      <div
        v-if="showPasswordModal"
        class="modal-backdrop"
        @click.self="closePasswordModal"
      >

        <section
          class="edit-modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="password-modal-title"
        >

          <div class="modal-header">

            <div>

              <span class="modal-eyebrow">
                امنیت حساب
              </span>

              <h2 id="password-modal-title">
                تغییر رمز عبور
              </h2>

              <p>
                برای امنیت بیشتر، رمز عبور حساب خود را
                به‌روزرسانی کنید.
              </p>

            </div>


            <button
              type="button"
              class="modal-close"
              aria-label="بستن"
              @click="closePasswordModal"
            >

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
              >
                <path d="M18 6 6 18" />
                <path d="m6 6 12 12" />
              </svg>

            </button>

          </div>


          <form
            class="edit-form"
            @submit.prevent="changePassword"
          >

            <div class="form-grid password-grid">

              <label class="form-field">

                <span>
                  رمز عبور فعلی
                </span>

                <input
                  v-model="passwordForm.current_password"
                  type="password"
                  autocomplete="current-password"
                  placeholder="رمز عبور فعلی"
                  required
                />

              </label>


              <label class="form-field">

                <span>
                  رمز عبور جدید
                </span>

                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  autocomplete="new-password"
                  placeholder="رمز عبور جدید"
                  minlength="8"
                  required
                />

              </label>


              <label class="form-field form-field-full">

                <span>
                  تکرار رمز عبور جدید
                </span>

                <input
                  v-model="passwordForm.new_password_confirm"
                  type="password"
                  autocomplete="new-password"
                  placeholder="تکرار رمز عبور جدید"
                  minlength="8"
                  required
                />

              </label>

            </div>


            <div class="password-hint">

              <span class="password-hint-icon">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.7"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="9"
                  />

                  <path d="M12 10v6" />

                  <path d="M12 7h.01" />

                </svg>

              </span>

              <span>
                رمز عبور جدید باید حداقل ۸ کاراکتر باشد.
              </span>

            </div>


            <div class="modal-actions">

              <button
                type="button"
                class="modal-cancel"
                :disabled="isChangingPassword"
                @click="closePasswordModal"
              >
                انصراف
              </button>


              <button
                type="submit"
                class="modal-save"
                :disabled="isChangingPassword"
              >

                <span
                  v-if="isChangingPassword"
                  class="button-spinner"
                ></span>

                <span v-if="isChangingPassword">
                  در حال تغییر...
                </span>

                <span v-else>
                  تغییر رمز عبور
                </span>

              </button>

            </div>

          </form>

        </section>

      </div>

    </Transition>


    <!-- ========================================================= -->
    <!-- TOAST -->
    <!-- ========================================================= -->

    <Transition name="toast">

      <div
        v-if="toast.visible"
        class="toast"
        :class="`toast-${toast.type}`"
      >

        <span class="toast-icon">

          <svg
            v-if="toast.type === 'success'"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="m5 12 4 4L19 6" />
          </svg>

          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle
              cx="12"
              cy="12"
              r="9"
            />

            <path d="M12 8v4" />

            <path d="M12 16h.01" />

          </svg>

        </span>


        <span>
          {{ toast.message }}
        </span>

      </div>

    </Transition>

  </div>
</template>


<script setup>

import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref
} from 'vue'

import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

import api from '../services/api'


const auth = useAuthStore()

const router = useRouter()


// ============================================================
// GENERAL
// ============================================================

const fileInput = ref(null)

const isDark = ref(false)

const activeTab = ref('overview')

const toast = ref({
  visible: false,
  message: '',
  type: 'success'
})

let themeObserver = null

let toastTimer = null


// ============================================================
// PERSONAL PROFILE MODAL
// ============================================================

const showEditModal = ref(false)

const isSavingProfile = ref(false)

const editForm = ref({
  first_name: '',
  last_name: '',
  phone_number: '',
  gender: '',
  bio: ''
})


// ============================================================
// ACADEMIC MODAL
// ============================================================

const showAcademicModal = ref(false)

const isSavingAcademic = ref(false)

const academicForm = ref({
  grade: '',
  field: '',
  province: '',
  school: ''
})


// ============================================================
// PASSWORD MODAL
// ============================================================

const showPasswordModal = ref(false)

const isChangingPassword = ref(false)

const passwordForm = ref({
  current_password: '',
  new_password: '',
  new_password_confirm: ''
})


// ============================================================
// IRAN PROVINCES
// ============================================================

const iranProvinces = [
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


// ============================================================
// COMPUTED
// ============================================================

const profileImage = computed(() => {

  const image = auth.user?.profile_image

  if (!image) {
    return null
  }

  if (image.startsWith('http')) {
    return image
  }

  return `http://127.0.0.1:8000${image}`
})


const avatarLetter = computed(() => {

  const firstName =
    auth.user?.first_name?.trim()

  if (firstName) {
    return firstName.charAt(0)
  }

  const username =
    auth.user?.username?.trim()

  if (username) {
    return username.charAt(0)
  }

  return 'ک'
})


const fullName = computed(() => {

  const firstName =
    auth.user?.first_name || ''

  const lastName =
    auth.user?.last_name || ''

  const name =
    `${firstName} ${lastName}`.trim()

  return name || 'کاربر دوپامین'
})


const gradeLabel = computed(() => {

  const grades = {
    '10': 'دهم',
    '11': 'یازدهم',
    '12': 'دوازدهم'
  }

  return (
    grades[auth.user?.grade] ||
    'ثبت نشده'
  )
})


const fieldLabel = computed(() => {

  const fields = {
    experimental: 'تجربی',
    mathematics: 'ریاضی',
    humanities: 'انسانی'
  }

  return (
    fields[auth.user?.field] ||
    'ثبت نشده'
  )
})


const genderLabel = computed(() => {

  const genders = {
    male: 'مرد',
    female: 'زن'
  }

  return (
    genders[auth.user?.gender] ||
    'ثبت نشده'
  )
})


const birthDateLabel = computed(() => {

  if (auth.user?.birth_date_jalali) {
    return auth.user.birth_date_jalali
  }

  if (auth.user?.birth_date_gregorian) {
    return auth.user.birth_date_gregorian
  }

  return 'ثبت نشده'
})


const profileCompletion = computed(() => {

  const user = auth.user

  if (!user) {
    return 0
  }

  const fields = [
    user.first_name,
    user.last_name,
    user.phone_number,
    user.gender,
    user.bio,
    user.grade,
    user.field,
    user.province,
    user.school,
    user.profile_image
  ]

  const completed =
    fields.filter(
      value =>
        value !== null &&
        value !== undefined &&
        String(value).trim() !== ''
    ).length

  return Math.round(
    (completed / fields.length) * 100
  )
})


// ============================================================
// TABS
// ============================================================

function setActiveTab(tab) {

  const validTabs = [
    'overview',
    'personal',
    'academic',
    'security'
  ]

  if (!validTabs.includes(tab)) {
    return
  }

  activeTab.value = tab

  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}


// ============================================================
// PROFILE IMAGE
// ============================================================

function openFilePicker() {
  fileInput.value?.click()
}


async function handleImageChange(event) {

  const file =
    event.target.files?.[0]

  if (!file) {
    return
  }


  if (!file.type.startsWith('image/')) {

    showToast(
      'فایل انتخاب‌شده تصویر نیست.',
      'error'
    )

    event.target.value = ''

    return
  }


  if (file.size > 5 * 1024 * 1024) {

    showToast(
      'حجم تصویر نباید بیشتر از ۵ مگابایت باشد.',
      'error'
    )

    event.target.value = ''

    return
  }


  const formData = new FormData()

  formData.append(
    'profile_image',
    file
  )


  try {

    const response =
      await api.patch(
        '/accounts/me/',
        formData
      )

    auth.user = response.data

    localStorage.setItem(
      'user',
      JSON.stringify(response.data)
    )

    showToast(
      'تصویر پروفایل با موفقیت تغییر کرد.'
    )

  } catch (error) {

    console.error(
      'خطای profile_image:',
      error.response?.data?.errors?.profile_image
    )

    console.error(
      'پاسخ کامل:',
      error.response?.data
    )


    const imageError =
      error.response?.data?.errors?.profile_image?.[0]


    showToast(
      imageError ||
        'آپلود تصویر با خطا مواجه شد.',
      'error'
    )

  } finally {

    event.target.value = ''

  }
}


// ============================================================
// PERSONAL PROFILE
// ============================================================

function openEditModal() {

  activeTab.value = 'personal'

  editForm.value = {

    first_name:
      auth.user?.first_name || '',

    last_name:
      auth.user?.last_name || '',

    phone_number:
      auth.user?.phone_number || '',

    gender:
      auth.user?.gender || '',

    bio:
      auth.user?.bio || ''

  }

  showAcademicModal.value = false

  showPasswordModal.value = false

  showEditModal.value = true
}


function closeEditModal() {

  if (isSavingProfile.value) {
    return
  }

  showEditModal.value = false
}


async function saveProfile() {

  if (isSavingProfile.value) {
    return
  }

  isSavingProfile.value = true


  try {

    const response =
      await api.patch(
        '/accounts/me/',
        {

          first_name:
            editForm.value.first_name.trim(),

          last_name:
            editForm.value.last_name.trim(),

          phone_number:
            editForm.value.phone_number.trim(),

          gender:
            editForm.value.gender,

          bio:
            editForm.value.bio.trim()

        }
      )


    auth.user = response.data

    localStorage.setItem(
      'user',
      JSON.stringify(response.data)
    )


    showEditModal.value = false


    showToast(
      'اطلاعات پروفایل با موفقیت ذخیره شد.'
    )

  } catch (error) {

    console.error(
      'خطا در ذخیره پروفایل:',
      error.response?.data || error
    )


    const errors =
      error.response?.data?.errors


    if (errors) {

      const firstError =
        Object.values(errors)
          .flat()
          .find(Boolean)


      showToast(
        firstError ||
          'اطلاعات واردشده معتبر نیست.',
        'error'
      )

    } else {

      showToast(
        'ذخیره اطلاعات با خطا مواجه شد.',
        'error'
      )

    }

  } finally {

    isSavingProfile.value = false

  }
}


// ============================================================
// ACADEMIC
// ============================================================

function openAcademicModal() {

  activeTab.value = 'academic'

  academicForm.value = {

    grade:
      auth.user?.grade || '',

    field:
      auth.user?.field || '',

    province:
      auth.user?.province || '',

    school:
      auth.user?.school || ''

  }

  showEditModal.value = false

  showPasswordModal.value = false

  showAcademicModal.value = true
}


function closeAcademicModal() {

  if (isSavingAcademic.value) {
    return
  }

  showAcademicModal.value = false
}


async function saveAcademic() {

  if (isSavingAcademic.value) {
    return
  }

  isSavingAcademic.value = true


  try {

    const response =
      await api.patch(
        '/accounts/me/',
        {

          grade:
            academicForm.value.grade,

          field:
            academicForm.value.field,

          province:
            academicForm.value.province,

          school:
            academicForm.value.school.trim()

        }
      )


    auth.user = response.data

    localStorage.setItem(
      'user',
      JSON.stringify(response.data)
    )


    showAcademicModal.value = false


    showToast(
      'اطلاعات تحصیلی با موفقیت ذخیره شد.'
    )

  } catch (error) {

    console.error(
      'خطا در ذخیره اطلاعات تحصیلی:',
      error.response?.data || error
    )


    const errors =
      error.response?.data?.errors


    if (errors) {

      const firstError =
        Object.values(errors)
          .flat()
          .find(Boolean)


      showToast(
        firstError ||
          'اطلاعات تحصیلی معتبر نیست.',
        'error'
      )

    } else {

      showToast(
        'ذخیره اطلاعات تحصیلی با خطا مواجه شد.',
        'error'
      )

    }

  } finally {

    isSavingAcademic.value = false

  }
}


// ============================================================
// PASSWORD
// ============================================================

function openPasswordModal() {

  activeTab.value = 'security'

  passwordForm.value = {

    current_password: '',
    new_password: '',
    new_password_confirm: ''

  }

  showEditModal.value = false

  showAcademicModal.value = false

  showPasswordModal.value = true
}


function closePasswordModal() {

  if (isChangingPassword.value) {
    return
  }

  showPasswordModal.value = false
}


async function changePassword() {

  if (isChangingPassword.value) {
    return
  }


  if (
    passwordForm.value.new_password !==
    passwordForm.value.new_password_confirm
  ) {

    showToast(
      'رمز عبور جدید و تکرار آن یکسان نیستند.',
      'error'
    )

    return
  }


  if (
    passwordForm.value.new_password.length < 8
  ) {

    showToast(
      'رمز عبور جدید باید حداقل ۸ کاراکتر باشد.',
      'error'
    )

    return
  }


  isChangingPassword.value = true


  try {

    await api.post(
      '/accounts/change-password/',
      {

        current_password:
          passwordForm.value.current_password,

        new_password:
          passwordForm.value.new_password,

        new_password_confirm:
          passwordForm.value.new_password_confirm

      }
    )


    showPasswordModal.value = false


    passwordForm.value = {

      current_password: '',
      new_password: '',
      new_password_confirm: ''

    }


    showToast(
      'رمز عبور با موفقیت تغییر کرد.'
    )

  } catch (error) {

    console.error(
      'خطا در تغییر رمز عبور:',
      error.response?.data || error
    )


    const errors =
      error.response?.data?.errors


    if (errors) {

      const firstError =
        Object.values(errors)
          .flat()
          .find(Boolean)


      showToast(
        firstError ||
          'تغییر رمز عبور انجام نشد.',
        'error'
      )

    } else {

      showToast(
        'تغییر رمز عبور با خطا مواجه شد.',
        'error'
      )

    }

  } finally {

    isChangingPassword.value = false

  }
}


// ============================================================
// LOGOUT
// ============================================================

function logout() {

  auth.logout()

  router.push({
    name: 'login'
  })
}


// ============================================================
// TOAST
// ============================================================

function showToast(
  message,
  type = 'success'
) {

  toast.value = {

    visible: true,

    message,

    type

  }


  clearTimeout(toastTimer)


  toastTimer =
    setTimeout(() => {

      toast.value.visible = false

    }, 2400)
}


// ============================================================
// DARK MODE
// ============================================================

function detectDarkMode() {

  const root =
    document.documentElement

  const body =
    document.body


  const rootTheme =
    root.getAttribute(
      'data-theme'
    )

  const bodyTheme =
    body.getAttribute(
      'data-theme'
    )


  isDark.value =

    rootTheme === 'dark' ||

    bodyTheme === 'dark' ||

    root.classList.contains(
      'dark'
    ) ||

    body.classList.contains(
      'dark'
    ) ||

    root.classList.contains(
      'dark-mode'
    ) ||

    body.classList.contains(
      'dark-mode'
    )
}


// ============================================================
// ESCAPE KEY
// ============================================================

function handleEscape(event) {

  if (event.key !== 'Escape') {
    return
  }

  if (showEditModal.value) {
    closeEditModal()
    return
  }

  if (showAcademicModal.value) {
    closeAcademicModal()
    return
  }

  if (showPasswordModal.value) {
    closePasswordModal()
  }
}


// ============================================================
// LIFECYCLE
// ============================================================

onMounted(() => {

  detectDarkMode()


  window.addEventListener(
    'keydown',
    handleEscape
  )


  themeObserver =
    new MutationObserver(() => {

      detectDarkMode()

    })


  themeObserver.observe(
    document.documentElement,
    {
      attributes: true,
      attributeFilter: [
        'class',
        'data-theme',
        'style'
      ]
    }
  )


  themeObserver.observe(
    document.body,
    {
      attributes: true,
      attributeFilter: [
        'class',
        'data-theme',
        'style'
      ]
    }
  )

})


onBeforeUnmount(() => {

  themeObserver?.disconnect()

  window.removeEventListener(
    'keydown',
    handleEscape
  )

  clearTimeout(toastTimer)

})

</script>


<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');


/* =========================================================
   BASE
========================================================= */

.profile-page {

  /*
   * مهم:
   * رنگ اصلی این صفحه از سیستم Theme اصلی پروژه می‌آید.
   *
   * اینجا عمداً --primary یا --primary-rgb تعریف نشده است.
   *
   * بنابراین رنگی که کاربر در تنظیمات پروژه انتخاب کرده،
   * مستقیماً روی این صفحه نیز اعمال می‌شود.
   */

  --profile-bg: #f6f8fb;
  --profile-card: #ffffff;
  --profile-soft: #f7f8fa;
  --profile-border: #e7ebf1;
  --profile-text: #172033;
  --profile-muted: #7c8494;

  min-height: 100vh;

  direction: rtl;

  background:
    linear-gradient(
      180deg,
      #f8fafc 0%,
      #f8fafc 72%,
      var(--primary-50) 100%
    );

  color:
    var(--profile-text);

  font-family:
    Vazirmatn,
    IRANSans,
    Tahoma,
    sans-serif;

  transition:
    background .25s ease,
    color .25s ease;
}


/* =========================================================
   DARK MODE
========================================================= */

.profile-page.profile-dark {

  --profile-bg: #0b1120;
  --profile-card: #111827;
  --profile-soft: #172033;
  --profile-border: #263244;
  --profile-text: #f8fafc;
  --profile-muted: #a8b3c4;

  background:
    radial-gradient(
      circle at 8% 0%,
      rgba(
        var(--primary-rgb),
        .08
      ),
      transparent 30%
    ),
    radial-gradient(
      circle at 92% 8%,
      rgba(
        var(--primary-rgb),
        .055
      ),
      transparent 28%
    ),
    linear-gradient(
      180deg,
      #070d18 0%,
      #0b1120 62%,
      #101827 100%
    );

  color:
    var(--profile-text);
}


/* =========================================================
   WRAPPER
========================================================= */

.page-wrapper {

  width:
    min(
      1180px,
      calc(100% - 40px)
    );

  margin:
    0 auto;

  padding:
    42px 0 125px;
}


/* =========================================================
   HEADER
========================================================= */

.profile-header {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    24px;

  margin-bottom:
    24px;
}


.profile-header-content {
  min-width: 0;
}


.header-eyebrow {

  display:
    block;

  margin-bottom:
    7px;

  color:
    var(--primary);

  font-size:
    12px;

  font-weight:
    700;
}


.profile-header h1 {

  margin:
    0;

  color:
    var(--profile-text);

  font-size:
    clamp(
      25px,
      3vw,
      30px
    );

  line-height:
    1.4;

  font-weight:
    800;

  letter-spacing:
    -.3px;
}


.profile-header p {

  margin:
    5px 0 0;

  color:
    var(--profile-muted);

  font-size:
    13px;

  line-height:
    1.8;
}


.header-badge {

  width:
    48px;

  height:
    48px;

  flex:
    0 0 48px;

  display:
    grid;

  place-items:
    center;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .12
    );

  border-radius:
    14px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .09
    );
}


.header-badge svg {

  width:
    23px;

  height:
    23px;
}


/* =========================================================
   PROFILE OVERVIEW
========================================================= */

.profile-overview {

  position:
    relative;

  overflow:
    hidden;

  margin-bottom:
    18px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    22px;

  background:
    var(--profile-card);

  box-shadow:
    0 12px 40px
    rgba(
      15,
      23,
      42,
      .055
    );
}


.profile-dark .profile-overview {

  background:
    radial-gradient(
      circle at 8% 20%,
      rgba(
        var(--primary-rgb),
        .08
      ),
      transparent 32%
    ),
    var(--profile-card);

  box-shadow:
    0 18px 50px
    rgba(
      0,
      0,
      0,
      .20
    );
}


.profile-glow {

  position:
    absolute;

  pointer-events:
    none;

  border-radius:
    999px;

  filter:
    blur(55px);
}


.profile-glow-one {

  width:
    270px;

  height:
    270px;

  top:
    -160px;

  left:
    -90px;

  background:
    rgba(
      var(--primary-rgb),
      .12
    );
}


.profile-glow-two {

  width:
    230px;

  height:
    230px;

  right:
    -120px;

  bottom:
    -150px;

  background:
    rgba(
      var(--primary-rgb),
      .07
    );
}


.profile-overview-content {

  position:
    relative;

  z-index:
    1;

  display:
    flex;

  align-items:
    center;

  gap:
    22px;

  padding:
    25px;
}


/* =========================================================
   AVATAR
========================================================= */

.avatar-wrapper {

  position:
    relative;

  flex-shrink:
    0;
}


.profile-avatar {

  width:
    88px;

  height:
    88px;

  overflow:
    hidden;

  display:
    grid;

  place-items:
    center;

  border:
    3px solid
    var(--profile-card);

  border-radius:
    50%;

  color:
    #ffffff;

  background:
    linear-gradient(
      135deg,
      var(--primary),
      var(--primary-600, var(--primary))
    );

  font-size:
    28px;

  font-weight:
    800;

  box-shadow:
    0 10px 30px
    rgba(
      var(--primary-rgb),
      .22
    );
}


.profile-avatar img {

  width:
    100%;

  height:
    100%;

  display:
    block;

  object-fit:
    cover;
}


.avatar-edit-button {

  position:
    absolute;

  right:
    -3px;

  bottom:
    0;

  width:
    30px;

  height:
    30px;

  display:
    grid;

  place-items:
    center;

  border:
    3px solid
    var(--profile-card);

  border-radius:
    50%;

  color:
    #ffffff;

  background:
    var(--primary);

  cursor:
    pointer;

  box-shadow:
    0 5px 15px
    rgba(
      var(--primary-rgb),
      .22
    );

  transition:
    transform .2s ease,
    box-shadow .2s ease;
}


.avatar-edit-button:hover {

  transform:
    scale(1.08);

  box-shadow:
    0 7px 20px
    rgba(
      var(--primary-rgb),
      .30
    );
}


.avatar-edit-button svg {

  width:
    14px;

  height:
    14px;
}


/* =========================================================
   IDENTITY
========================================================= */

.profile-identity {

  min-width:
    0;

  flex:
    1;
}


.profile-name-row {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;
}


.profile-name-row h2 {

  overflow:
    hidden;

  margin:
    0;

  color:
    var(--profile-text);

  font-size:
    21px;

  font-weight:
    800;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.verified-badge {

  width:
    19px;

  height:
    19px;

  flex:
    0 0 19px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    50%;


  box-shadow:
    0 3px 10px
    rgba(
      34,
      197,
      94,
      .18
    );
}


.verified-badge svg {

  width:
    11px;

  height:
    11px;
}


.profile-username {

  display:
    block;

  margin-top:
    4px;

  direction:
    ltr;

  text-align:
    right;

  color:
    var(--profile-muted);

  font-size:
    12px;
}


.school-badge {

  display:
    inline-flex;

  align-items:
    center;

  margin-top:
    9px;

  padding:
    5px 9px;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .10
    );

  border-radius:
    8px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .08
    );

  font-size:
    11px;

  font-weight:
    700;
}


/* =========================================================
   QUICK STATS
========================================================= */

.profile-quick-stats {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;
}


.quick-stat {

  min-width:
    86px;

  padding:
    11px 12px;

  text-align:
    center;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    13px;

  background:
    var(--profile-soft);

  transition:
    border-color .2s ease,
    transform .2s ease;
}


.quick-stat:hover {

  transform:
    translateY(-1px);

  border-color:
    rgba(
      var(--primary-rgb),
      .25
    );
}


.quick-stat strong {

  display:
    block;

  overflow:
    hidden;

  color:
    var(--profile-text);

  font-size:
    13px;

  font-weight:
    800;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.quick-stat span {

  display:
    block;

  margin-top:
    3px;

  color:
    var(--profile-muted);

  font-size:
    10px;
}


/* =========================================================
   TABS
========================================================= */

.profile-tabs {

  position:
    relative;

  display:
    flex;

  align-items:
    center;

  gap:
    4px;

  margin-bottom:
    18px;

  padding:
    5px;

  overflow-x:
    auto;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    15px;

  background:
    var(--profile-card);

  box-shadow:
    0 5px 22px
    rgba(
      15,
      23,
      42,
      .035
    );

  scrollbar-width:
    none;
}


.profile-tabs::-webkit-scrollbar {
  display:
    none;
}


.profile-tab {

  position:
    relative;

  min-height:
    44px;

  flex:
    1 0 auto;

  display:
    inline-flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    8px;

  padding:
    8px 17px;

  border:
    0;

  border-radius:
    10px;

  color:
    var(--profile-muted);

  background:
    transparent;

  font-family:
    inherit;

  font-size:
    12px;

  font-weight:
    600;

  white-space:
    nowrap;

  cursor:
    pointer;

  transition:
    color .2s ease,
    background .2s ease,
    box-shadow .2s ease;
}


.profile-tab:hover {

  color:
    var(--profile-text);

  background:
    var(--profile-soft);
}


.profile-tab.active {

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .09
    );

  box-shadow:
    inset 0 0 0 1px
    rgba(
      var(--primary-rgb),
      .08
    );
}


.profile-tab.active::after {

  content:
    '';

  position:
    absolute;

  right:
    14px;

  left:
    14px;

  bottom:
    0;

  height:
    2px;

  border-radius:
    99px;

  background:
    var(--primary);
}


.tab-icon {

  width:
    18px;

  height:
    18px;

  display:
    grid;

  place-items:
    center;

  flex:
    0 0 18px;
}


.tab-icon svg {

  width:
    17px;

  height:
    17px;
}


/* =========================================================
   TAB CONTENT
========================================================= */

.profile-tab-content {

  min-height:
    300px;
}


.tab-panel {

  width:
    100%;
}


.tab-enter-active,
.tab-leave-active {

  transition:
    opacity .18s ease,
    transform .18s ease;
}


.tab-enter-from {

  opacity:
    0;

  transform:
    translateY(6px);
}


.tab-leave-to {

  opacity:
    0;

  transform:
    translateY(-4px);
}


/* =========================================================
   GRID
========================================================= */

.overview-grid {

  display:
    grid;

  grid-template-columns:
    repeat(
      2,
      minmax(0, 1fr)
    );

  gap:
    18px;
}


.security-grid {

  display:
    grid;

  grid-template-columns:
    minmax(
      0,
      .95fr
    )
    minmax(
      0,
      1.05fr
    );

  gap:
    18px;
}


/* =========================================================
   CARD
========================================================= */

.profile-card {

  min-width:
    0;

  padding:
    23px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    19px;

  background:
    var(--profile-card);

  box-shadow:
    0 8px 28px
    rgba(
      15,
      23,
      42,
      .035
    );

  transition:
    border-color .2s ease,
    box-shadow .2s ease;
}


.profile-dark .profile-card {

  box-shadow:
    0 12px 35px
    rgba(
      0,
      0,
      0,
      .12
    );
}


.profile-card:hover {

  border-color:
    rgba(
      var(--primary-rgb),
      .15
    );
}


/* =========================================================
   SECTION HEADER
========================================================= */

.section-header {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    15px;

  margin-bottom:
    20px;
}


.section-heading {

  display:
    flex;

  align-items:
    center;

  gap:
    11px;

  min-width:
    0;
}


.section-icon {

  width:
    39px;

  height:
    39px;

  flex:
    0 0 39px;

  display:
    grid;

  place-items:
    center;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .08
    );

  border-radius:
    11px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .08
    );
}


.section-icon svg {

  width:
    19px;

  height:
    19px;
}


.section-heading h3 {

  margin:
    0;

  color:
    var(--profile-text);

  font-size:
    15px;

  font-weight:
    800;
}


.section-heading span {

  display:
    block;

  margin-top:
    3px;

  color:
    var(--profile-muted);

  font-size:
    10px;
}


.edit-button {

  flex-shrink:
    0;

  min-height:
    34px;

  padding:
    0 11px;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .10
    );

  border-radius:
    9px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .08
    );

  font-family:
    inherit;

  font-size:
    11px;

  font-weight:
    700;

  cursor:
    pointer;

  transition:
    background .2s ease,
    transform .2s ease,
    border-color .2s ease;
}


.edit-button:hover {

  background:
    rgba(
      var(--primary-rgb),
      .14
    );

  border-color:
    rgba(
      var(--primary-rgb),
      .18
    );

  transform:
    translateY(-1px);
}


/* =========================================================
   ABOUT
========================================================= */

.bio-content {

  min-height:
    105px;

  padding:
    16px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    13px;

  background:
    var(--profile-soft);
}


.bio-content p {

  margin:
    0;

  color:
    var(--profile-text);

  font-size:
    12px;

  line-height:
    2;
}


.bio-content .empty-text {

  color:
    var(--profile-muted);
}


/* =========================================================
   EMPTY STATE
========================================================= */

.empty-state {

  min-height:
    105px;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  flex-direction:
    column;

  gap:
    4px;

  text-align:
    center;
}


.empty-state-icon {

  width:
    32px;

  height:
    32px;

  display:
    grid;

  place-items:
    center;

  margin-bottom:
    3px;

  border-radius:
    10px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .09
    );
}


.empty-state-icon svg {

  width:
    15px;

  height:
    15px;
}


.empty-state strong {

  color:
    var(--profile-text);

  font-size:
    11px;

  font-weight:
    700;
}


.empty-state > span:last-child {

  color:
    var(--profile-muted);

  font-size:
    10px;
}


/* =========================================================
   SUMMARY
========================================================= */

.summary-list {

  display:
    flex;

  flex-direction:
    column;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    13px;

  overflow:
    hidden;
}


.summary-row {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    15px;

  min-height:
    45px;

  padding:
    8px 13px;

  border-bottom:
    1px solid
    var(--profile-border);
}


.summary-row:last-child {

  border-bottom:
    0;
}


.summary-row > span {

  color:
    var(--profile-muted);

  font-size:
    11px;
}


.summary-row strong {

  max-width:
    60%;

  overflow:
    hidden;

  color:
    var(--profile-text);

  font-size:
    11px;

  font-weight:
    700;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.status-active {

  display:
    inline-flex;

  align-items:
    center;

  gap:
    5px;

  color:
    #10b981 !important;
}


.status-active span {

  width:
    6px;

  height:
    6px;

  border-radius:
    50%;

  background:
    #10b981;

  box-shadow:
    0 0 0 3px
    rgba(
      16,
      185,
      129,
      .10
    );
}


.completion-wrapper {

  margin-top:
    17px;
}


.completion-header {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  margin-bottom:
    7px;

  color:
    var(--profile-muted);

  font-size:
    10px;
}


.completion-header strong {

  color:
    var(--primary);

  font-size:
    11px;
}


.completion-track {

  height:
    7px;

  overflow:
    hidden;

  border-radius:
    99px;

  background:
    var(--profile-soft);

  border:
    1px solid
    var(--profile-border);
}


.completion-value {

  height:
    100%;

  border-radius:
    inherit;

  background:
    var(--primary);

  box-shadow:
    0 0 12px
    rgba(
      var(--primary-rgb),
      .25
    );

  transition:
    width .5s ease;
}


/* =========================================================
   QUICK INFO
========================================================= */

.quick-info-grid {

  display:
    grid;

  grid-template-columns:
    repeat(
      2,
      minmax(0, 1fr)
    );

  gap:
    10px;
}


.quick-info-item {

  min-width:
    0;

  display:
    flex;

  align-items:
    center;

  gap:
    10px;

  padding:
    12px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    12px;

  color:
    var(--profile-text);

  background:
    var(--profile-soft);

  font-family:
    inherit;

  text-align:
    right;

  cursor:
    pointer;

  transition:
    border-color .2s ease,
    transform .2s ease,
    background .2s ease;
}


.quick-info-item:hover {

  transform:
    translateY(-1px);

  border-color:
    rgba(
      var(--primary-rgb),
      .20
    );

  background:
    rgba(
      var(--primary-rgb),
      .045
    );
}


.quick-info-icon {

  width:
    34px;

  height:
    34px;

  flex:
    0 0 34px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    10px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .09
    );
}


.quick-info-icon svg {

  width:
    17px;

  height:
    17px;
}


.quick-info-content {

  min-width:
    0;

  flex:
    1;
}


.quick-info-content small {

  display:
    block;

  color:
    var(--profile-muted);

  font-size:
    9px;
}


.quick-info-content strong {

  display:
    block;

  overflow:
    hidden;

  margin-top:
    3px;

  font-size:
    11px;

  font-weight:
    700;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.quick-info-arrow {

  color:
    var(--profile-muted);

  font-size:
    13px;
}


/* =========================================================
   OVERVIEW ACTIONS
========================================================= */

.overview-action-grid {

  display:
    grid;

  grid-template-columns:
    repeat(
      3,
      minmax(0, 1fr)
    );

  gap:
    9px;
}


.overview-action {

  min-height:
    78px;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  flex-direction:
    column;

  gap:
    8px;

  padding:
    10px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    12px;

  color:
    var(--profile-text);

  background:
    var(--profile-soft);

  font-family:
    inherit;

  font-size:
    10px;

  font-weight:
    700;

  cursor:
    pointer;

  transition:
    transform .2s ease,
    border-color .2s ease,
    background .2s ease;
}


.overview-action:hover {

  transform:
    translateY(-2px);

  border-color:
    rgba(
      var(--primary-rgb),
      .20
    );

  background:
    rgba(
      var(--primary-rgb),
      .05
    );
}


.overview-action-icon {

  width:
    31px;

  height:
    31px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    9px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .09
    );
}


.overview-action-icon svg {

  width:
    16px;

  height:
    16px;
}


/* =========================================================
   PERSONAL BANNER
========================================================= */

.personal-profile-banner {

  display:
    flex;

  align-items:
    center;

  gap:
    13px;

  margin-bottom:
    18px;

  padding:
    15px;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .10
    );

  border-radius:
    14px;

  background:
    linear-gradient(
      135deg,
      rgba(
        var(--primary-rgb),
        .07
      ),
      var(--profile-soft)
    );
}


.personal-banner-avatar {

  width:
    48px;

  height:
    48px;

  flex:
    0 0 48px;

  overflow:
    hidden;

  display:
    grid;

  place-items:
    center;

  border-radius:
    50%;

  color:
    #ffffff;

  background:
    var(--primary);

  font-size:
    16px;

  font-weight:
    800;
}


.personal-banner-avatar img {

  width:
    100%;

  height:
    100%;

  object-fit:
    cover;
}


.personal-banner-content {

  min-width:
    0;

  flex:
    1;
}


.personal-banner-content strong {

  display:
    block;

  overflow:
    hidden;

  color:
    var(--profile-text);

  font-size:
    13px;

  font-weight:
    800;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.personal-banner-content span {

  display:
    block;

  margin-top:
    3px;

  color:
    var(--profile-muted);

  font-size:
    10px;

  direction:
    ltr;

  text-align:
    right;
}


.secondary-outline-button {

  flex-shrink:
    0;

  min-height:
    34px;

  padding:
    0 11px;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .18
    );

  border-radius:
    9px;

  color:
    var(--primary);

  background:
    transparent;

  font-family:
    inherit;

  font-size:
    10px;

  font-weight:
    700;

  cursor:
    pointer;

  transition:
    background .2s ease;
}


.secondary-outline-button:hover {

  background:
    rgba(
      var(--primary-rgb),
      .08
    );
}


/* =========================================================
   INFO
========================================================= */

.info-grid,
.academic-grid {

  display:
    grid;

  grid-template-columns:
    repeat(
      2,
      minmax(0, 1fr)
    );

  gap:
    13px;
}


.info-item {

  min-width:
    0;

  padding:
    14px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    12px;

  background:
    var(--profile-soft);
}


.info-item span {

  display:
    block;

  margin-bottom:
    6px;

  color:
    var(--profile-muted);

  font-size:
    10px;
}


.info-item strong {

  display:
    block;

  overflow:
    hidden;

  color:
    var(--profile-text);

  font-size:
    12px;

  font-weight:
    700;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.profile-card-divider {

  height:
    1px;

  margin:
    20px 0;

  background:
    var(--profile-border);
}


.bio-section-heading {

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    15px;

  margin-bottom:
    10px;
}


.bio-section-heading strong {

  color:
    var(--profile-text);

  font-size:
    12px;

  font-weight:
    800;
}


.bio-section-heading span {

  color:
    var(--profile-muted);

  font-size:
    10px;
}


/* =========================================================
   ACADEMIC
========================================================= */

.academic-highlight {

  display:
    flex;

  align-items:
    center;

  gap:
    13px;

  margin-bottom:
    18px;

  padding:
    15px;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .11
    );

  border-radius:
    14px;

  background:
    linear-gradient(
      135deg,
      rgba(
        var(--primary-rgb),
        .075
      ),
      var(--profile-soft)
    );
}


.academic-highlight-icon {

  width:
    45px;

  height:
    45px;

  flex:
    0 0 45px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    12px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .10
    );
}


.academic-highlight-icon svg {

  width:
    23px;

  height:
    23px;
}


.academic-highlight-content {

  min-width:
    0;
}


.academic-highlight-content span {

  display:
    block;

  color:
    var(--profile-muted);

  font-size:
    10px;
}


.academic-highlight-content strong {

  display:
    block;

  overflow:
    hidden;

  margin-top:
    3px;

  color:
    var(--profile-text);

  font-size:
    14px;

  font-weight:
    800;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


.academic-highlight-content small {

  display:
    block;

  margin-top:
    3px;

  overflow:
    hidden;

  color:
    var(--profile-muted);

  font-size:
    10px;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;
}


/* =========================================================
   SECURITY
========================================================= */

.security-intro-card {

  display:
    flex;

  align-items:
    center;

  gap:
    20px;
}


.security-visual {

  width:
    105px;

  height:
    105px;

  flex:
    0 0 105px;

  display:
    grid;

  place-items:
    center;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .10
    );

  border-radius:
    22px;

  background:
    radial-gradient(
      circle,
      rgba(
        var(--primary-rgb),
        .13
      ),
      rgba(
        var(--primary-rgb),
        .035
      )
    );
}


.security-visual-icon {

  width:
    55px;

  height:
    55px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    17px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .10
    );

  box-shadow:
    0 10px 30px
    rgba(
      var(--primary-rgb),
      .12
    );
}


.security-visual-icon svg {

  width:
    27px;

  height:
    27px;
}


.security-intro-content {

  min-width:
    0;

  flex:
    1;
}


.security-label {

  display:
    block;

  color:
    var(--primary);

  font-size:
    10px;

  font-weight:
    800;
}


.security-intro-content h3 {

  margin:
    5px 0 5px;

  color:
    var(--profile-text);

  font-size:
    17px;

  font-weight:
    800;
}


.security-intro-content p {

  margin:
    0 0 14px;

  color:
    var(--profile-muted);

  font-size:
    11px;

  line-height:
    1.9;
}


.primary-button {

  min-height:
    38px;

  padding:
    0 14px;

  border:
    0;

  border-radius:
    10px;

  color:
    #ffffff;

  background:
    var(--primary);

  box-shadow:
    0 7px 20px
    rgba(
      var(--primary-rgb),
      .18
    );

  font-family:
    inherit;

  font-size:
    11px;

  font-weight:
    700;

  cursor:
    pointer;

  transition:
    transform .2s ease,
    box-shadow .2s ease;
}


.primary-button:hover {

  transform:
    translateY(-1px);

  box-shadow:
    0 10px 25px
    rgba(
      var(--primary-rgb),
      .25
    );
}


/* =========================================================
   ACTIONS
========================================================= */

.actions-card {

  min-width:
    0;
}


.actions-list {

  display:
    flex;

  flex-direction:
    column;

  gap:
    5px;
}


.action-item {

  width:
    100%;

  display:
    flex;

  align-items:
    center;

  gap:
    12px;

  padding:
    12px;

  border:
    0;

  border-radius:
    13px;

  color:
    inherit;

  background:
    transparent;

  font-family:
    inherit;

  text-align:
    right;

  cursor:
    pointer;

  transition:
    background .2s ease,
    transform .2s ease;
}


.action-item:hover {

  background:
    var(--profile-soft);

  transform:
    translateX(-2px);
}


.action-icon {

  width:
    40px;

  height:
    40px;

  flex:
    0 0 40px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    11px;

  color:
    var(--primary);

  background:
    rgba(
      var(--primary-rgb),
      .08
    );
}


.action-icon svg {

  width:
    19px;

  height:
    19px;
}


.action-content {

  min-width:
    0;

  flex:
    1;
}


.action-content strong {

  display:
    block;

  color:
    var(--profile-text);

  font-size:
    12px;

  font-weight:
    800;
}


.action-content small {

  display:
    block;

  margin-top:
    3px;

  color:
    var(--profile-muted);

  font-size:
    10px;
}


.action-arrow {

  color:
    var(--profile-muted);
}


.action-arrow svg {

  width:
    17px;

  height:
    17px;
}


.action-danger .action-icon {

  color:
    #ef4444;

  background:
    rgba(
      239,
      68,
      68,
      .08
    );
}


.action-danger .action-content strong {

  color:
    #ef4444;
}


/* =========================================================
   MODAL
========================================================= */

.modal-backdrop {

  position:
    fixed;

  inset:
    0;

  z-index:
    1000;

  display:
    grid;

  place-items:
    center;

  padding:
    20px;

  background:
    rgba(
      10,
      14,
      22,
      .55
    );

  backdrop-filter:
    blur(8px);
}


.edit-modal {

  width:
    min(
      560px,
      100%
    );

  max-height:
    calc(
      100vh - 40px
    );

  overflow-y:
    auto;

  padding:
    24px;

  border:
    1px solid
    var(--profile-border);

  border-radius:
    21px;

  background:
    var(--profile-card);

  color:
    var(--profile-text);

  box-shadow:
    0 24px 80px
    rgba(
      0,
      0,
      0,
      .22
    );
}


.profile-page.profile-dark .edit-modal {

  box-shadow:
    0 25px 90px
    rgba(
      0,
      0,
      0,
      .45
    );
}


.modal-header {

  display:
    flex;

  align-items:
    flex-start;

  justify-content:
    space-between;

  gap:
    20px;

  margin-bottom:
    24px;
}


.modal-eyebrow {

  display:
    block;

  margin-bottom:
    6px;

  color:
    var(--primary);

  font-size:
    10px;

  font-weight:
    800;
}


.modal-header h2 {

  margin:
    0;

  color:
    var(--profile-text);

  font-size:
    19px;

  font-weight:
    800;
}


.modal-header p {

  margin:
    6px 0 0;

  color:
    var(--profile-muted);

  font-size:
    11px;

  line-height:
    1.8;
}


.modal-close {

  width:
    35px;

  height:
    35px;

  flex:
    0 0 35px;

  display:
    grid;

  place-items:
    center;

  border:
    0;

  border-radius:
    10px;

  color:
    var(--profile-muted);

  background:
    var(--profile-soft);

  cursor:
    pointer;

  transition:
    color .2s ease,
    background .2s ease;
}


.modal-close:hover {

  color:
    var(--profile-text);

  background:
    rgba(
      var(--primary-rgb),
      .09
    );
}


.modal-close svg {

  width:
    17px;

  height:
    17px;
}


/* =========================================================
   FORM
========================================================= */

.edit-form {

  display:
    flex;

  flex-direction:
    column;

  gap:
    20px;
}


.form-grid {

  display:
    grid;

  grid-template-columns:
    repeat(
      2,
      minmax(0, 1fr)
    );

  gap:
    15px;
}


.form-field {

  display:
    flex;

  flex-direction:
    column;

  gap:
    6px;
}


.form-field-full {

  grid-column:
    1 / -1;
}


.form-field > span {

  color:
    var(--profile-text);

  font-size:
    11px;

  font-weight:
    700;
}


.form-field input,
.form-field select,
.form-field textarea {

  width:
    100%;

  box-sizing:
    border-box;

  border:
    1px solid
    var(--profile-border);

  outline:
    none;

  border-radius:
    10px;

  color:
    var(--profile-text);

  background:
    var(--profile-soft);

  font-family:
    inherit;

  font-size:
    12px;

  transition:
    border-color .2s ease,
    box-shadow .2s ease,
    background .2s ease;
}


.form-field input,
.form-field select {

  height:
    43px;

  padding:
    0 12px;
}


.form-field textarea {

  min-height:
    100px;

  padding:
    11px 12px;

  resize:
    vertical;

  line-height:
    1.8;
}


.form-field input::placeholder,
.form-field textarea::placeholder {

  color:
    var(--profile-muted);
}


.form-field input:focus,
.form-field select:focus,
.form-field textarea:focus {

  border-color:
    var(--primary);

  background:
    var(--profile-card);

  box-shadow:
    0 0 0 3px
    rgba(
      var(--primary-rgb),
      .09
    );
}


/* =========================================================
   PASSWORD HINT
========================================================= */

.password-hint {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  padding:
    10px 12px;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .09
    );

  border-radius:
    10px;

  color:
    var(--profile-muted);

  background:
    rgba(
      var(--primary-rgb),
      .045
    );

  font-size:
    10px;
}


.password-hint-icon {

  width:
    20px;

  height:
    20px;

  flex:
    0 0 20px;

  display:
    grid;

  place-items:
    center;

  color:
    var(--primary);
}


.password-hint-icon svg {

  width:
    16px;

  height:
    16px;
}


/* =========================================================
   MODAL BUTTONS
========================================================= */

.modal-actions {

  display:
    flex;

  justify-content:
    flex-start;

  gap:
    9px;
}


.modal-cancel,
.modal-save {

  min-height:
    41px;

  padding:
    0 17px;

  border:
    0;

  border-radius:
    10px;

  font-family:
    inherit;

  font-size:
    11px;

  font-weight:
    700;

  cursor:
    pointer;

  transition:
    opacity .2s ease,
    transform .2s ease;
}


.modal-cancel {

  color:
    var(--profile-text);

  background:
    var(--profile-soft);
}


.modal-save {

  display:
    inline-flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    7px;

  color:
    #ffffff;

  background:
    var(--primary);

  box-shadow:
    0 7px 20px
    rgba(
      var(--primary-rgb),
      .17
    );
}


.modal-cancel:hover:not(:disabled),
.modal-save:hover:not(:disabled) {

  transform:
    translateY(-1px);
}


.modal-cancel:disabled,
.modal-save:disabled {

  opacity:
    .6;

  cursor:
    not-allowed;
}


.button-spinner {

  width:
    14px;

  height:
    14px;

  border:
    2px solid
    rgba(
      255,
      255,
      255,
      .4
    );

  border-top-color:
    #ffffff;

  border-radius:
    50%;

  animation:
    button-spin .7s linear infinite;
}


@keyframes button-spin {

  to {
    transform:
      rotate(360deg);
  }

}


/* =========================================================
   MODAL TRANSITION
========================================================= */

.modal-enter-active,
.modal-leave-active {

  transition:
    opacity .2s ease;
}


.modal-enter-active .edit-modal,
.modal-leave-active .edit-modal {

  transition:
    transform .2s ease,
    opacity .2s ease;
}


.modal-enter-from,
.modal-leave-to {

  opacity:
    0;
}


.modal-enter-from .edit-modal,
.modal-leave-to .edit-modal {

  opacity:
    0;

  transform:
    translateY(12px)
    scale(.98);
}


/* =========================================================
   TOAST
========================================================= */

.toast {

  position:
    fixed;

  left:
    50%;

  bottom:
    30px;

  z-index:
    2000;

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  min-width:
    250px;

  max-width:
    calc(
      100% - 30px
    );

  padding:
    11px 14px;

  transform:
    translateX(-50%);

  border:
    1px solid
    var(--profile-border);

  border-radius:
    12px;

  background:
    var(--profile-card);

  color:
    var(--profile-text);

  box-shadow:
    0 15px 40px
    rgba(
      0,
      0,
      0,
      .17
    );

  font-size:
    11px;

  font-weight:
    700;
}


.toast-icon {

  width:
    22px;

  height:
    22px;

  flex:
    0 0 22px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    50%;

  color:
    #22c55e;

  background:
    rgba(
      34,
      197,
      94,
      .10
    );
}


.toast-icon svg {

  width:
    13px;

  height:
    13px;
}


.toast-error .toast-icon {

  color:
    #ef4444;

  background:
    rgba(
      239,
      68,
      68,
      .10
    );
}


.toast-enter-active,
.toast-leave-active {

  transition:
    opacity .2s ease,
    transform .2s ease;
}


.toast-enter-from,
.toast-leave-to {

  opacity:
    0;

  transform:
    translateX(-50%)
    translateY(10px);
}


/* =========================================================
   FOCUS
========================================================= */

.profile-page :focus-visible {

  outline:
    2px solid
    var(--primary);

  outline-offset:
    2px;
}


/* =========================================================
   RESPONSIVE — 1024
========================================================= */

@media (max-width: 1024px) {

  .profile-overview-content {

    flex-wrap:
      wrap;
  }


  .profile-quick-stats {

    width:
      100%;
  }


  .quick-stat {

    flex:
      1;
  }


  .security-grid {

    grid-template-columns:
      1fr;
  }

}


/* =========================================================
   RESPONSIVE — 760
========================================================= */

@media (max-width: 760px) {

  .page-wrapper {

    width:
      min(
        100% - 24px,
        1180px
      );

    padding:
      28px 0 120px;
  }


  .profile-header {

    margin-bottom:
      20px;
  }


  .profile-header h1 {

    font-size:
      25px;
  }


  .profile-header p {

    font-size:
      12px;
  }


  .profile-overview-content {

    padding:
      21px;
  }


  .overview-grid {

    grid-template-columns:
      1fr;
  }


  .security-intro-card {

    align-items:
      flex-start;
  }


  .profile-tabs {

    border-radius:
      13px;
  }


  .profile-tab {

    min-height:
      42px;

    padding:
      8px 13px;
  }


  .profile-tab.active::after {

    right:
      11px;

    left:
      11px;
  }

}


/* =========================================================
   RESPONSIVE — 520
========================================================= */

@media (max-width: 520px) {

  .page-wrapper {

    width:
      calc(
        100% - 20px
      );

    padding-top:
      21px;
  }


  .profile-header {

    align-items:
      flex-start;

    gap:
      12px;
  }


  .profile-header h1 {

    font-size:
      22px;
  }


  .header-badge {

    width:
      41px;

    height:
      41px;

    flex-basis:
      41px;

    border-radius:
      12px;
  }


  .profile-overview {

    border-radius:
      19px;
  }


  .profile-overview-content {

    gap:
      15px;

    padding:
      17px;
  }


  .profile-avatar {

    width:
      73px;

    height:
      73px;

    font-size:
      23px;
  }


  .profile-name-row h2 {

    font-size:
      17px;
  }


  .profile-quick-stats {

    display:
      grid;

    grid-template-columns:
      repeat(
        3,
        minmax(0, 1fr)
      );

    gap:
      6px;
  }


  .quick-stat {

    min-width:
      0;

    padding:
      9px 6px;
  }


  .quick-stat strong {

    font-size:
      11px;
  }


  .quick-stat span {

    font-size:
      9px;
  }


  .profile-card {

    padding:
      17px;

    border-radius:
      17px;
  }


  .section-header {

    align-items:
      flex-start;
  }


  .section-heading h3 {

    font-size:
      14px;
  }


  .section-heading span {

    font-size:
      9px;
  }


  .section-icon {

    width:
      36px;

    height:
      36px;

    flex-basis:
      36px;
  }


  .edit-button {

    min-height:
      32px;

    padding:
      0 9px;

    font-size:
      10px;
  }


  .quick-info-grid {

    grid-template-columns:
      1fr;
  }


  .overview-action-grid {

    grid-template-columns:
      1fr;
  }


  .info-grid,
  .academic-grid {

    grid-template-columns:
      1fr;
  }


  .personal-profile-banner {

    align-items:
      flex-start;

    flex-wrap:
      wrap;
  }


  .personal-banner-content {

    padding-top:
      4px;
  }


  .secondary-outline-button {

    width:
      100%;
  }


  .security-intro-card {

    flex-direction:
      column;

    align-items:
      stretch;
  }


  .security-visual {

    width:
      100%;

    height:
      100px;

    flex:
      0 0 100px;
  }


  .security-intro-content {

    text-align:
      right;
  }


  .primary-button {

    width:
      100%;
  }


  .form-grid {

    grid-template-columns:
      1fr;
  }


  .form-field-full {

    grid-column:
      auto;
  }


  .edit-modal {

    max-height:
      calc(
        100vh - 24px
      );

    padding:
      18px;

    border-radius:
      18px;
  }


  .modal-actions {

    flex-direction:
      column-reverse;
  }


  .modal-cancel,
  .modal-save {

    width:
      100%;
  }


  .toast {

    bottom:
      22px;
  }

}


/* =========================================================
   RESPONSIVE — 380
========================================================= */

@media (max-width: 380px) {

  .page-wrapper {

    width:
      calc(
        100% - 16px
      );
  }


  .profile-tabs {

    padding:
      4px;
  }


  .profile-tab {

    min-height:
      40px;

    padding:
      7px 10px;

    font-size:
      10px;
  }


  .profile-tab .tab-icon {

    display:
      none;
  }


  .profile-overview-content {

    padding:
      15px;
  }


  .profile-card {

    padding:
      14px;
  }


  .profile-name-row h2 {

    font-size:
      16px;
  }


  .profile-quick-stats {

    gap:
      5px;
  }


  .quick-stat {

    padding:
      8px 4px;
  }


  .quick-stat strong {

    font-size:
      10px;
  }


  .quick-stat span {

    font-size:
      8px;
  }


  .summary-row {

    padding:
      8px 10px;
  }

}

</style>