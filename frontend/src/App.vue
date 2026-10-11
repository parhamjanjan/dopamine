<template>
  <div id="app-shell" dir="rtl">
    <RouterView />

    <!-- Minimal, fluid Dopamine cursor -->
    <div id="dopamine-cursor" aria-hidden="true">
      <span class="dc-glow"></span>
      <span class="dc-ring dc-ring--outer"></span>
      <span class="dc-ring dc-ring--inner"></span>
      <span class="dc-core"><i></i></span>
      <span class="dc-spark dc-spark--one"></span>
      <span class="dc-spark dc-spark--two"></span>
    </div>
    <div id="dopamine-cursor-trail" aria-hidden="true"></div>
    <div id="dopamine-cursor-particles" aria-hidden="true"></div>
    <div id="dopamine-cursor-effects" aria-hidden="true"></div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useTheme } from './composables/useTheme'

const auth = useAuthStore()
const { applyTheme } = useTheme()

let destroyCursor = null

onMounted(async () => {
  if (auth.accessToken) {
    try {
      await auth.fetchUser()
    } catch (error) {
      console.error('خطا در دریافت اطلاعات کاربر:', error)
    }
  }

  applyTheme()
  destroyCursor = mountDopamineCursor()
})

onBeforeUnmount(() => {
  destroyCursor?.()
  destroyCursor = null
})

function mountDopamineCursor() {
  const pointerQuery = window.matchMedia('(hover: hover) and (pointer: fine)')
  if (!pointerQuery.matches) return null

  const cursor = document.getElementById('dopamine-cursor')
  const trail = document.getElementById('dopamine-cursor-trail')
  const particles = document.getElementById('dopamine-cursor-particles')
  const effects = document.getElementById('dopamine-cursor-effects')
  if (!cursor || !trail || !particles || !effects) return null

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
  const trailCount = reducedMotion.matches ? 4 : 15
  const particleLimit = reducedMotion.matches ? 8 : 34
  const trailDots = []
  let mouseX = window.innerWidth / 2
  let mouseY = window.innerHeight / 2
  let smoothX = mouseX
  let smoothY = mouseY
  let rafId = 0
  let lastParticleTime = 0
  let lastParticleX = mouseX
  let lastParticleY = mouseY
  let isInside = false
  let destroyed = false
  let clickTimeout = 0
  let hoverElement = null

  for (let i = 0; i < trailCount; i += 1) {
    const dot = document.createElement('span')
    dot.className = 'dc-trail-dot'
    dot.style.setProperty('--trail-index', i)
    dot.style.setProperty('--trail-size', `${Math.max(2, 7 - i * 0.34)}px`)
    trail.appendChild(dot)
    trailDots.push({
      el: dot,
      x: mouseX,
      y: mouseY,
      lag: Math.max(0.13, 0.38 - i * 0.018),
    })
  }

  const findInteractive = (target) => {
    if (!(target instanceof Element)) return null
    return target.closest(
      'a, button, input, textarea, select, summary, label, [role="button"], [role="link"], [tabindex]:not([tabindex="-1"]), .cursor-pointer',
    )
  }

  const updateHover = (target) => {
    const next = findInteractive(target)
    if (next === hoverElement) return
    hoverElement = next
    document.body.classList.toggle('dc-hover', Boolean(next))
    cursor.classList.toggle('dc-form-control', Boolean(next?.matches('input, textarea, select')))
  }

  const addParticle = (x, y, burst = false) => {
    if (reducedMotion.matches && !burst) return
    while (particles.childElementCount >= particleLimit) {
      particles.firstElementChild?.remove()
    }

    const particle = document.createElement('span')
    const type = Math.random()
    particle.className = `dc-particle ${type > 0.72 ? 'dc-particle--diamond' : type > 0.38 ? 'dc-particle--plus' : 'dc-particle--dot'}`
    const angle = Math.random() * Math.PI * 2
    const distance = burst ? 24 + Math.random() * 58 : 8 + Math.random() * 24
    const size = burst ? 3 + Math.random() * 3.5 : 1.8 + Math.random() * 2.2
    particle.style.left = `${x}px`
    particle.style.top = `${y}px`
    particle.style.width = `${size}px`
    particle.style.height = `${size}px`
    particle.style.setProperty('--fly-x', `${Math.cos(angle) * distance}px`)
    particle.style.setProperty('--fly-y', `${Math.sin(angle) * distance}px`)
    particle.style.setProperty('--spin', `${Math.random() * 240 - 120}deg`)
    particle.style.setProperty('--particle-life', `${burst ? 620 + Math.random() * 240 : 480 + Math.random() * 240}ms`)
    particles.appendChild(particle)
    particle.addEventListener('animationend', () => particle.remove(), { once: true })
  }

  const addShockwave = (x, y) => {
    const wave = document.createElement('span')
    wave.className = 'dc-shockwave'
    wave.style.left = `${x}px`
    wave.style.top = `${y}px`
    effects.appendChild(wave)
    wave.addEventListener('animationend', () => wave.remove(), { once: true })

    const flash = document.createElement('span')
    flash.className = 'dc-flash'
    flash.style.left = `${x}px`
    flash.style.top = `${y}px`
    effects.appendChild(flash)
    flash.addEventListener('animationend', () => flash.remove(), { once: true })
  }

  const onMove = (event) => {
    mouseX = event.clientX
    mouseY = event.clientY
    isInside = true
    document.body.classList.add('dc-visible')
    updateHover(event.target)

    if (reducedMotion.matches) {
      smoothX = mouseX
      smoothY = mouseY
    }

    const now = performance.now()
    const moved = Math.hypot(mouseX - lastParticleX, mouseY - lastParticleY)
    if (moved > 8 && now - lastParticleTime > 24) {
      addParticle(mouseX, mouseY)
      lastParticleX = mouseX
      lastParticleY = mouseY
      lastParticleTime = now
    }
  }

  const onOver = (event) => updateHover(event.target)
  const onOut = (event) => updateHover(event.relatedTarget)

  const onDown = (event) => {
    mouseX = event.clientX
    mouseY = event.clientY
    document.body.classList.add('dc-click')
    addShockwave(mouseX, mouseY)
    const burstCount = reducedMotion.matches ? 4 : 13
    for (let i = 0; i < burstCount; i += 1) addParticle(mouseX, mouseY, true)
    window.clearTimeout(clickTimeout)
    clickTimeout = window.setTimeout(() => document.body.classList.remove('dc-click'), 500)
  }

  const onUp = () => document.body.classList.remove('dc-click')
  const onLeave = () => {
    isInside = false
    document.body.classList.remove('dc-visible', 'dc-hover', 'dc-click')
  }
  const onEnter = () => {
    isInside = true
  }
  const onBlur = () => {
    isInside = false
    document.body.classList.remove('dc-visible', 'dc-hover', 'dc-click')
  }
  const onFocus = () => {
    if (isInside) document.body.classList.add('dc-visible')
  }

  const animate = () => {
    if (destroyed) return

    const ease = reducedMotion.matches ? 1 : 0.31
    smoothX += (mouseX - smoothX) * ease
    smoothY += (mouseY - smoothY) * ease
    cursor.style.transform = `translate3d(${smoothX}px, ${smoothY}px, 0) translate(-50%, -50%)`

    let nextX = mouseX
    let nextY = mouseY
    trailDots.forEach((dot) => {
      dot.x += (nextX - dot.x) * dot.lag
      dot.y += (nextY - dot.y) * dot.lag
      dot.el.style.transform = `translate3d(${dot.x}px, ${dot.y}px, 0) translate(-50%, -50%)`
      nextX = dot.x
      nextY = dot.y
    })

    rafId = window.requestAnimationFrame(animate)
  }

  document.addEventListener('pointermove', onMove, { passive: true })
  document.addEventListener('pointerover', onOver, { passive: true })
  document.addEventListener('pointerout', onOut, { passive: true })
  document.addEventListener('pointerdown', onDown, { passive: true })
  document.addEventListener('pointerup', onUp, { passive: true })
  document.addEventListener('mouseleave', onLeave)
  document.addEventListener('mouseenter', onEnter)
  window.addEventListener('blur', onBlur)
  window.addEventListener('focus', onFocus)
  rafId = window.requestAnimationFrame(animate)

  return () => {
    destroyed = true
    window.cancelAnimationFrame(rafId)
    window.clearTimeout(clickTimeout)
    document.removeEventListener('pointermove', onMove)
    document.removeEventListener('pointerover', onOver)
    document.removeEventListener('pointerout', onOut)
    document.removeEventListener('pointerdown', onDown)
    document.removeEventListener('pointerup', onUp)
    document.removeEventListener('mouseleave', onLeave)
    document.removeEventListener('mouseenter', onEnter)
    window.removeEventListener('blur', onBlur)
    window.removeEventListener('focus', onFocus)
    document.body.classList.remove('dc-visible', 'dc-hover', 'dc-click')
    trailDots.forEach(({ el }) => el.remove())
    particles.replaceChildren()
    effects.replaceChildren()
  }
}
</script>

<style>
/* Dopamine — polished cursor system. The pointer itself stays small and precise. */
@media (hover: hover) and (pointer: fine) {
  html, body, #app, #app-shell, #app-shell * { cursor: none !important; }

  #dopamine-cursor, #dopamine-cursor-trail, #dopamine-cursor-particles, #dopamine-cursor-effects {
    position: fixed; inset: 0; pointer-events: none; overflow: visible;
  }
  #dopamine-cursor { --dc-primary: var(--primary, #8b5cf6); --dc-rgb: var(--primary-rgb, 112,85,232);
    z-index: 2147483647; inset: auto; left: 0; top: 0; width: 42px; height: 42px;
    opacity: 0; will-change: transform; transition: opacity .18s ease; isolation: isolate;
  }
  #dopamine-cursor-trail { z-index: 2147483645; opacity: 0; transition: opacity .18s ease; }
  #dopamine-cursor-particles { z-index: 2147483646; }
  #dopamine-cursor-effects { z-index: 2147483644; }
  body.dc-visible #dopamine-cursor, body.dc-visible #dopamine-cursor-trail { opacity: 1; }

  .dc-glow { position:absolute; left:50%; top:50%; width:66px; height:66px; border-radius:50%;
    transform:translate(-50%,-50%); background:radial-gradient(circle,rgba(var(--dc-rgb),.24) 0%,rgba(var(--dc-rgb),.12) 32%,rgba(93,225,255,.055) 48%,transparent 72%);
    filter:blur(4px); transition:width .3s cubic-bezier(.2,.8,.2,1),height .3s cubic-bezier(.2,.8,.2,1),opacity .2s;
  }
  .dc-ring { position:absolute; left:50%; top:50%; border-radius:50%; transform:translate(-50%,-50%); box-sizing:border-box; }
  .dc-ring--outer { width:29px; height:29px; border:1px solid rgba(var(--dc-rgb),.72);
    border-top-color:#fff; border-right-color:rgba(125,239,255,.95); box-shadow:0 0 7px rgba(var(--dc-rgb),.28),inset 0 0 6px rgba(var(--dc-rgb),.08);
    animation:dc-orbit 4s linear infinite;
  }
  .dc-ring--inner { width:17px; height:17px; border:1px dashed rgba(255,255,255,.72); opacity:.8; animation:dc-orbit-reverse 6s linear infinite; }
  .dc-core { position:absolute; left:50%; top:50%; width:7px; height:7px; display:grid; place-items:center;
    border-radius:50%; transform:translate(-50%,-50%); background:#fff; box-shadow:0 0 5px #fff,0 0 12px rgba(var(--dc-rgb),1),0 0 23px rgba(var(--dc-rgb),.85);
  }
  .dc-core i { display:block; width:3px; height:3px; border-radius:50%; background:#a9f8ff; box-shadow:0 0 6px #a9f8ff; }
  .dc-spark { position:absolute; width:3px; height:3px; border-radius:50%; background:#fff; box-shadow:0 0 8px #fff,0 0 13px #7defff; }
  .dc-spark--one { left:5px; top:8px; animation:dc-twinkle 1.5s ease-in-out infinite; }
  .dc-spark--two { right:3px; bottom:7px; animation:dc-twinkle 1.9s ease-in-out infinite reverse; }

  .dc-trail-dot { position:fixed; left:0; top:0; width:var(--trail-size,5px); height:var(--trail-size,5px); border-radius:50%;
    background:rgba(180,158,255,calc(.75 - var(--trail-index,0)*.035)); box-shadow:0 0 9px rgba(var(--dc-rgb,112,85,232),.8);
    opacity:calc(.78 - var(--trail-index,0)*.045); will-change:transform; }
  .dc-particle { position:fixed; left:0; top:0; display:block; border-radius:50%; background:#fff; pointer-events:none;
    box-shadow:0 0 5px #fff,0 0 11px rgba(124,237,255,.9),0 0 17px rgba(var(--primary-rgb,112,85,232),.85);
    animation:dc-particle-flight var(--particle-life,600ms) cubic-bezier(.16,1,.3,1) forwards;
  }
  .dc-particle--diamond { border-radius:1px; transform:rotate(45deg); background:#c8faff; }
  .dc-particle--plus { width:5px!important; height:1px!important; border-radius:2px; }
  .dc-shockwave { position:fixed; width:14px; height:14px; margin:-7px 0 0 -7px; border:1px solid rgba(255,255,255,.9); border-radius:50%;
    box-shadow:0 0 10px rgba(var(--primary-rgb,112,85,232),.8),inset 0 0 8px rgba(var(--primary-rgb,112,85,232),.25);
    animation:dc-shockwave .58s cubic-bezier(.12,.72,.22,1) forwards;
  }
  .dc-flash { position:fixed; width:7px; height:7px; margin:-3.5px 0 0 -3.5px; border-radius:50%; background:#fff;
    box-shadow:0 0 10px #fff,0 0 25px rgba(var(--primary-rgb,112,85,232),1); animation:dc-flash .22s ease-out forwards;
  }
  body.dc-hover .dc-glow { width:92px; height:92px; }
  body.dc-hover .dc-ring--outer { width:35px; height:35px; border-width:1.5px; }
  body.dc-hover .dc-ring--inner { width:22px; height:22px; border-style:solid; opacity:1; }
  body.dc-hover .dc-core { width:9px; height:9px; }
  body.dc-form-control .dc-ring--outer { border-color:rgba(125,239,255,.95); }
  body.dc-click .dc-glow { width:110px; height:110px; }
  body.dc-click .dc-ring--outer { animation-duration:.55s; }

  @keyframes dc-orbit { to { transform:translate(-50%,-50%) rotate(360deg); } }
  @keyframes dc-orbit-reverse { to { transform:translate(-50%,-50%) rotate(-360deg); } }
  @keyframes dc-twinkle { 0%,100% { opacity:.35; transform:scale(.65); } 50% { opacity:1; transform:scale(1.5); } }
  @keyframes dc-particle-flight { 0% { opacity:1; transform:translate3d(0,0,0) rotate(0) scale(1); } 100% { opacity:0; transform:translate3d(var(--fly-x),var(--fly-y),0) rotate(var(--spin,90deg)) scale(.12); } }
  @keyframes dc-shockwave { 0% { opacity:.95; transform:scale(.35); } 70% { opacity:.6; } 100% { opacity:0; transform:scale(6.5); } }
  @keyframes dc-flash { 0% { opacity:1; transform:scale(.4); } 100% { opacity:0; transform:scale(3.2); } }
}
@media (hover: none), (pointer: coarse) {
  #dopamine-cursor, #dopamine-cursor-trail, #dopamine-cursor-particles, #dopamine-cursor-effects { display:none!important; }
}
@media (prefers-reduced-motion: reduce) {
  .dc-ring, .dc-spark { animation-duration:8s!important; }
}
</style>