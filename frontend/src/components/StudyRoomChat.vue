<template>
  <section
    class="room-chat"
    :class="{ 'is-dark': isDark }"
    @click="handleRoomClick"
  >

    <!-- =====================================================
         HEADER
         ===================================================== -->

    <div class="chat-header">

      <div
        :class="
          socketConnected
            ? 'online'
            : 'offline'
        "
        class="room-chat-badge"
      >
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


    <!-- =====================================================
         CHAT BODY
         ===================================================== -->

    <div class="chat-body">

      <!-- ===================================================
           MESSAGES
           =================================================== -->

      <div
        ref="messagesEl"
        class="messages custom-scrollbar"
        role="log"
        aria-live="polite"
        style="max-height: min(42vh, 390px);"
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


        <!-- =================================================
             MESSAGE LIST
             ================================================= -->

        <template v-else>

          <article
            v-for="message in messages"
            :key="getMessageKey(message)"
            :data-message-id="message.messageId"
            class="message-row"
            :class="{
              mine: message.isMine,
              deleted: message.isDeleted
            }"
            @contextmenu.prevent.stop="
              openMessageMenu(
                $event,
                message
              )
            "
            @touchstart="
              startLongPress(
                $event,
                message
              )
            "
            @touchend="cancelLongPress"
            @touchmove="cancelLongPress"
          >

            <!-- Avatar -->

            <div
              class="message-avatar"
              :class="{
                mine: message.isMine
              }"
            >
              {{ getInitial(message.username) }}
            </div>


            <!-- Message Content -->

            <div class="message-content">

              <!-- Meta -->

              <div class="message-meta">

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


              <!-- =================================================
                   REPLY PREVIEW
                   ================================================= -->

              <div
                v-if="message.replyTo"
                class="message-reply-preview"
                @click.stop="
                  scrollToMessage(
                    message.replyTo.id
                  )
                "
              >

                <span class="reply-preview-line"></span>

                <div class="reply-preview-content">

                  <strong>
                    {{
                      message.replyTo.username ||
                      'کاربر'
                    }}
                  </strong>

                  <span>
                    {{
                      message.replyTo.isDeleted
                        ? 'این پیام حذف شده است'
                        : message.replyTo.message
                    }}
                  </span>

                </div>

              </div>


              <!-- =================================================
                   BUBBLE + ACTION BUTTON
                   ================================================= -->

              <div class="message-bubble-wrap">

                <div
                  class="message-bubble"
                  :class="{
                    deleted: message.isDeleted
                  }"
                >

                  <!-- Deleted -->

                  <template
                    v-if="message.isDeleted"
                  >

                    <span class="deleted-message">

                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                      >
                        <path
                          d="M9 3h6"
                        />

                        <path
                          d="M5 6h14"
                        />

                        <path
                          d="m8 6 .7 13h6.6L16 6"
                        />

                        <path
                          d="M10 10v5M14 10v5"
                        />
                      </svg>

                      این پیام حذف شده است

                    </span>

                  </template>


                  <!-- Normal -->

                  <template v-else>

                    <span class="message-text">
                      {{ message.text }}
                    </span>

                    <span
                      v-if="message.editedAt"
                      class="edited-label"
                    >
                      ویرایش‌شده
                    </span>

                  </template>

                </div>


                <!-- More button -->

                <button
                  v-if="!message.isDeleted"
                  type="button"
                  class="message-more"
                  aria-label="عملیات پیام"
                  title="عملیات پیام"
                  @click.stop="
                    openMessageMenuFromButton(
                      $event,
                      message
                    )
                  "
                >
                  ⋮
                </button>

              </div>


              <!-- =================================================
                   REACTIONS
                   ================================================= -->

              <div
                v-if="
                  !message.isDeleted &&
                  getReactionSummary(message).length
                "
                class="message-reactions"
              >

                <button
                  v-for="
                    reaction in
                    getReactionSummary(message)
                  "
                  :key="reaction.type"
                  type="button"
                  class="reaction-chip"
                  :class="{
                    selected:
                      reaction.myReaction
                  }"
                  @click.stop="
                    toggleReaction(
                      message,
                      reaction.type
                    )
                  "
                >

                  <span>
                    {{
                      getReactionEmoji(
                        reaction.type
                      )
                    }}
                  </span>

                  <small>
                    {{ reaction.count }}
                  </small>

                </button>

              </div>

            </div>

          </article>

        </template>

      </div>


      <!-- =====================================================
           EDIT / REPLY BAR
           ===================================================== -->

      <Transition name="chat-action-bar">

        <div
          v-if="
            editingMessage ||
            replyingTo
          "
          class="chat-action-bar"
        >

          <div class="chat-action-bar-icon">

            <svg
              v-if="editingMessage"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path
                d="M12 20h9"
              />

              <path
                d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"
              />
            </svg>

            <svg
              v-else
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path
                d="M9 14 4 9l5-5"
              />

              <path
                d="M4 9h10a6 6 0 0 1 6 6v1"
              />
            </svg>

          </div>


          <div class="chat-action-bar-content">

            <strong>
              {{
                editingMessage
                  ? 'ویرایش پیام'
                  : 'پاسخ به پیام'
              }}
            </strong>

            <span>
              {{
                editingMessage
                  ? editingMessage.text
                  : (
                      replyingTo?.isDeleted
                        ? 'این پیام حذف شده است'
                        : replyingTo?.text
                    )
              }}
            </span>

          </div>


          <button
            type="button"
            class="chat-action-bar-close"
            aria-label="لغو"
            @click="cancelAction"
          >
            ×
          </button>

        </div>

      </Transition>


      <!-- =====================================================
           COMPOSER
           ===================================================== -->

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
          :placeholder="
            editingMessage
              ? 'متن پیام را ویرایش کن...'
              : replyingTo
                ? 'پاسخت را بنویس...'
                : 'پیامت را برای اعضای سالن بنویس...'
          "
          @keydown.enter.exact.prevent="
            sendMessage
          "
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
          :aria-label="
            editingMessage
              ? 'ذخیره ویرایش'
              : replyingTo
                ? 'ارسال پاسخ'
                : 'ارسال پیام'
          "
        >

          <span
            v-if="sending"
            class="send-loader"
          ></span>


          <!-- Save edit -->

          <svg
            v-else-if="editingMessage"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <path
              d="m5 12 4 4L19 6"
            />
          </svg>


          <!-- Send -->

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


    <!-- =====================================================
         MESSAGE CONTEXT MENU
         ===================================================== -->

    <Transition name="message-menu">

      <div
        v-if="contextMenu.visible"
        ref="contextMenuEl"
        class="message-context-menu"
        :style="contextMenuStyle"
        @click.stop
      >

        <!-- Header -->

        <div class="context-menu-user">

          <div class="context-menu-avatar">
            {{
              getInitial(
                contextMenu.message?.username
              )
            }}
          </div>

          <div>

            <strong>
              {{
                contextMenu.message?.username ||
                'کاربر'
              }}
            </strong>

            <span>
              {{
                contextMenu.message?.isMine
                  ? 'پیام شما'
                  : 'پیام کاربر'
              }}
            </span>

          </div>

        </div>


        <div class="context-menu-divider"></div>


        <!-- Reply -->

        <button
          type="button"
          class="context-menu-item"
          @click="
            replyToMessage(
              contextMenu.message
            )
          "
        >

          <span class="context-menu-item-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path
                d="M9 14 4 9l5-5"
              />

              <path
                d="M4 9h10a6 6 0 0 1 6 6v1"
              />
            </svg>
          </span>

          <span>
            پاسخ
          </span>

        </button>


        <!-- Reaction -->

        <button
          v-if="
            !contextMenu.message?.isDeleted
          "
          type="button"
          class="context-menu-item"
          @click="toggleReactionMenu"
        >

          <span class="context-menu-item-icon">
            <span class="reaction-face">
              😀
            </span>
          </span>

          <span>
            واکنش
          </span>

          <span class="context-menu-arrow">
            ‹
          </span>

        </button>


        <!-- Reaction Picker -->

        <div
          v-if="contextMenu.showReactions"
          class="reaction-picker"
        >

          <button
            v-for="type in reactionTypes"
            :key="type"
            type="button"
            class="reaction-picker-button"
            :class="{
              selected:
                getUserReaction(
                  contextMenu.message
                ) === type
            }"
            :title="
              getReactionLabel(type)
            "
            @click="
              selectReactionFromMenu(
                type
              )
            "
          >
            {{
              getReactionEmoji(type)
            }}
          </button>

        </div>


        <!-- Edit -->

        <button
          v-if="
            contextMenu.message &&
            contextMenu.message.isMine &&
            !contextMenu.message.isDeleted
          "
          type="button"
          class="context-menu-item"
          @click="
            startEditMessage(
              contextMenu.message
            )
          "
        >

          <span class="context-menu-item-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path
                d="M12 20h9"
              />

              <path
                d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"
              />
            </svg>
          </span>

          <span>
            ویرایش
          </span>

        </button>


        <!-- Delete -->

        <button
          v-if="
            contextMenu.message &&
            contextMenu.message.isMine &&
            !contextMenu.message.isDeleted
          "
          type="button"
          class="context-menu-item danger"
          @click="
            deleteMessage(
              contextMenu.message
            )
          "
        >

          <span class="context-menu-item-icon">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path
                d="M9 3h6"
              />

              <path
                d="M5 6h14"
              />

              <path
                d="m8 6 .7 13h6.6L16 6"
              />

              <path
                d="M10 10v5M14 10v5"
              />
            </svg>

          </span>

          <span>
            حذف
          </span>

        </button>

      </div>

    </Transition>

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

const messagesEl =
  ref(null)

const inputEl =
  ref(null)

const contextMenuEl =
  ref(null)


/* =========================================================
   STATE
   ========================================================= */

const messages =
  ref([])

const draft =
  ref('')

const loadingHistory =
  ref(false)

const sending =
  ref(false)

const socketConnected =
  ref(false)

const isDark =
  ref(false)


/* =========================================================
   CHAT ACTION STATE
   ========================================================= */

const editingMessage =
  ref(null)

const replyingTo =
  ref(null)


/* =========================================================
   CONTEXT MENU
   ========================================================= */

const contextMenu =
  ref({

    visible: false,

    x: 0,

    y: 0,

    message: null,

    showReactions: false,

  })


const contextMenuStyle =
  ref({})


/* =========================================================
   REACTIONS
   ========================================================= */

const reactionTypes = [
  'cry',
  'laugh',
  'heart',
  'like',
  'dislike',
]


const reactionEmojis = {

  cry: '😢',

  laugh: '😂',

  heart: '❤️',

  like: '👍',

  dislike: '👎',

}


const reactionLabels = {

  cry: 'گریه',

  laugh: 'خنده',

  heart: 'قلب',

  like: 'لایک',

  dislike: 'دیسلایک',

}


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

let longPressTimer =
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


  const replyRaw =
    source.reply_to ??
    null


  const replyTo =
    replyRaw
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
            'کاربر',

          message:
            replyRaw.message ??
            replyRaw.text ??
            '',

          isDeleted:
            Boolean(
              replyRaw.is_deleted
            ),

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

    text:
      typeof text === 'string'
        ? text.trim()
        : '',

    createdAt,

    editedAt:
      source.edited_at ??
      null,

    isDeleted:
      Boolean(
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

    return (
      `message-${message.messageId}`
    )

  }

  return (
    `client-${message.clientId}`
  )

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

    messages.value[index] = {

      ...messages.value[index],

      ...message,

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


  /* =====================================================
     CONNECTION
     ===================================================== */

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


  /* =====================================================
     HISTORY
     ===================================================== */

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


  /* =====================================================
     NEW MESSAGE
     ===================================================== */

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


  /* =====================================================
     EDITED
     ===================================================== */

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


  /* =====================================================
     DELETED
     ===================================================== */

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


  /* =====================================================
     REACTION UPDATED
     ===================================================== */

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


  /* =====================================================
     REACTION REMOVED
     ===================================================== */

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


  messages.value[index] = {

    ...messages.value[index],

    ...message,

    isMine:
      messages.value[index]
        .isMine,

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


  messages.value[index] = {

    ...messages.value[index],

    ...message,

    isDeleted:
      true,

    text:
      '',

    isMine:
      messages.value[index]
        .isMine,

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
    ...(message.reactions || [])
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


/* =========================================================
   SEND / EDIT
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


  /* =====================================================
     EDIT
     ===================================================== */

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


  /* =====================================================
     NORMAL / REPLY
     ===================================================== */

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
    ...message
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
    ...message
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


  cancelLongPress()


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

})

</script>


<style scoped>

/* =========================================================
   ROOM CHAT
   ========================================================= */

.room-chat {

  --chat-bg:
    var(
      --app-card,
      #ffffff
    );

  --chat-border:
    var(
      --border,
      rgba(
        148,
        163,
        184,
        .18
      )
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
    visible;

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


/* =========================================================
   ORIGINAL STATUS BADGE
   ========================================================= */

.room-chat-badge {

  display:
    inline-flex;

  align-items:
    center;

  gap:
    7px;

  padding:
    7px 10px;

  border-radius:
    999px;

  color:
    #047857;

  background:
    #ecfdf5;

  border:
    1px solid
    #d1fae5;

  font-size:
    10px;

  font-weight:
    850;

  white-space:
    nowrap;

}


.room-chat-badge.offline {

  color:
    #64748b;

  background:
    #f1f5f9;

  border-color:
    #e2e8f0;

}


.room-chat-badge-dot,
.room-chat-badge-dot::after {

  width:
    7px;

  height:
    7px;

  border-radius:
    50%;

}


.room-chat-badge-dot {

  position:
    relative;

  background:
    #10b981;

}


.room-chat-badge.offline
.room-chat-badge-dot {

  background:
    #94a3b8;

}


.room-chat-badge-dot::after {

  content:
    "";

  position:
    absolute;

  inset:
    0;

  background:
    #10b981;

  animation:
    roomChatPulse
    1.8s
    infinite
    ease-out;

}


.room-chat-badge.offline
.room-chat-badge-dot::after {

  display:
    none;

}


@keyframes roomChatPulse {

  0% {

    transform:
      scale(1);

    opacity:
      .45;

  }

  70%,
  100% {

    transform:
      scale(2.5);

    opacity:
      0;

  }

}


.study-room-page.is-dark
.room-chat-badge {

  color:
    #6ee7b7;

  background:
    rgba(
      16,
      185,
      129,
      .10
    );

  border-color:
    rgba(
      16,
      185,
      129,
      .18
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
   MESSAGE ROW
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

  touch-action:
    pan-y;

}


.message-row.mine {

  margin-right:
    auto;

  flex-direction:
    row-reverse;

}


/* =========================================================
   AVATAR
   ========================================================= */

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


/* =========================================================
   MESSAGE CONTENT
   ========================================================= */

.message-content {

  min-width:
    0;

}


.message-row.mine
.message-content {

  text-align:
    right;

}


/* =========================================================
   META
   ========================================================= */

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


/* =========================================================
   REPLY PREVIEW
   ========================================================= */

.message-reply-preview {

  display:
    flex;

  align-items:
    stretch;

  max-width:
    100%;

  margin:
    0 0 4px;

  padding:
    5px 7px;

  box-sizing:
    border-box;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    9px;

  background:
    var(--chat-soft);

  cursor:
    pointer;

  text-align:
    right;

}


.message-reply-preview:hover {

  border-color:
    rgba(
      var(--primary-rgb),
      .25
    );

}


.reply-preview-line {

  width:
    3px;

  flex:
    0 0 3px;

  margin-left:
    7px;

  border-radius:
    5px;

  background:
    var(--primary);

}


.reply-preview-content {

  min-width:
    0;

  display:
    flex;

  flex-direction:
    column;

  overflow:
    hidden;

}


.reply-preview-content strong {

  color:
    var(--primary);

  font-size:
    9px;

  font-weight:
    850;

}


.reply-preview-content span {

  overflow:
    hidden;

  color:
    var(--chat-muted);

  font-size:
    9px;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;

}


/* =========================================================
   BUBBLE WRAP
   ========================================================= */

.message-bubble-wrap {

  display:
    flex;

  align-items:
    flex-end;

  gap:
    3px;

}


.message-row.mine
.message-bubble-wrap {

  flex-direction:
    row-reverse;

}


/* =========================================================
   BUBBLE
   ========================================================= */

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


.message-bubble.deleted {

  color:
    var(--chat-muted);

  background:
    transparent;

  border-style:
    dashed;

}


.deleted-message {

  display:
    inline-flex;

  align-items:
    center;

  gap:
    5px;

  font-size:
    11px;

  font-style:
    italic;

}


.deleted-message svg {

  width:
    14px;

  height:
    14px;

}


/* =========================================================
   EDITED
   ========================================================= */

.edited-label {

  display:
    inline-block;

  margin-right:
    6px;

  color:
    rgba(
      255,
      255,
      255,
      .65
    );

  font-size:
    8px;

}


.message-row:not(.mine)
.edited-label {

  color:
    var(--chat-muted);

}


/* =========================================================
   MORE BUTTON
   ========================================================= */

.message-more {

  width:
    24px;

  height:
    24px;

  flex:
    0 0 24px;

  display:
    grid;

  place-items:
    center;

  padding:
    0;

  border:
    0;

  border-radius:
    8px;

  background:
    transparent;

  color:
    var(--chat-muted);

  font-size:
    17px;

  line-height:
    1;

  cursor:
    pointer;

  opacity:
    0;

  transition:
    opacity .15s ease,
    background .15s ease,
    color .15s ease;

}


.message-row:hover
.message-more {

  opacity:
    1;

}


.message-more:hover {

  color:
    var(--chat-text);

  background:
    var(--chat-soft);

}


@media (hover: none) {

  .message-more {

    opacity:
      .75;

  }

}


/* =========================================================
   REACTIONS
   ========================================================= */

.message-reactions {

  display:
    flex;

  flex-wrap:
    wrap;

  align-items:
    center;

  gap:
    4px;

  margin-top:
    4px;

}


.message-row.mine
.message-reactions {

  justify-content:
    flex-end;

}


.reaction-chip {

  display:
    inline-flex;

  align-items:
    center;

  gap:
    3px;

  min-height:
    23px;

  padding:
    2px 6px;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    999px;

  background:
    var(--chat-bg);

  color:
    var(--chat-text);

  cursor:
    pointer;

  font-family:
    inherit;

  transition:
    border-color .15s ease,
    background .15s ease,
    transform .15s ease;

}


.reaction-chip:hover {

  transform:
    translateY(-1px);

  border-color:
    rgba(
      var(--primary-rgb),
      .35
    );

}


.reaction-chip.selected {

  border-color:
    var(--primary);

  background:
    var(--chat-soft);

}


.reaction-chip span {

  font-size:
    12px;

}


.reaction-chip small {

  font-size:
    9px;

  font-weight:
    800;

}


/* =========================================================
   ACTION BAR
   ========================================================= */

.chat-action-bar {

  display:
    flex;

  align-items:
    center;

  gap:
    9px;

  min-height:
    48px;

  margin:
    0 0 7px;

  padding:
    6px 9px;

  box-sizing:
    border-box;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    13px;

  background:
    var(--chat-soft);

}


.chat-action-bar-icon {

  width:
    31px;

  height:
    31px;

  flex:
    0 0 31px;

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
      .08
    );

}


.chat-action-bar-icon svg {

  width:
    16px;

  height:
    16px;

}


.chat-action-bar-content {

  min-width:
    0;

  flex:
    1;

  display:
    flex;

  flex-direction:
    column;

}


.chat-action-bar-content strong {

  color:
    var(--primary);

  font-size:
    9px;

  font-weight:
    850;

}


.chat-action-bar-content span {

  overflow:
    hidden;

  color:
    var(--chat-muted);

  font-size:
    9px;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;

}


.chat-action-bar-close {

  width:
    28px;

  height:
    28px;

  display:
    grid;

  place-items:
    center;

  padding:
    0;

  border:
    0;

  border-radius:
    8px;

  background:
    transparent;

  color:
    var(--chat-muted);

  font-size:
    18px;

  cursor:
    pointer;

}


.chat-action-bar-close:hover {

  color:
    var(--chat-text);

  background:
    var(--chat-bg);

}


.chat-action-bar-enter-active,
.chat-action-bar-leave-active {

  transition:
    opacity .15s ease,
    transform .15s ease;

}


.chat-action-bar-enter-from,
.chat-action-bar-leave-to {

  opacity:
    0;

  transform:
    translateY(5px);

}


/* =========================================================
   CONTEXT MENU
   ========================================================= */

.message-context-menu {

  position:
    fixed;

  z-index:
    9999;

  width:
    225px;

  box-sizing:
    border-box;

  padding:
    7px;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    16px;

  background:
    var(--chat-bg);

  box-shadow:
    0 18px 45px
    rgba(
      15,
      23,
      42,
      .16
    );

  direction:
    rtl;

}


.context-menu-user {

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  padding:
    6px 6px 8px;

}


.context-menu-avatar {

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

  color:
    var(--primary);

  background:
    var(--chat-soft);

  font-size:
    11px;

  font-weight:
    850;

}


.context-menu-user > div:last-child {

  min-width:
    0;

  display:
    flex;

  flex-direction:
    column;

}


.context-menu-user strong {

  overflow:
    hidden;

  color:
    var(--chat-text);

  font-size:
    10px;

  white-space:
    nowrap;

  text-overflow:
    ellipsis;

}


.context-menu-user span {

  color:
    var(--chat-muted);

  font-size:
    8px;

}


.context-menu-divider {

  height:
    1px;

  margin:
    2px 4px 5px;

  background:
    var(--chat-border);

}


.context-menu-item {

  width:
    100%;

  min-height:
    38px;

  display:
    flex;

  align-items:
    center;

  gap:
    8px;

  padding:
    5px 7px;

  border:
    0;

  border-radius:
    10px;

  background:
    transparent;

  color:
    var(--chat-text);

  font-family:
    inherit;

  font-size:
    11px;

  text-align:
    right;

  cursor:
    pointer;

  transition:
    background .15s ease,
    color .15s ease;

}


.context-menu-item:hover {

  background:
    var(--chat-soft);

}


.context-menu-item.danger {

  color:
    #ef4444;

}


.context-menu-item.danger:hover {

  background:
    rgba(
      239,
      68,
      68,
      .08
    );

}


.context-menu-item-icon {

  width:
    28px;

  height:
    28px;

  flex:
    0 0 28px;

  display:
    grid;

  place-items:
    center;

  border-radius:
    8px;

  background:
    var(--chat-soft);

}


.context-menu-item-icon svg {

  width:
    15px;

  height:
    15px;

}


.reaction-face {

  font-size:
    14px;

}


.context-menu-arrow {

  margin-right:
    auto;

  color:
    var(--chat-muted);

  font-size:
    17px;

}


/* =========================================================
   REACTION PICKER
   ========================================================= */

.reaction-picker {

  display:
    flex;

  align-items:
    center;

  justify-content:
    center;

  gap:
    2px;

  margin:
    3px 4px 5px;

  padding:
    5px;

  border:
    1px solid
    var(--chat-border);

  border-radius:
    11px;

  background:
    var(--chat-soft);

}


.reaction-picker-button {

  width:
    34px;

  height:
    34px;

  display:
    grid;

  place-items:
    center;

  padding:
    0;

  border:
    0;

  border-radius:
    9px;

  background:
    transparent;

  font-size:
    17px;

  cursor:
    pointer;

  transition:
    transform .15s ease,
    background .15s ease;

}


.reaction-picker-button:hover {

  transform:
    scale(1.12);

  background:
    var(--chat-bg);

}


.reaction-picker-button.selected {

  background:
    var(--chat-bg);

  box-shadow:
    inset 0 0 0 1px
    var(--primary);

}


/* =========================================================
   MENU ANIMATION
   ========================================================= */

.message-menu-enter-active,
.message-menu-leave-active {

  transition:
    opacity .12s ease,
    transform .12s ease;

}


.message-menu-enter-from,
.message-menu-leave-to {

  opacity:
    0;

  transform:
    scale(.95)
    translateY(-4px);

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
   MESSAGE HIGHLIGHT
   ========================================================= */

.message-highlight
.message-bubble {

  animation:
    messageHighlight
    1s
    ease;

}


@keyframes messageHighlight {

  0%,
  100% {

    box-shadow:
      none;

  }

  50% {

    box-shadow:
      0 0 0 4px
      rgba(
        var(--primary-rgb),
        .20
      );

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


  .message-row {

    max-width:
      94%;

  }


  .message-context-menu {

    width:
      min(
        225px,
        calc(
          100vw - 20px
        )
      );

  }

}


/* =========================================================
   SMALL MOBILE
   ========================================================= */

@media (
  max-width: 480px
) {

  .room-chat {

    padding:
      14px;

  }


  .message-row {

    max-width:
      96%;

  }


  .message-avatar {

    width:
      32px;

    height:
      32px;

    flex-basis:
      32px;

    border-radius:
      10px;

  }


  .message-bubble {

    font-size:
      11px;

    padding:
      9px 11px;

  }


  .message-meta strong {

    font-size:
      9px;

  }

}

</style>