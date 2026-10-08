<template>
  <div dir="rtl">
    <RouterView />

   
  </div>
<!-- =====================================================
     DOPAMINE LASER CURSOR
===================================================== -->

<div
  id="dopamine-laser-cursor"
  aria-hidden="true"
>
  <div class="laser-core">
    <span></span>
  </div>

  <div class="laser-ring laser-ring-1"></div>
  <div class="laser-ring laser-ring-2"></div>
  <div class="laser-ring laser-ring-3"></div>

  <div class="laser-aura"></div>

  <div class="laser-cross laser-cross-x"></div>
  <div class="laser-cross laser-cross-y"></div>
</div>

<div
  id="dopamine-laser-trail"
  aria-hidden="true"
></div>

<div
  id="dopamine-laser-particles"
  aria-hidden="true"
></div>

</template>
<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useTheme } from './composables/useTheme'

const auth = useAuthStore()
const { applyTheme } = useTheme()

onMounted(async () => {
  if (auth.accessToken) {
    try {
      await auth.fetchUser()
    } catch (error) {
      console.error('خطا در دریافت اطلاعات کاربر:', error)
    }
  }

  applyTheme()
})
/* =========================================================
   DOPAMINE — LASER CURSOR ENGINE
========================================================= */

import {
  onBeforeUnmount
} from "vue";


let destroyLaserCursor = null;


onMounted(() => {

  /* فقط دستگاه‌های دارای موس واقعی */

  const pointer =
    window.matchMedia(
      "(hover: hover) and (pointer: fine)"
    );

  if (!pointer.matches) {
    return;
  }


  const cursor =
    document.getElementById(
      "dopamine-laser-cursor"
    );

  const trail =
    document.getElementById(
      "dopamine-laser-trail"
    );

  const particles =
    document.getElementById(
      "dopamine-laser-particles"
    );


  if (
    !cursor ||
    !trail ||
    !particles
  ) {
    return;
  }


  /* =======================================================
     SETTINGS
  ======================================================= */

  const TRAIL_COUNT = 13;

  const trailDots = [];

  for (
    let i = 0;
    i < TRAIL_COUNT;
    i++
  ) {

    const dot =
      document.createElement("span");

    dot.className =
      "laser-trail-dot";

    const size =
      2.5 -
      (i / TRAIL_COUNT) * 1.7;

    dot.style.width =
      `${Math.max(size, 1)}px`;

    dot.style.height =
      `${Math.max(size, 1)}px`;

    dot.style.opacity =
      `${1 - i / (TRAIL_COUNT + 1)}`;

    trail.appendChild(dot);

    trailDots.push({
      element: dot,
      x: window.innerWidth / 2,
      y: window.innerHeight / 2
    });
  }


  /* =======================================================
     MOUSE STATE
  ======================================================= */

  let mouseX =
    window.innerWidth / 2;

  let mouseY =
    window.innerHeight / 2;

  let cursorX = mouseX;
  let cursorY = mouseY;

  let lastParticleTime = 0;

  let animationFrame = null;

  let mouseInside = false;


  /* =======================================================
     MOUSE MOVE
  ======================================================= */

  const handleMouseMove = (event) => {

    mouseX = event.clientX;
    mouseY = event.clientY;

    mouseInside = true;

    document.body.classList.add(
      "laser-cursor-visible"
    );
  };


  /* =======================================================
     SMOOTH MAIN CURSOR
  ======================================================= */

  const animate = (time) => {

    /* Cursor اصلی */

    cursorX +=
      (mouseX - cursorX) * 0.32;

    cursorY +=
      (mouseY - cursorY) * 0.32;


    cursor.style.transform =
      `translate3d(
        ${cursorX}px,
        ${cursorY}px,
        0
      ) translate(-50%, -50%)`;


    /* =====================================================
       TRAIL CHAIN
    ===================================================== */

    let previousX = mouseX;
    let previousY = mouseY;


    trailDots.forEach(
      (dot, index) => {

        const follow =
          index === 0
            ? 0.32
            : 0.20;


        dot.x +=
          (previousX - dot.x) * follow;

        dot.y +=
          (previousY - dot.y) * follow;


        dot.element.style.transform =
          `translate3d(
            ${dot.x}px,
            ${dot.y}px,
            0
          ) translate(-50%, -50%)`;


        previousX = dot.x;
        previousY = dot.y;
      }
    );


    /* =====================================================
       RANDOM LASER PARTICLES
    ===================================================== */

    if (
      mouseInside &&
      time - lastParticleTime > 42
    ) {

      createParticle(
        mouseX,
        mouseY
      );

      lastParticleTime = time;
    }


    animationFrame =
      requestAnimationFrame(animate);
  };


  /* =======================================================
     PARTICLE GENERATOR
  ======================================================= */

  const createParticle = (
    x,
    y
  ) => {

    /*
      همیشه ذره نسازیم تا performance حفظ شود
    */

    if (
      particles.childElementCount > 35
    ) {
      return;
    }


    const particle =
      document.createElement("span");

    particle.className =
      "laser-particle";


    const angle =
      Math.random() *
      Math.PI *
      2;

    const distance =
      8 +
      Math.random() * 20;


    particle.style.left =
      `${x}px`;

    particle.style.top =
      `${y}px`;


    particle.style.setProperty(
      "--particle-x",
      `${Math.cos(angle) * distance}px`
    );

    particle.style.setProperty(
      "--particle-y",
      `${Math.sin(angle) * distance}px`
    );


    const size =
      1.5 +
      Math.random() * 2.5;

    particle.style.width =
      `${size}px`;

    particle.style.height =
      `${size}px`;


    particles.appendChild(
      particle
    );


    particle.addEventListener(
      "animationend",
      () => {

        particle.remove();

      },
      {
        once: true
      }
    );
  };


  /* =======================================================
     HOVER
  ======================================================= */

  const isInteractive = (element) => {

    if (
      !element ||
      !(element instanceof Element)
    ) {
      return false;
    }


    return Boolean(
      element.closest(
        [
          "a",
          "button",
          "input",
          "textarea",
          "select",
          "[role='button']",
          ".cursor-pointer"
        ].join(",")
      )
    );
  };


  const handleMouseOver = (event) => {

    if (
      isInteractive(event.target)
    ) {

      document.body.classList.add(
        "laser-cursor-hover"
      );
    }
  };


  const handleMouseOut = (event) => {

    const target =
      event.relatedTarget;


    if (
      !isInteractive(target)
    ) {

      document.body.classList.remove(
        "laser-cursor-hover"
      );
    }
  };


  /* =======================================================
     CLICK
  ======================================================= */

  const handleMouseDown = () => {

    document.body.classList.add(
      "laser-cursor-click"
    );


    /*
      یک burst کوچک از ذرات
    */

    for (
      let i = 0;
      i < 7;
      i++
    ) {

      createParticle(
        mouseX,
        mouseY
      );
    }
  };


  const handleMouseUp = () => {

    window.setTimeout(
      () => {

        document.body.classList.remove(
          "laser-cursor-click"
        );

      },
      550
    );
  };


  /* =======================================================
     LEAVE / ENTER
  ======================================================= */

  const handleMouseLeave = () => {

    mouseInside = false;

    document.body.classList.remove(
      "laser-cursor-visible",
      "laser-cursor-hover"
    );
  };


  const handleMouseEnter = () => {

    mouseInside = true;

    document.body.classList.add(
      "laser-cursor-visible"
    );
  };


  /* =======================================================
     EVENTS
  ======================================================= */

  document.addEventListener(
    "mousemove",
    handleMouseMove,
    { passive: true }
  );

  document.addEventListener(
    "mouseover",
    handleMouseOver,
    { passive: true }
  );

  document.addEventListener(
    "mouseout",
    handleMouseOut,
    { passive: true }
  );

  document.addEventListener(
    "mousedown",
    handleMouseDown,
    { passive: true }
  );

  document.addEventListener(
    "mouseup",
    handleMouseUp,
    { passive: true }
  );

  document.addEventListener(
    "mouseleave",
    handleMouseLeave
  );

  document.addEventListener(
    "mouseenter",
    handleMouseEnter
  );


  /* =======================================================
     START
  ======================================================= */

  animationFrame =
    requestAnimationFrame(animate);


  /* =======================================================
     CLEANUP
  ======================================================= */

  destroyLaserCursor = () => {

    if (animationFrame) {
      cancelAnimationFrame(
        animationFrame
      );
    }


    document.removeEventListener(
      "mousemove",
      handleMouseMove
    );

    document.removeEventListener(
      "mouseover",
      handleMouseOver
    );

    document.removeEventListener(
      "mouseout",
      handleMouseOut
    );

    document.removeEventListener(
      "mousedown",
      handleMouseDown
    );

    document.removeEventListener(
      "mouseup",
      handleMouseUp
    );

    document.removeEventListener(
      "mouseleave",
      handleMouseLeave
    );

    document.removeEventListener(
      "mouseenter",
      handleMouseEnter
    );


    document.body.classList.remove(
      "laser-cursor-visible",
      "laser-cursor-hover",
      "laser-cursor-click"
    );


    trailDots.forEach(
      (dot) => {
        dot.element.remove();
      }
    );


    particles.innerHTML = "";
  };

});


onBeforeUnmount(() => {

  if (destroyLaserCursor) {

    destroyLaserCursor();

    destroyLaserCursor = null;
  }

});

</script>

<style>
/* =========================================================
   DOPAMINE — PREMIUM LASER CURSOR
   رنگ کاملاً متصل به Theme System
   --primary
   --primary-rgb
========================================================= */

@media (hover: hover) and (pointer: fine) {

  /* -------------------------------------------------------
     Hide native cursor
  ------------------------------------------------------- */

  html,
  body,
  #app,
  #app *,
  a,
  button,
  input,
  textarea,
  select {
    cursor: none !important;
  }


  /* =======================================================
     MAIN CURSOR
  ======================================================= */

  #dopamine-laser-cursor {

    position: fixed;

    left: 0;
    top: 0;

    width: 22px;
    height: 22px;

    pointer-events: none;

    z-index: 2147483647;

    opacity: 0;

    transform:
      translate3d(-100px, -100px, 0);

    will-change: transform;

    transition:
      opacity .2s ease,
      width .3s cubic-bezier(.16,1,.3,1),
      height .3s cubic-bezier(.16,1,.3,1);
  }


  /* =======================================================
     WHITE LASER CORE
  ======================================================= */

  .laser-core {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 5px;
    height: 5px;

    transform:
      translate(-50%, -50%);

    border-radius: 50%;

    background: #fff;

    box-shadow:

      0 0 2px #fff,

      0 0 5px #fff,

      0 0 9px var(--primary),

      0 0 18px var(--primary),

      0 0 32px rgba(var(--primary-rgb), .95),

      0 0 55px rgba(var(--primary-rgb), .65);

    z-index: 10;

    transition:
      width .2s ease,
      height .2s ease;
  }


  .laser-core span {

    position: absolute;

    inset: -5px;

    border-radius: 50%;

    background:
      radial-gradient(
        circle,
        rgba(255,255,255,.9) 0%,
        rgba(var(--primary-rgb), .55) 35%,
        transparent 72%
      );

    filter: blur(2px);

    animation:
      laser-core-pulse 1.3s
      ease-in-out infinite;
  }


  /* =======================================================
     ENERGY RINGS
  ======================================================= */

  .laser-ring {

    position: absolute;

    left: 50%;
    top: 50%;

    border-radius: 50%;

    transform:
      translate(-50%, -50%);

    border:
      1px solid
      rgba(var(--primary-rgb), .75);

    box-shadow:
      0 0 8px
      rgba(var(--primary-rgb), .45),

      inset 0 0 7px
      rgba(var(--primary-rgb), .25);

    opacity: .75;
  }


  .laser-ring-1 {

    width: 22px;
    height: 22px;

    animation:
      laser-ring-1
      2s
      linear
      infinite;
  }


  .laser-ring-2 {

    width: 34px;
    height: 34px;

    border-style: dashed;

    opacity: .42;

    animation:
      laser-ring-2
      3.5s
      linear
      infinite;
  }


  .laser-ring-3 {

    width: 48px;
    height: 48px;

    border-color:
      rgba(var(--primary-rgb), .22);

    box-shadow:
      0 0 18px
      rgba(var(--primary-rgb), .15);

    opacity: .35;

    animation:
      laser-ring-3
      5s
      linear
      infinite;
  }


  /* =======================================================
     AURA
  ======================================================= */

  .laser-aura {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 110px;
    height: 110px;

    transform:
      translate(-50%, -50%);

    border-radius: 50%;

    background:
      radial-gradient(
        circle,

        rgba(var(--primary-rgb), .16)
        0%,

        rgba(var(--primary-rgb), .09)
        22%,

        rgba(var(--primary-rgb), .035)
        45%,

        transparent
        72%
      );

    filter: blur(5px);

    opacity: .85;

    transition:
      width .4s cubic-bezier(.16,1,.3,1),
      height .4s cubic-bezier(.16,1,.3,1),
      opacity .3s ease;
  }


  /* =======================================================
     CROSSHAIR LASER
  ======================================================= */

  .laser-cross {

    position: absolute;

    left: 50%;
    top: 50%;

    background:
      linear-gradient(
        90deg,
        transparent,
        rgba(var(--primary-rgb), .65),
        transparent
      );

    opacity: .18;
  }


  .laser-cross-x {

    width: 62px;
    height: 1px;

    transform:
      translate(-50%, -50%);
  }


  .laser-cross-y {

    width: 1px;
    height: 62px;

    transform:
      translate(-50%, -50%);

    background:
      linear-gradient(
        180deg,
        transparent,
        rgba(var(--primary-rgb), .65),
        transparent
      );
  }


  /* =======================================================
     TRAIL CONTAINER
  ======================================================= */

  #dopamine-laser-trail {

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 2147483645;

    overflow: hidden;

    opacity: 0;
  }


  /* =======================================================
     TRAIL DOTS
  ======================================================= */

  .laser-trail-dot {

    position: fixed;

    left: 0;
    top: 0;

    width: 5px;
    height: 5px;

    border-radius: 50%;

    pointer-events: none;

    background: var(--primary);

    box-shadow:

      0 0 5px
      rgba(var(--primary-rgb), 1),

      0 0 12px
      rgba(var(--primary-rgb), .8),

      0 0 24px
      rgba(var(--primary-rgb), .45);

    transform:
      translate(-50%, -50%);

    will-change: transform, opacity;

    transition:
      opacity .12s linear;
  }


  /* =======================================================
     PARTICLES
  ======================================================= */

  #dopamine-laser-particles {

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 2147483644;

    overflow: hidden;
  }


  .laser-particle {

    position: fixed;

    width: 3px;
    height: 3px;

    border-radius: 50%;

    pointer-events: none;

    background: #fff;

    box-shadow:
      0 0 5px #fff,
      0 0 12px var(--primary),
      0 0 20px var(--primary);

    transform:
      translate(-50%, -50%);

    animation:
      laser-particle-fade
      .65s
      ease-out
      forwards;
  }


  /* =======================================================
     ACTIVE
  ======================================================= */

  body.laser-cursor-visible
  #dopamine-laser-cursor {

    opacity: 1;
  }


  body.laser-cursor-visible
  #dopamine-laser-trail {

    opacity: 1;
  }


  /* =======================================================
     HOVER
  ======================================================= */

  body.laser-cursor-hover
  #dopamine-laser-cursor {

    width: 38px;
    height: 38px;
  }


  body.laser-cursor-hover
  .laser-core {

    width: 7px;
    height: 7px;

    box-shadow:

      0 0 3px #fff,

      0 0 8px #fff,

      0 0 15px var(--primary),

      0 0 30px var(--primary),

      0 0 55px
      rgba(var(--primary-rgb), 1),

      0 0 90px
      rgba(var(--primary-rgb), .55);
  }


  body.laser-cursor-hover
  .laser-ring-1 {

    width: 38px;
    height: 38px;
  }


  body.laser-cursor-hover
  .laser-ring-2 {

    width: 54px;
    height: 54px;
  }


  body.laser-cursor-hover
  .laser-ring-3 {

    width: 70px;
    height: 70px;
  }


  body.laser-cursor-hover
  .laser-aura {

    width: 155px;
    height: 155px;

    opacity: 1;
  }


  body.laser-cursor-hover
  .laser-cross {

    opacity: .3;
  }


  /* =======================================================
     CLICK
  ======================================================= */

  body.laser-cursor-click
  .laser-ring-1 {

    animation:
      laser-click
      .55s
      cubic-bezier(.16,1,.3,1);
  }


  body.laser-cursor-click
  .laser-aura {

    width: 190px;
    height: 190px;

    opacity: 1;
  }


  body.laser-cursor-click
  .laser-core {

    width: 10px;
    height: 10px;
  }


  /* =======================================================
     ANIMATIONS
  ======================================================= */

  @keyframes laser-core-pulse {

    0%,
    100% {
      transform: scale(.8);
      opacity: .55;
    }

    50% {
      transform: scale(1.25);
      opacity: 1;
    }
  }


  @keyframes laser-ring-1 {

    0% {
      transform:
        translate(-50%, -50%)
        rotate(0deg)
        scale(1);
    }

    50% {
      transform:
        translate(-50%, -50%)
        rotate(180deg)
        scale(1.12);
    }

    100% {
      transform:
        translate(-50%, -50%)
        rotate(360deg)
        scale(1);
    }
  }


  @keyframes laser-ring-2 {

    0% {
      transform:
        translate(-50%, -50%)
        rotate(360deg)
        scale(.95);
    }

    100% {
      transform:
        translate(-50%, -50%)
        rotate(0deg)
        scale(1.08);
    }
  }


  @keyframes laser-ring-3 {

    0% {
      transform:
        translate(-50%, -50%)
        rotate(0deg)
        scale(1);
    }

    50% {
      transform:
        translate(-50%, -50%)
        rotate(180deg)
        scale(.9);
    }

    100% {
      transform:
        translate(-50%, -50%)
        rotate(360deg)
        scale(1);
    }
  }


  @keyframes laser-click {

    0% {
      transform:
        translate(-50%, -50%)
        scale(.5);

      opacity: 1;
    }

    100% {
      transform:
        translate(-50%, -50%)
        scale(3.5);

      opacity: 0;
    }
  }


  @keyframes laser-particle-fade {

    0% {
      opacity: 1;
      transform:
        translate(-50%, -50%)
        scale(1);
    }

    100% {
      opacity: 0;
      transform:
        translate(
          calc(-50% + var(--particle-x)),
          calc(-50% + var(--particle-y))
        )
        scale(.1);
    }
  }
}


/* =========================================================
   TOUCH DEVICES
========================================================= */

@media (hover: none), (pointer: coarse) {

  #dopamine-laser-cursor,
  #dopamine-laser-trail,
  #dopamine-laser-particles {

    display: none !important;
  }

  html,
  body,
  #app,
  #app *,
  a,
  button,
  input,
  textarea,
  select {

    cursor: auto !important;
  }
}

</style>