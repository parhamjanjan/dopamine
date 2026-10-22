<template>
  <div class="quest" dir="rtl">
    <div class="bg-stars"></div><div class="aurora a1"></div><div class="aurora a2"></div><div class="aurora a3"></div>
    <div class="confetti" aria-hidden="true"><i v-for="c in confetti" :key="c.id" :style="{ '--x': c.x, '--d': c.d + 's', '--t': c.t + 's', '--r': c.r + 'deg', '--c': c.c, width: c.s + 'px', height: c.s * 1.6 + 'px' }"></i></div>

    <header class="topbar">
      <RouterLink to="/notes" class="brand"><span class="gem">✦</span><span><b>DOPAMINE</b><small>آکادمی ماجراجویی</small></span></RouterLink>
      <div class="top-actions">
        <button class="icon" :disabled="bookmarkBusy" @click="toggleBookmark" :title="bookmarked ? 'حذف از ذخیره‌شده‌ها' : 'ذخیرهٔ جزوه'">{{ bookmarked ? '♥' : '♡' }}</button>
        <button class="icon" @click="printNote" title="چاپ یا PDF">⤓</button>
        <RouterLink v-if="isAdmin" :to="`/notes/admin/${noteId}/edit`" class="icon" title="ویرایش جزوه">⚙</RouterLink>
      </div>
      <div class="top-progress"><i :style="{ width: progressPercent + '%' }"></i></div>
    </header>

    <div v-if="loading" class="state"><div class="portal"><span></span></div><b>در حال ساخت دنیای یادگیری…</b></div>
    <div v-else-if="error" class="state"><div class="err-gem">!</div><h2>این جزوه باز نشد</h2><p>{{ error }}</p><RouterLink to="/notes" class="btn primary">بازگشت به کتابخانه</RouterLink></div>

    <main v-else class="world">
      <!-- Hero -->
      <section class="hero" :style="{ '--cover': safeCoverColor }">
        <div class="hero-icon">{{ note.cover_icon || '📘' }}</div>
        <div class="hero-copy">
          <div class="meta">{{ note.subject || 'درس آموزشی' }} · {{ note.grade || 'همهٔ پایه‌ها' }}</div>
          <h1>{{ note.title || 'ماجراجویی یادگیری' }}</h1>
          <p>{{ note.subtitle || 'هر مرحله یک قدرت تازه؛ هر قدم یک پیروزی.' }}</p>
          <div class="chips"><span>◷ {{ note.estimated_minutes || 10 }} دقیقه</span><span>◉ {{ note.view_count || 0 }} بازدید</span><span>⚑ {{ stages.length }} مرحله</span></div>
        </div>
        <div class="hero-card">
          <div class="ring" :style="{ '--p': progressPercent }"><b>{{ progressPercent }}%</b></div>
          <div class="hero-card-text">
            <small>{{ progressPercent === 100 ? 'همه‌چیز کامل شد' : 'ادامهٔ مسیر' }}</small>
            <b>{{ progressPercent === 100 ? 'افسانه شدی! 🏆' : (nextStage?.title || 'شروع کن') }}</b>
            <span>{{ completedCount }} از {{ totalBlocks }} بخش انجام شده</span>
          </div>
          <button class="btn primary" @click="continueQuest">{{ completedCount ? (progressPercent === 100 ? 'مرور دوباره' : 'ادامه بده') : 'شروع ماجراجویی' }}</button>
        </div>
      </section>

      <!-- Responsive learning timeline -->
      <section v-if="stages.length" class="timeline-wrap">
        <div class="timeline-heading">
          <div><span class="timeline-kicker">LEARNING PATH</span><h2>مسیر یادگیری</h2></div>
          <span class="timeline-count">{{ completedStages }} از {{ stages.length }} مرحله تکمیل شده</span>
        </div>
        <div class="timeline">
          <button v-for="(stage, i) in stages" :key="stage.id" type="button"
            class="timeline-item" :class="{ active: activeStageIndex === i, done: isStageDone(stage) }"
            @click="selectStage(i)" :aria-current="activeStageIndex === i ? 'step' : undefined">
            <span class="timeline-index">{{ isStageDone(stage) ? '✓' : String(i + 1).padStart(2, '0') }}</span>
            <span class="timeline-copy">
              <small>مرحلهٔ {{ String(i + 1).padStart(2, '0') }}</small>
              <strong>{{ stage.title }}</strong>
              <span>{{ stage.description }}</span>
            </span>
            <span class="timeline-status">{{ isStageDone(stage) ? 'تکمیل‌شده' : activeStageIndex === i ? 'در حال مطالعه' : 'مشاهدهٔ مرحله' }}</span>
            <span class="timeline-arrow" aria-hidden="true">←</span>
          </button>
        </div>
      </section>

      <!-- Study zone -->
      <section v-if="activeStage" class="study">
        <div class="stage-head">
          <div class="stage-title">
            <small>مرحلهٔ {{ activeStageIndex + 1 }} از {{ stages.length }}</small>
            <h2>{{ activeStage.title }}</h2>
            <p>{{ activeStage.description }}</p>
          </div>
          <div class="stage-medal" :class="{ won: isStageDone(activeStage) }">{{ isStageDone(activeStage) ? '🏆' : '⚔️' }}</div>
        </div>
        <div class="stage-track"><i :style="{ width: stagePercent(activeStage) + '%' }"></i><span>{{ stagePercent(activeStage) }}%</span></div>

        <TransitionGroup name="card" tag="div" class="stack card">
          <article v-for="entry in activeStage.blocks" :key="entry.index" :id="`blk-${entry.index}`" class="">
            <div class="content">
              <h2 v-if="entry.block.type === 'heading'" class="c-heading" :class="`lv${entry.block.level || 2}`">{{ entry.block.text || entry.block.title }}</h2>
              <p v-else-if="entry.block.type === 'paragraph'" class="c-para" v-html="rich(entry.block.text)"></p>
              <ul v-else-if="entry.block.type === 'list'" class="c-list"><li v-for="(l, i) in listItems(entry.block)" :key="i"><span>✦</span><div v-html="rich(l)"></div></li></ul>

              <div v-else-if="entry.block.type === 'callout'" class="callout" :data-style="entry.block.style || 'tip'" :style="calloutStyle(entry.block)">
                <div class="callout-in">
                  <div class="callout-head"><span class="callout-icon">{{ entry.block.icon || styleIcon(entry.block.style) }}</span>
                    <div><small>{{ styleKind(entry.block.style) }}</small><b>{{ entry.block.title || styleTitle(entry.block.style) }}</b></div></div>
                  <p v-html="rich(entry.block.text)"></p>
                </div>
              </div>

              <div v-else-if="entry.block.type === 'formula'" class="formula"><small>گنجینهٔ فرمول</small><p>{{ entry.block.text }}</p></div>
              <blockquote v-else-if="entry.block.type === 'quote'" class="quote">{{ entry.block.text }}</blockquote>
              <div v-else-if="entry.block.type === 'divider'" class="rune"><i></i><span>✦</span><i></i></div>

              <div v-else-if="entry.block.type === 'flashcard'" class="flash" :class="{ on:flipped.has(entry.index) }" @click="flip(entry.index)" tabindex="0" role="button" @keydown.enter.prevent="flip(entry.index)" @keydown.space.prevent="flip(entry.index)">
                <div class="flash-in">
                  <div class="face"><small>فلش‌کارت · فکر کن، بعد بزن</small><b>{{ entry.block.front }}</b></div>
                  <div class="face back"><small>پاسخ</small><b>{{ entry.block.back }}</b></div>
                </div>
              </div>

              <div v-else-if="entry.block.type === 'quiz'" class="boss">
                <div class="boss-head"><span>☠</span><div><small>چالش دانشی</small><b>مینی‌باس</b></div><em v-if="quizTries[entry.index]">{{ quizTries[entry.index] }} تلاش</em></div>
                <h3>{{ entry.block.question || 'پاسخ درست را انتخاب کن' }}</h3>
                <div class="opts">
                  <button v-for="(o, i) in (entry.block.options || [])" :key="i" class="opt" :disabled="quizSolved(entry)"
                          :class="{ correct: quizAnswers[entry.index] === i && i === Number(entry.block.answer), wrong: quizAnswers[entry.index] === i && i !== Number(entry.block.answer), reveal: quizSolved(entry) && i === Number(entry.block.answer) }"
                          @click="answerQuiz(entry, i)">
                    <span class="letter">{{ letters[i] }}</span><span class="txt">{{ o }}</span>
                    <span class="res">{{ quizAnswers[entry.index] === i ? (i === Number(entry.block.answer) ? '✓' : '×') : '' }}</span>
                  </button>
                </div>
                <Transition name="fade">
                  <div v-if="quizAnswers[entry.index] !== undefined" class="feedback" :class="{ ok: quizSolved(entry) }">
                    <b>{{ quizSolved(entry) ? 'آفرین! باس شکست خورد.' : 'نه این‌یکی؛ دوباره فکر کن.' }}</b>
                    <p v-if="quizSolved(entry) && entry.block.explanation" v-html="rich(entry.block.explanation)"></p>
                  </div>
                </Transition>
              </div>

              <figure v-else-if="entry.block.type === 'image'" class="img">
                <img v-if="entry.block.url" :src="entry.block.url" :alt="entry.block.caption || 'تصویر آموزشی'" loading="lazy" @error="hideBroken" />
                <figcaption v-if="entry.block.caption">{{ entry.block.caption }}</figcaption>
                <div v-if="!entry.block.url" class="img-ph">▧ تصویر آموزشی</div>
              </figure>

              <div v-else-if="entry.block.type === 'checklist'" class="checklist">
                <label v-for="(item, i) in listItems(entry.block)" :key="i" :class="{ on: checks[`${entry.index}-${i}`] }">
                  <input v-model="checks[`${entry.index}-${i}`]" type="checkbox" @change="onCheck(entry)" /><span class="box">✓</span><span>{{ item }}</span>
                </label>
              </div>

              <div v-else class="unknown"><b>{{ entry.block.title || 'بخش آموزشی' }}</b><p>{{ entry.block.text }}</p></div>
            </div>
          </article>
        </TransitionGroup>

        <div v-if="!activeStage.blocks.length" class="empty"><h3>این مرحله هنوز خالی است</h3><p>از نقشه یک مرحلهٔ دیگر انتخاب کن.</p></div>

        <div class="finish" :class="{ won: isStageDone(activeStage) }">
          <div class="finish-emblem">{{ isStageDone(activeStage) ? '🏆' : '🗝️' }}</div>
          <div class="finish-text">
            <b>{{ isStageDone(activeStage) ? 'مرحله را فتح کردی!' : 'آمادهٔ فتح این مرحله‌ای؟' }}</b>
            <p>{{ isStageDone(activeStage) ? 'می‌توانی مرور کنی یا به مرحلهٔ بعد بروی.' : 'همهٔ بخش‌ها را تیک بزن تا نشان مرحله را بگیری.' }}</p>
          </div>
          <div class="finish-actions">
            <button v-if="isStageDone(activeStage)" class="btn quiet" @click="completeStage">لغو تکمیل</button>
            <button class="btn primary" @click="goNextStage">{{ activeStageIndex < stages.length - 1 ? 'مرحلهٔ بعدی' : 'شروع دوباره' }}</button>
          </div>
        </div>
      </section>
    </main>

    <Transition name="reward"><div v-if="rewardToast" class="reward"><span>✦</span><b>{{ rewardToast }}</b></div></Transition>
    <footer class="foot">یاد بگیر · سطح بگیر · تکرار کن</footer>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { notesApi } from '../services/notes'

const route = useRoute(), auth = useAuthStore()
const noteId = computed(() => route.params.id)
const isAdmin = computed(() => Boolean(auth.user?.is_staff || auth.user?.is_superuser))

const note = ref({ blocks: [] })
const loading = ref(true), error = ref('')
const bookmarked = ref(false), bookmarkBusy = ref(false)
const completed = ref([]), currentBlock = ref(0), activeStageIndex = ref(0)
const quizAnswers = ref({}), quizTries = reactive({}), checks = ref({}), flipped = reactive(new Set())
const rewardToast = ref(''), confetti = ref([])
let toastTimer = null, ready = false
const letters = ['A', 'B', 'C', 'D', 'E', 'F']

/* ───────── derived data ───────── */
const safeCoverColor = computed(() => /^#[0-9a-f]{6}$/i.test(note.value.cover_color || '') ? note.value.cover_color : '#7055e8')
const allBlocks = computed(() => Array.isArray(note.value.blocks) ? note.value.blocks : [])
const stages = computed(() => {
  const blocks = allBlocks.value.map((block, index) => ({ block: block || {}, index }))
  if (!blocks.length) return []
  const groups = []
  if (blocks.some(e => e.block.type === 'heading')) {
    let cur = null
    for (const e of blocks) {
      if (e.block.type === 'heading') {
        cur = { id: `s-${e.index}`, title: String(e.block.text || e.block.title || `مرحلهٔ ${groups.length + 1}`).trim(), description: 'این بخش را بخوان و نکته‌های مهمش را به خاطر بسپار.', blocks: [] }
        groups.push(cur)
      } else if (!cur) {
        cur = { id: 's-intro', title: 'شروع ماجراجویی', description: 'پیش‌درآمد مسیر یادگیری.', blocks: [] }
        groups.push(cur)
      }
      cur.blocks.push(e)
    }
    return groups
  }
  for (let i = 0; i < blocks.length; i += 4) groups.push({ id: `s-${i}`, title: i === 0 ? 'شروع ماجراجویی' : `مرحلهٔ ${groups.length + 1}`, description: 'چند قدم کوچک برای پیشروی.', blocks: blocks.slice(i, i + 4) })
  return groups
})
const activeStage = computed(() => stages.value[activeStageIndex.value] || null)
const nextStage = computed(() => stages.value.find(s => !isStageDone(s)) || null)
const totalBlocks = computed(() => allBlocks.value.length)
const completedCount = computed(() => new Set(completed.value.filter(i => Number.isInteger(i) && i >= 0 && i < totalBlocks.value)).size)
const progressPercent = computed(() => totalBlocks.value ? Math.round(completedCount.value / totalBlocks.value * 100) : 0)
const completedStages = computed(() => stages.value.filter(isStageDone).length)

/* ───────── helpers ───────── */
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const rich = t => esc(t).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/==(.+?)==/g, '<mark>$1</mark>').replace(/`(.+?)`/g, '<code>$1</code>').replace(/\n/g, '<br>')
const isCompleted = i => completed.value.includes(i)
const isStageDone = s => Boolean(s?.blocks?.length) && s.blocks.every(e => isCompleted(e.index))
const stagePercent = s => s?.blocks?.length ? Math.round(s.blocks.filter(e => isCompleted(e.index)).length / s.blocks.length * 100) : 0
function listItems(b) {
  if (Array.isArray(b.items)) return b.items.map(String).filter(x => x.trim())
  return String(b.text || '').split('\n').map(x => x.trim()).filter(Boolean)
}
const styleIcon = s => ({ tip: '💡', definition: '◈', warning: '⚠️', trap: '🎯', example: '✦', summary: '✓', exam: '🧠', custom: '✧' })[s] || '✧'
const styleTitle = s => ({ tip: 'نکتهٔ مهم', definition: 'تعریف', warning: 'هشدار', trap: 'دام تستی', example: 'مثال', summary: 'خلاصه', exam: 'نکتهٔ امتحانی', custom: 'توجه' })[s] || 'توجه'
const styleKind = s => ({ warning: 'هشدار', trap: 'دام تستی', definition: 'تعریف', example: 'مثال', summary: 'جمع‌بندی', exam: 'نکتهٔ امتحانی' })[s] || 'نکتهٔ ویژه'
const calloutStyle = b => b.customColor && b.style === 'custom' && /^#[0-9a-f]{6}$/i.test(b.customColor) ? { '--c': b.customColor } : {}
const hideBroken = e => { if (e?.target) e.target.style.display = 'none' }
function flip(id){ flipped.has(id) ? flipped.delete(id) : flipped.add(id) }
const printNote = () => window.print()

function showReward(msg) {
  rewardToast.value = msg
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { rewardToast.value = '' }, 2600)
}
function burst() {
  const colors = ['#5be7ff', '#8f7bff', '#ffcf5a', '#ff5c82', '#4df0c0', '#ffffff']
  confetti.value = Array.from({ length: 46 }, (_, i) => ({ id: `${Date.now()}-${i}`, x: Math.random() * 100, d: +(Math.random() * .5).toFixed(2), t: +(1.5 + Math.random() * 1.2).toFixed(2), r: Math.round(Math.random() * 360), c: colors[i % colors.length], s: 5 + Math.round(Math.random() * 6) }))
  setTimeout(() => { confetti.value = [] }, 3200)
}

/* ───────── actions ───────── */
function selectStage(i, scroll = true) {
  if (i < 0 || i >= stages.value.length) return
  activeStageIndex.value = i
  const first = stages.value[i]?.blocks?.[0]; if (first) currentBlock.value = first.index
  persistProgress()
  if (scroll) nextTick(() => document.querySelector('.study')?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
}
async function goNextStage() {
  const stage = activeStage.value
  if (!stage) return

  // تمام بلوک‌های مرحلهٔ فعلی را تکمیل کن
  const blockIds = stage.blocks.map(block => block.index)

  completed.value = [
    ...new Set([...completed.value, ...blockIds])
  ].sort((a, b) => a - b)

  // ذخیرهٔ پیشرفت و نمایش انیمیشن موفقیت
  await persistProgress()
  burst()
  showReward('همهٔ بخش‌های این مرحله تکمیل شدند!')

  // رفتن به مرحلهٔ بعدی
  if (activeStageIndex.value < stages.value.length - 1) {
    selectStage(activeStageIndex.value + 1)
  } else {
    showReward('تبریک! همهٔ مراحل را پشت سر گذاشتی! 🏆')
  }
}function continueQuest() {
  const i = stages.value.findIndex(s => !isStageDone(s))
  selectStage(i === -1 ? 0 : i)
}
function setCompleted(index, on) {
  const has = isCompleted(index)
  if (on && !has) completed.value = [...completed.value, index].sort((a, b) => a - b)
  if (!on && has) completed.value = completed.value.filter(x => x !== index)
}
function afterStageChange(wasDone) {
  if (!wasDone && isStageDone(activeStage.value)) { burst(); showReward('مرحله با موفقیت تکمیل شد!') }
}
function toggleCompleted(index) {
  const wasDone = isStageDone(activeStage.value)
  const on = !isCompleted(index)
  setCompleted(index, on); currentBlock.value = index
  if (on) { showReward('بخش تکمیل شد.'); afterStageChange(wasDone) }
  persistProgress()
}
function completeStage() {
  const s = activeStage.value; if (!s) return
  const ids = s.blocks.map(e => e.index)
  if (isStageDone(s)) { completed.value = completed.value.filter(i => !ids.includes(i)); showReward('تکمیل مرحله لغو شد.') }
  else { completed.value = [...new Set([...completed.value, ...ids])].sort((a, b) => a - b); burst(); showReward('مرحله با موفقیت تکمیل شد!') }
  persistProgress()
}
const quizSolved = e => quizAnswers.value[e.index] !== undefined && quizAnswers.value[e.index] === Number(e.block.answer)
function answerQuiz(e, choice) {
  if (quizSolved(e)) return
  quizAnswers.value = { ...quizAnswers.value, [e.index]: choice }
  quizTries[e.index] = (quizTries[e.index] || 0) + 1
  if (choice === Number(e.block.answer)) {
    const wasDone = isStageDone(activeStage.value)
    if (!isCompleted(e.index)) { setCompleted(e.index, true); persistProgress() }
    showReward(quizTries[e.index] === 1 ? 'پاسخ درست بود!' : 'درست شد!')
    afterStageChange(wasDone)
  } else {
    // allow retry: clear the wrong pick after the shake
    setTimeout(() => { if (quizAnswers.value[e.index] === choice && !quizSolved(e)) { const { [e.index]: _, ...rest } = quizAnswers.value; quizAnswers.value = rest } }, 1100)
  }
}
function onCheck(e) {
  const items = listItems(e.block)
  if (items.length && items.every((_, i) => checks.value[`${e.index}-${i}`]) && !isCompleted(e.index)) {
    const wasDone = isStageDone(activeStage.value)
    setCompleted(e.index, true); showReward('چک‌لیست کامل شد!'); persistProgress(); afterStageChange(wasDone)
  }
}

/* ───────── persistence ───────── */
async function persistProgress() {
  if (!auth.isAuthenticated || !note.value.id) return
  try { await notesApi.saveProgress(note.value.id, { completed_blocks: completed.value, last_block: currentBlock.value, percent: progressPercent.value }) }
  catch (err) { console.warn('Progress save failed', err) }
}
async function load() {
  loading.value = true; error.value = ''; completed.value = []; ready = false
  quizAnswers.value = {}; checks.value = {}; for (const k of Object.keys(flipped)) delete flipped[k]
  try {
    const res = await notesApi.get(noteId.value)
    note.value = res.data || { blocks: [] }
    bookmarked.value = Boolean(note.value.is_bookmarked)
    if (auth.isAuthenticated) {
      try {
        const p = (await notesApi.getProgress(noteId.value)).data || {}
        const len = (note.value.blocks || []).length
        completed.value = [...new Set((Array.isArray(p.completed_blocks) ? p.completed_blocks : []).filter(i => Number.isInteger(i) && i >= 0 && i < len))]
        currentBlock.value = Math.min(Math.max(Number(p.last_block) || 0, 0), Math.max(len - 1, 0))
      } catch { /* مطالعه بدون حساب هم ممکن است */ }
    }
    const si = stages.value.findIndex(s => s.blocks.some(e => e.index === currentBlock.value))
    activeStageIndex.value = si >= 0 ? si : 0
  } catch (err) {
    error.value = err.response?.data?.detail || 'جزوه پیدا نشد یا هنوز منتشر نشده است.'
  } finally {
    loading.value = false
    await nextTick(); ready = true
  }
}
async function toggleBookmark() {
  if (bookmarkBusy.value) return
  bookmarkBusy.value = true
  try {
    const res = await notesApi.bookmark(note.value.id)
    bookmarked.value = Boolean(res.data?.bookmarked)
    showReward(bookmarked.value ? 'به ذخیره‌شده‌ها اضافه شد.' : 'از ذخیره‌شده‌ها حذف شد.')
  } catch { showReward('برای ذخیرهٔ جزوه باید وارد حساب شوی.') }
  finally { bookmarkBusy.value = false }
}


watch(noteId, load)
watch(progressPercent, (n, o) => { if (ready && n === 100 && o < 100) { burst(); showReward('مطالعهٔ جزوه را به پایان رساندی!') } })
onMounted(load)
onBeforeUnmount(() => clearTimeout(toastTimer))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap');
@property --ang { syntax: '<angle>'; initial-value: 0deg; inherits: false; }

:global(*) { box-sizing: border-box }
:global(body) { margin: 0; background: #070b1d; font-family: 'Vazirmatn', Tahoma, sans-serif }

.quest {
  --bg: #070b1d; --card: #0f1830; --card2: #15213f; --line: #27375f; --txt: #eef3ff; --mut: #8fa2cf;
  --cy: #5be7ff; --vi: #8f7bff; --am: #ffcf5a; --co: #ff5c82; --mi: #4df0c0;
  position: relative; min-height: 100vh; overflow-x: hidden; color: var(--txt); font-family: 'Vazirmatn', Tahoma, sans-serif; isolation: isolate;
  background: radial-gradient(ellipse at 50% -10%, #223468 0, transparent 46%), var(--bg)
}
.bg-stars { position: absolute; inset: 0; z-index: -1; opacity: .26; pointer-events: none; background-image: radial-gradient(#8adfff 1px, transparent 1px), radial-gradient(#b7a0ff 1px, transparent 1px); background-size: 73px 73px, 131px 131px; background-position: 0 0, 31px 44px; animation: drift 100s linear infinite }
.aurora { position: absolute; z-index: -1; width: 480px; height: 480px; border-radius: 50%; filter: blur(110px); opacity: .17; pointer-events: none; animation: float 14s ease-in-out infinite alternate }
.a1 { background: #4b76ff; top: 260px; left: -220px } .a2 { background: #b04aff; top: 900px; right: -220px; animation-delay: -5s } .a3 { background: #00e0c0; top: 1500px; left: 30%; animation-delay: -9s }
button { font-family: inherit } :focus-visible { outline: 2px solid var(--cy); outline-offset: 2px }

/* topbar */
.topbar { position: sticky; top: 0; z-index: 30; display: flex; align-items: center; gap: 16px; height: 68px; padding: 0 clamp(14px, 3.5vw, 56px); background: #0a1228d9; backdrop-filter: blur(18px); border-bottom: 1px solid var(--line) }
.brand { display: flex; align-items: center; gap: 10px; color: inherit; text-decoration: none; margin-left: auto }
.gem { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 12px; font-size: 22px; color: #0a1330; background: linear-gradient(145deg, #a6efff, #7a82ff); box-shadow: 0 0 24px #5ec3ff55; animation: bob 4s ease-in-out infinite }
.brand b { display: block; font-size: 12px; letter-spacing: 1.5px } .brand small { color: var(--mut); font-size: 10px }

.top-actions { display: flex; gap: 8px }
.icon { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 12px; border: 1px solid #34466f; background: #17213e; color: #c9d7ff; font-size: 18px; cursor: pointer; text-decoration: none; transition: .22s }
.icon:hover { transform: translateY(-3px) rotate(-4deg); border-color: #7d91ff; color: #fff } .icon:disabled { opacity: .5 }
.top-progress { position: absolute; inset: auto 0 -1px 0; height: 2px; background: transparent } .top-progress i { display: block; height: 100%; margin-right: 0; margin-left: auto; background: linear-gradient(270deg, var(--cy), var(--vi), var(--am)); box-shadow: 0 0 10px var(--cy); transition: width .6s }

.btn { display: inline-flex; align-items: center; justify-content: center; padding: 10px 16px; border-radius: 12px; font-size: 12px; font-weight: 800; cursor: pointer; text-decoration: none; white-space: nowrap; border: 1px solid transparent; transition: transform .2s, box-shadow .2s }
.btn:hover { transform: translateY(-2px) }
.btn.quiet { background: #172342; color: #c4d2f8; border-color: #3f527e }
.btn.primary { position: relative; overflow: hidden; color: #fff; border-color: #aaa5ff; background: linear-gradient(105deg, #5f7bff, #a06bff); box-shadow: 0 6px 22px #7770ff40 }
.btn.primary::after { content: ''; position: absolute; inset: 0; background: linear-gradient(105deg, transparent 35%, #ffffff40 50%, transparent 65%); transform: translateX(120%); animation: shine 4.5s ease-in-out infinite }

.world { max-width: 1100px; margin: auto; padding: 26px clamp(14px, 3vw, 40px) 30px; display: grid; gap: 22px }

/* hero */
.hero { --cover: #7055e8; position: relative; overflow: hidden; display: grid; grid-template-columns: auto 1fr; gap: 24px; align-items: center; padding: 34px; border-radius: 28px; border: 1px solid #ffffff2a; background: radial-gradient(ellipse at 85% 0, #ffffff26, transparent 45%), linear-gradient(120deg, color-mix(in srgb, var(--cover) 60%, #0d1530), color-mix(in srgb, var(--cover) 22%, #101a3a) 75%); box-shadow: 0 30px 80px #0005, inset 0 1px #ffffff30; isolation: isolate }
.hero::before { content: ''; position: absolute; z-index: -1; width: 520px; height: 520px; border: 1px solid #ffffff18; border-radius: 50%; left: -160px; bottom: -330px }
.hero-icon { width: 92px; height: 92px; display: grid; place-items: center; font-size: 46px; border-radius: 28px; background: linear-gradient(145deg, #ffffff48, #ffffff14); border: 1px solid #ffffff5a; box-shadow: 0 16px 38px #0006, inset 0 2px #ffffff80; backdrop-filter: blur(10px); animation: bob 5s ease-in-out infinite }
.meta { font-size: 12px; color: #d9e8ff; margin-bottom: 6px } .hero h1 { margin: 0; font-size: clamp(24px, 3.2vw, 40px); line-height: 1.5; font-weight: 900; text-shadow: 0 3px 20px #0006 }
.hero-copy p { margin: 8px 0 0; font-size: 13px; line-height: 2; color: #d3e0fa; max-width: 60ch }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px } .chips span { padding: 6px 11px; border-radius: 10px; font-size: 11px; border: 1px solid #ffffff22; background: #07152e66 }
.hero-card { grid-column: 1 / -1; display: flex; align-items: center; gap: 16px; padding: 14px 18px; border-radius: 18px; border: 1px solid #ffffff2e; background: #07152e8c; backdrop-filter: blur(12px) }
.ring { --p: 0; width: 58px; height: 58px; flex-shrink: 0; display: grid; place-items: center; border-radius: 50%; background: radial-gradient(#0c1730 57%, transparent 59%), conic-gradient(var(--cy) calc(var(--p) * 1%), #ffffff1c 0); transition: .6s } .ring b { font-size: 12px }
.hero-card-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px } .hero-card-text small { font-size: 10px; color: var(--cy) } .hero-card-text b { font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap } .hero-card-text span { font-size: 11px; color: #a8b9e0 }

/* Responsive learning timeline */
.timeline-wrap { overflow:hidden; padding:22px; border:1px solid var(--line); border-radius:24px; background:linear-gradient(145deg,#131e3eee,#0c1530ee); }
.timeline-heading { display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:20px; }
.timeline-heading h2 { margin:3px 0 0; font-size:20px; font-weight:900; }
.timeline-kicker { color:var(--cy); font-size:9px; letter-spacing:2px; font-weight:800; }
.timeline-count { color:var(--mut); font-size:11px; }
.timeline { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,245px),1fr)); gap:12px; }
.timeline-item { position:relative; display:flex; align-items:center; gap:12px; min-width:0; width:100%; min-height:100px; padding:15px; text-align:right; font:inherit; color:var(--txt); cursor:pointer; border:1px solid #2b3b62; border-radius:17px; background:linear-gradient(145deg,#172442,#101a32); transition:transform .22s,border-color .22s,background .22s,box-shadow .22s; }
.timeline-item:hover { transform:translateY(-3px); border-color:#6478b5; }
.timeline-index { display:grid; place-items:center; flex:0 0 43px; width:43px; height:43px; border-radius:13px; border:1px solid #455783; color:#c8d6ff; background:linear-gradient(145deg,#2b3c67,#192544); font-size:13px; font-weight:900; }
.timeline-copy { display:flex; flex:1; flex-direction:column; gap:4px; min-width:0; }
.timeline-copy small { color:var(--cy); font-size:10px; }
.timeline-copy strong { font-size:13px; line-height:1.8; overflow-wrap:anywhere; }
.timeline-copy > span { color:var(--mut); font-size:10px; line-height:1.8; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.timeline-status { position:absolute; left:13px; bottom:10px; font-size:9px; color:#8fa2cf; }
.timeline-arrow { position:absolute; left:12px; top:12px; color:#7185b6; font-size:15px; opacity:.75; }
.timeline-item.active { border-color:#6cdeff; background:linear-gradient(145deg,#203b60,#20234d); box-shadow:0 0 0 1px #5be7ff20,0 10px 30px #0002; }
.timeline-item.active .timeline-index { color:#fff; border-color:#8beaff; background:linear-gradient(145deg,#35bfe8,#7969f7); box-shadow:0 0 20px #5be7ff35; }
.timeline-item.active .timeline-status { color:var(--cy); }
.timeline-item.done { border-color:#357b78; }
.timeline-item.done .timeline-index { color:#06241f; border-color:#a2ffe6; background:linear-gradient(145deg,#8bffda,#39c5b5); }
.timeline-item.done .timeline-status { color:#75e7c9; }

/* study */
.study { display: grid; gap: 14px }
.stage-head { display: flex; align-items: center; justify-content: space-between; gap: 18px; padding: 6px 4px 0 } .stage-title small { font-size: 11px; color: var(--cy) } .stage-title h2 { margin: 4px 0 5px; font-size: clamp(21px, 2.4vw, 28px); font-weight: 900 } .stage-title p { margin: 0; font-size: 12px; color: var(--mut) }
.stage-medal { width: 64px; height: 64px; flex-shrink: 0; display: grid; place-items: center; font-size: 28px; border-radius: 20px; border: 1px solid #4a5583; background: linear-gradient(145deg, #2b315d, #171d3b); transform: rotate(3deg); transition: .4s } .stage-medal.won { border-color: #e4b85d; box-shadow: 0 0 26px #ffcb5544; animation: pop .6s cubic-bezier(.2, 1.6, .4, 1) }
.stage-track { position: relative; height: 8px; border-radius: 9px; background: #060b1c; border: 1px solid #28385f; margin: 4px 0 6px } .stage-track i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--cy), var(--vi), #c07aff); box-shadow: 0 0 14px #6d7cff; transition: width .6s } .stage-track span { position: absolute; top: 12px; left: 0; font-size: 10px; color: var(--mut) }

.stack { display: grid; gap: 14px; margin-top: 12px }
.card {  padding: 18px 18px 18px 22px; border: 1px solid #2c3c63; border-radius: 20px; background: linear-gradient(145deg, #172342f5, #101a34f8); box-shadow: 0 14px 34px #0002; transition: border-color .3s, background .3s }
.card.done { border-color: #2a7a74aa; background: linear-gradient(145deg, #12303a, #101a34) }
.card.t-heading { background: transparent; border-color: transparent; box-shadow: none; padding-top: 4px; padding-bottom: 0 }
.check { width: 44px; display: grid; justify-items: center; align-content: start; gap: 4px; border: 0; background: none; cursor: pointer; padding: 0; color: var(--mut) }
.check span { width: 32px; height: 32px; display: grid; place-items: center; border-radius: 11px; border: 2px solid #43588c; background: #0b142b; color: #052b25; font-weight: 900; transition: .3s cubic-bezier(.2, 1.6, .4, 1) }
.check small { font-size: 9px; color: var(--am); transition: .2s } .check:hover span { border-color: var(--cy); transform: scale(1.08) }
.check.on span { background: linear-gradient(145deg, #8bffda, #39c5b5); border-color: #a2ffe6; box-shadow: 0 0 18px #4df0c066; transform: scale(1.06) } .check.on small { opacity: 0 }
.content { min-width: 0 }
.c-heading { margin: 0; font-size: 22px; line-height: 1.8; font-weight: 900 } .c-heading.lv1 { font-size: 27px } .c-heading.lv3 { font-size: 17px }
.c-para { margin: 0; font-size: 15px; line-height: 2.3; color: #d3def8 }
.c-para :deep(mark), .callout p :deep(mark), .c-list :deep(mark) { background: #ffd25c30; color: #ffe9a6; padding: 0 5px; border-radius: 6px }
.c-para :deep(code), .callout p :deep(code), .c-list :deep(code), .feedback :deep(code) { direction: ltr; unicode-bidi: embed; background: #1d2850; color: #9fe7ff; padding: 1px 7px; border-radius: 7px; font-size: .92em }
.c-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px } .c-list li { display: flex; gap: 10px; line-height: 2.1; font-size: 14px; color: #d3def8 } .c-list li > span { color: var(--cy); margin-top: 1px }

.callout { --c: #8f7bff; border-radius: 17px; padding: 1.5px; background: conic-gradient(from var(--ang), color-mix(in srgb, var(--c) 30%, transparent) 55%, var(--c) 78%, color-mix(in srgb, var(--c) 30%, transparent)); animation: spinAng 4s linear infinite; box-shadow: 0 0 28px color-mix(in srgb, var(--c) 16%, transparent) }
.callout[data-style=definition] { --c: #19c5b2 } .callout[data-style=warning] { --c: #ffd34f } .callout[data-style=trap] { --c: #ff456a } .callout[data-style=example] { --c: #4b8dff } .callout[data-style=summary] { --c: #3ddc84 } .callout[data-style=exam] { --c: #b07cff }
.callout-in { border-radius: 16px; padding: 16px 18px; background: linear-gradient(120deg, color-mix(in srgb, var(--c) 10%, #111a35), #111a35) }
.callout-head { display: flex; align-items: center; gap: 12px } .callout-icon { width: 40px; height: 40px; display: grid; place-items: center; border-radius: 13px; font-size: 20px; background: color-mix(in srgb, var(--c) 18%, #121b35); border: 1px solid color-mix(in srgb, var(--c) 55%, transparent) }
.callout-head small { display: block; font-size: 10px; font-weight: 700; color: var(--c) } .callout-head b { font-size: 14px }
.callout p { margin: 12px 0 0; font-size: 13px; line-height: 2.2; color: #d9deef }

.formula { padding: 20px; text-align: center; border-radius: 16px; border: 1px solid #4a74a7; background: linear-gradient(130deg, #102c48, #25204e) } .formula small { font-size: 10px; color: var(--cy); font-weight: 700 } .formula p { margin: 4px 0 0; font-size: 23px; font-weight: 800; color: #e6faff; line-height: 2; white-space: pre-wrap; direction: ltr }
.quote { margin: 0; padding: 16px 20px; border-right: 3px solid #a18bff; border-radius: 0 13px 13px 0; background: #242044; color: #e6deff; font-size: 15px; line-height: 2.2 } .quote::before { content: '“'; margin-left: 4px } .quote::after { content: '”'; margin-right: 4px }
.rune { display: flex; align-items: center; gap: 13px; color: var(--cy) } .rune i { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #5d76b4, transparent) }

.flash { perspective: 900px; cursor: pointer; height: 150px } .flash-in { position: relative; height: 100%; transition: transform .6s cubic-bezier(.3, 1.2, .4, 1); transform-style: preserve-3d } .flash.on .flash-in { transform: rotateY(180deg) }

.face { position: absolute; inset: 0; display: grid; place-content: center; text-align: center; gap: 8px; padding: 20px; border-radius: 18px; backface-visibility: hidden; background: linear-gradient(135deg, #3b2b72, #1c2a5c); border: 1px solid #8f7bff99; box-shadow: 0 12px 30px #0004 }
.face small { font-size: 10px; color: #c0b8f2 } .face b { font-size: 17px; line-height: 1.9 } .face.back { transform: rotateY(180deg); background: linear-gradient(135deg, #0e4d4a, #1c2a5c); border-color: #4df0c099 } .face.back small { color: #a4f5dc }

.boss { position: relative; padding: 18px; border-radius: 18px; border: 1px solid transparent; background: linear-gradient(140deg, #29182d, #1a1730 55%, #151b35) padding-box, conic-gradient(from var(--ang), #4a2a4a 55%, #ff426b 76%, #ffb05b 82%, #4a2a4a) border-box; animation: spinAng 4s linear infinite }
.boss-head { display: flex; align-items: center; gap: 11px; margin-bottom: 12px } .boss-head > span { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 13px; background: #61253f; color: #ff8b9d; font-size: 23px }
.boss-head > div { flex: 1; display: flex; flex-direction: column } .boss-head small { font-size: 10px; color: #ff8fa8 } .boss-head b { font-size: 13px } .boss-head em { font-style: normal; font-size: 10px; padding: 5px 9px; border: 1px solid #b34464; border-radius: 8px; color: #ffb3c1 }
.boss h3 { margin: 0 0 14px; font-size: 15px; line-height: 2.1 }
.opts { display: grid; grid-template-columns: 1fr 1fr; gap: 9px }
.opt { display: flex; align-items: center; gap: 10px; text-align: right; padding: 11px; border: 1px solid #47314f; border-radius: 13px; background: #15172e; color: #e0def2; cursor: pointer; font-size: 12.5px; line-height: 1.8; transition: .22s }
.opt:hover:not(:disabled) { transform: translateY(-2px); border-color: #ff7590; background: #2a1b36 } .opt:disabled { cursor: default }
.letter { width: 28px; height: 28px; flex: 0 0 28px; display: grid; place-items: center; border-radius: 9px; background: #38213d; color: #ff9caf; font-size: 11px; font-weight: 900 } .txt { flex: 1 } .res { font-size: 18px; font-weight: 900 }
.opt.correct, .opt.reveal { border-color: #40e5b0; background: #123d3b; color: #caffed } .opt.correct .letter, .opt.reveal .letter { background: #2ba88b; color: #fff } .opt.correct { animation: pop .5s cubic-bezier(.2, 1.6, .4, 1) }
.opt.wrong { border-color: #ff4c70; background: #4a1b35; color: #ffe0e7; animation: shake .4s }
.feedback { margin-top: 13px; padding: 12px 14px; border-radius: 12px; border: 1px solid #ff587b66; background: #4a1c354d; color: #ffa5b8 } .feedback.ok { border-color: #42e7b4aa; background: #0f443d66; color: #8ff8d8 } .feedback b { font-size: 12px } .feedback p { margin: 6px 0 0; font-size: 12px; line-height: 2; color: #dcd6ee }

.img { margin: 0 } .img img { display: block; margin: auto; max-width: 100%; max-height: 520px; object-fit: contain; border-radius: 14px; border: 1px solid #3b4d76 } .img figcaption { margin-top: 9px; text-align: center; font-size: 11px; color: var(--mut) } .img-ph { padding: 46px; text-align: center; border: 1px dashed #465a87; border-radius: 14px; color: #90a4d2 }
.checklist { display: grid; gap: 8px } .checklist label { position: relative; display: flex; align-items: center; gap: 11px; padding: 11px 13px; border-radius: 13px; border: 1px solid #2d4065; background: #101a33; color: #d3e1ff; font-size: 13px; cursor: pointer; transition: .25s }
.checklist input { position: absolute; opacity: 0 } .checklist input:focus-visible + .box { outline: 2px solid var(--cy) }
.box { width: 24px; height: 24px; flex: 0 0 24px; display: grid; place-items: center; border-radius: 8px; border: 1.5px solid #4b618f; color: transparent; transition: .25s cubic-bezier(.2, 1.6, .4, 1) } .checklist label.on { border-color: #2a887e; color: #8ff0d2; background: #0f2d33 } .checklist label.on .box { color: #052b2a; background: #5ae4bd; border-color: #5ae4bd; transform: scale(1.1) }
.unknown p { white-space: pre-wrap; line-height: 2; color: #ccd9f4 }
.empty { text-align: center; padding: 40px; color: var(--mut) }

.finish { display: flex; align-items: center; gap: 15px; margin-top: 8px; padding: 18px; border-radius: 20px; border: 1px solid #3b4774; background: linear-gradient(100deg, #171f3e, #25234a); transition: .4s }
.finish.won { border-color: #8d8049; background: linear-gradient(100deg, #222b3b, #3d3242) }
.finish-emblem { width: 54px; height: 54px; flex-shrink: 0; display: grid; place-items: center; font-size: 27px; border-radius: 17px; background: linear-gradient(145deg, #5d70bc, #2c315d) } .won .finish-emblem { background: linear-gradient(145deg, #ffdb7d, #ce8d40) }
.finish-text { flex: 1; min-width: 0 } .finish-text b { font-size: 14px } .finish-text p { margin: 4px 0 0; font-size: 11.5px; color: #a4b4da; line-height: 1.9 } .finish-actions { display: flex; gap: 8px; flex-wrap: wrap }

.reward { position: fixed; z-index: 60; bottom: 26px; left: 26px; display: flex; align-items: center; gap: 12px; padding: 13px 18px; border-radius: 16px; border: 1px solid #f4ce69; background: linear-gradient(120deg, #342b39, #172542); box-shadow: 0 16px 50px #0009, 0 0 30px #ffd55a22 }
.reward span { font-size: 22px; color: #ffdc70; animation: spin 3s linear infinite } .reward b { font-size: 12px }
.reward-enter-active { animation: pop .4s cubic-bezier(.2, 1.6, .4, 1) } .reward-leave-active { transition: .25s } .reward-leave-to { opacity: 0; transform: translateY(12px) }
.confetti { position: fixed; inset: 0; z-index: 70; pointer-events: none; overflow: hidden }
.confetti i { position: absolute; top: -20px; left: calc(var(--x) * 1%); border-radius: 2px; background: var(--c); opacity: 0; transform: rotate(var(--r)); animation: fall var(--t) cubic-bezier(.3, .5, .6, 1) var(--d) forwards }
.foot { text-align: center; padding: 8px 0 28px; font-size: 11px; color: #4f6499; letter-spacing: .5px }

.state { min-height: 68vh; display: grid; place-content: center; justify-items: center; gap: 14px; text-align: center } .state p { margin: 0; color: var(--mut); font-size: 12px }
.portal { position: relative; width: 96px; height: 96px; display: grid; place-items: center } .portal::before, .portal::after { content: ''; position: absolute; border-radius: 50%; border: 2px solid transparent; border-top-color: var(--cy); border-bottom-color: var(--vi); inset: 4px; animation: spin 2s linear infinite } .portal::after { inset: 18px; border-color: #8b72ff transparent var(--cy); animation-direction: reverse }
.portal span { width: 26px; height: 26px; border-radius: 9px; background: linear-gradient(145deg, #80f4ff, #9a78ff); box-shadow: 0 0 34px #70b9ff; animation: bob 1.5s infinite }
.err-gem { width: 64px; height: 64px; display: grid; place-items: center; font-size: 34px; border-radius: 20px; color: #ff9db1; background: #492338; border: 1px solid #ff668b }
.card-enter-active, .card-leave-active { transition: all .3s ease } .card-enter-from { opacity: 0; transform: translateY(18px) scale(.98) } .card-leave-to { opacity: 0 } .fade-enter-active { transition: .3s } .fade-enter-from { opacity: 0; transform: translateY(-6px) }

@keyframes spinAng { to { --ang: 360deg } } @keyframes spin { to { transform: rotate(360deg) } }
@keyframes bob { 0%, 100% { transform: translateY(0) } 50% { transform: translateY(-6px) } }
@keyframes float { to { transform: translate(60px, -40px) scale(1.15) } } @keyframes drift { to { background-position: 0 1200px, 31px 1700px } }
@keyframes twinkle { from { opacity: .15; transform: scale(.6) } to { opacity: 1; transform: scale(1.5) } }
@keyframes shine { 0%, 60% { transform: translateX(120%) } 100% { transform: translateX(-120%) } }
@keyframes nodePulse { 0%, 100% { box-shadow: 0 0 16px #54cfff44 } 50% { box-shadow: 0 0 32px #54cfffaa } }
@keyframes pop { from { opacity: 0; transform: scale(.85) } 60% { transform: scale(1.06) } to { opacity: 1; transform: none } }
@keyframes shake { 0%, 100% { transform: translateX(0) } 25% { transform: translateX(5px) } 75% { transform: translateX(-5px) } }
@keyframes fall { 0% { opacity: 1; transform: translateY(0) rotate(var(--r)) } 100% { opacity: .9; transform: translateY(108vh) rotate(calc(var(--r) + 720deg)) translateX(40px) } }

@media (max-width: 760px) {
  .topbar { gap: 8px; height: 62px } .brand span:last-child { display: none }
  .hero { grid-template-columns: 1fr; padding: 22px 18px } .hero-icon { width: 64px; height: 64px; font-size: 32px; border-radius: 20px } .hero-card { flex-wrap: wrap } .hero-card .btn { width: 100% }
  .timeline-wrap { padding:16px 12px } .timeline-heading { align-items:flex-start; flex-direction:column; gap:6px } .timeline { grid-template-columns:1fr; gap:10px } .timeline-item { min-height:88px; padding:13px 12px } .timeline-status { left:10px; bottom:7px } .card { padding:14px 12px }
  .c-para { font-size: 14px } .opts { grid-template-columns: 1fr } .finish { flex-wrap: wrap } .finish-actions { width: 100% } .finish-actions .btn { flex: 1 }
  .reward { left: 12px; right: 12px; bottom: 12px } .stage-medal { width: 52px; height: 52px; font-size: 23px }
}
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important } .confetti { display: none } }
@media print {
  .topbar, .timeline-wrap, .hero-card, .check, .finish, .reward, .confetti, .foot, .bg-stars, .aurora { display: none !important }
  .quest { background: #fff; color: #111 } .hero, .card, .callout-in, .boss, .formula, .quote { background: #fff !important; color: #111 !important; box-shadow: none !important; border: 1px solid #bbb !important; animation: none }
  .card { grid-template-columns: 1fr; break-inside: avoid } .c-para, .c-list li, .callout p { color: #222 } .hero-copy p, .meta { color: #333 } .callout { background: #ddd !important }
}
</style>
