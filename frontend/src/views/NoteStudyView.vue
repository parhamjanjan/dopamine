<template>
  <div class="quest" :class="{ 'theme-light': !isDark }" dir="rtl" @click="handleViewportNavigation">
    <div class="bg-stars" aria-hidden="true"></div>
    <div class="aurora a1" aria-hidden="true"></div>
    <div class="aurora a2" aria-hidden="true"></div>
    <div class="aurora a3" aria-hidden="true"></div>

    <div class="confetti" aria-hidden="true">
      <i
        v-for="c in confetti"
        :key="c.id"
        :style="{
          '--x': c.x,
          '--d': c.d + 's',
          '--t': c.t + 's',
          '--r': c.r + 'deg',
          '--c': c.c,
          width: c.s + 'px',
          height: c.s * 1.6 + 'px'
        }"
      ></i>
    </div>

    <header class="topbar">
      <RouterLink to="/notes" class="brand" aria-label="بازگشت به کتابخانه جزوه‌ها">
        <span class="gem" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2.8 14.6 9.4 21.2 12l-6.6 2.6L12 21.2l-2.6-6.6L2.8 12l6.6-2.6L12 2.8Z"/><path d="m18.5 2 .9 2.6L22 5.5l-2.6.9-.9 2.6-.9-2.6-2.6-.9 2.6-.9.9-2.6Z"/></svg></span>
        <span class="brand-copy">
          <b>DOPAMINE</b>
          <small>آکادمی ماجراجویی</small>
        </span>
      </RouterLink>

      <div class="top-actions">
        <button
          class="icon"
          type="button"
          :disabled="bookmarkBusy || loading || Boolean(error)"
          @click="toggleBookmark"
          :title="bookmarked ? 'حذف از ذخیره‌شده‌ها' : 'ذخیرهٔ جزوه'"
          :aria-label="bookmarked ? 'حذف از ذخیره‌شده‌ها' : 'ذخیرهٔ جزوه'"
        ><svg viewBox="0 0 24 24" aria-hidden="true"><path :d="bookmarked ? 'M12 20.2s-7.5-4.4-7.5-10.1A4.1 4.1 0 0 1 12 7.8a4.1 4.1 0 0 1 7.5 2.3c0 5.7-7.5 10.1-7.5 10.1Z' : 'M20.8 9.5c0 5.7-8.8 10.7-8.8 10.7S3.2 15.2 3.2 9.5A4.6 4.6 0 0 1 12 7.4a4.6 4.6 0 0 1 8.8 2.1Z'"/></svg></button>

        <button
          class="icon"
          type="button"
          @click="printNote"
          title="چاپ یا ذخیره به صورت PDF"
          aria-label="چاپ یا ذخیره به صورت PDF"
        ><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v11m-4-4 4 4 4-4M5 17v3h14v-3"/></svg></button>

        <RouterLink
          v-if="isAdmin"
          :to="`/notes/admin/${noteId}/edit`"
          class="icon"
          title="ویرایش جزوه"
          aria-label="ویرایش جزوه"
        ><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8.2a3.8 3.8 0 1 0 0 7.6 3.8 3.8 0 0 0 0-7.6Z"/><path d="m19.4 13.5 1.1.9-1.8 3.1-1.4-.5a7.9 7.9 0 0 1-1.5.9l-.2 1.5h-3.6l-.3-1.5a7.9 7.9 0 0 1-1.5-.9l-1.4.5L7 14.4l1.1-.9a7.6 7.6 0 0 1 0-1.8L7 10.8l1.8-3.1 1.4.5a7.9 7.9 0 0 1 1.5-.9l.3-1.5h3.6l.2 1.5a7.9 7.9 0 0 1 1.5.9l1.4-.5 1.8 3.1-1.1.9a7.6 7.6 0 0 1 0 1.8Z"/></svg></RouterLink>
      </div>

      <div class="top-progress" aria-label="پیشرفت مطالعه">
        <i :style="{ width: progressPercent + '%' }"></i>
      </div>
    </header>

    <div v-if="loading" class="state">
      <div class="portal"><span></span></div>
      <b>در حال آماده‌سازی دنیای یادگیری…</b>
      <p>چند لحظه صبر کن.</p>
    </div>

    <div v-else-if="error" class="state error-state">
      <div class="err-gem">!</div>
      <h2>این جزوه باز نشد</h2>
      <p>{{ error }}</p>
      <RouterLink to="/notes" class="btn primary">بازگشت به کتابخانه</RouterLink>
    </div>

    <main v-else class="world">
      <section class="hero" :style="{ '--cover': safeCoverColor }">
        <div class="hero-icon" aria-hidden="true"><svg viewBox="0 0 48 48"><path d="M8 10.5c6-2.1 11.3-1.3 16 2.1v26c-4.7-3.4-10-4.2-16-2.1v-26Z"/><path d="M40 10.5c-6-2.1-11.3-1.3-16 2.1v26c4.7-3.4 10-4.2 16-2.1v-26Z"/><path d="M13 17h6M13 22h6M29 17h6M29 22h6"/></svg></div>

        <div class="hero-copy">
          <div class="meta">
            {{ note.subject || 'درس آموزشی' }} · {{ note.grade || 'همهٔ پایه‌ها' }}
          </div>
          <h1>{{ note.title || 'ماجراجویی یادگیری' }}</h1>
          <p>{{ note.subtitle || 'هر مرحله یک قدرت تازه؛ هر قدم یک پیروزی.' }}</p>

          <div class="chips">
            <span><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.2 2"/></svg>{{ note.estimated_minutes || 10 }} دقیقه</span>
            <span><svg viewBox="0 0 24 24"><path d="M3 12s3.2-6 9-6 9 6 9 6-3.2 6-9 6-9-6-9-6Z"/><circle cx="12" cy="12" r="2.5"/></svg>{{ note.view_count || 0 }} بازدید</span>
            <span><svg viewBox="0 0 24 24"><path d="M5 4.5h14v15H5z"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>{{ stages.length }} مرحله</span>
          </div>
        </div>

        <div class="hero-card">
          <div class="ring" :style="{ '--p': progressPercent }">
            <b>{{ progressPercent }}%</b>
          </div>

          <div class="hero-card-text">
            <small>{{ progressPercent === 100 ? 'همه‌چیز کامل شد' : 'ادامهٔ مسیر' }}</small>
            <b>
              {{
                progressPercent === 100
                  ? 'مسیر را کامل کردی'
                  : (nextStage?.title || 'شروع کن')
              }}
            </b>
            <span>{{ completedCount }} از {{ totalBlocks }} بخش انجام شده</span>
          </div>

          <button class="btn primary" type="button" @click="continueQuest">
            {{
              progressPercent === 100
                ? 'مرور مسیر'
                : completedCount
                  ? 'ادامه بده'
                  : 'شروع ماجراجویی'
            }}
          </button>
        </div>
      </section>

      <section v-if="stages.length" class="timeline-wrap">
        <div class="timeline-heading">
          <div>
            <span class="timeline-kicker">LEARNING PATH</span>
            <h2>مسیر یادگیری</h2>
          </div>
          <span class="timeline-count">
            {{ completedStages }} از {{ stages.length }} مرحله تکمیل شده
          </span>
        </div>

        <div class="timeline">
          <button
            v-for="(stage, i) in stages"
            :key="stage.id"
            type="button"
            class="timeline-item"
            :class="{
              active: activeStageIndex === i,
              done: isStageDone(stage)
            }"
            @click="selectStage(i)"
            :aria-current="activeStageIndex === i ? 'step' : undefined"
          >
            <span class="timeline-index">
              <svg v-if="isStageDone(stage)" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg>
              <template v-else>{{ String(i + 1).padStart(2, '0') }}</template>
            </span>

            <span class="timeline-copy">
              <small>مرحلهٔ {{ String(i + 1).padStart(2, '0') }}</small>
              <strong>{{ stage.title }}</strong>
              <span>{{ stage.description }}</span>
            </span>

            <span class="timeline-status">
              {{
                isStageDone(stage)
                  ? 'تکمیل‌شده'
                  : activeStageIndex === i
                    ? 'در حال مطالعه'
                    : 'مشاهدهٔ مرحله'
              }}
            </span>
            <span class="timeline-arrow" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5m6 6-6-6 6-6"/></svg></span>
          </button>
        </div>
      </section>

      <section v-if="activeStage" class="study">
        <div class="stage-head">
          <div class="stage-title">
            <small>مرحلهٔ {{ activeStageIndex + 1 }} از {{ stages.length }}</small>
            <h2 class="typewriter-text">{{ typedStageTitle }}<span class="typing-caret" aria-hidden="true"></span></h2>
            <p class="stage-description">{{ typedStageDescription }}</p>
          </div>

          <div class="stage-medal" :class="{ won: isStageDone(activeStage) }" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 4h8v4.5a4 4 0 0 1-8 0V4Z"/><path d="M8 6H4v2a4 4 0 0 0 4 4M16 6h4v2a4 4 0 0 1-4 4M12 12.5V17m-4 3h8m-6-3h4"/></svg></div>
        </div>

        <div class="stage-track">
          <i :style="{ width: stagePercent(activeStage) + '%' }"></i>
          <span>{{ stagePercent(activeStage) }}%</span>
        </div>

        <TransitionGroup name="card" tag="div" class="stack">
          <article
            v-for="entry in activeStage.blocks"
            :key="entry.index"
            :id="`blk-${entry.index}`"
            :data-block-index="entry.index"
            data-block-card
            class="content-card"
            :class="[
              blockToneClass(entry.block),
              {
                'is-complete': isCompleted(entry.index),
                'is-current': currentBlock === entry.index,
                'is-revealed': isBlockRevealed(entry.index),
                'is-pending': !isBlockRevealed(entry.index)
              }
            ]"
          >

            <div v-if="isBlockRevealed(entry.index)" class="content block-content-reveal">
              <span v-if="typingBlockIndex === entry.index" class="block-typing-caret" aria-hidden="true"></span>
              <h2
                v-if="entry.block.type === 'heading'"
                class="c-heading"
                :class="`lv${entry.block.level || 2}`"
              >{{ blockDisplayText(entry, entry.block.text || entry.block.title) }}</h2>

              <p
  v-else-if="entry.block.type === 'paragraph'"
  class="c-para math-content"
  v-html="rich(blockDisplayText(entry, entry.block.text))"
></p>

              <ul v-else-if="entry.block.type === 'list'" class="c-list">
                <li v-for="(item, i) in listItems(entry.block)" :key="i">
                  <span class="list-bullet" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/></svg></span>
<div class="math-content" v-html="rich(item)"></div>                </li>
              </ul>

              <div
                v-else-if="entry.block.type === 'callout'"
                class="callout"
                :data-style="entry.block.style || 'tip'"
                :style="calloutStyle(entry.block)"
              >
                <div class="callout-in">
                  <div class="callout-head">
                    <span class="callout-icon block-type-icon" aria-hidden="true">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                        <path v-for="(path, pathIndex) in styleIconPaths(entry.block.style)" :key="pathIndex" :d="path" />
                      </svg>
                    </span>
                    <div>
                      <small>{{ styleKind(entry.block.style) }}</small>
                      <b>{{ entry.block.title || styleTitle(entry.block.style) }}</b>
                    </div>
                  </div>
                  <p
  class="math-content"
  v-html="rich(blockDisplayText(entry, entry.block.text))"
></p>
                </div>
              </div>

<div v-else-if="entry.block.type === 'formula'" class="formula math-content">
  <small>گنجینهٔ فرمول</small>
  <div>{{ blockDisplayText(entry, entry.block.text) }}</div>
</div>
              <blockquote v-else-if="entry.block.type === 'quote'" class="quote">
                {{ blockDisplayText(entry, entry.block.text) }}
              </blockquote>

              <div v-else-if="entry.block.type === 'divider'" class="rune">
                <i></i><span class="divider-mark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m12 3 2.4 6.6L21 12l-6.6 2.4L12 21l-2.4-6.6L3 12l6.6-2.4L12 3Z"/></svg></span><i></i>
              </div>

              <div
                v-else-if="entry.block.type === 'flashcard'"
                class="flash"
                :class="{ on: flipped.has(entry.index) }"
                @click="flip(entry.index)"
                tabindex="0"
                role="button"
                :aria-label="flipped.has(entry.index) ? 'نمایش روی فلش‌کارت' : 'نمایش پاسخ فلش‌کارت'"
                @keydown.enter.prevent="flip(entry.index)"
                @keydown.space.prevent="flip(entry.index)"
              >
                <div class="flash-in">
                  <div class="face">
                    <small>فلش‌کارت · فکر کن، بعد بزن</small>
                    <b>{{ blockDisplayText(entry, entry.block.front) }}</b>
                  </div>
                  <div class="face back">
                    <small>پاسخ</small>
                    <b>{{ entry.block.back }}</b>
                  </div>
                </div>
              </div>

              <div v-else-if="entry.block.type === 'quiz'" class="boss">
                <div class="boss-head">
                  <span class="boss-icon block-type-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                      <path v-for="(path, pathIndex) in blockIconPaths(entry.block)" :key="pathIndex" :d="path" />
                    </svg>
                  </span>
                  <div>
                    <small>چالش دانشی</small>
                    <b>مینی‌باس</b>
                  </div>
                  <em v-if="quizTries[entry.index]">
                    {{ quizTries[entry.index] }} تلاش
                  </em>
                </div>

                <h3>{{ blockDisplayText(entry, entry.block.question || 'پاسخ درست را انتخاب کن') }}</h3>

                <div class="opts">
                  <button
                    v-for="(option, i) in (entry.block.options || [])"
                    :key="i"
                    type="button"
                    class="opt"
                    :disabled="quizSolved(entry)"
                    :class="{
                      correct: quizAnswers[entry.index] === i && i === Number(entry.block.answer),
                      wrong: quizAnswers[entry.index] === i && i !== Number(entry.block.answer),
                      reveal: quizSolved(entry) && i === Number(entry.block.answer)
                    }"
                    @click="answerQuiz(entry, i)"
                  >
                    <span class="letter">{{ letters[i] || (i + 1) }}</span>
                    <span class="txt">{{ option }}</span>
                    <span class="res" aria-hidden="true">
                      <svg v-if="quizAnswers[entry.index] === i && i === Number(entry.block.answer)" viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/></svg>
                      <svg v-else-if="quizAnswers[entry.index] === i && i !== Number(entry.block.answer)" viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></svg>
                    </span>
                  </button>
                </div>

                <Transition name="fade">
                  <div
                    v-if="quizAnswers[entry.index] !== undefined"
                    class="feedback"
                    :class="{ ok: quizSolved(entry) }"
                    aria-live="polite"
                  >
                    <b>
                      {{
                        quizSolved(entry)
                          ? 'آفرین! پاسخ درست بود.'
                          : 'این گزینه درست نیست؛ دوباره فکر کن.'
                      }}
                    </b>
                    <p
                      v-if="quizSolved(entry) && entry.block.explanation"
                      v-html="rich(entry.block.explanation)"
                    ></p>
                  </div>
                </Transition>
              </div>

              <figure v-else-if="entry.block.type === 'image'" class="img">
                <img
                  v-if="entry.block.url"
                  :src="entry.block.url"
                  :alt="entry.block.caption || 'تصویر آموزشی'"
                  loading="lazy"
                  @error="hideBroken"
                />
                <figcaption v-if="entry.block.caption">{{ entry.block.caption }}</figcaption>
                <div v-if="!entry.block.url" class="img-ph"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9" r="1.5"/><path d="m4 17 5-5 3 3 3-4 5 6"/></svg><span>تصویر آموزشی</span></div>
              </figure>

              <div v-else-if="entry.block.type === 'checklist'" class="checklist">
                <label
                  v-for="(item, i) in listItems(entry.block)"
                  :key="i"
                  :class="{ on: checks[`${entry.index}-${i}`] }"
                >
                  <input
                    v-model="checks[`${entry.index}-${i}`]"
                    type="checkbox"
                    @change="onCheck(entry)"
                  />
                  <span class="box"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg></span>
                  <span>{{ item }}</span>
                </label>
              </div>

              <div v-else class="unknown">
                <b>{{ entry.block.title || 'بخش آموزشی' }}</b>
                <p>{{ entry.block.text }}</p>
              </div>
            </div>
            <div v-else class="block-teaser" aria-label="محتوای این بلوک هنوز نمایش داده نشده">
              <span class="teaser-orbit"><i></i><i></i><i></i></span>
              <b class="teaser-title"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2L12 3Z"/><path d="m19 2 .7 2.3L22 5l-2.3.7L19 8l-.7-2.3L16 5l2.3-.7L19 2Z"/></svg> آمادهٔ کشف</b>
              <span>برای دیدن محتوا به این بلوک برو</span>
            </div>


          </article>
        </TransitionGroup>

        <div v-if="!activeStage.blocks.length" class="empty">
          <h3>این مرحله هنوز خالی است</h3>
          <p>از نقشه یک مرحلهٔ دیگر انتخاب کن.</p>
        </div>

        <div class="stage-end" :class="{ won: isStageDone(activeStage) }" data-stage-end>
          <div class="finish-emblem" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 4h8v4.5a4 4 0 0 1-8 0V4Z"/><path d="M8 6H4v2a4 4 0 0 0 4 4M16 6h4v2a4 4 0 0 1-4 4M12 12.5V17m-4 3h8m-6-3h4"/></svg></div>
          <div class="finish-text">
            <b>{{ isStageDone(activeStage) ? 'این مرحله کامل شد!' : 'پایان این مرحله' }}</b>
            <p>{{ isStageDone(activeStage) ? 'پیشرفتت ذخیره شد؛ مسیر یادگیری ادامه دارد.' : 'پس از مرور محتوا، برای ثبت این مرحله و ادامهٔ مسیر از دکمهٔ زیر استفاده کن.' }}</p>
          </div>
          <div class="stage-actions">
            <button class="btn primary stage-next-btn" type="button" @click="completeAndNextStage">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13m-5-5 5 5-5 5"/></svg>
              {{ activeStageIndex < stages.length - 1 ? 'تکمیل مرحله و رفتن به بعدی' : (isStageDone(activeStage) ? 'پایان مسیر یادگیری' : 'تکمیل و پایان مطالعه') }}
            </button>
            <span class="stage-action-hint">پیشرفت این مرحله با فشردن دکمه ثبت می‌شود.</span>
          </div>
        </div>
      </section>

      <div v-if="!stages.length" class="empty empty-page">
        <h2>هنوز محتوایی برای نمایش وجود ندارد</h2>
        <p>این جزوه هنوز بلوک آموزشی ندارد.</p>
        <RouterLink to="/notes" class="btn primary">بازگشت به کتابخانه</RouterLink>
      </div>
    </main>

    <Transition name="reward">
      <div v-if="rewardToast" class="reward" role="status" aria-live="polite">
        <span class="reward-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m12 3 2.7 6 6.1 3-6.1 3-2.7 6-2.7-6-6.1-3 6.1-3L12 3Z"/></svg></span>
        <b>{{ rewardToast }}</b>
      </div>
    </Transition>

    <footer class="foot">یاد بگیر · سطح بگیر · تکرار کن</footer>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { notesApi } from '../services/notes'
import renderMathInElement from 'katex/contrib/auto-render'
import 'katex/dist/katex.min.css'
const route = useRoute()
const auth = useAuthStore()

const noteId = computed(() => route.params.id)
const isAdmin = computed(() => Boolean(auth.user?.is_staff || auth.user?.is_superuser))

const note = ref({ blocks: [] })
const loading = ref(true)
const error = ref('')
const isDark = ref(true)

const bookmarked = ref(false)
const bookmarkBusy = ref(false)
const completed = ref([])
const currentBlock = ref(0)
const activeStageIndex = ref(0)
const quizAnswers = ref({})
const quizTries = reactive({})
const checks = ref({})
const flipped = reactive(new Set())
const rewardToast = ref('')
const confetti = ref([])
const typedStageTitle = ref('')
const typedStageDescription = ref('')
const revealedBlocks = ref(new Set())
const typingBlockIndex = ref(null)
const typedBlockText = ref('')

let toastTimer = null
let confettiTimer = null
let themeObserver = null
let systemThemeQuery = null
let stageObserver = null
let blockObserver = null
let scrollIdleTimer = null
let scrollRaf = null
let lastScrollY = 0
let scrollDirection = 0
let programmaticScrollUntil = 0
let navigationLockTimer = null
let navigationTargetIndex = null
let lastProgressSaveTimer = null
let typingTimer = null
let blockTypingTimer = null
let centerScrollTimer = null
let autoAdvanceTimer = null
let autoAdvanceBusy = false
let ready = false

const letters = ['A', 'B', 'C', 'D', 'E', 'F']




async function renderNoteMath() {
  await nextTick()

  const root = document.querySelector('.quest')
  if (!root) return

  root.querySelectorAll('.math-content').forEach((el) => {
    // جلوگیری از رندر مجدد روی HTML قبلاً پردازش‌شده
    if (el.dataset.mathRendered === 'true') return

    renderMathInElement(el, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
      ],
      throwOnError: false,
      trust: false,
      ignoredClasses: ['katex'],
    })

    el.dataset.mathRendered = 'true'
  })
}


/* ---------------- Theme ---------------- */

function detectDarkTheme() {
  const root = document.documentElement
  const body = document.body

  const dataTheme =
    root.getAttribute('data-theme') ||
    body?.getAttribute('data-theme')

  if (dataTheme === 'dark') return true
  if (dataTheme === 'light') return false

  if (
    root.classList.contains('dark') ||
    body?.classList.contains('dark') ||
    root.classList.contains('dark-mode') ||
    body?.classList.contains('dark-mode')
  ) return true

  if (
    root.classList.contains('light') ||
    body?.classList.contains('light') ||
    root.classList.contains('light-mode') ||
    body?.classList.contains('light-mode')
  ) return false

  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function syncTheme() {
  isDark.value = detectDarkTheme()
}

function initThemeWatcher() {
  syncTheme()

  themeObserver?.disconnect()
  themeObserver = new MutationObserver(syncTheme)

  const config = {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style']
  }

  themeObserver.observe(document.documentElement, config)

  if (document.body) {
    themeObserver.observe(document.body, config)
  }

  systemThemeQuery = window.matchMedia('(prefers-color-scheme: dark)')
  systemThemeQuery.addEventListener?.('change', syncTheme)
}

/* ---------------- Derived data ---------------- */

const safeCoverColor = computed(() =>
  /^#[0-9a-f]{6}$/i.test(note.value.cover_color || '')
    ? note.value.cover_color
    : '#7055e8'
)

const allBlocks = computed(() =>
  Array.isArray(note.value.blocks) ? note.value.blocks : []
)

const stages = computed(() => {
  const blocks = allBlocks.value.map((block, index) => ({
    block: block || {},
    index
  }))

  if (!blocks.length) return []

  const groups = []

  if (blocks.some(entry => entry.block.type === 'heading')) {
    let current = null

    for (const entry of blocks) {
      if (entry.block.type === 'heading') {
        current = {
          id: `s-${entry.index}`,
          title: String(
            entry.block.text ||
            entry.block.title ||
            `مرحلهٔ ${groups.length + 1}`
          ).trim(),
          description: 'این بخش را بخوان و نکته‌های مهمش را به خاطر بسپار.',
          blocks: []
        }
        groups.push(current)
      } else if (!current) {
        current = {
          id: 's-intro',
          title: 'شروع ماجراجویی',
          description: 'پیش‌درآمد مسیر یادگیری.',
          blocks: []
        }
        groups.push(current)
      }

      current.blocks.push(entry)
    }

    return groups
  }

  for (let i = 0; i < blocks.length; i += 4) {
    groups.push({
      id: `s-${i}`,
      title: i === 0 ? 'شروع ماجراجویی' : `مرحلهٔ ${groups.length + 1}`,
      description: 'چند قدم کوچک برای پیشروی.',
      blocks: blocks.slice(i, i + 4)
    })
  }

  return groups
})

const activeStage = computed(() => stages.value[activeStageIndex.value] || null)
const nextStage = computed(() => stages.value.find(stage => !isStageDone(stage)) || null)
const totalBlocks = computed(() => allBlocks.value.length)

const completedCount = computed(() =>
  new Set(
    completed.value.filter(
      index => Number.isInteger(index) && index >= 0 && index < totalBlocks.value
    )
  ).size
)

const progressPercent = computed(() =>
  totalBlocks.value
    ? Math.round(completedCount.value / totalBlocks.value * 100)
    : 0
)

const completedStages = computed(() =>
  stages.value.filter(stage => isStageDone(stage)).length
)

/* ---------------- Helpers ---------------- */

const esc = value =>
  String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')

const rich = value =>
  esc(value)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/==(.+?)==/g, '<mark>$1</mark>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')

const isCompleted = index => completed.value.includes(index)
const isBlockRevealed = index => revealedBlocks.value.has(index)
const blockPosition = entry => activeStage.value?.blocks?.findIndex(item => item.index === entry.index) ?? 0

function canAutoComplete(entry) {
  if (!entry) return false
  if (entry.block.type === 'quiz') return quizSolved(entry)
  if (entry.block.type === 'checklist') {
    const items = listItems(entry.block)
    return items.length > 0 && items.every((_, index) => Boolean(checks.value[`${entry.index}-${index}`]))
  }
  if (entry.block.type === 'flashcard') return flipped.has(entry.index)
  return true
}

const blockLabel = type => ({
  heading: 'عنوان و شروع مبحث',
  paragraph: 'مطالعهٔ متن',
  list: 'مرور نکته‌ها',
  callout: 'نکتهٔ ویژه',
  formula: 'فرمول آموزشی',
  quote: 'جملهٔ کلیدی',
  divider: 'تغییر بخش',
  flashcard: 'فلش‌کارت',
  quiz: 'آزمون کوتاه',
  image: 'تصویر آموزشی',
  checklist: 'چک‌لیست مرور'
}[type] || 'بخش آموزشی')

const blockIconName = block => {
  if (block?.type === 'callout') return `callout-${block.style || 'tip'}`
  return ({
    heading: 'heading', paragraph: 'paragraph', list: 'list', formula: 'formula',
    quote: 'quote', divider: 'divider', flashcard: 'flashcard', quiz: 'quiz',
    image: 'image', checklist: 'checklist'
  }[block?.type] || 'default')
}

// مجموعه مسیرهای SVG با سبک خطی یکپارچه؛ بدون فونت آیکون یا وابستگی خارجی.
const blockIconPaths = block => {
  if (block?.type === 'callout') return styleIconPaths(block.style)
  const icons = {
    heading: ['M4 6h16', 'M4 12h10', 'M4 18h16'],
    paragraph: ['M5 5h14', 'M5 9h14', 'M5 13h10', 'M5 17h12'],
    list: ['M9 6h11', 'M9 12h11', 'M9 18h11', 'M4 6h.01', 'M4 12h.01', 'M4 18h.01'],
    formula: ['M7 4 17 20', 'M17 4 7 20', 'M4 9h16', 'M4 15h16'],
    quote: ['M4 6h16v12H8l-4 3V6Z', 'M8 10h.01', 'M12 10h.01', 'M16 10h.01'],
    divider: ['M4 12h5', 'M15 12h5', 'm12 4 3 8-3 8-3-8 3-8Z'],
    flashcard: ['M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z', 'M4 6h13', 'M8 8v8'],
    quiz: ['M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2.5-3 4', 'M12 17.5h.01', 'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z'],
    image: ['M4 4h16v16H4z', 'M8.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z', 'm4 16 5-5 3 3 3-4 5 6'],
    checklist: ['m4 6 1.5 1.5L8 5', 'M11 6h9', 'm4 12 1.5 1.5L8 11', 'M11 12h9', 'm4 18 1.5 1.5L8 17', 'M11 18h9'],
    default: ['M12 3 14.5 9.5 21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z']
  }
  return icons[block?.type] || icons.default
}

const styleIconPaths = style => {
  const icons = {
    tip: ['M9 18h6', 'M10 22h4', 'M8.2 14.5a6 6 0 1 1 7.6 0c-.8.6-1.3 1.5-1.5 2.5h-4.6c-.2-1-.7-1.9-1.5-2.5Z', 'M12 2v2'],
    definition: ['M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z', 'M4 6h12', 'M8 9h8', 'M8 12h6'],
    warning: ['M10.3 3.9 2.7 17a2 2 0 0 0 1.7 3h15.2a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z', 'M12 9v4', 'M12 16.5h.01'],
    trap: ['M12 3 20 7v5c0 5-3.4 7.8-8 9-4.6-1.2-8-4-8-9V7l8-4Z', 'm9 12 2 2 4-4'],
    example: ['M12 3 14.5 9.5 21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z', 'M19 2v4', 'M17 4h4'],
    summary: ['M5 5h14', 'M5 10h14', 'M5 15h9', 'm16 18 2 2 4-4'],
    exam: ['M12 3 14.7 9.3 21 12l-6.3 2.7L12 21l-2.7-6.3L3 12l6.3-2.7L12 3Z', 'M12 8v4l2.5 1.5'],
    custom: ['M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z', 'M12 10h.01'],
  }
  return icons[style] || icons.tip
}

const blockToneClass = block => {
  if (block?.type === 'callout') return `tone-${block.style || 'tip'}`
  return `tone-${block?.type || 'default'}`
}

const isStageDone = stage =>
  Boolean(stage?.blocks?.length) &&
  stage.blocks.every(entry => isCompleted(entry.index))

const stagePercent = stage =>
  stage?.blocks?.length
    ? Math.round(
        stage.blocks.filter(entry => isCompleted(entry.index)).length /
        stage.blocks.length * 100
      )
    : 0

function listItems(block) {
  if (Array.isArray(block.items)) {
    return block.items.map(String).filter(item => item.trim())
  }

  return String(block.text || '')
    .split('\n')
    .map(item => item.trim())
    .filter(Boolean)
}

const styleIcon = () => 'sparkles'

const styleTitle = style => ({
  tip: 'نکتهٔ مهم',
  definition: 'تعریف',
  warning: 'هشدار',
  trap: 'دام تستی',
  example: 'مثال',
  summary: 'خلاصه',
  exam: 'نکتهٔ امتحانی',
  custom: 'توجه'
}[style] || 'توجه')

const styleKind = style => ({
  warning: 'هشدار',
  trap: 'دام تستی',
  definition: 'تعریف',
  example: 'مثال',
  summary: 'جمع‌بندی',
  exam: 'نکتهٔ امتحانی'
}[style] || 'نکتهٔ ویژه')

const calloutStyle = block =>
  block.customColor &&
  block.style === 'custom' &&
  /^#[0-9a-f]{6}$/i.test(block.customColor)
    ? { '--c': block.customColor }
    : {}

function hideBroken(event) {
  if (event?.target) event.target.style.display = 'none'
}

function flip(id) {
  if (flipped.has(id)) {
    flipped.delete(id)
    return
  }

  flipped.add(id)
  if (!isCompleted(id)) {
    setCompleted(id, true)
    persistProgress()
    showReward('فلش‌کارت مرور شد')
  }

}

function printNote() {
  window.print()
}

function showReward(message) {
  rewardToast.value = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    rewardToast.value = ''
  }, 2600)
}

function burst() {
  const colors = ['#5be7ff', '#8f7bff', '#ffcf5a', '#ff5c82', '#4df0c0', '#ffffff']

  confetti.value = Array.from({ length: 46 }, (_, index) => ({
    id: `${Date.now()}-${index}`,
    x: Math.random() * 100,
    d: +(Math.random() * 0.5).toFixed(2),
    t: +(1.5 + Math.random() * 1.2).toFixed(2),
    r: Math.round(Math.random() * 360),
    c: colors[index % colors.length],
    s: 5 + Math.round(Math.random() * 6)
  }))

  clearTimeout(confettiTimer)
  confettiTimer = setTimeout(() => {
    confetti.value = []
  }, 3200)
}

/* ---------------- Progress actions ---------------- */

function startTypewriter(stage) {
  clearInterval(typingTimer)
  typedStageTitle.value = ''
  typedStageDescription.value = ''
  if (!stage) return

  const titleChars = Array.from(String(stage.title || ''))
  const descriptionChars = Array.from(String(stage.description || ''))
  let titleIndex = 0
  let descriptionIndex = 0

  // عنوان با افکت تایپ ظاهر می‌شود؛ سپس توضیح مرحله نوشته می‌شود.
  typingTimer = setInterval(() => {
    if (titleIndex < titleChars.length) {
      typedStageTitle.value += titleChars[titleIndex++]
      return
    }
    if (descriptionIndex < descriptionChars.length) {
      typedStageDescription.value += descriptionChars[descriptionIndex++]
      return
    }
    clearInterval(typingTimer)
    typingTimer = null
  }, 28)
}

function primaryBlockText(entry) {
  const block = entry?.block || {}
  switch (block.type) {
    case 'heading': return String(block.text || block.title || '')
    case 'paragraph': return String(block.text || '')
    case 'callout': return String(block.text || '')
    case 'formula': return String(block.text || '')
    case 'quote': return String(block.text || '')
    case 'quiz': return String(block.question || 'پاسخ درست را انتخاب کن')
    case 'flashcard': return String(block.front || '')
    default: return String(block.text || block.title || '')
  }
}

function blockDisplayText(entry, value) {
  // Keep the full text in the layout. A character-by-character DOM update changes
  // card heights while scrolling and was a major source of block-selection jitter.
  return value
}

function startBlockTypewriter(entry) {
  // Content uses a visual reveal animation instead of changing its height one
  // character at a time. This keeps scroll geometry stable and navigation reliable.
  clearInterval(blockTypingTimer)
  blockTypingTimer = null
  typingBlockIndex.value = null
  typedBlockText.value = ''
}

function handleViewportNavigation(event) {
  // فقط کلیک در ناحیهٔ مطالعه پیمایش می‌کند؛ کنترل‌های تست، فرم‌ها و لینک‌ها دست‌نخورده می‌مانند.
  if (!ready || !activeStage.value || !event.target?.closest?.('.study')) return
  if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return
  if (window.getSelection?.()?.toString()) return
  if (event.target.closest('button, a, input, textarea, select, option, [role="button"], label, .flash, .opts, .checklist')) return

  const y = event.clientY
  const third = window.innerHeight / 3
  let direction = 0
  if (y < third) direction = -1
  else if (y >= third * 2) direction = 1
  if (!direction) return

  const blocks = activeStage.value.blocks || []
  const position = blocks.findIndex(item => item.index === currentBlock.value)
  const entry = blocks[position]
  if (!entry || !blocks[position + direction]) return

  navigateBlock(entry, direction)
}

function releaseNavigationScrollLock() {
  if (navigationTargetIndex === null || navigationTargetIndex === undefined) return
  clearTimeout(navigationLockTimer)
  navigationLockTimer = setTimeout(() => {
    programmaticScrollUntil = 0
    navigationTargetIndex = null
    lastScrollY = window.scrollY
  }, 120)
}

function navigateBlock(entry, direction) {
  const blocks = activeStage.value?.blocks || []
  const position = blocks.findIndex(item => item.index === entry?.index)
  const target = blocks[position + direction]
  if (!target) return

  clearTimeout(centerScrollTimer)
  clearTimeout(scrollIdleTimer)
  if (scrollRaf !== null) {
    cancelAnimationFrame(scrollRaf)
    scrollRaf = null
  }

  navigationTargetIndex = target.index
  currentBlock.value = target.index
  revealedBlocks.value = new Set([...revealedBlocks.value, target.index])
  startBlockTypewriter(target)

  // Lock the target while smooth scrolling. The lock is released by scrollend
  // when supported, with a conservative timeout as a fallback.
  programmaticScrollUntil = Date.now() + 1800
  clearTimeout(navigationLockTimer)
  navigationLockTimer = setTimeout(() => {
    programmaticScrollUntil = 0
    navigationTargetIndex = null
    lastScrollY = window.scrollY
  }, 1900)

  nextTick(() => {
    const card = document.getElementById(`blk-${target.index}`)
    if (!card) return
    card.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' })
    persistProgress()
  })
}

function stopBlockObserver() {
  blockObserver?.disconnect()
  blockObserver = null
  clearTimeout(scrollIdleTimer)
  if (scrollRaf !== null) {
    cancelAnimationFrame(scrollRaf)
    scrollRaf = null
  }
}

// Scroll-driven selection uses a fixed activation line and only advances to
// adjacent cards in the user's scroll direction. It never initiates scrolling.
// This avoids the feedback loop between observers, smooth scrolling and layout shifts.
function observeContentBlocks() {
  stopBlockObserver()
  if (!ready || !activeStage.value) return
  lastScrollY = window.scrollY
  scrollDirection = 0
}

function handleStudyScroll() {
  if (!ready || !activeStage.value) return

  // Listen to the actual viewport geometry, not a cached scrollTop. This works
  // whether the page scrolls on window or inside an app/layout scroll container.
  if (scrollRaf !== null) return
  scrollRaf = requestAnimationFrame(() => {
    scrollRaf = null
    updateCurrentBlockFromScroll()
  })
}

function updateCurrentBlockFromScroll() {
  if (!ready || !activeStage.value) return

  const stageBlocks = activeStage.value.blocks || []
  if (!stageBlocks.length) return

  const cards = stageBlocks
    .map(entry => ({
      entry,
      element: document.getElementById(`blk-${entry.index}`)
    }))
    .filter(item => item.element && item.element.isConnected)

  if (!cards.length) return

  // The activation line is fixed to the visible viewport. A block becomes
  // active when it reaches this line, regardless of which element scrolls.
  const activationLine = Math.min(window.innerHeight * 0.48, window.innerHeight - 80)
  const currentItem = cards.find(item => item.entry.index === currentBlock.value)
  const distanceToLine = (element) => {
    const rect = element.getBoundingClientRect()
    if (rect.top <= activationLine && rect.bottom >= activationLine) return 0
    return Math.min(Math.abs(rect.top - activationLine), Math.abs(rect.bottom - activationLine))
  }

  let candidate = cards[0]
  let candidateDistance = distanceToLine(candidate.element)
  for (let i = 1; i < cards.length; i += 1) {
    const distance = distanceToLine(cards[i].element)
    if (distance < candidateDistance) {
      candidate = cards[i]
      candidateDistance = distance
    }
  }

  if (!currentItem) {
    activateScrolledBlock(candidate.entry)
    return
  }

  const currentDistance = distanceToLine(currentItem.element)
  const hysteresis = Math.max(18, Math.min(42, window.innerHeight * 0.035))

  // A block containing the activation line always wins. In the gaps between
  // cards, hysteresis keeps the active block stable instead of flickering.
  if (candidate.entry.index !== currentBlock.value && (
    candidateDistance === 0 || candidateDistance + hysteresis < currentDistance
  )) {
    activateScrolledBlock(candidate.entry)
  }
}

function activateScrolledBlock(entry) {
  if (!entry || currentBlock.value === entry.index) return
  currentBlock.value = entry.index
  revealedBlocks.value = new Set([...revealedBlocks.value, entry.index])
  // CSS animates the card/content. Do not mutate the text during scroll; that
  // would change the card height and make the scroll position unstable.
  queueProgressSave()
}

function queueProgressSave() {
  clearTimeout(lastProgressSaveTimer)
  lastProgressSaveTimer = setTimeout(() => {
    persistProgress()
  }, 450)
}

function stopStageObserver() {
  stageObserver?.disconnect()
  stageObserver = null
}

function observeStageEnd() {
  // مرحله بعد فقط با دکمهٔ انتهای مرحله باز می‌شود.
  stopStageObserver()
}

function selectStage(index, scroll = true) {
  if (index < 0 || index >= stages.value.length) return
  clearTimeout(autoAdvanceTimer)
  autoAdvanceBusy = false
  stopStageObserver()

  activeStageIndex.value = index
  programmaticScrollUntil = Date.now() + (scroll ? 1500 : 250)
  navigationTargetIndex = null
  clearTimeout(navigationLockTimer)
  const selectedBlocks = stages.value[index]?.blocks || []
  const firstBlock = selectedBlocks[0]
  revealedBlocks.value = new Set([
    ...revealedBlocks.value,
    ...selectedBlocks.map(entry => entry.index)
  ])
  if (firstBlock) currentBlock.value = firstBlock.index

  persistProgress()
  nextTick(() => {
    startTypewriter(activeStage.value)
    if (firstBlock) startBlockTypewriter(firstBlock)
    if (scroll) {
      document.querySelector('.study')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      })
    }
    observeContentBlocks()
    observeStageEnd()
    lastScrollY = window.scrollY
  })
}

async function goNextStage() {
  const stage = activeStage.value
  if (!stage) return
  completed.value = [...new Set([...completed.value, ...stage.blocks.map(entry => entry.index)])].sort((a, b) => a - b)
  await persistProgress()
  if (activeStageIndex.value < stages.value.length - 1) selectStage(activeStageIndex.value + 1)
}

async function completeAndNextStage() {
  const stage = activeStage.value
  if (!stage) return

  const ids = stage.blocks.map(entry => entry.index)
  completed.value = [...new Set([...completed.value, ...ids])].sort((a, b) => a - b)
  await persistProgress()
  burst()

  if (activeStageIndex.value < stages.value.length - 1) {
    showReward('مرحله ثبت شد؛ بریم سراغ مرحلهٔ بعد!')
    selectStage(activeStageIndex.value + 1)
  } else {
    showReward('مسیر یادگیری کامل شد!')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function continueQuest() {
  const index = stages.value.findIndex(stage => !isStageDone(stage))
  selectStage(index === -1 ? 0 : index)
}

function setCompleted(index, shouldComplete) {
  const has = isCompleted(index)

  if (shouldComplete && !has) {
    completed.value = [...completed.value, index].sort((a, b) => a - b)
  } else if (!shouldComplete && has) {
    completed.value = completed.value.filter(item => item !== index)
  }
}

function afterStageChange(wasDone) {
  if (!wasDone && isStageDone(activeStage.value)) {
    burst()
    showReward('مرحله با موفقیت تکمیل شد!')
  }
}

function toggleCompleted(index) {
  const wasDone = isStageDone(activeStage.value)
  const shouldComplete = !isCompleted(index)

  setCompleted(index, shouldComplete)
  currentBlock.value = index

  if (shouldComplete) {
    showReward('بخش تکمیل شد.')
    afterStageChange(wasDone)
  }

  persistProgress()
}

function completeStage() {
  const stage = activeStage.value
  if (!stage) return

  const ids = stage.blocks.map(entry => entry.index)

  if (isStageDone(stage)) {
    completed.value = completed.value.filter(index => !ids.includes(index))
    showReward('تکمیل مرحله لغو شد.')
  } else {
    completed.value = [...new Set([...completed.value, ...ids])].sort((a, b) => a - b)
    burst()
    showReward('مرحله با موفقیت تکمیل شد!')
  }

  persistProgress()
}

/* ---------------- Quiz and checklist ---------------- */

const quizSolved = entry =>
  quizAnswers.value[entry.index] !== undefined &&
  quizAnswers.value[entry.index] === Number(entry.block.answer)

function answerQuiz(entry, choice) {
  if (quizSolved(entry)) return

  quizAnswers.value = {
    ...quizAnswers.value,
    [entry.index]: choice
  }

  quizTries[entry.index] = (quizTries[entry.index] || 0) + 1

  if (choice === Number(entry.block.answer)) {
    const wasDone = isStageDone(activeStage.value)

    if (!isCompleted(entry.index)) {
      setCompleted(entry.index, true)
      persistProgress()
    }

    showReward(quizTries[entry.index] === 1 ? 'پاسخ درست بود!' : 'درست شد!')
    afterStageChange(wasDone)
    return
  }

  // پاسخ اشتباه پس از نمایش کوتاه باز می‌شود تا امکان تلاش مجدد باشد.
  setTimeout(() => {
    if (quizAnswers.value[entry.index] === choice && !quizSolved(entry)) {
      const { [entry.index]: removed, ...rest } = quizAnswers.value
      quizAnswers.value = rest
    }
  }, 1100)
}

function onCheck(entry) {
  const items = listItems(entry.block)
  if (!items.length) return

  const allChecked = items.every((_, index) =>
    Boolean(checks.value[`${entry.index}-${index}`])
  )

  const wasDone = isStageDone(activeStage.value)

  if (allChecked && !isCompleted(entry.index)) {
    setCompleted(entry.index, true)
    showReward('چک‌لیست کامل شد!')
    persistProgress()
    afterStageChange(wasDone)
  } else if (!allChecked && isCompleted(entry.index)) {
    setCompleted(entry.index, false)
    persistProgress()
  }
}

/* ---------------- API persistence ---------------- */

async function persistProgress() {
  if (!auth.isAuthenticated || !note.value.id) return

  try {
    await notesApi.saveProgress(note.value.id, {
      completed_blocks: completed.value,
      last_block: currentBlock.value,
      percent: progressPercent.value
    })
  } catch (err) {
    console.warn('Progress save failed', err)
  }
}

async function load() {
  loading.value = true
  error.value = ''
  ready = false

  completed.value = []
  revealedBlocks.value = new Set()
  typingBlockIndex.value = null
  typedBlockText.value = ''
  currentBlock.value = 0
  activeStageIndex.value = 0
  quizAnswers.value = {}
  Object.keys(quizTries).forEach(key => delete quizTries[key])
  checks.value = {}
  flipped.clear()

  try {
    const response = await notesApi.get(noteId.value)
    note.value = response.data || { blocks: [] }
    bookmarked.value = Boolean(note.value.is_bookmarked)

    if (auth.isAuthenticated) {
      try {
        const progressResponse = await notesApi.getProgress(noteId.value)
        const progress = progressResponse.data || {}
        const length = allBlocks.value.length

        completed.value = [
          ...new Set(
            (Array.isArray(progress.completed_blocks) ? progress.completed_blocks : [])
              .filter(index =>
                Number.isInteger(index) &&
                index >= 0 &&
                index < length
              )
          )
        ].sort((a, b) => a - b)

        currentBlock.value = Math.min(
          Math.max(Number(progress.last_block) || 0, 0),
          Math.max(length - 1, 0)
        )
      } catch {
        // در صورت نبودن پیشرفت ذخیره‌شده، مطالعه همچنان امکان‌پذیر است.
      }
    }

    const stageIndex = stages.value.findIndex(stage =>
      stage.blocks.some(entry => entry.index === currentBlock.value)
    )

    activeStageIndex.value = stageIndex >= 0 ? stageIndex : 0
    // بلوک‌های تکمیل‌شده قبلی باقی می‌مانند؛ فقط اولین بلوکِ ناتمام به‌صورت اولیه باز می‌شود.
    revealedBlocks.value = new Set(completed.value)
    const selectedStage = stages.value[activeStageIndex.value]
    const firstUncompleted = selectedStage?.blocks?.find(entry => !isCompleted(entry.index))
    const initialEntry = firstUncompleted || selectedStage?.blocks?.[0]
    revealedBlocks.value = new Set([
      ...revealedBlocks.value,
      ...(selectedStage?.blocks || []).map(entry => entry.index)
    ])
    if (initialEntry) currentBlock.value = initialEntry.index
  } catch (err) {
    error.value =
      err.response?.data?.detail ||
      'جزوه پیدا نشد یا هنوز منتشر نشده است.'
  } finally {
    loading.value = false
    await nextTick()
    ready = true
    await nextTick()
    startTypewriter(activeStage.value)
    const initialEntry = activeStage.value?.blocks?.find(entry => entry.index === currentBlock.value)
    if (initialEntry) startBlockTypewriter(initialEntry)
    observeContentBlocks()
    observeStageEnd()
    lastScrollY = window.scrollY
  }
}

async function toggleBookmark() {
  if (bookmarkBusy.value || !note.value.id) return

  bookmarkBusy.value = true

  try {
    const response = await notesApi.bookmark(note.value.id)
    bookmarked.value = Boolean(response.data?.bookmarked)
    showReward(
      bookmarked.value
        ? 'به ذخیره‌شده‌ها اضافه شد.'
        : 'از ذخیره‌شده‌ها حذف شد.'
    )
  } catch {
    showReward('برای ذخیرهٔ جزوه باید وارد حساب شوی.')
  } finally {
    bookmarkBusy.value = false
  }
}

/* ---------------- Lifecycle ---------------- */

watch(noteId, () => {
  load()
})

watch(progressPercent, (newValue, oldValue) => {
  if (ready && newValue === 100 && oldValue < 100) {
    burst()
    showReward('مطالعهٔ جزوه را به پایان رساندی!')
  }
})

watch(
  () => [
    activeStageIndex,
    activeStage.value?.blocks?.map((entry) => [
      entry.index,
      isBlockRevealed(entry.index),
    ]),
  ],
  async () => {
    await nextTick()
    await renderNoteMath()
  },
  { deep: true, flush: 'post' }
)


onMounted(() => {
  initThemeWatcher()
  lastScrollY = window.scrollY
  // Capture catches scroll events from nested app containers as well as the page.
  document.addEventListener('scroll', handleStudyScroll, { passive: true, capture: true })
  window.addEventListener('scroll', handleStudyScroll, { passive: true })
  window.addEventListener('resize', handleStudyScroll, { passive: true })
  window.addEventListener('scrollend', releaseNavigationScrollLock, { passive: true })
  load()
})

onBeforeUnmount(() => {
  clearTimeout(toastTimer)
  clearTimeout(confettiTimer)
  clearTimeout(autoAdvanceTimer)
  clearTimeout(centerScrollTimer)
  clearTimeout(scrollIdleTimer)
  document.removeEventListener('scroll', handleStudyScroll, true)
  window.removeEventListener('scroll', handleStudyScroll)
  window.removeEventListener('resize', handleStudyScroll)
  window.removeEventListener('scrollend', releaseNavigationScrollLock)
  clearTimeout(navigationLockTimer)
  clearTimeout(lastProgressSaveTimer)
  if (scrollRaf !== null) cancelAnimationFrame(scrollRaf)
  clearInterval(typingTimer)
  clearInterval(blockTypingTimer)
  stopBlockObserver()
  stopStageObserver()
  themeObserver?.disconnect()
  systemThemeQuery?.removeEventListener?.('change', syncTheme)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap');

@property --ang {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
}
/* جهت صحیح فرمول‌های ریاضی در متن فارسی */
.math-content {
  direction: rtl;
}

.math-content :deep(.katex),
.math-content :deep(.katex *) {
  direction: ltr !important;
  unicode-bidi: isolate !important;
}

.math-content :deep(.katex-display) {
  direction: ltr !important;
  text-align: center !important;
  overflow-x: auto;
  overflow-y: hidden;
}

.quest {
  --bg: #070b1d;
  --card: #101a34;
  --card2: #172342;
  --line: #29385f;
  --txt: #eef3ff;
  --mut: #91a2cb;
  --cy: #5be7ff;
  --vi: #8f7bff;
  --am: #ffcf5a;
  --co: #ff5c82;
  --mi: #4df0c0;

  position: relative;
  min-height: 100vh;
  overflow-x: clip;
  isolation: isolate;
  color: var(--txt);
  background:
    radial-gradient(ellipse at 50% -10%, #223468 0, transparent 46%),
    var(--bg);
  font-family: 'Vazirmatn', Tahoma, sans-serif;
  transition: background-color .25s ease, color .25s ease;
}

button,
input {
  font-family: inherit;
}

.quest :focus-visible {
  outline: 2px solid var(--cy);
  outline-offset: 3px;
}

.bg-stars {
  position: absolute;
  inset: 0;
  z-index: -1;
  opacity: .22;
  pointer-events: none;
  background-image:
    radial-gradient(#8adfff 1px, transparent 1px),
    radial-gradient(#b7a0ff 1px, transparent 1px);
  background-size: 73px 73px, 131px 131px;
  background-position: 0 0, 31px 44px;
  animation: drift 100s linear infinite;
}

.aurora {
  position: absolute;
  z-index: -1;
  width: 480px;
  height: 480px;
  border-radius: 50%;
  filter: blur(110px);
  opacity: .15;
  pointer-events: none;
  animation: float 14s ease-in-out infinite alternate;
}

.a1 { background: #4b76ff; top: 260px; left: -220px; }
.a2 { background: #b04aff; top: 900px; right: -220px; animation-delay: -5s; }
.a3 { background: #00e0c0; top: 1500px; left: 30%; animation-delay: -9s; }

/* Header */
.topbar {
  position: sticky;
  top: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  gap: 16px;
  height: 68px;
  padding: 0 clamp(14px, 3.5vw, 56px);
  background: rgba(10, 18, 40, .86);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--line);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: inherit;
  text-decoration: none;
  margin-left: auto;
}

.gem {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  flex: 0 0 38px;
  border-radius: 13px;
  font-size: 22px;
  color: #0a1330;
  background: linear-gradient(145deg, #a6efff, #7a82ff);
  box-shadow: 0 0 24px #5ec3ff44;
  animation: bob 4s ease-in-out infinite;
}

.brand-copy b {
  display: block;
  font-size: 12px;
  letter-spacing: 1.5px;
}

.brand-copy small {
  color: var(--mut);
  font-size: 10px;
}

.top-actions {
  display: flex;
  gap: 8px;
}

.icon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  border: 1px solid #34466f;
  background: #17213e;
  color: #c9d7ff;
  font-size: 18px;
  cursor: pointer;
  text-decoration: none;
  transition: transform .22s, border-color .22s, color .22s, background .22s;
}

.icon:hover {
  transform: translateY(-2px);
  border-color: #7d91ff;
  color: #fff;
}

.icon:disabled {
  opacity: .5;
  cursor: not-allowed;
  transform: none;
}

.top-progress {
  position: absolute;
  inset: auto 0 -1px;
  height: 3px;
  background: transparent;
}

.top-progress i {
  display: block;
  height: 100%;
  margin-right: 0;
  margin-left: auto;
  background: linear-gradient(270deg, var(--cy), var(--vi), var(--am));
  box-shadow: 0 0 10px #5be7ff55;
  transition: width .5s ease;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
  white-space: normal;
  border: 1px solid transparent;
  transition: transform .2s, box-shadow .2s, filter .2s;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn.quiet {
  background: #172342;
  color: #c4d2f8;
  border-color: #3f527e;
}

.btn.primary {
  position: relative;
  overflow: hidden;
  color: #fff;
  border-color: #aaa5ff;
  background: linear-gradient(105deg, #5f7bff, #a06bff);
  box-shadow: 0 6px 22px #7770ff30;
}

.btn.primary::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(105deg, transparent 35%, #ffffff40 50%, transparent 65%);
  transform: translateX(120%);
  animation: shine 4.5s ease-in-out infinite;
}

/* Main layout */
.world {
  width: min(1100px, 100%);
  margin: auto;
  padding: 26px clamp(14px, 3vw, 40px) 30px;
  display: grid;
  gap: 22px;
}

/* Hero */
.hero {
  --cover: #7055e8;
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 24px;
  align-items: center;
  padding: 32px;
  border-radius: 28px;
  border: 1px solid #ffffff2a;
  background:
    radial-gradient(ellipse at 85% 0, #ffffff26, transparent 45%),
    linear-gradient(
      120deg,
      color-mix(in srgb, var(--cover) 60%, #0d1530),
      color-mix(in srgb, var(--cover) 22%, #101a3a) 75%
    );
  box-shadow: 0 30px 70px #0003, inset 0 1px #ffffff30;
  isolation: isolate;
}

.hero::before {
  content: '';
  position: absolute;
  z-index: -1;
  width: 520px;
  height: 520px;
  border: 1px solid #ffffff18;
  border-radius: 50%;
  left: -160px;
  bottom: -330px;
  pointer-events: none;
}

.hero-icon {
  width: 92px;
  height: 92px;
  display: grid;
  place-items: center;
  font-size: 46px;
  border-radius: 28px;
  background: linear-gradient(145deg, #ffffff48, #ffffff14);
  border: 1px solid #ffffff5a;
  box-shadow: 0 16px 38px #0004, inset 0 2px #ffffff80;
  backdrop-filter: blur(10px);
  animation: bob 5s ease-in-out infinite;
}

.meta {
  font-size: 12px;
  color: #d9e8ff;
  margin-bottom: 6px;
}

.hero h1 {
  margin: 0;
  font-size: clamp(24px, 3.2vw, 40px);
  line-height: 1.5;
  font-weight: 900;
  overflow-wrap: anywhere;
  text-shadow: 0 3px 20px #0004;
}

.hero-copy p {
  margin: 8px 0 0;
  font-size: 13px;
  line-height: 2;
  color: #d3e0fa;
  max-width: 60ch;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.chips span {
  padding: 6px 11px;
  border-radius: 10px;
  font-size: 11px;
  border: 1px solid #ffffff22;
  background: #07152e66;
}

.hero-card {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  border-radius: 18px;
  border: 1px solid #ffffff2e;
  background: #07152e8c;
  backdrop-filter: blur(12px);
}

.ring {
  --p: 0;
  width: 58px;
  height: 58px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background:
    radial-gradient(#0c1730 57%, transparent 59%),
    conic-gradient(var(--cy) calc(var(--p) * 1%), #ffffff1c 0);
  transition: background .5s ease;
}

.ring b { font-size: 12px; }

.hero-card-text {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hero-card-text small { font-size: 10px; color: var(--cy); }

.hero-card-text b {
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero-card-text span { font-size: 11px; color: #a8b9e0; }

/* Learning timeline */
.timeline-wrap {
  overflow: hidden;
  padding: 22px;
  border: 1px solid var(--line);
  border-radius: 24px;
  background: linear-gradient(145deg, #131e3eee, #0c1530ee);
  box-shadow: 0 12px 36px #00000012;
}

.timeline-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.timeline-heading h2 {
  margin: 3px 0 0;
  font-size: 20px;
  font-weight: 900;
}

.timeline-kicker {
  color: var(--cy);
  font-size: 9px;
  letter-spacing: 2px;
  font-weight: 800;
}

.timeline-count { color: var(--mut); font-size: 11px; }

.timeline {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 245px), 1fr));
  gap: 12px;
}

.timeline-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  width: 100%;
  min-height: 100px;
  padding: 15px;
  text-align: right;
  font: inherit;
  color: var(--txt);
  cursor: pointer;
  border: 1px solid #2b3b62;
  border-radius: 17px;
  background: linear-gradient(145deg, #172442, #101a32);
  transition: transform .22s, border-color .22s, background .22s, box-shadow .22s;
}

.timeline-item:hover {
  transform: translateY(-3px);
  border-color: #6478b5;
}

.timeline-index {
  display: grid;
  place-items: center;
  flex: 0 0 43px;
  width: 43px;
  height: 43px;
  border-radius: 13px;
  border: 1px solid #455783;
  color: #c8d6ff;
  background: linear-gradient(145deg, #2b3c67, #192544);
  font-size: 13px;
  font-weight: 900;
}

.timeline-copy {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.timeline-copy small { color: var(--cy); font-size: 10px; }

.timeline-copy strong {
  font-size: 13px;
  line-height: 1.8;
  overflow-wrap: anywhere;
}

.timeline-copy > span {
  color: var(--mut);
  font-size: 10px;
  line-height: 1.8;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.timeline-status {
  position: absolute;
  left: 13px;
  bottom: 10px;
  font-size: 9px;
  color: #8fa2cf;
}

.timeline-arrow {
  position: absolute;
  left: 12px;
  top: 12px;
  color: #7185b6;
  font-size: 15px;
  opacity: .75;
}

.timeline-item.active {
  border-color: #6cdeff;
  background: linear-gradient(145deg, #203b60, #20234d);
  box-shadow: 0 0 0 1px #5be7ff20, 0 10px 30px #0002;
}

.timeline-item.active .timeline-index {
  color: #fff;
  border-color: #8beaff;
  background: linear-gradient(145deg, #35bfe8, #7969f7);
  box-shadow: 0 0 20px #5be7ff25;
}

.timeline-item.active .timeline-status { color: var(--cy); }
.timeline-item.done { border-color: #357b78; }

.timeline-item.done .timeline-index {
  color: #06241f;
  border-color: #a2ffe6;
  background: linear-gradient(145deg, #8bffda, #39c5b5);
}

.timeline-item.done .timeline-status { color: #75e7c9; }

/* Study stage */
.study {
  display: grid;
  gap: 14px;
  scroll-margin-top: 84px;
}

.stage-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 6px 4px 0;
}

.stage-title small { font-size: 11px; color: var(--cy); }

.stage-title h2 {
  margin: 4px 0 5px;
  font-size: clamp(21px, 2.4vw, 28px);
  font-weight: 900;
  overflow-wrap: anywhere;
}

.stage-title p { margin: 0; font-size: 12px; color: var(--mut); }

.stage-medal {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  font-size: 28px;
  border-radius: 20px;
  border: 1px solid #4a5583;
  background: linear-gradient(145deg, #2b315d, #171d3b);
  transform: rotate(3deg);
  transition: .4s;
}

.stage-medal.won {
  border-color: #e4b85d;
  box-shadow: 0 0 26px #ffcb5533;
  animation: pop .6s cubic-bezier(.2, 1.6, .4, 1);
}

.stage-track {
  position: relative;
  height: 8px;
  border-radius: 9px;
  background: #060b1c;
  border: 1px solid #28385f;
  margin: 4px 0 6px;
}

.stage-track i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--cy), var(--vi), #c07aff);
  box-shadow: 0 0 14px #6d7cff66;
  transition: width .5s ease;
}

.stage-track span {
  position: absolute;
  top: 12px;
  left: 0;
  font-size: 10px;
  color: var(--mut);
}

/* پایان خودکار مرحله و افکت تایپ */
.typewriter-text { min-height: 1.55em; }
.typing-caret {
  display: inline-block;
  width: 2px;
  height: .95em;
  margin-right: 5px;
  vertical-align: -.08em;
  background: var(--cy);
  border-radius: 2px;
  animation: typingBlink .8s steps(2, start) infinite;
}
.stage-description { min-height: 1.8em; }
.stage-end {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  padding: 20px;
  margin-top: 8px;
  overflow: hidden;
  border: 1px solid #5666a0;
  border-radius: 22px;
  background: radial-gradient(circle at 8% 50%, #5be7ff18, transparent 36%), linear-gradient(135deg, #172342, #171b3b);
  box-shadow: 0 16px 42px #0002;
  animation: endReveal .65s cubic-bezier(.2,.8,.2,1) both;
}
.stage-end::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(110deg, transparent 25%, #ffffff08 48%, transparent 68%);
  transform: translateX(-100%);
  animation: endShimmer 2.8s ease-in-out infinite;
}
.stage-end.won { border-color: #47c8a6; }
.finish-emblem {
  display: grid;
  place-items: center;
  width: 52px;
  height: 52px;
  flex: 0 0 52px;
  border-radius: 17px;
  color: #fff;
  font-size: 24px;
  background: linear-gradient(140deg, var(--cy), var(--vi));
  box-shadow: 0 8px 24px #5be7ff20;
}
.finish-text { flex: 1 1 220px; min-width: 0; }
.finish-text b { display: block; font-size: 15px; font-weight: 900; }
.finish-text p { margin: 5px 0 0; color: var(--mut); font-size: 12px; line-height: 1.9; }
.auto-next-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border: 1px solid #5be7ff35;
  border-radius: 999px;
  color: var(--cy);
  background: #5be7ff0c;
  font-size: 11px;
  white-space: nowrap;
}
.auto-next-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #4df0c0;
  box-shadow: 0 0 0 0 #4df0c080;
  animation: nextPulse 1.5s infinite;
}
.completed-path { color: #ffcf5a; border-color: #ffcf5a35; }
@keyframes typingBlink { to { opacity: 0; } }
@keyframes endReveal { from { opacity: 0; transform: translateY(18px) scale(.985); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes endShimmer { 0%, 35% { transform: translateX(-100%); } 75%, 100% { transform: translateX(100%); } }
@keyframes nextPulse { 0% { box-shadow: 0 0 0 0 #4df0c080; } 70% { box-shadow: 0 0 0 7px #4df0c000; } 100% { box-shadow: 0 0 0 0 #4df0c000; } }
.quest.theme-light .stage-end { background: radial-gradient(circle at 8% 50%, #7055e818, transparent 36%), linear-gradient(135deg, #fff, #f3f2ff); border-color: #d7d9ee; }
.quest.theme-light .stage-end.won { border-color: #8bdcc8; }
@media (max-width: 620px) {
  .stage-end { align-items: flex-start; padding: 16px; gap: 12px; }
  .auto-next-indicator { margin-right: 0; }
}

/* Content cards */
.stack {
  display: grid;
  gap: 14px;
  margin-top: 12px;
}

.content-card {
  min-width: 0;
  padding: 19px;
  border: 1px solid #2c3c63;
  border-radius: 20px;
  background: linear-gradient(145deg, #172342f5, #101a34f8);
  box-shadow: 0 14px 34px #00000012;
  transition: border-color .3s, background .3s, box-shadow .3s;
}

.content-card.is-complete {
  border-color: #347d76a8;
}

.content-card:has(.c-heading:only-child) {
  padding-top: 8px;
  padding-bottom: 8px;
}

/* Sequential content journey: every block reveals as the learner scrolls */
.block-stepbar {
  display: flex;
  align-items: center;
  gap: 11px;
  margin-bottom: 16px;
  padding-bottom: 13px;
  border-bottom: 1px solid #8c9cc51b;
}
.block-step-icon {
  display: grid;
  place-items: center;
  flex: 0 0 38px;
  width: 38px;
  height: 38px;
  border: 1px solid #6175a74a;
  border-radius: 13px;
  color: #bdc9ed;
  background: linear-gradient(145deg, #27365c, #182341);
  font-size: 12px;
  font-weight: 900;
  transition: .35s ease;
}
.block-step-icon.current { color: #071827; border-color: #a6f5ff; background: linear-gradient(135deg, #78f0ff, #9c8aff); box-shadow: 0 0 22px #5be7ff25; }
.block-step-icon.done { color: #052a23; border-color: #a2ffe6; background: linear-gradient(135deg, #9dffe0, #45cdbb); }
.block-step-label { display: flex; flex: 1; min-width: 0; flex-direction: column; gap: 2px; }
.block-step-label small { color: var(--mut); font-size: 10px; }
.block-step-label b { color: var(--txt); font-size: 13px; font-weight: 900; }
.block-step-status { color: var(--mut); font-size: 10px; white-space: nowrap; }
.block-step-status.done { color: #5fe0bd; }
.content-card.is-current { border-color: #5be7ff80; box-shadow: 0 0 0 1px #5be7ff14, 0 18px 42px #0002; }
.content-card.is-revealed .block-content-reveal { animation: blockMaterialize .72s cubic-bezier(.18,.78,.22,1) both; }
.content-card.is-revealed .block-step-icon.current { animation: blockPulse 2s ease-in-out infinite; }
.block-content-reveal { position: relative; }
.block-typing-caret { position: absolute; top: 0; right: -7px; width: 2px; height: 1.2em; border-radius: 3px; background: var(--cy); box-shadow: 0 0 10px var(--cy); animation: typingBlink .7s steps(2, start) infinite; pointer-events: none; }
.block-teaser {
  min-height: 126px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 7px;
  text-align: center;
  border: 1px dashed #6879ad58;
  border-radius: 16px;
  background: radial-gradient(circle at 50% 20%, #8c7aff12, transparent 60%);
  color: var(--mut);
  animation: teaserBreath 3s ease-in-out infinite;
}
.block-teaser b { color: var(--txt); font-size: 13px; }
.block-teaser > span:not(.teaser-orbit) { font-size: 11px; }
.teaser-orbit { position: relative; width: 28px; height: 28px; display: block; border: 1px solid #8b80ff70; border-radius: 50%; animation: orbitSpin 4s linear infinite; }
.teaser-orbit i { position: absolute; width: 6px; height: 6px; border-radius: 50%; background: var(--cy); box-shadow: 0 0 9px var(--cy); }
.teaser-orbit i:nth-child(1) { top: -3px; left: 10px; }
.teaser-orbit i:nth-child(2) { right: -3px; bottom: 4px; background: #a18bff; }
.teaser-orbit i:nth-child(3) { left: -2px; bottom: 4px; background: #ffcf5a; }
.teaser-arrow { color: var(--cy); font-size: 16px !important; animation: arrowNudge 1.2s ease-in-out infinite; }
@keyframes blockMaterialize { from { opacity: 0; transform: translateY(17px) scale(.99); filter: blur(5px); clip-path: inset(0 0 35% 0 round 14px); } to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); clip-path: inset(0 0 0 0 round 0); } }
@keyframes blockPulse { 0%,100% { box-shadow: 0 0 0 0 #5be7ff00; } 50% { box-shadow: 0 0 0 5px #5be7ff14; } }
@keyframes teaserBreath { 0%,100% { border-color: #6879ad58; } 50% { border-color: #8b80ff99; } }
@keyframes orbitSpin { to { transform: rotate(360deg); } }
@keyframes arrowNudge { 0%,100% { transform: translateY(0); opacity: .65; } 50% { transform: translateY(4px); opacity: 1; } }
.quest.theme-light .block-stepbar { border-bottom-color: #34406418; }
.quest.theme-light .block-step-icon { color: #4f5a7d; background: linear-gradient(145deg, #f1f3ff, #e2e7fb); border-color: #d8def0; }
.quest.theme-light .block-step-icon.current { color: #fff; background: linear-gradient(135deg, #1aa5c4, #8067ed); border-color: #7d9aff; }
.quest.theme-light .block-step-icon.done { color: #075f4f; background: linear-gradient(135deg, #d4fff0, #8de4cf); }
.quest.theme-light .block-step-label b, .quest.theme-light .block-teaser b { color: #252b45; }
.quest.theme-light .block-teaser { border-color: #bfc8e4; background: radial-gradient(circle at 50% 20%, #8c7aff0d, transparent 60%); }
@media (prefers-reduced-motion: reduce) {
  .content-card.is-revealed .block-content-reveal, .content-card.is-revealed .block-step-icon.current, .block-teaser, .teaser-orbit, .teaser-arrow { animation: none !important; }
}

.content { min-width: 0; }

.c-heading {
  margin: 0;
  font-size: 22px;
  line-height: 1.8;
  font-weight: 900;
  overflow-wrap: anywhere;
}

.c-heading.lv1 { font-size: 27px; }
.c-heading.lv3 { font-size: 17px; }

.c-para {
  margin: 0;
  font-size: 15px;
  line-height: 2.3;
  color: #d3def8;
  overflow-wrap: anywhere;
}

.c-para :deep(strong),
.callout p :deep(strong),
.c-list :deep(strong) {
  font-weight: 900;
}

.c-para :deep(mark),
.callout p :deep(mark),
.c-list :deep(mark) {
  background: #ffd25c30;
  color: #ffe9a6;
  padding: 0 5px;
  border-radius: 6px;
}

.c-para :deep(code),
.callout p :deep(code),
.c-list :deep(code),
.feedback :deep(code) {
  direction: ltr;
  unicode-bidi: embed;
  background: #1d2850;
  color: #9fe7ff;
  padding: 1px 7px;
  border-radius: 7px;
  font-size: .92em;
}

.c-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 8px;
}

.c-list li {
  display: flex;
  gap: 10px;
  line-height: 2.1;
  font-size: 14px;
  color: #d3def8;
}

.c-list li > span { color: var(--cy); margin-top: 1px; }

/* Callout */
.callout {
  --c: #8f7bff;
  border-radius: 17px;
  padding: 1.5px;
  background: conic-gradient(
    from var(--ang),
    color-mix(in srgb, var(--c) 30%, transparent) 55%,
    var(--c) 78%,
    color-mix(in srgb, var(--c) 30%, transparent)
  );
  animation: spinAng 4s linear infinite;
  box-shadow: 0 0 28px color-mix(in srgb, var(--c) 12%, transparent);
}

.callout[data-style="definition"] { --c: #19c5b2; }
.callout[data-style="warning"] { --c: #ffd34f; }
.callout[data-style="trap"] { --c: #ff456a; }
.callout[data-style="example"] { --c: #4b8dff; }
.callout[data-style="summary"] { --c: #3ddc84; }
.callout[data-style="exam"] { --c: #b07cff; }

.callout-in {
  border-radius: 16px;
  padding: 16px 18px;
  background: linear-gradient(120deg, color-mix(in srgb, var(--c) 10%, #111a35), #111a35);
}

.callout-head { display: flex; align-items: center; gap: 12px; }

.callout-icon {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  flex: 0 0 40px;
  border-radius: 13px;
  font-size: 20px;
  background: color-mix(in srgb, var(--c) 18%, #121b35);
  border: 1px solid color-mix(in srgb, var(--c) 55%, transparent);
}

.callout-head small {
  display: block;
  font-size: 10px;
  font-weight: 700;
  color: var(--c);
}

.callout-head b { font-size: 14px; }
.callout p { margin: 12px 0 0; font-size: 13px; line-height: 2.2; color: #d9deef; }

/* Formula, quote, divider */
.formula {
  padding: 20px;
  text-align: center;
  border-radius: 16px;
  border: 1px solid #4a74a7;
  background: linear-gradient(130deg, #102c48, #25204e);
}

.formula small { font-size: 10px; color: var(--cy); font-weight: 700; }

.formula p {
  margin: 4px 0 0;
  font-size: 23px;
  font-weight: 800;
  color: #e6faff;
  line-height: 2;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  direction: ltr;
}

.quote {
  margin: 0;
  padding: 16px 20px;
  border-right: 3px solid #a18bff;
  border-radius: 0 13px 13px 0;
  background: #242044;
  color: #e6deff;
  font-size: 15px;
  line-height: 2.2;
}

.quote::before { content: '“'; margin-left: 4px; }
.quote::after { content: '”'; margin-right: 4px; }

.rune { display: flex; align-items: center; gap: 13px; color: var(--cy); }
.rune i { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #5d76b4, transparent); }

/* Flashcards */
.flash {
  perspective: 900px;
  cursor: pointer;
  height: 160px;
  outline-offset: 5px;
}

.flash-in {
  position: relative;
  height: 100%;
  transition: transform .6s cubic-bezier(.3, 1.2, .4, 1);
  transform-style: preserve-3d;
}

.flash.on .flash-in { transform: rotateY(180deg); }

.face {
  position: absolute;
  inset: 0;
  display: grid;
  place-content: center;
  text-align: center;
  gap: 8px;
  padding: 20px;
  border-radius: 18px;
  backface-visibility: hidden;
  background: linear-gradient(135deg, #3b2b72, #1c2a5c);
  border: 1px solid #8f7bff99;
  box-shadow: 0 12px 30px #0003;
}

.face small { font-size: 10px; color: #c0b8f2; }
.face b { font-size: 17px; line-height: 1.9; overflow-wrap: anywhere; }
.face.back { transform: rotateY(180deg); background: linear-gradient(135deg, #0e4d4a, #1c2a5c); border-color: #4df0c099; }
.face.back small { color: #a4f5dc; }

/* Quiz */
.boss {
  position: relative;
  padding: 18px;
  border-radius: 18px;
  border: 1px solid transparent;
  background:
    linear-gradient(140deg, #29182d, #1a1730 55%, #151b35) padding-box,
    conic-gradient(from var(--ang), #4a2a4a 55%, #ff426b 76%, #ffb05b 82%, #4a2a4a) border-box;
  animation: spinAng 4s linear infinite;
}

.boss-head { display: flex; align-items: center; gap: 11px; margin-bottom: 12px; }

.boss-head > span {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 13px;
  background: #61253f;
  color: #ff8b9d;
  font-size: 23px;
}

.boss-head > div { flex: 1; display: flex; flex-direction: column; }
.boss-head small { font-size: 10px; color: #ff8fa8; }
.boss-head b { font-size: 13px; }
.boss-head em { font-style: normal; font-size: 10px; padding: 5px 9px; border: 1px solid #b34464; border-radius: 8px; color: #ffb3c1; }

.boss h3 { margin: 0 0 14px; font-size: 15px; line-height: 2.1; }

.opts { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }

.opt {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  text-align: right;
  padding: 11px;
  border: 1px solid #47314f;
  border-radius: 13px;
  background: #15172e;
  color: #e0def2;
  cursor: pointer;
  font-size: 12.5px;
  line-height: 1.8;
  transition: transform .22s, border-color .22s, background .22s;
}

.opt:hover:not(:disabled) { transform: translateY(-2px); border-color: #ff7590; background: #2a1b36; }
.opt:disabled { cursor: default; }

.letter {
  width: 28px;
  height: 28px;
  flex: 0 0 28px;
  display: grid;
  place-items: center;
  border-radius: 9px;
  background: #38213d;
  color: #ff9caf;
  font-size: 11px;
  font-weight: 900;
}

.txt { flex: 1; overflow-wrap: anywhere; }
.res { font-size: 18px; font-weight: 900; }

.opt.correct,
.opt.reveal { border-color: #40e5b0; background: #123d3b; color: #caffed; }

.opt.correct .letter,
.opt.reveal .letter { background: #2ba88b; color: #fff; }

.opt.correct { animation: pop .5s cubic-bezier(.2, 1.6, .4, 1); }
.opt.wrong { border-color: #ff4c70; background: #4a1b35; color: #ffe0e7; animation: shake .4s; }

.feedback {
  margin-top: 13px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid #ff587b66;
  background: #4a1c354d;
  color: #ffa5b8;
}

.feedback.ok { border-color: #42e7b4aa; background: #0f443d66; color: #8ff8d8; }
.feedback b { font-size: 12px; }
.feedback p { margin: 6px 0 0; font-size: 12px; line-height: 2; color: #dcd6ee; }

/* Images and checklist */
.img { margin: 0; }
.img img { display: block; margin: auto; max-width: 100%; max-height: 520px; object-fit: contain; border-radius: 14px; border: 1px solid #3b4d76; }
.img figcaption { margin-top: 9px; text-align: center; font-size: 11px; color: var(--mut); }
.img-ph { padding: 46px; text-align: center; border: 1px dashed #465a87; border-radius: 14px; color: #90a4d2; }

.checklist { display: grid; gap: 8px; }

.checklist label {
  position: relative;
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 11px 13px;
  border-radius: 13px;
  border: 1px solid #2d4065;
  background: #101a33;
  color: #d3e1ff;
  font-size: 13px;
  line-height: 1.9;
  cursor: pointer;
  transition: .25s;
}

.checklist input { position: absolute; opacity: 0; width: 1px; height: 1px; }

.checklist input:focus-visible + .box {
  outline: 2px solid var(--cy);
  outline-offset: 3px;
}

.box {
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  border: 1.5px solid #4b618f;
  color: transparent;
  transition: .25s;
}

.checklist label.on { border-color: #2a887e; color: #8ff0d2; background: #0f2d33; }
.checklist label.on .box { color: #052b2a; background: #5ae4bd; border-color: #5ae4bd; transform: scale(1.06); }

.unknown p { white-space: pre-wrap; line-height: 2; color: #ccd9f4; }

/* Per-block completion control */
.block-complete {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 8px 12px;
  border: 1px solid var(--line);
  border-radius: 11px;
  background: var(--card2);
  color: var(--mut);
  font: inherit;
  font-size: 11px;
  cursor: pointer;
  transition: .2s ease;
}

.block-complete > span { font-size: 15px; font-weight: 900; }

.block-complete:hover {
  border-color: var(--vi);
  color: var(--vi);
  transform: translateY(-1px);
}

.block-complete.done {
  color: var(--mi);
  border-color: color-mix(in srgb, var(--mi) 45%, transparent);
  background: color-mix(in srgb, var(--mi) 9%, var(--card));
}

.empty {
  text-align: center;
  padding: 40px;
  color: var(--mut);
}

.empty h2,
.empty h3 { color: var(--txt); }

.empty-page {
  border: 1px dashed var(--line);
  border-radius: 22px;
}

/* Stage finish */
.finish {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 8px;
  padding: 18px;
  border-radius: 20px;
  border: 1px solid #3b4774;
  background: linear-gradient(100deg, #171f3e, #25234a);
  transition: .4s;
}

.finish.won {
  border-color: #8d8049;
  background: linear-gradient(100deg, #222b3b, #3d3242);
}

.finish-emblem {
  width: 54px;
  height: 54px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  font-size: 27px;
  border-radius: 17px;
  background: linear-gradient(145deg, #5d70bc, #2c315d);
}

.finish.won .finish-emblem { background: linear-gradient(145deg, #ffdb7d, #ce8d40); }

.finish-text { flex: 1; min-width: 0; }
.finish-text b { font-size: 14px; }
.finish-text p { margin: 4px 0 0; font-size: 11.5px; color: #a4b4da; line-height: 1.9; }

.finish-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* Toast and confetti */
.reward {
  position: fixed;
  z-index: 60;
  bottom: 26px;
  left: 26px;
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: min(460px, calc(100vw - 24px));
  padding: 13px 18px;
  border-radius: 16px;
  border: 1px solid #f4ce69;
  background: linear-gradient(120deg, #342b39, #172542);
  box-shadow: 0 16px 50px #0006, 0 0 30px #ffd55a18;
}

.reward span { font-size: 22px; color: #ffdc70; animation: spin 3s linear infinite; }
.reward b { font-size: 12px; }

.reward-enter-active { animation: pop .4s cubic-bezier(.2, 1.6, .4, 1); }
.reward-leave-active { transition: .25s; }
.reward-leave-to { opacity: 0; transform: translateY(12px); }

.confetti {
  position: fixed;
  inset: 0;
  z-index: 70;
  pointer-events: none;
  overflow: hidden;
}

.confetti i {
  position: absolute;
  top: -20px;
  left: calc(var(--x) * 1%);
  border-radius: 2px;
  background: var(--c);
  opacity: 0;
  transform: rotate(var(--r));
  animation: fall var(--t) cubic-bezier(.3, .5, .6, 1) var(--d) forwards;
}

.foot {
  text-align: center;
  padding: 8px 0 28px;
  font-size: 11px;
  color: #7181ad;
  letter-spacing: .5px;
}

/* Loading and error states */
.state {
  min-height: 68vh;
  display: grid;
  align-content: center;
  justify-items: center;
  gap: 14px;
  padding: 24px;
  text-align: center;
}

.state p { margin: 0; color: var(--mut); font-size: 12px; }
.state h2 { margin: 0; }

.portal { position: relative; width: 96px; height: 96px; display: grid; place-items: center; }

.portal::before,
.portal::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: var(--cy);
  border-bottom-color: var(--vi);
  inset: 4px;
  animation: spin 2s linear infinite;
}

.portal::after {
  inset: 18px;
  border-color: #8b72ff transparent var(--cy);
  animation-direction: reverse;
}

.portal span {
  width: 26px;
  height: 26px;
  border-radius: 9px;
  background: linear-gradient(145deg, #80f4ff, #9a78ff);
  box-shadow: 0 0 34px #70b9ff;
  animation: bob 1.5s infinite;
}

.err-gem {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  font-size: 34px;
  border-radius: 20px;
  color: #ff9db1;
  background: #492338;
  border: 1px solid #ff668b;
}

/* Transitions */
.card-enter-active,
.card-leave-active { transition: all .3s ease; }

.card-enter-from { opacity: 0; transform: translateY(18px) scale(.985); }
.card-leave-to { opacity: 0; transform: translateY(-8px); }

.fade-enter-active { transition: .3s; }
.fade-enter-from { opacity: 0; transform: translateY(-6px); }

/* =========================================================
   LIGHT THEME — follows site data-theme / classes
   ========================================================= */
.quest.theme-light {
  --bg: #f4f6fc;
  --card: #ffffff;
  --card2: #f0f3fb;
  --line: #e1e6f2;
  --txt: #202742;
  --mut: #68738e;
  --cy: #168ca8;
  --vi: #7456dc;
  --am: #bd8213;
  --co: #d9486b;
  --mi: #168e75;

  color: var(--txt);
  background:
    radial-gradient(ellipse at 50% -10%, rgba(139, 125, 255, .12), transparent 48%),
    var(--bg);
}

.quest.theme-light .bg-stars {
  opacity: .12;
  background-image:
    radial-gradient(#8b82d9 1px, transparent 1px),
    radial-gradient(#53a9c5 1px, transparent 1px);
}

.quest.theme-light .aurora { opacity: .09; }

.quest.theme-light .topbar {
  background: rgba(255, 255, 255, .88);
  border-bottom-color: var(--line);
  box-shadow: 0 4px 24px rgba(37, 48, 83, .05);
}

.quest.theme-light .brand { color: #252b45; }
.quest.theme-light .brand-copy small { color: var(--mut); }

.quest.theme-light .icon {
  color: #59627d;
  background: rgba(255, 255, 255, .92);
  border-color: #e0e5f1;
}

.quest.theme-light .icon:hover {
  color: #6f56d9;
  background: #f2efff;
  border-color: #bdb0f6;
}

.quest.theme-light .hero {
  border-color: color-mix(in srgb, var(--cover) 30%, white);
  box-shadow: 0 22px 55px rgba(43, 47, 92, .12), inset 0 1px rgba(255, 255, 255, .75);
}

.quest.theme-light .hero-icon {
  box-shadow: 0 12px 30px rgba(28, 36, 75, .13), inset 0 1px rgba(255, 255, 255, .8);
}

.quest.theme-light .meta,
.quest.theme-light .hero-copy p { color: #f6f5ff; }

.quest.theme-light .chips span {
  color: #fff;
  background: rgba(24, 29, 63, .20);
  border-color: rgba(255, 255, 255, .28);
}

.quest.theme-light .hero-card {
  background: rgba(255, 255, 255, .90);
  border-color: rgba(255, 255, 255, .75);
  box-shadow: 0 8px 26px rgba(31, 39, 78, .08);
}

.quest.theme-light .ring {
  background:
    radial-gradient(#fff 57%, transparent 59%),
    conic-gradient(var(--vi) calc(var(--p) * 1%), #e7e8f2 0);
}

.quest.theme-light .ring b { color: #292e49; }
.quest.theme-light .hero-card-text small { color: #7256d9; }
.quest.theme-light .hero-card-text b { color: #252b45; }
.quest.theme-light .hero-card-text span { color: #6b7590; }

.quest.theme-light .timeline-wrap {
  background: linear-gradient(145deg, #fff, #f9faff);
  border-color: var(--line);
  box-shadow: 0 12px 38px rgba(39, 50, 90, .055);
}

.quest.theme-light .timeline-heading h2 { color: #252b45; }
.quest.theme-light .timeline-kicker { color: #7456dc; }
.quest.theme-light .timeline-count { color: #737e98; }

.quest.theme-light .timeline-item {
  color: #252b45;
  background: linear-gradient(145deg, #fff, #f7f8fd);
  border-color: #e1e6f2;
  box-shadow: 0 3px 12px rgba(34, 43, 79, .025);
}

.quest.theme-light .timeline-item:hover {
  background: #f5f3ff;
  border-color: #bdb1f3;
  box-shadow: 0 8px 22px rgba(91, 73, 173, .08);
}

.quest.theme-light .timeline-index {
  color: #6d638e;
  background: linear-gradient(145deg, #f1efff, #e7e8fa);
  border-color: #ded8fa;
}

.quest.theme-light .timeline-copy small { color: #7456dc; }
.quest.theme-light .timeline-copy strong { color: #252b45; }
.quest.theme-light .timeline-copy > span { color: #747e97; }
.quest.theme-light .timeline-status { color: #7b849c; }
.quest.theme-light .timeline-arrow { color: #8b84b6; }

.quest.theme-light .timeline-item.active {
  background: linear-gradient(145deg, #f0f0ff, #e8f7ff);
  border-color: #8a81ed;
  box-shadow: 0 0 0 1px rgba(116, 86, 220, .08), 0 10px 28px rgba(65, 71, 133, .08);
}

.quest.theme-light .timeline-item.active .timeline-index {
  color: #fff;
  border-color: #8b80e9;
  background: linear-gradient(145deg, #38bfe2, #8065e8);
}

.quest.theme-light .timeline-item.active .timeline-status { color: #6550c6; }

.quest.theme-light .timeline-item.done {
  border-color: #9bd8c7;
  background: linear-gradient(145deg, #f5fffb, #f1fbf8);
}

.quest.theme-light .timeline-item.done .timeline-index {
  color: #fff;
  border-color: #79cbb5;
  background: linear-gradient(145deg, #51c8a8, #249e87);
}

.quest.theme-light .timeline-item.done .timeline-status { color: #18856e; }

.quest.theme-light .stage-title h2 { color: #262d49; }
.quest.theme-light .stage-title small { color: #7456dc; }
.quest.theme-light .stage-title p { color: #737d97; }

.quest.theme-light .stage-medal {
  border-color: #e0e3f1;
  background: linear-gradient(145deg, #fff, #eeeffb);
}

.quest.theme-light .stage-track {
  background: #e7eaf4;
  border-color: #dfe4f0;
}

.quest.theme-light .content-card {
  color: #29304b;
  background: linear-gradient(145deg, #fff, #fbfcff);
  border-color: #e2e6f1;
  box-shadow: 0 9px 28px rgba(36, 46, 83, .045);
}

.quest.theme-light .content-card.is-complete { border-color: #a8dfd0; }
.quest.theme-light .c-heading { color: #252b45; }
.quest.theme-light .c-para,
.quest.theme-light .c-list li { color: #454e68; }

.quest.theme-light .c-para :deep(mark),
.quest.theme-light .callout p :deep(mark),
.quest.theme-light .c-list :deep(mark) {
  color: #72500c;
  background: #fff0bf;
}

.quest.theme-light .c-para :deep(code),
.quest.theme-light .callout p :deep(code),
.quest.theme-light .c-list :deep(code),
.quest.theme-light .feedback :deep(code) {
  color: #4b4396;
  background: #efedff;
}

.quest.theme-light .callout-in {
  background: linear-gradient(120deg, color-mix(in srgb, var(--c) 7%, white), white);
}

.quest.theme-light .callout-head b { color: #2a3049; }
.quest.theme-light .callout p { color: #515b73; }
.quest.theme-light .callout-icon { background: color-mix(in srgb, var(--c) 10%, white); }

.quest.theme-light .formula {
  background: linear-gradient(130deg, #f0f9ff, #f4f0ff);
  border-color: #cbdaf0;
}

.quest.theme-light .formula small { color: #287eaa; }
.quest.theme-light .formula p { color: #27324e; }

.quest.theme-light .quote {
  color: #51456e;
  background: #f4f0ff;
  border-right-color: #9077e6;
}

.quest.theme-light .face {
  color: #fff;
  background: linear-gradient(135deg, #6850b5, #394c91);
  border-color: #b6a9ef;
  box-shadow: 0 12px 30px rgba(50, 43, 103, .13);
}

.quest.theme-light .face small { color: #e3ddff; }
.quest.theme-light .face.back { background: linear-gradient(135deg, #167e76, #365c91); border-color: #86dcca; }

.quest.theme-light .boss {
  background:
    linear-gradient(140deg, #fff8fb, #f7f3ff 55%, #f0f6ff) padding-box,
    conic-gradient(from var(--ang), #e6d8e5 55%, #f07898 76%, #ffc77d 82%, #e6d8e5) border-box;
}

.quest.theme-light .boss-head > span { color: #bf4369; background: #ffe5ed; }
.quest.theme-light .boss-head small { color: #b33c64; }
.quest.theme-light .boss-head b,
.quest.theme-light .boss h3 { color: #2a3049; }
.quest.theme-light .boss-head em { color: #a83e60; border-color: #f0c1d0; }

.quest.theme-light .opt {
  color: #3b435d;
  background: #fff;
  border-color: #e5dce8;
}

.quest.theme-light .opt:hover:not(:disabled) { background: #fff3f7; border-color: #e7a0b5; }
.quest.theme-light .letter { color: #a33d62; background: #fff0f5; }

.quest.theme-light .opt.correct,
.quest.theme-light .opt.reveal {
  color: #176a56;
  background: #e7faf3;
  border-color: #79cfb5;
}

.quest.theme-light .opt.correct .letter,
.quest.theme-light .opt.reveal .letter { color: #fff; background: #36a98c; }

.quest.theme-light .opt.wrong {
  color: #a52e4e;
  background: #fff0f3;
  border-color: #ee9ab0;
}

.quest.theme-light .feedback {
  color: #a43b5a;
  background: #fff3f6;
  border-color: #f0c2d0;
}

.quest.theme-light .feedback.ok {
  color: #14735c;
  background: #edfbf6;
  border-color: #a2dfcb;
}

.quest.theme-light .feedback p { color: #59627a; }
.quest.theme-light .img img { border-color: #e0e5f0; }
.quest.theme-light .img-ph { color: #727c96; border-color: #cbd3e5; }

.quest.theme-light .checklist label {
  color: #3d4660;
  background: #fff;
  border-color: #e1e6f1;
}

.quest.theme-light .checklist label.on {
  color: #18725e;
  background: #edfbf6;
  border-color: #9bdac7;
}

.quest.theme-light .box { border-color: #cbd3e5; }

.quest.theme-light .checklist label.on .box {
  color: #fff;
  background: #31aa8b;
  border-color: #31aa8b;
}

.quest.theme-light .unknown p { color: #515b73; }

.quest.theme-light .block-complete {
  background: #f8f9ff;
  border-color: #e0e5f1;
  color: #68738e;
}

.quest.theme-light .block-complete.done {
  color: #168e75;
  background: #edfbf6;
  border-color: #a8dfd0;
}

.quest.theme-light .empty { color: #68738e; }
.quest.theme-light .empty h2,
.quest.theme-light .empty h3 { color: #252b45; }

.quest.theme-light .finish {
  background: linear-gradient(100deg, #fff, #f3f2ff);
  border-color: #e0e2f1;
}

.quest.theme-light .finish.won {
  background: linear-gradient(100deg, #fffdf4, #fff5e4);
  border-color: #e7d5a5;
}

.quest.theme-light .finish-text b { color: #292f49; }
.quest.theme-light .finish-text p { color: #68738d; }
.quest.theme-light .finish-emblem { background: linear-gradient(145deg, #9ca9ed, #6f72bd); }
.quest.theme-light .finish.won .finish-emblem { background: linear-gradient(145deg, #ffdb7d, #ce8d40); }

.quest.theme-light .btn.quiet {
  color: #514a78;
  background: #f0edff;
  border-color: #d7d0fa;
}

.quest.theme-light .reward {
  color: #33304b;
  background: linear-gradient(120deg, #fffdf5, #fff);
  border-color: #ebd38a;
  box-shadow: 0 16px 45px rgba(39, 39, 66, .13);
}

.quest.theme-light .reward b { color: #39334d; }
.quest.theme-light .foot { color: #858eaa; }
.quest.theme-light .state { color: #292f49; }
.quest.theme-light .state p { color: #727c96; }

.quest.theme-light .err-gem {
  color: #bd3f62;
  background: #fff0f4;
  border-color: #f0b1c2;
}

/* Responsive */
@media (max-width: 760px) {
  .topbar { gap: 8px; height: 62px; padding-inline: 12px; }
  .brand-copy { display: none; }

  .hero {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 22px 18px;
    border-radius: 23px;
  }

  .hero-icon {
    width: 64px;
    height: 64px;
    font-size: 32px;
    border-radius: 20px;
  }

  .hero-card { flex-wrap: wrap; padding: 13px; }
  .hero-card .btn { width: 100%; }

  .timeline-wrap { padding: 16px 12px; }
  .timeline-heading { align-items: flex-start; flex-direction: column; gap: 6px; }
  .timeline { grid-template-columns: 1fr; gap: 10px; }
  .timeline-item { min-height: 88px; padding: 13px 12px; }
  .timeline-status { left: 10px; bottom: 7px; }

  .content-card { padding: 15px 13px; }
  .c-para { font-size: 14px; }
  .opts { grid-template-columns: 1fr; }

  .finish { flex-wrap: wrap; }
  .finish-actions { width: 100%; }
  .finish-actions .btn { flex: 1; }

  .reward { left: 12px; right: 12px; bottom: 12px; }
  .stage-medal { width: 52px; height: 52px; font-size: 23px; }
}

@media (max-width: 420px) {
  .world { padding-inline: 10px; }
  .hero h1 { font-size: 25px; }
  .hero-card-text b { white-space: normal; }
  .timeline-status { max-width: 90px; text-align: left; }
  .content-card { border-radius: 16px; }
  .finish-emblem { width: 45px; height: 45px; }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .quest *,
  .quest *::before,
  .quest *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }

  .confetti { display: none; }
}

/* Print */
@media print {
  .topbar,
  .timeline-wrap,
  .hero-card,
  .block-complete,
  .finish,
  .reward,
  .confetti,
  .foot,
  .bg-stars,
  .aurora {
    display: none !important;
  }

  .quest,
  .quest.theme-light {
    color: #111 !important;
    background: #fff !important;
  }

  .hero,
  .content-card,
  .callout-in,
  .boss,
  .formula,
  .quote {
    color: #111 !important;
    background: #fff !important;
    box-shadow: none !important;
    border: 1px solid #bbb !important;
    animation: none !important;
  }

  .content-card { break-inside: avoid; }
  .c-heading,
  .c-para,
  .c-list li,
  .callout p,
  .formula p,
  .quote,
  .boss h3 {
    color: #222 !important;
  }

  .hero-copy p,
  .meta { color: #333 !important; }
  .callout { background: #ddd !important; }
  .flash { break-inside: avoid; }
}

@keyframes spinAng { to { --ang: 360deg; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
@keyframes float { to { transform: translate(60px, -40px) scale(1.15); } }
@keyframes drift { to { background-position: 0 1200px, 31px 1700px; } }
@keyframes shine {
  0%, 60% { transform: translateX(120%); }
  100% { transform: translateX(-120%); }
}
@keyframes pop {
  from { opacity: 0; transform: scale(.85); }
  60% { transform: scale(1.06); }
  to { opacity: 1; transform: none; }
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
}
@keyframes fall {
  0% { opacity: 1; transform: translateY(0) rotate(var(--r)); }
  100% {
    opacity: .9;
    transform: translateY(108vh) rotate(calc(var(--r) + 720deg)) translateX(40px);
  }
}


/* --- Modern Dopamine reader refresh: global theme-aware surfaces --- */
.quest {
  --accent: var(--primary, #7867f5);
  --accent-hover: var(--primary-hover, #6552e8);
  --accent-soft: var(--primary-50, color-mix(in srgb, var(--accent) 12%, transparent));
  --bg: #0a0d16;
  --card: #111722;
  --card2: #171f2d;
  --line: #293345;
  --txt: #f4f6fb;
  --mut: #9ba7bb;
  --cy: var(--accent);
  --vi: #9b8cff;
  --am: #e9b96e;
  --co: #f0788e;
  --mi: #59d7b1;
  background: var(--bg);
  color: var(--txt);
}
.quest.theme-light {
  --bg: #f4f6fb;
  --card: #ffffff;
  --card2: #f8f9fd;
  --line: #e1e6ef;
  --txt: #20283a;
  --mut: #727d91;
  --cy: var(--primary, #7055e8);
  --vi: #7965e9;
  --am: #ad7b2b;
  --co: #c34e69;
  --mi: #218f76;
  background: radial-gradient(ellipse at 50% -20%, color-mix(in srgb, var(--accent) 10%, white), transparent 48%), var(--bg);
}
.quest .bg-stars { opacity: .08; }
.quest.theme-light .bg-stars { opacity: .12; background-image: radial-gradient(color-mix(in srgb, var(--accent) 30%, white) 1px, transparent 1px), radial-gradient(#c8cfe0 1px, transparent 1px); }
.quest .aurora { opacity: .09; }
.quest.theme-light .aurora { opacity: .06; }
.quest .topbar {
  background: color-mix(in srgb, var(--bg) 86%, transparent);
  border-bottom-color: var(--line);
  box-shadow: 0 8px 30px #00000008;
}
.quest.theme-light .topbar { background: color-mix(in srgb, #ffffff 88%, transparent); }
.quest .gem { background: color-mix(in srgb, var(--accent) 15%, var(--card)); color: var(--accent); border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent); box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 14%, transparent); }
.quest .gem svg, .quest .icon svg, .quest .chips svg, .quest .timeline-index svg, .quest .block-step-icon svg, .quest .timeline-arrow svg, .quest .teaser-arrow svg, .quest .res svg, .quest .box svg, .quest .divider-mark svg, .quest .img-ph svg, .quest .stage-medal svg, .quest .finish-emblem svg, .quest .btn svg, .quest .callout-icon svg, .quest .boss-icon svg, .quest .reward-icon svg, .quest .list-bullet svg { width: 21px; height: 21px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.quest .timeline-index svg, .quest .block-step-icon svg { width: 19px; height: 19px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.quest .timeline-arrow svg, .quest .teaser-arrow svg { width: 17px; height: 17px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.quest .res svg, .quest .box svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.quest .divider-mark svg { width: 20px; height: 20px; fill: currentColor; stroke: none; }
.quest .img-ph { display: flex; align-items: center; justify-content: center; gap: 9px; }
.quest .img-ph svg { width: 24px; height: 24px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.quest .gem svg { width: 24px; height: 24px; fill: currentColor; stroke: none; }
.quest .icon { background: var(--card); border-color: var(--line); color: var(--mut); }
.quest .icon:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }
.quest .top-progress { background: color-mix(in srgb, var(--line) 70%, transparent); }
.quest .top-progress i { background: linear-gradient(90deg, var(--accent), color-mix(in srgb, var(--accent) 35%, #7dd3fc)); box-shadow: 0 0 12px color-mix(in srgb, var(--accent) 30%, transparent); }
.quest .btn.primary { border: 1px solid color-mix(in srgb, var(--accent) 45%, white); background: linear-gradient(135deg, var(--accent), color-mix(in srgb, var(--accent) 72%, #9d8cff)); box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 20%, transparent); }
.quest .btn.quiet { color: var(--txt); background: var(--card); border-color: var(--line); }
.quest .hero { border-color: color-mix(in srgb, var(--accent) 25%, var(--line)); background: linear-gradient(125deg, color-mix(in srgb, var(--cover) 24%, var(--card)), var(--card) 78%); box-shadow: 0 24px 65px #0000000c, inset 0 1px #ffffff0a; }
.quest.theme-light .hero { background: linear-gradient(125deg, color-mix(in srgb, var(--cover) 13%, white), white 78%); }
.quest .hero-icon { color: var(--accent); background: color-mix(in srgb, var(--accent) 9%, var(--card)); border-color: color-mix(in srgb, var(--accent) 24%, var(--line)); box-shadow: 0 12px 30px color-mix(in srgb, var(--accent) 10%, transparent); }
.quest .hero-icon svg { width: 54px; height: 54px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.quest .meta, .quest .hero-copy p { color: var(--mut); }
.quest .hero h1 { color: var(--txt); text-shadow: none; }
.quest .chips span { display: inline-flex; align-items: center; gap: 7px; color: var(--mut); border-color: var(--line); background: color-mix(in srgb, var(--card) 75%, transparent); }
.quest .chips svg { width: 15px; height: 15px; color: var(--accent); }
.quest .hero-card { background: color-mix(in srgb, var(--card) 90%, transparent); border-color: var(--line); }
.quest .ring { background: radial-gradient(var(--card) 57%, transparent 59%), conic-gradient(var(--accent) calc(var(--p) * 1%), var(--line) 0); }
.quest .hero-card-text small { color: var(--accent); }
.quest .hero-card-text span { color: var(--mut); }

/* Timeline: connected journey with clear active/completed states */
.quest .timeline-wrap { padding: clamp(18px, 3vw, 28px); background: var(--card); border-color: var(--line); border-radius: 26px; box-shadow: 0 18px 45px #00000006; }
.quest .timeline-heading { align-items: flex-end; }
.quest .timeline-kicker { color: var(--accent); letter-spacing: 2.4px; }
.quest .timeline-heading h2 { color: var(--txt); font-size: clamp(20px, 2.4vw, 25px); }
.quest .timeline-count { padding: 7px 11px; border-radius: 999px; color: var(--mut); background: var(--card2); border: 1px solid var(--line); }
.quest .timeline { position: relative; gap: 14px; }
.quest .timeline-item { min-height: 108px; padding: 18px 16px 22px; border: 1px solid var(--line); border-radius: 19px; background: var(--card2); overflow: hidden; }
.quest .timeline-item::before { content: ''; position: absolute; inset: 0 auto 0 0; width: 3px; background: transparent; transition: background .25s; }
.quest .timeline-item.active { border-color: color-mix(in srgb, var(--accent) 60%, var(--line)); background: color-mix(in srgb, var(--accent) 7%, var(--card)); box-shadow: 0 10px 28px color-mix(in srgb, var(--accent) 10%, transparent); }
.quest .timeline-item.active::before { background: var(--accent); }
.quest .timeline-item.done .timeline-index { background: color-mix(in srgb, var(--mi) 14%, var(--card)); border-color: color-mix(in srgb, var(--mi) 45%, var(--line)); color: var(--mi); }
.quest .timeline-index { border-radius: 15px; background: var(--card); border-color: var(--line); color: var(--mut); }
.quest .timeline-item.active .timeline-index { color: var(--accent); border-color: color-mix(in srgb, var(--accent) 45%, var(--line)); background: color-mix(in srgb, var(--accent) 11%, var(--card)); }
.quest .timeline-copy small { color: var(--accent); }
.quest .timeline-copy strong { color: var(--txt); }
.quest .timeline-copy > span, .quest .timeline-status, .quest .timeline-arrow { color: var(--mut); }
.quest .timeline-status { left: 15px; bottom: 12px; }
.quest .timeline-arrow { top: 13px; left: 14px; color: var(--accent); }

/* Stage and centered reading cards */
.quest .study { scroll-margin-top: 86px; }
.quest .stage-head { padding: 8px 2px 16px; }
.quest .stage-title small { color: var(--accent); }
.quest .stage-title h2 { color: var(--txt); letter-spacing: -.3px; }
.quest .stage-description { color: var(--mut); }
.quest .stage-medal { display: grid; place-items: center; color: var(--accent); background: color-mix(in srgb, var(--accent) 9%, var(--card)); border: 1px solid color-mix(in srgb, var(--accent) 28%, var(--line)); border-radius: 20px; }
.quest .stage-medal svg { width: 34px; height: 34px; }
.quest .stage-track { background: var(--card); border-color: var(--line); }
.quest .stage-track i { background: linear-gradient(90deg, var(--accent), #72d4e8); }
.quest .stack { gap: 25px; padding-block: 28vh 30vh; }
.quest .content-card { position: relative; scroll-margin-block: 42vh; border-color: var(--line); background: var(--card); box-shadow: 0 22px 55px #00000008; opacity: .38; filter: blur(1.2px) saturate(.78); transform: scale(.965); transition: opacity .45s ease, filter .45s ease, transform .45s ease, border-color .35s ease, box-shadow .35s ease; }
.quest .content-card.is-current { opacity: 1; filter: none; transform: scale(1); border-color: color-mix(in srgb, var(--accent) 38%, var(--line)); box-shadow: 0 26px 70px #00000012, 0 0 0 1px color-mix(in srgb, var(--accent) 6%, transparent); }
.quest .content-card.is-complete .block-step-icon { color: var(--mi); border-color: color-mix(in srgb, var(--mi) 48%, var(--line)); background: color-mix(in srgb, var(--mi) 10%, var(--card)); }
.quest .block-stepbar { border-bottom-color: var(--line); }
.quest .block-step-icon { color: var(--mut); border-color: var(--line); background: var(--card2); }
.quest .block-step-icon.current { color: var(--accent); border-color: color-mix(in srgb, var(--accent) 55%, var(--line)); background: color-mix(in srgb, var(--accent) 10%, var(--card)); }
.quest .block-step-label small { color: var(--mut); }
.quest .block-step-label b { color: var(--txt); }
.quest .block-step-status { color: var(--mut); }
.quest .block-step-status.done { color: var(--mi); }
.quest .c-heading, .quest .boss h3, .quest .unknown b { color: var(--txt); }
.quest .c-para, .quest .c-list, .quest .callout p, .quest .quote, .quest .unknown p { color: color-mix(in srgb, var(--txt) 82%, var(--mut)); }
.quest .c-para { font-size: 16px; line-height: 2.35; }
.quest .c-list li { color: var(--txt); }
.quest .list-bullet { display: grid; place-items: center; flex: 0 0 25px; width: 25px; height: 25px; border-radius: 8px; color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--card)); }
.quest .list-bullet svg { width: 15px; height: 15px; }
.quest .callout { border-color: color-mix(in srgb, var(--c, var(--accent)) 34%, var(--line)); background: color-mix(in srgb, var(--c, var(--accent)) 7%, var(--card)); }
.quest .callout-icon { display: grid; place-items: center; color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--card)); border-radius: 12px; width: 42px; height: 42px; }
.quest .callout-icon svg { width: 24px; height: 24px; }
.quest .formula, .quest .quote, .quest .boss, .quest .flash, .quest .checklist label, .quest .unknown { background: var(--card2); border-color: var(--line); color: var(--txt); }
.quest .formula small, .quest .flash small, .quest .boss-head small { color: var(--accent); }
.quest .formula p { color: var(--txt); }
.quest .boss-icon { display: grid; place-items: center; color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--card)); width: 38px; height: 38px; border-radius: 12px; }
.quest .opt { background: var(--card); border-color: var(--line); color: var(--txt); }
.quest .opt:hover:not(:disabled) { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 6%, var(--card)); }
.quest .opt .letter { background: var(--card2); border-color: var(--line); color: var(--mut); }
.quest .feedback { background: color-mix(in srgb, var(--co) 8%, var(--card)); color: var(--txt); }
.quest .feedback.ok { background: color-mix(in srgb, var(--mi) 9%, var(--card)); }
.quest .checklist label { color: var(--txt); }
.quest .checklist label.on { border-color: color-mix(in srgb, var(--mi) 42%, var(--line)); background: color-mix(in srgb, var(--mi) 8%, var(--card)); }
.quest .checklist input { accent-color: var(--accent); }
.quest .img { border-color: var(--line); background: var(--card2); }
.quest .img figcaption { color: var(--mut); }
.quest .block-teaser { background: color-mix(in srgb, var(--card2) 80%, transparent); color: var(--mut); }
.quest .teaser-arrow { color: var(--accent); }
.quest .stage-end { border-color: var(--line); background: var(--card); }
.quest .finish-emblem { display: grid; place-items: center; color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--card2)); border: 1px solid color-mix(in srgb, var(--accent) 28%, var(--line)); border-radius: 16px; }
.quest .finish-emblem svg { width: 27px; height: 27px; }
.quest .finish-text b { color: var(--txt); }
.quest .finish-text p { color: var(--mut); }
.quest .stage-actions { display: flex; flex-direction: column; align-items: flex-start; gap: 9px; margin-top: 20px; }
.quest .stage-next-btn { gap: 10px; min-height: 48px; padding-inline: 20px; }
.quest .stage-next-btn svg { width: 18px; height: 18px; }
.quest .stage-action-hint { font-size: 11px; color: var(--mut); }
.quest .reward { background: var(--card); color: var(--txt); border-color: var(--line); box-shadow: 0 18px 45px #0002; }
.quest .reward-icon { display: grid; place-items: center; color: var(--accent); }
.quest .foot { color: var(--mut); }
.quest .state { color: var(--txt); }
.quest .state p { color: var(--mut); }
.quest .empty { background: var(--card); color: var(--txt); border-color: var(--line); }

@media (max-width: 680px) {
  .quest .world { padding-top: 14px; gap: 16px; }
  .quest .topbar { height: 60px; padding-inline: 12px; }
  .quest .brand-copy small { display: none; }
  .quest .gem { width: 34px; height: 34px; flex-basis: 34px; }
  .quest .icon { width: 35px; height: 35px; }
  .quest .hero { grid-template-columns: 1fr; gap: 14px; padding: 22px 18px; border-radius: 22px; }
  .quest .hero-icon { width: 62px; height: 62px; border-radius: 19px; }
  .quest .hero-icon svg { width: 42px; height: 42px; }
  .quest .hero-card { flex-wrap: wrap; padding: 13px; }
  .quest .hero-card .btn { width: 100%; }
  .quest .timeline-wrap { padding: 16px; border-radius: 20px; }
  .quest .timeline { grid-template-columns: 1fr; gap: 9px; }
  .quest .timeline-item { min-height: 88px; }
  .quest .timeline-status { display: none; }
  .quest .stack { gap: 18px; padding-block: 20vh 22vh; }
  .quest .content-card { scroll-margin-block: 35vh; }
  .quest .c-para { font-size: 14px; line-height: 2.15; }
  .quest .stage-actions { align-items: stretch; }
  .quest .stage-next-btn { width: 100%; }
}
@media (prefers-reduced-motion: reduce) {
  .quest *, .quest *::before, .quest *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
}



/* Minimal card chrome, refined SVG icons, and viewport-third navigation */
.quest .block-stepbar { display: none !important; }
.quest .content-card {
  --block-tone: var(--accent);
  position: relative;
  isolation: isolate;
  overflow: hidden;
  padding: 14px 19px 16px;
  background: color-mix(in srgb, var(--block-tone) 7%, var(--card));
  border-color: color-mix(in srgb, var(--block-tone) 24%, var(--line));
}
.quest .content-card::before {
  content: '';
  position: absolute;
  z-index: 0;
  inset: -1px;
  border-radius: inherit;
  padding: 1.5px;
  background: conic-gradient(from var(--ang), transparent 0 48%, color-mix(in srgb, var(--block-tone) 88%, white) 58%, transparent 72% 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: .12;
  pointer-events: none;
  animation: spinAng 5.5s linear infinite;
  transition: opacity .35s ease;
}
.quest .content-card.is-current::before { opacity: .95; }
.quest .content-card.is-current {
  background: color-mix(in srgb, var(--block-tone) 10%, var(--card));
  border-color: color-mix(in srgb, var(--block-tone) 48%, var(--line));
  box-shadow: 0 20px 55px color-mix(in srgb, var(--block-tone) 10%, transparent), 0 0 0 1px color-mix(in srgb, var(--block-tone) 10%, transparent);
}
.quest .content-card.tone-heading { --block-tone: #9b83ff; }
.quest .content-card.tone-paragraph { --block-tone: #57a6ff; }
.quest .content-card.tone-list { --block-tone: #40d9cb; }
.quest .content-card.tone-tip { --block-tone: #ffc857; }
.quest .content-card.tone-warning { --block-tone: #ffd34f; }
.quest .content-card.tone-trap { --block-tone: #ff526f; }
.quest .content-card.tone-definition { --block-tone: #29cbb7; }
.quest .content-card.tone-example { --block-tone: #5796ff; }
.quest .content-card.tone-summary { --block-tone: #45d69a; }
.quest .content-card.tone-exam { --block-tone: #b18aff; }
.quest .content-card.tone-custom { --block-tone: #ff9f63; }
.quest .content-card.tone-formula { --block-tone: #ffae58; }
.quest .content-card.tone-quote { --block-tone: #b18aff; }
.quest .content-card.tone-divider { --block-tone: #8b9ab6; }
.quest .content-card.tone-flashcard { --block-tone: #35c9e8; }
.quest .content-card.tone-quiz { --block-tone: #ff526f; }
.quest .content-card.tone-image { --block-tone: #8c91ff; }
.quest .content-card.tone-checklist { --block-tone: #45d69a; }
.quest .content-card.tone-default { --block-tone: #8f7bff; }
.quest .block-nav-edge { position: relative; z-index: 2; display: flex; align-items: center; min-height: 28px; }
.quest .block-nav-top { justify-content: flex-start; margin: -2px 0 10px; }
.quest .block-type-icon {
  display: inline-grid;
  place-items: center;
  border-radius: 12px;
  color: var(--block-tone);
  background: color-mix(in srgb, var(--block-tone) 12%, var(--card2));
  border: 1px solid color-mix(in srgb, var(--block-tone) 28%, var(--line));
  box-shadow: inset 0 1px 0 #ffffff12, 0 5px 14px color-mix(in srgb, var(--block-tone) 8%, transparent);
  transition: transform .3s ease, box-shadow .3s ease;
}
.quest .block-type-icon svg { width: 20px; height: 20px; overflow: visible; }
.quest .content-card.is-current .block-type-icon { transform: translateY(-1px); box-shadow: 0 0 0 4px color-mix(in srgb, var(--block-tone) 8%, transparent), 0 8px 20px color-mix(in srgb, var(--block-tone) 16%, transparent); }
.quest .content-card .block-content-reveal { position: relative; z-index: 1; }
.quest .content-card > .block-nav-edge, .quest .content-card > .block-teaser { position: relative; z-index: 1; }
.quest .callout[data-style="tip"] { --c: #ffc857; }
.quest .callout[data-style="custom"] { --c: #ff9f63; }
.quest .callout-icon svg, .quest .boss-icon svg { width: 22px; height: 22px; }
.quest .boss-icon { display: grid; place-items: center; }
.quest .teaser-title { display: inline-flex; align-items: center; gap: 8px; }
.quest .teaser-title svg { width: 19px; height: 19px; color: var(--accent); }
.quest.theme-light .content-card { background: color-mix(in srgb, var(--block-tone) 5%, white); }
.quest.theme-light .content-card.is-current { background: color-mix(in srgb, var(--block-tone) 8%, white); }
@media (max-width: 680px) {
  .quest .content-card { padding: 12px 13px 13px; }
  .quest .block-type-icon { width: 32px; height: 32px; border-radius: 10px; }
  .quest .block-type-icon svg { width: 18px; height: 18px; }
}


/* Refined motion system: richer depth without allowing animations to drive navigation. */
@keyframes cardArrival {
  0% { opacity: .55; transform: translateY(18px) scale(.985); filter: blur(5px); }
  65% { opacity: 1; transform: translateY(-2px) scale(1.003); filter: blur(0); }
  100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}
@keyframes toneGlow {
  0%, 100% { box-shadow: 0 22px 58px color-mix(in srgb, var(--block-tone) 10%, transparent), 0 0 0 1px color-mix(in srgb, var(--block-tone) 10%, transparent); }
  50% { box-shadow: 0 28px 72px color-mix(in srgb, var(--block-tone) 18%, transparent), 0 0 0 1px color-mix(in srgb, var(--block-tone) 22%, transparent); }
}
@keyframes iconFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-3px) rotate(-2deg); }
}
.quest .content-card.is-current {
  animation: cardArrival .62s cubic-bezier(.2,.8,.2,1) both, toneGlow 4.8s ease-in-out .62s infinite;
  will-change: transform, opacity, filter;
}
.quest .content-card.is-current .block-type-icon {
  animation: iconFloat 3.2s ease-in-out .7s infinite;
}
.quest .content-card.is-current .block-content-reveal {
  animation: contentReveal .55s cubic-bezier(.2,.75,.25,1) both;
}
@keyframes contentReveal {
  from { opacity: .4; transform: translateY(9px); filter: blur(2px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.quest .content-card::after {
  content: '';
  position: absolute;
  pointer-events: none;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  background: linear-gradient(112deg, transparent 15%, color-mix(in srgb, var(--block-tone) 7%, transparent) 48%, transparent 75%);
  background-size: 220% 100%;
  opacity: 0;
  transition: opacity .35s ease;
}
.quest .content-card.is-current::after {
  opacity: 1;
  animation: cardSheen 5.5s ease-in-out infinite;
}
@keyframes cardSheen {
  0%, 100% { background-position: 120% 0; }
  50% { background-position: -20% 0; }
}
@media (prefers-reduced-motion: reduce) {
  .quest .content-card.is-current,
  .quest .content-card.is-current .block-type-icon,
  .quest .content-card.is-current .block-content-reveal,
  .quest .content-card.is-current::after { animation: none !important; }
}



/* Premium motion polish: layered glass, controlled ambient light and accessible motion. */
.quest .topbar {
  box-shadow: 0 10px 35px rgba(0, 0, 0, .10);
  transition: background .35s ease, border-color .35s ease, box-shadow .35s ease;
}
.quest .brand:hover .gem {
  transform: translateY(-2px) rotate(-7deg) scale(1.04);
  box-shadow: 0 0 0 6px color-mix(in srgb, var(--cy) 9%, transparent), 0 0 34px color-mix(in srgb, var(--cy) 36%, transparent);
}
.quest .icon {
  transition: transform .22s cubic-bezier(.2,.8,.2,1), background .25s ease, border-color .25s ease, box-shadow .25s ease;
}
.quest .icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px color-mix(in srgb, var(--cy) 16%, transparent);
}
.quest .hero {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  box-shadow: 0 28px 85px rgba(0,0,0,.16), inset 0 1px rgba(255,255,255,.12);
  animation: heroLift .8s cubic-bezier(.2,.8,.2,1) both;
}
.quest .hero::before {
  content: '';
  position: absolute;
  inset: -1px;
  z-index: -1;
  pointer-events: none;
  background: radial-gradient(circle at 12% 12%, color-mix(in srgb, var(--cover) 28%, transparent), transparent 42%), linear-gradient(115deg, transparent 25%, rgba(255,255,255,.07) 48%, transparent 68%);
  background-size: auto, 220% 100%;
  animation: heroGleam 9s ease-in-out infinite;
}
.quest .hero h1 { letter-spacing: -.045em; text-wrap: balance; }
.quest .hero-icon { transition: transform .4s cubic-bezier(.2,.8,.2,1), box-shadow .4s ease; }
.quest .hero:hover .hero-icon { transform: translateY(-4px) rotate(-3deg); box-shadow: 0 18px 42px color-mix(in srgb, var(--accent) 22%, transparent); }
.quest .timeline-wrap { position: relative; overflow: hidden; backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); }
.quest .timeline-wrap::before {
  content: '';
  position: absolute;
  inset: 0 0 auto;
  height: 1px;
  pointer-events: none;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--accent) 65%, white), transparent);
  opacity: .8;
}
.quest .timeline-item {
  transform: translateZ(0);
  transition: transform .28s cubic-bezier(.2,.8,.2,1), background .28s ease, border-color .28s ease, box-shadow .28s ease;
}
.quest .timeline-item:hover { transform: translateY(-3px); border-color: color-mix(in srgb, var(--accent) 45%, var(--line)); }
.quest .timeline-item.active { animation: timelinePulse 3.8s ease-in-out infinite; }
.quest .timeline-index { transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s ease; }
.quest .timeline-item:hover .timeline-index, .quest .timeline-item.active .timeline-index { transform: scale(1.06); box-shadow: 0 0 0 5px color-mix(in srgb, var(--accent) 8%, transparent); }
.quest .stage-head { animation: stageIn .55s cubic-bezier(.2,.8,.2,1) both; }
.quest .stage-track > i { transition: width .7s cubic-bezier(.2,.8,.2,1); }
.quest .content-card { transform-origin: 50% 50%; backface-visibility: hidden; }
.quest .content-card.is-current { z-index: 2; }
.quest .content-card.is-complete { border-color: color-mix(in srgb, var(--mi) 38%, var(--line)); }
.quest .content-card .block-type-icon { transition: transform .35s cubic-bezier(.2,.8,.2,1), color .3s ease, background .3s ease, box-shadow .3s ease; }
.quest .content-card.is-current .block-type-icon { transform: translateY(-2px) rotate(-4deg) scale(1.04); }
.quest .content-card.is-current .content { animation: contentFloatIn .65s cubic-bezier(.2,.8,.2,1) both; }
.quest .content-card .opts button, .quest .content-card .btn, .quest .content-card .checklist label { transition: transform .2s ease, box-shadow .25s ease, border-color .25s ease, background .25s ease; }
.quest .content-card .opts button:hover, .quest .content-card .btn:hover { transform: translateY(-2px); }
.quest .content-card .opts button:active, .quest .content-card .btn:active { transform: scale(.985); }
.quest .reward { animation: rewardArrival .42s cubic-bezier(.18,.9,.3,1.25) both; }
@keyframes heroLift { from { opacity: 0; transform: translateY(16px) scale(.99); filter: blur(7px); } to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); } }
@keyframes heroGleam { 0%,100% { background-position: center, 120% 0; } 50% { background-position: center, -20% 0; } }
@keyframes timelinePulse { 0%,100% { box-shadow: 0 10px 28px color-mix(in srgb, var(--accent) 8%, transparent); } 50% { box-shadow: 0 14px 38px color-mix(in srgb, var(--accent) 15%, transparent); } }
@keyframes stageIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes contentFloatIn { from { opacity: .55; transform: translateY(12px); filter: blur(2px); } to { opacity: 1; transform: translateY(0); filter: blur(0); } }
@keyframes rewardArrival { from { opacity: 0; transform: translateY(10px) scale(.92); } to { opacity: 1; transform: translateY(0) scale(1); } }
.quest.theme-light .topbar { box-shadow: 0 8px 28px rgba(32, 48, 80, .07); }
.quest.theme-light .hero { box-shadow: 0 24px 70px rgba(45, 60, 100, .10), inset 0 1px rgba(255,255,255,.9); }
@media (prefers-reduced-motion: reduce) {
  .quest .hero, .quest .hero::before, .quest .timeline-item.active, .quest .stage-head,
  .quest .reward, .quest .content-card.is-current .content,
  .quest .content-card.is-current .block-type-icon { animation: none !important; }
  .quest *, .quest *::before, .quest *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
}



/* Dopamine reading experience: polished motion, depth, and responsive focus */
.quest .topbar {
  -webkit-backdrop-filter: blur(22px) saturate(1.35);
  backdrop-filter: blur(22px) saturate(1.35);
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 16%, var(--line));
}
.quest .brand .gem {
  filter: drop-shadow(0 0 14px color-mix(in srgb, var(--accent) 35%, transparent));
  transition: transform .45s cubic-bezier(.2,.8,.2,1), filter .45s ease;
}
.quest .brand:hover .gem { transform: rotate(-12deg) scale(1.08); filter: drop-shadow(0 0 20px color-mix(in srgb, var(--accent) 48%, transparent)); }
.quest .hero {
  isolation: isolate;
  overflow: hidden;
  animation: dopHeroReveal .8s cubic-bezier(.16,1,.3,1) both;
}
.quest .hero::after {
  content: '';
  position: absolute;
  inset: -45% auto -45% -35%;
  width: 34%;
  pointer-events: none;
  background: linear-gradient(90deg, transparent, #ffffff18, transparent);
  transform: rotate(18deg) translateX(-220%);
  animation: dopHeroSweep 8s ease-in-out 1s infinite;
  z-index: -1;
}
.quest .hero-icon { animation: dopIconFloat 5s ease-in-out infinite; }
.quest .hero-card { transform: translateZ(0); transition: transform .45s cubic-bezier(.2,.8,.2,1), box-shadow .45s ease; }
.quest .hero-card:hover { transform: translateY(-5px) rotate(.5deg); }
.quest .timeline-wrap { position: relative; isolation: isolate; }
.quest .timeline-wrap::before {
  content: '';
  position: absolute;
  inset: 10px 0 auto;
  height: 1px;
  pointer-events: none;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--accent) 34%, transparent), transparent);
  opacity: .8;
}
.quest .timeline-item { will-change: transform; overflow: hidden; }
.quest .timeline-item::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  background: radial-gradient(circle at 90% 0%, color-mix(in srgb, var(--accent) 15%, transparent), transparent 52%);
  transition: opacity .35s ease;
}
.quest .timeline-item:hover::before, .quest .timeline-item.active::before { opacity: 1; }
.quest .timeline-index { position: relative; isolation: isolate; }
.quest .timeline-item.active .timeline-index::after {
  content: '';
  position: absolute;
  inset: -5px;
  border: 1px solid color-mix(in srgb, var(--accent) 48%, transparent);
  border-radius: inherit;
  animation: dopTimelineRing 2.4s ease-out infinite;
}
.quest .stage-head { position: relative; }
.quest .stage-title h2 { text-wrap: balance; }
.quest .stage-medal { box-shadow: 0 8px 28px color-mix(in srgb, var(--accent) 12%, transparent), inset 0 1px #ffffff18; }
.quest .stage-track { overflow: hidden; }
.quest .stage-track > i { position: relative; overflow: hidden; }
.quest .stage-track > i::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(100deg, transparent 10%, #ffffff60 48%, transparent 82%);
  transform: translateX(-100%);
  animation: dopProgressGleam 3.6s ease-in-out infinite;
}
.quest .stack { perspective: 1100px; }
.quest .content-card {
  isolation: isolate;
  overflow: hidden;
  transform-origin: center center;
  transition: opacity .48s ease, filter .48s ease, transform .55s cubic-bezier(.2,.8,.2,1), border-color .4s ease, box-shadow .45s ease, background .4s ease;
}
.quest .content-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  pointer-events: none;
  opacity: 0;
  background: linear-gradient(125deg, color-mix(in srgb, var(--block-tone, var(--accent)) 70%, transparent), transparent 32%, color-mix(in srgb, var(--block-tone, var(--accent)) 34%, transparent) 72%, transparent);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  transition: opacity .4s ease;
}
.quest .content-card.is-current::before { opacity: 1; }
.quest .content-card.is-current { box-shadow: 0 30px 90px #00000018, 0 0 0 1px color-mix(in srgb, var(--accent) 12%, transparent); }
.quest .content-card.is-current .block-nav-top { animation: dopCardIconIn .55s cubic-bezier(.2,.8,.2,1) both; }
.quest .content-card.is-current .content { animation: dopContentReveal .58s cubic-bezier(.16,1,.3,1) both; }
.quest .content-card.is-complete::after {
  content: '';
  position: absolute;
  inset: auto 12% 0;
  height: 2px;
  pointer-events: none;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--mi) 70%, transparent), transparent);
  opacity: .75;
}
.quest .content-card .block-type-icon { box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 10%, transparent); }
.quest .callout, .quest .formula, .quest .quote, .quest .boss, .quest .flash, .quest .unknown {
  transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s ease, border-color .3s ease;
}
.quest .callout:hover, .quest .formula:hover, .quest .quote:hover, .quest .boss:hover, .quest .unknown:hover { transform: translateY(-2px); box-shadow: 0 14px 32px #0000000c; }
.quest .opt { position: relative; overflow: hidden; }
.quest .opt::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(105deg, transparent 15%, #ffffff20 50%, transparent 85%);
  transform: translateX(-120%);
  transition: transform .65s ease;
}
.quest .opt:hover::after { transform: translateX(120%); }
.quest .btn.primary { box-shadow: 0 10px 26px color-mix(in srgb, var(--accent) 23%, transparent); transition: transform .22s ease, box-shadow .28s ease, filter .28s ease; }
.quest .btn.primary:hover { transform: translateY(-2px); box-shadow: 0 15px 34px color-mix(in srgb, var(--accent) 30%, transparent); filter: saturate(1.12); }
.quest button:focus-visible, .quest a:focus-visible { outline: 3px solid color-mix(in srgb, var(--accent) 68%, white); outline-offset: 4px; }
@keyframes dopHeroReveal { from { opacity: 0; transform: translateY(20px) scale(.985); filter: blur(8px); } to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); } }
@keyframes dopHeroSweep { 0%, 24% { transform: rotate(18deg) translateX(-220%); } 52%, 100% { transform: rotate(18deg) translateX(650%); } }
@keyframes dopIconFloat { 0%,100% { transform: translateY(0) rotate(0); } 50% { transform: translateY(-5px) rotate(2deg); } }
@keyframes dopTimelineRing { 0% { transform: scale(.86); opacity: .8; } 100% { transform: scale(1.28); opacity: 0; } }
@keyframes dopProgressGleam { 0%, 38% { transform: translateX(-110%); } 72%,100% { transform: translateX(110%); } }
@keyframes dopCardIconIn { from { opacity: .5; transform: translateY(8px) scale(.92) rotate(-6deg); } to { opacity: 1; transform: translateY(0) scale(1) rotate(0); } }
@keyframes dopContentReveal { from { opacity: .72; transform: translateY(14px) scale(.995); filter: blur(3px); } to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); } }
@media (max-width: 700px) {
  .quest .hero::after { display: none; }
  .quest .content-card.is-current { box-shadow: 0 18px 46px #00000012; }
}
@media (prefers-reduced-motion: reduce) {
  .quest .hero, .quest .hero::after, .quest .hero-icon, .quest .timeline-item.active .timeline-index::after,
  .quest .stage-track > i::after { animation: none !important; }
}
</style>