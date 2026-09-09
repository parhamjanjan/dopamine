<template>
  <div class="rooms-page">
    <div class="rooms-wrapper">

      <!-- Header -->
      <header class="page-header">
        <div class="header-content">
          <div class="eyebrow">
            <span class="eyebrow-dot"></span>
            فضای مطالعه
          </div>

          <h1>سالن‌های مطالعه</h1>

          <p>
            یک سالن مناسب انتخاب کن و با بقیه همراه شو.
          </p>
        </div>

        <button
          class="icon-button"
          type="button"
          aria-label="ساخت سالن جدید"
          @click="openCreateModal"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M12 5v14" />
            <path d="M5 12h14" />
          </svg>
        </button>
      </header>

      <!-- Current membership -->
      <section
        v-if="currentMembership"
        class="current-room-card"
      >
        <div class="current-room-icon">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M3 21h18" />
            <path d="M5 21V7l7-4 7 4v14" />
            <path d="M9 21v-6h6v6" />
            <path d="M9 9h.01" />
            <path d="M15 9h.01" />
            <path d="M9 12h.01" />
            <path d="M15 12h.01" />
          </svg>
        </div>

        <div class="current-room-content">
          <span class="current-room-label">
            سالن فعلی شما
          </span>

          <strong>
            {{ currentMembership.name }}
          </strong>

          <p>
            شما عضو این سالن هستی و برای ورود به سالن دیگری
            ابتدا باید از سالن فعلی خارج شوی.
          </p>
        </div>

        <button
          class="current-room-button"
          type="button"
          @click="enterCurrentRoom"
        >
          ورود به سالن
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M5 12h14" />
            <path d="m13 6 6 6-6 6" />
          </svg>
        </button>
      </section>

      <!-- Create room -->
      <section class="create-card">
        <div class="create-card-icon">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M12 5v14" />
            <path d="M5 12h14" />
          </svg>
        </div>

        <div class="create-card-content">
          <h2>
            سالن مطالعه جدید بساز
          </h2>

          <p>
            یک فضای اختصاصی برای مطالعه و همراهی با دوستانت ایجاد کن.
          </p>
        </div>

        <button
          class="primary-button"
          type="button"
          @click="openCreateModal"
        >
          ساخت سالن
        </button>
      </section>

      <!-- Search -->
      <div class="search-box">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle
            cx="11"
            cy="11"
            r="7"
          />
          <path d="m20 20-4-4" />
        </svg>

        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجوی سالن..."
        />

        <button
          v-if="searchQuery"
          class="clear-search"
          type="button"
          aria-label="پاک کردن جستجو"
          @click="searchQuery = ''"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M18 6 6 18" />
            <path d="m6 6 12 12" />
          </svg>
        </button>
      </div>

      <!-- Section -->
      <div class="section-heading">
        <div>
          <div class="section-title-row">
            <h2>
              سالن‌های فعال
            </h2>

            <span class="room-count-badge">
              {{ filteredRooms.length }}
            </span>
          </div>

          <p>
            سالن‌های آماده برای مطالعه و همراهی
          </p>
        </div>
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        class="loading-state"
      >
        <div class="loading-spinner"></div>

        <p>
          در حال دریافت سالن‌ها...
        </p>
      </div>

      <!-- Rooms -->
      <section
        v-else
        class="rooms-grid"
      >
        <article
          v-for="room in filteredRooms"
          :key="room.id"
          class="room-card"
          :class="{
            'room-card-current':
              currentMembership?.id === room.id
          }"
        >

          <!-- Card top -->
          <div class="room-card-top">

            <div
              class="room-icon"
              :style="{
                background: getRoomColor(room) + '18',
                color: getRoomColor(room)
              }"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M3 21h18" />
                <path d="M5 21V7l7-4 7 4v14" />
                <path d="M9 21v-6h6v6" />
                <path d="M9 9h.01" />
                <path d="M15 9h.01" />
                <path d="M9 12h.01" />
                <path d="M15 12h.01" />
              </svg>
            </div>

            <div class="room-statuses">

              <span class="online-badge">
                <span></span>
                فعال
              </span>

              <span
                v-if="room.is_private"
                class="privacy-badge"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <rect
                    x="4"
                    y="10"
                    width="16"
                    height="11"
                    rx="2"
                  />
                  <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                </svg>

                خصوصی
              </span>

            </div>
          </div>

          <!-- Title -->
          <div class="room-title-area">
            <h3>
              {{ room.name }}
            </h3>

            <span
              v-if="currentMembership?.id === room.id"
              class="you-badge"
            >
              عضو هستی
            </span>
          </div>

          <!-- Description -->
          <p class="room-description">
            {{
              room.description ||
              'فضایی مناسب برای مطالعه و تمرکز گروهی.'
            }}
          </p>

          <!-- Details -->
          <div class="room-details">

            <!-- Members -->
            <div class="detail-item">

              <div class="detail-icon">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path
                    d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"
                  />
                  <circle
                    cx="9"
                    cy="7"
                    r="4"
                  />
                  <path
                    d="M22 21v-2a4 4 0 0 0-3-3.87"
                  />
                  <path
                    d="M16 3.13a4 4 0 0 1 0 7.75"
                  />
                </svg>
              </div>

              <div class="detail-text">
                <strong>
                  {{ getMemberCount(room) }}
                </strong>

                <span>
                  عضو
                </span>
              </div>

            </div>

            <!-- Occupancy -->
            <div
              class="detail-item occupancy-item"
              :class="getOccupancyClass(room)"
            >

              <div class="detail-icon">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M4 19V9" />
                  <path d="M10 19V5" />
                  <path d="M16 19V12" />
                  <path d="M22 19V3" />
                </svg>
              </div>

              <div class="detail-text">
                <strong>
                  {{ getRoomOccupancy(room) }}٪
                </strong>

                <span>
                  {{ getOccupancyLabel(room) }}
                </span>
              </div>

            </div>

            <!-- Study time -->
            <div class="detail-item">

              <div class="detail-icon">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="9"
                  />
                  <path d="M12 7v5l3 2" />
                </svg>
              </div>

              <div class="detail-text">
                <strong>
                  {{ getRoomStudyTime(room) }}
                </strong>

                <span>
                  مطالعه
                </span>
              </div>

            </div>

          </div>

          <!-- Members avatars -->
          <div class="room-members-row">

            <div class="members-left">

              <div class="avatars">
                <span
                  v-for="(member, index) in getMemberLetters(room)"
                  :key="index"
                  class="avatar"
                  :style="{
                    zIndex: 10 - index
                  }"
                >
                  {{ member }}
                </span>

                <span
                  v-if="getMemberCount(room) > 3"
                  class="avatar more"
                >
                  +{{ getMemberCount(room) - 3 }}
                </span>

                <span
                  v-if="getMemberCount(room) === 0"
                  class="no-members"
                >
                  خالی
                </span>
              </div>

              <span class="members-label">
                اعضای سالن
              </span>

            </div>

            <span class="capacity-label">
              حداکثر {{ getRoomCapacity(room) }} نفر
            </span>

          </div>

          <!-- Join / Enter -->
          <button
            class="join-button"
            type="button"
            :class="{
              'join-button-current':
                currentMembership?.id === room.id,
              'join-button-disabled':
                hasDifferentRoomMembership(room)
            }"
            :disabled="
              joiningRoomId === room.id ||
              hasDifferentRoomMembership(room)
            "
            @click="joinRoom(room)"
          >

            <span
              v-if="joiningRoomId === room.id"
            >
              در حال ورود...
            </span>

            <span
              v-else-if="
                currentMembership?.id === room.id
              "
            >
              ورود به سالن
            </span>

            <span
              v-else-if="
                hasDifferentRoomMembership(room)
              "
            >
              عضو سالن دیگری هستی
            </span>

            <span v-else>
              ورود به سالن
            </span>

            <svg
              v-if="
                joiningRoomId !== room.id &&
                !hasDifferentRoomMembership(room)
              "
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M5 12h14" />
              <path d="m13 6 6 6-6 6" />
            </svg>

          </button>

        </article>

        <!-- Empty -->
        <div
          v-if="filteredRooms.length === 0"
          class="empty-state"
        >
          <div class="empty-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle
                cx="11"
                cy="11"
                r="7"
              />
              <path d="m20 20-4-4" />
            </svg>
          </div>

          <h3>
            سالن موردنظر پیدا نشد
          </h3>

          <p>
            عبارت جستجو را تغییر بده یا یک سالن جدید بساز.
          </p>

          <button
            class="empty-action"
            type="button"
            @click="openCreateModal"
          >
            ساخت سالن جدید
          </button>
        </div>

      </section>

    </div>

    <!-- Create Modal -->
    <div
      v-if="showCreateModal"
      class="modal-backdrop"
      @click.self="closeCreateModal"
    >

      <div class="modal-card">

        <div class="modal-header">

          <div>
            <div class="modal-eyebrow">
              سالن جدید
            </div>

            <h2>
              ساخت سالن مطالعه
            </h2>

            <p>
              اطلاعات سالن جدید را وارد کن.
            </p>
          </div>

          <button
            class="modal-close"
            type="button"
            aria-label="بستن"
            @click="closeCreateModal"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M18 6 6 18" />
              <path d="m6 6 12 12" />
            </svg>
          </button>

        </div>

        <form @submit.prevent="createRoom">

          <!-- Name -->
          <label>
            <span>
              نام سالن
            </span>

            <input
              v-model="newRoom.name"
              type="text"
              placeholder="مثلاً سالن مطالعه کنکوری‌ها"
              maxlength="100"
              required
            />
          </label>

          <!-- Description -->
          <label>
            <span>
              توضیحات
            </span>

            <textarea
              v-model="newRoom.description"
              rows="3"
              maxlength="500"
              placeholder="توضیح کوتاهی درباره سالن..."
            ></textarea>
          </label>

          <!-- Capacity -->
          <label>
            <span>
              ظرفیت سالن
            </span>

            <div class="capacity-input-wrapper">
              <input
                v-model.number="newRoom.max_members"
                type="number"
                min="1"
                max="1000"
                required
              />

              <span>
                نفر
              </span>
            </div>
          </label>

          <!-- Private -->
          <label class="checkbox-label">

            <div class="checkbox-info">
              <strong>
                سالن خصوصی
              </strong>

              <small>
                فقط افرادی که کد ورود دارند می‌توانند وارد شوند.
              </small>
            </div>

            <input
              v-model="newRoom.is_private"
              type="checkbox"
            />

          </label>

          <!-- Actions -->
          <div class="modal-actions">

            <button
              class="secondary-button"
              type="button"
              @click="closeCreateModal"
            >
              انصراف
            </button>

            <button
              class="primary-button"
              type="submit"
              :disabled="creatingRoom"
            >
              {{
                creatingRoom
                  ? 'در حال ساخت...'
                  : 'ساخت سالن'
              }}
            </button>

          </div>

        </form>

      </div>

    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div
        v-if="toastMessage"
        class="toast"
      >
        <span class="toast-icon">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M20 6 9 17l-5-5" />
          </svg>
        </span>

        {{ toastMessage }}
      </div>
    </Transition>

  </div>
</template>

<script setup>
import {
  computed,
  onMounted,
  onUnmounted,
  ref
} from 'vue'

import { useRouter } from 'vue-router'

import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

/* =========================
   State
   ========================= */

const searchQuery = ref('')
const showCreateModal = ref(false)
const toastMessage = ref('')
const loading = ref(false)
const creatingRoom = ref(false)
const joiningRoomId = ref(null)

const rooms = ref([])

const newRoom = ref({
  name: '',
  description: '',
  max_members: 20,
  is_private: false
})

/* =========================
   Computed
   ========================= */

const filteredRooms = computed(() => {
  const query = searchQuery.value
    .trim()
    .toLowerCase()

  if (!query) {
    return rooms.value
  }

  return rooms.value.filter((room) => {
    const name = String(
      room.name || ''
    ).toLowerCase()

    const description = String(
      room.description || ''
    ).toLowerCase()

    const owner = String(
      room.owner_username || ''
    ).toLowerCase()

    return (
      name.includes(query) ||
      description.includes(query) ||
      owner.includes(query)
    )
  })
})

/*
 * پیدا کردن سالن فعلی کاربر.
 *
 * Backend فعلی member_count را می‌دهد،
 * اما ممکن است members را مستقیماً برنگرداند.
 * بنابراین چند فرمت مختلف را پشتیبانی می‌کنیم.
 */
const currentMembership = computed(() => {
  const userId = auth.user?.id

  if (!userId) {
    return null
  }

  const room = rooms.value.find((room) => {
    // حالت اصلی: بک‌اند current_user_membership برمی‌گرداند
    if (room.current_user_membership) {
      const membershipUserId =
        room.current_user_membership.user

      return (
        String(membershipUserId) ===
        String(userId)
      )
    }

    // پشتیبانی از فرمت‌های قبلی
    if (Array.isArray(room.members)) {
      return room.members.some((member) => {
        const memberId =
          typeof member === 'object'
            ? member?.user
            : null

        return (
          String(memberId) ===
          String(userId)
        )
      })
    }

    return (
      room.current_user_member === true ||
      room.is_member === true ||
      room.user_is_member === true
    )
  })

  if (!room) {
    return null
  }

  return {
    id: room.id,
    name: room.name
  }
})

/* =========================
   Room helpers
   ========================= */

function getRoomColor(room) {
  return (
    room?.color ||
    auth.user?.primary_color ||
    '#7055e8'
  )
}

function getMemberCount(room) {
  return Math.max(
    0,
    Number(room?.member_count || 0)
  )
}

function getRoomCapacity(room) {
  return Math.max(
    1,
    Number(room?.max_members || 1)
  )
}

function getRoomOccupancy(room) {
  const current =
    getMemberCount(room)

  const capacity =
    getRoomCapacity(room)

  return Math.min(
    100,
    Math.round(
      (current / capacity) * 100
    )
  )
}

function getOccupancyLabel(room) {
  const percent =
    getRoomOccupancy(room)

  if (percent >= 90) {
    return 'تقریباً تکمیل'
  }

  if (percent >= 70) {
    return 'شلوغ'
  }

  if (percent >= 40) {
    return 'متعادل'
  }

  return 'فضای کافی'
}

function getOccupancyClass(room) {
  const percent =
    getRoomOccupancy(room)

  if (percent >= 90) {
    return 'high'
  }

  if (percent >= 70) {
    return 'medium'
  }

  return 'low'
}

function getMemberLetters(room) {
  if (!Array.isArray(room?.members)) {
    return []
  }

  return room.members
    .slice(0, 3)
    .map((member) => {
      if (typeof member === 'string') {
        return member
          .trim()
          .slice(0, 1)
          .toUpperCase()
      }

      return String(
        member?.username ||
        member?.first_name ||
        '?'
      )
        .trim()
        .slice(0, 1)
        .toUpperCase()
    })
}

function getRoomStudyTime(room) {
  if (
    room?.study_time !== undefined &&
    room?.study_time !== null
  ) {
    return room.study_time
  }

  if (
    room?.study_minutes !== undefined &&
    room?.study_minutes !== null
  ) {
    const minutes =
      Number(room.study_minutes) || 0

    if (minutes < 60) {
      return `${minutes} دقیقه`
    }

    const hours =
      Math.floor(minutes / 60)

    return `${hours} ساعت`
  }

  return 'امروز'
}

/* =========================
   Membership helpers
   ========================= */

function hasDifferentRoomMembership(room) {
  if (!currentMembership.value) {
    return false
  }

  return (
    String(currentMembership.value.id) !==
    String(room?.id)
  )
}

/* =========================
   Load rooms
   ========================= */

async function loadRooms() {
  loading.value = true

  try {
    const response =
      await api.get('/rooms/')

    rooms.value =
      Array.isArray(response.data)
        ? response.data
        : []

  } catch (error) {
    console.error(
      'خطا در دریافت سالن‌ها:',
      error
    )

    if (
      error.response?.status === 401
    ) {
      showToast(
        'نشست شما منقضی شده است.'
      )

      return
    }

    showToast(
      error.response?.data?.detail ||
      'دریافت سالن‌ها با خطا مواجه شد.'
    )

  } finally {
    loading.value = false
  }
}

/* =========================
   Create modal
   ========================= */

function openCreateModal() {
  showCreateModal.value = true
}

function closeCreateModal() {
  if (creatingRoom.value) {
    return
  }

  showCreateModal.value = false

  newRoom.value = {
    name: '',
    description: '',
    max_members: 20,
    is_private: false
  }
}

/* =========================
   Create room
   ========================= */

async function createRoom() {
  const name =
    newRoom.value.name.trim()

  if (!name) {
    showToast(
      'نام سالن را وارد کن.'
    )

    return
  }

  const maxMembers =
    Number(
      newRoom.value.max_members
    )

  if (
    !Number.isFinite(maxMembers) ||
    maxMembers < 1
  ) {
    showToast(
      'ظرفیت سالن معتبر نیست.'
    )

    return
  }

  creatingRoom.value = true

  try {
    const payload = {
      name,

      description:
        newRoom.value.description.trim(),

      max_members:
        maxMembers,

      is_private:
        !!newRoom.value.is_private
    }

    const response =
      await api.post(
        '/rooms/',
        payload
      )

    const createdRoom =
      response.data

    rooms.value.unshift(
      createdRoom
    )

    closeCreateModal()

    showToast(
      'سالن با موفقیت ساخته شد.'
    )

  } catch (error) {
    console.error(
      'خطا در ساخت سالن:',
      error
    )

    showToast(
      error.response?.data?.detail ||
      'ساخت سالن با خطا مواجه شد.'
    )

  } finally {
    creatingRoom.value = false
  }
}

/* =========================
   Join room
   ========================= */
function enterRoom(roomId) {
  if (!roomId) {
    return
  }

  router.push({
    name: 'study-room',
    params: {
      roomId: String(roomId)
    }
  })
}


async function joinRoom(room) {
  if (!room?.id) {
    return
  }

  /*
   * اگر کاربر عضو همین سالن است،
   * اصلاً درخواست join به بک‌اند نمی‌فرستیم.
   * مستقیماً وارد StudyRoomView می‌شویم.
   */
  if (
    currentMembership.value &&
    String(currentMembership.value.id) ===
      String(room.id)
  ) {
    enterRoom(room.id)
    return
  }

  /*
   * اگر کاربر عضو سالن دیگری است،
   * اجازه ورود مستقیم به سالن جدید نداریم.
   */
  if (hasDifferentRoomMembership(room)) {
    showToast(
      'شما در حال حاضر عضو یک سالن دیگر هستید.'
    )
    return
  }

  joiningRoomId.value = room.id

  try {
    let payload = {}

    /*
     * سالن خصوصی
     */
    if (room.is_private) {
      const joinCode = window.prompt(
        'کد ورود سالن را وارد کنید:'
      )

      if (!joinCode) {
        return
      }

      payload = {
        join_code: joinCode.trim()
      }
    }

    /*
     * ثبت عضویت در بک‌اند
     */
    await api.post(
      `/rooms/${room.id}/join/`,
      payload
    )

    /*
     * بعد از عضویت، مستقیماً وارد سالن شو.
     */
    enterRoom(room.id)

  } catch (error) {
    console.error(
      'خطا در ورود به سالن:',
      error
    )

    const detail =
      error.response?.data?.detail

    /*
     * اگر به هر دلیلی بک‌اند گفت
     * قبلاً عضو هستی، باز هم وارد سالن شو.
     *
     * این باعث می‌شود حتی اگر وضعیت فرانت
     * هنوز تازه نشده باشد، کاربر گیر نکند.
     */
    if (
      error.response?.status === 400 &&
      detail ===
        'شما قبلاً عضو این سالن هستید.'
    ) {
      enterRoom(room.id)
      return
    }

    showToast(
      detail ||
        'ورود به سالن با خطا مواجه شد.'
    )
  } finally {
    joiningRoomId.value = null
  }
}

function enterCurrentRoom() {
  if (
    !currentMembership.value
  ) {
    return
  }

  enterRoom(
    currentMembership.value.id
  )
}

/* =========================
   Toast
   ========================= */

function showToast(message) {
  toastMessage.value =
    message

  window.clearTimeout(
    showToast.timer
  )

  showToast.timer =
    window.setTimeout(() => {
      toastMessage.value = ''
    }, 2800)
}

/* =========================
   Escape
   ========================= */

function handleEscape(event) {
  if (
    event.key === 'Escape' &&
    showCreateModal.value
  ) {
    closeCreateModal()
  }
}

/* =========================
   Lifecycle
   ========================= */

onMounted(() => {
  window.addEventListener(
    'keydown',
    handleEscape
  )

  loadRooms()
})

onUnmounted(() => {
  window.removeEventListener(
    'keydown',
    handleEscape
  )

  window.clearTimeout(
    showToast.timer
  )
})
</script>

<style scoped>

/* =========================
   Page
   ========================= */

.rooms-page {
  min-height: 100vh;

  padding:
    30px
    18px
    130px;

  background:
    linear-gradient(
      180deg,
      var(--app-bg) 0%,
      var(--app-bg) 72%,
      var(--primary-50) 100%
    );

  color:
    var(--text-main);

  transition:
    background .25s ease,
    color .25s ease;
}

.rooms-wrapper {
  width:
    min(1200px, 100%);

  margin:
    0 auto;
}

/* =========================
   Header
   ========================= */

.page-header {
  display:
    flex;

  align-items:
    flex-start;

  justify-content:
    space-between;

  gap:
    20px;

  margin-bottom:
    26px;
}

.header-content {
  min-width:
    0;
}

.eyebrow {
  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  margin-bottom:
    8px;

  color:
    var(--primary);

  font-size:
    12px;

  font-weight:
    750;
}

.eyebrow-dot {
  width:
    7px;

  height:
    7px;

  flex-shrink:
    0;

  border-radius:
    50%;

  background:
    var(--primary);

  box-shadow:
    0 0 0 4px
    rgba(var(--primary-rgb), .08);
}

.page-header h1 {
  margin:
    0;

  font-size:
    clamp(26px, 4vw, 36px);

  line-height:
    1.25;

  font-weight:
    850;

  letter-spacing:
    -.7px;
}

.page-header p {
  margin:
    9px 0 0;

  color:
    var(--text-muted);

  font-size:
    13px;

  line-height:
    1.8;
}

.icon-button {
  width:
    46px;

  height:
    46px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border:
    1px solid
    var(--border);

  border-radius:
    13px;

  background:
    var(--card-bg, #fff);

  color:
    var(--text-main);

  cursor:
    pointer;

  transition:
    border-color .2s ease,
    color .2s ease,
    background .2s ease,
    transform .2s ease,
    box-shadow .2s ease;
}

.icon-button:hover {
  border-color:
    var(--primary-300);

  color:
    var(--primary);

  transform:
    translateY(-1px);

  box-shadow:
    0 7px 20px
    rgba(var(--primary-rgb), .09);
}

.icon-button svg {
  width:
    21px;

  height:
    21px;
}

/* =========================
   Current room
   ========================= */

.current-room-card {
  display:
    flex;

  align-items:
    center;

  gap:
    15px;

  padding:
    17px;

  margin-bottom:
    16px;

  border:
    1px solid
    rgba(var(--primary-rgb), .2);

  border-radius:
    18px;

  background:
    linear-gradient(
      135deg,
      rgba(var(--primary-rgb), .11),
      rgba(var(--primary-rgb), .035)
    );
}

.current-room-icon {
  width:
    48px;

  height:
    48px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border-radius:
    14px;

  background:
    rgba(var(--primary-rgb), .12);

  color:
    var(--primary);
}

.current-room-icon svg {
  width:
    23px;

  height:
    23px;
}

.current-room-content {
  min-width:
    0;

  flex:
    1;
}

.current-room-label {
  display:
    block;

  margin-bottom:
    3px;

  color:
    var(--primary);

  font-size:
    10px;

  font-weight:
    750;
}

.current-room-content strong {
  display:
    block;

  overflow:
    hidden;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;

  font-size:
    15px;

  font-weight:
    800;
}

.current-room-content p {
  margin:
    4px 0 0;

  color:
    var(--text-muted);

  font-size:
    10px;

  line-height:
    1.7;
}

.current-room-button {
  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    7px;

  flex-shrink:
    0;

  padding:
    10px 14px;

  border:
    0;

  border-radius:
    10px;

  background:
    var(--primary);

  color:
    #fff;

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
    transform .2s ease;
}

.current-room-button:hover {
  background:
    var(--primary-hover);

  transform:
    translateY(-1px);
}

.current-room-button svg {
  width:
    15px;

  height:
    15px;
}

/* =========================
   Create card
   ========================= */

.create-card {
  position:
    relative;

  overflow:
    hidden;

  display:
    flex;

  align-items:
    center;

  gap:
    16px;

  padding:
    21px;

  margin-bottom:
    22px;

  border:
    1px solid
    rgba(var(--primary-rgb), .15);

  border-radius:
    19px;

  background:
    linear-gradient(
      135deg,
      rgba(var(--primary-rgb), .085),
      rgba(var(--primary-rgb), .025)
    );
}

.create-card::after {
  content:
    '';

  position:
    absolute;

  width:
    180px;

  height:
    180px;

  left:
    -80px;

  bottom:
    -100px;

  border-radius:
    50%;

  background:
    rgba(var(--primary-rgb), .05);

  pointer-events:
    none;
}

.create-card-icon {
  width:
    48px;

  height:
    48px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border-radius:
    14px;

  background:
    rgba(var(--primary-rgb), .12);

  color:
    var(--primary);
}

.create-card-icon svg {
  width:
    23px;

  height:
    23px;
}

.create-card-content {
  flex:
    1;

  min-width:
    0;
}

.create-card h2 {
  margin:
    0 0 5px;

  font-size:
    15px;

  font-weight:
    800;
}

.create-card p {
  margin:
    0;

  color:
    var(--text-muted);

  font-size:
    11px;

  line-height:
    1.7;
}

/* =========================
   Buttons
   ========================= */

.primary-button,
.secondary-button {
  border-radius:
    10px;

  padding:
    10px 16px;

  font-family:
    inherit;

  font-size:
    12px;

  font-weight:
    700;

  cursor:
    pointer;

  transition:
    background .2s ease,
    border-color .2s ease,
    color .2s ease,
    transform .2s ease,
    opacity .2s ease;
}

.primary-button {
  border:
    0;

  background:
    var(--primary);

  color:
    #fff;
}

.primary-button:hover {
  background:
    var(--primary-hover);

  transform:
    translateY(-1px);
}

.primary-button:disabled {
  opacity:
    .55;

  cursor:
    not-allowed;

  transform:
    none;
}

.secondary-button {
  border:
    1px solid
    var(--border);

  background:
    transparent;

  color:
    var(--text-main);
}

.secondary-button:hover {
  border-color:
    var(--primary-300);

  color:
    var(--primary);
}

/* =========================
   Search
   ========================= */

.search-box {
  height:
    49px;

  display:
    flex;

  align-items:
    center;

  gap:
    10px;

  margin-bottom:
    26px;

  padding:
    0 14px;

  border:
    1px solid
    var(--border);

  border-radius:
    13px;

  background:
    var(--card-bg, #fff);

  transition:
    border-color .2s ease,
    box-shadow .2s ease,
    background .2s ease;
}

.search-box:focus-within {
  border-color:
    var(--primary-300);

  box-shadow:
    0 0 0 3px
    rgba(var(--primary-rgb), .08);
}

.search-box > svg {
  width:
    19px;

  height:
    19px;

  flex-shrink:
    0;

  color:
    var(--text-muted);
}

.search-box input {
  width:
    100%;

  min-width:
    0;

  border:
    0;

  outline:
    0;

  background:
    transparent;

  color:
    var(--text-main);

  font-family:
    inherit;

  font-size:
    12px;
}

.search-box input::placeholder {
  color:
    var(--text-muted);
}

.clear-search {
  width:
    28px;

  height:
    28px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border:
    0;

  border-radius:
    8px;

  background:
    transparent;

  color:
    var(--text-muted);

  cursor:
    pointer;
}

.clear-search:hover {
  background:
    rgba(var(--primary-rgb), .08);

  color:
    var(--primary);
}

.clear-search svg {
  width:
    15px;

  height:
    15px;
}

/* =========================
   Section
   ========================= */

.section-heading {
  margin-bottom:
    14px;
}

.section-title-row {
  display:
    flex;

  align-items:
    center;

  gap:
    8px;
}

.section-heading h2 {
  margin:
    0;

  font-size:
    18px;

  font-weight:
    800;
}

.room-count-badge {
  min-width:
    24px;

  height:
    22px;

  display:
    inline-flex;

  align-items:
    center;

  justify-content:
    center;

  padding:
    0 7px;

  border-radius:
    999px;

  background:
    rgba(var(--primary-rgb), .1);

  color:
    var(--primary);

  font-size:
    10px;

  font-weight:
    800;
}

.section-heading p {
  margin:
    4px 0 0;

  color:
    var(--text-muted);

  font-size:
    11px;
}

/* =========================
   Loading
   ========================= */

.loading-state {
  min-height:
    300px;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  justify-content:
    center;

  gap:
    14px;

  color:
    var(--text-muted);
}

.loading-state p {
  margin:
    0;

  font-size:
    11px;
}

.loading-spinner {
  width:
    31px;

  height:
    31px;

  border:
    3px solid
    rgba(var(--primary-rgb), .13);

  border-top-color:
    var(--primary);

  border-radius:
    50%;

  animation:
    room-spin .8s linear infinite;
}

@keyframes room-spin {
  to {
    transform:
      rotate(360deg);
  }
}

/* =========================
   Grid
   ========================= */

.rooms-grid {
  display:
    grid;

  grid-template-columns:
    repeat(2, minmax(0, 1fr));

  gap:
    16px;
}

/* =========================
   Room card
   ========================= */

.room-card {
  min-width:
    0;

  padding:
    19px;

  border:
    1px solid
    var(--border);

  border-radius:
    19px;

  background:
    var(--card-bg, #fff);

  box-shadow:
    0 1px 2px
    rgba(15, 23, 42, .025),
    0 8px 28px
    rgba(15, 23, 42, .035);

  transition:
    transform .2s ease,
    border-color .2s ease,
    box-shadow .2s ease,
    background .2s ease;
}

.room-card:hover {
  border-color:
    rgba(var(--primary-rgb), .3);

  box-shadow:
    0 4px 8px
    rgba(15, 23, 42, .035),
    0 14px 35px
    rgba(15, 23, 42, .07);

  transform:
    translateY(-2px);
}

.room-card-current {
  border-color:
    rgba(var(--primary-rgb), .35);

  box-shadow:
    0 0 0 1px
    rgba(var(--primary-rgb), .07),
    0 10px 32px
    rgba(var(--primary-rgb), .07);
}

/* =========================
   Card top
   ========================= */

.room-card-top {
  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    10px;

  margin-bottom:
    15px;
}

.room-icon {
  width:
    45px;

  height:
    45px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border-radius:
    13px;
}

.room-icon svg {
  width:
    22px;

  height:
    22px;
}

.room-statuses {
  display:
    flex;

  align-items:
    center;

  gap:
    6px;
}

.online-badge,
.privacy-badge,
.you-badge {
  display:
    inline-flex;

  align-items:
    center;

  gap:
    5px;

  border-radius:
    999px;

  font-size:
    9px;

  font-weight:
    700;
}

.online-badge {
  padding:
    5px 8px;

  background:
    rgba(16, 185, 129, .1);

  color:
    #10b981;
}

.online-badge > span {
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
    rgba(16, 185, 129, .1);
}

.privacy-badge {
  padding:
    5px 8px;

  background:
    rgba(var(--primary-rgb), .08);

  color:
    var(--primary);
}

.privacy-badge svg {
  width:
    11px;

  height:
    11px;
}

/* =========================
   Title
   ========================= */

.room-title-area {
  display:
    flex;

  align-items:
    center;

  gap:
    7px;

  min-width:
    0;

  margin-bottom:
    6px;
}

.room-card h3 {
  min-width:
    0;

  overflow:
    hidden;

  margin:
    0;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;

  font-size:
    16px;

  font-weight:
    800;
}

.you-badge {
  flex-shrink:
    0;

  padding:
    4px 7px;

  background:
    rgba(var(--primary-rgb), .1);

  color:
    var(--primary);
}

/* =========================
   Description
   ========================= */

.room-description {
  min-height:
    42px;

  margin:
    0;

  color:
    var(--text-muted);

  font-size:
    11px;

  line-height:
    1.85;

  display:
    -webkit-box;

  -webkit-line-clamp:
    2;

  -webkit-box-orient:
    vertical;

  overflow:
    hidden;
}

/* =========================
   Details
   ========================= */

.room-details {
  display:
    grid;

  grid-template-columns:
    repeat(3, minmax(0, 1fr));

  gap:
    8px;

  margin-top:
    17px;

  padding-top:
    15px;

  border-top:
    1px solid
    var(--border);
}

.detail-item {
  display:
    flex;

  align-items:
    center;

  gap:
    7px;

  min-width:
    0;
}

.detail-icon {
  width:
    31px;

  height:
    31px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border-radius:
    9px;

  background:
    rgba(var(--primary-rgb), .07);

  color:
    var(--primary);
}

.detail-icon svg {
  width:
    15px;

  height:
    15px;
}

.detail-text {
  display:
    flex;

  flex-direction:
    column;

  min-width:
    0;
}

.detail-text strong {
  overflow:
    hidden;

  color:
    var(--text-main);

  font-size:
    10px;

  font-weight:
    800;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;
}

.detail-text span {
  overflow:
    hidden;

  color:
    var(--text-muted);

  font-size:
    8px;

  text-overflow:
    ellipsis;

  white-space:
    nowrap;
}

.occupancy.high .detail-icon {
  background:
    rgba(239, 68, 68, .1);

  color:
    #ef4444;
}

.occupancy.high .detail-text strong {
  color:
    #ef4444;
}

.occupancy.medium .detail-icon {
  background:
    rgba(245, 158, 11, .1);

  color:
    #f59e0b;
}

.occupancy.medium .detail-text strong {
  color:
    #f59e0b;
}

/* =========================
   Members
   ========================= */

.room-members-row {
  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    10px;

  margin-top:
    15px;
}

.members-left {
  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  min-width:
    0;
}

.avatars {
  display:
    flex;

  direction:
    ltr;

  flex-shrink:
    0;
}

.avatar {
  width:
    27px;

  height:
    27px;

  display:
    grid;

  place-items:
    center;

  margin-left:
    -7px;

  border:
    2px solid
    var(--card-bg, #fff);

  border-radius:
    50%;

  background:
    var(--primary-100);

  color:
    var(--primary);

  font-size:
    9px;

  font-weight:
    800;
}

.avatar:first-child {
  margin-left:
    0;
}

.avatar.more {
  background:
    #f1f5f9;

  color:
    #64748b;
}

.no-members {
  padding:
    5px 8px;

  border-radius:
    999px;

  background:
    rgba(var(--primary-rgb), .06);

  color:
    var(--text-muted);

  font-size:
    8px;
}

.members-label,
.capacity-label {
  color:
    var(--text-muted);

  font-size:
    9px;

  white-space:
    nowrap;
}

.capacity-label {
  flex-shrink:
    0;
}

/* =========================
   Join
   ========================= */

.join-button {
  width:
    100%;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    7px;

  margin-top:
    16px;

  padding:
    10px 14px;

  border:
    1px solid
    rgba(var(--primary-rgb), .15);

  border-radius:
    10px;

  background:
    rgba(var(--primary-rgb), .06);

  color:
    var(--primary);

  font-family:
    inherit;

  font-size:
    11px;

  font-weight:
    750;

  cursor:
    pointer;

  transition:
    background .2s ease,
    color .2s ease,
    border-color .2s ease,
    opacity .2s ease,
    transform .2s ease;
}

.join-button:hover:not(:disabled) {
  background:
    var(--primary);

  border-color:
    var(--primary);

  color:
    #fff;

  transform:
    translateY(-1px);
}

.join-button:disabled {
  opacity:
    .58;

  cursor:
    not-allowed;

  transform:
    none;
}

.join-button-current {
  background:
    rgba(var(--primary-rgb), .1);

  border-color:
    rgba(var(--primary-rgb), .22);
}

.join-button-disabled {
  background:
    rgba(100, 116, 139, .06);

  border-color:
    var(--border);

  color:
    var(--text-muted);
}

.join-button svg {
  width:
    15px;

  height:
    15px;
}

/* =========================
   Empty
   ========================= */

.empty-state {
  grid-column:
    1 / -1;

  padding:
    65px 20px;

  text-align:
    center;
}

.empty-icon {
  width:
    56px;

  height:
    56px;

  display:
    grid;

  place-items:
    center;

  margin:
    0 auto 14px;

  border-radius:
    16px;

  background:
    rgba(var(--primary-rgb), .08);

  color:
    var(--primary);
}

.empty-icon svg {
  width:
    25px;

  height:
    25px;
}

.empty-state h3 {
  margin:
    0 0 6px;

  font-size:
    16px;

  font-weight:
    800;
}

.empty-state p {
  margin:
    0 auto 15px;

  max-width:
    350px;

  color:
    var(--text-muted);

  font-size:
    11px;

  line-height:
    1.8;
}

.empty-action {
  border:
    0;

  border-radius:
    9px;

  padding:
    9px 14px;

  background:
    rgba(var(--primary-rgb), .09);

  color:
    var(--primary);

  font-family:
    inherit;

  font-size:
    11px;

  font-weight:
    700;

  cursor:
    pointer;
}

/* =========================
   Modal
   ========================= */

.modal-backdrop {
  position:
    fixed;

  z-index:
    2000;

  inset:
    0;

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  padding:
    20px;

  background:
    rgba(15, 23, 42, .55);

  backdrop-filter:
    blur(6px);

  -webkit-backdrop-filter:
    blur(6px);
}

.modal-card {
  width:
    min(480px, 100%);

  max-height:
    calc(100vh - 40px);

  overflow-y:
    auto;

  padding:
    22px;

  border:
    1px solid
    var(--border);

  border-radius:
    20px;

  background:
    var(--card-bg, #fff);

  color:
    var(--text-main);

  box-shadow:
    0 25px 80px
    rgba(15, 23, 42, .2);
}

.modal-header {
  display:
    flex;

  align-items:
    flex-start;

  justify-content:
    space-between;

  gap:
    15px;

  margin-bottom:
    22px;
}

.modal-eyebrow {
  margin-bottom:
    4px;

  color:
    var(--primary);

  font-size:
    10px;

  font-weight:
    750;
}

.modal-header h2 {
  margin:
    0 0 5px;

  font-size:
    19px;

  font-weight:
    800;
}

.modal-header p {
  margin:
    0;

  color:
    var(--text-muted);

  font-size:
    11px;
}

.modal-close {
  width:
    34px;

  height:
    34px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border:
    0;

  border-radius:
    9px;

  background:
    transparent;

  color:
    var(--text-muted);

  cursor:
    pointer;

  transition:
    background .2s ease,
    color .2s ease;
}

.modal-close:hover {
  background:
    rgba(var(--primary-rgb), .08);

  color:
    var(--text-main);
}

.modal-close svg {
  width:
    18px;

  height:
    18px;
}

.modal-card form {
  display:
    flex;

  flex-direction:
    column;

  gap:
    15px;
}

.modal-card label {
  display:
    flex;

  flex-direction:
    column;

  gap:
    7px;

  color:
    var(--text-main);

  font-size:
    11px;

  font-weight:
    700;
}

.modal-card label > span {
  font-size:
    11px;
}

.modal-card input,
.modal-card textarea {
  width:
    100%;

  box-sizing:
    border-box;

  border:
    1px solid
    var(--border);

  border-radius:
    10px;

  padding:
    11px 12px;

  outline:
    none;

  background:
    var(--card-bg, #fff);

  color:
    var(--text-main);

  font-family:
    inherit;

  font-size:
    11px;

  resize:
    vertical;

  transition:
    border-color .2s ease,
    box-shadow .2s ease,
    background .2s ease;
}

.modal-card input::placeholder,
.modal-card textarea::placeholder {
  color:
    var(--text-muted);
}

.modal-card input:focus,
.modal-card textarea:focus {
  border-color:
    var(--primary-300);

  box-shadow:
    0 0 0 3px
    rgba(var(--primary-rgb), .07);
}

.capacity-input-wrapper {
  position:
    relative;
}

.capacity-input-wrapper input {
  padding-left:
    45px;
}

.capacity-input-wrapper > span {
  position:
    absolute;

  left:
    13px;

  top:
    50%;

  transform:
    translateY(-50%);

  color:
    var(--text-muted);

  font-size:
    10px;

  font-weight:
    600;

  pointer-events:
    none;
}

.checkbox-label {
  flex-direction:
    row !important;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    15px;

  padding:
    12px;

  border:
    1px solid
    var(--border);

  border-radius:
    10px;
}

.checkbox-info {
  display:
    flex;

  flex-direction:
    column;

  gap:
    3px;
}

.checkbox-info strong {
  font-size:
    11px;
}

.checkbox-info small {
  color:
    var(--text-muted);

  font-size:
    9px;

  font-weight:
    500;

  line-height:
    1.6;
}

.checkbox-label input {
  width:
    18px;

  height:
    18px;

  flex-shrink:
    0;

  accent-color:
    var(--primary);

  cursor:
    pointer;
}

.modal-actions {
  display:
    flex;

  justify-content:
    flex-end;

  gap:
    9px;

  margin-top:
    5px;
}

/* =========================
   Toast
   ========================= */

.toast {
  position:
    fixed;

  z-index:
    3000;

  left:
    50%;

  bottom:
    100px;

  transform:
    translateX(-50%);

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  max-width:
    calc(100vw - 30px);

  padding:
    11px 15px;

  border:
    1px solid
    rgba(255, 255, 255, .08);

  border-radius:
    11px;

  background:
    rgba(15, 23, 42, .96);

  color:
    #fff;

  font-size:
    11px;

  box-shadow:
    0 12px 35px
    rgba(15, 23, 42, .22);
}

.toast-icon {
  width:
    20px;

  height:
    20px;

  display:
    grid;

  place-items:
    center;

  flex-shrink:
    0;

  border-radius:
    50%;

  background:
    rgba(255, 255, 255, .1);
}

.toast-icon svg {
  width:
    12px;

  height:
    12px;
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
    translate(-50%, 10px);
}

/* =========================
   Dark Mode — robust
   ========================= */

/*
 * این صفحه به‌تنهایی به متغیرهای تم وابسته نیست.
 * بنابراین در دارک‌مود، تمام رنگ‌های اصلی کامپوننت همین‌جا
 * مقداردهی می‌شوند تا اگر تم در html، body یا wrapper فعال شد،
 * هیچ بخش سفیدی باقی نماند.
 */
:global(html.dark) .rooms-page,
:global(body.dark) .rooms-page,
:global(html[data-theme="dark"]) .rooms-page,
:global(body[data-theme="dark"]) .rooms-page,
:global(html.dark-mode) .rooms-page,
:global(body.dark-mode) .rooms-page {
  --app-bg: #070b14;
  --card-bg: #111827;
  --surface-bg: #0d1422;
  --surface-hover: #151f31;
  --border: #273449;
  --border-strong: #334155;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-soft: #64748b;
  --primary: #8b7cf6;
  --primary-hover: #9b8df8;
  --primary-50: #111827;
  --primary-100: #1e293b;
  --primary-300: #a79df9;
  --primary-rgb: 139, 124, 246;

  color-scheme: dark;

  background:
    linear-gradient(
      180deg,
      #070b14 0%,
      #0b1120 68%,
      #10172a 100%
    );

  color: var(--text-main);
}

:global(html.dark) .rooms-page::selection,
:global(body.dark) .rooms-page::selection,
:global(html[data-theme="dark"]) .rooms-page::selection,
:global(body[data-theme="dark"]) .rooms-page::selection,
:global(html.dark-mode) .rooms-page::selection,
:global(body.dark-mode) .rooms-page::selection {
  background: rgba(var(--primary-rgb), .28);
  color: #fff;
}

/* Shared dark surfaces */
:global(html.dark) .room-card,
:global(body.dark) .room-card,
:global(html[data-theme="dark"]) .room-card,
:global(body[data-theme="dark"]) .room-card,
:global(html.dark-mode) .room-card,
:global(body.dark-mode) .room-card,

:global(html.dark) .search-box,
:global(body.dark) .search-box,
:global(html[data-theme="dark"]) .search-box,
:global(body[data-theme="dark"]) .search-box,
:global(html.dark-mode) .search-box,
:global(body.dark-mode) .search-box,

:global(html.dark) .icon-button,
:global(body.dark) .icon-button,
:global(html[data-theme="dark"]) .icon-button,
:global(body[data-theme="dark"]) .icon-button,
:global(html.dark-mode) .icon-button,
:global(body.dark-mode) .icon-button,

:global(html.dark) .modal-card,
:global(body.dark) .modal-card,
:global(html[data-theme="dark"]) .modal-card,
:global(body[data-theme="dark"]) .modal-card,
:global(html.dark-mode) .modal-card,
:global(body.dark-mode) .modal-card {
  --card-bg: #111827;

  background: #111827;
  border-color: #273449;
  color: #f8fafc;
}

:global(html.dark) .room-card,
:global(body.dark) .room-card,
:global(html[data-theme="dark"]) .room-card,
:global(body[data-theme="dark"]) .room-card,
:global(html.dark-mode) .room-card,
:global(body.dark-mode) .room-card {
  box-shadow:
    0 1px 2px rgba(0, 0, 0, .16),
    0 10px 30px rgba(0, 0, 0, .20);
}

:global(html.dark) .room-card:hover,
:global(body.dark) .room-card:hover,
:global(html[data-theme="dark"]) .room-card:hover,
:global(body[data-theme="dark"]) .room-card:hover,
:global(html.dark-mode) .room-card:hover,
:global(body.dark-mode) .room-card:hover {
  background: #141d2d;
  border-color: rgba(var(--primary-rgb), .42);
  box-shadow:
    0 10px 25px rgba(0, 0, 0, .22),
    0 18px 45px rgba(0, 0, 0, .18);
}

:global(html.dark) .room-card-current,
:global(body.dark) .room-card-current,
:global(html[data-theme="dark"]) .room-card-current,
:global(body[data-theme="dark"]) .room-card-current,
:global(html.dark-mode) .room-card-current,
:global(body.dark-mode) .room-card-current {
  border-color: rgba(var(--primary-rgb), .48);
  box-shadow:
    0 0 0 1px rgba(var(--primary-rgb), .10),
    0 14px 38px rgba(0, 0, 0, .22);
}

/* Header / secondary text */
:global(html.dark) .page-header p,
:global(body.dark) .page-header p,
:global(html[data-theme="dark"]) .page-header p,
:global(body[data-theme="dark"]) .page-header p,
:global(html.dark-mode) .page-header p,
:global(body.dark-mode) .page-header p,

:global(html.dark) .create-card p,
:global(body.dark) .create-card p,
:global(html[data-theme="dark"]) .create-card p,
:global(body[data-theme="dark"]) .create-card p,
:global(html.dark-mode) .create-card p,
:global(body.dark-mode) .create-card p,

:global(html.dark) .current-room-content p,
:global(body.dark) .current-room-content p,
:global(html[data-theme="dark"]) .current-room-content p,
:global(body[data-theme="dark"]) .current-room-content p,
:global(html.dark-mode) .current-room-content p,
:global(body.dark-mode) .current-room-content p,

:global(html.dark) .room-description,
:global(body.dark) .room-description,
:global(html[data-theme="dark"]) .room-description,
:global(body[data-theme="dark"]) .room-description,
:global(html.dark-mode) .room-description,
:global(body.dark-mode) .room-description,

:global(html.dark) .section-heading p,
:global(body.dark) .section-heading p,
:global(html[data-theme="dark"]) .section-heading p,
:global(body[data-theme="dark"]) .section-heading p,
:global(html.dark-mode) .section-heading p,
:global(body.dark-mode) .section-heading p,

:global(html.dark) .members-label,
:global(body.dark) .members-label,
:global(html[data-theme="dark"]) .members-label,
:global(body[data-theme="dark"]) .members-label,
:global(html.dark-mode) .members-label,
:global(body.dark-mode) .members-label,

:global(html.dark) .capacity-label,
:global(body.dark) .capacity-label,
:global(html[data-theme="dark"]) .capacity-label,
:global(body[data-theme="dark"]) .capacity-label,
:global(html.dark-mode) .capacity-label,
:global(body.dark-mode) .capacity-label,

:global(html.dark) .detail-text span,
:global(body.dark) .detail-text span,
:global(html[data-theme="dark"]) .detail-text span,
:global(body[data-theme="dark"]) .detail-text span,
:global(html.dark-mode) .detail-text span,
:global(body.dark-mode) .detail-text span {
  color: #94a3b8;
}

:global(html.dark) .detail-text strong,
:global(body.dark) .detail-text strong,
:global(html[data-theme="dark"]) .detail-text strong,
:global(body[data-theme="dark"]) .detail-text strong,
:global(html.dark-mode) .detail-text strong,
:global(body.dark-mode) .detail-text strong,

:global(html.dark) .room-card h3,
:global(body.dark) .room-card h3,
:global(html[data-theme="dark"]) .room-card h3,
:global(body[data-theme="dark"]) .room-card h3,
:global(html.dark-mode) .room-card h3,
:global(body.dark-mode) .room-card h3,

:global(html.dark) .section-heading h2,
:global(body.dark) .section-heading h2,
:global(html[data-theme="dark"]) .section-heading h2,
:global(body[data-theme="dark"]) .section-heading h2,
:global(html.dark-mode) .section-heading h2,
:global(body.dark-mode) .section-heading h2 {
  color: #f8fafc;
}

/* Current room / create room */
:global(html.dark) .current-room-card,
:global(body.dark) .current-room-card,
:global(html[data-theme="dark"]) .current-room-card,
:global(body[data-theme="dark"]) .current-room-card,
:global(html.dark-mode) .current-room-card,
:global(body.dark-mode) .current-room-card {
  background:
    linear-gradient(
      135deg,
      rgba(var(--primary-rgb), .17),
      rgba(var(--primary-rgb), .055)
    );
  border-color: rgba(var(--primary-rgb), .28);
}

:global(html.dark) .create-card,
:global(body.dark) .create-card,
:global(html[data-theme="dark"]) .create-card,
:global(body[data-theme="dark"]) .create-card,
:global(html.dark-mode) .create-card,
:global(body.dark-mode) .create-card {
  background:
    linear-gradient(
      135deg,
      rgba(var(--primary-rgb), .14),
      rgba(var(--primary-rgb), .035)
    );
  border-color: rgba(var(--primary-rgb), .25);
}

/* Inputs */
:global(html.dark) .search-box,
:global(body.dark) .search-box,
:global(html[data-theme="dark"]) .search-box,
:global(body[data-theme="dark"]) .search-box,
:global(html.dark-mode) .search-box,
:global(body.dark-mode) .search-box {
  background: #0f1726;
  border-color: #29364a;
}

:global(html.dark) .search-box:focus-within,
:global(body.dark) .search-box:focus-within,
:global(html[data-theme="dark"]) .search-box:focus-within,
:global(body[data-theme="dark"]) .search-box:focus-within,
:global(html.dark-mode) .search-box:focus-within,
:global(body.dark-mode) .search-box:focus-within {
  border-color: var(--primary-300);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), .13);
}

:global(html.dark) .search-box input,
:global(body.dark) .search-box input,
:global(html[data-theme="dark"]) .search-box input,
:global(body[data-theme="dark"]) .search-box input,
:global(html.dark-mode) .search-box input,
:global(body.dark-mode) .search-box input,
:global(html.dark) .modal-card input,
:global(body.dark) .modal-card input,
:global(html[data-theme="dark"]) .modal-card input,
:global(body[data-theme="dark"]) .modal-card input,
:global(html.dark-mode) .modal-card input,
:global(body.dark-mode) .modal-card input,
:global(html.dark) .modal-card textarea,
:global(body.dark) .modal-card textarea,
:global(html[data-theme="dark"]) .modal-card textarea,
:global(body[data-theme="dark"]) .modal-card textarea,
:global(html.dark-mode) .modal-card textarea,
:global(body.dark-mode) .modal-card textarea {
  background: #0b1220;
  border-color: #334155;
  color: #f8fafc;
  color-scheme: dark;
}

:global(html.dark) .modal-card input:focus,
:global(body.dark) .modal-card input:focus,
:global(html[data-theme="dark"]) .modal-card input:focus,
:global(body[data-theme="dark"]) .modal-card input:focus,
:global(html.dark-mode) .modal-card input:focus,
:global(body.dark-mode) .modal-card input:focus,
:global(html.dark) .modal-card textarea:focus,
:global(body.dark) .modal-card textarea:focus,
:global(html[data-theme="dark"]) .modal-card textarea:focus,
:global(body[data-theme="dark"]) .modal-card textarea:focus,
:global(html.dark-mode) .modal-card textarea:focus,
:global(body.dark-mode) .modal-card textarea:focus {
  border-color: var(--primary-300);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), .12);
}

:global(html.dark) .modal-card input::placeholder,
:global(body.dark) .modal-card input::placeholder,
:global(html[data-theme="dark"]) .modal-card input::placeholder,
:global(body[data-theme="dark"]) .modal-card input::placeholder,
:global(html.dark-mode) .modal-card input::placeholder,
:global(body.dark-mode) .modal-card input::placeholder,
:global(html.dark) .modal-card textarea::placeholder,
:global(body.dark) .modal-card textarea::placeholder,
:global(html[data-theme="dark"]) .modal-card textarea::placeholder,
:global(body[data-theme="dark"]) .modal-card textarea::placeholder,
:global(html.dark-mode) .modal-card textarea::placeholder,
:global(body.dark-mode) .modal-card textarea::placeholder,
:global(html.dark) .search-box input::placeholder,
:global(body.dark) .search-box input::placeholder,
:global(html[data-theme="dark"]) .search-box input::placeholder,
:global(body[data-theme="dark"]) .search-box input::placeholder,
:global(html.dark-mode) .search-box input::placeholder,
:global(body.dark-mode) .search-box input::placeholder {
  color: #64748b;
  opacity: 1;
}

/* Avatars */
:global(html.dark) .avatar,
:global(body.dark) .avatar,
:global(html[data-theme="dark"]) .avatar,
:global(body[data-theme="dark"]) .avatar,
:global(html.dark-mode) .avatar,
:global(body.dark-mode) .avatar {
  border-color: #111827;
  background: #1e293b;
  color: var(--primary-300);
}

:global(html.dark) .avatar.more,
:global(body.dark) .avatar.more,
:global(html[data-theme="dark"]) .avatar.more,
:global(body[data-theme="dark"]) .avatar.more,
:global(html.dark-mode) .avatar.more,
:global(body.dark-mode) .avatar.more {
  background: #1e293b;
  color: #94a3b8;
}

/* Borders / neutral controls */
:global(html.dark) .room-details,
:global(body.dark) .room-details,
:global(html[data-theme="dark"]) .room-details,
:global(body[data-theme="dark"]) .room-details,
:global(html.dark-mode) .room-details,
:global(body.dark-mode) .room-details,

:global(html.dark) .checkbox-label,
:global(body.dark) .checkbox-label,
:global(html[data-theme="dark"]) .checkbox-label,
:global(body[data-theme="dark"]) .checkbox-label,
:global(html.dark-mode) .checkbox-label,
:global(body.dark-mode) .checkbox-label {
  border-color: #334155;
}

:global(html.dark) .secondary-button,
:global(body.dark) .secondary-button,
:global(html[data-theme="dark"]) .secondary-button,
:global(body[data-theme="dark"]) .secondary-button,
:global(html.dark-mode) .secondary-button,
:global(body.dark-mode) .secondary-button {
  border-color: #334155;
  background: #111827;
  color: #e2e8f0;
}

:global(html.dark) .secondary-button:hover,
:global(body.dark) .secondary-button:hover,
:global(html[data-theme="dark"]) .secondary-button:hover,
:global(body[data-theme="dark"]) .secondary-button:hover,
:global(html.dark-mode) .secondary-button:hover,
:global(body.dark-mode) .secondary-button:hover {
  border-color: var(--primary-300);
  background: #182235;
  color: var(--primary-300);
}

:global(html.dark) .join-button-disabled,
:global(body.dark) .join-button-disabled,
:global(html[data-theme="dark"]) .join-button-disabled,
:global(body[data-theme="dark"]) .join-button-disabled,
:global(html.dark-mode) .join-button-disabled,
:global(body.dark-mode) .join-button-disabled {
  background: rgba(100, 116, 139, .10);
  border-color: #334155;
  color: #64748b;
}

/* Modal backdrop and dialog */
:global(html.dark) .modal-backdrop,
:global(body.dark) .modal-backdrop,
:global(html[data-theme="dark"]) .modal-backdrop,
:global(body[data-theme="dark"]) .modal-backdrop,
:global(html.dark-mode) .modal-backdrop,
:global(body.dark-mode) .modal-backdrop {
  background: rgba(2, 6, 23, .72);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

:global(html.dark) .modal-card,
:global(body.dark) .modal-card,
:global(html[data-theme="dark"]) .modal-card,
:global(body[data-theme="dark"]) .modal-card,
:global(html.dark-mode) .modal-card,
:global(body.dark-mode) .modal-card {
  background: #111827;
  border-color: #2b384c;
  box-shadow: 0 28px 90px rgba(0, 0, 0, .42);
}

/* Native checkbox/range-like controls should follow dark UI */
:global(html.dark) .modal-card input[type="checkbox"],
:global(body.dark) .modal-card input[type="checkbox"],
:global(html[data-theme="dark"]) .modal-card input[type="checkbox"],
:global(body[data-theme="dark"]) .modal-card input[type="checkbox"],
:global(html.dark-mode) .modal-card input[type="checkbox"],
:global(body.dark-mode) .modal-card input[type="checkbox"] {
  accent-color: var(--primary);
}

/* Keep toast readable above every dark surface */
:global(html.dark) .toast,
:global(body.dark) .toast,
:global(html[data-theme="dark"]) .toast,
:global(body[data-theme="dark"]) .toast,
:global(html.dark-mode) .toast,
:global(body.dark-mode) .toast {
  background: #182235;
  color: #f8fafc;
  border: 1px solid #334155;
  box-shadow: 0 16px 42px rgba(0, 0, 0, .35);
}

/* =========================
   Responsive
   ========================= */

@media (max-width: 820px) {
  .rooms-grid {
    grid-template-columns:
      1fr;
  }
}

@media (max-width: 650px) {
  .rooms-page {
    padding:
      23px
      14px
      125px;
  }

  .current-room-card {
    align-items:
      flex-start;

    flex-wrap:
      wrap;
  }

  .current-room-content {
    width:
      calc(100% - 64px);

    flex:
      none;
  }

  .current-room-button {
    width:
      100%;
  }

  .create-card {
    align-items:
      flex-start;

    flex-wrap:
      wrap;
  }

  .create-card-content {
    min-width:
      calc(100% - 70px);
  }

  .create-card .primary-button {
    width:
      100%;
  }

  .room-details {
    grid-template-columns:
      repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 430px) {
  .page-header h1 {
    font-size:
      26px;
  }

  .page-header p {
    font-size:
      11px;
  }

  .room-card {
    padding:
      16px;
  }

  .room-details {
    gap:
      5px;
  }

  .detail-icon {
    width:
      28px;

    height:
      28px;
  }

  .detail-icon svg {
    width:
      14px;

    height:
      14px;
  }

  .detail-text strong {
    font-size:
      9px;
  }

  .members-label {
    display:
      none;
  }

  .capacity-label {
    font-size:
      8px;
    }
  }

  .modal-card {
    padding:
      18px;
  }

</style>