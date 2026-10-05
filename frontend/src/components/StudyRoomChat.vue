<template>
  <section
    ref="chatRootEl"
    class="room-chat"
    :class="{ 'is-dark': isDark }"
    @click="handleRoomClick"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- ═══════════════════════════════════════════════════
         INTERACTIVE MOUSE-REACTIVE BACKGROUND
         ═══════════════════════════════════════════════════ -->
    <div class="chat-ambient" aria-hidden="true">
      <!-- Base gradient -->
      <div class="bg-base"></div>

      <!-- Mouse-following spotlight -->
      <div
        class="mouse-spotlight"
        :style="{
          transform: `translate3d(${mouse.x}px, ${mouse.y}px, 0)`
        }"
      ></div>

      <!-- Floating gradient orbs that react to mouse -->
      <div
        class="react-orb react-orb-1"
        :style="getOrbStyle(0.04, -0.03)"
      ></div>
      <div
        class="react-orb react-orb-2"
        :style="getOrbStyle(-0.05, 0.04)"
      ></div>
      <div
        class="react-orb react-orb-3"
        :style="getOrbStyle(0.03, 0.05)"
      ></div>
      <div
        class="react-orb react-orb-4"
        :style="getOrbStyle(-0.04, -0.04)"
      ></div>

      <!-- Mesh gradient that shifts with mouse -->
      <div
        class="mesh-gradient"
        :style="{
          transform: `translate3d(${mouse.x * 0.02}px, ${mouse.y * 0.02}px, 0)`
        }"
      ></div>

      <!-- Interactive particle field -->
      <div class="particle-field">
        <span
          v-for="n in 18"
          :key="n"
          class="field-particle"
          :style="getParticleStyle(n)"
        ></span>
      </div>

      <!-- Subtle grid that reacts to mouse -->
      <div
        class="ambient-grid"
        :style="{
          transform: `perspective(800px) rotateX(58deg) translate3d(${mouse.x * 0.015}px, calc(-12% + ${mouse.y * 0.01}px), 0)`
        }"
      ></div>

      <!-- Noise overlay -->
      <div class="bg-noise"></div>

      <!-- Soft vignette -->
      <div class="vignette"></div>
    </div>

    <header class="chat-header">
      <div class="chat-title">
        <div class="chat-title-mark">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
            <path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5 8.3 8.3 0 0 1-3.1-.6L4 20l1.6-4.2A7.5 7.5 0 1 1 20 11.5Z"/>
            <path d="M8 10h8M8 14h5"/>
          </svg>
        </div>
        <div>
          <strong>گفت‌وگوی سالن</strong>
          <span>محیطی برای ارتباط و همراهی</span>
        </div>
      </div>

      <div class="chat-header-tools">
        <label class="chat-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <circle cx="11" cy="11" r="6.5"/><path d="m16 16 5 5"/>
          </svg>
          <input v-model="searchQuery" type="search" placeholder="جستجو در گفتگو..." aria-label="جستجو در گفتگو" />
          <button v-if="searchQuery" type="button" @click="searchQuery = ''" aria-label="پاک کردن جستجو">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m7 7 10 10M17 7 7 17"/></svg>
          </button>
        </label>

        <button type="button" class="header-icon-button" @click.stop="showPinnedOnly = !showPinnedOnly" :class="{ active: showPinnedOnly }" title="پیام‌های سنجاق‌شده" aria-label="پیام‌های سنجاق‌شده">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m15 4 5 5-3 1-4 4v5l-2 2-1-7-4-4 3-1 4-4Z"/><path d="m4 20 6-6"/></svg>
          <span v-if="pinnedCount">{{ pinnedCount }}</span>
        </button>

        <button type="button" class="header-icon-button" @click.stop="clearNotifications" title="پاک کردن اعلان‌ها" aria-label="اعلان‌ها">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></svg>
          <span v-if="notifications.length">{{ notifications.length }}</span>
        </button>
      </div>

      <div class="room-chat-badge" :class="socketConnected ? 'online' : 'offline'">
        <span class="room-chat-badge-dot"></span>
        <span>{{ socketConnected ? 'اتصال پایدار' : 'در حال اتصال...' }}</span>
      </div>
    </header>

    <div class="chat-body">
      <div ref="messagesEl" class="messages custom-scrollbar" role="log" aria-live="polite">
        <div v-if="loadingHistory" class="chat-state">
          <span class="mini-loader"></span>
          <span>در حال دریافت پیام‌ها...</span>
        </div>

        <div v-else-if="messages.length === 0" class="empty-chat">
          <div class="empty-chat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
              <path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5 8.3 8.3 0 0 1-3.1-.6L4 20l1.6-4.2A7.5 7.5 0 1 1 20 11.5Z"/>
              <path d="M8 10h8M8 14h5"/>
            </svg>
          </div>
          <h3>گفت‌وگو هنوز شروع نشده</h3>
          <p>اولین پیام را بفرست و فضای سالن را زنده کن.</p>
          <button type="button" class="empty-chat-action" @click.stop="inputEl?.focus()">
            شروع گفتگو
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m5 12 14 0"/><path d="m13 6 6 6-6 6"/></svg>
          </button>
        </div>

        <template v-else>
          <template v-for="(message, index) in visibleMessages" :key="getMessageKey(message)">
            <div v-if="shouldShowDateDivider(index)" class="date-divider">
              <span class="date-divider-line"></span>
              <span class="date-divider-text">{{ getDateLabel(message.createdAt) }}</span>
              <span class="date-divider-line"></span>
            </div>

            <article
              :data-message-id="message.messageId"
              class="message-row"
              :class="{
                mine: message.isMine,
                deleted: message.isDeleted,
                admin: message.isStaff === true,
                pinned: isPinned(message),
                highlighted: searchQuery && message.text.toLowerCase().includes(searchQuery.toLowerCase()),
                consecutive: isConsecutive(index)
              }"
              @contextmenu.prevent.stop="openMessageMenu($event, message)"
              @touchstart="startLongPress($event, message)"
              @touchend="cancelLongPress"
              @touchmove="cancelLongPress"
            >
              <div
                class="message-avatar"
                :class="{
                  mine: message.isMine,
                  admin: message.isStaff === true,
                  invisible: isConsecutive(index)
                }"
              >
                <template v-if="message.isStaff === true">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m3 7 4.2 3.5L12 4l4.8 6.5L21 7l-2 13H5L3 7Z"/><path d="M5 20h14"/></svg>
                </template>
                <template v-else>{{ getInitial(message.username) }}</template>
              </div>

              <div class="message-content">
                <div v-if="message.isStaff === true && !isConsecutive(index)" class="admin-badge">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m3 7 4.2 3.5L12 4l4.8 6.5L21 7l-2 13H5L3 7Z"/><path d="M5 20h14"/></svg>
                  <span>ادمین وبسایت</span>
                </div>

                <div class="message-meta" :class="{ 'has-admin-badge': message.isStaff === true && !isConsecutive(index), invisible: isConsecutive(index) }">
                  <strong>{{ message.isStaff === true ? message.username : (message.isMine ? 'شما' : message.username) }}</strong>
                  <time>{{ formatTime(message.createdAt) }}</time>
                  <svg v-if="message.isMine && !message.isDeleted" class="message-status" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m4 12 4 4L20 5"/><path d="m8 17 4 3 8-10"/></svg>
                </div>

                <div
                  v-if="message.replyTo"
                  class="message-reply-preview"
                  :class="{ 'reply-from-admin': message.replyTo.isStaff === true }"
                  @click.stop="scrollToMessage(message.replyTo.id)"
                >
                  <span class="reply-preview-line"></span>
                  <div class="reply-preview-content">
                    <div class="reply-preview-author">
                      <strong>{{ message.replyTo.username || 'کاربر' }}</strong>
                      <span v-if="message.replyTo.isStaff === true" class="reply-admin-badge">ادمین</span>
                    </div>
                    <span>{{ message.replyTo.isDeleted ? 'این پیام حذف شده است' : message.replyTo.message }}</span>
                  </div>
                </div>

                <div class="message-bubble-wrap">
                  <div class="message-bubble" :class="{ deleted: message.isDeleted }">
                    <template v-if="message.isDeleted">
                      <span class="deleted-message">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 3h6M5 6h14m-6 4v5m4-5v5"/><path d="m8 6 .7 13h6.6L16 6"/></svg>
                        این پیام حذف شده است
                      </span>
                    </template>
                    <template v-else>
                      <span class="message-text">{{ message.text }}</span>
                      <span v-if="message.editedAt" class="edited-label">ویرایش‌شده</span>
                    </template>
                  </div>

                  <button v-if="!message.isDeleted" type="button" class="message-more" aria-label="عملیات پیام" title="عملیات پیام" @click.stop="openMessageMenuFromButton($event, message)">
                    <svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.7"/><circle cx="12" cy="12" r="1.7"/><circle cx="19" cy="12" r="1.7"/></svg>
                  </button>
                </div>

                <div v-if="!message.isDeleted && getReactionSummary(message).length" class="message-reactions">
                  <button v-for="reaction in getReactionSummary(message)" :key="reaction.type" type="button" class="reaction-chip" :class="{ selected: reaction.myReaction }" @click.stop="toggleReaction(message, reaction.type)">
                    <span>{{ getReactionEmoji(reaction.type) }}</span><small>{{ reaction.count }}</small>
                  </button>
                </div>
              </div>
            </article>
          </template>
        </template>
      </div>

      <button
        v-if="messages.length && showScrollButton"
        type="button"
        class="scroll-bottom-button"
        aria-label="رفتن به پایین گفتگو"
        title="رفتن به پایین گفتگو"
        @click.stop="scrollToBottomSmooth"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 4v14"/><path d="m6 12 6 6 6-6"/></svg>
        <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
      </button>

      <Transition name="chat-action-bar">
        <div v-if="editingMessage || replyingTo" class="chat-action-bar">
          <div class="chat-action-bar-icon">
            <svg v-if="editingMessage" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 6 6v1"/></svg>
          </div>
          <div class="chat-action-bar-content">
            <strong>{{ editingMessage ? 'ویرایش پیام' : 'پاسخ به پیام' }}</strong>
            <span>{{ editingMessage ? editingMessage.text : (replyingTo?.isDeleted ? 'این پیام حذف شده است' : replyingTo?.text) }}</span>
          </div>
          <button type="button" class="chat-action-bar-close" aria-label="لغو" @click="cancelAction">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m7 7 10 10M17 7 7 17"/></svg>
          </button>
        </div>
      </Transition>

      <div v-if="typingUsers.length" class="typing-indicator">
        <span class="typing-dots"><i></i><i></i><i></i></span>
        <span>{{ typingUsers.join('، ') }} در حال نوشتن است...</span>
      </div>

      <TransitionGroup name="room-toast" tag="div" class="room-notifications">
        <div v-for="item in notifications" :key="item.id" class="room-notification">
          <span class="notification-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></svg>
          </span>
          <div><strong>{{ item.title }}</strong><small>{{ item.text }}</small></div>
        </div>
      </TransitionGroup>

      <form class="chat-composer" @submit.prevent="sendMessage">
        <button type="button" class="composer-tool" :class="{ active: showEmojiPicker }" aria-label="انتخاب ایموجی" title="ایموجی" @click.stop="toggleEmojiPicker">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="8.5"/><path d="M8.5 14.2a4.5 4.5 0 0 0 7 0M9 10h.01M15 10h.01"/></svg>
        </button>

        <textarea ref="inputEl" v-model="draft" class="chat-input" rows="1" maxlength="1000"
          :disabled="sending || !socketConnected"
          :placeholder="editingMessage ? 'متن پیام را ویرایش کن...' : replyingTo ? 'پاسخت را بنویس...' : 'پیامت را برای اعضای سالن بنویس...'"
          @keydown.enter.exact.prevent="sendMessage" @input="handleComposerInput"></textarea>

        <div class="composer-counter" :class="{ danger: draft.length > 900 }">{{ draft.length }}/1000</div>

        <button type="submit" class="send-button" :disabled="sending || !socketConnected || !draft.trim()"
          :aria-label="editingMessage ? 'ذخیره ویرایش' : replyingTo ? 'ارسال پاسخ' : 'ارسال پیام'">
          <span v-if="sending" class="send-loader"></span>
          <svg v-else-if="editingMessage" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m5 12 4 4L19 6"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
        </button>
      </form>

      <Transition name="emoji-pop">
        <div v-if="showEmojiPicker" class="emoji-picker" @click.stop>
          <div class="emoji-picker-head">
            <div>
              <strong>انتخاب ایموجی</strong>
              <span>پیامت را با یک واکنش کامل‌تر کن</span>
            </div>
            <button type="button" class="emoji-close" @click="closeEmojiPicker" aria-label="بستن">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m7 7 10 10M17 7 7 17"/></svg>
            </button>
          </div>

          <label class="emoji-search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 5 5"/></svg>
            <input v-model="emojiSearch" type="search" placeholder="جستجو یا انتخاب از دسته‌ها..." />
          </label>

          <div class="emoji-categories" v-if="!emojiSearch">
            <button v-for="(category, key) in emojiCategories" :key="key" type="button" :class="{ active: emojiCategory === key }" @click="emojiCategory = key" :title="category.label">{{ category.icon }}</button>
          </div>

          <div class="emoji-grid custom-scrollbar">
            <button v-for="(emoji, index) in allEmojiItems" :key="`${emoji}-${index}`" type="button" class="emoji-item" @click="selectEmoji(emoji)" :aria-label="`افزودن ${emoji}`">{{ emoji }}</button>
          </div>
        </div>
      </Transition>
    </div>

    <Transition name="message-menu">
      <div v-if="contextMenu.visible" ref="contextMenuEl" class="message-context-menu" :class="{ 'admin-context-menu': contextMenu.message?.isStaff === true }" :style="contextMenuStyle" @click.stop>
        <div class="context-menu-user">
          <div class="context-menu-avatar" :class="{ admin: contextMenu.message?.isStaff === true }">
            <svg v-if="contextMenu.message?.isStaff === true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m3 7 4.2 3.5L12 4l4.8 6.5L21 7l-2 13H5L3 7Z"/><path d="M5 20h14"/></svg>
            <template v-else>{{ getInitial(contextMenu.message?.username) }}</template>
          </div>
          <div>
            <div class="context-menu-name-row">
              <strong>{{ contextMenu.message?.username || 'کاربر' }}</strong>
              <span v-if="contextMenu.message?.isStaff === true" class="context-admin-label">ادمین</span>
            </div>
            <span>{{ contextMenu.message?.isStaff === true ? 'ادمین وبسایت' : (contextMenu.message?.isMine ? 'پیام شما' : 'پیام کاربر') }}</span>
          </div>
        </div>

        <div class="context-menu-divider"></div>

        <button type="button" class="context-menu-item" @click="replyToMessage(contextMenu.message)">
          <span class="context-menu-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 6 6v1"/></svg></span><span>پاسخ</span>
        </button>

        <button v-if="!contextMenu.message?.isDeleted" type="button" class="context-menu-item" @click="toggleReactionMenu">
          <span class="context-menu-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="8.5"/><path d="M8.5 14.2a4.5 4.5 0 0 0 7 0M9 10h.01M15 10h.01"/></svg></span><span>واکنش</span><span class="context-menu-arrow">‹</span>
        </button>

        <div v-if="contextMenu.showReactions" class="reaction-picker">
          <button v-for="type in reactionTypes" :key="type" type="button" class="reaction-picker-button" :class="{ selected: getUserReaction(contextMenu.message) === type }" :title="getReactionLabel(type)" @click="selectReactionFromMenu(type)">{{ getReactionEmoji(type) }}</button>
        </div>

        <button v-if="contextMenu.message" type="button" class="context-menu-item" @click="togglePin(contextMenu.message)">
          <span class="context-menu-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m15 4 5 5-3 1-4 4v5l-2 2-1-7-4-4 3-1 4-4Z"/><path d="m4 20 6-6"/></svg></span><span>{{ isPinned(contextMenu.message) ? 'برداشتن سنجاق' : 'سنجاق کردن' }}</span>
        </button>

        <button v-if="contextMenu.message && contextMenu.message.isMine && !contextMenu.message.isDeleted" type="button" class="context-menu-item" @click="startEditMessage(contextMenu.message)">
          <span class="context-menu-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"/></svg></span><span>ویرایش</span>
        </button>

        <button v-if="contextMenu.message && contextMenu.message.isMine && !contextMenu.message.isDeleted" type="button" class="context-menu-item danger" @click="deleteMessage(contextMenu.message)">
          <span class="context-menu-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 3h6M5 6h14"/><path d="m8 6 .7 13h6.6L16 6"/><path d="M10 10v5M14 10v5"/></svg></span><span>حذف</span>
        </button>
      </div>
    </Transition>
  </section>
</template>

<script setup>
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'

/* =========================================================
   PROPS
   ========================================================= */

const props = defineProps({
  roomId: {
    type: [String, Number],
    required: true,
  },
})

/* =========================================================
   DOM
   ========================================================= */

const chatRootEl = ref(null)
const messagesEl = ref(null)
const inputEl = ref(null)
const contextMenuEl = ref(null)
const showEmojiPicker = ref(false)
const emojiSearch = ref('')
const emojiCategory = ref('smileys')

/* =========================================================
   MOUSE TRACKING
   ========================================================= */

const mouse = ref({
  x: 0,
  y: 0,
  targetX: 0,
  targetY: 0,
})
let mouseRafId = null
let mouseLoop = null

function handleMouseMove(event) {
  const root = chatRootEl.value
  if (!root) return
  const rect = root.getBoundingClientRect()
  mouse.value.targetX = event.clientX - rect.left
  mouse.value.targetY = event.clientY - rect.top
}

function handleMouseLeave() {
  const root = chatRootEl.value
  if (!root) return
  const rect = root.getBoundingClientRect()
  mouse.value.targetX = rect.width / 2
  mouse.value.targetY = rect.height / 2
}

function startMouseLoop() {
  mouseLoop = () => {
    // Smooth lerp towards target
    mouse.value.x += (mouse.value.targetX - mouse.value.x) * 0.08
    mouse.value.y += (mouse.value.targetY - mouse.value.y) * 0.08
    mouseRafId = requestAnimationFrame(mouseLoop)
  }
  mouseRafId = requestAnimationFrame(mouseLoop)
}

function getOrbStyle(fx, fy) {
  return {
    transform: `translate3d(${mouse.value.x * fx}px, ${mouse.value.y * fy}px, 0)`
  }
}

function getParticleStyle(n) {
  const left = (n * 41 + 11) % 100
  const top = (n * 29 + 17) % 100
  const size = 1.5 + (n % 3)
  const delay = (n * 0.35) % 5
  const duration = 8 + (n % 6)
  return {
    left: left + '%',
    top: top + '%',
    width: size + 'px',
    height: size + 'px',
    animationDelay: delay + 's',
    animationDuration: duration + 's',
  }
}

/* =========================================================
   STATE
   ========================================================= */

const messages = ref([])
const draft = ref('')
const loadingHistory = ref(false)
const sending = ref(false)
const socketConnected = ref(false)
const isDark = ref(false)
const searchQuery = ref('')
const showPinnedOnly = ref(false)
const pinnedIds = ref([])
const notifications = ref([])
const typingUsers = ref([])
const unreadCount = ref(0)
const showScrollButton = ref(false)
let typingTimer = null
let notificationTimer = null

const pinnedCount = computed(() => pinnedIds.value.length)
const visibleMessages = computed(() => {
  let list = messages.value
  if (showPinnedOnly.value) list = list.filter(isPinned)
  const q = searchQuery.value.trim().toLowerCase()
  if (q) list = list.filter(m => (m.text || '').toLowerCase().includes(q) || (m.username || '').toLowerCase().includes(q))
  return list
})

/* =========================================================
   CHAT ACTION STATE
   ========================================================= */

const editingMessage = ref(null)
const replyingTo = ref(null)

/* =========================================================
   CONTEXT MENU
   ========================================================= */

const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  message: null,
  showReactions: false,
})

const contextMenuStyle = ref({})

/* =========================================================
   REACTIONS
   ========================================================= */

const reactionTypes = [
  'cry',
  'laugh',
  'heart',
  'like',
  'dislike',
  'fire',
  'brain',
  'wow',
]

const reactionEmojis = {
  cry: '😢',
  laugh: '😂',
  heart: '❤️',
  like: '👍',
  dislike: '👎',
  fire: '🔥',
  brain: '🧠',
  wow: '🤯',
}

const reactionLabels = {
  cry: 'گریه',
  laugh: 'خنده',
  heart: 'قلب',
  like: 'لایک',
  dislike: 'دیسلایک',
  fire: 'آتش',
  brain: 'مغز',
  wow: 'واو',
}

const emojiCategories = {
  smileys: {
    label: 'لبخندها',
    icon: '☺',
    items: '😀 😃 😄 😁 😆 😅 😂 🤣 😊 😇 🙂 🙃 😉 😌 😍 🥰 😘 😗 😙 😚 😋 😛 😝 😜 🤪 🤨 🧐 🤓 😎 🤩 🥳 😏 😒 😞 😔 😟 😕 🙁 ☹️ 😣 😖 😫 😩 🥺 😢 😭 😤 😠 😡 🤬 🤯 😳 🥵 🥶 😱 😨 😰 😥 😓 🤗 🤔 🫡 🤭 🤫 🤥 😶 😐 😑 😬 🙄 😯 😦 😧 😮 😲 🥱 😴 🤤 😪 😵 🤐 🥴 🤢 🤮 🤧 😷 🤒 🤕 🤑 🤠 😈 👿 👹 👺 🤡 💩 👻 💀 ☠️ 👽 👾 🤖 🎃 😺 😸 😹 😻 😼 😽 🙀 😿 😾'.split(' ')
  },
  people: {
    label: 'افراد',
    icon: '♙',
    items: '👋 🤚 🖐️ ✋ 🖖 👌 🤏 ✌️ 🤞 🤟 🤘 🤙 👈 👉 👆 👇 ☝️ ✍️ 🤳 💪 🖕 🙏 👏 🙌 👐 🤝 ❤️‍🩹 ❤️‍🔥 🫶 💅 👂 👃 🧠 🫀 🫁 🦷 🦴 👀 👁️ 👅 👄 🫦 👶 🧒 👦 👧 🧑 👱 👨 🧔 👨‍🦰 👨‍🦱 👨‍🦳 👨‍🦲 👩 👩‍🦰 👩‍🦱 👩‍🦳 👩‍🦲 🧓 👴 👵 🙍 🙎 🙅 🙆 💁 🙋 🧏 🙇 🤦 🤷 🧘 🧍 🧎 🏃 💃 🕺 🕴️ 👯 🗣️ 👤 👥'.split(' ')
  },
  animals: {
    label: 'حیوانات',
    icon: '🐾',
    items: '🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐽 🐸 🐵 🙈 🙉 🙊 🐒 🐔 🐧 🐦 🐤 🐣 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🪱 🦋 🐌 🐞 🐜 🕷️ 🦂 🐢 🐍 🦎 🦖 🦕 🐙 🦑 🦀 🦞 🦐 🐠 🐟 🐡 🦈 🐳 🐋 🐊 🦓 🦒 🐘 🦏 🦛 🐪 🐫 🦘 🦬 🐃 🐂 🐄 🐎 🐖 🐏 🐑 🦙 🐐 🦌 🐕 🐈 🐓 🦃 🕊️ 🦢 🦩 🦚 🦜 🐇 🦝 🦨 🦡 🦫 🦦 🦥 🦔'.split(' ')
  },
  food: {
    label: 'غذا',
    icon: '🍕',
    items: '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🫐 🍈 🍒 🍑 🥭 🍍 🥥 🥝 🍅 🥑 🫛 🥦 🥬 🥒 🌶️ 🫑 🌽 🥕 🫒 🧄 🧅 🥔 🍠 🥐 🥯 🍞 🥖 🥨 🧀 🥚 🍳 🧈 🥞 🧇 🥓 🥩 🍗 🍖 🌭 🍔 🍟 🍕 🥪 🥙 🧆 🌮 🌯 🫔 🥗 🥘 🫕 🍝 🍜 🍲 🍛 🍣 🍱 🥟 🦪 🍤 🍙 🍚 🍘 🍥 🥠 🥮 🍡 🍧 🍨 🍦 🥧 🧁 🍰 🎂 🍮 🍭 🍬 🍫 🍿 🍩 🍪 🌰 🥜 🍯 🥛 ☕ 🍵 🧃 🥤 🧋 🍺 🍻 🥂 🍷 🍸 🍹 🧉'.split(' ')
  },
  travel: {
    label: 'سفر',
    icon: '✈',
    items: '🚗 🚕 🚙 🚌 🚎 🏎️ 🚓 🚑 🚒 🚐 🚚 🚛 🚜 🛵 🏍️ 🚲 🛴 🛹 🚨 🚔 🚍 🚘 🚖 ✈️ 🛫 🛬 🛩️ 🚁 🚀 🛸 🚢 ⛵ 🚤 🛥️ 🛳️ 🚂 🚆 🚇 🚊 🚉 🗺️ 🧭 🗿 🗽 🗼 🏰 🏯 🏟️ 🎡 🎢 🎠 🏖️ 🏝️ 🏜️ 🏕️ ⛺ 🏠 🏡 🏢 🏥 🏦 🏨 🏪 🏫 🏛️ ⛪ 🕌 🛕 🕍'.split(' ')
  },
  activities: {
    label: 'فعالیت',
    icon: '⚽',
    items: '⚽ 🏀 🏈 ⚾ 🥎 🎾 🏐 🏉 🥏 🎱 🪀 🪁 🏓 🏸 🏒 🏑 🥍 🏏 ⛳ 🏹 🎣 🤿 🥊 🥋 🎽 🛹 🛼 🏋️ 🤸 🤼 🤽 🤾 🧗 🚵 🚴 🏊 🧘 🧖 🎮 🕹️ 🎲 ♟️ 🧩 🧸 🎯 🎳 🎭 🎨 🎬 🎤 🎧 🎼 🎹 🥁 🎷 🎺 🎸 🎻 🎺 🎪'.split(' ')
  },
  objects: {
    label: 'اشیا',
    icon: '💡',
    items: '⌚ 📱 💻 ⌨️ 🖥️ 🖨️ 🖱️ 🖲️ 💾 💿 📷 📸 📹 🎥 📞 ☎️ 📺 📻 🔋 🔌 💡 🔦 🕯️ 🧯 🛒 💰 💳 💎 ⚖️ 🔧 🔨 ⚒️ 🛠️ ⛏️ 🔩 ⚙️ 🧲 🔬 🔭 📡 💊 💉 🩹 🧪 📚 📖 📝 ✏️ 🖊️ 🖋️ 📎 🖇️ 📌 📍 ✂️ 🔒 🔓 🔑 🔐 🗝️ 🛡️ 🔔 🔕 📣 📢 💬 💭 🗨️ ✉️ 📧 📦 🧳 🕰️ ⏰ ⌛ 📅 📆'.split(' ')
  },
  symbols: {
    label: 'نمادها',
    icon: '✨',
    items: '❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 💔 ❣️ 💕 💞 💓 💗 💖 💘 💝 💟 ☮️ ✝️ ☪️ 🕉️ ☯️ ✡️ 🔯 🪯 ☦️ 🛐 ☢️ ☣️ ⚠️ 🚸 🔱 ⚜️ 🔰 ♻️ ✅ ❌ ❗ ❓ ⁉️ ‼️ ⁉️ 💯 💢 💥 💫 ⭐ 🌟 ✨ ⚡ 🔥 💦 💨 🎉 🎊 🎈 🎁 🏆 🥇 🥈 🥉 🏅 🚀 💡 🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪ ⬛ ⬜ ◼️ ◻️ 🔺 🔻 🔷 🔶 🔹 🔸'.split(' ')
  }
}
const allEmojiItems = computed(() => {
  const q = emojiSearch.value.trim().toLowerCase()
  const categories = Object.values(emojiCategories)
  const all = categories.flatMap(category => category.items)
  return q ? all.filter(emoji => emoji.includes(q)) : emojiCategories[emojiCategory.value].items
})

/* =========================================================
   INTERNAL
   ========================================================= */

let socket = null
let reconnectTimer = null
let reconnectAttempts = 0
let destroyed = false
let themeObserver = null
let longPressTimer = null
let localUserId = null
let localUsername = ''

const MAX_MESSAGES = 300

/* =========================================================
   ACCESS TOKEN
   ========================================================= */

function getAccessToken() {
  return (
    localStorage.getItem(
      'access_token'
    ) || ''
  )
}

/* =========================================================
   DARK MODE
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
   BOOLEAN NORMALIZER
   ========================================================= */

function normalizeBoolean(value) {
  if (
    value === true ||
    value === 1 ||
    value === '1' ||
    value === 'true' ||
    value === 'True' ||
    value === 'TRUE'
  ) {
    return true
  }

  return false
}

/* =========================================================
   NORMALIZE MESSAGE
   ========================================================= */

function normalizeMessage(raw) {
  if (!raw) {
    return null
  }

  const source =
    raw.message_data ??
    raw

  const text =
    source.message ??
    source.text ??
    source.content ??
    source.body ??
    ''

  const senderId =
    source.user_id ??
    source.sender_id ??
    source.sender?.id ??
    source.author_id ??
    source.user?.id ??
    null

  const username =
    source.username ??
    source.sender_username ??
    source.sender?.username ??
    source.user?.username ??
    'کاربر'

  const createdAt =
    source.created_at ??
    source.timestamp ??
    new Date().toISOString()

  const messageId =
    source.id ??
    source.message_id ??
    null

  const clientId =
    String(
      source.client_id ??
      (
        messageId != null
          ? `server-${messageId}`
          : `${senderId || 'u'}-${createdAt}-${Math.random()
              .toString(36)
              .slice(2, 8)}`
      )
    )

  const rawIsStaff =
    source.is_staff ??
    source.user?.is_staff ??
    source.sender?.is_staff ??
    null

  const isStaff =
    rawIsStaff === null ||
    rawIsStaff === undefined
      ? null
      : normalizeBoolean(
          rawIsStaff
        )

  const replyRaw =
    source.reply_to ??
    null

  const replyTo = replyRaw
    ? {
        id:
          replyRaw.id ??
          replyRaw.message_id ??
          null,

        userId:
          replyRaw.user_id ??
          replyRaw.sender_id ??
          null,

        username:
          replyRaw.username ??
          replyRaw.sender_username ??
          replyRaw.user?.username ??
          replyRaw.sender?.username ??
          'کاربر',

        message:
          replyRaw.message ??
          replyRaw.text ??
          replyRaw.content ??
          '',

        isDeleted:
          normalizeBoolean(
            replyRaw.is_deleted
          ),

        isStaff:
          replyRaw.is_staff ??
          replyRaw.user?.is_staff ??
          replyRaw.sender?.is_staff ??
          null,
      }
    : null

  const reactions =
    Array.isArray(
      source.reactions
    )
      ? source.reactions.map(
          reaction => ({
            id:
              reaction.id ??
              null,

            messageId:
              reaction.message_id ??
              messageId,

            userId:
              reaction.user_id ??
              null,

            username:
              reaction.username ??
              'کاربر',

            reaction:
              reaction.reaction ??
              null,

            createdAt:
              reaction.created_at ??
              null,
          })
        )
      : []

  return {
    messageId:
      messageId != null
        ? Number(messageId)
        : null,

    clientId,

    senderId:
      senderId != null
        ? Number(senderId)
        : null,

    username,

    isStaff,

    text:
      typeof text === 'string'
        ? text.trim()
        : '',

    createdAt,

    editedAt:
      source.edited_at ??
      null,

    isDeleted:
      normalizeBoolean(
        source.is_deleted
      ),

    deletedAt:
      source.deleted_at ??
      null,

    replyTo,

    reactions,

    isMine:
      senderId != null &&
      localUserId != null &&
      String(senderId) ===
        String(localUserId),
  }
}

/* =========================================================
   MESSAGE KEY
   ========================================================= */

function getMessageKey(message) {
  if (
    message.messageId != null
  ) {
    return `message-${message.messageId}`
  }

  return `client-${message.clientId}`
}

/* =========================================================
   SAME MESSAGE
   ========================================================= */

function sameMessage(
  first,
  second
) {
  if (
    first.messageId != null &&
    second.messageId != null
  ) {
    return (
      Number(first.messageId) ===
      Number(second.messageId)
    )
  }

  return (
    first.clientId ===
    second.clientId
  )
}

/* =========================================================
   PUSH MESSAGE
   ========================================================= */

function pushMessage(message) {
  if (!message) {
    return
  }

  const index =
    messages.value.findIndex(
      item =>
        sameMessage(
          item,
          message
        )
    )

  if (index !== -1) {
    const existing =
      messages.value[index]

    messages.value[index] = {
      ...existing,
      ...message,

      isStaff:
        message.isStaff ??
        existing.isStaff ??
        null,
    }

    messages.value = [
      ...messages.value,
    ]

    scrollToBottom()

    return
  }

  messages.value = [
    ...messages.value,
    message,
  ].slice(
    -MAX_MESSAGES
  )

  scrollToBottom()
}

/* =========================================================
   SOCKET MESSAGE
   ========================================================= */

function handleIncoming(data) {
  if (!data) {
    return
  }

  if (
    data.type ===
    'connection'
  ) {
    const serverUserId =
      data.user_id ??
      data.user?.id

    if (
      serverUserId != null
    ) {
      localUserId =
        serverUserId

      localStorage.setItem(
        'user_id',
        String(
          serverUserId
        )
      )
    }

    localUsername =
      data.username ??
      data.user?.username ??
      localStorage.getItem(
        'username'
      ) ??
      'کاربر'

    if (
      localUsername &&
      localUsername !==
        'کاربر'
    ) {
      localStorage.setItem(
        'username',
        localUsername
      )
    }
  }

  if (data.type === 'room_typing') {
    const name = data.username || 'کاربر'
    if (data.is_typing) {
      if (!typingUsers.value.includes(name)) typingUsers.value = [...typingUsers.value, name].slice(-4)
    } else {
      typingUsers.value = typingUsers.value.filter(x => x !== name)
    }
    return
  }

  if (
    data.type ===
      'chat_history' ||
    data.type ===
      'room_chat_history'
  ) {
    const history =
      Array.isArray(
        data.messages
      )
        ? data.messages
        : []

    messages.value =
      history
        .map(
          normalizeMessage
        )
        .filter(Boolean)
        .slice(
          -MAX_MESSAGES
        )

    loadingHistory.value =
      false

    nextTick(() => {
      scrollToBottom()
    })

    return
  }

  if (
    [
      'chat_message',
      'room_chat_message',
      'message',
      'chat',
    ].includes(
      data.type
    )
  ) {
    const rawMessage =
      data.message_data ??
      data.message ??
      data

    const message =
      normalizeMessage(
        rawMessage
      )

    if (!message) {
      return
    }

    pushMessage(
      message
    )

    if (!message.isMine && !document.hidden) {
      pushNotification(`پیام جدید از ${message.username}`, message.text.slice(0, 80))
    }

    if (
      message.isMine
    ) {
      sending.value =
        false
    }

    return
  }

  if (
    data.type ===
    'chat_message_edited'
  ) {
    handleEditedMessage(
      data.message_data ??
      data.data ??
      data
    )

    return
  }

  if (
    data.type ===
    'chat_message_deleted'
  ) {
    handleDeletedMessage(
      data.message_data ??
      data.data ??
      data
    )

    return
  }

  if (
    data.type ===
    'chat_message_reaction_updated'
  ) {
    handleReactionUpdated(
      data.reaction_data ??
      data.data ??
      data
    )

    return
  }

  if (
    data.type ===
    'chat_message_reaction_removed'
  ) {
    handleReactionRemoved(
      data.reaction_data ??
      data.data ??
      data
    )
  }
}

/* =========================================================
   EDITED MESSAGE
   ========================================================= */

function handleEditedMessage(
  raw
) {
  const message =
    normalizeMessage(
      raw
    )

  if (!message) {
    return
  }

  const index =
    findMessageIndex(
      message.messageId
    )

  if (index === -1) {
    return
  }

  const existing =
    messages.value[index]

  messages.value[index] = {
    ...existing,
    ...message,

    isStaff:
      message.isStaff ??
      existing.isStaff ??
      null,

    isMine:
      existing.isMine,
  }

  messages.value = [
    ...messages.value,
  ]

  if (
    editingMessage.value &&
    Number(
      editingMessage.value.messageId
    ) ===
      Number(
        message.messageId
      )
  ) {
    clearEdit()

    draft.value = ''

    autoResize()
  }

  sending.value =
    false
}

/* =========================================================
   DELETED MESSAGE
   ========================================================= */

function handleDeletedMessage(
  raw
) {
  const message =
    normalizeMessage(
      raw
    )

  if (!message) {
    return
  }

  const index =
    findMessageIndex(
      message.messageId
    )

  if (index === -1) {
    return
  }

  const existing =
    messages.value[index]

  messages.value[index] = {
    ...existing,
    ...message,

    isStaff:
      message.isStaff ??
      existing.isStaff ??
      null,

    isDeleted:
      true,

    text:
      '',

    isMine:
      existing.isMine,
  }

  messages.value = [
    ...messages.value,
  ]

  if (
    replyingTo.value &&
    Number(
      replyingTo.value.messageId
    ) ===
      Number(
        message.messageId
      )
  ) {
    replyingTo.value =
      messages.value[index]
  }

  if (
    editingMessage.value &&
    Number(
      editingMessage.value.messageId
    ) ===
      Number(
        message.messageId
      )
  ) {
    cancelAction()
  }
}

/* =========================================================
   REACTION UPDATED
   ========================================================= */

function handleReactionUpdated(
  raw
) {
  const reaction =
    normalizeReaction(
      raw
    )

  if (!reaction) {
    return
  }

  const index =
    findMessageIndex(
      reaction.messageId
    )

  if (index === -1) {
    return
  }

  const message =
    messages.value[index]

  const reactions = [
    ...(message.reactions || []),
  ]

  const sameUserIndex =
    reactions.findIndex(
      item =>
        Number(
          item.userId
        ) ===
        Number(
          reaction.userId
        )
    )

  if (
    sameUserIndex !== -1
  ) {
    reactions[
      sameUserIndex
    ] = reaction
  } else {
    reactions.push(
      reaction
    )
  }

  messages.value[index] = {
    ...message,
    reactions,
  }

  messages.value = [
    ...messages.value,
  ]
}

/* =========================================================
   REACTION REMOVED
   ========================================================= */

function handleReactionRemoved(
  raw
) {
  const reaction =
    normalizeReaction(
      raw
    )

  if (!reaction) {
    return
  }

  const index =
    findMessageIndex(
      reaction.messageId
    )

  if (index === -1) {
    return
  }

  const message =
    messages.value[index]

  const reactions =
    (
      message.reactions ||
      []
    ).filter(
      item => {
        if (
          reaction.id != null
        ) {
          return (
            Number(item.id) !==
            Number(reaction.id)
          )
        }

        return !(
          Number(
            item.userId
          ) ===
          Number(
            reaction.userId
          )
        )
      }
    )

  messages.value[index] = {
    ...message,
    reactions,
  }

  messages.value = [
    ...messages.value,
  ]
}

/* =========================================================
   NORMALIZE REACTION
   ========================================================= */

function normalizeReaction(
  raw
) {
  if (!raw) {
    return null
  }

  return {
    id:
      raw.id ??
      null,

    messageId:
      raw.message_id ??
      raw.messageId ??
      null,

    userId:
      raw.user_id ??
      raw.userId ??
      null,

    username:
      raw.username ??
      'کاربر',

    reaction:
      raw.reaction ??
      null,

    createdAt:
      raw.created_at ??
      null,
  }
}

/* =========================================================
   FIND MESSAGE
   ========================================================= */

function findMessageIndex(
  messageId
) {
  if (
    messageId == null
  ) {
    return -1
  }

  return messages.value.findIndex(
    message =>
      message.messageId != null &&
      Number(
        message.messageId
      ) ===
        Number(
          messageId
        )
  )
}

/* =========================================================
   SOCKET URL
   ========================================================= */

function buildSocketUrl() {

  const token =
    encodeURIComponent(
      getAccessToken()
    )

  const isProduction =
    window.location.hostname ===
    'dopamine-st2u.onrender.com'

  const protocol =
    window.location.protocol ===
    'https:'
      ? 'wss:'
      : 'ws:'

  const host =
    isProduction
      ? 'dopamine-backend-3vbz.onrender.com'
      : '127.0.0.1:8000'

  return (
    `${protocol}//${host}` +
    `/ws/rooms/${props.roomId}/` +
    `?token=${token}`
  )

}


/* =========================================================
   CONNECT
   ========================================================= */

function connect() {
  if (
    destroyed ||
    !props.roomId
  ) {
    return
  }

  const token =
    getAccessToken()

  if (!token) {
    console.error(
      'ROOM CHAT: ACCESS TOKEN NOT FOUND'
    )

    return
  }

  try {
    socket?.close()
  } catch {
    // ignore
  }

  loadingHistory.value =
    messages.value.length === 0

  const ws =
    new WebSocket(
      buildSocketUrl()
    )

  socket =
    ws

  ws.onopen = () => {
    reconnectAttempts =
      0

    socketConnected.value =
      true

    console.log(
      'ROOM CHAT SOCKET CONNECTED:',
      props.roomId
    )

    ws.send(
      JSON.stringify({
        type:
          'chat_history_request',
      })
    )

    nextTick(() => {
      autoResize()
    })
  }

  ws.onmessage =
    event => {
      try {
        const data =
          JSON.parse(
            event.data
          )

        console.log(
          'ROOM CHAT SOCKET MESSAGE:',
          data
        )

        handleIncoming(
          data
        )
      } catch (error) {
        console.error(
          'ROOM CHAT MESSAGE ERROR:',
          error
        )
      }
    }

  ws.onerror =
    error => {
      console.error(
        'ROOM CHAT SOCKET ERROR:',
        error
      )
    }

  ws.onclose = () => {
    socketConnected.value =
      false

    if (destroyed) {
      return
    }

    scheduleReconnect()
  }
}

/* =========================================================
   RECONNECT
   ========================================================= */

function scheduleReconnect() {
  if (
    reconnectTimer ||
    destroyed
  ) {
    return
  }

  const delay =
    Math.min(
      10000,
      800 *
        Math.pow(
          2,
          reconnectAttempts
        )
    )

  reconnectAttempts++

  reconnectTimer =
    window.setTimeout(
      () => {
        reconnectTimer =
          null

        connect()
      },
      delay
    )
}

function loadPinned() {
  try { pinnedIds.value = JSON.parse(localStorage.getItem(`room-pins-${props.roomId}`) || '[]') } catch { pinnedIds.value = [] }
}

function persistPinned() {
  localStorage.setItem(`room-pins-${props.roomId}`, JSON.stringify(pinnedIds.value))
}

function isPinned(message) {
  return !!message?.messageId && pinnedIds.value.includes(Number(message.messageId))
}

function togglePin(message) {
  if (!message?.messageId) return
  const id = Number(message.messageId)
  pinnedIds.value = isPinned(message) ? pinnedIds.value.filter(x => x !== id) : [...pinnedIds.value, id].slice(-100)
  persistPinned()
  closeContextMenu()
}

function pushNotification(title, text) {
  const item = { id: `${Date.now()}-${Math.random()}`, title, text }
  notifications.value = [item, ...notifications.value].slice(0, 4)
  clearTimeout(notificationTimer)
  notificationTimer = window.setTimeout(() => { notifications.value = [] }, 7000)
}

function clearNotifications() { notifications.value = [] }

function handleComposerInput() {
  autoResize()
  if (!socket || socket.readyState !== WebSocket.OPEN) return
  sendSocket({ type: 'room_typing', is_typing: !!draft.value.trim() })
  clearTimeout(typingTimer)
  typingTimer = window.setTimeout(() => sendSocket({ type: 'room_typing', is_typing: false }), 900)
}

/* =========================================================
   SEND / EDIT
   ========================================================= */

function sendMessage() {
  closeEmojiPicker()
  const text =
    draft.value.trim()

  if (!text) {
    return
  }

  if (
    !socket ||
    socket.readyState !==
      WebSocket.OPEN
  ) {
    return
  }

  if (sending.value) {
    return
  }

  if (
    editingMessage.value
  ) {
    const messageId =
      editingMessage.value
        .messageId

    if (messageId == null) {
      return
    }

    sending.value =
      true

    try {
      socket.send(
        JSON.stringify({
          type:
            'chat_message_edit',

          message_id:
            messageId,

          message:
            text,
        })
      )
    } catch (error) {
      console.error(
        'ROOM CHAT EDIT ERROR:',
        error
      )

      sending.value =
        false
    }

    return
  }

  const clientId =
    `local-${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 8)}`

  const payload = {
    type:
      'chat_message',

    message:
      text,

    client_id:
      clientId,
  }

  if (
    replyingTo.value &&
    replyingTo.value.messageId != null
  ) {
    payload.reply_to_id =
      replyingTo.value.messageId
  }

  sending.value =
    true

  try {
    socket.send(
      JSON.stringify(
        payload
      )
    )

    draft.value =
      ''

    clearReply()

    nextTick(() => {
      autoResize()
    })
  } catch (error) {
    console.error(
      'ROOM CHAT SEND ERROR:',
      error
    )

    sending.value =
      false
  }
}

/* =========================================================
   EDIT MESSAGE
   ========================================================= */

function startEditMessage(
  message
) {
  closeContextMenu()

  if (!message) {
    return
  }

  if (!message.isMine) {
    return
  }

  if (message.isDeleted) {
    return
  }

  clearReply()

  editingMessage.value = {
    ...message,
  }

  draft.value =
    message.text

  nextTick(() => {
    autoResize()

    inputEl.value?.focus()

    if (inputEl.value) {
      inputEl.value.setSelectionRange(
        inputEl.value.value.length,
        inputEl.value.value.length
      )
    }
  })
}

function clearEdit() {
  editingMessage.value =
    null
}

/* =========================================================
   DELETE
   ========================================================= */

function deleteMessage(
  message
) {
  closeContextMenu()

  if (!message) {
    return
  }

  if (!message.isMine) {
    return
  }

  if (message.isDeleted) {
    return
  }

  if (
    message.messageId == null
  ) {
    return
  }

  const confirmed =
    window.confirm(
      'آیا مطمئنی می‌خواهی این پیام را حذف کنی؟'
    )

  if (!confirmed) {
    return
  }

  if (
    !socket ||
    socket.readyState !==
      WebSocket.OPEN
  ) {
    return
  }

  socket.send(
    JSON.stringify({
      type:
        'chat_message_delete',

      message_id:
        message.messageId,
    })
  )
}

/* =========================================================
   REPLY
   ========================================================= */

function replyToMessage(
  message
) {
  closeContextMenu()

  if (!message) {
    return
  }

  clearEdit()

  replyingTo.value = {
    ...message,
  }

  nextTick(() => {
    inputEl.value?.focus()
  })
}

/* =========================================================
   CANCEL ACTION
   ========================================================= */

function cancelAction() {
  clearEdit()

  clearReply()

  draft.value =
    ''

  nextTick(() => {
    autoResize()
  })
}

/* =========================================================
   REPLY CLEAR
   ========================================================= */

function clearReply() {
  replyingTo.value =
    null
}

/* =========================================================
   REACTIONS
   ========================================================= */

function toggleReaction(
  message,
  type
) {
  if (!message) {
    return
  }

  if (message.isDeleted) {
    return
  }

  if (
    message.messageId == null
  ) {
    return
  }

  const current =
    getUserReaction(
      message
    )

  if (
    current === type
  ) {
    sendSocket({
      type:
        'chat_message_reaction_remove',

      message_id:
        message.messageId,
    })
  } else {
    sendSocket({
      type:
        'chat_message_reaction',

      message_id:
        message.messageId,

      reaction:
        type,
    })
  }
}

function getUserReaction(
  message
) {
  if (!message) {
    return null
  }

  const reaction =
    (
      message.reactions ||
      []
    ).find(
      item =>
        Number(
          item.userId
        ) ===
        Number(
          localUserId
        )
    )

  return reaction
    ? reaction.reaction
    : null
}

function getReactionSummary(
  message
) {
  if (!message) {
    return []
  }

  const result = []

  for (
    const type of reactionTypes
  ) {
    const items =
      (
        message.reactions ||
        []
      ).filter(
        item =>
          item.reaction ===
          type
      )

    if (!items.length) {
      continue
    }

    result.push({
      type,

      count:
        items.length,

      myReaction:
        items.some(
          item =>
            Number(
              item.userId
            ) ===
            Number(
              localUserId
            )
        ),
    })
  }

  return result
}

function getReactionEmoji(
  type
) {
  return (
    reactionEmojis[type] ||
    '🙂'
  )
}

function getReactionLabel(
  type
) {
  return (
    reactionLabels[type] ||
    'واکنش'
  )
}

/* =========================================================
   CONTEXT MENU
   ========================================================= */

function openMessageMenu(
  event,
  message
) {
  openMessageMenuAt(
    event.clientX,
    event.clientY,
    message
  )
}

function openMessageMenuFromButton(
  event,
  message
) {
  openMessageMenuAt(
    event.clientX,
    event.clientY,
    message
  )
}

function openMessageMenuAt(
  x,
  y,
  message
) {
  if (!message) {
    return
  }

  const width =
    225

  const height =
    message.isMine
      ? 255
      : 175

  let finalX =
    x

  let finalY =
    y

  if (
    finalX + width >
    window.innerWidth - 10
  ) {
    finalX =
      window.innerWidth -
      width -
      10
  }

  if (
    finalY + height >
    window.innerHeight - 10
  ) {
    finalY =
      window.innerHeight -
      height -
      10
  }

  finalX =
    Math.max(
      10,
      finalX
    )

  finalY =
    Math.max(
      10,
      finalY
    )

  contextMenu.value = {
    visible:
      true,

    x:
      finalX,

    y:
      finalY,

    message,

    showReactions:
      false,
  }

  contextMenuStyle.value = {
    left:
      `${finalX}px`,

    top:
      `${finalY}px`,
  }
}

function toggleReactionMenu() {
  contextMenu.value.showReactions =
    !contextMenu.value
      .showReactions
}

function selectReactionFromMenu(
  type
) {
  const message =
    contextMenu.value.message

  closeContextMenu()

  if (!message) {
    return
  }

  toggleReaction(
    message,
    type
  )
}

function closeContextMenu() {
  contextMenu.value.visible =
    false

  contextMenu.value.message =
    null

  contextMenu.value.showReactions =
    false
}

/* =========================================================
   CLICK OUTSIDE
   ========================================================= */

function toggleEmojiPicker() {
  showEmojiPicker.value = !showEmojiPicker.value
  if (showEmojiPicker.value) {
    nextTick(() => inputEl.value?.focus())
  }
}

function closeEmojiPicker() {
  showEmojiPicker.value = false
}

function selectEmoji(emoji) {
  draft.value += emoji
  closeEmojiPicker()
  nextTick(() => {
    autoResize()
    inputEl.value?.focus()
    const input = inputEl.value
    if (input) input.selectionStart = input.selectionEnd = input.value.length
  })
}

function scrollToBottomSmooth() {
  const element = messagesEl.value
  if (!element) return
  element.scrollTo({ top: element.scrollHeight, behavior: 'smooth' })
  unreadCount.value = 0
  showScrollButton.value = false
}

function handleScroll() {
  const element = messagesEl.value
  if (!element) return
  const atBottom =
    element.scrollHeight - element.scrollTop - element.clientHeight < 100
  showScrollButton.value = !atBottom
  if (atBottom) unreadCount.value = 0
}

function handleRoomClick(
  event
) {
  if (
    contextMenuEl.value &&
    contextMenuEl.value.contains(
      event.target
    )
  ) {
    return
  }

  closeContextMenu()
  closeEmojiPicker()
}

/* =========================================================
   LONG PRESS
   ========================================================= */

function startLongPress(
  event,
  message
) {
  cancelLongPress()

  longPressTimer =
    window.setTimeout(
      () => {
        const touch =
          event.touches?.[0]

        if (!touch) {
          return
        }

        openMessageMenuAt(
          touch.clientX,
          touch.clientY,
          message
        )
      },
      550
    )
}

function cancelLongPress() {
  if (
    longPressTimer
  ) {
    window.clearTimeout(
      longPressTimer
    )

    longPressTimer =
      null
  }
}

/* =========================================================
   SCROLL TO MESSAGE
   ========================================================= */

function scrollToMessage(
  messageId
) {
  if (
    messageId == null
  ) {
    return
  }

  const target =
    messagesEl.value?.querySelector(
      `[data-message-id="${messageId}"]`
    )

  if (!target) {
    return
  }

  target.scrollIntoView({
    behavior:
      'smooth',

    block:
      'center',
  })

  target.classList.add(
    'message-highlight'
  )

  window.setTimeout(
    () => {
      target.classList.remove(
        'message-highlight'
      )
    },
    1000
  )
}

/* =========================================================
   SOCKET SEND
   ========================================================= */

function sendSocket(
  data
) {
  if (
    !socket ||
    socket.readyState !==
      WebSocket.OPEN
  ) {
    return false
  }

  try {
    socket.send(
      JSON.stringify(
        data
      )
    )

    return true
  } catch (error) {
    console.error(
      'ROOM CHAT SOCKET SEND ERROR:',
      error
    )

    return false
  }
}

/* =========================================================
   SCROLL
   ========================================================= */

function scrollToBottom() {
  nextTick(() => {
    const element =
      messagesEl.value

    if (!element) {
      return
    }

    element.scrollTop =
      element.scrollHeight
  })
}

/* =========================================================
   AUTO RESIZE
   ========================================================= */

function autoResize() {
  const input =
    inputEl.value

  if (!input) {
    return
  }

  input.style.height =
    'auto'

  input.style.height =
    `${Math.min(
      input.scrollHeight,
      120
    )}px`
}

/* =========================================================
   INITIAL
   ========================================================= */

function getInitial(
  username
) {
  const value =
    String(
      username || ''
    ).trim()

  if (!value) {
    return '?'
  }

  return value
    .charAt(0)
    .toUpperCase()
}

/* =========================================================
   TIME
   ========================================================= */

function formatTime(
  value
) {
  const date =
    new Date(
      value
    )

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return ''
  }

  return date.toLocaleTimeString(
    'fa-IR',
    {
      hour:
        '2-digit',

      minute:
        '2-digit',
    }
  )
}

/* =========================================================
   DATE DIVIDER
   ========================================================= */

function isConsecutive(index) {
  if (index === 0) return false
  const current = visibleMessages.value[index]
  const prev = visibleMessages.value[index - 1]
  if (!current || !prev) return false
  if (current.senderId !== prev.senderId) return false
  const diff = new Date(current.createdAt) - new Date(prev.createdAt)
  return diff < 5 * 60 * 1000
}

function shouldShowDateDivider(index) {
  if (index === 0) return true
  const current = visibleMessages.value[index]
  const prev = visibleMessages.value[index - 1]
  if (!current || !prev) return false
  const d1 = new Date(current.createdAt).toDateString()
  const d2 = new Date(prev.createdAt).toDateString()
  return d1 !== d2
}

function getDateLabel(value) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return ''
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) return 'امروز'
  if (date.toDateString() === yesterday.toDateString()) return 'دیروز'

  const diffDays = Math.floor((today - date) / (1000 * 60 * 60 * 24))
  if (diffDays < 7) return `${diffDays} روز پیش`

  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

/* =========================================================
   WATCH — unread badge
   ========================================================= */

watch(messages, () => {
  const el = messagesEl.value
  if (!el) return
  const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 120
  if (!atBottom && messages.value.length) {
    unreadCount.value++
    showScrollButton.value = true
  }
}, { deep: true })

/* =========================================================
   MOUNTED
   ========================================================= */

onMounted(() => {
  const storedUserId =
    localStorage.getItem(
      'user_id'
    )

  if (
    storedUserId
  ) {
    localUserId =
      storedUserId
  }

  localUsername =
    localStorage.getItem(
      'username'
    ) || ''

  observeTheme()

  loadPinned()

  connect()

  // init mouse position to center
  nextTick(() => {
    const root = chatRootEl.value
    if (root) {
      const rect = root.getBoundingClientRect()
      mouse.value.x = rect.width / 2
      mouse.value.y = rect.height / 2
      mouse.value.targetX = rect.width / 2
      mouse.value.targetY = rect.height / 2
    }
    autoResize()
  })

  startMouseLoop()

  const el = messagesEl.value
  if (el) el.addEventListener('scroll', handleScroll, { passive: true })
})

/* =========================================================
   UNMOUNTED
   ========================================================= */

onBeforeUnmount(() => {
  destroyed =
    true

  cancelLongPress()

  if (mouseRafId) {
    cancelAnimationFrame(mouseRafId)
    mouseRafId = null
  }

  if (
    reconnectTimer
  ) {
    window.clearTimeout(
      reconnectTimer
    )
  }

  reconnectTimer =
    null

  themeObserver?.disconnect()

  try {
    socket?.close()
  } catch {
    // ignore
  }

  socket =
    null

  socketConnected.value =
    false

  const el = messagesEl.value
  if (el) el.removeEventListener('scroll', handleScroll)
})
</script>


<style scoped>
:global(*) { box-sizing: border-box; }
:global(button), :global(input), :global(textarea) { font-family: inherit; }
:global(button) { -webkit-tap-highlight-color: transparent; }

/* ═══════════════════════════════════════════════════════════
   ROOM CHAT CONTAINER
   ═══════════════════════════════════════════════════════════ */
.room-chat {
  --chat-bg: #ffffff;
  --chat-surface: #ffffff;
  --chat-soft: #f6f7fb;
  --chat-text: #0f1a2e;
  --chat-muted: #7a8ba3;
  --chat-border: rgba(100, 116, 139, 0.13);
  --chat-primary: var(--primary, #7055e8);
  --chat-primary-rgb: var(--primary-rgb, 112, 85, 232);
  --chat-primary-soft: rgba(var(--chat-primary-rgb), 0.08);
  --admin-gold: #c28a24;
  --admin-gold-light: #f2cf72;
  --admin-gold-soft: rgba(194, 138, 36, 0.075);
  --admin-gold-border: rgba(194, 138, 36, 0.22);

  position: relative;
  isolation: isolate;
  width: 100%;
  height: 100%;
  max-height: 100vh;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  direction: rtl;
  color: var(--chat-text);
  background: var(--chat-bg);
  border-radius: 22px;
  border: 1px solid var(--chat-border);
  font-family: inherit;
  box-shadow:
    0 25px 60px rgba(15, 26, 46, 0.08),
    0 0 0 1px rgba(255, 255, 255, 0.6) inset;
}

.room-chat.is-dark {
  --chat-bg: #0a0e1a;
  --chat-surface: #131a2a;
  --chat-soft: #1a2233;
  --chat-text: #eef2ff;
  --chat-muted: #8b97b0;
  --chat-border: rgba(148, 163, 184, 0.11);
  --chat-primary-soft: rgba(var(--chat-primary-rgb), 0.14);
  --admin-gold-soft: rgba(194, 138, 36, 0.10);
  box-shadow:
    0 25px 60px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.03) inset;
}

/* ═══════════════════════════════════════════════════════════
   INTERACTIVE MOUSE-REACTIVE BACKGROUND
   ═══════════════════════════════════════════════════════════ */
.chat-ambient {
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
  border-radius: inherit;
}

/* --- Base gradient --- */
.bg-base {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 15%, rgba(var(--chat-primary-rgb), 0.12), transparent 45%),
    radial-gradient(circle at 80% 85%, rgba(6, 182, 212, 0.10), transparent 45%),
    radial-gradient(circle at 50% 50%, rgba(236, 72, 153, 0.05), transparent 60%);
  transition: background 0.4s ease;
}

.is-dark .bg-base {
  background:
    radial-gradient(circle at 20% 15%, rgba(var(--chat-primary-rgb), 0.20), transparent 45%),
    radial-gradient(circle at 80% 85%, rgba(6, 182, 212, 0.14), transparent 45%),
    radial-gradient(circle at 50% 50%, rgba(236, 72, 153, 0.08), transparent 60%);
}

/* --- Mesh gradient that follows mouse --- */
.mesh-gradient {
  position: absolute;
  inset: -10%;
  background:
    radial-gradient(circle at 30% 30%, rgba(var(--chat-primary-rgb), 0.20), transparent 40%),
    radial-gradient(circle at 70% 60%, rgba(6, 182, 212, 0.16), transparent 40%),
    radial-gradient(circle at 45% 75%, rgba(236, 72, 153, 0.12), transparent 40%),
    radial-gradient(circle at 65% 25%, rgba(167, 139, 250, 0.15), transparent 40%);
  filter: blur(50px);
  opacity: 0.55;
  will-change: transform;
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  animation: meshShift 22s ease-in-out infinite alternate;
}

.is-dark .mesh-gradient {
  opacity: 0.45;
}

@keyframes meshShift {
  0%   { filter: blur(50px) hue-rotate(0deg); }
  100% { filter: blur(60px) hue-rotate(25deg); }
}

/* --- Mouse spotlight --- */
.mouse-spotlight {
  position: absolute;
  top: -300px;
  left: -300px;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(var(--chat-primary-rgb), 0.18) 0%,
    rgba(var(--chat-primary-rgb), 0.08) 30%,
    transparent 70%
  );
  pointer-events: none;
  will-change: transform;
  transition: opacity 0.4s ease;
  mix-blend-mode: multiply;
}

.is-dark .mouse-spotlight {
  background: radial-gradient(
    circle,
    rgba(var(--chat-primary-rgb), 0.28) 0%,
    rgba(var(--chat-primary-rgb), 0.12) 30%,
    transparent 70%
  );
  mix-blend-mode: screen;
}

/* --- React orbs (parallax to mouse) --- */
.react-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(45px);
  opacity: 0.7;
  will-change: transform;
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  mix-blend-mode: multiply;
}

.is-dark .react-orb {
  mix-blend-mode: screen;
  opacity: 0.4;
  filter: blur(60px);
}

.react-orb-1 {
  width: 380px; height: 380px;
  top: -140px; right: -140px;
  background: radial-gradient(circle, rgba(var(--chat-primary-rgb), 0.55), transparent 70%);
  animation: orbPulse1 14s ease-in-out infinite alternate;
}

.react-orb-2 {
  width: 320px; height: 320px;
  bottom: -120px; left: -120px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.5), transparent 70%);
  animation: orbPulse2 18s ease-in-out infinite alternate;
}

.react-orb-3 {
  width: 240px; height: 240px;
  top: 35%; left: 42%;
  background: radial-gradient(circle, rgba(236, 72, 153, 0.4), transparent 70%);
  opacity: 0.55;
  animation: orbPulse3 22s ease-in-out infinite alternate;
}

.react-orb-4 {
  width: 200px; height: 200px;
  top: 15%; left: 18%;
  background: radial-gradient(circle, rgba(167, 139, 250, 0.45), transparent 70%);
  opacity: 0.5;
  animation: orbPulse4 26s ease-in-out infinite alternate;
}

@keyframes orbPulse1 {
  0%, 100% { filter: blur(45px); }
  50%      { filter: blur(55px); }
}
@keyframes orbPulse2 {
  0%, 100% { filter: blur(45px); }
  50%      { filter: blur(58px); }
}
@keyframes orbPulse3 {
  0%, 100% { filter: blur(45px); }
  50%      { filter: blur(52px); }
}
@keyframes orbPulse4 {
  0%, 100% { filter: blur(45px); }
  50%      { filter: blur(55px); }
}

/* --- Particle field --- */
.particle-field {
  position: absolute;
  inset: 0;
}

.field-particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, #ffffff 0%, rgba(var(--chat-primary-rgb), 0.9) 50%, transparent 75%);
  box-shadow: 0 0 8px rgba(var(--chat-primary-rgb), 0.7);
  opacity: 0;
  filter: blur(0.4px);
  animation: particleRise linear infinite;
  will-change: transform, opacity;
}

.is-dark .field-particle {
  background: radial-gradient(circle, #ffffff 0%, rgba(167, 139, 250, 0.9) 50%, transparent 75%);
  box-shadow: 0 0 10px rgba(167, 139, 250, 0.8);
}

@keyframes particleRise {
  0%   { transform: translate3d(0, 0, 0) scale(0.6); opacity: 0; }
  10%  { opacity: 1; }
  50%  { transform: translate3d(15px, -180px, 0) scale(1.1); opacity: 0.9; }
  90%  { opacity: 0.6; }
  100% { transform: translate3d(-10px, -400px, 0) scale(0.7); opacity: 0; }
}

/* --- Grid --- */
.ambient-grid {
  position: absolute;
  inset: -30%;
  opacity: 0.14;
  background-image:
    linear-gradient(rgba(100, 116, 139, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(100, 116, 139, 0.08) 1px, transparent 1px);
  background-size: 48px 48px;
  transform-origin: center;
  transform: perspective(800px) rotateX(58deg) translateY(-12%);
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  mask-image: linear-gradient(to bottom, transparent, #000 28%, #000 72%, transparent);
  -webkit-mask-image: linear-gradient(to bottom, transparent, #000 28%, #000 72%, transparent);
}

.is-dark .ambient-grid { opacity: 0.10; }

/* --- Noise --- */
.bg-noise {
  position: absolute;
  inset: 0;
  opacity: 0.12;
  pointer-events: none;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  border-radius: inherit;
}

.is-dark .bg-noise { opacity: 0.07; }

/* --- Vignette --- */
.vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(15, 26, 46, 0.06) 100%);
  pointer-events: none;
}

.is-dark .vignette {
  background: radial-gradient(ellipse at center, transparent 40%, rgba(0, 0, 0, 0.35) 100%);
}

/* ═══════════════════════════════════════════════════════════
   HEADER
   ═══════════════════════════════════════════════════════════ */
.chat-header {
  position: relative;
  z-index: 10;
  flex: 0 0 auto;
  display: grid;
  grid-template-columns: minmax(180px, 1fr) auto minmax(180px, 1fr);
  align-items: center;
  gap: 14px;
  min-height: 76px;
  padding: 13px 18px;
  border-bottom: 1px solid var(--chat-border);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(255, 255, 255, 0.5));
  backdrop-filter: blur(24px) saturate(145%);
  -webkit-backdrop-filter: blur(24px) saturate(145%);
}
.is-dark .chat-header {
  background: linear-gradient(180deg, rgba(10, 14, 26, 0.85), rgba(10, 14, 26, 0.6));
}

.chat-title { display: flex; align-items: center; gap: 11px; min-width: 0; }
.chat-title-mark {
  width: 43px; height: 43px; flex: 0 0 43px;
  display: grid; place-items: center;
  border: 1px solid rgba(var(--chat-primary-rgb), 0.18);
  border-radius: 14px;
  color: var(--chat-primary);
  background: linear-gradient(145deg, rgba(var(--chat-primary-rgb), 0.14), rgba(var(--chat-primary-rgb), 0.04));
  box-shadow: 0 10px 25px rgba(var(--chat-primary-rgb), 0.09);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease;
}
.chat-title-mark:hover {
  transform: rotate(-6deg) scale(1.06);
  box-shadow: 0 14px 32px rgba(var(--chat-primary-rgb), 0.18);
}
.chat-title-mark svg { width: 22px; height: 22px; }
.chat-title div:last-child { min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.chat-title strong { font-size: 13px; font-weight: 900; letter-spacing: -0.2px; }
.chat-title span { font-size: 9px; color: var(--chat-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.chat-header-tools { display: flex; align-items: center; gap: 7px; justify-content: center; }
.chat-search {
  width: min(330px, 34vw);
  height: 42px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 11px;
  border: 1px solid var(--chat-border);
  border-radius: 13px;
  background: var(--chat-surface);
  color: var(--chat-muted);
  box-shadow: 0 8px 25px rgba(15, 26, 46, 0.045);
  transition: 0.2s ease;
}
.chat-search:focus-within {
  border-color: rgba(var(--chat-primary-rgb), 0.3);
  box-shadow: 0 0 0 4px rgba(var(--chat-primary-rgb), 0.07);
}
.chat-search > svg { width: 16px; height: 16px; flex: 0 0 16px; }
.chat-search input { min-width: 0; flex: 1; border: 0; outline: 0; background: transparent; color: var(--chat-text); font-size: 10px; }
.chat-search input::placeholder { color: var(--chat-muted); }
.chat-search button {
  width: 24px; height: 24px; display: grid; place-items: center;
  border: 0; border-radius: 8px; background: transparent;
  color: var(--chat-muted); cursor: pointer;
}
.chat-search button:hover { background: var(--chat-soft); color: var(--chat-text); }
.chat-search button svg { width: 13px; height: 13px; }

.header-icon-button {
  position: relative;
  width: 42px; height: 42px;
  display: grid; place-items: center;
  border: 1px solid var(--chat-border);
  border-radius: 13px;
  background: var(--chat-surface);
  color: var(--chat-muted);
  cursor: pointer;
  transition: 0.2s ease;
  box-shadow: 0 8px 25px rgba(15, 26, 46, 0.04);
}
.header-icon-button:hover,
.header-icon-button.active {
  color: var(--chat-primary);
  border-color: rgba(var(--chat-primary-rgb), 0.22);
  background: var(--chat-primary-soft);
  transform: translateY(-1px);
  box-shadow: 0 10px 28px rgba(var(--chat-primary-rgb), 0.14);
}
.header-icon-button svg { width: 17px; height: 17px; }
.header-icon-button span {
  position: absolute;
  top: -5px; left: -4px;
  min-width: 17px; height: 17px;
  padding: 0 4px;
  display: grid; place-items: center;
  border-radius: 999px;
  background: var(--chat-primary);
  color: #fff;
  font-size: 8px;
  font-weight: 900;
  border: 2px solid var(--chat-bg);
  animation: badgePop 0.3s cubic-bezier(0.22, 1.4, 0.36, 1);
}
@keyframes badgePop {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.room-chat-badge {
  justify-self: end;
  display: inline-flex; align-items: center; gap: 7px;
  height: 34px; padding: 0 11px;
  border: 1px solid var(--chat-border);
  border-radius: 999px;
  background: var(--chat-surface);
  font-size: 9px; font-weight: 800;
  color: var(--chat-muted);
  white-space: nowrap;
}
.room-chat-badge-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #f59e0b;
  box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.1);
}
.room-chat-badge.online { color: #16865b; border-color: rgba(22, 134, 91, 0.16); }
.room-chat-badge.online .room-chat-badge-dot {
  background: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12);
  animation: onlinePulse 2s infinite;
}
.room-chat-badge.offline { color: #b7791f; }
@keyframes onlinePulse { 50% { box-shadow: 0 0 0 7px rgba(34, 197, 94, 0); } }

/* ═══════════════════════════════════════════════════════════
   BODY / MESSAGES
   ═══════════════════════════════════════════════════════════ */
.chat-body {
  position: relative;
  z-index: 2;
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 10px 12px 12px;
  overflow: hidden;
}

.messages {
  position: relative;
  flex: 1 1 auto;
  min-height: 0;
  max-height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 10px clamp(5px, 2vw, 30px) 18px;
  scroll-behavior: smooth;
  overscroll-behavior: contain;
  scrollbar-gutter: stable;
}

.custom-scrollbar::-webkit-scrollbar { width: 7px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(100, 116, 139, 0.22); border-radius: 99px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(var(--chat-primary-rgb), 0.42); }

.chat-state {
  height: 100%; min-height: 240px;
  display: flex; align-items: center; justify-content: center;
  gap: 10px;
  color: var(--chat-muted);
  font-size: 11px;
}
.mini-loader,
.send-loader {
  width: 16px; height: 16px;
  border: 2px solid rgba(var(--chat-primary-rgb), 0.18);
  border-top-color: var(--chat-primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
.mini-loader { width: 20px; height: 20px; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-chat {
  min-height: 380px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  padding: 30px;
}
.empty-chat-icon {
  width: 78px; height: 78px;
  display: grid; place-items: center;
  border: 1px solid rgba(var(--chat-primary-rgb), 0.17);
  border-radius: 26px;
  color: var(--chat-primary);
  background: linear-gradient(145deg, rgba(var(--chat-primary-rgb), 0.13), rgba(var(--chat-primary-rgb), 0.035));
  box-shadow: 0 18px 50px rgba(var(--chat-primary-rgb), 0.11);
  animation: emptyFloat 4s ease-in-out infinite;
}
.empty-chat-icon svg { width: 34px; height: 34px; }
.empty-chat h3 { margin: 18px 0 7px; font-size: 16px; font-weight: 900; }
.empty-chat p { margin: 0; color: var(--chat-muted); font-size: 10px; }
.empty-chat-action {
  margin-top: 18px;
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 14px;
  border: 1px solid rgba(var(--chat-primary-rgb), 0.18);
  border-radius: 11px;
  background: var(--chat-primary-soft);
  color: var(--chat-primary);
  font: 800 10px inherit;
  cursor: pointer;
  transition: 0.2s ease;
}
.empty-chat-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(var(--chat-primary-rgb), 0.15);
}
.empty-chat-action svg { width: 14px; height: 14px; }
@keyframes emptyFloat { 50% { transform: translateY(-7px); } }

.date-divider {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 20px auto 14px;
  max-width: 850px;
  padding: 0 12px;
}
.date-divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--chat-border), transparent);
}
.date-divider-text {
  padding: 5px 13px;
  border-radius: 999px;
  background: var(--chat-surface);
  border: 1px solid var(--chat-border);
  color: var(--chat-muted);
  font-size: 10px;
  font-weight: 800;
  white-space: nowrap;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 10px rgba(15, 26, 46, 0.05);
}

.message-row {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 9px;
  max-width: min(850px, 92%);
  margin: 0 auto 11px;
  padding: 1px 5px;
  transition: 0.18s ease;
  animation: messageSlideIn 0.38s cubic-bezier(0.22, 1, 0.36, 1);
}
@keyframes messageSlideIn {
  from { opacity: 0; transform: translateY(10px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.message-row.mine { flex-direction: row-reverse; }
.message-row.pinned { filter: drop-shadow(0 7px 16px rgba(var(--chat-primary-rgb), 0.05)); }
.message-row.pinned::before {
  content: "";
  position: absolute;
  inset: 0 -5px;
  border: 1px solid rgba(var(--chat-primary-rgb), 0.10);
  border-radius: 18px;
  pointer-events: none;
}
.message-row.highlighted .message-bubble {
  animation: highlightPulse 1.2s ease;
}
@keyframes highlightPulse {
  0% { box-shadow: 0 0 0 0 rgba(var(--chat-primary-rgb), 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(var(--chat-primary-rgb), 0); }
  100% { box-shadow: 0 0 0 0 rgba(var(--chat-primary-rgb), 0); }
}

.message-avatar {
  width: 35px; height: 35px;
  flex: 0 0 35px;
  display: grid; place-items: center;
  margin-top: 18px;
  border: 1px solid var(--chat-border);
  border-radius: 12px;
  background: var(--chat-surface);
  color: var(--chat-primary);
  font-size: 10px; font-weight: 900;
  box-shadow: 0 8px 20px rgba(15, 26, 46, 0.055);
  transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}
.message-avatar svg { width: 17px; height: 17px; }
.message-avatar.mine { background: var(--chat-primary-soft); }
.message-avatar.admin {
  color: #fff;
  background: linear-gradient(145deg, #b67e17, #e5bb58, #9b6c17);
  border-color: rgba(194, 138, 36, 0.32);
  box-shadow: 0 8px 22px rgba(194, 138, 36, 0.16);
}
.message-row:hover .message-avatar:not(.invisible) {
  transform: scale(1.08) rotate(-4deg);
}
.message-avatar.invisible { visibility: hidden; }

.message-content {
  position: relative;
  min-width: 0;
  max-width: min(680px, calc(100% - 44px));
}
.message-row.mine .message-content { text-align: right; }
.message-row.admin .message-content {
  padding: 8px 10px 10px;
  border: 1px solid rgba(194, 138, 36, 0.14);
  border-radius: 18px;
  background: var(--admin-gold-soft);
  isolation: isolate;
}
.message-row.admin .message-content::before {
  content: "";
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  padding: 1px;
  background: conic-gradient(
    from var(--admin-angle),
    transparent 0 245deg,
    rgba(214, 168, 61, 0.15) 275deg,
    #f2cf72 305deg,
    #c28a24 325deg,
    rgba(214, 168, 61, 0.15) 345deg,
    transparent 360deg
  );
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
  z-index: -1;
  animation: adminBorderLight 4.5s linear infinite;
}
@property --admin-angle { syntax: "<angle>"; inherits: false; initial-value: 0deg; }
@keyframes adminBorderLight { to { --admin-angle: 360deg; } }

.admin-badge {
  position: absolute;
  top: -10px; right: 12px;
  display: inline-flex; align-items: center; gap: 5px;
  min-height: 20px;
  padding: 3px 8px;
  border: 1px solid var(--admin-gold-border);
  border-radius: 999px;
  background: var(--chat-bg);
  color: var(--admin-gold);
  font-size: 8px;
  font-weight: 900;
  line-height: 1;
  box-shadow: 0 5px 14px rgba(0, 0, 0, 0.05);
}
.admin-badge svg { width: 11px; height: 11px; }
.message-meta {
  display: flex; align-items: center; gap: 7px;
  margin: 0 0 5px;
  padding: 0 3px;
}
.message-meta.invisible { visibility: hidden; height: 0; margin: 0; overflow: hidden; }
.message-meta.has-admin-badge { padding-top: 7px; }
.message-meta strong {
  max-width: 220px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  font-size: 9px; font-weight: 900;
}
.message-meta time { color: var(--chat-muted); font-size: 8px; }
.message-status { width: 13px; height: 13px; color: var(--chat-primary); }
.message-row.admin .message-meta strong { color: var(--admin-gold); }

.message-reply-preview {
  display: flex;
  align-items: stretch;
  max-width: 100%;
  margin: 0 0 5px;
  padding: 6px 8px;
  border: 1px solid var(--chat-border);
  border-radius: 11px;
  background: var(--chat-soft);
  cursor: pointer;
  text-align: right;
  transition: 0.16s ease;
}
.message-reply-preview:hover {
  border-color: rgba(var(--chat-primary-rgb), 0.25);
  transform: translateY(-1px);
}
.message-reply-preview.reply-from-admin {
  border-color: var(--admin-gold-border);
  background: var(--admin-gold-soft);
}
.reply-preview-line {
  width: 3px; flex: 0 0 3px;
  margin-left: 8px;
  border-radius: 6px;
  background: var(--chat-primary);
}
.reply-from-admin .reply-preview-line { background: var(--admin-gold); }
.reply-preview-content { min-width: 0; display: flex; flex-direction: column; overflow: hidden; }
.reply-preview-author { display: flex; align-items: center; gap: 5px; }
.reply-preview-content strong {
  max-width: 180px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  color: var(--chat-primary);
  font-size: 9px;
}
.reply-from-admin .reply-preview-content strong { color: var(--admin-gold); }
.reply-admin-badge {
  padding: 2px 5px;
  border: 1px solid var(--admin-gold-border);
  border-radius: 999px;
  color: var(--admin-gold);
  font-size: 7px; font-weight: 900;
}
.reply-preview-content > span {
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  color: var(--chat-muted);
  font-size: 9px;
}

.message-bubble-wrap { display: flex; align-items: flex-end; gap: 4px; }
.message-row.mine .message-bubble-wrap { flex-direction: row-reverse; }
.message-bubble {
  max-width: min(620px, 100%);
  padding: 9px 13px;
  border: 1px solid var(--chat-border);
  border-radius: 17px 17px 17px 6px;
  background: var(--chat-surface);
  color: var(--chat-text);
  font-size: 11.5px;
  line-height: 1.9;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  box-shadow: 0 7px 20px rgba(15, 26, 46, 0.035);
  transition: 0.18s ease;
}
.message-bubble:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(15, 26, 46, 0.06);
}
.message-row.mine .message-bubble {
  border-color: transparent;
  border-radius: 17px 17px 6px 17px;
  color: #fff;
  background: linear-gradient(135deg, var(--chat-primary), color-mix(in srgb, var(--chat-primary) 72%, #111827));
  box-shadow: 0 10px 28px rgba(var(--chat-primary-rgb), 0.18);
}
.message-row.admin .message-bubble {
  border-color: rgba(194, 138, 36, 0.18);
  background: rgba(255, 255, 255, 0.55);
  color: var(--chat-text);
}
.is-dark .message-row.admin .message-bubble { background: rgba(15, 23, 42, 0.45); }
.message-bubble.deleted {
  background: transparent !important;
  color: var(--chat-muted);
  border-style: dashed;
  box-shadow: none;
}
.deleted-message { display: inline-flex; align-items: center; gap: 6px; font-size: 10px; font-style: italic; }
.deleted-message svg { width: 14px; height: 14px; }
.edited-label {
  display: inline-block;
  margin-right: 6px;
  color: rgba(255, 255, 255, 0.65);
  font-size: 8px;
}
.message-row:not(.mine) .edited-label,
.message-row.admin .edited-label { color: var(--chat-muted); }

.message-more {
  width: 26px; height: 26px;
  flex: 0 0 26px;
  display: grid; place-items: center;
  padding: 0;
  border: 1px solid transparent;
  border-radius: 9px;
  background: transparent;
  color: var(--chat-muted);
  cursor: pointer;
  opacity: 0;
  transition: 0.15s;
}
.message-row:hover .message-more,
.message-more:focus-visible { opacity: 1; }
.message-more:hover {
  border-color: var(--chat-border);
  background: var(--chat-surface);
  color: var(--chat-text);
  transform: scale(1.08) rotate(90deg);
}
.message-more svg { width: 15px; height: 15px; }
@media (hover: none) { .message-more { opacity: 0.8; } }

.message-reactions { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 5px; }
.message-row.mine .message-reactions { justify-content: flex-end; }
.reaction-chip {
  display: inline-flex; align-items: center; gap: 3px;
  min-height: 23px;
  padding: 2px 7px;
  border: 1px solid var(--chat-border);
  border-radius: 999px;
  background: var(--chat-bg);
  color: var(--chat-text);
  cursor: pointer;
  font: inherit;
  transition: 0.15s;
}
.reaction-chip:hover {
  transform: translateY(-1px) scale(1.05);
  border-color: rgba(var(--chat-primary-rgb), 0.35);
}
.reaction-chip.selected {
  border-color: var(--chat-primary);
  background: var(--chat-primary-soft);
}
.reaction-chip span { font-size: 12px; }
.reaction-chip small { font-size: 9px; font-weight: 900; }

.scroll-bottom-button {
  position: absolute;
  left: 24px; bottom: 91px;
  z-index: 35;
  width: 39px; height: 39px;
  display: grid; place-items: center;
  border: 1px solid var(--chat-border);
  border-radius: 13px;
  background: var(--chat-surface);
  color: var(--chat-primary);
  box-shadow: 0 12px 30px rgba(15, 26, 46, 0.12);
  cursor: pointer;
  backdrop-filter: blur(18px);
  transition: 0.18s;
  animation: scrollBtnIn 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
.scroll-bottom-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 35px rgba(var(--chat-primary-rgb), 0.16);
}
.scroll-bottom-button svg { width: 17px; height: 17px; }
.unread-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  min-width: 19px;
  height: 19px;
  padding: 0 5px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: #ef4444;
  color: #fff;
  font-size: 9px;
  font-weight: 900;
  box-shadow: 0 4px 10px rgba(239, 68, 68, 0.4);
  animation: badgePop 0.3s cubic-bezier(0.22, 1.4, 0.36, 1);
}
@keyframes scrollBtnIn {
  from { opacity: 0; transform: translateY(10px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.chat-action-bar {
  display: flex; align-items: center; gap: 9px;
  min-height: 48px;
  margin: 0 0 7px;
  padding: 6px 9px;
  border: 1px solid var(--chat-border);
  border-radius: 14px;
  background: var(--chat-soft);
  box-shadow: 0 8px 22px rgba(15, 26, 46, 0.04);
}
.chat-action-bar-icon {
  width: 32px; height: 32px;
  flex: 0 0 32px;
  display: grid; place-items: center;
  border-radius: 10px;
  color: var(--chat-primary);
  background: var(--chat-primary-soft);
}
.chat-action-bar-icon svg { width: 16px; height: 16px; }
.chat-action-bar-content {
  min-width: 0; flex: 1;
  display: flex; flex-direction: column; gap: 2px;
}
.chat-action-bar-content strong { color: var(--chat-primary); font-size: 9px; font-weight: 900; }
.chat-action-bar-content span {
  overflow: hidden;
  color: var(--chat-muted);
  font-size: 9px;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.chat-action-bar-close {
  width: 29px; height: 29px;
  display: grid; place-items: center;
  border: 0; border-radius: 9px;
  background: transparent;
  color: var(--chat-muted);
  cursor: pointer;
}
.chat-action-bar-close:hover { background: var(--chat-bg); color: var(--chat-text); transform: rotate(90deg); }
.chat-action-bar-close svg { width: 14px; height: 14px; }

.typing-indicator {
  display: flex; align-items: center; gap: 8px;
  padding: 5px 10px;
  color: var(--chat-muted);
  font-size: 9px;
}
.typing-dots { display: flex; gap: 3px; }
.typing-dots i {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--chat-primary);
  animation: typingDot 1s infinite;
}
.typing-dots i:nth-child(2) { animation-delay: 0.15s; }
.typing-dots i:nth-child(3) { animation-delay: 0.3s; }
@keyframes typingDot {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40% { transform: translateY(-3px); opacity: 1; }
}

.room-notifications {
  position: absolute;
  left: 15px; bottom: 80px;
  z-index: 60;
  display: flex; flex-direction: column; gap: 7px;
  pointer-events: none;
}
.room-notification {
  display: flex; align-items: flex-start; gap: 9px;
  min-width: 225px; max-width: 330px;
  padding: 10px 12px;
  border: 1px solid var(--chat-border);
  border-radius: 15px;
  background: var(--chat-surface);
  box-shadow: 0 18px 42px rgba(15, 26, 46, 0.14);
  pointer-events: auto;
  backdrop-filter: blur(18px);
}
.notification-icon {
  width: 29px; height: 29px;
  display: grid; place-items: center;
  flex: 0 0 29px;
  border-radius: 9px;
  color: var(--chat-primary);
  background: var(--chat-primary-soft);
}
.notification-icon svg { width: 14px; height: 14px; }
.room-notification div { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.room-notification strong { font-size: 10px; }
.room-notification small {
  color: var(--chat-muted);
  font-size: 9px;
  line-height: 1.5;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

.chat-composer {
  position: relative;
  z-index: 50;
  flex: 0 0 auto;
  width: 100%;
  min-height: 58px;
  display: flex;
  align-items: flex-end;
  gap: 7px;
  padding: 7px;
  border: 1px solid var(--chat-border);
  border-radius: 19px;
  background: var(--chat-surface);
  box-shadow: 0 13px 35px rgba(15, 26, 46, 0.07);
  backdrop-filter: blur(22px);
  transition: 0.2s;
}
.chat-composer:focus-within {
  border-color: rgba(var(--chat-primary-rgb), 0.28);
  box-shadow:
    0 0 0 4px rgba(var(--chat-primary-rgb), 0.055),
    0 14px 35px rgba(15, 26, 46, 0.08);
}
.composer-tool {
  width: 41px; height: 41px;
  flex: 0 0 41px;
  display: grid; place-items: center;
  border: 1px solid var(--chat-border);
  border-radius: 13px;
  background: var(--chat-soft);
  color: var(--chat-muted);
  cursor: pointer;
  transition: 0.18s;
}
.composer-tool:hover,
.composer-tool.active {
  color: var(--chat-primary);
  border-color: rgba(var(--chat-primary-rgb), 0.25);
  background: var(--chat-primary-soft);
  transform: translateY(-1px);
}
.composer-tool svg { width: 20px; height: 20px; }
.chat-input {
  display: block; width: 100%;
  min-width: 0;
  min-height: 41px; max-height: 120px;
  flex: 1;
  resize: none;
  overflow-y: auto;
  padding: 9px 4px 7px;
  border: 0; outline: 0;
  background: transparent;
  color: var(--chat-text);
  font: 11.5px/1.8 inherit;
}
.chat-input::placeholder { color: var(--chat-muted); }
.chat-input:disabled { opacity: 0.55; cursor: not-allowed; }
.composer-counter {
  align-self: flex-end;
  padding-bottom: 7px;
  color: var(--chat-muted);
  font-size: 7px;
  direction: ltr;
  white-space: nowrap;
  transition: color 0.2s;
}
.composer-counter.danger { color: #ef4444; font-weight: 800; }
.send-button {
  width: 44px; height: 44px;
  flex: 0 0 44px;
  display: grid; place-items: center;
  border: 0; border-radius: 14px;
  color: #fff;
  background: linear-gradient(145deg, var(--chat-primary), color-mix(in srgb, var(--chat-primary) 72%, #111827));
  box-shadow: 0 10px 24px rgba(var(--chat-primary-rgb), 0.24);
  cursor: pointer;
  transition: 0.18s;
}
.send-button:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 14px 28px rgba(var(--chat-primary-rgb), 0.28);
}
.send-button:disabled { opacity: 0.42; box-shadow: none; cursor: not-allowed; }
.send-button svg { width: 19px; height: 19px; }
.send-loader { border-color: rgba(255, 255, 255, 0.3); border-top-color: #fff; }

.emoji-picker {
  position: absolute;
  z-index: 70;
  right: 12px; bottom: 78px;
  width: min(390px, calc(100% - 24px));
  padding: 11px;
  border: 1px solid var(--chat-border);
  border-radius: 20px;
  background: var(--chat-surface);
  box-shadow: 0 24px 70px rgba(15, 26, 46, 0.18);
  backdrop-filter: blur(25px) saturate(150%);
  transform-origin: bottom right;
}
.emoji-picker-head {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  padding: 2px 2px 9px;
}
.emoji-picker-head div { display: flex; flex-direction: column; gap: 2px; }
.emoji-picker-head strong { font-size: 11px; font-weight: 900; }
.emoji-picker-head span { font-size: 8px; color: var(--chat-muted); }
.emoji-close {
  width: 29px; height: 29px;
  display: grid; place-items: center;
  border: 0; border-radius: 9px;
  background: var(--chat-soft);
  color: var(--chat-muted);
  cursor: pointer;
}
.emoji-close:hover { color: var(--chat-text); transform: rotate(90deg); }
.emoji-close svg { width: 14px; height: 14px; }
.emoji-search {
  height: 37px;
  display: flex; align-items: center; gap: 7px;
  padding: 0 9px;
  border: 1px solid var(--chat-border);
  border-radius: 11px;
  background: var(--chat-soft);
  color: var(--chat-muted);
}
.emoji-search svg { width: 14px; height: 14px; }
.emoji-search input {
  width: 100%; border: 0; outline: 0;
  background: transparent;
  color: var(--chat-text);
  font-size: 9px;
}
.emoji-search input::placeholder { color: var(--chat-muted); }
.emoji-categories {
  display: flex; gap: 4px;
  margin: 9px 0 7px;
  padding: 3px;
  overflow-x: auto;
  border-radius: 11px;
  background: var(--chat-soft);
}
.emoji-categories button {
  width: 35px; height: 32px;
  flex: 0 0 35px;
  border: 0; border-radius: 8px;
  background: transparent;
  font-size: 17px;
  cursor: pointer;
  transition: 0.15s;
}
.emoji-categories button:hover,
.emoji-categories button.active {
  background: var(--chat-surface);
  box-shadow: 0 3px 10px rgba(15, 26, 46, 0.07);
  transform: translateY(-1px);
}
.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 3px;
  max-height: 205px;
  overflow-y: auto;
  padding: 2px;
}
.emoji-item {
  aspect-ratio: 1;
  display: grid; place-items: center;
  border: 0; border-radius: 9px;
  background: transparent;
  font-size: 21px;
  cursor: pointer;
  transition: 0.12s;
}
.emoji-item:hover {
  background: var(--chat-primary-soft);
  transform: scale(1.15);
}

.message-context-menu {
  position: fixed;
  z-index: 9999;
  width: 225px;
  padding: 7px;
  border: 1px solid var(--chat-border);
  border-radius: 17px;
  background: var(--chat-surface);
  box-shadow: 0 22px 60px rgba(15, 26, 46, 0.18);
  direction: rtl;
  backdrop-filter: blur(24px);
}
.message-context-menu.admin-context-menu {
  border-color: var(--admin-gold-border);
  box-shadow: 0 22px 60px rgba(194, 138, 36, 0.12);
}
.context-menu-user { display: flex; align-items: center; gap: 8px; padding: 6px 6px 8px; }
.context-menu-avatar {
  width: 33px; height: 33px;
  flex: 0 0 33px;
  display: grid; place-items: center;
  border-radius: 10px;
  color: var(--chat-primary);
  background: var(--chat-soft);
  font-size: 11px; font-weight: 900;
}
.context-menu-avatar svg { width: 17px; height: 17px; }
.context-menu-avatar.admin {
  color: #fff8df;
  background: linear-gradient(145deg, #b88722, #e6bd55, #9c6c13);
}
.context-menu-user > div:last-child { min-width: 0; display: flex; flex-direction: column; }
.context-menu-name-row { display: flex; align-items: center; gap: 5px; min-width: 0; }
.context-menu-user strong {
  max-width: 160px;
  overflow: hidden;
  color: var(--chat-text);
  font-size: 10px;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.context-menu-user span { color: var(--chat-muted); font-size: 8px; }
.context-admin-label {
  padding: 2px 5px;
  border: 1px solid var(--admin-gold-border);
  border-radius: 999px;
  color: var(--admin-gold) !important;
  font-size: 7px !important;
  font-weight: 900;
}
.context-menu-divider { height: 1px; margin: 2px 4px 5px; background: var(--chat-border); }
.context-menu-item {
  width: 100%; min-height: 38px;
  display: flex; align-items: center; gap: 8px;
  padding: 5px 7px;
  border: 0; border-radius: 10px;
  background: transparent;
  color: var(--chat-text);
  font-size: 10px;
  text-align: right;
  cursor: pointer;
  transition: 0.15s;
}
.context-menu-item:hover {
  background: var(--chat-soft);
  transform: translateX(-2px);
}
.context-menu-item.danger { color: #ef4444; }
.context-menu-item.danger:hover { background: rgba(239, 68, 68, 0.08); }
.context-menu-item-icon {
  width: 28px; height: 28px;
  flex: 0 0 28px;
  display: grid; place-items: center;
  border-radius: 8px;
  background: var(--chat-soft);
}
.context-menu-item-icon svg { width: 15px; height: 15px; }
.context-menu-arrow { margin-right: auto; color: var(--chat-muted); font-size: 17px; }
.reaction-picker {
  display: flex; align-items: center; justify-content: center;
  gap: 2px;
  margin: 3px 4px 5px;
  padding: 5px;
  border: 1px solid var(--chat-border);
  border-radius: 11px;
  background: var(--chat-soft);
}
.reaction-picker-button {
  width: 31px; height: 31px;
  display: grid; place-items: center;
  padding: 0; border: 0; border-radius: 8px;
  background: transparent;
  font-size: 16px;
  cursor: pointer;
  transition: 0.15s;
}
.reaction-picker-button:hover { transform: scale(1.12); background: var(--chat-bg); }
.reaction-picker-button.selected { background: var(--chat-bg); box-shadow: inset 0 0 0 1px var(--chat-primary); }

.message-menu-enter-active,
.message-menu-leave-active { transition: 0.13s ease; }
.message-menu-enter-from,
.message-menu-leave-to { opacity: 0; transform: scale(0.95) translateY(-4px); }

.chat-action-bar-enter-active,
.chat-action-bar-leave-active { transition: 0.16s ease; }
.chat-action-bar-enter-from,
.chat-action-bar-leave-to { opacity: 0; transform: translateY(5px); }

.emoji-pop-enter-active,
.emoji-pop-leave-active { transition: 0.18s ease; }
.emoji-pop-enter-from,
.emoji-pop-leave-to { opacity: 0; transform: translateY(8px) scale(0.96); }

.room-toast-enter-active { transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1); }
.room-toast-leave-active { transition: all 0.25s ease-in; }
.room-toast-enter-from { opacity: 0; transform: translateX(-20px) scale(0.9); }
.room-toast-leave-to { opacity: 0; transform: translateX(-20px) scale(0.9); }

@media (max-width: 900px) {
  .chat-header { grid-template-columns: 1fr auto; }
  .chat-header-tools { grid-column: 1 / -1; grid-row: 2; justify-content: stretch; }
  .chat-search { width: auto; flex: 1; }
  .room-chat-badge { grid-column: 2; grid-row: 1; }
  .chat-title { grid-column: 1; grid-row: 1; }
  .message-row { max-width: 96%; }
}
@media (max-width: 680px) {
  .room-chat { border-radius: 18px; min-height: 400px; }
  .chat-header { padding: 10px; min-height: 118px; gap: 9px; }
  .chat-title-mark { width: 38px; height: 38px; flex-basis: 38px; border-radius: 12px; }
  .chat-title strong { font-size: 11px; }
  .chat-title span { font-size: 8px; }
  .room-chat-badge { height: 31px; padding: 0 9px; font-size: 8px; }
  .header-icon-button { width: 38px; height: 38px; }
  .chat-search { height: 38px; }
  .chat-body { padding: 7px; }
  .messages { padding-inline: 1px; }
  .message-row { max-width: 100%; gap: 7px; }
  .message-avatar { width: 31px; height: 31px; flex-basis: 31px; margin-top: 17px; }
  .message-content { max-width: calc(100% - 38px); }
  .message-bubble { font-size: 11px; padding: 8px 11px; }
  .scroll-bottom-button { left: 12px; bottom: 88px; }
  .emoji-picker { right: 7px; bottom: 75px; }
  .emoji-grid { grid-template-columns: repeat(7, 1fr); }
  .composer-counter { display: none; }
  .chat-composer { border-radius: 16px; }
  .send-button { width: 42px; height: 42px; flex-basis: 42px; }
  .composer-tool { width: 39px; height: 39px; flex-basis: 39px; }
  .room-notifications { left: 7px; right: 7px; bottom: 78px; }
  .room-notification { min-width: 0; max-width: none; }
}

@media (prefers-reduced-motion: reduce) {
  .mesh-gradient,
  .react-orb,
  .field-particle,
  .empty-chat-icon,
  .message-row.admin .message-content::before,
  .room-chat-badge.online .room-chat-badge-dot,
  .message-row {
    animation: none !important;
  }
  .messages { scroll-behavior: auto; }
  .message-bubble,
  .header-icon-button,
  .send-button,
  .composer-tool,
  .message-avatar,
  .mouse-spotlight,
  .react-orb,
  .mesh-gradient,
  .ambient-grid {
    transition: none;
  }
}
</style>