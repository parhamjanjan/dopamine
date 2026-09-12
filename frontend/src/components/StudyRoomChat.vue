```vue
<template>
  <section
    class="room-chat"
    :class="{ 'is-dark': isDark }"
  >

    <!-- ==============================
         HEADER
         ============================== -->
    <div class="chat-header">

      


      

      <div :class="
          socketConnected
            ? 'online'
            : 'offline'
        " class="room-chat-badge">
              <span class="room-chat-badge-dot"></span>
              <span>
          {{
            socketConnected
              ? 'آنلاین'
              : 'اتصال قطع است'
          }}
        </span>
      </div>

    </div>


    <!-- ==============================
         CHAT BODY
         ============================== -->
    <div class="chat-body">

      <!-- Messages -->
      <div style="  max-height: min(42vh, 390px);"
        ref="messagesEl"
        class="messages custom-scrollbar"
        role="log"
        aria-live="polite"
      >

        <!-- Loading -->
        <div
          v-if="loadingHistory"
          class="chat-state"
        >

          <span class="mini-loader"></span>

          <span>
            در حال دریافت پیام‌ها...
          </span>

        </div>


        <!-- Empty -->
        <div
          v-else-if="messages.length === 0"
          class="empty-chat"
        >

          <div class="empty-chat-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.7"
            >
              <path d="M8 10h8M8 14h5" />

              <path
                d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5
                   8.3 8.3 0 0 1-3.1-.6L4 20l1.6-4.2
                   A7.5 7.5 0 1 1 20 11.5Z"
              />
            </svg>

          </div>

          <h3>
            هنوز پیامی ارسال نشده
          </h3>

          <p>
            اولین پیام را بفرست و گفت‌وگوی سالن را شروع کن.
          </p>

        </div>


        <!-- Message List -->
        <template v-else>

          <article
            v-for="message in messages"
            :key="message.clientId"
            class="message-row"
            :class="{
              mine: message.isMine
            }"
          >

            <div
              class="message-avatar"
              :class="{
                mine: message.isMine
              }"
            >
              {{ getInitial(message.username) }}
            </div>

            <div
              class="message-content"
            >

              <div
                class="message-meta"
              >

                <strong>
                  {{
                    message.isMine
                      ? 'شما'
                      : message.username
                  }}
                </strong>

                <time>
                  {{
                    formatTime(
                      message.createdAt
                    )
                  }}
                </time>

              </div>

              <div class="message-bubble">
                {{ message.text }}
              </div>

            </div>

          </article>

        </template>

      </div>


      <!-- ============================
           COMPOSER
           خارج از Messages
           ============================ -->
      <form
        class="chat-composer"
        @submit.prevent="sendMessage"
      >

        <textarea
          ref="inputEl"
          v-model="draft"
          class="chat-input"
          rows="1"
          maxlength="1000"
          :disabled="
            sending ||
            !socketConnected
          "
          placeholder="پیامت را برای اعضای سالن بنویس..."
          @keydown.enter.exact.prevent="sendMessage"
          @input="autoResize"
        ></textarea>


        <button
          type="submit"
          class="send-button"
          :disabled="
            sending ||
            !socketConnected ||
            !draft.trim()
          "
          aria-label="ارسال پیام"
        >

          <span
            v-if="sending"
            class="send-loader"
          ></span>


          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <path
              d="m22 2-7 20-4-9-9-4Z"
            />

            <path
              d="M22 2 11 13"
            />
          </svg>

        </button>

      </form>

    </div>

  </section>
</template>


<script setup>

import {
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
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

const messagesEl = ref(null)
const inputEl = ref(null)


/* =========================================================
   STATE
   ========================================================= */

const messages = ref([])

const draft = ref('')

const loadingHistory =
  ref(false)

const sending =
  ref(false)

const socketConnected =
  ref(false)

const isDark =
  ref(false)


/* =========================================================
   INTERNAL
   ========================================================= */

let socket = null

let reconnectTimer =
  null

let reconnectAttempts =
  0

let destroyed =
  false

let themeObserver =
  null

let localUserId =
  null

let localUsername =
  ''


const MAX_MESSAGES =
  300


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

  const root =
    document.documentElement

  const body =
    document.body

  const dataTheme =
    root.getAttribute(
      'data-theme'
    ) ||
    body?.getAttribute(
      'data-theme'
    )

  return (
    dataTheme === 'dark' ||

    root.classList.contains(
      'dark'
    ) ||

    body?.classList.contains(
      'dark'
    ) ||

    root.classList.contains(
      'dark-mode'
    ) ||

    body?.classList.contains(
      'dark-mode'
    )
  )

}


function observeTheme() {

  isDark.value =
    detectDark()


  themeObserver =
    new MutationObserver(
      () => {

        isDark.value =
          detectDark()

      }
    )


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
   NORMALIZE MESSAGE
   ========================================================= */

function normalizeMessage(raw) {

  if (!raw) {
    return null
  }


  const text =
    raw.message ??
    raw.text ??
    raw.content ??
    raw.body


  if (
    typeof text !== 'string' ||
    !text.trim()
  ) {

    return null

  }


  const senderId =
    raw.user_id ??
    raw.sender_id ??
    raw.sender?.id ??
    raw.author_id ??
    null


  const username =
    raw.username ??
    raw.sender_username ??
    raw.sender?.username ??
    raw.user?.username ??
    'کاربر'


  const createdAt =
    raw.created_at ??
    raw.timestamp ??
    new Date().toISOString()


  const clientId =
    String(
      raw.client_id ??
      raw.id ??
      raw.message_id ??
      `${senderId || 'u'}-${createdAt}-${Math.random()
        .toString(36)
        .slice(2, 8)}`
    )


  return {

    clientId,

    senderId,

    username,

    text:
      text.trim(),

    createdAt,

    isMine:
      senderId != null &&
      localUserId != null &&
      String(senderId) ===
        String(localUserId),

  }

}


/* =========================================================
   PUSH MESSAGE
   ========================================================= */

function pushMessage(message) {

  if (!message) {
    return
  }


  const duplicate =
    messages.value.some(
      item =>
        item.clientId ===
        message.clientId
    )


  if (duplicate) {
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


  /* -----------------------------------------------
     Connection
     ----------------------------------------------- */

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
        String(serverUserId)
      )

    }


    localUsername =
  data.username ??
  data.user?.username ??
  localStorage.getItem('username') ??
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


  /* -----------------------------------------------
     History
     ----------------------------------------------- */

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
        .slice(-MAX_MESSAGES)


    loadingHistory.value =
      false


    scrollToBottom()

    return

  }


  /* -----------------------------------------------
     Chat message
     ----------------------------------------------- */

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


    if (
      message.isMine
    ) {

      sending.value =
        false

    }


    return

  }

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


/* =========================================================
   SEND MESSAGE
   ========================================================= */

function sendMessage() {

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


  const clientId =
    `local-${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 8)}`


  sending.value =
    true


  try {

    socket.send(
      JSON.stringify({

        type:
          'chat_message',

        message:
          text,

        client_id:
          clientId,

      })
    )


    /*
     * پیام را اینجا به صورت محلی
     * اضافه نمی‌کنیم.
     *
     * Consumer بک‌اند آن را ذخیره
     * و سپس broadcast می‌کند.
     */


    draft.value =
      ''


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
    new Date(value)


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
   MOUNTED
   ========================================================= */

onMounted(() => {

  const storedUserId =
    localStorage.getItem(
      'user_id'
    )


  if (storedUserId) {

    localUserId =
      storedUserId

  }


  localUsername =
    localStorage.getItem(
      'username'
    ) || ''


  observeTheme()

  connect()


  nextTick(() => {

    autoResize()

  })

})


/* =========================================================
   UNMOUNTED
   ========================================================= */

onBeforeUnmount(() => {

  destroyed =
    true


  if (reconnectTimer) {

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

})

</script>


<style scoped>

/* =========================================================
   ROOM CHAT
   ========================================================= */

.room-chat {

  --chat-bg:
    var(--app-card, #ffffff);

  --chat-border:
    var(
      --border,
      rgba(148, 163, 184, .18)
    );

  --chat-text:
    var(
      --text-main,
      #0f172a
    );

  --chat-muted:
    var(
      --text-muted,
      #64748b
    );

  --chat-soft:
    var(
      --primary-50,
      #f8f7ff
    );

  --chat-shadow:
    0 18px 45px
    rgba(
      15,
      23,
      42,
      .06
    );


  width:
    100%;

  margin:
    0 0 18px;

  padding:
    20px;

  box-sizing:
    border-box;

  display:
    flex;

  flex-direction:
    column;

  overflow:
    hidden;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    24px;

  background:
    var(--chat-bg);

  box-shadow:
    var(--chat-shadow);

  color:
    var(--chat-text);

}


/* =========================================================
   DARK
   ========================================================= */

.room-chat.is-dark {

  --chat-bg:
    #111827;

  --chat-border:
    #243047;

  --chat-text:
    #f8fafc;

  --chat-muted:
    #94a3b8;

  --chat-soft:
    rgba(
      var(--primary-rgb),
      .09
    );

  --chat-shadow:
    0 18px 45px
    rgba(
      0,
      0,
      0,
      .18
    );

}


/* =========================================================
   HEADER
   ========================================================= */

.chat-header {

  width:
    100%;

  min-height:
    46px;

  display:
    flex;

  align-items:
    center;

  justify-content:
    space-between;

  gap:
    16px;

  flex:
    0 0 auto;

  margin:
    0 0 16px;

}


.chat-title-wrap {

  display:
    flex;

  align-items:
    center;

  gap:
    12px;

  min-width:
    0;

}


.chat-icon {

  width:
    46px;

  height:
    46px;

  flex:
    0 0 46px;

  display:
    grid;

  place-items:
    center;

  border:
    1px solid
    rgba(
      var(--primary-rgb),
      .14
    );

  border-radius:
    15px;

  background:
    var(--chat-soft);

  color:
    var(--primary);

}


.chat-icon svg {

  width:
    23px;

  height:
    23px;

}


.chat-heading {

  min-width:
    0;

}


.chat-eyebrow {

  display:
    block;

  margin:
    0 0 3px;

  color:
    var(--primary);

  font-size:
    10px;

  font-weight:
    800;

}


.chat-title-wrap h2 {

  margin:
    0;

  font-size:
    19px;

  font-weight:
    850;

}


/* =========================================================
   STATUS
   ========================================================= */

.chat-status {

  display:
    inline-flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    6px;

  flex:
    0 0 auto;

  padding:
    7px 10px;

  border-radius:
    999px;

  font-size:
    10px;

  font-weight:
    800;

}


.chat-status.online {

  color:
    #047857;

  background:
    #ecfdf5;

}


.chat-status.offline {

  color:
    #64748b;

  background:
    #f1f5f9;

}


.chat-status
.status-dot {

  width:
    7px;

  height:
    7px;

  flex:
    0 0 7px;

  border-radius:
    50%;

  background:
    #94a3b8;

}


.chat-status.online
.status-dot {

  background:
    #10b981;

  box-shadow:
    0 0 0 4px
    rgba(
      16,
      185,
      129,
      .1
    );

}


/* =========================================================
   CHAT BODY
   ========================================================= */

.chat-body {

  width:
    100%;

  display:
    flex;

  flex-direction:
    column;

  flex:
    0 0 auto;

  min-height:
    0;

}


/* =========================================================
   MESSAGES
   ========================================================= */

.messages {

  width:
    100%;

  

  box-sizing:
    border-box;

  padding:
    8px 4px 14px;

  overflow-y:
    auto;

  overflow-x:
    hidden;

  scroll-behavior:
    smooth;

}


/* =========================================================
   MESSAGE
   ========================================================= */

.message-row {

  display:
    flex;

  align-items:
    flex-end;

  gap:
    9px;

  max-width:
    88%;

  margin:
    0 0 12px;

}


.message-row.mine {

  margin-right:
    auto;

  flex-direction:
    row-reverse;

}


.message-avatar {

  width:
    36px;

  height:
    36px;

  flex:
    0 0 36px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    12px;

  color:
    var(--primary);

  background:
    var(--chat-soft);

  font-size:
    12px;

  font-weight:
    850;

}


.message-avatar.mine {

  color:
    #fff;

  background:
    linear-gradient(
      135deg,
      var(--primary),
      color-mix(
        in srgb,
        var(--primary)
        72%,
        #0f172a
      )
    );

}


.message-content {

  min-width:
    0;

}


.message-row.mine
.message-content {

  text-align:
    right;

}


.message-meta {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  margin:
    0 0 4px;

  padding:
    0 3px;

}


.message-meta strong {

  font-size:
    10px;

  font-weight:
    800;

}


.message-meta time {

  color:
    var(--chat-muted);

  font-size:
    8px;

}


.message-bubble {

  padding:
    10px 13px;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    15px 15px 15px 5px;

  background:
    var(--chat-soft);

  color:
    var(--chat-text);

  font-size:
    12px;

  line-height:
    1.9;

  white-space:
    pre-wrap;

  overflow-wrap:
    anywhere;

}


.message-row.mine
.message-bubble {

  border-color:
    transparent;

  border-radius:
    15px 15px 5px 15px;

  color:
    #fff;

  background:
    linear-gradient(
      135deg,
      var(--primary),
      color-mix(
        in srgb,
        var(--primary)
        82%,
        #0f172a
      )
    );

}


/* =========================================================
   COMPOSER
   ========================================================= */

.chat-composer {
  
  z-index:
    50;

  width:
    100%;

  min-height:
    56px;

  flex:
    0 0 auto;

  display:
    flex;

  align-items:
    flex-end;

  gap:
    9px;

  box-sizing:
    border-box;

  
  padding:
    7px;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    18px;

  background:
    var(--chat-soft);

}


.chat-input {

  display:
    block;

  width:
    100%;

  min-width:
    0;

  min-height:
    42px;

  max-height:
    120px;

  flex:
    1 1 auto;

  resize:
    none;

  overflow-y:
    auto;

  box-sizing:
    border-box;

  border:
    0;

  outline:
    none;

  background:
    transparent;

  color:
    var(--chat-text);

  font-family:
    inherit;

  font-size:
    12px;

  line-height:
    1.8;

  padding:
    9px 10px;

}


.chat-input:disabled {

  opacity:
    .65;

  cursor:
    not-allowed;

}


.chat-input::placeholder {

  color:
    var(--chat-muted);

}


/* =========================================================
   SEND BUTTON
   ========================================================= */

.send-button {

  width:
    42px;

  height:
    42px;

  flex:
    0 0 42px;

  display:
    grid;

  place-items:
    center;

  box-sizing:
    border-box;

  border:
    0;

  border-radius:
    13px;

  color:
    #fff;

  background:
    var(--primary);

  cursor:
    pointer;

  transition:
    transform .2s ease,
    opacity .2s ease,
    box-shadow .2s ease;

  box-shadow:
    0 8px 20px
    rgba(
      var(--primary-rgb),
      .20
    );

}


.send-button:hover:not(:disabled) {

  transform:
    translateY(-1px);

  box-shadow:
    0 11px 25px
    rgba(
      var(--primary-rgb),
      .28
    );

}


.send-button:disabled {

  opacity:
    .45;

  cursor:
    not-allowed;

  box-shadow:
    none;

}


.send-button svg {

  width:
    19px;

  height:
    19px;

}


/* =========================================================
   EMPTY / LOADING
   ========================================================= */

.chat-state,
.empty-chat {

  width:
    100%;

  min-height:
    350px;

  box-sizing:
    border-box;

  display:
    flex;

  flex-direction:
    column;

  align-items:
    center;

  justify-content:
    center;

  gap:
    9px;

  text-align:
    center;

  color:
    var(--chat-muted);

  font-size:
    12px;

}


.empty-chat-icon {

  width:
    58px;

  height:
    58px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    17px;

  background:
    var(--chat-soft);

  color:
    var(--primary);

}


.empty-chat-icon svg {

  width:
    28px;

  height:
    28px;

}


.empty-chat h3 {

  margin:
    0;

  color:
    var(--chat-text);

  font-size:
    14px;

  font-weight:
    800;

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

.study-room-page.is-dark .room-chat-badge {
  color: #6ee7b7;
  background: rgba(16,185,129,.10);
  border-color: rgba(16,185,129,.18);
}

.empty-chat p {

  margin:
    0;

  color:
    var(--chat-muted);

  font-size:
    11px;

}


/* =========================================================
   LOADERS
   ========================================================= */

.mini-loader,
.send-loader {

  border-radius:
    50%;

  animation:
    chat-spin .7s
    linear infinite;

}


.mini-loader {

  width:
    19px;

  height:
    19px;

  border:
    2px solid
    rgba(
      var(--primary-rgb),
      .2
    );

  border-top-color:
    var(--primary);

}


.send-loader {

  width:
    15px;

  height:
    15px;

  border:
    2px solid
    rgba(
      255,
      255,
      255,
      .35
    );

  border-top-color:
    #fff;

}


@keyframes chat-spin {

  to {
    transform:
      rotate(360deg);
  }

}


/* =========================================================
   MOBILE
   ========================================================= */

@media (
  max-width: 760px
) {

  .room-chat {

    padding:
      16px;

    border-radius:
      20px;

  }


  .chat-header {

    align-items:
      flex-start;

  }


  .chat-title-wrap {

    gap:
      9px;

  }


  .chat-icon {

    width:
      42px;

    height:
      42px;

    flex-basis:
      42px;

    border-radius:
      13px;

  }


  .chat-icon svg {

    width:
      21px;

    height:
      21px;

  }


  .chat-title-wrap h2 {

    font-size:
      17px;

  }


 


  .message-row {

    max-width:
      94%;

  }

}


@media (
  max-width: 480px
) {

  .chat-header {

    gap:
      8px;

  }


  .chat-status {

    padding:
      6px 8px;

    font-size:
      9px;

  }


  .chat-title-wrap h2 {

    font-size:
      16px;

  }


  .chat-eyebrow {

    font-size:
      9px;

  }


 

}
</style>
