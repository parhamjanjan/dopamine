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
      'ساخت سالن با خطا مواجه شد. در صورت عضویت در سالن دیگر ابتدا از آن خارج شوید'
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

<style src="../assets/room.css" scoped> </style>