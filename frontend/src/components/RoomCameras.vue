<template>
  <section class="room-cameras" :class="{ 'theme-dark': isDarkTheme }">
    <div class="camera-shell">
      <header class="cameras-header">
        <div class="camera-heading">
          <div class="heading-icon" aria-hidden="true">
            <svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 10.5V7.25A2.25 2.25 0 0 0 12.75 5h-7.5A2.25 2.25 0 0 0 3 7.25v9.5A2.25 2.25 0 0 0 5.25 19h7.5A2.25 2.25 0 0 0 15 16.75V13.5l5.2 3.2a.75.75 0 0 0 1.15-.64V7.94a.75.75 0 0 0-1.15-.64L15 10.5Z"/></svg>
          </div>
          <div class="heading-copy">
            <div class="heading-eyebrow">
              <span class="live-pulse"></span>
              ارتباط زنده سالن
            </div>
            <h2>دوربین‌های سالن</h2>
            <p>
              <strong>{{ cameras.length }}</strong>
              دوربین فعال
            </p>
          </div>
        </div>

        <div class="camera-actions">
          

          <button
            v-if="cameraOn"
            class="share-toggle"
            :class="{ sharing: sharing }"
            type="button"
            :disabled="cameraLoading"
            :aria-pressed="sharing"
            @click="toggleSharing"
          >
            <span class="action-icon">
              <svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.25"/><circle cx="6" cy="12" r="2.25"/><circle cx="18" cy="19" r="2.25"/><path d="m8 11 7.8-4.7M8 13l7.8 4.7"/></svg>
            </span>
            <span class="action-copy">
              <strong>
                {{ sharing ? 'توقف اشتراک‌گذاری' : 'اشتراک‌گذاری دوربین' }}
              </strong>
              <small>{{ sharing ? 'تصویر برای اعضای سالن قابل مشاهده است' : 'نمایش دوربین برای اعضا' }}</small>
            </span>
          </button>
        </div>
      </header>

      <div v-if="cameras.length" class="camera-grid">
        <article
          v-for="camera in cameras"
          :key="camera.userId"
          class="camera-card"
          :class="{ 'is-local': camera.isLocal, 'is-shared': !camera.isLocal }"
        >
          <div class="video-wrapper">
            <video
              :ref="el => setVideoRef(el, camera.userId)"
              :class="{ 'local-video': camera.isLocal }"
              autoplay
              playsinline
              muted
            ></video>

            <div class="video-topbar">
              <span v-if="camera.isLocal" class="camera-badge local">
                <svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.2"/><path d="M5.5 19.2a6.5 6.5 0 0 1 13 0"/></svg>
                شما
              </span>
              <span v-else class="camera-badge remote">
                <svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 9a4.3 4.3 0 0 0 0 6M15 9a4.3 4.3 0 0 1 0 6M6.2 6.2a8.3 8.3 0 0 0 0 11.6M17.8 6.2a8.3 8.3 0 0 1 0 11.6M12 12v.01"/></svg>
                اشتراکی
              </span>

              <span class="quality-badge">
                <span class="quality-dot"></span>
                LIVE
              </span>
            </div>

            <div class="video-overlay">
              <div class="user-info">
                <span class="status-dot"></span>
                <span class="user-name">
                  {{ camera.isLocal ? (localUsername || 'شما') : (camera.username || 'کاربر') }}
                </span>
              </div>
            </div>
          </div>
        </article>
      </div>

      <div v-else class="empty-cameras">
        <div class="empty-visual" aria-hidden="true">
          <span class="empty-ring ring-one"></span>
          <span class="empty-ring ring-two"></span>
          <span class="empty-icon">
            <svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 10.5V7.25A2.25 2.25 0 0 0 12.75 5h-7.5A2.25 2.25 0 0 0 3 7.25v9.5A2.25 2.25 0 0 0 5.25 19h7.5A2.25 2.25 0 0 0 15 16.75V13.5l5.2 3.2a.75.75 0 0 0 1.15-.64V7.94a.75.75 0 0 0-1.15-.64L15 10.5Z"/><path d="m4 4 16 16"/></svg>
          </span>
        </div>

        <div class="empty-content">
          <span class="empty-label">اتصال دوربین</span>
          <h3>هنوز دوربینی فعال نیست</h3>
          <p>
            دوربین خود را روشن کنید تا تصویر شما در سالن آماده شود.
            برای نمایش تصویر به سایر اعضا، اشتراک‌گذاری را نیز فعال کنید.
          </p>
        </div>

        
      </div>
    </div>
  </section>
</template>

<script setup>

import {
  computed,
  nextTick,
  onMounted,
  onUnmounted,
  ref,
  shallowRef,
  watch,
} from 'vue'

const props = defineProps({
  roomId: {
    type: [String, Number],
    required: true,
  },
})

const emit = defineEmits([
  'camera-stream',
  'camera-state',
  'socket-state',
  'ranking-update',
])

/* --------------------------------------------------------------------------
 * Theme state
 * The component reads the app theme from the document root/body and mirrors
 * it onto the scoped component root so dark mode works reliably with
 * <style scoped>.
 * -------------------------------------------------------------------------- */
const isDarkTheme = ref(false)
let themeObserver = null

function detectDarkTheme() {
  const root = document.documentElement
  const body = document.body

  const rootTheme = root.getAttribute('data-theme')
  const bodyTheme = body?.getAttribute('data-theme')

  if (rootTheme === 'dark' || bodyTheme === 'dark') return true
  if (rootTheme === 'light' || bodyTheme === 'light') return false

  return (
    root.classList.contains('dark') ||
    body?.classList.contains('dark') ||
    root.classList.contains('dark-mode') ||
    body?.classList.contains('dark-mode')
  )
}

function syncTheme() {
  isDarkTheme.value = detectDarkTheme()
}

function startThemeObserver() {
  syncTheme()

  if (typeof MutationObserver === 'undefined') return

  themeObserver = new MutationObserver(syncTheme)
  const options = { attributes: true, attributeFilter: ['class', 'data-theme', 'style'] }
  themeObserver.observe(document.documentElement, options)

  if (document.body) {
    themeObserver.observe(document.body, options)
  }
}

/* --------------------------------------------------------------------------
 * Camera state
 * -------------------------------------------------------------------------- */
const cameraOn = ref(false)
const sharing = ref(false)
const cameraLoading = ref(false)
const localStream = shallowRef(null)
const localUserId = ref(null)
const localUsername = ref('')

/* --------------------------------------------------------------------------
 * Socket state
 * -------------------------------------------------------------------------- */
const socket = ref(null)
const socketConnected = ref(false)
const rankingPeriod = ref('today')
let rankingPingTimer = null
const RANKING_PING_INTERVAL_MS = 2000

/* --------------------------------------------------------------------------
 * DOM / WebRTC storage
 * -------------------------------------------------------------------------- */
const videoElements = new Map()
const peerConnections = new Map()
const peerStates = new Map()
const pendingIceCandidates = new Map()

/* --------------------------------------------------------------------------
 * Remote peers
 *
 * stream/track is intentionally kept after stop-sharing so that starting
 * the same camera again can resume the existing RTP track without creating
 * another PeerConnection.
 * -------------------------------------------------------------------------- */
const remotePeers = shallowRef([])

const RTC_CONFIGURATION = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' },
  ],
}

/* --------------------------------------------------------------------------
 * Cameras computed
 * -------------------------------------------------------------------------- */
const cameras = computed(() => {
  const result = []

  if (cameraOn.value && localStream.value && localUserId.value !== null) {
    result.push({
      userId: localUserId.value,
      username: localUsername.value,
      stream: localStream.value,
      isLocal: true,
    })
  }

  for (const peer of remotePeers.value) {
    if (!peer.sharing || !peer.stream) {
      continue
    }

    result.push({
      userId: peer.userId,
      username: peer.username,
      stream: peer.stream,
      isLocal: false,
    })
  }

  return result
})

/* --------------------------------------------------------------------------
 * Authentication / socket helpers
 * -------------------------------------------------------------------------- */
function getAccessToken() {
  return localStorage.getItem('access_token')
}

function sendSocketMessage(message) {
  const ws = socket.value

  if (!ws || ws.readyState !== WebSocket.OPEN) {
    console.warn('ROOM CAMERAS SOCKET NOT READY:', message)
    return false
  }

  ws.send(JSON.stringify(message))
  return true
}

function startRankingPing() {
  stopRankingPing()

  rankingPingTimer = window.setInterval(() => {
    if (
      socket.value &&
      socket.value.readyState === WebSocket.OPEN
    ) {
      sendSocketMessage({ type: 'ping' })
    }
  }, RANKING_PING_INTERVAL_MS)
}

function stopRankingPing() {
  if (rankingPingTimer !== null) {
    window.clearInterval(rankingPingTimer)
    rankingPingTimer = null
  }
}

function emitSocketState(value) {
  socketConnected.value = value
  emit('socket-state', value)
}

function applyRanking(data) {
  emit('ranking-update', {
    ranking: data.ranking || [],
    period: data.period || rankingPeriod.value,
  })
}

function changeRankingPeriod(period) {
  const validPeriods = [
    'today',
    'yesterday',
    'week',
    'all',
  ]

  if (!validPeriods.includes(period)) {
    return
  }

  rankingPeriod.value = period

  sendSocketMessage({
    type: 'ranking_period',
    period,
  })
}

/* --------------------------------------------------------------------------
 * Video helpers
 * -------------------------------------------------------------------------- */
function setVideoRef(element, userId) {
  if (userId === null || userId === undefined) {
    return
  }

  const id = String(userId)

  if (!element) {
    videoElements.delete(id)
    return
  }

  videoElements.set(id, element)

  const camera = cameras.value.find(
    item => String(item.userId) === id
  )

  if (camera?.stream) {
    attachVideoStream(userId, camera.stream)
  }
}

async function attachVideoStream(userId, stream) {
  await nextTick()

  const video = videoElements.get(String(userId))

  if (!video || !stream) {
    return
  }

  /*
   * Audio فعلاً نداریم؛ mute بودن ویدئو اجازه autoplay بی‌دردسر می‌دهد.
   */
  video.autoplay = true
  video.playsInline = true
  video.muted = true

  if (video.srcObject !== stream) {
    video.srcObject = stream
  }

  try {
    await video.play()
  } catch (error) {
    if (error?.name !== 'AbortError') {
      console.warn('VIDEO PLAY WAITING:', {
        userId,
        error,
      })
    }
  }
}

function upsertRemotePeer(
  userId,
  username = '',
  stream = null,
  sharingState = null,
) {
  const id = String(userId)

  const current = remotePeers.value.find(
    peer => String(peer.userId) === id
  )

  if (current) {
    remotePeers.value = remotePeers.value.map(peer => {
      if (String(peer.userId) !== id) {
        return peer
      }

      return {
        ...peer,
        username: username || peer.username,
        stream: stream || peer.stream,
        sharing:
          sharingState === null
            ? peer.sharing
            : sharingState,
      }
    })
  } else {
    remotePeers.value = [
      ...remotePeers.value,
      {
        userId,
        username: username || 'کاربر',
        stream,
        sharing: sharingState === true,
      },
    ]
  }

  if (stream) {
    attachVideoStream(userId, stream)
  }
}

function setRemoteSharingState(userId, sharingState) {
  const id = String(userId)

  const current = remotePeers.value.find(
    peer => String(peer.userId) === id
  )

  if (!current) {
    remotePeers.value = [
      ...remotePeers.value,
      {
        userId,
        username: 'کاربر',
        stream: null,
        sharing: sharingState,
      },
    ]
    return
  }

  remotePeers.value = remotePeers.value.map(peer =>
    String(peer.userId) === id
      ? { ...peer, sharing: sharingState }
      : peer
  )

  if (sharingState && current.stream) {
    attachVideoStream(userId, current.stream)
  }
}

function removeRemotePeer(userId) {
  const id = String(userId)
  const video = videoElements.get(id)

  if (video) {
    try {
      video.pause()
    } catch {
      // ignore
    }
    video.srcObject = null
  }

  videoElements.delete(id)

  remotePeers.value = remotePeers.value.filter(
    peer => String(peer.userId) !== id
  )
}

/* --------------------------------------------------------------------------
 * Perfect Negotiation helpers
 * -------------------------------------------------------------------------- */
function isPolite(remoteUserId) {
  if (localUserId.value === null) {
    return true
  }

  const localId = Number(localUserId.value)
  const remoteId = Number(remoteUserId)

  if (Number.isNaN(localId) || Number.isNaN(remoteId)) {
    return true
  }

  /* شناسه بزرگ‌تر = polite */
  return localId > remoteId
}

function getPeerState(remoteUserId) {
  const id = String(remoteUserId)
  let state = peerStates.get(id)

  if (!state) {
    state = {
      makingOffer: false,
      ignoreOffer: false,
      username: '',
    }

    peerStates.set(id, state)
  }

  return state
}

function getPeerConnection(remoteUserId) {
  return peerConnections.get(String(remoteUserId)) || null
}

async function replaceLocalTrack(remoteUserId) {
  const pc = getPeerConnection(remoteUserId)

  if (!pc) {
    return
  }

  const transceiver = pc.getTransceivers().find(
    item => item.sender && item.receiver?.track?.kind === 'video'
  )

  if (!transceiver) {
    return
  }

  const track = sharing.value
    ? localStream.value
        ?.getVideoTracks()
        ?.find(item => item.readyState === 'live') || null
    : null

  try {
    await transceiver.sender.replaceTrack(track)

    if (track && localStream.value) {
      try {
        transceiver.sender.setStreams(localStream.value)
      } catch {
        // browser may not support setStreams fully
      }
    }

    transceiver.direction = 'sendrecv'

    console.log('WEBRTC LOCAL TRACK SYNC:', {
      remoteUserId,
      sharing: sharing.value,
      hasTrack: !!track,
      trackId: track?.id || null,
      direction: transceiver.direction,
      currentDirection: transceiver.currentDirection,
    })
  } catch (error) {
    console.error('WEBRTC LOCAL TRACK SYNC ERROR:', {
      remoteUserId,
      error,
    })
  }
}

function ensurePeerConnection(remoteUserId, username = '') {
  const id = String(remoteUserId)

  if (localUserId.value !== null && id === String(localUserId.value)) {
    return null
  }

  let pc = peerConnections.get(id)
  const peerState = getPeerState(id)

  if (username) {
    peerState.username = username
  }

  if (pc) {
    return pc
  }

  console.log('WEBRTC CREATE PEER:', {
    remoteUserId,
    username,
    polite: isPolite(remoteUserId),
  })

  pc = new RTCPeerConnection(RTC_CONFIGURATION)
  peerConnections.set(id, pc)
  pendingIceCandidates.set(id, [])
  peerState.username = username || 'کاربر'

  /*
   * این transceiver یک‌بار ساخته می‌شود و همیشه sendrecv باقی می‌ماند.
   * روشن/خاموش شدن دوربین فقط replaceTrack است و مذاکره جدید لازم ندارد.
   */
  const transceiver = pc.addTransceiver('video', {
    direction: 'sendrecv',
  })

  if (sharing.value && localStream.value) {
    const track = localStream.value
      .getVideoTracks()
      .find(item => item.readyState === 'live')

    if (track) {
      transceiver.sender
        .replaceTrack(track)
        .then(() => {
          try {
            transceiver.sender.setStreams(localStream.value)
          } catch {
            // ignore
          }
        })
        .catch(error => {
          console.error('WEBRTC INITIAL TRACK ERROR:', {
            remoteUserId,
            error,
          })
        })
    }
  }

  pc.onicecandidate = event => {
    if (!event.candidate) {
      return
    }

    sendSocketMessage({
      type: 'webrtc_ice_candidate',
      target_user_id: Number(remoteUserId),
      candidate: event.candidate,
    })
  }

  pc.ontrack = event => {
    console.log('WEBRTC REMOTE TRACK:', {
      remoteUserId,
      username: peerState.username,
      trackId: event.track?.id,
      kind: event.track?.kind,
      streams: event.streams,
    })

    let stream = event.streams?.[0]

    if (!stream) {
      const existing = remotePeers.value.find(
        peer => String(peer.userId) === id
      )

      stream = existing?.stream || new MediaStream()

      if (
        event.track &&
        !stream.getTracks().some(
          track => track.id === event.track.id
        )
      ) {
        stream.addTrack(event.track)
      }
    }

    upsertRemotePeer(
      remoteUserId,
      peerState.username,
      stream,
      null,
    )

    event.track.onunmute = () => {
      console.log('WEBRTC REMOTE TRACK UNMUTED:', remoteUserId)

      upsertRemotePeer(
        remoteUserId,
        peerState.username,
        stream,
        null,
      )
    }

    event.track.onmute = () => {
      console.log('WEBRTC REMOTE TRACK MUTED:', remoteUserId)
    }

    event.track.onended = () => {
      console.log('WEBRTC REMOTE TRACK ENDED:', remoteUserId)
    }
  }

  pc.onnegotiationneeded = async () => {
    const state = getPeerState(remoteUserId)

    if (state.makingOffer) {
      return
    }

    if (pc.signalingState !== 'stable') {
      return
    }

    try {
      state.makingOffer = true

      console.log('WEBRTC NEGOTIATION START:', {
        remoteUserId,
      })

      await pc.setLocalDescription()

      console.log('WEBRTC OFFER SEND:', {
        remoteUserId,
        type: pc.localDescription?.type,
      })

      sendSocketMessage({
        type: 'webrtc_offer',
        target_user_id: Number(remoteUserId),
        offer: pc.localDescription,
      })
    } catch (error) {
      console.error('WEBRTC NEGOTIATION ERROR:', {
        remoteUserId,
        error,
      })
    } finally {
      state.makingOffer = false
    }
  }

  pc.onconnectionstatechange = () => {
    console.log('WEBRTC CONNECTION STATE:', {
      remoteUserId,
      state: pc.connectionState,
    })

    if (
      pc.connectionState === 'failed' ||
      pc.connectionState === 'closed'
    ) {
      closePeerConnection(remoteUserId)
    }
  }

  pc.oniceconnectionstatechange = () => {
    console.log('WEBRTC ICE STATE:', {
      remoteUserId,
      state: pc.iceConnectionState,
    })

    if (pc.iceConnectionState === 'failed') {
      console.warn('WEBRTC ICE FAILED:', remoteUserId)
    }
  }

  return pc
}

function closePeerConnection(remoteUserId) {
  const id = String(remoteUserId)
  const pc = peerConnections.get(id)

  if (pc) {
    try {
      pc.close()
    } catch {
      // ignore
    }
  }

  peerConnections.delete(id)
  peerStates.delete(id)
  pendingIceCandidates.delete(id)
  removeRemotePeer(remoteUserId)
}

function closeAllPeerConnections() {
  const ids = [...peerConnections.keys()]

  for (const id of ids) {
    closePeerConnection(id)
  }

  peerConnections.clear()
  peerStates.clear()
  pendingIceCandidates.clear()
  remotePeers.value = []
}

async function flushPendingIceCandidates(remoteUserId) {
  const id = String(remoteUserId)
  const pc = peerConnections.get(id)

  if (!pc || !pc.remoteDescription) {
    return
  }

  const queue = pendingIceCandidates.get(id) || []
  pendingIceCandidates.set(id, [])

  for (const candidate of queue) {
    try {
      await pc.addIceCandidate(new RTCIceCandidate(candidate))
      console.log('WEBRTC QUEUED ICE ADDED:', remoteUserId)
    } catch (error) {
      console.error('WEBRTC QUEUED ICE ERROR:', {
        remoteUserId,
        error,
      })
    }
  }
}

/* --------------------------------------------------------------------------
 * WebRTC message handlers
 * -------------------------------------------------------------------------- */
async function handleOffer(data) {
  const remoteUserId = data.sender_id

  if (remoteUserId === null || remoteUserId === undefined) {
    return
  }

  const pc = ensurePeerConnection(
    remoteUserId,
    data.sender_username,
  )

  if (!pc) {
    return
  }

  const state = getPeerState(remoteUserId)
  const polite = isPolite(remoteUserId)

  const offerCollision =
    state.makingOffer ||
    pc.signalingState !== 'stable'

  state.ignoreOffer = !polite && offerCollision

  if (state.ignoreOffer) {
    console.warn('WEBRTC OFFER IGNORED:', {
      remoteUserId,
      signalingState: pc.signalingState,
      polite,
    })
    return
  }

  try {
    if (offerCollision && polite) {
      await pc.setLocalDescription({ type: 'rollback' })
    }

    await pc.setRemoteDescription(
      new RTCSessionDescription(data.offer)
    )

    console.log('WEBRTC REMOTE OFFER SET:', {
      remoteUserId,
      signalingState: pc.signalingState,
    })

    await flushPendingIceCandidates(remoteUserId)

    await replaceLocalTrack(remoteUserId)

    await pc.setLocalDescription()

    console.log('WEBRTC ANSWER SEND:', {
      remoteUserId,
      type: pc.localDescription?.type,
    })

    sendSocketMessage({
      type: 'webrtc_answer',
      target_user_id: Number(remoteUserId),
      answer: pc.localDescription,
    })
  } catch (error) {
    console.error('WEBRTC HANDLE OFFER ERROR:', {
      remoteUserId,
      error,
    })
  }
}

async function handleAnswer(data) {
  const remoteUserId = data.sender_id
  const pc = getPeerConnection(remoteUserId)

  if (!pc) {
    console.warn('WEBRTC ANSWER PEER NOT FOUND:', remoteUserId)
    return
  }

  try {
    await pc.setRemoteDescription(
      new RTCSessionDescription(data.answer)
    )

    console.log('WEBRTC ANSWER REMOTE DESCRIPTION SET:', {
      remoteUserId,
      signalingState: pc.signalingState,
    })

    await flushPendingIceCandidates(remoteUserId)
  } catch (error) {
    console.error('WEBRTC HANDLE ANSWER ERROR:', {
      remoteUserId,
      error,
    })
  }
}

async function handleIceCandidate(data) {
  const remoteUserId = data.sender_id

  if (remoteUserId === null || remoteUserId === undefined) {
    return
  }

  const id = String(remoteUserId)
  const pc = ensurePeerConnection(remoteUserId)

  if (!pc) {
    return
  }

  if (!pc.remoteDescription) {
    const queue = pendingIceCandidates.get(id) || []
    queue.push(data.candidate)
    pendingIceCandidates.set(id, queue)
    return
  }

  try {
    await pc.addIceCandidate(
      new RTCIceCandidate(data.candidate)
    )
  } catch (error) {
    const state = getPeerState(remoteUserId)

    if (!state.ignoreOffer) {
      console.error('WEBRTC ICE ERROR:', {
        remoteUserId,
        error,
      })
    }
  }
}

/* --------------------------------------------------------------------------
 * Room events
 * -------------------------------------------------------------------------- */
function handleMemberJoined(data) {
  const remoteUserId = data.user_id

  if (
    remoteUserId === null ||
    remoteUserId === undefined ||
    String(remoteUserId) === String(localUserId.value)
  ) {
    return
  }

  ensurePeerConnection(remoteUserId, data.username)
}

function handleMemberLeft(data) {
  if (data.user_id === null || data.user_id === undefined) {
    return
  }

  closePeerConnection(data.user_id)
}

function handleRemoteCameraStarted(data) {
  const remoteUserId = data.user_id

  if (
    remoteUserId === null ||
    remoteUserId === undefined ||
    String(remoteUserId) === String(localUserId.value)
  ) {
    return
  }

  ensurePeerConnection(remoteUserId, data.username)

  setRemoteSharingState(remoteUserId, true)
}

function handleRemoteCameraStopped(data) {
  const remoteUserId = data.user_id

  if (remoteUserId === null || remoteUserId === undefined) {
    return
  }

  setRemoteSharingState(remoteUserId, false)
}

function handleCameraStateRequest(data) {
  const requesterId = data.requester_id

  if (
    requesterId === null ||
    requesterId === undefined ||
    String(requesterId) === String(localUserId.value)
  ) {
    return
  }

  if (!sharing.value || !localStream.value) {
    return
  }

  sendSocketMessage({
    type: 'camera_state_response',
    target_user_id: Number(requesterId),
  })
}

function handleCameraStateResponse(data) {
  const remoteUserId = data.user_id

  if (
    remoteUserId === null ||
    remoteUserId === undefined ||
    String(remoteUserId) === String(localUserId.value)
  ) {
    return
  }

  ensurePeerConnection(remoteUserId, data.username)
  setRemoteSharingState(remoteUserId, true)
}

/* --------------------------------------------------------------------------
 * Socket router / connection
 * -------------------------------------------------------------------------- */
function handleSocketMessage(data) {
  switch (data.type) {
    case 'connection':
      localUserId.value = data.user_id
      localUsername.value = data.username || ''
      rankingPeriod.value = data.period || 'today'

      console.log('ROOM CAMERA CONNECTION:', {
        userId: localUserId.value,
        username: localUsername.value,
      })

      applyRanking(data)

      sendSocketMessage({
        type: 'camera_state_request',
      })
      break

    case 'ranking_update':
      if (data.period) {
        rankingPeriod.value = data.period
      }
      applyRanking(data)
      break

    case 'room_member_joined':
      handleMemberJoined(data)
      break

    case 'room_member_left':
      handleMemberLeft(data)
      break

    case 'camera_share_started':
      handleRemoteCameraStarted(data)
      break

    case 'camera_share_stopped':
      handleRemoteCameraStopped(data)
      break

    case 'camera_state_request':
      handleCameraStateRequest(data)
      break

    case 'camera_state_response':
      handleCameraStateResponse(data)
      break

    case 'webrtc_offer':
      handleOffer(data)
      break

    case 'webrtc_answer':
      handleAnswer(data)
      break

    case 'webrtc_ice_candidate':
      handleIceCandidate(data)
      break

    default:
      break
  }
}

function connectSocket() {
  const token = getAccessToken()

  if (!token) {
    console.error('Access token not found.')
    return
  }

  disconnectSocket()
  closeAllPeerConnections()

  const isProduction = window.location.hostname === 'dopamine-st2u.onrender.com'

  const wsProtocol = window.location.protocol === 'https:'
    ? 'wss:'
    : 'ws:'

  const wsHost = isProduction
    ? 'dopamine-backend-3vbz.onrender.com'
    : '127.0.0.1:8000'

  const wsUrl =
    `${wsProtocol}//${wsHost}/ws/rooms/${props.roomId}/` +
    `?token=${encodeURIComponent(token)}`

  console.log('ROOM CAMERAS SOCKET CONNECTING:', wsUrl)

  const ws = new WebSocket(wsUrl)

  socket.value = ws

  ws.onopen = () => {
    emitSocketState(true)

    console.log(
      'ROOM CAMERAS SOCKET CONNECTED:',
      props.roomId
    )

    startRankingPing()
  }

  ws.onmessage = event => {
    try {
      const data = JSON.parse(event.data)

      console.log(
        'ROOM CAMERAS SOCKET MESSAGE:',
        data
      )

      handleSocketMessage(data)
    } catch (error) {
      console.error(
        'WebSocket message error:',
        error
      )
    }
  }

  ws.onerror = error => {
    console.error(
      'WebSocket error:',
      error
    )
  }

  ws.onclose = event => {
    console.log(
      'ROOM CAMERAS SOCKET CLOSED:',
      event
    )

    emitSocketState(false)

    stopRankingPing()

    closeAllPeerConnections()
  }
}

function disconnectSocket() {
  stopRankingPing()

  if (!socket.value) {
    emitSocketState(false)
    return
  }

  try {
    socket.value.close()
  } catch {
    // ignore
  }

  socket.value = null
  emitSocketState(false)
}

/* --------------------------------------------------------------------------
 * One and only one physical MediaStream
 * -------------------------------------------------------------------------- */
async function startCamera() {
  if (cameraOn.value) {
    return localStream.value
  }

  if (
    !navigator.mediaDevices ||
    !navigator.mediaDevices.getUserMedia
  ) {
    console.error('Camera API is not available.')
    return null
  }

  cameraLoading.value = true

  try {
    console.log('LOCAL CAMERA STARTING...')

    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: 'user',
      },
      audio: false,
    })

    localStream.value = stream
    cameraOn.value = true
    sharing.value = false

    emit('camera-stream', stream)
    emit('camera-state', true)

    await nextTick()

    if (localUserId.value !== null) {
      await attachVideoStream(localUserId.value, stream)
    }

    /*
     * دوربین فقط روشن شده؛ هنوز اشتراک‌گذاری شروع نشده است.
     */

    console.log('LOCAL CAMERA STARTED SUCCESSFULLY')
    return stream
  } catch (error) {
    console.error('Camera start error:', error)

    localStream.value = null
    cameraOn.value = false
    sharing.value = false
    emit('camera-stream', null)
    emit('camera-state', false)
    return null
  } finally {
    cameraLoading.value = false
  }
}

async function startSharing() {
  if (!cameraOn.value || !localStream.value || sharing.value) {
    return
  }

  sharing.value = true

  sendSocketMessage({
    type: 'camera_share_started',
  })

  const ids = [...peerConnections.keys()]

  for (const userId of ids) {
    await replaceLocalTrack(userId)
  }

  console.log('LOCAL CAMERA SHARING STARTED')
}

async function stopSharing() {
  if (!sharing.value) {
    return
  }

  sharing.value = false

  sendSocketMessage({
    type: 'camera_share_stopped',
  })

  const ids = [...peerConnections.keys()]

  for (const userId of ids) {
    await replaceLocalTrack(userId)
  }

  console.log('LOCAL CAMERA SHARING STOPPED')
}

async function stopCamera() {
  if (!cameraOn.value && !localStream.value) {
    return
  }

  console.log('LOCAL CAMERA STOPPING...')

  if (sharing.value) {
    await stopSharing()
  }

  if (localStream.value) {
    for (const track of localStream.value.getTracks()) {
      track.stop()
    }
  }

  localStream.value = null
  cameraOn.value = false
  sharing.value = false

  if (localUserId.value !== null) {
    const localVideo = videoElements.get(String(localUserId.value))

    if (localVideo) {
      try {
        localVideo.pause()
      } catch {
        // ignore
      }
      localVideo.srcObject = null
    }
  }

  emit('camera-stream', null)
  emit('camera-state', false)

  console.log('LOCAL CAMERA STOPPED')
}

async function toggleSharing() {
  if (!cameraOn.value) {
    return
  }

  if (sharing.value) {
    await stopSharing()
  } else {
    await startSharing()
  }
}

async function toggleCamera() {
  if (cameraOn.value) {
    await stopCamera()

  } else {
    await startCamera()
  }
}

/* --------------------------------------------------------------------------
 * Watch room
 * -------------------------------------------------------------------------- */
watch(
  () => props.roomId,
  async newRoomId => {
    if (!newRoomId) {
      return
    }

    await stopCamera()
    closeAllPeerConnections()
    localUserId.value = null
    localUsername.value = ''
    remotePeers.value = []
    connectSocket()
  }
)

/* --------------------------------------------------------------------------
 * Lifecycle
 * -------------------------------------------------------------------------- */
onMounted(() => {
  startThemeObserver()
  connectSocket()
})

onUnmounted(async () => {
  themeObserver?.disconnect()
  themeObserver = null
  await stopCamera()
  closeAllPeerConnections()
  disconnectSocket()
})

defineExpose({
  startCamera,
  stopCamera,
  startSharing,
  stopSharing,
  changeRankingPeriod,
})
</script>
<style scoped>
.room-cameras {
  --camera-primary: var(--primary, #6366f1);
  --camera-primary-rgb: var(--primary-rgb, 99, 102, 241);

  --camera-bg: #f6f8fc;
  --camera-surface: rgba(255, 255, 255, 0.88);
  --camera-surface-solid: #ffffff;
  --camera-border: rgba(15, 23, 42, 0.08);
  --camera-border-strong: rgba(15, 23, 42, 0.13);
  --camera-text: #101827;
  --camera-text-soft: #5f6b7d;
  --camera-muted: #8a94a6;
  --camera-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
  --camera-video: #0b1020;
  --camera-success: #17b978;
  --camera-danger: #ef5b67;

  width: 100%;
  margin-bottom: 24px;
}

.camera-shell {
  position: relative;
  overflow: hidden;
  padding: 22px;
  border: 1px solid var(--camera-border);
  border-radius: 26px;
  background:
    radial-gradient(circle at 100% 0, rgba(var(--camera-primary-rgb), 0.08), transparent 28%),
    radial-gradient(circle at 0 100%, rgba(var(--camera-primary-rgb), 0.05), transparent 30%),
    var(--camera-surface);
  box-shadow: var(--camera-shadow);
  backdrop-filter: blur(18px);
}

.camera-shell::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.48),
      transparent 34%,
      transparent 70%,
      rgba(var(--camera-primary-rgb), 0.04)
    );
}

.cameras-header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 22px;
  margin-bottom: 20px;
}

.camera-heading {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.heading-icon {
  display: grid;
  place-items: center;
  width: 52px;
  height: 52px;
  flex: 0 0 52px;
  border: 1px solid rgba(var(--camera-primary-rgb), 0.15);
  border-radius: 16px;
  color: var(--camera-primary);
  background: linear-gradient(
    145deg,
    rgba(var(--camera-primary-rgb), 0.16),
    rgba(var(--camera-primary-rgb), 0.06)
  );
  box-shadow: 0 10px 28px rgba(var(--camera-primary-rgb), 0.12);
  font-size: 20px;
}

.heading-copy {
  min-width: 0;
}

.heading-eyebrow {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 4px;
  color: var(--camera-primary);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.03em;
}

.live-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--camera-success);
  box-shadow: 0 0 0 4px rgba(23, 185, 120, 0.1);
  animation: cameraPulse 1.8s ease-in-out infinite;
}

.cameras-header h2 {
  margin: 0;
  color: var(--camera-text);
  font-size: 21px;
  font-weight: 850;
  letter-spacing: -0.02em;
}

.cameras-header p {
  margin: 4px 0 0;
  color: var(--camera-muted);
  font-size: 12px;
}

.cameras-header p strong {
  color: var(--camera-text-soft);
  font-weight: 800;
}

.camera-actions {
  display: flex;
  align-items: stretch;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

.camera-toggle,
.share-toggle,
.empty-camera-button {
  border: 1px solid transparent;
  border-radius: 15px;
  font-family: inherit;
  cursor: pointer;
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    background 0.22s ease,
    border-color 0.22s ease,
    opacity 0.22s ease;
}

.camera-toggle,
.share-toggle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 52px;
  padding: 10px 14px;
  text-align: right;
}

.camera-toggle {
  color: var(--camera-text);
  border-color: var(--camera-border);
  background: var(--camera-surface-solid);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.camera-toggle:hover:not(:disabled),
.share-toggle:hover:not(:disabled),
.empty-camera-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.camera-toggle.active {
  border-color: rgba(239, 91, 103, 0.18);
  color: #d94855;
  background: linear-gradient(145deg, rgba(239, 91, 103, 0.1), rgba(255, 255, 255, 0.95));
  box-shadow: 0 10px 26px rgba(239, 91, 103, 0.08);
}

.share-toggle {
  color: var(--camera-primary);
  border-color: rgba(var(--camera-primary-rgb), 0.13);
  background: rgba(var(--camera-primary-rgb), 0.07);
  box-shadow: 0 8px 24px rgba(var(--camera-primary-rgb), 0.06);
}

.share-toggle.sharing {
  color: #0b8b5e;
  border-color: rgba(23, 185, 120, 0.18);
  background: rgba(23, 185, 120, 0.08);
  box-shadow: 0 10px 26px rgba(23, 185, 120, 0.08);
}

.action-icon {
  display: grid;
  place-items: center;
  width: 33px;
  height: 33px;
  flex: 0 0 33px;
  border-radius: 10px;
  background: rgba(148, 163, 184, 0.1);
  font-size: 14px;
}

.camera-toggle.active .action-icon {
  background: rgba(239, 91, 103, 0.11);
}

.share-toggle .action-icon {
  background: rgba(var(--camera-primary-rgb), 0.11);
}

.share-toggle.sharing .action-icon {
  background: rgba(23, 185, 120, 0.1);
}

.action-copy {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.action-copy strong {
  font-size: 12px;
  font-weight: 800;
  line-height: 1.35;
}

.action-copy small {
  color: var(--camera-muted);
  font-size: 10px;
  font-weight: 500;
  line-height: 1.3;
}

.camera-toggle.active .action-copy small {
  color: rgba(217, 72, 85, 0.7);
}

.share-toggle.sharing .action-copy small {
  color: rgba(11, 139, 94, 0.72);
}

.button-spinner {
  width: 14px;
  height: 14px;
  flex: 0 0 14px;
  border: 2px solid currentColor;
  border-left-color: transparent;
  border-radius: 50%;
  animation: cameraSpin 0.75s linear infinite;
}

.camera-toggle:disabled,
.share-toggle:disabled,
.empty-camera-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
  transform: none !important;
}

.camera-grid {
  position: relative;
  z-index: 1;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}

.camera-card {
  min-width: 0;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  background: var(--camera-video);
  box-shadow:
    0 16px 40px rgba(2, 6, 23, 0.18),
    0 0 0 1px rgba(2, 6, 23, 0.04);
  transition:
    transform 0.24s ease,
    box-shadow 0.24s ease,
    border-color 0.24s ease;
}

.camera-card:hover {
  transform: translateY(-3px);
  border-color: rgba(var(--camera-primary-rgb), 0.22);
  box-shadow:
    0 20px 50px rgba(2, 6, 23, 0.24),
    0 0 0 1px rgba(var(--camera-primary-rgb), 0.07);
}

.video-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  isolation: isolate;
  background:
    radial-gradient(circle at center, rgba(var(--camera-primary-rgb), 0.08), transparent 44%),
    var(--camera-video);
}

.video-wrapper::after {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(
    180deg,
    rgba(2, 6, 23, 0.22),
    transparent 26%,
    transparent 68%,
    rgba(2, 6, 23, 0.62)
  );
}

.video-wrapper video {
  position: relative;
  z-index: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  background: var(--camera-video);
}

.local-video {
  transform: scaleX(-1);
}

.video-topbar {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.camera-badge,
.quality-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 28px;
  padding: 5px 9px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9px;
  color: #fff;
  background: rgba(2, 6, 23, 0.46);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.14);
  backdrop-filter: blur(10px);
  font-size: 10px;
  font-weight: 800;
}

.camera-badge.local i {
  color: #93c5fd;
}

.camera-badge.remote i {
  color: #86efac;
}

.quality-badge {
  padding-inline: 8px;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(23, 185, 120, 0.2);
}

.quality-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #67e8a4;
  box-shadow: 0 0 0 3px rgba(103, 232, 164, 0.12);
}

.video-overlay {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 2;
  padding: 34px 14px 13px;
  pointer-events: none;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  color: #fff;
  font-size: 13px;
  font-weight: 800;
}

.user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-dot {
  width: 8px;
  height: 8px;
  flex: 0 0 8px;
  border-radius: 50%;
  background: #4fd276;
  box-shadow:
    0 0 0 3px rgba(79, 210, 118, 0.18),
    0 0 12px rgba(79, 210, 118, 0.42);
  animation: cameraPulse 1.8s ease-in-out infinite;
}

.empty-cameras {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  padding: 36px 22px;
  overflow: hidden;
  border: 1px dashed var(--camera-border-strong);
  border-radius: 22px;
  background:
    radial-gradient(circle at 50% 0, rgba(var(--camera-primary-rgb), 0.08), transparent 42%),
    var(--camera-surface-solid);
  text-align: center;
}

.empty-cameras::before,
.empty-cameras::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(1px);
}

.empty-cameras::before {
  width: 220px;
  height: 220px;
  top: -130px;
  right: -90px;
  border: 1px solid rgba(var(--camera-primary-rgb), 0.08);
}

.empty-cameras::after {
  width: 170px;
  height: 170px;
  bottom: -110px;
  left: -70px;
  border: 1px solid rgba(var(--camera-primary-rgb), 0.06);
}

.empty-visual {
  position: relative;
  display: grid;
  place-items: center;
  width: 96px;
  height: 96px;
  margin-bottom: 18px;
}

.empty-icon {
  position: relative;
  z-index: 2;
  display: grid;
  place-items: center;
  width: 64px;
  height: 64px;
  border: 1px solid rgba(var(--camera-primary-rgb), 0.16);
  border-radius: 20px;
  color: var(--camera-primary);
  background: linear-gradient(
    145deg,
    rgba(var(--camera-primary-rgb), 0.16),
    rgba(var(--camera-primary-rgb), 0.05)
  );
  box-shadow:
    0 16px 36px rgba(var(--camera-primary-rgb), 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.55);
  font-size: 23px;
}

.empty-ring {
  position: absolute;
  border: 1px solid rgba(var(--camera-primary-rgb), 0.12);
  border-radius: 50%;
  animation: cameraFloat 3.2s ease-in-out infinite;
}

.ring-one {
  width: 82px;
  height: 82px;
}

.ring-two {
  width: 96px;
  height: 96px;
  opacity: 0.7;
  animation-delay: -1.2s;
}

.empty-content {
  position: relative;
  z-index: 1;
}

.empty-label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 24px;
  padding: 4px 9px;
  margin-bottom: 9px;
  border: 1px solid rgba(var(--camera-primary-rgb), 0.11);
  border-radius: 999px;
  color: var(--camera-primary);
  background: rgba(var(--camera-primary-rgb), 0.06);
  font-size: 10px;
  font-weight: 850;
}

.empty-cameras h3 {
  margin: 0 0 8px;
  color: var(--camera-text);
  font-size: 18px;
  font-weight: 850;
  letter-spacing: -0.02em;
}

.empty-cameras p {
  max-width: 500px;
  margin: 0 0 20px;
  color: var(--camera-text-soft);
  font-size: 12px;
  line-height: 2;
}

.empty-camera-button {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-height: 46px;
  padding: 10px 18px;
  color: #fff;
  background: linear-gradient(
    135deg,
    var(--camera-primary),
    color-mix(in srgb, var(--camera-primary) 76%, #000)
  );
  box-shadow:
    0 12px 28px rgba(var(--camera-primary-rgb), 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
  font-size: 12px;
  font-weight: 800;
}

.empty-camera-button:hover:not(:disabled) {
  box-shadow:
    0 16px 34px rgba(var(--camera-primary-rgb), 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

:global(html.dark) .room-cameras,
:global(body.dark) .room-cameras,
:global(html.dark-mode) .room-cameras,
:global(body.dark-mode) .room-cameras,
:global(html[data-theme='dark']) .room-cameras,
:global(body[data-theme='dark']) .room-cameras {
  --camera-bg: #080c16;
  --camera-surface: rgba(15, 23, 42, 0.82);
  --camera-surface-solid: #101827;
  --camera-border: rgba(148, 163, 184, 0.14);
  --camera-border-strong: rgba(148, 163, 184, 0.2);
  --camera-text: #f8fafc;
  --camera-text-soft: #b3bfd1;
  --camera-muted: #7d899d;
  --camera-shadow: 0 20px 55px rgba(0, 0, 0, 0.28);
}

:global(html.dark) .camera-shell,
:global(body.dark) .camera-shell,
:global(html.dark-mode) .camera-shell,
:global(body.dark-mode) .camera-shell,
:global(html[data-theme='dark']) .camera-shell,
:global(body[data-theme='dark']) .camera-shell {
  background:
    radial-gradient(circle at 100% 0, rgba(var(--camera-primary-rgb), 0.12), transparent 28%),
    radial-gradient(circle at 0 100%, rgba(var(--camera-primary-rgb), 0.06), transparent 30%),
    var(--camera-surface);
}

:global(html.dark) .camera-toggle,
:global(body.dark) .camera-toggle,
:global(html.dark-mode) .camera-toggle,
:global(body.dark-mode) .camera-toggle,
:global(html[data-theme='dark']) .camera-toggle,
:global(body[data-theme='dark']) .camera-toggle {
  background: #141d2c;
}

:global(html.dark) .camera-toggle.active,
:global(body.dark) .camera-toggle.active,
:global(html.dark-mode) .camera-toggle.active,
:global(body.dark-mode) .camera-toggle.active,
:global(html[data-theme='dark']) .camera-toggle.active,
:global(body[data-theme='dark']) .camera-toggle.active {
  background: rgba(239, 91, 103, 0.1);
}

:global(html.dark) .empty-cameras,
:global(body.dark) .empty-cameras,
:global(html.dark-mode) .empty-cameras,
:global(body.dark-mode) .empty-cameras,
:global(html[data-theme='dark']) .empty-cameras,
:global(body[data-theme='dark']) .empty-cameras {
  background:
    radial-gradient(circle at 50% 0, rgba(var(--camera-primary-rgb), 0.12), transparent 42%),
    var(--camera-surface-solid);
}

:global(html.dark) .empty-icon,
:global(body.dark) .empty-icon,
:global(html.dark-mode) .empty-icon,
:global(body.dark-mode) .empty-icon,
:global(html[data-theme='dark']) .empty-icon,
:global(body[data-theme='dark']) .empty-icon {
  box-shadow:
    0 16px 36px rgba(var(--camera-primary-rgb), 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

@keyframes cameraPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.55;
    transform: scale(0.82);
  }
}

@keyframes cameraSpin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes cameraFloat {
  0%, 100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.06);
    opacity: 1;
  }
}

@media (max-width: 900px) {
  .cameras-header {
    align-items: stretch;
    flex-direction: column;
  }

  .camera-actions {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .camera-toggle,
  .share-toggle {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .camera-shell {
    padding: 16px;
    border-radius: 22px;
  }

  .camera-grid {
    grid-template-columns: 1fr;
  }

  .camera-actions {
    grid-template-columns: 1fr;
  }

  .heading-icon {
    width: 46px;
    height: 46px;
    flex-basis: 46px;
  }

  .cameras-header h2 {
    font-size: 19px;
  }
}

@media (max-width: 420px) {
  .camera-heading {
    align-items: flex-start;
  }

  .heading-eyebrow {
    font-size: 10px;
  }

  .camera-shell {
    padding: 13px;
  }

  .video-wrapper {
    aspect-ratio: 16 / 11;
  }

  .action-copy small {
    display: none;
  }

  .camera-toggle,
  .share-toggle {
    min-height: 48px;
  }
}


/* --------------------------------------------------------------------------
 * Reliable theme bridge + dependency-free icons
 * -------------------------------------------------------------------------- */
.ui-icon {
  width: 1.15em;
  height: 1.15em;
  display: block;
  flex: 0 0 auto;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.ui-icon.spinning {
  animation: cameraSpin 0.8s linear infinite;
}

/* Dark theme: based on the component class, not global scoped selectors. */
.room-cameras.theme-dark {
  --camera-bg: #090d16;
  --camera-surface: rgba(17, 24, 39, 0.94);
  --camera-surface-solid: #111827;
  --camera-border: rgba(148, 163, 184, 0.14);
  --camera-border-strong: rgba(148, 163, 184, 0.2);
  --camera-text: #f8fafc;
  --camera-text-soft: #cbd5e1;
  --camera-muted: #94a3b8;
  --camera-shadow: 0 22px 60px rgba(0, 0, 0, 0.34);
  --camera-video: #020617;
}

.room-cameras.theme-dark .camera-shell {
  background:
    radial-gradient(circle at 100% 0, rgba(var(--camera-primary-rgb), 0.13), transparent 28%),
    radial-gradient(circle at 0 100%, rgba(var(--camera-primary-rgb), 0.08), transparent 30%),
    var(--camera-surface);
  border-color: var(--camera-border);
  box-shadow: var(--camera-shadow);
}

.room-cameras.theme-dark .camera-shell::before {
  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.025),
      transparent 34%,
      transparent 70%,
      rgba(var(--camera-primary-rgb), 0.05)
    );
}

.room-cameras.theme-dark .camera-toggle {
  color: var(--camera-text);
  background: #111827;
  border-color: var(--camera-border);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
}

.room-cameras.theme-dark .camera-toggle.active {
  color: #fda4af;
  background: rgba(127, 29, 29, 0.22);
  border-color: rgba(248, 113, 113, 0.2);
}

.room-cameras.theme-dark .share-toggle {
  color: #c4b5fd;
  background: rgba(var(--camera-primary-rgb), 0.12);
  border-color: rgba(var(--camera-primary-rgb), 0.18);
}

.room-cameras.theme-dark .share-toggle.sharing {
  color: #6ee7b7;
  background: rgba(6, 78, 59, 0.26);
  border-color: rgba(52, 211, 153, 0.18);
}

.room-cameras.theme-dark .action-copy small {
  color: #94a3b8;
}

.room-cameras.theme-dark .camera-card {
  background: #020617;
  border: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.3);
}

.room-cameras.theme-dark .empty-cameras {
  background: rgba(15, 23, 42, 0.72);
  border-color: rgba(148, 163, 184, 0.18);
}

.room-cameras.theme-dark .empty-icon {
  background: rgba(var(--camera-primary-rgb), 0.12);
  color: var(--camera-primary);
}

.room-cameras.theme-dark .empty-cameras h3 {
  color: #f8fafc;
}

.room-cameras.theme-dark .empty-cameras p {
  color: #94a3b8;
}

.room-cameras.theme-dark .empty-camera-button {
  background: linear-gradient(135deg, var(--camera-primary), rgba(var(--camera-primary-rgb), 0.78));
  box-shadow: 0 14px 30px rgba(var(--camera-primary-rgb), 0.2);
}

.room-cameras.theme-dark .heading-icon {
  background: linear-gradient(145deg, rgba(var(--camera-primary-rgb), 0.2), rgba(var(--camera-primary-rgb), 0.07));
}

@keyframes cameraSpin {
  to { transform: rotate(360deg); }
}

</style>
