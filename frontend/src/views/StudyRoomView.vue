<template>
  <div class="study-room-page" :class="{ 'is-dark': isDark }">
    <main class="page-wrapper">

      <!-- Header -->
      <header class="room-header justify-between">
        <div class="flex items-center gap-3">
        <button
          class="back-button"
          type="button"
          @click="goBack"
          aria-label="بازگشت"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>

        <div class="room-title-wrapper">
          <div class="room-title-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path d="M17 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle cx="9.5" cy="7" r="4" />
              <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </div>

          <div>
            <h1>
              {{ room.name || 'سالن مطالعه' }}
            </h1>

            <div class="room-meta">
              <span>
                {{ room.member_count ?? 0 }} / {{ room.max_members ?? 0 }} عضو
              </span>

              <span class="meta-dot">•</span>

              <span
                :class="[
                  'room-status',
                  room.is_active ? 'active' : 'inactive'
                ]"
              >
                <span class="status-dot"></span>
                {{ room.is_active ? 'فعال' : 'غیرفعال' }}
              </span>
            </div>
          </div>
        </div>
        </div>
        <button
  class="leave-room-button"
  type="button"
  :disabled="leavingRoom"
  @click="leaveRoom"
  aria-label="خروج از سالن"
>
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
  >
    <path d="M10 17l5-5-5-5" />
    <path d="M15 12H3" />
    <path d="M21 19V5a2 2 0 0 0-2-2h-6" />
  </svg>

  <span>
    {{ leavingRoom ? 'در حال خروج...' : 'خروج از سالن' }}
  </span>
</button>

      </header>

      <!-- Loading -->
      <div
        v-if="loading"
        class="state-card"
      >
        <div class="loader"></div>

        <p>
          در حال دریافت اطلاعات سالن...
        </p>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="state-card error-card"
      >
        <div class="state-icon error-icon">
          !
        </div>

        <h2>
          خطا در دریافت سالن
        </h2>

        <p>
          {{ error }}
        </p>

        <button
          type="button"
          class="primary-button"
          @click="loadRoom"
        >
          تلاش دوباره
        </button>
      </div>

      <!-- Room -->
      <template v-else-if="room.id">

        <!-- Overview -->
        <section class="overview-card">
          <div class="overview-content">

            <div class="status-badge">
              <span class="status-dot"></span>
              سالن مطالعه
            </div>

            <h2>
              {{ room.name }}
            </h2>

            <p>
              {{ room.description || 'برای شروع مطالعه آماده‌ای؟' }}
            </p>

            <div class="overview-info">

              <div class="info-item">
                <div class="info-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                  >
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                    <circle cx="9" cy="7" r="4" />
                    <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                  </svg>
                </div>

                <div>
                  <span>اعضای سالن</span>
                  <strong>
                    {{ room.member_count ?? 0 }}
                  </strong>
                </div>
              </div>

              <div class="info-item">
                <div class="info-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                  >
                    <path d="M12 6v6l4 2" />
                    <circle cx="12" cy="12" r="9" />
                  </svg>
                </div>

                <div>
                  <span>ظرفیت</span>
                  <strong>
                    {{ room.max_members ?? 0 }}
                  </strong>
                </div>
              </div>

              <div class="info-item">
                <div class="info-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                  >
                    <path d="M12 2l3 7h7l-5.5 4.2 2 7-6.5-4.1L5.5 20l2-6.8L2 9h7z" />
                  </svg>
                </div>

                <div>
                  <span>نوع سالن</span>
                  <strong>
                    {{ room.is_private ? 'خصوصی' : 'عمومی' }}
                  </strong>
                </div>
              </div>

            </div>
          </div>
        </section>

        <!-- Room Navigation -->
        <nav class="room-tabs" aria-label="بخش‌های سالن مطالعه">
          <button
            type="button"
            class="room-tab"
            :class="{ active: activeRoomTab === 'study' }"
            :aria-selected="activeRoomTab === 'study'"
            @click="activeRoomTab = 'study'"
          >
            <span class="room-tab-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v19H6.5A2.5 2.5 0 0 1 4 18.5v-14A2.5 2.5 0 0 1 6.5 2Z"/>
                <path d="M8 6h8M8 10h6"/>
              </svg>
            </span>
            <span>اتاق مطالعه</span>
          </button>

          <button
            type="button"
            class="room-tab"
            :class="{ active: activeRoomTab === 'chat' }"
            :aria-selected="activeRoomTab === 'chat'"
            @click="activeRoomTab = 'chat'"
          >
            <span class="room-tab-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5 8.3 8.3 0 0 1-3.1-.6L4 20l1.6-4.2A7.5 7.5 0 1 1 20 11.5Z"/>
                <path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01"/>
              </svg>
            </span>
            <span>گفت‌وگو</span>
            <span class="room-tab-live" aria-hidden="true"></span>
          </button>

          <button
            type="button"
            class="room-tab"
            :class="{ active: activeRoomTab === 'ranking' }"
            :aria-selected="activeRoomTab === 'ranking'"
            @click="activeRoomTab = 'ranking'"
          >
            <span class="room-tab-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 19h16"/>
                <path d="M7 16V8M12 16V5M17 16v-4"/>
              </svg>
            </span>
            <span>رتبه‌بندی</span>
          </button>
        </nav>

        <div class="room-tab-panels">
        <!-- My Study -->
        <section v-show="activeRoomTab === 'study'" class="study-card">

          <div class="section-heading">
            <div>
              <span class="section-eyebrow">
                مطالعه من
              </span>

              <h2>
                وضعیت مطالعه
              </h2>
            </div>

            <div
              :class="[
                'connection-badge',
                socketConnected ? 'connected' : 'disconnected'
              ]"
            >
              <span></span>
              {{ socketConnected ? 'آنلاین' : 'آفلاین' }}
            </div>
          </div>
<!-- Overview -->



<!-- Study Status -->
          <!-- Hidden analysis video: receives the same MediaStream used by RoomCameras. -->
          <video
            ref="videoElement"
            class="face-analysis-video"
            autoplay
            muted
            playsinline
            aria-hidden="true"
          ></video>

          <!-- Study Status -->
          <div class="study-status-area mb-6">

            <div
              :class="[
                'study-status-circle',
                studyState
              ]"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
              >
                <path d="M9 18h6" />
                <path d="M10 22h4" />
                <path d="M12 2a7 7 0 0 0-4 12.74V17h8v-2.26A7 7 0 0 0 12 2Z" />
              </svg>
            </div>

            <div class="study-status-text">
              <h3>
                {{ studyStateLabel }}
              </h3>

              <p>
                {{ studyStateDescription }}
              </p>
            </div>

          </div>
<RoomCameras
  ref="roomCamerasRef"
  v-if="roomId"
  :room-id="roomId"
  @camera-stream="handleRoomCameraStream"
  @camera-state="handleRoomCameraState"
  @socket-state="handleSocketState"
  @ranking-update="handleRankingUpdate"
/>
          <!-- Actions -->
          <div class="study-actions">

            <button
              type="button"
              class="primary-button start-button"
              :disabled="!room.is_active || startingStudy"
              @click="startStudy"
            >
              <span
                v-if="startingStudy"
                class="button-loader"
              ></span>

              <svg
                v-else
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M8 5v14l11-7z" />
              </svg>

              {{
                startingStudy
                  ? 'در حال آماده‌سازی...'
                  : 'شروع مطالعه'
              }}
            </button>

            <button
              v-if="activeSession"
              type="button"
              class="secondary-button"
              :disabled="stoppingStudy"
              @click="stopStudy"
            >
              {{
                stoppingStudy
                  ? 'در حال توقف...'
                  : 'توقف مطالعه'
              }}
            </button>

          </div>

          <div
            v-if="activeSession"
            class="active-session"
          >
            <span class="live-dot"></span>
            جلسه مطالعه فعال است
          </div>

        </section>

        <!-- ========================= -->
        <!-- Room Chat -->
        <!-- ========================= -->
        <section v-show="activeRoomTab === 'chat'" class="room-chat-section">
          <div class="room-chat-section-header">
            <div class="room-chat-section-title">
              <div class="room-chat-section-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5 8.3 8.3 0 0 1-3.1-.6L4 20l1.6-4.2A7.5 7.5 0 1 1 20 11.5Z"/>
                  <path d="M8 11.5h.01M12 11.5h.01M16 11.5h.01"/>
                </svg>
              </div>
              <div>
                <span class="section-eyebrow">ارتباط اعضای سالن</span>
                <h2>گفت‌وگوی سالن</h2>
                <p>برای هماهنگی، انگیزه دادن و ارتباط سریع با اعضای سالن</p>
              </div>
            </div>

            <div class="room-chat-badge">
              <span class="room-chat-badge-dot"></span>
              چت زنده
            </div>
          </div>

          <div class="room-chat-host">
            <StudyRoomChat
              v-if="roomId"
              :room-id="roomId"
            />
          </div>
        </section>

        <!-- ========================= -->
        <!-- Ranking -->
        <!-- ========================= -->

        <section v-show="activeRoomTab === 'ranking'" class="ranking-card block">

          <!-- Ranking Header -->
          <div class="ranking-header">

            <div class="ranking-title-area">
              <div class="ranking-crown">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                >
                  <path d="M3 7l4 4 5-7 5 7 4-4-2 11H5L3 7Z" />
                  <path d="M5 21h14" />
                </svg>
              </div>

              <div>
                <span class="section-eyebrow">
                  سالن
                </span>

                <h2>
                  رتبه‌بندی مطالعه
                </h2>

                <p class="ranking-subtitle">
                  بر اساس مجموع زمان مطالعه اعضا
                </p>
              </div>
            </div>

            <div class="ranking-header-right">

              <div class="live-ranking-indicator">
                <span></span>
                زنده
              </div>

              <span class="ranking-count">
                {{ roomRanking.length }} نفر
              </span>

            </div>

          </div>

          <!-- Ranking Tabs -->
          <div class="ranking-tabs">

            <button
              type="button"
              :class="[
                'ranking-tab',
                rankingPeriod === 'today' ? 'active' : ''
              ]"
              @click="changeRankingPeriod('today')"
            >
              <span>امروز</span>
            </button>

            <button
              type="button"
              :class="[
                'ranking-tab',
                rankingPeriod === 'yesterday' ? 'active' : ''
              ]"
              @click="changeRankingPeriod('yesterday')"
            >
              <span>دیروز</span>
            </button>

            <button
              type="button"
              :class="[
                'ranking-tab',
                rankingPeriod === 'week' ? 'active' : ''
              ]"
              @click="changeRankingPeriod('week')"
            >
              <span>این هفته</span>
            </button>

            <button
              type="button"
              :class="[
                'ranking-tab',
                rankingPeriod === 'all' ? 'active' : ''
              ]"
              @click="changeRankingPeriod('all')"
            >
              <span>کل بازه</span>
            </button>

          </div>

          <!-- Empty -->
          <div
            v-if="roomRanking.length === 0"
            class="empty-ranking"
          >
            <div class="empty-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.7"
              >
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21a8 8 0 0 1 16 0" />
              </svg>
            </div>

            <h3>
              هنوز رتبه‌ای ثبت نشده
            </h3>

            <p>
              با شروع مطالعه اعضا، رتبه‌بندی اینجا نمایش داده می‌شود.
            </p>
          </div>

          <template v-else>

            <!-- ========================= -->
            <!-- Podium -->
            <!-- ========================= -->

            <div
              v-if="rankingTopThree.length"
              class="ranking-podium"
            >

              <!-- Second -->
              <article
                v-if="rankingTopThree[1]"
                class="podium-place second-place"
              >

                <div class="podium-person">

                  <div class="podium-avatar silver-avatar">
                    {{ getInitial(rankingTopThree[1].username) }}
                  </div>

                  <div class="podium-medal silver-medal">
                    ۲
                  </div>

                </div>

                <div class="podium-block silver-block">

                  <div class="podium-position">
                    نفر دوم
                  </div>

                  <div class="podium-name">
                    {{ rankingTopThree[1].username }}
                  </div>

                  <div class="podium-time">
                    {{ formatStudyTimeShort(rankingTopThree[1].study_seconds) }}
                  </div>

                  <div class="podium-time-label">
                    زمان مطالعه
                  </div>

                  <div
                    :class="[
                      'podium-status',
                      rankingTopThree[1].is_studying ? 'studying' : ''
                    ]"
                  >
                    <span></span>

                    {{
                      rankingTopThree[1].is_studying
                        ? 'در حال مطالعه'
                        : 'آماده'
                    }}
                  </div>

                </div>

              </article>

              <!-- First -->
              <article
                v-if="rankingTopThree[0]"
                class="podium-place first-place"
              >

                <div class="podium-person">

                  <div class="winner-crown">
                    <svg
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path d="M3 7l4 4 5-7 5 7 4-4-2 11H5L3 7Z" />
                      <path d="M5 21h14v-2H5v2Z" />
                    </svg>
                  </div>

                  <div class="podium-avatar gold-avatar">
                    {{ getInitial(rankingTopThree[0].username) }}
                  </div>

                  <div class="podium-medal gold-medal">
                    ۱
                  </div>

                </div>

                <div class="podium-block gold-block">

                  <div class="podium-position winner-position">
                    نفر اول
                  </div>

                  <div class="podium-name">
                    {{ rankingTopThree[0].username }}
                  </div>

                  <div class="podium-time">
                    {{ formatStudyTimeShort(rankingTopThree[0].study_seconds) }}
                  </div>

                  <div class="podium-time-label">
                    زمان مطالعه
                  </div>

                  <div
                    :class="[
                      'podium-status',
                      rankingTopThree[0].is_studying ? 'studying' : ''
                    ]"
                  >
                    <span></span>

                    {{
                      rankingTopThree[0].is_studying
                        ? 'در حال مطالعه'
                        : 'آماده'
                    }}
                  </div>

                </div>

              </article>

              <!-- Third -->
              <article
                v-if="rankingTopThree[2]"
                class="podium-place third-place"
              >

                <div class="podium-person">

                  <div class="podium-avatar bronze-avatar">
                    {{ getInitial(rankingTopThree[2].username) }}
                  </div>

                  <div class="podium-medal bronze-medal">
                    ۳
                  </div>

                </div>

                <div class="podium-block bronze-block">

                  <div class="podium-position">
                    نفر سوم
                  </div>

                  <div class="podium-name">
                    {{ rankingTopThree[2].username }}
                  </div>

                  <div class="podium-time">
                    {{ formatStudyTimeShort(rankingTopThree[2].study_seconds) }}
                  </div>

                  <div class="podium-time-label">
                    زمان مطالعه
                  </div>

                  <div
                    :class="[
                      'podium-status',
                      rankingTopThree[2].is_studying ? 'studying' : ''
                    ]"
                  >
                    <span></span>

                    {{
                      rankingTopThree[2].is_studying
                        ? 'در حال مطالعه'
                        : 'آماده'
                    }}
                  </div>

                </div>

              </article>

            </div>

            <!-- ========================= -->
            <!-- Ranking List -->
            <!-- ========================= -->

            <div
              v-if="rankingRest.length"
              class="ranking-list-container"
            >

              <div class="ranking-list-header">
                <span>رتبه</span>
                <span>کاربر</span>
                <span>زمان مطالعه</span>
              </div>

              <div class="ranking-list">

                <div
                  v-for="member in rankingRest"
                  :key="member.user_id"
                  class="ranking-row"
                >

                  <div class="rank-number">
                    {{ member.rank }}
                  </div>

                  <div class="member-avatar">
                    {{ getInitial(member.username) }}
                  </div>

                  <div class="member-info">

                    <strong>
                      {{ member.username }}
                    </strong>

                    <span
                      :class="[
                        'member-state',
                        member.is_studying ? 'studying' : ''
                      ]"
                    >
                      <span></span>

                      {{
                        member.is_studying
                          ? 'در حال مطالعه'
                          : 'آماده'
                      }}
                    </span>

                  </div>

                  <div class="member-time">

                    <strong>
                      {{ formatStudyTimeShort(member.study_seconds) }}
                    </strong>

                    <span>
                      مطالعه
                    </span>

                  </div>

                </div>

              </div>

            </div>

            <!-- ========================= -->
            <!-- Ranking Stats -->
            <!-- ========================= -->

            <div class="ranking-stats">

              <div class="ranking-stat">

                <div class="stat-icon purple-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                  >
                    <path d="M12 6v6l4 2" />
                    <circle cx="12" cy="12" r="9" />
                  </svg>
                </div>

                <div class="stat-content">

                  <span>
                    میانگین مطالعه
                  </span>

                  <strong>
                    {{ formatStudyTimeShort(rankingAverageSeconds) }}
                  </strong>

                </div>

              </div>

              <div class="ranking-stat">

                <div class="stat-icon blue-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                  >
                    <path d="M4 19h16" />
                    <path d="M7 16V8" />
                    <path d="M12 16V5" />
                    <path d="M17 16v-4" />
                  </svg>
                </div>

                <div class="stat-content">

                  <span>
                    کل زمان مطالعه
                  </span>

                  <strong>
                    {{ formatStudyTimeShort(rankingTotalSeconds) }}
                  </strong>

                </div>

              </div>

              <div class="ranking-stat">

                <div class="stat-icon green-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                  >
                    <circle cx="12" cy="12" r="9" />
                    <path d="M8 12l2.5 2.5L16 9" />
                  </svg>
                </div>

                <div class="stat-content">

                  <span>
                    اعضای فعال
                  </span>

                  <strong>
                    {{ rankingActiveCount }}
                  </strong>

                </div>

              </div>

            </div>

          </template>

        </section>
        </div>

      </template>

    </main>
  </div>
</template>

<script setup>
import RoomCameras from '../components/RoomCameras.vue'
import StudyRoomChat from '../components/StudyRoomChat.vue'

import {
  FaceLandmarker,
  FilesetResolver
} from '@mediapipe/tasks-vision'

import {
  computed,
  nextTick,
  onMounted,
  onUnmounted,
  ref,
  shallowRef
} from 'vue'

import {
  useRoute,
  useRouter
} from 'vue-router'

import api from '../services/api'


const route = useRoute()
const router = useRouter()
const roomCamerasRef = ref(null)

const isDark = ref(false)
const activeRoomTab = ref('study')
let themeObserver = null


const room = ref({})
const loading = ref(true)
const error = ref('')

const socketConnected = ref(false)
const roomRanking = ref([])

const rankingPeriod = ref('today')

const activeSession = ref(null)

const startingStudy = ref(false)
const stoppingStudy = ref(false)

const leavingRoom = ref(false)

const studyState = ref('away')
const rawStudyState = ref('away')

let candidateState = 'away'
let candidateStateSince = 0

const FACE_LOST_GRACE_MS = 1800
const HEARTBEAT_INTERVAL_MS = 2000

let faceLostSince = 0
let lastHeartbeatSentAt = 0
let heartbeatSending = false
let latestConfidence = 0

const STATE_STABILITY_MS = 1500


const videoElement = ref(null)
const cameraStream = ref(null)

const faceLandmarker = shallowRef(null)
const faceDetectionRunning = ref(false)

let faceDetectionFrame = null
let lastVideoTime = -1



const roomId = computed(() => route.params.roomId)


/*
 * =========================
 * Ranking Computed
 * =========================
 */

const rankingTopThree = computed(() => {
  return roomRanking.value.slice(0, 3)
})


const rankingRest = computed(() => {
  return roomRanking.value.slice(3)
})


const rankingTotalSeconds = computed(() => {
  return roomRanking.value.reduce(
    (total, member) => {
      return total + (
        Number(member.study_seconds) || 0
      )
    },
    0
  )
})


const rankingAverageSeconds = computed(() => {
  if (!roomRanking.value.length) {
    return 0
  }

  return Math.floor(
    rankingTotalSeconds.value /
    roomRanking.value.length
  )
})


const rankingActiveCount = computed(() => {
  return roomRanking.value.filter(
    member => member.is_studying
  ).length
})


/*
 * =========================
 * Study State
 * =========================
 */

const studyStateLabel = computed(() => {
  if (studyState.value === 'focused') {
    return 'متمرکز'
  }

  if (studyState.value === 'distracted') {
    return 'حواس‌پرت'
  }

  return 'از جلوی دوربین خارج شده'
})


const studyStateDescription = computed(() => {
  if (studyState.value === 'focused') {
    return 'وضعیت شما با دوربین در حال بررسی است.'
  }

  if (studyState.value === 'distracted') {
    return 'وضعیت فعلی برای ثبت زمان مطالعه مناسب نیست.'
  }

  return 'چهره‌ای از شما در دوربین شناسایی نمی‌شود.'
})


function handleRoomCameraStream(stream) {
  cameraStream.value = stream

  if (!stream) {
    stopFaceDetection()
    return
  }

  nextTick(async () => {
    if (!videoElement.value) {
      return
    }

    videoElement.value.srcObject = stream
    videoElement.value.muted = true
    videoElement.value.autoplay = true
    videoElement.value.playsInline = true

    try {
      await videoElement.value.play()
    } catch {
      // ignore autoplay restrictions
    }

    await initializeFaceLandmarker()

    if (faceLandmarker.value) {
      faceDetectionRunning.value = true
      lastVideoTime = -1

      if (!faceDetectionFrame) {
        detectFace()
      }
    }
  })
}

function handleRoomCameraState(isOn) {
  if (!isOn) {
    stopFaceDetection()
  }
}

async function leaveRoom() {
  if (leavingRoom.value || !roomId.value) {
    return
  }

  const confirmed = window.confirm(
    'آیا مطمئن هستید که می‌خواهید از این سالن خارج شوید؟'
  )

  if (!confirmed) {
    return
  }

  leavingRoom.value = true

  try {
    stopFaceDetection()

    if (roomCamerasRef.value) {
      await roomCamerasRef.value.stopCamera()
    }

    await api.post(
      `/rooms/${roomId.value}/leave/`
    )

    activeSession.value = null
    studyState.value = 'away'
    rawStudyState.value = 'away'
    latestConfidence = 0
    lastHeartbeatSentAt = 0
    faceLostSince = 0
    heartbeatSending = false

    router.push({
      name: 'rooms'
    })
  } catch (err) {
    console.error(
      'خطا در خروج از سالن:',
      err
    )

    const message =
      err.response?.data?.detail ||
      'خروج از سالن انجام نشد.'

    alert(message)
  } finally {
    leavingRoom.value = false
  }
}

function handleSocketState(connected) {
  socketConnected.value = connected
}

function handleRankingUpdate(data) {
  roomRanking.value = data?.ranking || []

  if (data?.period) {
    rankingPeriod.value = data.period
  }
}

function changeRankingPeriod(period) {
  roomCamerasRef.value?.changeRankingPeriod(period)
}

function stopFaceDetection() {
  if (faceDetectionFrame) {
    cancelAnimationFrame(faceDetectionFrame)
    faceDetectionFrame = null
  }

  faceDetectionRunning.value = false
  lastVideoTime = -1
}

/*
 * =========================
 * Load Room
 * =========================
 */

async function loadRoom() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get(
      `/rooms/${roomId.value}/`
    )

    console.log(
      'ROOM API RESPONSE:',
      response.data
    )

    room.value = response.data

    activeSession.value =
      response.data.active_session || null

    if (activeSession.value) {
      studyState.value =
        activeSession.value.current_state || 'away'

      rawStudyState.value =
        activeSession.value.current_state || 'away'

      candidateState =
        activeSession.value.current_state || 'away'

      candidateStateSince =
        performance.now()
    } else {
      studyState.value = 'away'
      rawStudyState.value = 'away'
      candidateState = 'away'
      candidateStateSince =
        performance.now()
    }

  } catch (err) {
    console.error(
      'خطا در دریافت سالن:',
      err
    )

    error.value =
      err.response?.data?.detail ||
      'اطلاعات سالن دریافت نشد.'

  } finally {
    loading.value = false
  }
}



/*
 * =========================
 * MediaPipe
 * =========================
 */

async function initializeFaceLandmarker() {

  if (faceLandmarker.value) {
    return
  }

  try {

    const vision =
      await FilesetResolver.forVisionTasks(
        '/mediapipe/wasm'
      )

    faceLandmarker.value =
      await FaceLandmarker.createFromOptions(
        vision,
        {
          baseOptions: {
            modelAssetPath:
              '/mediapipe/face_landmarker.task'
          },

          runningMode: 'VIDEO',

          numFaces: 1,

          outputFaceBlendshapes: true,

          minFaceDetectionConfidence: 0.5,
          minFacePresenceConfidence: 0.5,
          minTrackingConfidence: 0.5
        }
      )

    console.log(
      'MediaPipe Face Landmarker آماده شد.'
    )

  } catch (err) {

    console.error(
      'خطا در راه‌اندازی MediaPipe:',
      err
    )

    console.error(
      'ERROR OBJECT:',
      err
    )

    faceLandmarker.value = null
  }
}


/*
 * =========================
 * Stable State
 * =========================
 */

function updateStableStudyState(nextState) {

  const now =
    performance.now()

  if (nextState !== candidateState) {

    candidateState =
      nextState

    candidateStateSince =
      now

    console.log(
      'وضعیت پیشنهادی جدید:',
      nextState
    )

    return
  }

  const stableDuration =
    now - candidateStateSince

  if (
    stableDuration >=
    STATE_STABILITY_MS
  ) {

    if (
      studyState.value !==
      candidateState
    ) {

      studyState.value =
        candidateState

      console.log(
        'وضعیت پایدار شد:',
        candidateState
      )
    }
  }
}


/*
 * =========================
 * Analyze Face
 * =========================
 */

function analyzeFaceResult(result) {

  const landmarks =
    result?.faceLandmarks?.[0]

  if (!landmarks) {
    return {
      state: 'away',
      confidence: 0
    }
  }


  const leftEyeOuter =
    landmarks[33]

  const leftEyeInner =
    landmarks[133]

  const rightEyeInner =
    landmarks[362]

  const rightEyeOuter =
    landmarks[263]

  const nose =
    landmarks[1]


  if (
    !leftEyeOuter ||
    !leftEyeInner ||
    !rightEyeInner ||
    !rightEyeOuter ||
    !nose
  ) {

    return {
      state: 'distracted',
      confidence: 0.3
    }
  }


  const leftEyeCenterX =
    (
      leftEyeOuter.x +
      leftEyeInner.x
    ) / 2


  const rightEyeCenterX =
    (
      rightEyeInner.x +
      rightEyeOuter.x
    ) / 2


  const eyeCenterX =
    (
      leftEyeCenterX +
      rightEyeCenterX
    ) / 2


  const eyeDistance =
    Math.abs(
      rightEyeCenterX -
      leftEyeCenterX
    )


  if (eyeDistance < 0.01) {

    return {
      state: 'distracted',
      confidence: 0.3
    }
  }


  const headOffset =
    Math.abs(
      nose.x -
      eyeCenterX
    )


  const normalizedOffset =
    headOffset /
    eyeDistance


  if (
    normalizedOffset > 0.75
  ) {

    return {
      state: 'distracted',
      confidence: Math.min(
        1,
        normalizedOffset / 1.5
      )
    }
  }


  return {
    state: 'focused',
    confidence: 0.9
  }
}


/*
 * =========================
 * Face Detection
 * =========================
 */

function detectFace() {

  if (!activeSession.value) {

    rawStudyState.value =
      'away'

    studyState.value =
      'away'

    latestConfidence =
      0

    faceDetectionFrame =
      requestAnimationFrame(
        detectFace
      )

    return
  }


  if (
    !faceLandmarker.value ||
    !videoElement.value ||
    !cameraStream.value
  ) {

    faceDetectionRunning.value =
      false

    return
  }


  if (
    videoElement.value.readyState >= 2 &&
    videoElement.value.currentTime !== lastVideoTime
  ) {

    const currentVideoTime =
      videoElement.value.currentTime

    lastVideoTime =
      currentVideoTime


    try {

      const timestampMs =
        Math.round(
          currentVideoTime * 1000
        )


      const landmarker =
        faceLandmarker.value


      const result =
        landmarker.detectForVideo(
          videoElement.value,
          timestampMs
        )


      const faceCount =
        result?.faceLandmarks?.length || 0


      console.log(
        'تعداد چهره:',
        faceCount
      )


      if (faceCount === 0) {

        rawStudyState.value =
          'away'


        if (!faceLostSince) {

          faceLostSince =
            performance.now()

          console.log(
            'چهره موقتاً گم شد؛ شروع Grace Period'
          )
        }


        const lostDuration =
          performance.now() -
          faceLostSince


        if (
          lostDuration <
          FACE_LOST_GRACE_MS
        ) {

          sendHeartbeat(
            studyState.value,
            latestConfidence
          )

        } else {

          updateStableStudyState(
            'away'
          )

          latestConfidence =
            0

          sendHeartbeat(
            studyState.value,
            0
          )

          console.log(
            'چهره برای مدت کافی دیده نشد → away'
          )
        }

      } else {

        faceLostSince =
          0


        const analysis =
          analyzeFaceResult(
            result
          )


        rawStudyState.value =
          analysis.state

        latestConfidence =
          analysis.confidence


        updateStableStudyState(
          analysis.state
        )


        console.log(
          'وضعیت خام:',
          analysis.state,
          'اعتماد:',
          analysis.confidence
        )


        sendHeartbeat(
          studyState.value,
          latestConfidence
        )
      }

    } catch (err) {

      console.error(
        'خطا در تشخیص چهره:',
        err
      )

      console.error(
        'VIDEO CURRENT TIME:',
        videoElement.value.currentTime
      )

      faceDetectionRunning.value =
        false

      return
    }
  }


  faceDetectionFrame =
    requestAnimationFrame(
      detectFace
    )
}



/*
 * =========================
 * Start Study
 * =========================
 */

async function startStudy() {

  if (
    startingStudy.value ||
    !room.value.id
  ) {
    return
  }


  startingStudy.value =
    true


  try {

    const response =
      await api.post(
        `/rooms/${roomId.value}/start-study/`
      )


    activeSession.value =
      response.data


    studyState.value =
      'away'

    rawStudyState.value =
      'away'

    candidateState =
      'away'

    candidateStateSince =
      performance.now()


    if (roomCamerasRef.value) {
      await roomCamerasRef.value.startCamera()
    }

  } catch (err) {

    console.error(
      'خطا در شروع مطالعه:',
      err
    )


    const message =
      err.response?.data?.detail ||
      'شروع جلسه مطالعه انجام نشد.'


    alert(message)

  } finally {

    startingStudy.value =
      false
  }
}


/*
 * =========================
 * Stop Study
 * =========================
 */

async function stopStudy() {

  stoppingStudy.value =
    true

  try {

    await api.post(
      `/rooms/${roomId.value}/stop-study/`
    )


    activeSession.value =
      null


    rawStudyState.value =
      'away'

    studyState.value =
      'away'

    latestConfidence =
      0

    lastHeartbeatSentAt =
      0

    faceLostSince =
      0

    heartbeatSending =
      false


    if (roomCamerasRef.value) {
      await roomCamerasRef.value.stopCamera()
    }


    console.log(
      'مطالعه متوقف شد و دوربین کاملاً خاموش شد'
    )

  } catch (err) {

    console.error(
      'خطا در توقف مطالعه:',
      err
    )

  } finally {

    stoppingStudy.value =
      false
  }
}


/*
 * =========================
 * Heartbeat
 * =========================
 */

async function sendHeartbeat(
  state,
  confidence
) {

  if (
    !activeSession.value ||
    heartbeatSending
  ) {
    return
  }


  const now =
    performance.now()


  if (
    now - lastHeartbeatSentAt <
    HEARTBEAT_INTERVAL_MS
  ) {
    return
  }


  heartbeatSending =
    true


  try {

    const response =
      await api.post(
        `/rooms/${roomId.value}/heartbeat/`,
        {
          state,
          confidence
        }
      )


    lastHeartbeatSentAt =
      now


    console.log(
      'Heartbeat خودکار:',
      response.data
    )

  } catch (err) {

    console.error(
      'خطا در ارسال Heartbeat خودکار:',
      err
    )

  } finally {

    heartbeatSending =
      false
  }
}


/*
 * =========================
 * Format Full Time
 * =========================
 */

function formatStudyTimeShort(seconds) {
  const totalSeconds = Math.max(0, Number(seconds) || 0)

  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const secs = totalSeconds % 60

  return [
    String(hours).padStart(2, '0'),
    String(minutes).padStart(2, '0'),
    String(secs).padStart(2, '0')
  ].join(':')
}


/*
 * =========================
 * Format Ranking Time
 * =========================
 */




/*
 * =========================
 * Theme
 * =========================
 */

function detectDarkTheme() {
  const root = document.documentElement
  const body = document.body

  const dataTheme =
    root.getAttribute('data-theme') ||
    body?.getAttribute('data-theme')

  if (dataTheme === 'dark') return true
  if (dataTheme === 'light') return false

  return (
    root.classList.contains('dark') ||
    body?.classList.contains('dark') ||
    root.classList.contains('dark-mode') ||
    body?.classList.contains('dark-mode')
  )
}

function initThemeWatcher() {
  isDark.value = detectDarkTheme()

  themeObserver = new MutationObserver(() => {
    isDark.value = detectDarkTheme()
  })

  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style']
  })

  if (document.body) {
    themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'data-theme', 'style']
    })
  }
}


/*
 * =========================
 * Initial
 * =========================
 */

function getInitial(username) {

  if (!username) {
    return '?'
  }

  return String(username)
    .trim()
    .charAt(0)
    .toUpperCase()
}


/*
 * =========================
 * Back
 * =========================
 */

async function goBack() {

  stopFaceDetection()

  if (roomCamerasRef.value) {
    await roomCamerasRef.value.stopCamera()
  }

  router.push({
    name: 'rooms'
  })
}


/*
 * =========================
 * Mount
 * =========================
 */

onMounted(async () => {

  initThemeWatcher()

  await loadRoom()

  if (room.value.id && activeSession.value) {
    await nextTick()

    if (roomCamerasRef.value) {
      await roomCamerasRef.value.startCamera()
    }
  }
})


/*
 * =========================
 * Unmount
 * =========================
 */

onUnmounted(() => {
  stopFaceDetection()

  themeObserver?.disconnect()
  themeObserver = null
})
</script>

<style scoped>

.study-room-page {
  min-height: 100vh;

  background:
    linear-gradient(
      180deg,
      var(--app-bg) 0%,
      var(--app-bg) 72%,
      var(--primary-50) 100%
    );
}


.page-wrapper {
  width: min(1100px, 100%);
  margin: 0 auto;
  padding: 28px 20px 120px;
}


/* =========================
   Header
   ========================= */

.room-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}


.back-button {
  width: 44px;
  height: 44px;
  flex-shrink: 0;

  border: 1px solid var(--border);
  border-radius: 13px;

  background: white;
  color: var(--text-main);

  display: grid;
  place-items: center;

  cursor: pointer;

  transition:
    transform .2s ease,
    border-color .2s ease,
    background .2s ease;
}


.back-button:hover {
  transform: translateY(-1px);
  border-color: var(--primary-200);
  background: var(--primary-50);
}


.back-button svg {
  width: 21px;
  height: 21px;
}


.room-title-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}


.room-title-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;

  border-radius: 15px;

  background: var(--primary-100);
  color: var(--primary);

  display: grid;
  place-items: center;
}


.room-title-icon svg {
  width: 25px;
  height: 25px;
}


.room-title-wrapper h1 {
  margin: 0 0 5px;

  font-size: 21px;
  font-weight: 800;

  color: var(--text-main);
}


.room-meta {
  display: flex;
  align-items: center;
  gap: 7px;

  color: var(--text-muted);
  font-size: 12px;
}


.meta-dot {
  color: #cbd5e1;
}


.room-status {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}


.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;

  background: #94a3b8;
}


.room-status.active .status-dot {
  background: #10b981;
}


.room-status.inactive .status-dot {
  background: #ef4444;
}


/* =========================
   Overview
   ========================= */

.overview-card {
  position: relative;
  overflow: hidden;

  margin-bottom: 18px;
  padding: 30px;

  border-radius: 24px;

  color: white;

  background:
    radial-gradient(
      circle at 8% 10%,
      rgba(var(--primary-rgb), .32),
      transparent 32%
    ),

    radial-gradient(
      circle at 90% 90%,
      rgba(79, 70, 229, .28),
      transparent 30%
    ),

    #0f172a;

  box-shadow:
    0 18px 45px rgba(15, 23, 42, .12);
}


.overview-content {
  position: relative;
  z-index: 1;
  max-width: 760px;
}


.status-badge {
  width: fit-content;

  display: inline-flex;
  align-items: center;
  gap: 7px;

  padding: 7px 11px;

  border-radius: 999px;

  color: #d1fae5;

  background: rgba(16, 185, 129, .12);

  border: 1px solid rgba(16, 185, 129, .18);

  font-size: 11px;
  font-weight: 700;
}


.status-badge .status-dot {
  background: #34d399;
}


.overview-card h2 {
  margin: 18px 0 8px;

  font-size: clamp(25px, 4vw, 34px);
  line-height: 1.35;

  font-weight: 850;
}


.overview-card p {
  margin: 0;
  max-width: 650px;

  color: #cbd5e1;

  font-size: 14px;
  line-height: 2;
}


.overview-info {
  display: flex;
  flex-wrap: wrap;
  gap: 22px;

  margin-top: 25px;
}


.info-item {
  display: flex;
  align-items: center;
  gap: 9px;
}


.info-icon {
  width: 37px;
  height: 37px;

  border-radius: 11px;

  background: rgba(255, 255, 255, .08);

  display: grid;
  place-items: center;
}


.info-icon svg {
  width: 19px;
  height: 19px;
}


.info-item div:last-child {
  display: flex;
  flex-direction: column;
  gap: 2px;
}


.info-item span {
  color: #94a3b8;
  font-size: 10px;
}


.info-item strong {
  font-size: 13px;
}


/* =========================
   General Cards
   ========================= */

.study-card,
.ranking-card {
  background: white;

  border: 1px solid var(--border);
  border-radius: 20px;

  padding: 24px;
  margin-bottom: 18px;

  box-shadow:
    0 1px 2px rgba(15, 23, 42, .03),
    0 8px 30px rgba(15, 23, 42, .04);
}


.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 15px;
  margin-bottom: 24px;
}


.section-eyebrow {
  display: block;

  margin-bottom: 4px;

  color: var(--primary);

  font-size: 11px;
  font-weight: 800;
}


.section-heading h2 {
  margin: 0;

  font-size: 18px;
  font-weight: 800;
}


/* =========================
   Connection
   ========================= */

.connection-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  padding: 7px 10px;

  border-radius: 999px;

  font-size: 11px;
  font-weight: 700;
}


.connection-badge span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}


.connection-badge.connected {
  color: #047857;
  background: #ecfdf5;
}


.connection-badge.connected span {
  background: #10b981;
}


.connection-badge.disconnected {
  color: #64748b;
  background: #f1f5f9;
}


.connection-badge.disconnected span {
  background: #94a3b8;
}


/* =========================
   Camera
   ========================= */

.camera-preview {
  position: relative;

  width: 100%;
  max-width: 520px;

  margin: 0 auto 18px;

  overflow: hidden;

  border-radius: 18px;

  background: #0f172a;

  border: 1px solid var(--border);

  aspect-ratio: 4 / 3;
}


.camera-preview video {
  width: 100%;
  height: 100%;

  display: block;

  object-fit: cover;

  transform: scaleX(-1);
}


.camera-label {
  position: absolute;

  top: 12px;
  right: 12px;

  display: inline-flex;
  align-items: center;
  gap: 6px;

  padding: 7px 10px;

  border-radius: 999px;

  color: white;

  background: rgba(15, 23, 42, .72);

  backdrop-filter: blur(8px);

  font-size: 10px;
  font-weight: 700;
}


.camera-dot {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #10b981;
}


/* =========================
   Study Status
   ========================= */

.study-status-area {
  display: flex;
  align-items: center;
  gap: 17px;

  padding: 20px;

  border-radius: 16px;

  background: #f8fafc;

  border: 1px solid #eef2f7;
}


.study-status-circle {
  width: 62px;
  height: 62px;

  flex-shrink: 0;

  border-radius: 18px;

  display: grid;
  place-items: center;

  color: var(--primary);

  background: var(--primary-100);
}


.study-status-circle svg {
  width: 29px;
  height: 29px;
}


.study-status-circle.distracted {
  color: #d97706;
  background: #fff7ed;
}


.study-status-circle.focused {
  color: #059669;
  background: #ecfdf5;
}


.study-status-text h3 {
  margin: 0 0 4px;

  font-size: 15px;
  font-weight: 800;
}


.study-status-text p {
  margin: 0;

  color: var(--text-muted);

  font-size: 12px;
  line-height: 1.8;
}


/* =========================
   Buttons
   ========================= */
.leave-room-button {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  padding: 0 15px;

  border: 1px solid #fecaca;
  border-radius: 13px;

  background: #fff5f5;
  color: #dc2626;

  font-family: inherit;
  font-size: 12px;
  font-weight: 800;

  cursor: pointer;

  transition:
    transform .2s ease,
    background .2s ease,
    border-color .2s ease,
    opacity .2s ease;
}

.leave-room-button:hover:not(:disabled) {
  transform: translateY(-1px);
  background: #fee2e2;
  border-color: #fca5a5;
}

.leave-room-button:disabled {
  opacity: .55;
  cursor: not-allowed;
}

.leave-room-button svg {
  width: 19px;
  height: 19px;
}

.study-room-page.is-dark .leave-room-button {
  background: rgba(127, 29, 29, .18);
  border-color: rgba(248, 113, 113, .25);
  color: #fca5a5;
}

.study-room-page.is-dark .leave-room-button:hover:not(:disabled) {
  background: rgba(127, 29, 29, .28);
}


.study-actions {
  display: flex;
  gap: 10px;

  margin-top: 16px;
}


.primary-button,
.secondary-button {
  min-height: 44px;

  border-radius: 11px;

  padding: 10px 16px;

  border: 0;

  font-family: inherit;

  font-size: 13px;
  font-weight: 700;

  cursor: pointer;

  transition:
    transform .2s ease,
    background .2s ease,
    opacity .2s ease;
}


.primary-button {
  color: white;
  background: var(--primary);
}


.primary-button:hover:not(:disabled) {
  transform: translateY(-1px);
  background: var(--primary-hover);
}


.primary-button:disabled,
.secondary-button:disabled {
  opacity: .55;
  cursor: not-allowed;
}


.secondary-button {
  color: #334155;

  background: white;

  border: 1px solid #e2e8f0;
}


.secondary-button:hover:not(:disabled) {
  background: #f8fafc;
}


.start-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}


.start-button svg {
  width: 17px;
  height: 17px;
}


.active-session {
  display: flex;
  align-items: center;
  gap: 7px;

  margin-top: 13px;

  color: #047857;

  font-size: 11px;
  font-weight: 700;
}


.live-dot {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #10b981;

  box-shadow:
    0 0 0 4px rgba(16, 185, 129, .10);
}


/* =========================================================
   RANKING
   ========================================================= */

.ranking-card {
  position: relative;
  overflow: hidden;
}


/* =========================
   Ranking Header
   ========================= */

.ranking-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 18px;

  margin-bottom: 22px;
}


.ranking-title-area {
  display: flex;
  align-items: center;
  gap: 13px;
}


.ranking-crown {
  width: 48px;
  height: 48px;

  flex-shrink: 0;

  border-radius: 15px;

  display: grid;
  place-items: center;

  color: #f59e0b;

  background:
    linear-gradient(
      145deg,
      #fff8e7,
      #fff1c7
    );

  border: 1px solid #fde68a;

  box-shadow:
    0 8px 22px rgba(245, 158, 11, .10);
}


.ranking-crown svg {
  width: 25px;
  height: 25px;
}


.ranking-title-area .section-eyebrow {
  margin-bottom: 2px;
}


.ranking-title-area h2 {
  margin: 0;

  font-size: 19px;
  font-weight: 850;

  color: var(--text-main);
}


.ranking-subtitle {
  margin: 3px 0 0;

  color: var(--text-muted);

  font-size: 10px;
}


.ranking-header-right {
  display: flex;
  align-items: center;
  gap: 9px;
}


.ranking-count {
  color: var(--text-muted);

  font-size: 11px;
  font-weight: 700;
}


.live-ranking-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  padding: 6px 9px;

  border-radius: 999px;

  color: #047857;

  background: #ecfdf5;

  border: 1px solid #d1fae5;

  font-size: 10px;
  font-weight: 800;
}


.live-ranking-indicator span {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #10b981;

  box-shadow:
    0 0 0 3px rgba(16, 185, 129, .10);
}


/* =========================
   Ranking Tabs
   ========================= */

.ranking-tabs {
  display: grid;

  grid-template-columns:
    repeat(4, minmax(0, 1fr));

  gap: 6px;

  padding: 5px;

  margin-bottom: 25px;

  border-radius: 14px;

  background: #f8fafc;

  border: 1px solid #eef2f7;
}


.ranking-tab {
  min-height: 39px;

  padding: 7px 10px;

  border: 0;

  border-radius: 10px;

  background: transparent;

  color: #64748b;

  font-family: inherit;

  font-size: 11px;
  font-weight: 750;

  cursor: pointer;

  transition:
    background .2s ease,
    color .2s ease,
    box-shadow .2s ease,
    transform .2s ease;
}


.ranking-tab:hover {
  color: var(--primary);
}


.ranking-tab.active {
  color: var(--primary);

  background: white;

  box-shadow:
    0 3px 10px rgba(15, 23, 42, .07);
}


.ranking-tab:active {
  transform: scale(.98);
}


/* =========================
   Podium
   ========================= */

.ranking-podium {
  position: relative;

  max-width: 850px;

  min-height: 355px;

  margin: 0 auto 25px;

  padding: 60px 20px 0;

  display: flex;

  align-items: flex-end;

  justify-content: center;

  gap: 0;
}


.ranking-podium::before {
  content: "";

  position: absolute;

  left: 10%;
  right: 10%;
  top: 30px;
  bottom: 0;

  pointer-events: none;

  background:
    radial-gradient(
      ellipse at center,
      rgba(var(--primary-rgb), .08),
      transparent 67%
    );
}


.podium-place {
  position: relative;

  z-index: 2;

  width: 33.333%;

  display: flex;

  flex-direction: column;

  align-items: center;
}


.second-place {
  order: 1;
}


.first-place {
  order: 2;
}


.third-place {
  order: 3;
}


.podium-person {
  position: relative;

  z-index: 5;

  margin-bottom: -22px;
}


.podium-avatar {
  width: 88px;
  height: 88px;

  display: grid;
  place-items: center;

  border-radius: 50%;

  font-size: 25px;
  font-weight: 850;

  background:
    linear-gradient(
      145deg,
      #aeb6c5,
      #3d4657
    );

  color: white;

  border: 3px solid #94a3b8;

  box-shadow:
    0 0 0 6px rgba(148, 163, 184, .08),
    0 15px 35px rgba(15, 23, 42, .22);
}


.silver-avatar {
  border-color: #cbd5e1;

  background:
    linear-gradient(
      145deg,
      #cbd5e1,
      #64748b
    );
}


.gold-avatar {
  width: 106px;
  height: 106px;

  border-color: #f7b938;

  background:
    linear-gradient(
      145deg,
      #e9c46a,
      #8b641d
    );

  box-shadow:
    0 0 0 7px rgba(247, 185, 56, .08),
    0 0 32px rgba(247, 185, 56, .20),
    0 18px 45px rgba(15, 23, 42, .28);
}


.bronze-avatar {
  border-color: #c77845;

  background:
    linear-gradient(
      145deg,
      #d89a6d,
      #704025
    );
}


.podium-medal {
  position: absolute;

  left: 50%;
  bottom: -25px;

  transform: translateX(-50%);

  width: 43px;
  height: 43px;

  display: grid;
  place-items: center;

  border-radius: 50%;

  font-size: 12px;
  font-weight: 900;

  background: #182033;

  border: 1px solid rgba(255, 255, 255, .18);

  box-shadow:
    0 8px 20px rgba(0, 0, 0, .25);
}


.silver-medal {
  color: #e2e8f0;

  border-color: rgba(203, 213, 225, .55);

  background:
    linear-gradient(
      145deg,
      #4b5563,
      #1e293b
    );
}


.gold-medal {
  color: #ffd75c;

  border-color: rgba(247, 185, 56, .65);

  background:
    linear-gradient(
      145deg,
      #5b451b,
      #241b0b
    );
}


.bronze-medal {
  color: #f2a36e;

  border-color: rgba(181, 107, 61, .65);

  background:
    linear-gradient(
      145deg,
      #59321d,
      #24150d
    );
}


.winner-crown {
  position: absolute;

  left: 50%;
  top: -34px;

  transform: translateX(-50%);

  width: 36px;
  height: 36px;

  display: grid;
  place-items: center;

  color: #f7c74b;

  filter:
    drop-shadow(
      0 0 10px
      rgba(247, 199, 75, .42)
    );
}


.winner-crown svg {
  width: 31px;
  height: 31px;
}


/* =========================
   Podium Blocks
   ========================= */

.podium-block {
  width: 100%;

  min-height: 185px;

  padding: 48px 12px 18px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: flex-end;

  text-align: center;

  border-radius: 19px 19px 0 0;

  border: 1px solid;

  border-bottom: 0;

  box-shadow:
    inset 0 1px rgba(255, 255, 255, .08);
}


.silver-block {
  min-height: 185px;

  border-color: #dbe2ea;

  background:
    radial-gradient(
      circle at 50% 0,
      rgba(148, 163, 184, .18),
      transparent 48%
    ),

    linear-gradient(
      145deg,
      #f8fafc,
      #e9edf3
    );
}


.gold-block {
  min-height: 245px;

  border-color: rgba(247, 185, 56, .35);

  background:
    radial-gradient(
      circle at 50% 0,
      rgba(255, 205, 75, .22),
      transparent 48%
    ),

    linear-gradient(
      145deg,
      #fff8e7,
      #f5e3b7
    );

  box-shadow:
    inset 0 1px rgba(255, 255, 255, .45),
    0 10px 35px rgba(247, 185, 56, .07);
}


.bronze-block {
  min-height: 172px;

  border-color: rgba(181, 107, 61, .30);

  background:
    radial-gradient(
      circle at 50% 0,
      rgba(196, 106, 54, .15),
      transparent 48%
    ),

    linear-gradient(
      145deg,
      #fff4ed,
      #f4ded0
    );
}


.podium-position {
  color: #64748b;

  font-size: 9px;
  font-weight: 800;

  margin-bottom: 4px;
}


.winner-position {
  color: #a16207;
}


.podium-name {
  max-width: 90%;

  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;

  color: #1e293b;

  font-size: 13px;
  font-weight: 800;
}


.podium-time {
  margin-top: 8px;

  color: #0f172a;

  font-size: 19px;
  font-weight: 900;

  direction: ltr;
}


.podium-time-label {
  margin-top: 2px;

  color: #64748b;

  font-size: 9px;
}


.podium-status {
  display: inline-flex;

  align-items: center;

  gap: 5px;

  margin-top: 9px;

  color: #94a3b8;

  font-size: 8px;
  font-weight: 700;
}


.podium-status span {
  width: 5px;
  height: 5px;

  border-radius: 50%;

  background: #cbd5e1;
}


.podium-status.studying {
  color: #059669;
}


.podium-status.studying span {
  background: #10b981;

  box-shadow:
    0 0 0 3px
    rgba(16, 185, 129, .10);
}


/* =========================
   Ranking List
   ========================= */

.ranking-list-container {
  max-width: 850px;

  margin: 0 auto;

  padding: 16px;

  border-radius: 21px;

  background: #fafbfc;

  border: 1px solid #eef2f7;
}


.ranking-list-header {
  display: grid;

  grid-template-columns:
    65px
    minmax(0, 1fr)
    110px;

  align-items: center;

  padding: 0 13px 9px;

  color: #94a3b8;

  font-size: 9px;
  font-weight: 700;
}


.ranking-list-header span:last-child {
  text-align: left;
}


.ranking-list {
  display: flex;

  flex-direction: column;
}


.ranking-row {
  min-height: 58px;

  display: grid;

  grid-template-columns:
    45px
    40px
    minmax(0, 1fr)
    auto;

  align-items: center;

  gap: 10px;

  padding: 7px 12px;

  margin-top: 4px;

  border-radius: 14px;

  background: white;

  border: 1px solid transparent;

  transition:
    transform .2s ease,
    background .2s ease,
    border-color .2s ease,
    box-shadow .2s ease;
}


.ranking-row:nth-child(even) {
  background: #f8fafc;
}


.ranking-row:hover {
  transform: translateY(-1px);

  border-color:
    rgba(var(--primary-rgb), .14);

  background: white;

  box-shadow:
    0 7px 18px rgba(15, 23, 42, .05);
}


.rank-number {
  width: 31px;
  height: 31px;

  display: grid;
  place-items: center;

  border-radius: 9px;

  background: #f1f5f9;

  color: #64748b;

  font-size: 10px;
  font-weight: 800;
}


.member-avatar {
  width: 40px;
  height: 40px;

  border-radius: 12px;

  display: grid;
  place-items: center;

  color: var(--primary);

  background: var(--primary-100);

  font-size: 13px;
  font-weight: 850;
}


.member-info {
  min-width: 0;

  display: flex;

  flex-direction: column;

  gap: 4px;
}


.member-info strong {
  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;

  color: var(--text-main);

  font-size: 12px;
  font-weight: 750;
}


.member-state {
  display: flex;

  align-items: center;

  gap: 5px;

  color: #94a3b8;

  font-size: 9px;
}


.member-state span {
  width: 5px;
  height: 5px;

  border-radius: 50%;

  background: #cbd5e1;
}


.member-state.studying {
  color: #059669;
}


.member-state.studying span {
  background: #10b981;
}


.member-time {
  display: flex;

  flex-direction: column;

  align-items: flex-end;

  gap: 2px;
}


.member-time strong {
  color: var(--text-main);

  font-size: 11px;
  font-weight: 850;

  direction: ltr;
}


.member-time span {
  color: #94a3b8;

  font-size: 8px;
}


/* =========================
   Stats
   ========================= */

.ranking-stats {
  max-width: 850px;

  margin: 14px auto 0;

  display: grid;

  grid-template-columns:
    repeat(3, minmax(0, 1fr));

  gap: 10px;
}


.ranking-stat {
  min-height: 82px;

  display: flex;

  align-items: center;

  gap: 11px;

  padding: 13px;

  border-radius: 16px;

  background:
    linear-gradient(
      145deg,
      #ffffff,
      #f8fafc
    );

  border: 1px solid #eef2f7;
}


.stat-icon {
  width: 42px;
  height: 42px;

  flex-shrink: 0;

  display: grid;
  place-items: center;

  border-radius: 12px;
}


.stat-icon svg {
  width: 20px;
  height: 20px;
}


.purple-icon {
  color: #8b5cf6;

  background: rgba(139, 92, 246, .10);
}


.blue-icon {
  color: #3b82f6;

  background: rgba(59, 130, 246, .10);
}


.green-icon {
  color: #10b981;

  background: rgba(16, 185, 129, .10);
}


.stat-content {
  min-width: 0;

  display: flex;

  flex-direction: column;

  gap: 4px;
}


.stat-content span {
  color: #94a3b8;

  font-size: 9px;
}


.stat-content strong {
  color: var(--text-main);

  font-size: 15px;
  font-weight: 850;

  direction: ltr;

  text-align: right;
}


/* =========================
   Empty
   ========================= */

.empty-ranking {
  padding: 55px 15px;

  text-align: center;
}


.empty-icon {
  width: 58px;
  height: 58px;

  margin: 0 auto 13px;

  border-radius: 17px;

  background: #f8fafc;

  color: #94a3b8;

  display: grid;
  place-items: center;
}


.empty-icon svg {
  width: 27px;
  height: 27px;
}


.empty-ranking h3 {
  margin: 0 0 6px;

  color: var(--text-main);

  font-size: 14px;
  font-weight: 800;
}


.empty-ranking p {
  margin: 0;

  color: var(--text-muted);

  font-size: 11px;
}


/* =========================
   States
   ========================= */

.state-card {
  min-height: 280px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 12px;

  padding: 30px;

  background: white;

  border: 1px solid var(--border);

  border-radius: 20px;

  text-align: center;
}


.state-card p {
  margin: 0;

  color: var(--text-muted);

  font-size: 13px;
}


.state-card h2 {
  margin: 0;

  font-size: 18px;
}


.error-card {
  color: var(--text-main);
}


.error-card p {
  max-width: 400px;
}


.state-icon {
  width: 50px;
  height: 50px;

  border-radius: 15px;

  display: grid;
  place-items: center;

  font-size: 22px;
  font-weight: 900;
}


.error-icon {
  color: #dc2626;
  background: #fef2f2;
}


.loader,
.button-loader {
  border: 3px solid rgba(255, 255, 255, .35);

  border-top-color: currentColor;

  border-radius: 50%;

  animation: spin .8s linear infinite;
}


.loader {
  width: 32px;
  height: 32px;

  border-color: var(--primary-200);

  border-top-color: var(--primary);
}


.button-loader {
  width: 15px;
  height: 15px;
}


@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


/* =========================================================
   DARK MODE
   ========================================================= */

.dark .study-room-page {
  background:
    linear-gradient(
      180deg,
      #0f172a 0%,
      #0f172a 72%,
      #111827 100%
    );
}


.dark .back-button,
.dark .study-card,
.dark .ranking-card,
.dark .state-card {
  background: #111827;

  border-color: #1e293b;
}


.dark .back-button {
  color: #e2e8f0;
}


.dark .back-button:hover {
  background: #172033;
}


.dark .room-title-wrapper h1,
.dark .section-heading h2,
.dark .study-status-text h3,
.dark .member-time strong,
.dark .state-card h2,
.dark .ranking-title-area h2,
.dark .member-info strong,
.dark .stat-content strong {
  color: #f8fafc;
}


.dark .room-meta,
.dark .study-status-text p,
.dark .state-card p {
  color: #94a3b8;
}


.dark .study-status-area {
  background: #0f172a;

  border-color: #1e293b;
}


.dark .ranking-crown {
  background:
    linear-gradient(
      145deg,
      #33280e,
      #211b0b
    );

  border-color:
    rgba(247, 185, 56, .22);
}


.dark .ranking-title-area h2 {
  color: #f8fafc;
}


.dark .ranking-list-container {
  background: #0f172a;

  border-color: #1e293b;
}


.dark .ranking-row {
  background: #111827;

  border-color: transparent;
}


.dark .ranking-row:nth-child(even) {
  background: #0d1525;
}


.dark .ranking-row:hover {
  background: #172033;

  border-color:
    rgba(var(--primary-rgb), .18);
}


.dark .ranking-list-header {
  color: #64748b;
}


.dark .rank-number {
  background: #1e293b;

  color: #94a3b8;
}


.dark .member-avatar {
  background:
    rgba(var(--primary-rgb), .14);
}


.dark .ranking-tabs {
  background: #0f172a;

  border-color: #1e293b;
}


.dark .ranking-tab {
  color: #94a3b8;
}


.dark .ranking-tab:hover {
  color: var(--primary);
}


.dark .ranking-tab.active {
  color: var(--primary);

  background: #1e293b;

  box-shadow:
    0 2px 8px rgba(0, 0, 0, .18);
}


.dark .silver-block {
  border-color: #334155;

  background:
    radial-gradient(
      circle at 50% 0,
      rgba(148, 163, 184, .12),
      transparent 48%
    ),

    linear-gradient(
      145deg,
      #1e293b,
      #111827
    );
}


.dark .gold-block {
  border-color:
    rgba(247, 185, 56, .25);

  background:
    radial-gradient(
      circle at 50% 0,
      rgba(247, 185, 56, .12),
      transparent 48%
    ),

    linear-gradient(
      145deg,
      #3a2e13,
      #211b0e
    );
}


.dark .bronze-block {
  border-color:
    rgba(181, 107, 61, .25);

  background:
    radial-gradient(
      circle at 50% 0,
      rgba(196, 106, 54, .10),
      transparent 48%
    ),

    linear-gradient(
      145deg,
      #382318,
      #21160f
    );
}


.dark .podium-name,
.dark .podium-time {
  color: #f8fafc;
}


.dark .podium-position,
.dark .podium-time-label {
  color: #94a3b8;
}


.dark .winner-position {
  color: #f5c451;
}


.dark .ranking-stat {
  background:
    linear-gradient(
      145deg,
      #111827,
      #0f172a
    );

  border-color: #1e293b;
}


.dark .stat-content span {
  color: #64748b;
}


.dark .empty-icon {
  background: #0f172a;
}


.dark .empty-ranking h3 {
  color: #f8fafc;
}


/* Dark buttons */

.dark .secondary-button {
  color: #e2e8f0;

  background: #111827;

  border-color: #334155;
}


.dark .secondary-button:hover:not(:disabled) {
  background: #172033;
}


/* =========================
   Mobile
   ========================= */

@media (max-width: 760px) {

  .page-wrapper {
    padding:
      18px
      14px
      110px;
  }


  .room-header {
    margin-bottom: 18px;
  }


  .room-title-wrapper h1 {
    font-size: 18px;
  }


  .overview-card {
    padding: 22px;

    border-radius: 20px;
  }


  .overview-card h2 {
    font-size: 23px;
  }


  .overview-card p {
    font-size: 12px;
  }


  .overview-info {
    gap: 15px;
  }


  .study-card,
  .ranking-card {
    padding: 18px;

    border-radius: 18px;
  }


  .study-actions {
    flex-direction: column;
  }


  .primary-button,
  .secondary-button {
    width: 100%;
  }


  /* Ranking */

  .ranking-header {
    align-items: flex-start;
  }


  .ranking-crown {
    width: 43px;
    height: 43px;

    border-radius: 13px;
  }


  .ranking-title-area h2 {
    font-size: 16px;
  }


  .ranking-subtitle {
    font-size: 9px;
  }


  .ranking-header-right {
    flex-direction: column;
    align-items: flex-end;
    gap: 5px;
  }


  .ranking-tabs {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));

    gap: 5px;

    padding: 5px;

    margin-bottom: 18px;
  }


  .ranking-tab {
    min-height: 36px;

    font-size: 10px;

    padding:
      7px
      6px;
  }


  /* Podium */

  .ranking-podium {
    min-height: 290px;

    padding:
      50px
      0
      0;
  }


  .podium-avatar {
    width: 65px;
    height: 65px;

    font-size: 18px;
  }


  .gold-avatar {
    width: 78px;
    height: 78px;
  }


  .winner-crown {
    top: -26px;

    width: 27px;
    height: 27px;
  }


  .winner-crown svg {
    width: 24px;
    height: 24px;
  }


  .podium-medal {
    width: 34px;
    height: 34px;

    bottom: -20px;

    font-size: 10px;
  }


  .podium-block {
    min-height: 140px;

    padding:
      40px
      5px
      13px;
  }


  .gold-block {
    min-height: 185px;
  }


  .silver-block {
    min-height: 140px;
  }


  .bronze-block {
    min-height: 130px;
  }


  .podium-position {
    font-size: 7px;
  }


  .podium-name {
    font-size: 9px;
  }


  .podium-time {
    font-size: 12px;
  }


  .podium-time-label {
    font-size: 7px;
  }


  .podium-status {
    font-size: 7px;

    gap: 3px;
  }


  .podium-status span {
    width: 4px;
    height: 4px;
  }


  /* List */

  .ranking-list-container {
    padding: 9px;

    border-radius: 16px;
  }


  .ranking-list-header {
    grid-template-columns:
      43px
      minmax(0, 1fr)
      85px;

    padding:
      0
      8px
      7px;

    font-size: 8px;
  }


  .ranking-row {
    grid-template-columns:
      31px
      36px
      minmax(0, 1fr)
      auto;

    gap: 7px;

    min-height: 53px;

    padding:
      6px
      8px;
  }


  .rank-number {
    width: 28px;
    height: 28px;
  }


  .member-avatar {
    width: 36px;
    height: 36px;

    border-radius: 11px;
  }


  .member-info strong {
    font-size: 10px;
  }


  .member-state {
    font-size: 8px;
  }


  .member-time strong {
    font-size: 9px;
  }


  .member-time span {
    font-size: 7px;
  }


  /* Stats */

  .ranking-stats {
    grid-template-columns: 1fr;

    gap: 7px;
  }


  .ranking-stat {
    min-height: 65px;

    padding: 10px;
  }


  .stat-icon {
    width: 36px;
    height: 36px;

    border-radius: 10px;
  }


  .stat-icon svg {
    width: 18px;
    height: 18px;
  }


  .stat-content span {
    font-size: 8px;
  }


  .stat-content strong {
    font-size: 13px;
  }
}


/* =========================
   Very Small Screens
   ========================= */

@media (max-width: 420px) {

  .ranking-header {
    gap: 8px;
  }


  .ranking-title-area {
    gap: 9px;
  }


  .ranking-crown {
    width: 39px;
    height: 39px;
  }


  .ranking-crown svg {
    width: 21px;
    height: 21px;
  }


  .ranking-title-area h2 {
    font-size: 14px;
  }


  .ranking-subtitle {
    display: none;
  }


  .live-ranking-indicator {
    padding:
      5px
      7px;

    font-size: 8px;
  }


  .ranking-count {
    font-size: 9px;
  }


  .ranking-podium {
    min-height: 260px;
  }


  .podium-avatar {
    width: 57px;
    height: 57px;
  }


  .gold-avatar {
    width: 69px;
    height: 69px;
  }


  .podium-block {
    min-height: 125px;
  }


  .gold-block {
    min-height: 165px;
  }


  .silver-block {
    min-height: 125px;
  }


  .bronze-block {
    min-height: 116px;
  }


  .podium-name {
    max-width: 95%;

    font-size: 8px;
  }


  .podium-time {
    font-size: 10px;
  }


  .podium-time-label {
    font-size: 6px;
  }


  .podium-status {
    display: none;
  }


  .ranking-tabs {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }
}



.face-analysis-video {
  position: fixed;
  width: 2px;
  height: 2px;
  right: -10px;
  bottom: -10px;
  opacity: 0.01;
  pointer-events: none;
}


/* =========================================================
   MODERN ROOM UI + REAL LOCAL DARK THEME
   ========================================================= */

.study-room-page {
  position: relative;
  isolation: isolate;
  overflow-x: hidden;
  transition: background .35s ease, color .35s ease;
}

.study-room-page::before,
.study-room-page::after {
  content: "";
  position: fixed;
  z-index: -1;
  pointer-events: none;
  border-radius: 999px;
  filter: blur(30px);
  opacity: .28;
}

.study-room-page::before {
  width: 260px;
  height: 260px;
  top: 90px;
  right: -120px;
  background: rgba(var(--primary-rgb), .18);
}

.study-room-page::after {
  width: 220px;
  height: 220px;
  bottom: 80px;
  left: -120px;
  background: rgba(var(--primary-rgb), .12);
}

.room-header {
  position: sticky;
  top: 12px;
  z-index: 20;
  padding: 8px;
  margin-inline: -8px;
  border-radius: 18px;
  background: color-mix(in srgb, var(--app-bg) 82%, transparent);
  backdrop-filter: blur(16px);
}

.back-button,
.study-card,
.ranking-card,
.state-card,
.room-chat-section {
  transition:
    background .3s ease,
    border-color .3s ease,
    box-shadow .3s ease,
    transform .25s ease;
}

.back-button {
  box-shadow: 0 8px 24px rgba(15, 23, 42, .05);
}

.back-button:hover {
  box-shadow: 0 12px 28px rgba(var(--primary-rgb), .10);
}

.study-card:hover,
.ranking-card:hover,
.room-chat-section:hover {
  box-shadow:
    0 16px 42px rgba(15, 23, 42, .07),
    0 0 0 1px rgba(var(--primary-rgb), .04);
}

.overview-card {
  box-shadow:
    0 22px 55px rgba(15, 23, 42, .14),
    inset 0 1px rgba(255,255,255,.06);
}

.room-chat-section {
  position: relative;
  overflow: hidden;
  margin-bottom: 18px;
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: var(--card-bg, #fff);
  box-shadow:
    0 1px 2px rgba(15,23,42,.03),
    0 10px 34px rgba(15,23,42,.05);
}

.room-chat-section::before {
  content: "";
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--primary),
    transparent
  );
  opacity: .7;
}

.room-chat-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.room-chat-section-title {
  display: flex;
  align-items: center;
  gap: 13px;
  min-width: 0;
}

.room-chat-section-icon {
  width: 46px;
  height: 46px;
  flex: 0 0 46px;
  display: grid;
  place-items: center;
  border-radius: 15px;
  color: var(--primary);
  background: var(--primary-100);
  box-shadow: inset 0 0 0 1px rgba(var(--primary-rgb), .08);
}

.room-chat-section-icon svg {
  width: 23px;
  height: 23px;
}

.room-chat-section-title h2 {
  margin: 0;
  color: var(--text-main);
  font-size: 19px;
  font-weight: 850;
}

.room-chat-section-title p {
  margin: 4px 0 0;
  color: var(--text-muted);
  font-size: 11px;
  line-height: 1.8;
}

.room-chat-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 10px;
  border-radius: 999px;
  color: #047857;
  background: #ecfdf5;
  border: 1px solid #d1fae5;
  font-size: 10px;
  font-weight: 850;
  white-space: nowrap;
}

.room-chat-badge-dot,
.room-chat-badge-dot::after {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.room-chat-badge-dot {
  position: relative;
  background: #10b981;
}

.room-chat-badge-dot::after {
  content: "";
  position: absolute;
  inset: 0;
  background: #10b981;
  animation: roomChatPulse 1.8s infinite ease-out;
}

.room-chat-host {
  min-width: 0;
}

@keyframes roomChatPulse {
  0% {
    transform: scale(1);
    opacity: .45;
  }
  70%, 100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

/* ===== Local dark mode ===== */

.study-room-page.is-dark {
  --room-surface: #0f172a;
  --room-surface-2: #111827;
  --room-surface-3: #172033;
  --room-border: rgba(148, 163, 184, .14);
  --room-text: #f8fafc;
  --room-muted: #94a3b8;
  background:
    radial-gradient(circle at 80% 0%, rgba(var(--primary-rgb), .06), transparent 28%),
    linear-gradient(180deg, #070d19 0%, #0b1220 55%, #0f172a 100%);
}

.study-room-page.is-dark .room-header {
  background: rgba(7, 13, 25, .72);
}

.study-room-page.is-dark .back-button,
.study-room-page.is-dark .study-card,
.study-room-page.is-dark .ranking-card,
.study-room-page.is-dark .state-card,
.study-room-page.is-dark .room-chat-section {
  background: var(--room-surface-2);
  border-color: var(--room-border);
  box-shadow:
    0 14px 40px rgba(0,0,0,.20),
    inset 0 1px rgba(255,255,255,.025);
}

.study-room-page.is-dark .back-button {
  color: var(--room-text);
}

.study-room-page.is-dark .back-button:hover {
  background: var(--room-surface-3);
  border-color: rgba(var(--primary-rgb), .22);
}

.study-room-page.is-dark .room-title-wrapper h1,
.study-room-page.is-dark .section-heading h2,
.study-room-page.is-dark .ranking-title-area h2,
.study-room-page.is-dark .study-status-text h3,
.study-room-page.is-dark .member-info strong,
.study-room-page.is-dark .member-time strong,
.study-room-page.is-dark .stat-content strong,
.study-room-page.is-dark .state-card h2,
.study-room-page.is-dark .room-chat-section-title h2 {
  color: var(--room-text);
}

.study-room-page.is-dark .room-meta,
.study-room-page.is-dark .study-status-text p,
.study-room-page.is-dark .state-card p,
.study-room-page.is-dark .ranking-subtitle,
.study-room-page.is-dark .room-chat-section-title p {
  color: var(--room-muted);
}

.study-room-page.is-dark .study-status-area {
  background: #0b1422;
  border-color: var(--room-border);
}

.study-room-page.is-dark .secondary-button {
  color: #e2e8f0;
  background: #111827;
  border-color: #334155;
}

.study-room-page.is-dark .secondary-button:hover:not(:disabled) {
  background: #172033;
}

.study-room-page.is-dark .ranking-tabs {
  background: #0b1422;
  border-color: var(--room-border);
}

.study-room-page.is-dark .ranking-tab {
  color: #94a3b8;
}

.study-room-page.is-dark .ranking-tab.active {
  color: var(--primary);
  background: #182234;
  box-shadow: 0 5px 16px rgba(0,0,0,.20);
}

.study-room-page.is-dark .ranking-list-container {
  background: #0b1422;
  border-color: var(--room-border);
}

.study-room-page.is-dark .ranking-row {
  background: #111827;
  border-color: transparent;
}

.study-room-page.is-dark .ranking-row:nth-child(even) {
  background: #0e1625;
}

.study-room-page.is-dark .ranking-row:hover {
  background: #172033;
}

.study-room-page.is-dark .ranking-stat {
  background: linear-gradient(145deg, #111827, #0f172a);
  border-color: var(--room-border);
}

.study-room-page.is-dark .rank-number {
  background: #1e293b;
  color: #94a3b8;
}

.study-room-page.is-dark .empty-icon {
  background: #0b1422;
}

.study-room-page.is-dark .room-chat-badge {
  color: #6ee7b7;
  background: rgba(16,185,129,.10);
  border-color: rgba(16,185,129,.18);
}

.study-room-page.is-dark .room-chat-section-icon {
  background: rgba(var(--primary-rgb), .12);
  box-shadow: inset 0 0 0 1px rgba(var(--primary-rgb), .12);
}

@media (max-width: 760px) {
  .room-header {
    position: relative;
    top: auto;
    margin-inline: 0;
    padding: 0;
    background: transparent;
    backdrop-filter: none;
  }

  .room-chat-section {
    padding: 18px;
    border-radius: 18px;
  }

  .room-chat-section-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .room-chat-badge {
    align-self: flex-start;
  }
}

@media (max-width: 480px) {
  .room-chat-section {
    padding: 15px;
  }

  .room-chat-section-icon {
    width: 42px;
    height: 42px;
    flex-basis: 42px;
    border-radius: 13px;
  }

  .room-chat-section-title h2 {
    font-size: 16px;
  }

  .room-chat-section-title p {
    font-size: 10px;
  }
}


/* =========================================================
   COMPACT TAB-FIRST ROOM LAYOUT
   ========================================================= */
.room-tabs {
  position: sticky;
  top: 88px;
  z-index: 15;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 7px;
  width: min(100%, 980px);
  margin: 12px auto 14px;
  padding: 6px;
  border: 1px solid var(--room-border, rgba(148,163,184,.18));
  border-radius: 18px;
  background: color-mix(in srgb, var(--surface, #fff) 88%, transparent);
  box-shadow: 0 10px 34px rgba(15,23,42,.06);
  backdrop-filter: blur(18px) saturate(1.1);
}

.room-tab {
  position: relative;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  border: 0;
  border-radius: 13px;
  padding: 9px 14px;
  background: transparent;
  color: var(--text-secondary, #64748b);
  font: inherit;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: .22s ease;
}

.room-tab:hover {
  color: var(--text-primary, #0f172a);
  background: rgba(var(--primary-rgb), .055);
}

.room-tab.active {
  color: #fff;
  background: linear-gradient(135deg, var(--primary), color-mix(in srgb, var(--primary) 72%, #111827));
  box-shadow: 0 10px 24px rgba(var(--primary-rgb), .22), inset 0 1px 0 rgba(255,255,255,.18);
}

.room-tab-icon {
  width: 19px;
  height: 19px;
  display: inline-flex;
  flex: 0 0 19px;
}

.room-tab-icon svg {
  width: 100%;
  height: 100%;
}

.room-tab-live {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: #10b981;
  box-shadow: 0 0 0 4px rgba(16,185,129,.12);
}

.room-tab.active .room-tab-live {
  background: #fff;
  box-shadow: 0 0 0 4px rgba(255,255,255,.12);
}

.room-tab-panels {
  width: min(100%, 980px);
  margin: 0 auto;
}

.compact-overview {
  margin-bottom: 10px !important;
  padding: 18px 20px !important;
  border-radius: 20px !important;
}

.compact-overview .overview-content {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(300px, .9fr);
  gap: 16px 24px;
  align-items: center;
}

.compact-overview .overview-content > .status-badge,
.compact-overview .overview-content > h2,
.compact-overview .overview-content > p {
  grid-column: 1;
}

.compact-overview .overview-info {
  grid-column: 2;
  grid-row: 1 / span 3;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-top: 0 !important;
}

.compact-overview .info-item {
  min-width: 0;
  padding: 10px 9px;
  border: 1px solid var(--room-border, rgba(148,163,184,.16));
  border-radius: 14px;
  background: rgba(var(--primary-rgb), .025);
}

.compact-overview .info-icon {
  width: 30px;
  height: 30px;
  flex: 0 0 30px;
}

.compact-overview h2 {
  margin: 3px 0 2px;
  font-size: clamp(18px, 2vw, 23px);
}

.compact-overview p {
  margin: 0;
  max-width: 600px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.study-card,
.room-chat-section,
.ranking-card {
  min-height: 0;
  margin-bottom: 14px !important;
}

.room-chat-section {
  padding: 14px !important;
}

.room-chat-section-header {
  margin-bottom: 10px !important;
}

.room-chat-host {
  min-height: 0;
  overflow: hidden;
  border-radius: 16px;
}

.ranking-card {
  padding: 18px !important;
}

.ranking-header {
  margin-bottom: 12px !important;
}

.ranking-podium {
  margin-top: 12px !important;
  gap: 12px !important;
}

.ranking-list-container {
  max-height: min(42vh, 390px);
  overflow: auto;
  scrollbar-width: thin;
}

.ranking-stats {
  margin-top: 12px !important;
}

.study-card {
  padding: 18px !important;
}

.study-card .section-heading {
  margin-bottom: 12px !important;
}

.study-status-area {
  margin-bottom: 12px !important;
}

/* When a tab is inactive, v-show controls the display. This class keeps the panel clean when active. */
.room-tab-panels > section[style*="display: none"] {
  margin: 0 !important;
}

.study-room-page.is-dark .room-tabs {
  background: rgba(15,23,42,.82);
  border-color: var(--room-border, rgba(148,163,184,.16));
  box-shadow: 0 14px 40px rgba(0,0,0,.24);
}

.study-room-page.is-dark .room-tab {
  color: #94a3b8;
}

.study-room-page.is-dark .room-tab:hover {
  color: #e2e8f0;
  background: rgba(var(--primary-rgb), .08);
}

.study-room-page.is-dark .room-tab.active {
  color: #fff;
}

.study-room-page.is-dark .compact-overview .info-item {
  background: rgba(255,255,255,.018);
}

@media (max-width: 820px) {
  .room-tabs {
    top: 72px;
  }

  .compact-overview .overview-content {
    grid-template-columns: 1fr;
  }

  .compact-overview .overview-content > .status-badge,
  .compact-overview .overview-content > h2,
  .compact-overview .overview-content > p,
  .compact-overview .overview-info {
    grid-column: 1;
    grid-row: auto;
  }

  .compact-overview .overview-info {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .room-tabs {
    top: 66px;
    margin-top: 10px;
    border-radius: 15px;
    padding: 5px;
  }

  .room-tab {
    min-height: 44px;
    gap: 5px;
    padding-inline: 6px;
    font-size: 11px;
  }

  .room-tab-icon {
    width: 17px;
    height: 17px;
    flex-basis: 17px;
  }

  .compact-overview {
    padding: 15px !important;
  }

  .compact-overview .overview-info {
    grid-template-columns: 1fr;
  }

  .compact-overview p {
    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
}

</style>
