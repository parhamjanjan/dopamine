<template>
  <div class="forge" dir="rtl">
    <div class="bg-stars"></div><div class="aurora a1"></div><div class="aurora a2"></div><div class="aurora a3"></div>

    <header class="topbar">
      <RouterLink to="/notes" class="brand"><span class="brand-gem">✦</span><span><b>DOPAMINE</b><small>کارگاه ساخت جزوه</small></span></RouterLink>
      <nav class="crumb"><span>کتابخانه</span><i>‹</i><b>{{ isEdit ? 'ویرایش جزوه' : 'جزوهٔ جدید' }}</b></nav>
      <div class="top-tools">
        <button class="icon-btn" :disabled="!history.length" @click="undo" title="بازگشت (Ctrl+Z)">↶</button>
        <button class="icon-btn" :disabled="!future.length" @click="redo" title="جلو (Ctrl+Shift+Z)">↷</button>
        <div class="seg">
          <button :class="{ on: mode === 'edit' }" @click="mode = 'edit'">✎ ویرایش</button>
          <button :class="{ on: mode === 'preview' }" @click="mode = 'preview'">◉ پیش‌نمایش</button>
        </div>
        <span class="save-state" :class="{ ok: !dirty && lastSaved }"><i></i>{{ saveMessage }}</span>
        <button class="btn quiet" :disabled="saving" @click="save('draft')">ذخیره پیش‌نویس</button>
        <button class="btn primary" :disabled="saving" @click="save('published')">{{ saving ? 'در حال ذخیره…' : 'انتشار جزوه' }}</button>
      </div>
    </header>

    <div v-if="loading" class="state"><div class="loader"><i></i></div><b>در حال باز کردن کارگاه…</b></div>
    <div v-else-if="denied" class="state">
      <div class="lock">⚿</div><h2>این بخش فقط برای مدیران باز است</h2>
      <p>برای ساخت یا ویرایش جزوه با حساب مدیر وارد شو.</p>
      <RouterLink to="/notes" class="btn primary">بازگشت به کتابخانه</RouterLink>
    </div>

    <main v-else class="workspace">
      <!-- ───────── Sidebar ───────── -->
      <aside class="side">
        <section class="panel">
          <h1>{{ isEdit ? 'ویرایش جزوه' : 'یک دنیای تازه بساز' }}</h1>
          <p class="lead">عنوان و ظاهر جلد رو مشخص کن؛ بعد از بوم سمت چپ مرحله‌ها رو بچین.</p>

          <label class="field">عنوان جزوه
            <input v-model="form.title" maxlength="220" placeholder="مثلاً سفر به دنیای سلول‌ها" />
          </label>
          <label class="field">توضیح کوتاه
            <textarea v-model="form.subtitle" rows="3" placeholder="دانش‌آموز در این جزوه چه چیزی یاد می‌گیرد؟"></textarea>
          </label>
          <div class="grid2">
            <label class="field">درس<input v-model="form.subject" placeholder="زیست‌شناسی" /></label>
            <label class="field">پایه
              <select v-model="form.grade">
                <option value="">همه پایه‌ها</option>
                <option v-for="g in grades" :key="g">{{ g }}</option>
              </select>
            </label>
          </div>
          <div class="field">رنگ دنیا
            <div class="swatches">
              <button v-for="c in palette" :key="c" class="swatch" :class="{ on: form.cover_color === c }" :style="{ background: c }" @click="form.cover_color = c" :aria-label="c"></button>
              <input v-model="form.cover_color" type="color" class="swatch-custom" title="رنگ دلخواه" />
            </div>
          </div>
          <div class="field">آیکون جلد
            <div class="emoji-row">
              <button v-for="e in emojis" :key="e" :class="{ on: form.cover_icon === e }" @click="form.cover_icon = e">{{ e }}</button>
              <input v-model="form.cover_icon" maxlength="8" class="emoji-input" />
            </div>
          </div>
          <label class="field">زمان مطالعه (دقیقه)
            <div class="inline">
              <input v-model.number="form.estimated_minutes" type="number" min="1" max="600" />
              <button class="btn quiet small" @click="autoMinutes">محاسبهٔ خودکار</button>
            </div>
          </label>
          <label class="field">برچسب‌ها
            <input v-model="tagsText" placeholder="امتحان، نکته‌دار، فصل اول" />
            <small>با ویرگول جدا کن.</small>
          </label>
        </section>

        <section class="panel ready" :class="{ good: !errorCount }">
          <div class="ready-head">
            <div class="ring" :style="{ '--p': readiness }"><b>{{ readiness }}%</b></div>
            <div><h3>{{ errorCount ? 'هنوز آمادهٔ انتشار نیست' : 'آمادهٔ انتشار است' }}</h3>
              <small>{{ errorCount }} خطا · {{ warnCount }} پیشنهاد</small></div>
          </div>
          <ul v-if="issues.length" class="issue-list">
            <li v-for="(it, i) in issues" :key="i" :class="it.level" @click="it.id && focusBlock(it.id)">
              <span>{{ it.level === 'error' ? '!' : '•' }}</span>{{ it.text }}
            </li>
          </ul>
          <p v-else class="ok-note">همه‌چیز مرتبه؛ می‌تونی منتشر کنی.</p>
        </section>

        <section class="panel stats">
          <div><b>{{ form.blocks.length }}</b><small>بلوک</small></div>
          <div><b>{{ stageCount }}</b><small>مرحله</small></div>
          <div><b>{{ quizCount }}</b><small>آزمون</small></div>
          <div><b>{{ wordCount }}</b><small>کلمه</small></div>
        </section>

        <section class="panel tip">
          <b>راهنمای میان‌بر</b>
          <p>در متن‌ها از <code>**پررنگ**</code>، <code>==هایلایت==</code> و <code>`کد`</code> استفاده کن. <kbd>Ctrl</kbd>+<kbd>S</kbd> پیش‌نویس را ذخیره می‌کند. هر «عنوان» یک مرحلهٔ جدید در بازی می‌سازد.</p>
        </section>
      </aside>

      <!-- ───────── Canvas ───────── -->
      <section class="canvas">
        <div v-if="mode === 'edit'" class="toolbar">
          <div class="toolbar-title"><span class="live"></span><b>افزودن بلوک</b><small>بعد از بلوک انتخاب‌شده اضافه می‌شود</small></div>
          <div class="tools">
            <button v-for="t in tools" :key="t.type" class="tool" :data-type="t.type" @click="addBlock(t.type)">
              <span>{{ t.icon }}</span><b>{{ t.label }}</b>
            </button>
          </div>
        </div>
        <div v-else class="toolbar preview-bar">
          <b>پیش‌نمایش جزوه</b>
          <div class="seg">
            <button :class="{ on: device === 'desktop' }" @click="device = 'desktop'">▭ دسکتاپ</button>
            <button :class="{ on: device === 'mobile' }" @click="device = 'mobile'">▯ موبایل</button>
          </div>
        </div>

        <div class="paper" :class="{ mobile: mode === 'preview' && device === 'mobile' }">
          <header class="hero" :style="{ '--cover': form.cover_color }">
            <div class="hero-icon">{{ form.cover_icon || '📘' }}</div>
            <div class="hero-copy">
              <small>{{ form.subject || 'درس' }} · {{ form.grade || 'همهٔ پایه‌ها' }} · {{ form.estimated_minutes || 10 }} دقیقه</small>
              <h2>{{ form.title || 'عنوان جزوه' }}</h2>
              <p>{{ form.subtitle || 'توضیح کوتاه جزوه اینجا نمایش داده می‌شود.' }}</p>
            </div>
          </header>

          <!-- Edit mode -->
          <template v-if="mode === 'edit'">
            <div v-if="!form.blocks.length" class="empty">
              <div class="empty-gem">✧</div><h3>بوم هنوز خالیه</h3>
              <p>با یک عنوان شروع کن؛ هر عنوان یک مرحله از بازی می‌شود.</p>
              <button class="btn primary" @click="addBlock('heading')">ساخت اولین مرحله</button>
            </div>

            <TransitionGroup name="blk" tag="div" class="blocks">
              <div v-for="(block, index) in form.blocks" :key="block.id" class="blk-wrap"
                   @dragover.prevent="overIndex = index" @drop.prevent="onDrop(index)">
                <section :id="`blk-${block.id}`" class="block" :data-type="block.type"
                         :class="{ active: activeBlock === block.id, dragging: dragIndex === index, over: overIndex === index && dragIndex !== null && dragIndex !== index }"
                         @click="activeBlock = block.id">
                  <div class="bar">
                    <span class="grip" draggable="true" title="بکش و جابه‌جا کن" @dragstart="onDragStart(index, $event)" @dragend="onDragEnd">⠿</span>
                    <span class="num">{{ index + 1 }}</span>
                    <b>{{ blockLabel(block.type) }}</b>
                    <span class="spacer"></span>
                    <button title="جمع کردن" @click.stop="toggleCollapse(block.id)">{{ collapsed.has(block.id) ? '▾' : '▴' }}</button>
                    <button title="بالا" :disabled="index === 0" @click.stop="moveBlock(index, -1)">↑</button>
                    <button title="پایین" :disabled="index === form.blocks.length - 1" @click.stop="moveBlock(index, 1)">↓</button>
                    <button title="تکثیر" @click.stop="duplicateBlock(index)">⧉</button>
                    <button title="حذف" class="danger" @click.stop="removeBlock(index)">×</button>
                  </div>

                  <div v-show="!collapsed.has(block.id)" class="body">
                    <template v-if="block.type === 'heading'">
                      <input v-model="block.text" class="heading-input" placeholder="عنوان مرحله…" />
                      <div class="row-opt"><span>اندازه</span>
                        <div class="seg tiny"><button v-for="l in [1, 2, 3]" :key="l" :class="{ on: block.level === l }" @click="block.level = l">{{ ['بزرگ', 'متوسط', 'کوچک'][l - 1] }}</button></div>
                      </div>
                    </template>

                    <textarea v-else-if="block.type === 'paragraph'" v-model="block.text" rows="4" class="area" placeholder="متن آموزشی…"></textarea>

                    <template v-else-if="block.type === 'callout'">
                      <div class="callout-preview" :data-style="block.style" :style="calloutVars(block)">
                        <span>{{ block.icon || calloutIcon(block.style) }}</span>
                        <div><small>{{ calloutKind(block.style) }}</small><b>{{ block.title || 'عنوان باکس' }}</b><p v-html="rich(block.text) || 'متن باکس اینجا دیده می‌شود.'"></p></div>
                      </div>
                      <div class="chips">
                        <button v-for="s in calloutStyles" :key="s.v" :class="{ on: block.style === s.v }" @click="setCalloutStyle(block, s)">{{ s.icon }} {{ s.l }}</button>
                      </div>
                      <div class="grid2">
                        <label class="field">عنوان<input v-model="block.title" /></label>
                        <label class="field">آیکون<input v-model="block.icon" maxlength="8" /></label>
                      </div>
                      <label class="field">متن<textarea v-model="block.text" rows="3"></textarea></label>
                      <label v-if="block.style === 'custom'" class="field">رنگ سفارشی<input v-model="block.customColor" type="color" class="color" /></label>
                    </template>

                    <template v-else-if="block.type === 'list' || block.type === 'checklist'">
                      <label class="hint">هر مورد در یک خط</label>
                      <textarea v-model="block.text" rows="4" class="area"></textarea>
                    </template>

                    <div v-else-if="block.type === 'formula'" class="formula-box"><span>ƒx</span><textarea v-model="block.text" rows="2" class="area" placeholder="فرمول یا رابطه…"></textarea></div>
                    <textarea v-else-if="block.type === 'quote'" v-model="block.text" rows="3" class="area quote" placeholder="متن نقل‌قول…"></textarea>

                    <template v-else-if="block.type === 'flashcard'">
                      <div class="grid2">
                        <label class="field">روی کارت (سؤال)<textarea v-model="block.front" rows="3"></textarea></label>
                        <label class="field">پشت کارت (پاسخ)<textarea v-model="block.back" rows="3"></textarea></label>
                      </div>
                    </template>

                    <template v-else-if="block.type === 'quiz'">
                      <label class="field">صورت سؤال<textarea v-model="block.question" rows="2" placeholder="سؤال را وارد کن…"></textarea></label>
                      <div class="opts">
                        <div v-for="(o, i) in block.options" :key="i" class="opt" :class="{ right: block.answer === i }">
                          <span>{{ letters[i] }}</span>
                          <input v-model="block.options[i]" :placeholder="`گزینهٔ ${i + 1}`" />
                          <button class="mark" :class="{ on: block.answer === i }" @click="block.answer = i">{{ block.answer === i ? '✓ درست' : 'درست؟' }}</button>
                          <button class="x" :disabled="block.options.length <= 2" @click="removeOption(block, i)">×</button>
                        </div>
                      </div>
                      <button v-if="block.options.length < 6" class="btn quiet small" @click="block.options.push('')">＋ گزینهٔ تازه</button>
                      <label class="field">توضیح پاسخ<textarea v-model="block.explanation" rows="2" placeholder="چرا این گزینه درست است؟"></textarea></label>
                    </template>

                    <template v-else-if="block.type === 'image'">
                      <div class="grid2">
                        <label class="field">نشانی تصویر<input v-model="block.url" type="url" dir="ltr" placeholder="https://…" /></label>
                        <label class="field">توضیح یا منبع<input v-model="block.caption" /></label>
                      </div>
                      <img v-if="block.url" :src="block.url" alt="" class="img-prev" @error="$event.target.style.display = 'none'" @load="$event.target.style.display = 'block'" />
                    </template>

                    <div v-else-if="block.type === 'divider'" class="divider-prev"><i></i><span>✦</span><i></i></div>
                  </div>
                </section>

                <div class="gap" :class="{ open: insertAt === index + 1 }">
                  <button class="gap-btn" @click.stop="insertAt = insertAt === index + 1 ? null : index + 1" title="افزودن بلوک اینجا">＋</button>
                  <div v-if="insertAt === index + 1" class="gap-menu">
                    <button v-for="t in tools" :key="t.type" @click="insertBlock(index + 1, t.type)"><span>{{ t.icon }}</span>{{ t.label }}</button>
                  </div>
                </div>
              </div>
            </TransitionGroup>
          </template>

          <!-- Preview mode -->
          <div v-else class="blocks pv">
            <article v-for="b in form.blocks" :key="b.id" class="pv-item" :data-type="b.type">
              <component :is="`h${(b.level || 2) + 1}`" v-if="b.type === 'heading'" class="pv-h">{{ b.text }}</component>
              <p v-else-if="b.type === 'paragraph'" class="pv-p" v-html="rich(b.text)"></p>
              <ul v-else-if="b.type === 'list'" class="pv-list"><li v-for="(l, i) in lines(b.text)" :key="i" v-html="rich(l)"></li></ul>
              <div v-else-if="b.type === 'checklist'" class="pv-check"><label v-for="(l, i) in lines(b.text)" :key="i"><input type="checkbox" />{{ l }}</label></div>
              <div v-else-if="b.type === 'callout'" class="callout-preview" :data-style="b.style" :style="calloutVars(b)">
                <span>{{ b.icon || calloutIcon(b.style) }}</span><div><small>{{ calloutKind(b.style) }}</small><b>{{ b.title }}</b><p v-html="rich(b.text)"></p></div>
              </div>
              <div v-else-if="b.type === 'formula'" class="pv-formula">{{ b.text }}</div>
              <blockquote v-else-if="b.type === 'quote'" class="pv-quote">{{ b.text }}</blockquote>
              <div v-else-if="b.type === 'flashcard'" class="flip" :class="{ on: flipped.has(b.id) }" @click="toggleFlip(b.id)">
                <div class="flip-in"><div class="face">{{ b.front || 'روی کارت' }}<small>برای دیدن پاسخ بزن</small></div><div class="face back">{{ b.back || 'پشت کارت' }}</div></div>
              </div>
              <div v-else-if="b.type === 'quiz'" class="pv-quiz"><b>{{ b.question || 'سؤال' }}</b>
                <div v-for="(o, i) in b.options" :key="i" :class="{ right: b.answer === i }"><span>{{ letters[i] }}</span>{{ o }}</div>
              </div>
              <figure v-else-if="b.type === 'image' && b.url"><img :src="b.url" alt="" /><figcaption>{{ b.caption }}</figcaption></figure>
              <div v-else-if="b.type === 'divider'" class="divider-prev"><i></i><span>✦</span><i></i></div>
            </article>
          </div>

          <div v-if="form.blocks.length" class="paper-end">پایان جزوه</div>
        </div>

        <div class="bottom-actions">
          <div><b>آمادهٔ انتشاری؟</b><small>{{ errorCount ? `${errorCount} مورد باید اصلاح شود.` : 'مشکلی پیدا نشد.' }}</small></div>
          <button class="btn quiet" :disabled="saving" @click="save('draft')">ذخیره پیش‌نویس</button>
          <button class="btn primary" :disabled="saving" @click="save('published')">انتشار جزوه</button>
        </div>
      </section>
    </main>

    <Transition name="toast"><div v-if="toast" class="toast"><span>✦</span>{{ toast }}</div></Transition>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink, onBeforeRouteLeave, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { notesApi } from '../services/notes'

const route = useRoute(), router = useRouter(), auth = useAuthStore()
const isEdit = computed(() => Boolean(route.params.id))
const loading = ref(true), denied = ref(false), saving = ref(false), toast = ref('')
const mode = ref('edit'), device = ref('desktop')
const activeBlock = ref(null), insertAt = ref(null)
const dirty = ref(false), lastSaved = ref(false)
const collapsed = reactive(new Set()), flipped = reactive(new Set())
const dragIndex = ref(null), overIndex = ref(null)

const form = reactive({ title: '', subtitle: '', subject: '', grade: '', cover_color: '#7055e8', cover_icon: '📘', estimated_minutes: 10, tags: [], chapters: [], blocks: [], status: 'draft' })
const tagsText = ref('')

const grades = ['هفتم', 'هشتم', 'نهم', 'دهم', 'یازدهم', 'دوازدهم']
const palette = ['#7055e8', '#2563eb', '#0d9488', '#16a34a', '#d97706', '#db2777', '#e11d48', '#0891b2']
const emojis = ['📘', '🧬', '🧪', '📐', '🌍', '⚡', '🧠', '🚀']
const letters = ['A', 'B', 'C', 'D', 'E', 'F']
const tools = [
  { type: 'heading', label: 'عنوان مرحله', icon: 'T' }, { type: 'paragraph', label: 'متن', icon: '¶' },
  { type: 'callout', label: 'باکس نکته', icon: '💡' }, { type: 'list', label: 'فهرست', icon: '☷' },
  { type: 'formula', label: 'فرمول', icon: 'ƒx' }, { type: 'quiz', label: 'آزمون', icon: '☠' },
  { type: 'flashcard', label: 'فلش‌کارت', icon: '🃏' }, { type: 'image', label: 'تصویر', icon: '▧' },
  { type: 'quote', label: 'نقل‌قول', icon: '❞' }, { type: 'checklist', label: 'چک‌لیست', icon: '☑' },
  { type: 'divider', label: 'جداکننده', icon: '—' }
]
const calloutStyles = [
  { v: 'tip', l: 'نکته', icon: '💡', t: 'نکتهٔ مهم' }, { v: 'definition', l: 'تعریف', icon: '◈', t: 'تعریف' },
  { v: 'warning', l: 'هشدار', icon: '⚠️', t: 'هشدار' }, { v: 'trap', l: 'دام تستی', icon: '🎯', t: 'دام تستی' },
  { v: 'example', l: 'مثال', icon: '✦', t: 'مثال' }, { v: 'summary', l: 'خلاصه', icon: '✓', t: 'خلاصه' },
  { v: 'exam', l: 'امتحانی', icon: '🧠', t: 'نکتهٔ امتحانی' }, { v: 'custom', l: 'سفارشی', icon: '✧', t: 'توجه' }
]

/* ───────── helpers ───────── */
const uid = () => globalThis.crypto?.randomUUID?.() || `b-${Date.now()}-${Math.random().toString(36).slice(2)}`
const lines = t => String(t || '').split('\n').map(x => x.trim()).filter(Boolean)
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const rich = t => esc(t).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/==(.+?)==/g, '<mark>$1</mark>').replace(/`(.+?)`/g, '<code>$1</code>').replace(/\n/g, '<br>')
const blockLabel = type => tools.find(t => t.type === type)?.label || type
const calloutIcon = s => calloutStyles.find(x => x.v === s)?.icon || '💡'
const calloutKind = s => s === 'warning' ? 'هشدار' : s === 'trap' ? 'دام تستی' : s === 'definition' ? 'تعریف' : s === 'example' ? 'مثال' : s === 'summary' ? 'خلاصه' : s === 'exam' ? 'نکتهٔ امتحانی' : 'نکتهٔ ویژه'
const calloutVars = b => (b.style === 'custom' && /^#[0-9a-f]{6}$/i.test(b.customColor || '')) ? { '--c': b.customColor } : {}

function newBlock(type) {
  const base = { id: uid(), type }
  switch (type) {
    case 'heading': return { ...base, text: 'عنوان مرحلهٔ تازه', level: 2 }
    case 'callout': return { ...base, title: 'نکتهٔ مهم', text: '', style: 'tip', icon: '💡', customColor: '#7055e8' }
    case 'list': case 'checklist': return { ...base, text: 'مورد اول\nمورد دوم' }
    case 'quiz': return { ...base, question: '', options: ['', '', '', ''], answer: 0, explanation: '' }
    case 'flashcard': return { ...base, front: '', back: '' }
    case 'image': return { ...base, url: '', caption: '' }
    case 'divider': return base
    default: return { ...base, text: '' }
  }
}

/* ───────── block actions ───────── */
function insertBlock(at, type) {
  const b = newBlock(type)
  form.blocks.splice(at, 0, b)
  activeBlock.value = b.id; insertAt.value = null
  nextTick(() => focusBlock(b.id))
}
function addBlock(type) {
  const i = form.blocks.findIndex(x => x.id === activeBlock.value)
  insertBlock(i < 0 ? form.blocks.length : i + 1, type)
}
function removeBlock(index) { if (confirm('این بلوک حذف شود؟')) form.blocks.splice(index, 1) }
function duplicateBlock(index) {
  const copy = JSON.parse(JSON.stringify(form.blocks[index])); copy.id = uid()
  form.blocks.splice(index + 1, 0, copy); activeBlock.value = copy.id
}
function moveBlock(index, dir) {
  const t = index + dir
  if (t < 0 || t >= form.blocks.length) return
  const [b] = form.blocks.splice(index, 1); form.blocks.splice(t, 0, b)
}
function toggleCollapse(id) { collapsed.has(id) ? collapsed.delete(id) : collapsed.add(id) }
function toggleFlip(id) { flipped.has(id) ? flipped.delete(id) : flipped.add(id) }
function setCalloutStyle(b, s) {
  const wasDefault = !b.title || calloutStyles.some(x => x.t === b.title)
  b.style = s.v; b.icon = s.icon
  if (wasDefault) b.title = s.t
}
function removeOption(b, i) {
  if (b.options.length <= 2) return
  b.options.splice(i, 1)
  if (b.answer === i) b.answer = 0
  else if (b.answer > i) b.answer--
}
function focusBlock(id) {
  activeBlock.value = id
  mode.value = 'edit'
  nextTick(() => document.getElementById(`blk-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }))
}

/* drag & drop */
function onDragStart(i, e) {
  dragIndex.value = i
  e.dataTransfer.effectAllowed = 'move'
  e.dataTransfer.setData('text/plain', String(i))
  const el = e.target.closest('.block'); if (el) e.dataTransfer.setDragImage(el, 24, 24)
}
function onDrop(to) {
  const from = dragIndex.value
  if (from !== null && from !== to) { const [b] = form.blocks.splice(from, 1); form.blocks.splice(to, 0, b); activeBlock.value = b.id }
  onDragEnd()
}
function onDragEnd() { dragIndex.value = null; overIndex.value = null }

/* ───────── stats & validation ───────── */
const wordCount = computed(() => form.blocks.reduce((n, b) => n + [b.text, b.question, b.front, b.back, b.title, b.explanation].filter(Boolean).join(' ').split(/\s+/).filter(Boolean).length, 0))
const quizCount = computed(() => form.blocks.filter(b => b.type === 'quiz').length)
const stageCount = computed(() => { const h = form.blocks.filter(b => b.type === 'heading').length; return h || Math.ceil(form.blocks.length / 4) })
function autoMinutes() { form.estimated_minutes = Math.min(600, Math.max(1, Math.ceil(wordCount.value / 110) + quizCount.value)) }

const issues = computed(() => {
  const out = []
  const err = (text, id) => out.push({ level: 'error', text, id })
  const warn = (text, id) => out.push({ level: 'warn', text, id })
  if (!form.title.trim()) err('عنوان جزوه را بنویس.')
  if (!form.blocks.length) err('حداقل یک بلوک اضافه کن.')
  if (form.blocks.length && !form.blocks.some(b => b.type === 'heading')) warn('بدون عنوان مرحله، جزوه خودکار چهارتا‌چهارتا تقسیم می‌شود.')
  if (!form.subject.trim()) warn('درس مشخص نشده.')
  form.blocks.forEach((b, i) => {
    const n = i + 1
    if (b.type === 'heading' && !b.text?.trim()) err(`بلوک ${n}: عنوان خالی است.`, b.id)
    if (b.type === 'paragraph' && !b.text?.trim()) warn(`بلوک ${n}: متن خالی است.`, b.id)
    if (b.type === 'callout' && !b.text?.trim()) warn(`بلوک ${n}: باکس متن ندارد.`, b.id)
    if (b.type === 'image' && !b.url?.trim()) warn(`بلوک ${n}: نشانی تصویر خالی است.`, b.id)
    if (b.type === 'flashcard' && (!b.front?.trim() || !b.back?.trim())) err(`بلوک ${n}: هر دو روی فلش‌کارت را پر کن.`, b.id)
    if (b.type === 'quiz') {
      if (!b.question?.trim()) err(`بلوک ${n}: صورت سؤال خالی است.`, b.id)
      else if (b.options.filter(o => o.trim()).length < 2) err(`بلوک ${n}: حداقل دو گزینه لازم است.`, b.id)
      else if (!b.options[b.answer]?.trim()) err(`بلوک ${n}: گزینهٔ درست خالی است.`, b.id)
      if (!b.explanation?.trim()) warn(`بلوک ${n}: توضیح پاسخ نداری.`, b.id)
    }
  })
  return out
})
const errorCount = computed(() => issues.value.filter(i => i.level === 'error').length)
const warnCount = computed(() => issues.value.filter(i => i.level === 'warn').length)
const readiness = computed(() => Math.max(0, 100 - errorCount.value * 20 - warnCount.value * 6))

/* ───────── undo / redo / dirty ───────── */
const history = ref([]), future = ref([])
let lastSnap = '', snapTimer = null, restoring = false, ready = false
function pushHistory() {
  const s = JSON.stringify(form.blocks)
  if (s === lastSnap) return
  if (lastSnap) { history.value.push(lastSnap); if (history.value.length > 60) history.value.shift() }
  lastSnap = s; future.value = []
}
function restore(snap) { restoring = true; form.blocks = JSON.parse(snap); nextTick(() => { restoring = false }) }
function undo() {
  clearTimeout(snapTimer); pushHistory()
  if (!history.value.length) return
  future.value.push(lastSnap); lastSnap = history.value.pop(); restore(lastSnap)
}
function redo() {
  if (!future.value.length) return
  history.value.push(lastSnap); lastSnap = future.value.pop(); restore(lastSnap)
}
watch(() => [form, tagsText.value], () => {
  if (!ready) return
  dirty.value = true; lastSaved.value = false
  if (restoring) return
  clearTimeout(snapTimer); snapTimer = setTimeout(pushHistory, 450)
  backup()
}, { deep: true })

const saveMessage = computed(() => saving.value ? 'در حال ذخیره…' : dirty.value ? 'تغییرات ذخیره نشده' : lastSaved.value ? 'ذخیره شد' : 'بدون تغییر')
const backupKey = () => `forge-backup:${route.params.id || 'new'}`
let backupTimer = null
function backup() { clearTimeout(backupTimer); backupTimer = setTimeout(() => { try { localStorage.setItem(backupKey(), JSON.stringify({ form: JSON.parse(JSON.stringify(form)), tagsText: tagsText.value })) } catch { /* ignore */ } }, 900) }

function notify(msg) { toast.value = msg; setTimeout(() => { if (toast.value === msg) toast.value = '' }, 2600) }

/* ───────── load & save ───────── */
async function load() {
  loading.value = true
  try {
    if (!auth.user) await auth.fetchUser()
    if (!(auth.user?.is_staff || auth.user?.is_superuser)) { denied.value = true; return }
    if (isEdit.value) {
      const { data } = await notesApi.get(route.params.id)
      for (const k of Object.keys(form)) form[k] = data[k] ?? form[k]
      form.blocks = (data.blocks || []).map(b => ({ ...b, id: b.id || uid() }))
      tagsText.value = (data.tags || []).join(', ')
    } else {
      let restored = false
      try {
        const raw = localStorage.getItem(backupKey())
        if (raw) {
          const saved = JSON.parse(raw)
          if (saved.form?.blocks?.length && confirm('یک پیش‌نویس ذخیره‌نشده از قبل هست. بازیابی شود؟')) {
            Object.assign(form, saved.form); tagsText.value = saved.tagsText || ''; restored = true
          } else localStorage.removeItem(backupKey())
        }
      } catch { /* ignore */ }
      if (!restored) { form.blocks = [newBlock('heading'), newBlock('paragraph')]; form.blocks[0].text = 'شروع ماجراجویی' }
    }
    activeBlock.value = form.blocks[0]?.id || null
  } catch (e) {
    if ([401, 403].includes(e.response?.status)) denied.value = true
    else if (isEdit.value) notify('بارگذاری جزوه ناموفق بود.')
  } finally {
    loading.value = false
    await nextTick()
    lastSnap = JSON.stringify(form.blocks); history.value = []; future.value = []
    dirty.value = false; ready = true
  }
}

async function save(status) {
  if (!form.title.trim()) { notify('اول عنوان جزوه را بنویس.'); return }
  if (status === 'published' && errorCount.value) {
    notify(`${errorCount.value} مورد باید قبل از انتشار اصلاح شود.`)
    const first = issues.value.find(i => i.level === 'error' && i.id); if (first) focusBlock(first.id)
    return
  }
  saving.value = true
  const payload = { ...JSON.parse(JSON.stringify(form)), status, tags: tagsText.value.split(/[,،]/).map(x => x.trim()).filter(Boolean) }
  delete payload.id
  try {
    const res = isEdit.value ? await notesApi.update(route.params.id, payload) : await notesApi.create(payload)
    dirty.value = false; lastSaved.value = true
    try { localStorage.removeItem(backupKey()) } catch { /* ignore */ }
    notify(status === 'published' ? 'جزوه منتشر شد.' : 'پیش‌نویس ذخیره شد.')
    if (!isEdit.value) await router.replace(`/notes/admin/${res.data.id}/edit`)
  } catch (e) {
    const d = e.response?.data
    const msg = d?.detail || d?.title?.[0] || (typeof d?.blocks?.[0] === 'string' ? d.blocks[0] : '')
    notify(msg || 'ذخیره انجام نشد. مطمئن شو با حساب مدیر وارد شده‌ای.')
  } finally { saving.value = false }
}

/* ───────── global events ───────── */
function onKey(e) {
  const mod = e.ctrlKey || e.metaKey
  if (mod && e.key.toLowerCase() === 's') { e.preventDefault(); save('draft') }
  const typing = ['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)
  if (mod && e.key.toLowerCase() === 'z' && !typing) { e.preventDefault(); e.shiftKey ? redo() : undo() }
}
function onBeforeUnload(e) { if (dirty.value) { e.preventDefault(); e.returnValue = '' } }
onBeforeRouteLeave(() => (dirty.value && !saving.value) ? confirm('تغییرات ذخیره‌نشده از بین می‌رود. خارج می‌شوی؟') : true)
onMounted(() => { load(); window.addEventListener('keydown', onKey); window.addEventListener('beforeunload', onBeforeUnload) })
onBeforeUnmount(() => { window.removeEventListener('keydown', onKey); window.removeEventListener('beforeunload', onBeforeUnload); clearTimeout(snapTimer); clearTimeout(backupTimer) })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap');
@property --ang { syntax: '<angle>'; initial-value: 0deg; inherits: false; }

:global(*) { box-sizing: border-box }
:global(body) { margin: 0; background: #070b1d; font-family: 'Vazirmatn', Tahoma, sans-serif }

.forge {
  --bg: #070b1d; --card: #0f1830; --card2: #15213f; --line: #27375f; --txt: #eef3ff; --mut: #8fa2cf;
  --cy: #5be7ff; --vi: #8f7bff; --am: #ffcf5a; --co: #ff5c82; --mi: #4df0c0;
  position: relative; min-height: 100vh; overflow-x: hidden; color: var(--txt); font-family: 'Vazirmatn', Tahoma, sans-serif;
  background: radial-gradient(ellipse at 75% -10%, #25346a 0, transparent 45%), var(--bg); isolation: isolate;
}
.bg-stars { position: absolute; inset: 0; z-index: -1; opacity: .25; pointer-events: none;
  background-image: radial-gradient(#8adfff 1px, transparent 1px), radial-gradient(#b7a0ff 1px, transparent 1px);
  background-size: 71px 71px, 127px 127px; background-position: 0 0, 33px 41px; animation: drift 90s linear infinite }
.aurora { position: absolute; z-index: -1; width: 460px; height: 460px; border-radius: 50%; filter: blur(110px); opacity: .17; pointer-events: none; animation: float 14s ease-in-out infinite alternate }
.a1 { background: #4b76ff; top: 300px; left: -200px } .a2 { background: #b04aff; top: 900px; right: -200px; animation-delay: -5s } .a3 { background: #00e0c0; top: 1500px; left: 30%; animation-delay: -9s }
button { font-family: inherit }
:focus-visible { outline: 2px solid var(--cy); outline-offset: 2px }

/* topbar */
.topbar { position: sticky; top: 0; z-index: 30; display: flex; align-items: center; gap: 18px; min-height: 68px; padding: 8px clamp(14px, 3vw, 44px); background: #0a1228d9; backdrop-filter: blur(18px); border-bottom: 1px solid var(--line) }
.brand { display: flex; align-items: center; gap: 10px; color: inherit; text-decoration: none }
.brand-gem { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 12px; font-size: 22px; color: #0a1330; background: linear-gradient(145deg, #a6efff, #7a82ff); box-shadow: 0 0 24px #5ec3ff55; animation: bob 4s ease-in-out infinite }
.brand b { display: block; font-size: 12px; letter-spacing: 1.5px } .brand small { color: var(--mut); font-size: 10px }
.crumb { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--mut); flex: 1; min-width: 0 }
.crumb b { color: var(--txt); overflow: hidden; text-overflow: ellipsis; white-space: nowrap }
.top-tools { display: flex; align-items: center; gap: 8px; flex-wrap: wrap }
.icon-btn { width: 34px; height: 34px; border-radius: 10px; border: 1px solid var(--line); background: var(--card2); color: #c6d4fb; font-size: 17px; cursor: pointer; transition: .2s }
.icon-btn:hover:not(:disabled) { border-color: var(--vi); transform: translateY(-2px) } .icon-btn:disabled { opacity: .3; cursor: default }
.seg { display: inline-flex; padding: 3px; gap: 2px; border: 1px solid var(--line); border-radius: 11px; background: #0a1329 }
.seg button { border: 0; background: transparent; color: var(--mut); padding: 6px 11px; border-radius: 8px; font-size: 11px; font-weight: 600; cursor: pointer; transition: .2s }
.seg button.on { background: linear-gradient(110deg, #4f6bff, #8f6bff); color: #fff; box-shadow: 0 4px 14px #6a62ff44 }
.seg.tiny button { padding: 4px 9px; font-size: 10px }
.save-state { display: flex; align-items: center; gap: 6px; font-size: 10px; color: var(--mut); white-space: nowrap }
.save-state i { width: 7px; height: 7px; border-radius: 50%; background: var(--am); box-shadow: 0 0 8px var(--am) } .save-state.ok i { background: var(--mi); box-shadow: 0 0 8px var(--mi) }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; padding: 9px 15px; border-radius: 11px; font-size: 11px; font-weight: 700; cursor: pointer; text-decoration: none; white-space: nowrap; border: 1px solid transparent; transition: transform .2s, box-shadow .2s, border-color .2s }
.btn:disabled { opacity: .5; cursor: wait } .btn:hover:not(:disabled) { transform: translateY(-2px) }
.btn.quiet { background: var(--card2); color: #c3d2f7; border-color: var(--line) } .btn.quiet:hover:not(:disabled) { border-color: #6f84cc }
.btn.small { padding: 6px 10px; font-size: 10px }
.btn.primary { position: relative; overflow: hidden; color: #fff; border-color: #aaa5ff; background: linear-gradient(105deg, #5f7bff, #a06bff); box-shadow: 0 6px 22px #7770ff40 }
.btn.primary::after { content: ''; position: absolute; inset: 0; background: linear-gradient(105deg, transparent 35%, #ffffff40 50%, transparent 65%); transform: translateX(120%); animation: shine 4.5s ease-in-out infinite }

/* layout */
.workspace { max-width: 1640px; margin: auto; padding: 22px clamp(12px, 2.6vw, 40px) 60px; display: grid; grid-template-columns: 340px minmax(0, 1fr); gap: 22px; align-items: start }
.side { position: sticky; top: 90px; display: grid; gap: 14px; max-height: calc(100vh - 106px); overflow-y: auto; padding: 2px; scrollbar-width: thin; scrollbar-color: #33457a transparent }
.panel { border: 1px solid var(--line); border-radius: 20px; padding: 18px; background: linear-gradient(155deg, #151f40ee, #0e1730ee); box-shadow: 0 16px 40px #0003, inset 0 1px #ffffff0a }
.panel h1 { font-size: 20px; margin: 0 0 6px; font-weight: 800 } .lead { font-size: 11px; line-height: 2; color: var(--mut); margin: 0 0 16px }
.field { display: flex; flex-direction: column; gap: 6px; font-size: 11px; color: #b4c3e8; margin-bottom: 12px; font-weight: 500 }
.field small, .hint { font-size: 10px; color: #7b8fbf }
.field input, .field textarea, .field select, .area { width: 100%; min-width: 0; border: 1px solid #34476f; border-radius: 10px; background: #0a1329; color: #eaf0ff; padding: 9px 11px; font: 12px/1.9 'Vazirmatn', sans-serif; outline: none; resize: vertical; transition: border-color .2s, box-shadow .2s }
.field input:focus, .field textarea:focus, .field select:focus, .area:focus { border-color: #7a90ff; box-shadow: 0 0 0 3px #7a90ff22 }
::placeholder { color: #55699b }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px } .inline { display: flex; gap: 8px; align-items: center } .inline input { flex: 1 }
.color { height: 38px; padding: 3px !important; cursor: pointer }
.swatches, .emoji-row { display: flex; flex-wrap: wrap; gap: 7px; align-items: center }
.swatch { width: 26px; height: 26px; border-radius: 9px; border: 2px solid transparent; cursor: pointer; transition: .2s } .swatch:hover { transform: scale(1.12) } .swatch.on { border-color: #fff; box-shadow: 0 0 14px currentColor }
.swatch-custom { width: 30px; height: 30px; padding: 0; border: 0; background: none; cursor: pointer }
.emoji-row button { width: 32px; height: 32px; border-radius: 10px; border: 1px solid var(--line); background: #0a1329; font-size: 16px; cursor: pointer; transition: .2s } .emoji-row button.on, .emoji-row button:hover { border-color: var(--vi); background: #20294f }
.emoji-input { width: 56px !important; text-align: center; padding: 6px !important }

.ready-head { display: flex; align-items: center; gap: 13px; margin-bottom: 12px } .ready h3 { font-size: 13px; margin: 0 0 3px } .ready small { color: var(--mut); font-size: 10px }
.ring { --p: 0; width: 54px; height: 54px; border-radius: 50%; display: grid; place-items: center; flex-shrink: 0; background: radial-gradient(#0f1830 58%, transparent 60%), conic-gradient(var(--co) calc(var(--p) * 1%), #1c2a50 0); transition: .5s }
.ready.good .ring { background: radial-gradient(#0f1830 58%, transparent 60%), conic-gradient(var(--mi) calc(var(--p) * 1%), #1c2a50 0) } .ring b { font-size: 11px }
.issue-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 5px; max-height: 190px; overflow: auto }
.issue-list li { display: flex; gap: 8px; align-items: flex-start; padding: 7px 9px; border-radius: 9px; font-size: 10.5px; line-height: 1.8; color: #c8d3f1; background: #0b1429; cursor: pointer; border: 1px solid transparent }
.issue-list li:hover { border-color: var(--line) } .issue-list li span { font-weight: 900 } .issue-list .error span { color: var(--co) } .issue-list .warn span { color: var(--am) }
.ok-note { margin: 0; font-size: 11px; color: var(--mi) }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; text-align: center; padding: 14px 10px } .stats b { display: block; font-size: 18px } .stats small { font-size: 9px; color: var(--mut) }
.tip b { font-size: 11px; color: var(--am) } .tip p { margin: 6px 0 0; font-size: 10.5px; line-height: 2; color: #aebde2 }
code { background: #1d2850; padding: 1px 6px; border-radius: 6px; font-size: .92em; color: #9fe7ff } kbd { background: #1d2850; border: 1px solid #33467a; border-radius: 5px; padding: 0 5px; font-size: 10px }

/* canvas */
.canvas { min-width: 0 }
.toolbar { position: sticky; top: 78px; z-index: 12; margin-bottom: 14px; padding: 13px; border: 1px solid var(--line); border-radius: 18px; background: #101a36ee; backdrop-filter: blur(14px); box-shadow: 0 12px 30px #0003 }
.toolbar-title { display: flex; align-items: center; gap: 8px; margin-bottom: 10px } .toolbar-title b { font-size: 12px } .toolbar-title small { color: var(--mut); font-size: 10px }
.live { width: 7px; height: 7px; border-radius: 50%; background: var(--mi); box-shadow: 0 0 10px var(--mi); animation: pulse 2s infinite }
.tools { display: grid; grid-template-columns: repeat(auto-fill, minmax(92px, 1fr)); gap: 7px }
.tool { --t: #8ee6ff; display: flex; flex-direction: column; align-items: center; gap: 5px; padding: 9px 4px; border: 1px solid #2f4167; border-radius: 12px; background: #0b142b; color: #dbe6ff; cursor: pointer; transition: transform .2s, border-color .2s, background .2s }
.tool span { width: 30px; height: 30px; display: grid; place-items: center; border-radius: 10px; background: color-mix(in srgb, var(--t) 16%, #0b142b); color: var(--t); font-weight: 800; font-size: 15px; transition: transform .25s }
.tool b { font-size: 10px; font-weight: 600 } .tool:hover { transform: translateY(-3px); border-color: var(--t); background: #16213f } .tool:hover span { transform: rotate(-8deg) scale(1.1) }
.tool[data-type=callout] { --t: #ffd25c } .tool[data-type=quiz] { --t: #ff7d9b } .tool[data-type=formula] { --t: #b9a6ff } .tool[data-type=flashcard] { --t: #ff9f6b } .tool[data-type=image] { --t: #7df0cf } .tool[data-type=heading] { --t: #5be7ff }
.preview-bar { display: flex; align-items: center; justify-content: space-between }

.paper { margin: auto; border: 1px solid #34466f; border-radius: 24px; overflow: hidden; background: linear-gradient(150deg, #111b36, #0c1529); box-shadow: 0 25px 60px #0004; transition: max-width .4s cubic-bezier(.2, .8, .2, 1); max-width: 100% }
.paper.mobile { max-width: 400px }
.hero { --cover: #7055e8; position: relative; overflow: hidden; display: flex; align-items: center; gap: 20px; padding: 30px; min-height: 190px; background: radial-gradient(ellipse at 90% 0, #ffffff22, transparent 45%), linear-gradient(120deg, color-mix(in srgb, var(--cover) 62%, #0d1530), color-mix(in srgb, var(--cover) 22%, #121a3c) 70%); border-bottom: 1px solid #6c83c744 }
.hero::before { content: ''; position: absolute; width: 360px; height: 360px; border: 1px solid #ffffff1c; border-radius: 50%; right: -120px; top: -190px } .hero::after { content: ''; position: absolute; width: 250px; height: 250px; border: 1px solid #ffffff14; border-radius: 50%; right: -60px; top: -140px }
.hero-icon { width: 78px; height: 78px; flex: 0 0 78px; display: grid; place-items: center; font-size: 39px; border-radius: 24px; background: linear-gradient(145deg, #ffffff44, #ffffff14); border: 1px solid #ffffff55; box-shadow: 0 14px 34px #0005, inset 0 2px #ffffff77; animation: bob 4.5s ease-in-out infinite; backdrop-filter: blur(8px) }
.hero-copy { position: relative; min-width: 0 } .hero-copy small { font-size: 11px; color: #d6e4ff } .hero-copy h2 { font-size: clamp(20px, 2.3vw, 30px); margin: 8px 0 6px; line-height: 1.55; font-weight: 900 } .hero-copy p { margin: 0; font-size: 12px; color: #c9d7f4; line-height: 2 }
.mobile .hero { padding: 20px; gap: 13px } .mobile .hero-icon { width: 56px; height: 56px; flex-basis: 56px; font-size: 28px; border-radius: 17px } .mobile .hero-copy h2 { font-size: 18px }

.empty { display: grid; place-items: center; text-align: center; gap: 6px; padding: 54px 20px } .empty h3 { margin: 10px 0 0; font-size: 17px } .empty p { margin: 0 0 14px; color: var(--mut); font-size: 12px }
.empty-gem { width: 74px; height: 74px; display: grid; place-items: center; border-radius: 24px; font-size: 36px; color: var(--cy); border: 1px solid #6475c2; background: linear-gradient(145deg, #27365e, #191d40); animation: bob 4s infinite }

.blocks { padding: 18px; display: flex; flex-direction: column }
.blk-wrap { position: relative }
.block { --a: #7186df; position: relative; padding: 13px 15px 14px; border: 1px solid #2e4067; border-radius: 17px; background: linear-gradient(145deg, #172342, #10192f); transition: border-color .25s, box-shadow .25s, opacity .2s }
.block:hover { border-color: #43588c }
.block.active { border-color: transparent; background: linear-gradient(#141f3d, #0f182f) padding-box, conic-gradient(from var(--ang), #3a4a85 55%, var(--cy) 75%, var(--vi) 88%, #3a4a85) border-box; animation: spinAng 6s linear infinite; box-shadow: 0 14px 34px #0003 }
.block.dragging { opacity: .35 } .block.over { box-shadow: 0 -3px 0 var(--cy) }
.bar { display: flex; align-items: center; gap: 7px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px dashed #2c3d63 }
.bar b { font-size: 11px; color: #cdd9f6 } .spacer { flex: 1 }
.grip { cursor: grab; color: #6f86b8; font-size: 18px; padding: 0 3px; user-select: none } .grip:active { cursor: grabbing }
.num { min-width: 22px; height: 22px; display: grid; place-items: center; border-radius: 7px; background: #1e2c52; color: var(--cy); font-size: 10px; font-weight: 800 }
.bar button { width: 27px; height: 27px; border: 1px solid #33476f; border-radius: 8px; background: #0e1830; color: #aebde2; cursor: pointer; transition: .2s; font-size: 13px }
.bar button:hover:not(:disabled) { border-color: #7b8cff; background: #26345a; color: #fff } .bar button:disabled { opacity: .25 } .bar .danger { color: #ff8ca4; border-color: #63384e } .bar .danger:hover { background: #4a1f3a !important }
.heading-input { width: 100%; border: 0; border-bottom: 1px solid #35496f; background: transparent; color: #fff; font: 800 21px 'Vazirmatn', sans-serif; padding: 6px 0 11px; outline: none } .heading-input:focus { border-color: var(--cy) }
.row-opt { display: flex; align-items: center; gap: 10px; margin-top: 10px; font-size: 10px; color: var(--mut) }
.area { line-height: 2; margin: 0 } .quote { border-right: 3px solid #a58bff !important; border-radius: 0 10px 10px 0 !important; background: #1f1c3f !important }
.formula-box { display: flex; gap: 12px; align-items: center; padding: 11px; border: 1px solid #5c5b9d; border-radius: 13px; background: #201d43 } .formula-box > span { font-size: 22px; color: #b8a6ff } .formula-box .area { background: #151630 }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 12px 0 }
.chips button { padding: 6px 10px; border-radius: 9px; border: 1px solid #34476f; background: #0b142b; color: #b9c8ec; font-size: 10.5px; cursor: pointer; transition: .2s } .chips button.on { border-color: var(--cy); background: #17335a; color: #fff }

.callout-preview { --c: #8f7bff; position: relative; display: flex; gap: 12px; padding: 15px; border-radius: 15px; border: 1px solid transparent; background: linear-gradient(120deg, color-mix(in srgb, var(--c) 14%, #111a34), #111a34) padding-box, conic-gradient(from var(--ang), color-mix(in srgb, var(--c) 35%, transparent) 60%, var(--c) 80%, color-mix(in srgb, var(--c) 35%, transparent)) border-box; animation: spinAng 5s linear infinite; box-shadow: 0 0 24px color-mix(in srgb, var(--c) 14%, transparent) }
.callout-preview[data-style=definition] { --c: #19c5b2 } .callout-preview[data-style=warning] { --c: #ffd34f } .callout-preview[data-style=trap] { --c: #ff456a } .callout-preview[data-style=example] { --c: #4b8dff } .callout-preview[data-style=summary] { --c: #3ddc84 } .callout-preview[data-style=exam] { --c: #b07cff }
.callout-preview > span { width: 38px; height: 38px; flex: 0 0 38px; display: grid; place-items: center; border-radius: 12px; font-size: 19px; background: color-mix(in srgb, var(--c) 20%, #101a33) }
.callout-preview small { display: block; font-size: 10px; color: var(--c); font-weight: 700; margin-bottom: 2px } .callout-preview b { font-size: 13px } .callout-preview p { margin: 6px 0 0; font-size: 11.5px; line-height: 2.1; color: #d3dcf3 }

.opts { display: grid; gap: 7px; margin-bottom: 10px }
.opt { display: flex; align-items: center; gap: 8px; padding: 6px; border: 1px solid #3a3157; border-radius: 11px; background: #151330; transition: .2s } .opt.right { border-color: #2fcf9e; background: #10312f }
.opt > span { width: 26px; height: 26px; display: grid; place-items: center; border-radius: 8px; background: #38213d; color: #ff9bb0; font-size: 10px; font-weight: 800 } .opt.right > span { background: #1e7d66; color: #dcfff3 }
.opt input { flex: 1; min-width: 0; border: 0; background: transparent; color: #f2eaff; font: 12px 'Vazirmatn', sans-serif; outline: none; padding: 6px }
.opt .mark, .opt .x { border: 1px solid #4a3b66; border-radius: 8px; background: #231b3d; color: #b9aee0; cursor: pointer; font-size: 10px; padding: 5px 9px } .opt .mark.on { border-color: #2fcf9e; background: #13533f; color: #bfffe8 } .opt .x:disabled { opacity: .3 }
.img-prev { display: none; max-width: 100%; max-height: 300px; object-fit: contain; margin: 8px auto 0; border-radius: 12px; border: 1px solid #33476f }
.divider-prev { display: flex; align-items: center; gap: 12px; color: var(--cy) } .divider-prev i { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #5d76b4, transparent) }

.gap { position: relative; height: 22px; display: grid; place-items: center }
.gap-btn { width: 24px; height: 24px; border-radius: 50%; border: 1px dashed #43588c; background: #0e1830; color: #7f96d0; cursor: pointer; opacity: 0; transform: scale(.7); transition: .2s; line-height: 1 }
.blk-wrap:hover .gap-btn, .gap.open .gap-btn { opacity: 1; transform: scale(1) } .gap-btn:hover { border-color: var(--cy); color: var(--cy) }
.gap-menu { position: absolute; top: 26px; z-index: 6; display: flex; flex-wrap: wrap; justify-content: center; gap: 5px; max-width: 520px; padding: 9px; border: 1px solid #44599a; border-radius: 14px; background: #121c3cf5; box-shadow: 0 18px 40px #0007; animation: pop .22s cubic-bezier(.2, 1.4, .4, 1) }
.gap-menu button { display: flex; align-items: center; gap: 6px; padding: 6px 10px; border: 1px solid #34476f; border-radius: 9px; background: #0b142b; color: #d6e2ff; font-size: 10.5px; cursor: pointer } .gap-menu button:hover { border-color: var(--cy) } .gap-menu span { color: var(--cy) }
.paper-end { text-align: center; padding: 18px; font-size: 10px; letter-spacing: 1px; color: #5b73a8 }
.blk-move, .blk-enter-active, .blk-leave-active { transition: all .3s cubic-bezier(.2, .8, .2, 1) } .blk-enter-from { opacity: 0; transform: translateY(16px) scale(.98) } .blk-leave-to { opacity: 0; transform: translateX(-24px) } .blk-leave-active { position: absolute; width: calc(100% - 0px) }

/* preview */
.pv { gap: 14px; padding: 24px } .mobile .pv { padding: 16px }
.pv-h { margin: 14px 0 0; font-weight: 900; line-height: 1.7 } h2.pv-h { font-size: 26px } h3.pv-h { font-size: 21px } h4.pv-h { font-size: 17px } .pv-p { margin: 0; font-size: 14px; line-height: 2.3; color: #d1dcf7 }
.pv-p :deep(mark), .callout-preview :deep(mark) { background: #ffd25c33; color: #ffe9a6; padding: 0 4px; border-radius: 5px } .pv-p :deep(code), .callout-preview :deep(code) { direction: ltr; unicode-bidi: embed }
.pv-list { margin: 0; padding: 0 20px 0 0; line-height: 2.2; color: #d1dcf7 } .pv-check { display: grid; gap: 7px } .pv-check label { display: flex; gap: 9px; padding: 10px; border: 1px solid #2d4065; border-radius: 11px; background: #101a33; font-size: 12px }
.pv-formula { padding: 20px; text-align: center; font-size: 21px; font-weight: 800; border-radius: 15px; border: 1px solid #4a74a7; background: linear-gradient(130deg, #102c48, #25204e); white-space: pre-wrap; direction: ltr }
.pv-quote { margin: 0; padding: 16px 18px; border-right: 3px solid #a18bff; border-radius: 0 12px 12px 0; background: #242044; font-size: 14px; line-height: 2.1 }
.pv-quiz { padding: 16px; border: 1px solid #ff426b66; border-radius: 15px; background: linear-gradient(140deg, #29182d, #171a32); display: grid; gap: 7px } .pv-quiz > div { display: flex; gap: 9px; padding: 8px 10px; border-radius: 10px; background: #15172e; font-size: 12px } .pv-quiz > div.right { background: #123d3b; color: #bdffe6 } .pv-quiz span { color: #ff9bb0; font-weight: 800 }
.pv-item figure { margin: 0 } .pv-item img { max-width: 100%; border-radius: 13px; display: block; margin: auto } .pv-item figcaption { text-align: center; font-size: 11px; color: var(--mut); margin-top: 7px }
.flip { perspective: 900px; cursor: pointer; height: 150px } .flip-in { position: relative; height: 100%; transition: transform .6s cubic-bezier(.3, 1.2, .4, 1); transform-style: preserve-3d } .flip.on .flip-in { transform: rotateY(180deg) }
.face { position: absolute; inset: 0; display: grid; place-content: center; text-align: center; gap: 6px; padding: 18px; border-radius: 16px; font-size: 15px; font-weight: 700; backface-visibility: hidden; background: linear-gradient(135deg, #3a2a6e, #1c2a5c); border: 1px solid #8f7bff88 } .face small { font-size: 10px; color: #b8b0ee; font-weight: 400 } .face.back { transform: rotateY(180deg); background: linear-gradient(135deg, #0e4a4a, #1c2a5c); border-color: #4df0c088 }

.bottom-actions { display: flex; align-items: center; gap: 8px; margin-top: 16px; padding: 15px 17px; border: 1px solid var(--line); border-radius: 18px; background: #121c37 } .bottom-actions > div { flex: 1; display: flex; flex-direction: column; gap: 3px } .bottom-actions b { font-size: 12px } .bottom-actions small { font-size: 10px; color: var(--mut) }

/* states & toast */
.state { min-height: 70vh; display: grid; place-content: center; justify-items: center; gap: 14px; text-align: center } .state p { color: var(--mut); font-size: 12px; margin: 0 }
.loader { width: 70px; height: 70px; border-radius: 50%; border: 2px solid transparent; border-top-color: var(--cy); border-bottom-color: var(--vi); animation: spin 1.6s linear infinite; display: grid; place-items: center } .loader i { width: 12px; height: 12px; border-radius: 4px; background: var(--cy); box-shadow: 0 0 18px var(--cy) }
.lock { width: 64px; height: 64px; display: grid; place-items: center; border-radius: 20px; font-size: 28px; color: #ff9bc3; background: #3a243e; border: 1px solid #bb6693 }
.toast { position: fixed; z-index: 60; bottom: 24px; left: 24px; display: flex; align-items: center; gap: 10px; padding: 13px 18px; border-radius: 14px; border: 1px solid #6379b8; background: linear-gradient(120deg, #1e2b4d, #151c39); box-shadow: 0 15px 40px #0008; font-size: 12px } .toast span { color: var(--am); font-size: 18px }
.toast-enter-active { animation: pop .35s cubic-bezier(.2, 1.4, .4, 1) } .toast-leave-active { transition: .25s } .toast-leave-to { opacity: 0; transform: translateY(10px) }

@keyframes spinAng { to { --ang: 360deg } } @keyframes spin { to { transform: rotate(360deg) } }
@keyframes bob { 0%, 100% { transform: translateY(0) } 50% { transform: translateY(-6px) } }
@keyframes float { to { transform: translate(60px, -40px) scale(1.15) } } @keyframes drift { to { background-position: 0 1200px, 33px 1700px } }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 6px var(--mi) } 50% { box-shadow: 0 0 14px var(--mi) } }
@keyframes shine { 0%, 60% { transform: translateX(120%) } 100% { transform: translateX(-120%) } }
@keyframes pop { from { opacity: 0; transform: translateY(8px) scale(.92) } to { opacity: 1; transform: none } }

@media (max-width: 1100px) { .workspace { grid-template-columns: 1fr } .side { position: static; max-height: none } .save-state { display: none } .crumb { display: none } .top-tools { margin-right: auto } .toolbar { top: 70px } }
@media (max-width: 640px) { .grid2 { grid-template-columns: 1fr } .hero { padding: 18px; gap: 12px } .hero-icon { width: 54px; height: 54px; flex-basis: 54px; font-size: 27px; border-radius: 16px } .blocks { padding: 10px } .btn.quiet.top { display: none } .top-tools .seg button { padding: 6px 8px } .bar button { width: 30px; height: 30px } .toast { left: 12px; right: 12px; bottom: 12px } .tools { grid-template-columns: repeat(3, 1fr) } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important } }
</style>
