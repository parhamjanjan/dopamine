
<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import renderMathInElement from 'katex/contrib/auto-render'
import 'katex/dist/katex.min.css'

const props = defineProps({
  content: {
    type: String,
    default: '',
  },
})

const contentRef = ref(null)

async function renderMath() {
  await nextTick()

  if (!contentRef.value) return
  contentRef.value.textContent = props.content ?? ''

  // محتوای جدید ابتدا به‌صورت متن معمولی نمایش داده می‌شود.
  // سپس فقط عبارت‌های ریاضی مشخص‌شده رندر می‌شوند.
  try {
    renderMathInElement(contentRef.value, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
      ],
      throwOnError: false,
      trust: false,
      maxExpand: 100,
      maxSize: 10,
    })
  } catch (error) {
    console.error('خطا در رندر فرمول:', error)
  }
}

onMounted(renderMath)

watch(() => props.content, renderMath)
</script>

<template>
  <div
    ref="contentRef"
    class="math-content"
    dir="auto"
  >{{ content }}</div>
</template>

<style scoped>
.math-content {
  overflow-wrap: anywhere;
  line-height: 2;
}

.math-content :deep(.katex-display) {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0.5rem 0;
}

.math-content :deep(.katex) {
  direction: ltr;
  unicode-bidi: isolate;
}
</style>
