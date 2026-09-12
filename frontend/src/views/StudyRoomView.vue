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

<style src="../assets/studyroom.css" scoped></style>