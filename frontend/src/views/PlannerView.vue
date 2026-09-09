<template>
<div class="custom-scrollbar dopamine-planner">
<nav>
  <div class="container flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-emerald-400 flex items-center justify-center animate-float">
        <i class="fas fa-graduation-cap text-white text-xl"></i>
      </div>
      <a href="/" style="-webkit-background-clip:text;background:linear-gradient(135deg,var(--primary),var(--green));color:white;" class="font-bold text-xl animate-slide-in-right logo-text">
        Dopamine
      </a>
    </div>
    <div class="flex items-center no-print">
      <button id="themeToggle" class="theme-toggle">
        <i class="fas fa-moon"></i>
      </button>
      <button id="printReportBtn" class="btn-primary">
        <i class="fas fa-print ml-2"></i>
        گزارش هفتگی
      </button>
    </div>
  </div>
</nav>

<div class="container">
  <div class="planner">
    <!-- Sidebar -->
    <div class="sidebar custom-scrollbar" style="overflow-x: hidden;" id="sidebar">
      <div class="mb-8 animate-fade-in">
        <button class="btn-primary w-full mb-6" id="addListBtn">
            <i class="fas fa-plus ml-2"></i>
            لیست جدید
        </button>
        <input type="text" class="add-task-input" placeholder="جستجو در تسک‌ها..." id="searchInput">
      </div>
      
      <div class="!mb-8">
        <div class="list-item active" data-view="inbox" id="view-inbox">
            <div class="list-item-content">
                <i class="fas fa-inbox ml-3" style="font-size: 14px;"></i>
                <span style="font-size: 14px;" >صندوق ورودی</span>
                <span class="list-count" id="inbox-count">0</span>
            </div>
        </div>
        <div class="list-item" data-view="today" id="view-today">
            <div class="list-item-content">
                <i class="fas fa-calendar-day ml-3" style="color: #10b981;font-size: 14px;"></i>
                <span style="font-size: 14px;" >امروز</span>
                <span class="list-count" id="today-count">0</span>
            </div>
        </div>
        <div class="list-item" data-view="week" id="view-week">
            <div class="list-item-content">
                <i class="fas fa-calendar-week ml-3" style="color: #f59e0b; font-size: 14px;"></i>
                <span style="font-size: 14px;" >هفته جاری</span>
                <span class="list-count" id="week-count">0</span>
            </div>
        </div>
        <div class="list-item" data-view="important" id="view-important">
            <div class="list-item-content">
                <i class="fas fa-star ml-3" style="color: #ef4444;font-size: 14px;"></i>
                <span style="font-size: 14px;" >مهم</span>
                <span class="list-count" id="important-count">0</span>
            </div>
        </div>
        <div class="list-item" data-view="league" id="view-league">
            <div class="list-item-content">
                <i class="fas fa-trophy ml-3" style="color: #f59e0b;font-size: 14px;"></i>
                <span style="font-size: 14px;" >لیگ مطالعاتی</span>
            </div>
        </div>
      </div>
      
      <div class="mb-6">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-semibold text-slate-400">لیست‌های درسی</h3>
        </div>
        <div id="study-lists"><!-- JS fills here --></div>
      </div>
      
      <div>
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-semibold text-slate-400">لیست‌های شخصی</h3>
        </div>
        <div id="personal-lists"><!-- JS fills here --></div>
      </div>
    </div>

    <!-- MAIN -->
    <div class="main">
      <!-- stats -->
      <div class="stats-grid mb-6" style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:24px">
        <div class="stat-card animate-fade-in" style="animation-delay: 0.1s">
          <div class="text-3xl font-bold" id="total-study-time">0</div>
          <div class="text-sm text-slate-400">ساعت مطالعه این هفته</div>
        </div>
        <div class="stat-card animate-fade-in" style="animation-delay: 0.2s">
          <div class="text-3xl font-bold" id="completed-tasks">0</div>
          <div class="text-sm text-slate-400">تسک‌های تکمیل شده</div>
        </div>
        <div class="stat-card animate-fade-in" style="animation-delay: 0.3s">
          <div class="text-3xl font-bold" id="productivity-score">0%</div>
          <div class="text-sm text-slate-400">امتیاز بهره‌وری</div>
        </div>
      </div>

      <!-- weekly planner -->
      <div class="weekly-planner mb-6">
        <div class="flex justify-between items-center">
          <button id="prev-week" class="btn-primary animate-slide-in-left"><i class="fas fa-chevron-right ml-2"></i> هفته قبل</button>
          <h3 class="section-title text-xl font-bold" id="current-week">هفته جاری</h3>
          <button id="next-week" class="btn-primary animate-slide-in-right">هفته بعد <i class="fas fa-chevron-left mr-2"></i></button>
        </div>

        <div class="week-days" id="week-days"></div>
      </div>

      <!-- لیگ مطالعاتی -->
      <div id="league-view" style="display: none;">

        <div class="league-section">
          <!-- در بخش league-header تغییر دهید -->
<div class="league-header">
  <div class="league-title">
    <i class="fas fa-trophy league-icon" id="league-icon"></i>
    <span id="league-name">لیگ آموزشی</span>
  </div>
  <div class="flex items-center gap-3">
    <span id="league-points">امتیاز: 0</span>
    <button id="predictionSettingsBtn" class="btn-primary py-2 px-3 text-sm">
      <i class="fas fa-cog ml-1"></i>
      تنظیمات پیش‌بینی
    </button>
  </div>
</div>

          <div class="league-info">
            <div class="league-stat">
              <div class="league-stat-value" id="daily-hours">0</div>
              <div class="league-stat-label">میانگین روزانه (ساعت)</div>
            </div>
            <div class="league-stat">
              <div class="league-stat-value" id="weekly-hours">0</div>
              <div class="league-stat-label">مجموع هفتگی (ساعت)</div>
            </div>
            <div class="league-stat">
              <div class="league-stat-value" id="streak-days">0</div>
              <div class="league-stat-label">روزهای متوالی</div>
            </div>
          </div>

          <div class="league-progress">
            <div class="league-progress-bar" id="league-progress-bar" style="width: 0%;"></div>
          </div>

          <div class="flex justify-between items-center mb-3">
            <div class="text-sm">پیشرفت به لیگ بعدی</div>
            <div class="text-sm font-bold" id="league-next">0%</div>
          </div>

          <div class="badges-container" id="badges-container">
            <!-- نشان‌ها اینجا نمایش داده می‌شوند -->
          </div>
        </div>

        <!-- بخش جدید: پیش‌بینی نمره آزمون -->
        <div class="league-section grade-prediction-section">
          <h3 class="section-title mb-4 flex items-center gap-3">
            <i class="fas fa-chart-line text-green-500"></i>
            پیش‌بینی نمره آزمون‌های آخر هفته
          </h3>
          <div class="grade-prediction" id="grade-prediction">
            <!-- پیش‌بینی نمره دروس اینجا نمایش داده می‌شود -->
          </div>
        </div>

        <div class="league-section">
          <h3 class="section-title mb-4 flex items-center gap-3">
            <i class="fas fa-award text-yellow-500"></i>
            دستاوردهای شما
          </h3>
          <div class="league-rankings flex" id="league-rankings">
            <!-- دستاوردهای کاربر اینجا نمایش داده می‌شود -->
          </div>
        </div>
      </div>

      <!-- charts -->
      <div class="charts-container">
        <div class="chart-card">
          <div class="chart-title mb-4 text-lg font-semibold"><i class="fas fa-chart-line ml-2"></i> ساعات مطالعه هفته جاری</div>
          <div class="chart-wrapper">
            <canvas id="studyTimeChart"></canvas>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-title mb-4 text-lg font-semibold"><i class="fas fa-tasks ml-2"></i> پیشرفت درسی</div>
          <div class="chart-wrapper">
            <canvas id="progressChart"></canvas>
          </div>
        </div>
      </div>

      <!-- tasks -->
      <div id="tasks-view">
        <div class="section-title mb-6">
          <i class="fas fa-inbox ml-2"></i>
          <span id="current-list-title" class="text-xl font-bold animate-fade-in">صندوق ورودی</span>
        </div>

        <!-- بخش تشخیص خودکار دسته‌بندی -->
        <div class="auto-category-detection" id="auto-category-detection">
          <div class="flex items-center gap-3 mb-3">
            <i class="fas fa-robot text-green-500"></i>
            <span class="font-semibold">تشخیص خودکار دسته‌بندی</span>
          </div>
          <div class="detected-category" id="detected-category">
            <!-- تشخیص دسته‌بندی اینجا نمایش داده می‌شود -->
          </div>
        </div>

        <div class="mb-6 flex gap-4">
          <input type="text" id="new-task-input" class="add-task-input" placeholder="اضافه کردن تسک (برای تشخیص خودکار عنوان را وارد کنید)..." />
          <button id="openTaskModal" class="btn-primary">افزودن</button>
        </div>

        <div class="task-list" id="task-list"></div>

        <div class="mt-8 animate-fade-in" id="completed-section" style="animation-delay: 0.2s">
          <div class="section-title">
            <i class="ml-2 fas fa-check-circle text-green-500"></i>
            <span>تکمیل شده (<span id="completed-count">0</span>)</span>
          </div>
          <div id="completed-tasks-list"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- نوتیفیکیشن -->
<div class="notification" id="notification">
  <div class="notification-icon">
    <i class="fas fa-bell"></i>
  </div>
  <div class="notification-content">
    <div class="notification-title font-bold" id="notification-title">یادآوری</div>
    <div class="notification-message text-sm" id="notification-message">زمان مطالعه شما به پایان رسید!</div>
  </div>
  <button class="notification-close" id="notification-close">
    <i class="fas fa-times"></i>
  </button>
</div>

<!-- صفحه گزارش هفتگی -->
<div class="print-report" id="printReport">
  <div class="print-page">
    <div class="print-header">
      <h1>گزارش هفتگی فعالیت‌های آموزشی</h1>
      <div class="print-meta">
        <div id="report-week-range">هفته: -</div>
        <div id="report-generation-date">تاریخ تولید: -</div>
      </div>
    </div>

    <div class="print-summary">
      <h3>خلاصه عملکرد هفتگی</h3>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 15px;">
        <div style="text-align: center;">
          <div style="font-size: 22px; font-weight: bold; color: #4f46e5;" id="report-total-tasks">0</div>
          <div style="font-size: 14px; color: #666;">تعداد تسک‌ها</div>
        </div>
        <div style="text-align: center;">
          <div style="font-size: 22px; font-weight: bold; color: #10b981;" id="report-total-time">0 ساعت</div>
          <div style="font-size: 14px; color: #666;">مجموع زمان مطالعه</div>
        </div>
        <div style="text-align: center;">
          <div style="font-size: 22px; font-weight: bold; color: #f59e0b;" id="report-avg-time">0 ساعت</div>
          <div style="font-size: 14px; color: #666;">میانگین روزانه</div>
        </div>
      </div>
    </div>

    <table class="print-table">
      <thead>
        <tr>
          <th>ردیف</th>
          <th>عنوان تسک</th>
          <th>دسته‌بندی</th>
          <th>تاریخ انجام</th>
          <th>زمان مطالعه</th>
          <th>اولویت</th>
          <th>توضیحات</th>
        </tr>
      </thead>
      <tbody id="report-tasks-table">
        <!-- داده‌های تسک‌ها اینجا پر می‌شود -->
      </tbody>
    </table>

    <div class="print-summary">
      <h3>توزیع زمانی بر اساس روزهای هفته</h3>
      <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; margin-top: 15px; font-size: 14px;">
        <!-- داده‌های توزیع زمانی اینجا پر می‌شود -->
      </div>
    </div>

    <div class="print-footer">
      <p>این گزارش به صورت خودکار توسط Dopamine تولید شده است</p>
      <p>تاریخ تولید: <span id="report-footer-date">-</span></p>
    </div>
  </div>
</div>

<!-- Modals -->
<div class="modal" id="listModal">
  <div class="modal-content">
    <div class="modal-header">
      <div>
        <h2 class="text-lg font-bold" id="listModalTitle">ایجاد لیست جدید</h2>
        <p class="modal-subtitle">اطلاعات لیست را وارد کنید.</p>
      </div>
      <button type="button" class="modal-close" data-close-modal="listModal" aria-label="بستن">×</button>
    </div>
    <h2 class="sr-only" aria-hidden="true">ایجاد لیست جدید</h2>
    <div class="mb-4">
      <label class="block mb-2 text-sm font-semibold">نام لیست</label>
      <input id="listNameInput" class="form-input" placeholder="مثال: ریاضیات">
    </div>
    <div class="mb-4">
      <label class="block mb-2 text-sm font-semibold">نوع لیست</label>
      <select id="listTypeInput" class="form-input">
        <option value="study">📚 لیست درسی</option>
        <option value="personal">🏠 لیست شخصی</option>
      </select>
    </div>
    <div class="mb-6">
      <label class="block mb-2 text-sm font-semibold">رنگ</label>
      <input id="listColorInput" type="color" class="form-input" value="#8b5cf6">
    </div>
    <div class="flex justify-end gap-3">
      <button id="saveListBtn" class="btn-primary">ذخیره</button>
      <button id="cancelListBtn" class="btn-primary" style="background:transparent;border:2px solid var(--border-color)">لغو</button>
    </div>
  </div>
</div>

<div class="modal w-full" id="taskModal">
  <div class="modal-content w-full" style="margin-bottom: 5rem;">
    <div class="modal-header">
      <div>
        <h2 class="text-lg font-bold" id="taskModalTitle">ایجاد تسک جدید</h2>
        <p class="modal-subtitle">جزئیات فعالیت و زمان‌بندی را تنظیم کنید.</p>
      </div>
      <button type="button" class="modal-close" data-close-modal="taskModal" aria-label="بستن">×</button>
    </div>
    
    <div class="space-y-3 max-h-[70vh] overflow-y-auto pr-2 custom-scrollbar w-full">
      <!-- Title -->
      <div>
        <label class="block mb-1 text-sm font-semibold">عنوان</label>
        <input id="taskTitleInput" class="form-input py-2" placeholder="عنوان تسک">
      </div>
      
      <!-- Description -->
      <div>
        <label class="block mb-1 text-sm font-semibold">توضیحات</label>
        <textarea id="taskDescriptionInput" class="form-input py-2" rows="2" placeholder="توضیحات اختیاری"></textarea>
      </div>
      
      <!-- Date and Study Time in one row -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label class="block mb-1 text-sm font-semibold">تاریخ سررسید</label>
          <input id="taskDueDateInput" type="date" class="form-input py-2">
        </div>
        <div>
          <label class="block mb-1 text-sm font-semibold">زمان مطالعه</label>
          <div class="flex gap-2">
            <input id="taskStudyTimeInput" type="number" class="form-input py-2 flex-1" min="0" step="0.5" value="1" placeholder="مقدار">
            <select id="taskTimeUnitInput" class="form-input py-2 w-24" style="width:60%">
              <option value="hours">ساعت</option>
              <option value="minutes">دقیقه</option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- Start and End Time -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label class="block mb-1 text-sm font-semibold">زمان شروع</label>
          <input id="taskStartTimeInput" type="time" class="form-input py-2">
        </div>
        <div>
          <label class="block mb-1 text-sm font-semibold">یادآوری</label>
          <select id="taskReminderInput" class="form-input py-2">
            <option value="none">بدون یادآوری</option>
            <option value="5">۵ دقیقه قبل</option>
            <option value="10">۱۰ دقیقه قبل</option>
            <option value="15">۱۵ دقیقه قبل</option>
            <option value="30">۳۰ دقیقه قبل</option>
            <option value="60">۱ ساعت قبل</option>
          </select>
        </div>
      </div>
      
      <!-- Reminder and Time Category -->
      
      
      <!-- Category -->
      <div>
        <label class="block mb-1 text-sm font-semibold">دسته‌بندی</label>
        <select id="taskCategoryInput" class="form-input py-2"></select>
      </div>
    </div>
    
    <!-- Buttons -->
    <div class="flex justify-end gap-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
      <button id="saveTaskBtn" class="btn-primary px-4 py-2">
        <i class="fas fa-save ml-2"></i>
        ذخیره
      </button>
      <button id="cancelTaskBtn" class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
        لغو
      </button>
    </div>
  </div>
</div>
<!-- مودال تنظیمات پیش‌بینی -->
<div class="modal" id="predictionSettingsModal">
  <div class="modal-content">
    <div class="modal-header">
      <div>
        <h2 class="text-lg font-bold">تنظیمات پیش‌بینی نمره</h2>
        <p class="modal-subtitle">تنظیمات پیش‌بینی عملکرد درسی را مدیریت کنید.</p>
      </div>
      <button type="button" class="modal-close" data-close-modal="predictionSettingsModal" aria-label="بستن">×</button>
    </div>
    
    <div class="mb-6">
      <label class="block mb-3 text-sm font-semibold">انتخاب دروس برای پیش‌بینی</label>
      <div class="space-y-3" id="subject-selection">
        <!-- دروس اینجا اضافه می‌شوند -->
      </div>
    </div>
    
    <div class="mb-6">
      <label class="block mb-2 text-sm font-semibold">روش پیش‌بینی</label>
      <select id="predictionMethodSelect" class="form-input">
        <option value="simple">ساده (بر اساس ساعات مطالعه)</option>
        <option value="advanced">پیشرفته (ساعات + کیفیت + زمان)</option>
      </select>
    </div>
    
    <div class="mb-6">
      <label class="block mb-2 text-sm font-semibold">درصد هدف برای پیش‌بینی</label>
      <input type="range" id="targetPercentageSlider" min="50" max="100" step="5" value="70" class="w-full">
      <div class="flex justify-between text-sm text-slate-400 mt-2">
        <span>50%</span>
        <span id="targetPercentageValue">70%</span>
        <span>100%</span>
      </div>
    </div>
    
    <div class="flex justify-end gap-3">
      <button id="savePredictionSettingsBtn" class="btn-primary">ذخیره تنظیمات</button>
      <button id="cancelPredictionSettingsBtn" class="btn-primary" style="background:transparent;border:2px solid var(--border-color)">لغو</button>
    </div>
  </div>
</div>
</div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '../stores/auth'
import {
  getTasks as apiGetTasks,
  createTask as apiCreateTask,
  updateTask as apiUpdateTask,
  deleteTask as apiDeleteTask,
  getLists as apiGetLists,
  createList as apiCreateList,
  updateList as apiUpdateList,
  deleteList as apiDeleteList
} from '../services/planner'

const auth = useAuthStore()


let predictionSettings = JSON.parse(localStorage.getItem('plannerPredictionSettings') || '{}');
if (!Object.keys(predictionSettings).length) {
  predictionSettings = { enabledSubjects: [], predictionMethod: 'advanced', targetPercentage: 70 };
}
let tasks = [];
let lists = [];
let userStats = JSON.parse(localStorage.getItem('plannerUserStats') || '{}');
if (!Object.keys(userStats).length) {
  userStats = { dailyHours:0, weeklyHours:0, streak:0, league:'training', points:0, lastStudyDate:null, completedTasks:0, badges:[], studyHistory:{} };
}
let currentWeek = 0;
let currentView = 'inbox';
let currentCategory = '';
let editingListId = null;
let editingTaskId = null;
let currentTheme = localStorage.getItem('plannerTheme') || document.documentElement.getAttribute('data-theme') || (document.documentElement.classList.contains('dark') ? 'dark' : 'light');
let reminderTimeouts = [];
const todayDate = new Date().toISOString().split('T')[0];
let studyChart = null, progressChart = null;
let chartReady = false;
let themeObserver = null;

function saveAll(){
  localStorage.setItem('plannerUserStats', JSON.stringify(userStats));
  localStorage.setItem('plannerPredictionSettings', JSON.stringify(predictionSettings));
}
function genId(){ return Date.now().toString(36) + Math.random().toString(36).slice(2,8); }
function todayISO(){ return new Date().toISOString().split('T')[0]; }
function isoDate(d){ return new Date(d).toISOString().split('T')[0]; }


let personalListIds = new Set();

function loadPersonalListIds() {
  try {
    const raw = JSON.parse(localStorage.getItem('plannerPersonalListIds') || '[]');
    personalListIds = new Set(Array.isArray(raw) ? raw.map(String) : []);
  } catch {
    personalListIds = new Set();
  }
}

function isPersonalList(list) {
  return personalListIds.has(String(list.id));
}

function taskCategoryId(task) {
  return task?.category == null ? '' : String(task.category);
}

function normalizeTask(raw) {
  const plannerList = raw?.planner_list ?? null;
  return {
    id: raw.id,
    title: raw.title || '',
    description: raw.description || '',
    completed: !!raw.completed,
    important: !!raw.important,
    category: plannerList !== null && plannerList !== undefined ? String(plannerList) : String(raw.category || ''),
    plannerList,
    dueDate: raw.due_date || '',
    startTime: raw.start_time ? String(raw.start_time).slice(0,5) : null,
    endTime: raw.end_time ? String(raw.end_time).slice(0,5) : null,
    reminder: raw.reminder || 'none',
    timeCategory: raw.time_category || '',
    studyTime: parseFloat(raw.study_time) || 0,
    createdAt: raw.created_at,
    updatedAt: raw.updated_at
  };
}

function normalizeList(raw) {
  if (!raw || raw.id == null) return null;
  return {
    ...raw,
    id: String(raw.id),
    name: String(raw.name ?? '').trim(),
    color: raw.color || '#64748b'
  };
}

function normalizeLists(rawLists) {
  return (Array.isArray(rawLists) ? rawLists : [])
    .map(normalizeList)
    .filter(Boolean);
}

async function refreshListsFromBackend() {
  const rawLists = await apiGetLists();
  lists = normalizeLists(rawLists);
  return lists;
}

function toApiTask(task) {
  const listId = task.category ? Number(task.category) : null;
  return {
    title: task.title,
    description: task.description || '',
    completed: !!task.completed,
    important: !!task.important,
    category: task.category || '',
    due_date: task.dueDate || null,
    start_time: task.startTime || null,
    end_time: task.endTime || null,
    reminder: task.reminder || 'none',
    time_category: task.timeCategory || '',
    study_time: Number(task.studyTime) || 0,
    planner_list: Number.isFinite(listId) ? listId : null
  };
}

async function syncTask(task) {
  const payload = toApiTask(task);
  const saved = task.id && typeof task.id === 'number'
    ? await apiUpdateTask(task.id, payload)
    : await apiCreateTask(payload);
  return normalizeTask(saved);
}

function detectCategoryFromTitle(title) {
  if (!title || typeof title !== 'string') return null;
  const normalized = title.trim().toLowerCase();
  let best = null;
  let score = 0;
  lists.forEach(list => {
    const name = String(list.name || '').toLowerCase();
    const words = name.split(/\s+/).filter(w => w.length > 2);
    let s = 0;
    if (name && normalized.includes(name)) s += 3;
    words.forEach(word => { if (normalized.includes(word)) s += 1; });
    if (s > score) { score = s; best = String(list.id); }
  });
  return score >= 2 ? best : null;
}
function showCategoryDetection(categoryId) {
  const detectionDiv = document.getElementById('auto-category-detection');
  const detectedCategoryDiv = document.getElementById('detected-category');
  if (!categoryId) { detectionDiv.style.display='none'; return; }
  const list = lists.find(l => String(l.id) === String(categoryId));
  if (!list) { detectionDiv.style.display='none'; return; }
  detectionDiv.style.display='block';
  detectedCategoryDiv.innerHTML = `<i class="fas ${getCategoryIcon(categoryId)}" style="color:${escapeHtml(list.color)}"></i><span>تشخیص خودکار: <strong>${escapeHtml(list.name)}</strong></span><button class="btn-primary ml-auto py-1 px-3 text-sm" id="applyDetectedCategoryBtn">اعمال</button>`;
  document.getElementById('applyDetectedCategoryBtn')?.addEventListener('click', () => applyDetectedCategory(categoryId));
}


function applyDetectedCategory(categoryId) {
  const select = document.getElementById('taskCategoryInput');
  if (select) {
    if(select.value != categoryId){
    select.value = categoryId;
    }
  }
}

/* ---------------------------
   سیستم پیش‌بینی نمره آزمون
   --------------------------- */
function calculateGradePredictions() {
  const weekDates = getCurrentWeekDates(currentWeek);
  const predictions = [];
  
  // فقط دروس فعال را بررسی کن
  const activeLists = lists.filter(list => 
    !isPersonalList(list) && // درس‌های غیردرسی را حذف کن
    predictionSettings.enabledSubjects.includes(list.id) // فقط دروس فعال
  );
  
  activeLists.forEach(list => {
    const studyHours = tasks
      .filter(t => t.completed && String(t.category || "") === String(list.id) && t.dueDate && weekDates.includes(t.dueDate))
      .reduce((sum, task) => sum + (parseFloat(task.studyTime) || 0), 0);
    
    // تعداد تسک‌های انجام شده
    const completedTasks = tasks.filter(t => 
      t.completed && 
      String(t.category || "") === String(list.id) && 
      t.dueDate && 
      weekDates.includes(t.dueDate) &&
      (!t.dueDate || new Date(t.dueDate) <= new Date())
    ).length;
    
    const totalTasks = tasks.filter(t => 
      String(t.category || "") === String(list.id) && 
      t.dueDate && 
      weekDates.includes(t.dueDate)
    ).length;
    
    let predictedPercentage = 0;
    
    // انتخاب روش پیش‌بینی
    if (predictionSettings.predictionMethod === 'simple') {
      // روش ساده: فقط بر اساس ساعات مطالعه
      predictedPercentage = Math.min(100, (studyHours / 10) * 100);
    } else {
      // روش پیشرفته
      const prediction = calculateAdvancedPrediction(studyHours, completedTasks, totalTasks);
      predictedPercentage = prediction.total;
    }
    
    predictions.push({
      subject: list.name,
      subjectId: list.id,
      hours: studyHours,
      predictedPercentage: Math.round(predictedPercentage * 10) / 10,
      grade: studyHours > 0 ? calculateGradeFromPercentage(predictedPercentage) : 0,
      completedTasks: completedTasks,
      totalTasks: totalTasks,
      color: list.color
    });
  });
  

  return predictions;
}


// تابع کمکی برای محاسبه نمره از درصد
function calculateGradeFromPercentage(percentage) {
  // تبدیل درصد به نمره 20 (یک رقم اعشار)
  const grade = (percentage / 100) * 20;
  return Math.round(grade * 10) / 10;
}

  
// تابع برای باز کردن مودال تنظیمات
function openPredictionSettingsModal() {
  const modal = document.getElementById('predictionSettingsModal');
  const subjectSelection = document.getElementById('subject-selection');
  
  // پر کردن لیست دروس
  subjectSelection.innerHTML = '';
  

  // اضافه کردن سایر دروس
  lists.forEach(list => {
    const subjectDiv = document.createElement('div');
    subjectDiv.className = 'prediction-subject-option flex items-center gap-3 p-3 rounded-lg';
    subjectDiv.innerHTML = `
      <input type="checkbox" id="subject-${list.id}" class="w-5 h-5 rounded" ${predictionSettings.enabledSubjects.includes(list.id) ? 'checked' : ''}>
      <label for="subject-${list.id}" class="flex-1 cursor-pointer">
        <i class="fas ${getCategoryIcon(list.id)} ml-2" style="color: ${list.color}"></i>
        ${list.name}
      </label>
    `;
    subjectSelection.appendChild(subjectDiv);
  });
  
  // تنظیم مقادیر فعلی
  document.getElementById('predictionMethodSelect').value = predictionSettings.predictionMethod;
  document.getElementById('targetPercentageSlider').value = predictionSettings.targetPercentage;
  document.getElementById('targetPercentageValue').textContent = predictionSettings.targetPercentage + '%';
  
  // رویداد برای اسلایدر
  document.getElementById('targetPercentageSlider').addEventListener('input', function() {
    document.getElementById('targetPercentageValue').textContent = this.value + '%';
  });
  
  modal.style.display = 'flex';
}

// تابع برای ذخیره تنظیمات
function savePredictionSettings() {
  const enabledSubjects = [];
  
  // جمع‌آوری دروس انتخاب شده
  document.querySelectorAll('#subject-selection input[type="checkbox"]:checked').forEach(checkbox => {
    const subjectId = checkbox.id.replace('subject-', '');
    enabledSubjects.push(subjectId);
  });
  
  predictionSettings.enabledSubjects = enabledSubjects;
  predictionSettings.predictionMethod = document.getElementById('predictionMethodSelect').value;
  predictionSettings.targetPercentage = parseInt(document.getElementById('targetPercentageSlider').value);
  
  localStorage.setItem('plannerPredictionSettings', JSON.stringify(predictionSettings));
  closeModal('predictionSettingsModal');
  
  // به‌روزرسانی نمایش پیش‌بینی
  if (currentView === 'league') {
    renderGradePredictions();
  }
  
  showNotification('تنظیمات ذخیره شد', 'تنظیمات پیش‌بینی با موفقیت ذخیره شدند.');
}

// تابع پیشرفته برای پیش‌بینی
function calculateAdvancedPrediction(studyHours, completedTasks, totalTasks, daysUntilExam = 7) {
  let basePercentage = 0;
  
  // بخش اول: ساعات مطالعه (حداکثر 60%)
  if (studyHours > 0) {
    // فرمول: هر ساعت مطالعه 4% (تا 15 ساعت = 60%)
    basePercentage = Math.min(60, studyHours * 4);
  }
  
  // بخش دوم: کیفیت انجام تسک‌ها (حداکثر 25%)
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) : 0;
  const qualityBonus = completionRate * 25;
  
  // بخش سوم: فاکتور زمان باقی‌مانده (حداکثر 15%)
  const timeFactor = Math.min(15, daysUntilExam * 2); // هر روز 2% شانس بیشتر
  
  // مجموع
  const totalPercentage = Math.min(100, basePercentage + qualityBonus + timeFactor);
  
  return {
    base: Math.round(basePercentage),
    quality: Math.round(qualityBonus),
    time: Math.round(timeFactor),
    total: Math.round(totalPercentage)
  };
}



function renderGradePredictions() {
  const container = document.getElementById('grade-prediction');
  if (!container) return;

  const predictions = calculateGradePredictions();
  container.innerHTML = '';

  if (predictions.length === 0) {
    container.innerHTML = `
      <div class="prediction-empty">
        <div class="prediction-empty-icon"><i class="fas fa-chart-line"></i></div>
        <div class="prediction-empty-title">هنوز پیش‌بینی‌ای برای نمایش نداریم</div>
        <div class="prediction-empty-copy">دروس موردنظر را از تنظیمات انتخاب کنید تا پیش‌بینی نمره بر اساس عملکرد این هفته ساخته شود.</div>
        <button id="openSettingsFromEmpty" class="btn-primary mt-4 py-2 px-4">
          <i class="fas fa-sliders ml-2"></i>
          تنظیمات پیش‌بینی
        </button>
      </div>
    `;
    document.getElementById('openSettingsFromEmpty')?.addEventListener('click', openPredictionSettingsModal);
    return;
  }

  const getStatus = (percentage) => {
    if (percentage >= 90) return { className:'status-excellent', color:'#2563eb', icon:'fa-circle-check', text:'عملکرد عالی' };
    if (percentage >= predictionSettings.targetPercentage) return { className:'status-success', color:'#059669', icon:'fa-bullseye', text:'هدف محقق شده' };
    if (percentage >= predictionSettings.targetPercentage * 0.7) return { className:'status-warning', color:'#d97706', icon:'fa-chart-line', text:'در مسیر هدف' };
    return { className:'status-danger', color:'#dc2626', icon:'fa-arrow-trend-down', text:'نیاز به تلاش بیشتر' };
  };

  predictions.forEach((prediction, index) => {
    const status = getStatus(prediction.predictedPercentage);
    const target = Math.max(1, predictionSettings.targetPercentage || 1);
    const targetProgress = Math.min(100, Math.round((prediction.predictedPercentage / target) * 100));
    const grade = Number(prediction.grade || 0).toFixed(1);
    const completed = Number(prediction.completedTasks || 0);
    const total = Number(prediction.totalTasks || 0);
    const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;
    const subjectColor = prediction.color || '#64748b';
    const icon = getCategoryIcon(prediction.subjectId);

    const gradeCard = document.createElement('div');
    gradeCard.className = `grade-card ${status.className}`;
    gradeCard.style.animationDelay = `${index * 70}ms`;
    gradeCard.style.setProperty('--subject-color', `color-mix(in srgb, ${subjectColor} 12%, transparent)`);
    gradeCard.style.setProperty('--progress', `${prediction.predictedPercentage}%`);

    gradeCard.innerHTML = `
      <div class="grade-card-head">
        <div class="grade-subject-icon" style="--subject-color: color-mix(in srgb, ${subjectColor} 12%, transparent)">
          <i class="fas ${icon}"></i>
        </div>
        <div class="grade-subject-wrap">
          <div class="grade-subject">${prediction.subject}</div>
          <span class="grade-status"><i class="fas ${status.icon}"></i>${status.text}</span>
        </div>
        <button class="grade-remove" type="button" aria-label="حذف درس" onclick="toggleSubjectPrediction('${prediction.subjectId}')">
          <i class="fas fa-xmark"></i>
        </button>
      </div>

      <div class="grade-main">
        <div class="grade-ring" style="--progress:${prediction.predictedPercentage}%;">
          <div class="grade-ring-content">
            <span class="grade-ring-value">${Math.round(prediction.predictedPercentage)}%</span>
            <span class="grade-ring-label">پیش‌بینی</span>
          </div>
        </div>

        <div class="grade-score-meta">
          <div class="grade-score-label">نمره احتمالی</div>
          <div class="grade-score">${grade}<small>/20</small></div>
          <div class="grade-target-copy">هدف شما: <strong>${predictionSettings.targetPercentage}%</strong> • تحقق هدف: <strong>${targetProgress}%</strong></div>
        </div>
      </div>

      <div class="grade-progress" aria-label="پیشرفت نسبت به هدف">
        <div class="grade-progress-bar" style="width:${Math.min(100, prediction.predictedPercentage)}%; background:${status.color}"></div>
      </div>

      <div class="grade-target-row">
        <span>سطح پیش‌بینی</span>
        <strong>${targetProgress}% از هدف</strong>
      </div>

      <div class="grade-details">
        <div class="grade-detail">
          <span class="grade-detail-value">${prediction.hours.toFixed(1)} ساعت</span>
          <span class="grade-detail-label">مطالعه</span>
        </div>
        <div class="grade-detail">
          <span class="grade-detail-value">${completed}</span>
          <span class="grade-detail-label">تسک انجام‌شده</span>
        </div>
        <div class="grade-detail">
          <span class="grade-detail-value">${completionRate}%</span>
          <span class="grade-detail-label">نرخ تکمیل</span>
        </div>
      </div>
    `;

    container.appendChild(gradeCard);
  });
}

// تابع برای حذف یک درس از پیش‌بینی
function toggleSubjectPrediction(subjectId) {
  if (confirm('آیا می‌خواهید این درس را از پیش‌بینی حذف کنید؟')) {
    predictionSettings.enabledSubjects = predictionSettings.enabledSubjects.filter(id => id !== subjectId);
    localStorage.setItem('plannerPredictionSettings', JSON.stringify(predictionSettings));
    
    if (currentView === 'league') {
      renderGradePredictions();
    }
    
    showNotification('درس حذف شد', `درس از لیست پیش‌بینی حذف شد.`);
  }
}

/* ---------------------------
   سیستم لیگ مطالعاتی
   --------------------------- */
function updateUserStats() {
  const today = todayISO();
  const weekDates = getCurrentWeekDates(currentWeek);
  
  // محاسبه ساعات مطالعه هفته جاری
  const weeklyHours = tasks
    .filter(t => t.completed && t.dueDate && weekDates.includes(t.dueDate))
    .reduce((sum, task) => sum + (parseFloat(task.studyTime) || 0), 0);
  
  // محاسبه میانگین روزانه
  const dailyHours = weeklyHours / 7;
  
  // محاسبه استمرار بر اساس روزهایی که حداقل 4 ساعت مطالعه داشته‌اید
  const streak = calculateStudyStreak();
  
  // محاسبه امتیاز
  let points = Math.round(weeklyHours * 10); // 10 امتیاز به ازای هر ساعت مطالعه
  
  // تعیین لیگ بر اساس ساعات مطالعه
  let league = 'training';
  if (weeklyHours >= 50) {
    league = 'legendary';
  } else if (weeklyHours >= 40) {
    league = 'professional';
  } else if (weeklyHours >= 30) {
    league = 'beginner';
  }
  
  // به‌روزرسانی آمار کاربر
  userStats.dailyHours = dailyHours;
  userStats.weeklyHours = weeklyHours;
  userStats.streak = streak;
  userStats.league = league;
  userStats.points = points;
  userStats.lastStudyDate = today;
  userStats.completedTasks = tasks.filter(t => t.completed).length;
  
  // ذخیره تاریخچه مطالعه
  if (!userStats.studyHistory) userStats.studyHistory = {};
  userStats.studyHistory[today] = weeklyHours;
  
  // بررسی نشان‌ها
  checkBadges();
  
  saveAll();
}

function calculateStudyStreak() {
  // تاریخ‌های 30 روز گذشته
  const dates = [];
  for (let i = 0; i < 30; i++) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(isoDate(date));
  }
  
  // محاسبه ساعات مطالعه برای هر روز
  const dailyStudy = {};
  dates.forEach(date => {
    dailyStudy[date] = tasks
      .filter(t => t.completed && t.dueDate === date)
      .reduce((sum, task) => sum + (parseFloat(task.studyTime) || 0), 0);
  });
  
  // محاسبه استمرار از امروز به عقب
  let streak = 0;
  const today = todayISO();
  
  for (let i = 0; i < dates.length; i++) {
    const date = dates[i];
    const studyHours = dailyStudy[date] || 0;
    
    // اگر امروز است و هنوز مطالعه نکرده‌اید، ادامه دهید
    if (date === today && studyHours === 0) {
      continue;
    }
    
    // اگر روزی با حداقل 4 ساعت مطالعه پیدا شد
    if (studyHours >= 4) {
      streak++;
    } else {
      // اگر روزی با کمتر از 4 ساعت مطالعه پیدا شد، استمرار قطع می‌شود
      break;
    }
  }
  
  return streak;
}

function checkBadges() {
  const badges = [];
  
  // استمرار هفتگی (7 روز متوالی با حداقل 4 ساعت مطالعه در روز)
  if (userStats.streak >= 7) {
    badges.push({ id: 'streak-7', name: 'استمرار هفتگی', icon: 'fa-fire', description: '۷ روز مطالعه متوالی با حداقل ۴ ساعت در روز' });
  }
  
  // استمرار ماهانه (30 روز متوالی با حداقل 4 ساعت مطالعه در روز)
  if (userStats.streak >= 30) {
    badges.push({ id: 'streak-30', name: 'استمرار ماهانه', icon: 'fa-calendar', description: '۳۰ روز مطالعه متوالی با حداقل ۴ ساعت در روز' });
  }
  
  // مطالعه‌گر حرفه‌ای
  if (userStats.weeklyHours >= 50) {
    badges.push({ id: 'study-50', name: 'مطالعه‌گر حرفه‌ای', icon: 'fa-graduation-cap', description: '۵۰ ساعت مطالعه در هفته' });
  }
  
  // مطالعه‌گر افسانه‌ای
  if (userStats.weeklyHours >= 100) {
    badges.push({ id: 'study-100', name: 'مطالعه‌گر افسانه‌ای', icon: 'fa-crown', description: '۱۰۰ ساعت مطالعه در هفته' });
  }
  
  // تسک مستر
  if (userStats.completedTasks >= 100) {
    badges.push({ id: 'task-master', name: 'تسک مستر', icon: 'fa-tasks', description: 'تکمیل ۱۰۰ تسک' });
  }
  
  // پرنده سحرخیز
  const earlyBirdTasks = tasks.filter(t => {
    if (!t.startTime || !t.completed) return false;
    const [hours] = t.startTime.split(':').map(Number);
    return hours < 7;
  });
  
  if (earlyBirdTasks.length >= 10) {
    badges.push({ id: 'early-bird', name: 'پرنده سحرخیز', icon: 'fa-sun', description: 'مطالعه قبل از ۷ صبح' });
  }
  
  // بررسی نشان‌های جدید
  badges.forEach(badge => {
    if (!userStats.badges.some(b => b.id === badge.id)) {
      userStats.badges.push(badge);
      showNotification('🎉 تبریک!', `نشان "${badge.name}" را دریافت کردید!`);
    }
  });
  
  saveAll();
}

function renderLeagueView() {
  updateUserStats();
  
  // به‌روزرسانی اطلاعات لیگ
  document.getElementById('league-name').textContent = getLeagueName(userStats.league);
  document.getElementById('league-icon').className = `fas ${getLeagueIcon(userStats.league)} league-icon`;
  document.getElementById('league-points').textContent = `امتیاز: ${userStats.points}`;
  document.getElementById('daily-hours').textContent = userStats.dailyHours.toFixed(1);
  document.getElementById('weekly-hours').textContent = userStats.weeklyHours.toFixed(1);
  document.getElementById('streak-days').textContent = userStats.streak;
  
  // محاسبه پیشرفت به لیگ بعدی
  const progress = calculateLeagueProgress();
  document.getElementById('league-progress-bar').style.width = `${progress}%`;
  document.getElementById('league-progress-bar').style.background = getLeagueColor(userStats.league);
  document.getElementById('league-next').textContent = `${progress}%`;
  
  // نمایش نشان‌ها
  renderBadges();
  
  // نمایش پیش‌بینی نمره
  renderGradePredictions();
  
  // نمایش دستاوردها
  renderAchievements();
}

function getLeagueName(league) {
  const names = {
    'legendary': 'افسانه‌ای',
    'professional': 'حرفه‌ای',
    'beginner': 'مبتدی',
    'training': 'آموزشی'
  };
  return names[league] || 'آموزشی';
}

function getLeagueIcon(league) {
  const icons = {
    'legendary': 'fa-crown',
    'professional': 'fa-medal',
    'beginner': 'fa-award',
    'training': 'fa-user-graduate'
  };
  return icons[league] || 'fa-user-graduate';
}

function getLeagueColor(league) {
  const colors = {
    'legendary': '#ffd700',
    'professional': '#c0c0c0',
    'beginner': '#cd7f32',
    'training': '#4f46e5'
  };
  return colors[league] || '#4f46e5';
}

function calculateLeagueProgress() {
  // محاسبه پیشرفت به لیگ بعدی بر اساس ساعات مطالعه
  const nextLeagueThreshold = getNextLeagueThreshold();
  if (!nextLeagueThreshold) return 100;
  
  const progress = (userStats.weeklyHours / nextLeagueThreshold) * 100;
  return Math.min(100, Math.round(progress));
}

function getNextLeagueThreshold() {
  // آستانه‌های لیگ‌ها
  const thresholds = {
    'training': 30,
    'beginner': 40,
    'professional': 50,
    'legendary': null // بالاترین لیگ
  };
  
  return thresholds[userStats.league];
}

function renderBadges() {
  const container = document.getElementById('badges-container');
  container.innerHTML = '';
  
  if (userStats.badges.length === 0) {
    container.innerHTML = '<div class="text-slate-400 text-center py-6">هنوز هیچ نشان‌ای دریافت نکرده‌اید</div>';
    return;
  }
  
  userStats.badges.forEach(badge => {
    const badgeEl = document.createElement('div');
    badgeEl.className = 'badge bg-gradient-to-r from-green-500 to-emerald-600 text-white';
    badgeEl.title = badge.description;
    badgeEl.style.animationDelay = `${Math.random() * 0.3}s`;
    
    badgeEl.innerHTML = `
      <i class="fas ${badge.icon} badge-icon"></i>
      <span>${badge.name}</span>
    `;
    
    container.appendChild(badgeEl);
  });
}

function renderAchievements() {
  const container = document.getElementById('league-rankings');
  container.innerHTML = '';
  
  const achievements = [
    {
      title: 'تسک‌های تکمیل شده',
      value: userStats.completedTasks,
      target: 100,
      icon: 'fa-check-circle',
      color: '#10b981'
    },
    {
      title: 'روزهای متوالی مطالعه',
      value: userStats.streak,
      target: 30,
      icon: 'fa-fire',
      color: '#f59e0b'
    },
    {
      title: 'ساعت مطالعه این هفته',
      value: userStats.weeklyHours,
      target: 50,
      icon: 'fa-clock',
      color: '#4f46e5'
    },
    {
      title: 'میانگین روزانه',
      value: userStats.dailyHours,
      target: 7,
      icon: 'fa-chart-line',
      color: '#8b5cf6'
    }
  ];
  
  achievements.forEach((achievement, index) => {
    const progress = Math.min(100, (achievement.value / achievement.target) * 100);
    
    const achievementEl = document.createElement('div');
    achievementEl.className = 'ranking-card hover-3d';
    achievementEl.style.animationDelay = `${index * 0.1}s`;
    
    achievementEl.innerHTML = `
      <div class="ranking-avatar" style="background: ${achievement.color}">
        <i class="fas ${achievement.icon}"></i>
      </div>
      <div class="ranking-info">
        <div class="ranking-name">${achievement.title}</div>
        <div class="ranking-stats">${achievement.value.toFixed(1)} از ${achievement.target}</div>
        <div class="league-progress mt-3">
          <div class="league-progress-bar" style="width: ${progress}%; background: ${achievement.color}"></div>
        </div>
      </div>
      <div class="ranking-position">${Math.round(progress)}%</div>
    `;
    
    container.appendChild(achievementEl);
  });
}

/* ---------------------------
   مدیریت تم
   --------------------------- */
function detectCurrentTheme() {
  const root = document.documentElement;
  const dataTheme = root.getAttribute('data-theme');
  if (dataTheme === 'dark' || dataTheme === 'light') return dataTheme;
  return root.classList.contains('dark') ? 'dark' : 'light';
}

function applyPlannerTheme(theme) {
  const nextTheme = theme === 'dark' ? 'dark' : 'light';
  currentTheme = nextTheme;
  document.documentElement.setAttribute('data-theme', nextTheme);
  localStorage.setItem('plannerTheme', nextTheme);
  updateThemeToggle();
  if (chartReady) renderCharts();
}

function updateThemeToggle() {
  const themeToggle = document.getElementById('themeToggle');
  if (!themeToggle) return;
  const isDark = detectCurrentTheme() === 'dark';
  themeToggle.innerHTML = isDark
    ? '<i class="fas fa-sun"></i>'
    : '<i class="fas fa-moon"></i>';
  themeToggle.setAttribute('aria-label', isDark ? 'فعال‌سازی حالت روشن' : 'فعال‌سازی حالت تاریک');
  themeToggle.setAttribute('title', isDark ? 'حالت روشن' : 'حالت تاریک');
}

function initTheme() {
  const existingTheme = detectCurrentTheme();
  const storedTheme = localStorage.getItem('plannerTheme');
  const preferredTheme = storedTheme || existingTheme || currentTheme;

  if (preferredTheme === 'dark' || preferredTheme === 'light') {
    currentTheme = preferredTheme;
    document.documentElement.setAttribute('data-theme', preferredTheme);
    localStorage.setItem('plannerTheme', preferredTheme);
  } else {
    currentTheme = 'light';
    document.documentElement.setAttribute('data-theme', 'light');
  }

  updateThemeToggle();
  if (chartReady) renderCharts();
}

function toggleTheme() {
  applyPlannerTheme(detectCurrentTheme() === 'dark' ? 'light' : 'dark');
}

function watchExternalThemeChanges() {
  const root = document.documentElement;
  const observer = new MutationObserver(() => {
    const detected = detectCurrentTheme();
    if (detected !== currentTheme) {
      currentTheme = detected;
      updateThemeToggle();
      if (chartReady) renderCharts();
    }
  });

  observer.observe(root, {
    attributes: true,
    attributeFilter: ['class', 'data-theme', 'style']
  });

  return observer;
}

/* ---------------------------
   مدیریت یادآوری‌ها
   --------------------------- */
function setupReminders() {
  // پاک کردن تمام یادآوری‌های قبلی
  reminderTimeouts.forEach(timeout => clearTimeout(timeout));
  reminderTimeouts = [];

  const now = new Date();
  
  tasks.forEach(task => {
    if (task.completed || !task.startTime || !task.dueDate) return;
    
    // ترکیب تاریخ و زمان شروع
    const startDateTime = new Date(`${task.dueDate}T${task.startTime}`);
    
    // اگر زمان شروع در گذشته است، از آن صرف نظر کن
    if (startDateTime <= now) return;
    
    // تنظیم یادآوری اصلی
    const timeUntilStart = startDateTime - now;
    if (timeUntilStart > 0) {
      const timeout = setTimeout(() => {
        showNotification('یادآوری تسک', `زمان شروع تسک "${task.title}" فرا رسیده است.`);
        playNotificationSound();
      }, timeUntilStart);
      
      reminderTimeouts.push(timeout);
    }
    
    // تنظیم یادآوری زودتر از موعد (اگر تنظیم شده باشد)
    if (task.reminder && task.reminder !== 'none') {
      const reminderMinutes = parseInt(task.reminder);
      const reminderTime = startDateTime - (reminderMinutes * 60 * 1000);
      const timeUntilReminder = reminderTime - now;
      
      if (timeUntilReminder > 0) {
        const reminderTimeout = setTimeout(() => {
          showNotification('یادآوری تسک', `تسک "${task.title}" در ${reminderMinutes} دقیقه دیگر شروع می‌شود.`);
          playNotificationSound();
        }, timeUntilReminder);
        
        reminderTimeouts.push(reminderTimeout);
      }
    }
  });
}

/* ---------------------------
   مدیریت نوتیفیکیشن
   --------------------------- */
function showNotification(title, message) {
  const notification = document.getElementById('notification');
  const notificationTitle = document.getElementById('notification-title');
  const notificationMessage = document.getElementById('notification-message');
  
  notificationTitle.textContent = title;
  notificationMessage.textContent = message;
  
  notification.classList.add('show');
  
  // نمایش نوتیفیکیشن مرورگر
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification(title, { body: message, icon: '/favicon.ico' });
  }
  
  // پخش صدا
  playNotificationSound();
  
  // بسته شدن خودکار پس از 5 ثانیه
  setTimeout(() => {
    hideNotification();
  }, 5000);
}

function hideNotification() {
  const notification = document.getElementById('notification');
  notification.classList.remove('show');
}

function playNotificationSound() {
  // ایجاد صدا با Web Audio API
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.type = 'sine';
    oscillator.frequency.value = 800;
    gainNode.gain.value = 0.1;
    
    oscillator.start();
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);
    oscillator.stop(audioContext.currentTime + 1);
  } catch (e) {
    console.log('صدا پخش نشد:', e);
  }
}

/* ---------------------------
   Helpers
   --------------------------- */
function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function getCategoryName(id){
  if (!id) return 'بدون لیست';
  const l = lists.find(x => String(x.id) === String(id));
  return l ? l.name : 'لیست حذف‌شده';
}
function getCategoryIcon(id){ 
  
  return 'fa-list'; 
}
function getCategoryColor(id){ 
  const l = lists.find(x=>x.id===id); 
  return l ? l.color : '#6b7280'; 
}
function formatShort(dateStr){ 
  if(!dateStr) return 'بدون تاریخ'; 
  try { 
    return new Date(dateStr).toLocaleDateString('fa-IR'); 
  } catch(e){ 
    return dateStr; 
  } 
}

// تابع جدید برای فرمت کردن زمان برای نمایش
function formatTimeForDisplay(hours) {
  if (hours < 1) {
    const minutes = Math.round(hours * 60);
    return `${minutes} دقیقه`;
  } else if (hours === Math.floor(hours)) {
    return `${hours} ساعت`;
  } else {
    const wholeHours = Math.floor(hours);
    const minutes = Math.round((hours - wholeHours) * 60);
    if (wholeHours === 0) {
      return `${minutes} دقیقه`;
    } else {
      return `${wholeHours} ساعت و ${minutes} دقیقه`;
    }
  }
}

// تابع برای فرمت کردن زمان شروع
function formatStartTime(task) {
  if (!task.startTime) return '';
  
  const now = new Date();
  const today = todayISO();
  const taskDate = task.dueDate || today;
  
  if (taskDate === today) {
    const [hours, minutes] = task.startTime.split(':');
    const taskTime = new Date();
    taskTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    
    if (taskTime > now) {
      return `<span class="task-time-badge upcoming"><i class="fas fa-clock ml-1"></i>امروز ${task.startTime}</span>`;
    } else {
      return `<span class="task-time-badge past"><i class="fas fa-clock ml-1"></i>امروز ${task.startTime}</span>`;
    }
  } else {
    return `<span class="task-time-badge"><i class="fas fa-clock ml-1"></i>${formatShort(taskDate)} ${task.startTime}</span>`;
  }
}

/* ---------------------------
   تابع جدید برای تعیین دسته‌بندی زمانی بر اساس زمان پایان
   --------------------------- */
function getTimeCategory(startTime) {
  if (!startTime) return 'no-time';
  
  const [hours, minutes] = startTime.split(':').map(Number);
  const totalMinutes = hours * 60 + minutes;
  
  // دسته‌بندی‌های زمانی بر اساس زمان پایان
  if (totalMinutes < 600) { // قبل از 10:00
    return 'morning';
  } else if (totalMinutes < 840) { // قبل از 14:00
    return 'noon';
  } else if (totalMinutes < 1080) { // قبل از 18:00
    return 'afternoon';
  } else if (totalMinutes < 1320) { // قبل از 22:00
    return 'evening';
  } else { // قبل از 2:00 روز بعد
    return 'midnight';
  }
}

// تابع برای محاسبه زمان پایان بر اساس زمان شروع و مدت مطالعه
function calculateEndTime(startTime, studyTime) {
  if (!startTime || !studyTime) return '';
  
  const [hours, minutes] = startTime.split(':').map(Number);
  const totalMinutes = hours * 60 + minutes + (studyTime * 60);
  
  // محاسبه ساعت و دقیقه جدید
  let newHours = Math.floor(totalMinutes / 60) % 24;
  const newMinutes = totalMinutes % 60;
  
  // فرمت کردن به فرمت HH:MM
  return `${newHours.toString().padStart(2, '0')}:${newMinutes.toString().padStart(2, '0')}`;
}

/* ---------------------------
   Improved startOfWeek function
   --------------------------- */
function startOfWeek(refDate, offsetWeeks = 0) {
  const d = new Date(refDate);
  // تنظیم به شروع هفته (شنبه)
  let day = d.getDay(); // 0=یکشنبه, 1=دوشنبه, ..., 6=شنبه
  // تبدیل به تقویم ایرانی: شنبه=0, یکشنبه=1, ..., جمعه=6
  let iranDay = (day) % 7;
  
  const start = new Date(d);
  start.setDate(d.getDate() - iranDay + (offsetWeeks * 7));
  start.setHours(0, 0, 0, 0);
  return start;
}

// تابع برای محاسبه تاریخ‌های هفته جاری
function getCurrentWeekDates(offsetWeeks = 0) {
  const start = startOfWeek(new Date(), offsetWeeks);
  const dates = [];
  for (let i = 0; i < 7; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    dates.push(isoDate(date));
  }
  return dates;
}

/* ---------------------------
   Render sidebar lists (with 3-dot menu for edit/delete)
   --------------------------- */
function renderSidebarLists(){
  const studyEl = document.getElementById('study-lists');
  const personalEl = document.getElementById('personal-lists');
  if (!studyEl || !personalEl) return;

  studyEl.innerHTML = '';
  personalEl.innerHTML = '';

  if (lists.length === 0) {
    studyEl.innerHTML = '<div class="muted text-slate-400 text-sm text-center py-4">هنوز لیستی از سرور دریافت نشده است</div>';
    return;
  }

  lists.forEach((l, index) => {
    const tasksCount = tasks.filter(t => !t.completed && String(t.category || '') === String(l.id)).length;
    const completedCount = tasks.filter(t => t.completed && String(t.category || '') === String(l.id)).length;

    const el = document.createElement('div');
    el.className = 'list-item animate-scale-in flex text-sm';
    el.style.display = 'flex';
    el.style.animationDelay = `${index * 0.05}s`;
    el.dataset.category = l.id;

    const left = document.createElement('div');
    left.className = 'list-item-content';
    left.innerHTML = `<i class="fas ${getCategoryIcon(l.id)} ml-3" style="color:${l.color}"></i><span>${escapeHtml(l.name)}</span><span class="list-count">${tasksCount}</span>`;

    const controls = document.createElement('div');
    controls.style.display = 'flex';
    controls.className = 'list-controls';
    controls.style.zIndex = '1';
    controls.innerHTML = `
      <button class="list-menu-btn" title="بیشتر"><i class="fas fa-ellipsis-v"></i></button>
      <div class="list-menu z-50" style="margin-left:1.25rem; margin-top:-4.25rem">
        <button class="edit-list">ویرایش</button>
        <button class="delete-list text-red-400">حذف</button>
      </div>
    `;

    const completedDiv = document.createElement('div');
    completedDiv.className = 'flex items-center gap-1 ml-3';
    completedDiv.innerHTML = `<span class="text-xs text-green-400 completed-count">${completedCount}</span>`;

    el.appendChild(left);
    el.appendChild(completedDiv);
    el.appendChild(controls);

    left.addEventListener('click', () => setActiveView('category', l.id));

    controls.querySelector('.edit-list')?.addEventListener('click', (e) => {
      e.stopPropagation();
      openListModal(l.id);
    });

    controls.querySelector('.delete-list')?.addEventListener('click', async (e) => {
      e.stopPropagation();
      if (!confirm(`آیا از حذف لیست "${l.name}" و تمام تسک‌هایش مطمئنی؟`)) return;

      try {
        const related = tasks.filter(t => String(t.category || '') === String(l.id));
        await Promise.all(related.map(t => apiDeleteTask(t.id)));
        await apiDeleteList(l.id);

        tasks = tasks.filter(t => String(t.category || '') !== String(l.id));
        personalListIds.delete(String(l.id));
        localStorage.setItem('plannerPersonalListIds', JSON.stringify([...personalListIds]));

        await refreshListsFromBackend();

        if (currentView === 'category' && String(currentCategory) === String(l.id)) {
          setActiveView('inbox');
        }

        renderAll();
      } catch (error) {
        showNotification('خطا', 'حذف لیست انجام نشد.');
        console.error(error);
      }
    });

    if (isPersonalList(l)) personalEl.appendChild(el);
    else studyEl.appendChild(el);
  });

  if (!studyEl.children.length) {
    studyEl.innerHTML = '<div class="muted text-slate-400 text-sm text-center py-4">لیست درسی‌ای از سرور دریافت نشده است</div>';
  }

  if (!personalEl.children.length) {
    personalEl.innerHTML = '<div class="muted text-slate-400 text-sm text-center py-4">لیست شخصی‌ای از سرور دریافت نشده است</div>';
  }
}

/* ---------------------------
   Render tasks with time categories
   --------------------------- */
function renderTasks(){
  const taskList = document.getElementById('task-list');
  const completedListEl = document.getElementById('completed-tasks-list');
  taskList.innerHTML = '';
  if(completedListEl) completedListEl.innerHTML = '';

  let filtered = tasks.slice();
  const today = todayISO();

  if(currentView === 'today') filtered = filtered.filter(t => t.dueDate === today);
  else if(currentView === 'week'){
    const weekDates = getCurrentWeekDates(currentWeek);
    filtered = filtered.filter(t => t.dueDate && weekDates.includes(t.dueDate));
  } else if(currentView === 'important') filtered = filtered.filter(t => t.important);
  else if(currentView === 'category' && currentCategory) {
    if (!lists.some(l => String(l.id) === String(currentCategory))) {
      filtered = [];
    } else {
      filtered = filtered.filter(t => String(t.category || '') === String(currentCategory));
    }
  }

  // search
  const q = (document.getElementById('searchInput').value || '').toLowerCase().trim();
  if(q) filtered = filtered.filter(t => (t.title||'').toLowerCase().includes(q) || (t.description||'').toLowerCase().includes(q));

  const active = filtered.filter(t => !t.completed);
  const completed = filtered.filter(t => t.completed);

  // گروه‌بندی تسک‌ها بر اساس دسته‌بندی زمانی
  const timeCategories = {
    morning: { name: 'صبح', icon: 'fa-sun', tasks: [] },
    noon: { name: 'ظهر', icon: 'fa-cloud-sun', tasks: [] },
    afternoon: { name: 'غروب', icon: 'fa-sun', tasks: [] },
    evening: { name: 'شب', icon: 'fa-moon', tasks: [] },
    midnight: { name: 'نیمه‌شب', icon: 'fa-star', tasks: [] },
    'no-time': { name: 'بدون زمان', icon: 'fa-clock', tasks: [] }
  };

  // دسته‌بندی تسک‌های فعال
  active.forEach(task => {
    // اگر زمان پایان وجود دارد، از آن استفاده کن، در غیر این صورت از زمان شروع و مدت مطالعه محاسبه کن
    let endTime = task.endTime;
    
    
    const timeCategory = getTimeCategory(task.startTime);
    timeCategories[timeCategory].tasks.push(task);
  });

  // نمایش تسک‌ها بر اساس دسته‌بندی زمانی
  if(active.length === 0) {
    taskList.innerHTML = '<div class="text-slate-400 py-8 text-center"><i class="fas fa-tasks text-4xl mb-4"></i><div>هیچ تسکی یافت نشد</div></div>';
  } else {
    // نمایش دسته‌بندی‌های زمانی به ترتیب مشخص
    const categoryOrder = ['morning', 'noon', 'afternoon', 'evening', 'midnight', 'no-time'];
    
    categoryOrder.forEach((categoryKey, index) => {
      const category = timeCategories[categoryKey];
      if (category.tasks.length > 0) {
        const categoryEl = document.createElement('div');
        categoryEl.className = 'time-category expanded animate-fade-in';
        categoryEl.style.animationDelay = `${index * 0.1}s`;
        categoryEl.innerHTML = `
          <div class="time-category-header">
            <div class="time-category-title">
              <i class="fas ${category.icon} time-category-icon"></i>
              <span>${category.name}</span>
              <span class="time-category-count">${category.tasks.length}</span>
            </div>
          </div>
          <div class="time-category-content"></div>
        `;
        
        const contentEl = categoryEl.querySelector('.time-category-content');
        
        category.tasks.forEach((t, taskIndex) => {
  const el = document.createElement('div');
  el.className = '';
  el.draggable = true;
  el.dataset.taskId = t.id;
  el.style.animationDelay = `${taskIndex * 0.05}s`;
  el.innerHTML = `
  <div class="task-item new-item task-title-with-accordion" data-task-id="${t.id}" style="display:block;">
    <div class="flex items-center gap-4 left">
      <div class="task-checkbox ${t.completed ? 'checked' : ''}"></div>
      <div class="flex-1">
        
          <div class="flex items-center gap-2">
            <span class="task-title ${t.completed ? 'completed' : ''} font-medium">${t.title}</span>
            <i class="fas fa-chevron-down text-slate-400 text-xs transition-transform accordion-arrow"></i>
          </div>

          <div class="text-slate-400 text-xs flex items-center gap-3 flex-wrap">
          ${formatShort(t.dueDate)} 
          ${t.startTime ? '• ' + formatStartTime(t) : ''}
          ${t.endTime ? `• پایان: ${t.endTime}` : ''}
          • ${getCategoryName(t.category)} 
          • ${formatTimeForDisplay(t.studyTime||0)}
        </div>
        </div>
        
        <div class="flex items-center gap-4">
      <i class="fas fa-star ${t.important ? 'text-yellow-400 animate-pulse' : 'text-slate-400'} text-lg cursor-pointer star"></i>
      <i class="fas fa-pen text-sky-400 text-lg cursor-pointer edit"></i>
      <i class="fas fa-trash text-slate-400 text-lg cursor-pointer delete-task"></i>
    </div>
      </div>
      
      <div class="task-accordion" id="accordion-${t.id}">
          <div class="task-accordion-content">
            <div style=" white-space: pre-line;" class="task-description ${!t.description ? 'empty' : ''}">
              <span>${t.description ? t.description : 'توضیحاتی برای این تسک ثبت نشده است.'}</span>
            </div>
          </div>
        </div>
    
    </div>
    
  `;
  
  // events
  el.querySelector('.task-checkbox').addEventListener('click', ()=> toggleTaskCompletion(t.id));
  el.querySelector('.star').addEventListener('click', ()=> toggleTaskImportance(t.id));
  el.querySelector('.delete-task').addEventListener('click', ()=> { if(confirm('حذف؟')) deleteTask(t.id); });
  el.querySelector('.edit').addEventListener('click', ()=> openTaskModal(t.id));
  
  // رویداد کلیک برای باز کردن Accordion
  const accordionTrigger = el.querySelector('.task-title-with-accordion');
  accordionTrigger.addEventListener('click', (e) => {
    // جلوگیری از باز شدن وقتی روی چک‌بکس یا آیکون‌ها کلیک می‌شود
    if (e.target.closest('.task-checkbox') || e.target.closest('.star') || 
        e.target.closest('.edit') || e.target.closest('.delete-task')) {
      return;
    }
    
    const taskId = t.id;
    const accordion = el.querySelector(`#accordion-${taskId}`);
    const arrow = accordionTrigger.querySelector('.accordion-arrow');
    
    accordion.classList.toggle('expanded');
    arrow.classList.toggle('rotate-180');
  });

  // drag
  el.addEventListener('dragstart', (e) => { 
    e.dataTransfer.setData('text/plain', t.id); 
    el.classList.add('dragging'); 
  });
  el.addEventListener('dragend', () => el.classList.remove('dragging'));

  contentEl.appendChild(el);
});

        
        // کلیک برای باز/بسته کردن دسته‌بندی
        categoryEl.querySelector('.time-category-header').addEventListener('click', () => {
          categoryEl.classList.toggle('expanded');
        });
        
        taskList.appendChild(categoryEl);
      }
    });
  }

  // completed
  document.getElementById('completed-count').textContent = completed.length;
  completed.forEach((t, index) => {
    const el = document.createElement('div');
    el.className = 'task-item animate-scale-in';
    el.style.animationDelay = `${index * 0.05}s`;
    el.innerHTML = `
      <div class="flex items-center gap-4 left">
        <div class="task-checkbox checked"></div>
        <div class="flex-1">
          <div class="task-title completed font-medium mb-1">${t.title}</div>
          <div class="text-slate-400 text-xs flex items-center gap-3 flex-wrap">
            ${formatShort(t.dueDate)} • ${getCategoryName(t.category)} • ${formatTimeForDisplay(t.studyTime||0)}
          </div>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <i class="fas fa-undo text-sky-400 text-lg cursor-pointer undo"></i>
        <i class="fas fa-trash text-slate-400 text-lg cursor-pointer delete-task"></i>
      </div>
    `;
    el.querySelector('.undo').addEventListener('click', ()=> toggleTaskCompletion(t.id));
    el.querySelector('.delete-task').addEventListener('click', ()=> { if(confirm('حذف؟')) deleteTask(t.id); });
    if(completedListEl) completedListEl.appendChild(el);
  });

  updateSidebarCounts();
}
/* ---------------------------
   Weekly planner + drag/drop
   --------------------------- */
/* ---------------------------
   Weekly planner + drag/drop - تغییر این تابع
   --------------------------- */
function renderWeeklyPlanner(){
  const container = document.getElementById('week-days');
  container.innerHTML = '';
  const start = startOfWeek(new Date(), currentWeek);
  const days = ['شنبه','یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنجشنبه','جمعه'];
  const today = todayISO();

  for(let i=0;i<7;i++){
    const d = new Date(start); d.setDate(start.getDate()+i);
    const key = isoDate(d);
    const cell = document.createElement('div');
    cell.className = 'day-cell animate-scale-in' + (key === today ? ' today' : '');
    cell.style.animationDelay = `${i * 0.05}s`;
    cell.dataset.date = key;
    cell.innerHTML = `<div class="font-semibold mb-2">${days[i]}<br/><span class="text-slate-400 text-sm">${formatShort(key)}</span></div>`;

    // tasks for that date
    tasks.filter(t => t.dueDate === key && !t.completed).forEach(t => {
      const dt = document.createElement('div');
      
      // تغییر اصلی: اضافه کردن کلاس مهم برای تسک‌های مهم
      dt.className = 'day-task new-item' + (t.important ? ' important-task' : '');
      dt.draggable = true;
      dt.dataset.taskId = t.id;
      
      // تغییر: اضافه کردن آیکون ستاره برای تسک‌های مهم
      dt.innerHTML = `
        <div style="flex:1; display: flex; align-items: center; gap: 8px;">
          ${t.important ? '<i class="fas fa-star text-yellow-400 text-xs animate-pulse"></i>' : ''}
          <span>${t.title}</span>
        </div>
       
        <div class="delete-task-btn"><i class="fas fa-times"></i></div>
      `;

      // delete button
      dt.querySelector('.delete-task-btn').addEventListener('click', (e) => { 
        e.stopPropagation(); 
        if(confirm('حذف؟')) deleteTask(t.id); 
      });
      
      // drag
      dt.addEventListener('dragstart', (e) => { 
        e.dataTransfer.setData('text/plain', t.id); 
        dt.classList.add('dragging'); 
      });
      dt.addEventListener('dragend', () => dt.classList.remove('dragging'));
      
      cell.appendChild(dt);
    });

    // allow drop
    cell.addEventListener('dragover', (e) => { e.preventDefault(); cell.classList.add('drop-active'); });
    cell.addEventListener('dragleave', () => cell.classList.remove('drop-active'));
    cell.addEventListener('drop', async (e) => {
      e.preventDefault(); 
      cell.classList.remove('drop-active');
      const id = e.dataTransfer.getData('text/plain'); 
      if(!id) return;
      const t = tasks.find(x=>x.id===id); 
      if(!t) return;
      t.dueDate = cell.dataset.date;
      try { tasks[tasks.findIndex(x=>String(x.id)===String(t.id))] = normalizeTask(await apiUpdateTask(t.id, toApiTask(t))); } catch(error) { showNotification('خطا','جابجایی تسک ذخیره نشد.'); console.error(error); } 
      renderTasks(); 
      renderWeeklyPlanner(); 
      renderCharts(); 
      updateStats();
      setupReminders();
    });

    container.appendChild(cell);
  }

  // week title
  const end = new Date(start); end.setDate(start.getDate()+6);
  document.getElementById('current-week').textContent = `${formatShort(start.toISOString().split('T')[0])} — ${formatShort(end.toISOString().split('T')[0])}`;
}

/* ---------------------------
   Charts (use tasks, support fractional >1)
   --------------------------- */

function computeStudyByDateForCurrentWeek(){
  const week = ['شنبه' , 'یکشنبه' , 'دوشنبه' , 'سه‌شنبه' , 'چهارشنبه' , 'پنجشنبه' , 'جمعه']
  const weekDates = getCurrentWeekDates(currentWeek);
  const map = {};
  weekDates.forEach(date => { map[date] = 0; });
  console.log(map)
  tasks.filter(t => t.completed && t.dueDate && weekDates.includes(t.dueDate)).forEach(t => {
    const v = parseFloat(t.studyTime) || 0;
    map[t.dueDate] = (map[t.dueDate] || 0) + v;
  });
  
  return { dates: week, data: weekDates.map(date => map[date] || 0) };
}

// تابع جدید برای محاسبه درصد زمان مطالعه هر درس در هفته جاری
function computeStudyTimeByCategoryForCurrentWeek(){
  const weekDates = getCurrentWeekDates(currentWeek);
  
  // محاسبه کل زمان مطالعه هفته جاری
  const totalStudyTime = tasks
    .filter(t => t.completed && t.dueDate && weekDates.includes(t.dueDate))
    .reduce((sum, task) => sum + (parseFloat(task.studyTime) || 0), 0);
  
  // محاسبه زمان مطالعه برای هر دسته‌بندی در هفته جاری
  const categoryStudy = {};
  

  // دسته‌های درسی در هفته جاری
  lists.forEach(list => {
    const categoryTime = tasks
      .filter(t => t.completed && String(t.category || "") === String(list.id) && t.dueDate && weekDates.includes(t.dueDate))
      .reduce((sum, task) => sum + (parseFloat(task.studyTime) || 0), 0);
    
    if (categoryTime > 0) {
      categoryStudy[list.name] = {
        time: categoryTime,
        percentage: totalStudyTime > 0 ? (categoryTime / totalStudyTime * 100) : 0
      };
    }
  });
  
  return {
    categories: Object.keys(categoryStudy),
    percentages: Object.values(categoryStudy).map(item => Math.round(item.percentage)),
    times: Object.values(categoryStudy).map(item => item.time),
    totalStudyTime: totalStudyTime
  };
}

function readThemeColor(name, fallback) {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return value || fallback;
}

function readThemeRgb(name, fallback) {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return value || fallback;
}

function renderCharts(){
  if (!chartReady || !window.Chart) return;

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const chartText = isDark ? '#cbd5e1' : '#64748b';
  const chartGrid = isDark ? 'rgba(148,163,184,.10)' : 'rgba(100,116,139,.10)';
  const primary = readThemeColor('--primary', '#7055e8');
  const primaryRgb = readThemeRgb('--primary-rgb', '112,85,232');
  const primarySoft = `rgba(${primaryRgb},.16)`;
  const primaryFill = `rgba(${primaryRgb},.10)`;
  const success = '#10b981';
  const successFill = 'rgba(16,185,129,.10)';

  const weekData = computeStudyByDateForCurrentWeek();
  const labels = weekData.dates;
  const data = weekData.data;
  const maxVal = Math.max(1, ...data);
  const suggestedMax = Math.ceil(maxVal + 0.5);

  const canvas1 = document.getElementById('studyTimeChart');
  const canvas2 = document.getElementById('progressChart');
  if (!canvas1 || !canvas2) return;

  const ctx1 = canvas1.getContext('2d');
  if(studyChart) studyChart.destroy();
  try {
    studyChart = new window.Chart(ctx1, {
      type:'bar',
      data:{
        labels,
        datasets:[{
          label:'ساعات مطالعه',
          data,
          backgroundColor: primarySoft,
          borderColor: primary,
          borderWidth: 1.5,
          borderRadius: 7,
          hoverBackgroundColor: primary,
          hoverBorderColor: primary
        }]
      },
      options:{
        responsive:true,
        maintainAspectRatio:false,
        animation:{ duration:650, easing:'easeOutQuart' },
        scales:{
          y:{
            beginAtZero:true,
            max:suggestedMax,
            ticks:{ stepSize:0.5, color:chartText },
            title:{display:true,text:'ساعت',color:chartText},
            grid:{color:chartGrid}
          },
          x:{
            ticks:{color:chartText},
            grid:{color:chartGrid}
          }
        },
        plugins:{
          legend:{ labels:{color:chartText} }
        }
      }
    });
  } catch(e) { console.log(e); }

  const categoryData = computeStudyTimeByCategoryForCurrentWeek();
  const displayCategories = categoryData.categories.length > 0 ? categoryData.categories : ['هنوز داده‌ای وجود ندارد'];
  const displayPercentages = categoryData.percentages.length > 0 ? categoryData.percentages : [0];

  const ctx2 = canvas2.getContext('2d');
  if(progressChart) progressChart.destroy();
  try {
    progressChart = new window.Chart(ctx2, {
      type:'line',
      data:{
        labels:displayCategories,
        datasets:[{
          label:'درصد زمان مطالعه این هفته',
          data:displayPercentages,
          borderColor:success,
          backgroundColor:successFill,
          tension:0.35,
          fill:true,
          borderWidth:2,
          pointBackgroundColor:success,
          pointBorderColor:isDark ? '#111827' : '#ffffff',
          pointBorderWidth:2,
          pointRadius:5,
          pointHoverRadius:7
        }]
      },
      options:{
        responsive:true,
        maintainAspectRatio:false,
        animation:{duration:850,easing:'easeOutQuart'},
        scales:{
          y:{
            min:0,
            max:100,
            title:{display:true,text:'درصد',color:chartText},
            ticks:{color:chartText,callback:value => value + '%'},
            grid:{color:chartGrid}
          },
          x:{
            ticks:{color:chartText,maxRotation:45,minRotation:45},
            grid:{color:chartGrid}
          }
        },
        plugins:{
          tooltip:{
            callbacks:{
              label:function(context){
                if(categoryData.categories.length === 0) return 'هنوز داده‌ای برای این هفته وجود ندارد';
                const label=context.label || '';
                const value=context.raw || 0;
                const index=context.dataIndex;
                const hours=categoryData.times[index] || 0;
                return `${label}: ${value}% (${hours.toFixed(1)} ساعت)`;
              },
              afterLabel:function(){
                if(categoryData.categories.length > 0) return `کل زمان هفته: ${categoryData.totalStudyTime.toFixed(1)} ساعت`;
              }
            }
          },
          legend:{labels:{color:chartText}}
        }
      }
    });
  } catch(e) { console.log(e); }
}

/* ---------------------------
   Stats & sidebar counts
   --------------------------- */
function updateStats(){
  const weekDates = getCurrentWeekDates(currentWeek);
  const total = tasks.filter(t => t.completed && t.dueDate && weekDates.includes(t.dueDate))
                    .reduce((s,t)=> s + (parseFloat(t.studyTime)||0), 0);
  const done = tasks.filter(t=>t.completed).length;
  const prod = tasks.length ? Math.round(done / tasks.length * 100) : 0;
  document.getElementById('total-study-time').textContent = total.toFixed(1);
  document.getElementById('completed-tasks').textContent = done;
  document.getElementById('productivity-score').textContent = prod + '%';
}

function updateSidebarCounts(){
  const today = todayISO();
  const weekLater = new Date(); weekLater.setDate(weekLater.getDate()+7); const weekLaterStr = weekLater.toISOString().split('T')[0];
  document.getElementById('inbox-count').textContent = tasks.filter(t => !t.completed).length;
  document.getElementById('today-count').textContent = tasks.filter(t => t.dueDate === today && !t.completed).length;
  document.getElementById('week-count').textContent = tasks.filter(t => t.dueDate && t.dueDate >= today && t.dueDate <= weekLaterStr && !t.completed).length;
  document.getElementById('important-count').textContent = tasks.filter(t => t.important && !t.completed).length;

  // list counts
  lists.forEach(l => {
    const el = document.querySelector(`#study-lists [data-category="${l.id}"] .list-count`) || document.querySelector(`#personal-lists [data-category="${l.id}"] .list-count`);
    if(el) el.textContent = tasks.filter(t => t.category === l.id && !t.completed).length;
  });
}

/* ---------------------------
   Task actions
   --------------------------- */
async function toggleTaskCompletion(id){
  const index = tasks.findIndex(x=>String(x.id)===String(id));
  if(index < 0) return;
  const old = { ...tasks[index] };
  const next = { ...tasks[index], completed: !tasks[index].completed };
  if(next.completed && !next.dueDate) next.dueDate = todayISO();
  tasks[index] = next;
  renderAll();
  try {
    tasks[index] = normalizeTask(await apiUpdateTask(next.id, toApiTask(next)));
    updateUserStats();
    renderAll();
  } catch(error) {
    tasks[index] = old;
    renderAll();
    showNotification('خطا', 'ذخیره وضعیت تسک انجام نشد.');
    console.error(error);
  }
}
async function toggleTaskImportance(id){
  const index = tasks.findIndex(x=>String(x.id)===String(id));
  if(index < 0) return;
  const old = { ...tasks[index] };
  tasks[index] = { ...tasks[index], important: !tasks[index].important };
  renderAll();
  try {
    tasks[index] = normalizeTask(await apiUpdateTask(tasks[index].id, toApiTask(tasks[index])));
    renderAll();
  } catch(error) {
    tasks[index] = old;
    renderAll();
    showNotification('خطا', 'تغییر اولویت ذخیره نشد.');
    console.error(error);
  }
}
async function deleteTask(id){
  const taskElement = document.querySelector(`[data-task-id="${id}"]`);
  if (taskElement) taskElement.classList.add('removing-item');
  try {
    await apiDeleteTask(id);
    tasks = tasks.filter(t=>String(t.id)!==String(id));
    renderAll();
  } catch(error) {
    showNotification('خطا', 'حذف تسک انجام نشد.');
    console.error(error);
  }
}


function closeModal(modalId){
  const modal = document.getElementById(modalId);
  if(!modal) return;
  modal.style.display = 'none';
  modal.classList.remove('open');
  document.body.style.overflow = '';
  if(modalId === 'taskModal') editingTaskId = null;
  if(modalId === 'listModal') editingListId = null;
}

function openTaskModal(taskId=null){
  editingTaskId = taskId;
  populateCategorySelect();
  
  if(taskId){
    const t = tasks.find(x=>x.id===taskId); 
    if(!t) return;
    
    document.getElementById('taskModalTitle').textContent = 'ویرایش تسک';
    document.getElementById('taskTitleInput').value = t.title;
    document.getElementById('taskDescriptionInput').value = t.description || '';
    document.getElementById('taskDueDateInput').value = t.dueDate || '';
    document.getElementById('taskStartTimeInput').value = t.startTime || '';
    document.getElementById('taskReminderInput').value = t.reminder || 'none';
    
    // مدیریت زمان - اگر زمان بر اساس دقیقه ذخیره شده
    if (t.studyTime && t.studyTime < 1) {
      // اگر کمتر از 1 ساعت است، به دقیقه تبدیل کن
      document.getElementById('taskStudyTimeInput').value = Math.round(t.studyTime * 60);
      document.getElementById('taskTimeUnitInput').value = 'minutes';
    } else {
      document.getElementById('taskStudyTimeInput').value = t.studyTime || 1;
      document.getElementById('taskTimeUnitInput').value = 'hours';
    }
    
    document.getElementById('taskCategoryInput').value = t.category || '';
  } else {
    document.getElementById('taskModalTitle').textContent = 'ایجاد تسک جدید';
    document.getElementById('taskTitleInput').value = '';
    document.getElementById('taskDescriptionInput').value = '';
    // تنظیم تاریخ پیش‌فرض به امروز
    document.getElementById('taskDueDateInput').value = todayDate;
    document.getElementById('taskStartTimeInput').value = '';
    document.getElementById('taskReminderInput').value = 'none';
    document.getElementById('taskStudyTimeInput').value = 1;
    document.getElementById('taskTimeUnitInput').value = 'hours';
    document.getElementById('taskCategoryInput').value = '';
  }
  document.getElementById('taskModal').style.display = 'flex';
}
async function saveTaskFromModal(){
  const title = document.getElementById('taskTitleInput').value.trim();
  if(!title){ alert('عنوان را وارد کنید'); return; }
  const desc = document.getElementById('taskDescriptionInput').value.trim();
  const dueDate = document.getElementById('taskDueDateInput').value || todayDate;
  const startTime = document.getElementById('taskStartTimeInput').value || null;
  const endTime = EndTime || null;
  const reminder = document.getElementById('taskReminderInput').value || 'none';
  const timeCategory = TimeCategory || '';
  const timeValue = parseFloat(document.getElementById('taskStudyTimeInput').value) || 0;
  const timeUnit = document.getElementById('taskTimeUnitInput').value;
  const studyTime = timeUnit === 'minutes' ? timeValue / 60 : timeValue;
  const category = document.getElementById('taskCategoryInput').value || '';
  const payload = { title, description:desc, completed:false, important:false, category, dueDate, startTime, endTime, reminder, timeCategory, studyTime };
  try {
    if(editingTaskId){
      const index = tasks.findIndex(x=>String(x.id)===String(editingTaskId));
      if(index < 0) return;
      payload.completed = tasks[index].completed;
      payload.important = tasks[index].important;
      const updated = normalizeTask(await apiUpdateTask(editingTaskId, toApiTask(payload)));
      tasks[index] = updated;
      editingTaskId = null;
    } else {
      const created = normalizeTask(await apiCreateTask(toApiTask(payload)));
      tasks.unshift(created);
    }
    closeModal('taskModal');
    renderAll();
  } catch(error) {
    showNotification('خطا', 'ذخیره تسک انجام نشد.');
    console.error(error);
  }
}

/* ---------------------------
   List actions (create & edit via modal)
   --------------------------- */
function openListModal(listId = null){
  editingListId = listId;
  document.getElementById('listModalTitle').textContent = listId ? 'ویرایش لیست' : 'ایجاد لیست جدید';
  if(listId){
    const l = lists.find(x=>x.id===listId);
    if(!l) return;
    document.getElementById('listNameInput').value = l.name;
    document.getElementById('listColorInput').value = l.color || '#8b5cf6';
    if (document.getElementById('listTypeInput')) document.getElementById('listTypeInput').value = isPersonalList(l) ? 'personal' : 'study';
  } else {
    document.getElementById('listNameInput').value = '';
    document.getElementById('listColorInput').value = '#8b5cf6';
    if (document.getElementById('listTypeInput')) document.getElementById('listTypeInput').value = 'study';
  }
  document.getElementById('listModal').style.display = 'flex';
}

function updateCurrentListTitle() {
  const titleEl = document.getElementById('current-list-title');
  if (currentView === 'category' && currentCategory) {
    const list = lists.find(l => l.id === currentCategory);
    titleEl.textContent = list ? list.name : 'دسته‌بندی';
  } else if (currentView === 'league') {
    titleEl.textContent = 'لیگ مطالعاتی';
  } else {
    const viewTitles = {
      'inbox': 'صندوق ورودی',
      'today': 'امروز', 
      'week': 'هفته جاری',
      'important': 'مهم'
    };
    titleEl.textContent = viewTitles[currentView] || 'صندوق ورودی';
  }
}
async function saveListFromModal(){
  const name = document.getElementById('listNameInput').value.trim();
  const color = document.getElementById('listColorInput').value || '#8b5cf6';
  const type = document.getElementById('listTypeInput')?.value || 'study';
  if(!name){ alert('نام لیست را وارد کنید'); return; }

  try {
    let savedList;

    if(editingListId){
      savedList = normalizeList(await apiUpdateList(editingListId, { name, color }));
      if (!savedList) throw new Error('پاسخ نامعتبر از سرور هنگام ویرایش لیست');

      if(type === 'personal') personalListIds.add(String(savedList.id));
      else personalListIds.delete(String(savedList.id));
    } else {
      savedList = normalizeList(await apiCreateList({ name, color }));
      if (!savedList) throw new Error('پاسخ نامعتبر از سرور هنگام ایجاد لیست');

      if(type === 'personal') personalListIds.add(String(savedList.id));
      else personalListIds.delete(String(savedList.id));
    }

    localStorage.setItem('plannerPersonalListIds', JSON.stringify([...personalListIds]));
    await refreshListsFromBackend();

    editingListId = null;
    closeModal('listModal');
    renderAll();
  } catch(error) {
    showNotification('خطا', 'ذخیره لیست انجام نشد.');
    console.error(error);
  }
}

/* ---------------------------
   UI helpers & wiring
   --------------------------- */
function populateCategorySelect(){
  const sel = document.getElementById('taskCategoryInput');
  if (!sel) return;

  sel.innerHTML = '';

  const emptyOption = document.createElement('option');
  emptyOption.value = '';
  emptyOption.textContent = 'بدون لیست';
  sel.appendChild(emptyOption);

  if (lists.length === 0) return;

  const studyLists = lists.filter(l => !isPersonalList(l));
  const personalLists = lists.filter(l => isPersonalList(l));

  if (studyLists.length > 0) {
    const optgroupStudy = document.createElement('optgroup');
    optgroupStudy.label = '📚 لیست‌های درسی';

    studyLists.forEach(l => {
      const option = document.createElement('option');
      option.value = l.id;
      option.textContent = `📁 ${l.name}`;
      option.style.color = l.color;
      optgroupStudy.appendChild(option);
    });

    sel.appendChild(optgroupStudy);
  }

  if (personalLists.length > 0) {
    const optgroupPersonal = document.createElement('optgroup');
    optgroupPersonal.label = '🏠 لیست‌های شخصی';

    personalLists.forEach(l => {
      const option = document.createElement('option');
      option.value = l.id;
      option.textContent = `📁 ${l.name}`;
      option.style.color = l.color;
      optgroupPersonal.appendChild(option);
    });

    sel.appendChild(optgroupPersonal);
  }
}

function setActiveView(view, category=''){
  currentView = view;
  if(view === 'category'){
    currentView = 'category';
    currentCategory = category;
  } else { 
    currentCategory = ''; 
  }
  
  // update active classes
  document.querySelectorAll('.list-item').forEach(x => x.classList.remove('active'));
  
  // mark sidebar view items
  if(view && view !== 'category'){
    const el = document.querySelector(`.list-item[data-view="${view}"]`);
    if(el) el.classList.add('active');
  } else if(view === 'category' && category){
    const el = document.querySelector(`.list-item[data-category="${category}"]`);
    if(el) el.classList.add('active');
  }
  
  // نمایش یا پنهان کردن بخش‌های مختلف
  if (view === 'league') {
    document.getElementById('tasks-view').style.display = 'none';
    document.getElementById('league-view').style.display = 'block';
    renderLeagueView();
  } else {
    document.getElementById('tasks-view').style.display = 'block';
    document.getElementById('league-view').style.display = 'none';
    renderTasks();
  }
  
  // به‌روزرسانی عنوان
  updateCurrentListTitle();
}

function renderAll() {
  renderSidebarLists();
  renderTasks();
  renderWeeklyPlanner();
  renderCharts();
  updateStats();
  updateSidebarCounts();
  setupReminders(); // تنظیم یادآوری‌ها
}

/* ---------------------------
   گزارش هفتگی
   --------------------------- */
function generateWeeklyReport() {
  const weekDates = getCurrentWeekDates(currentWeek);
  const completedTasks = tasks.filter(t => t.completed && t.dueDate && weekDates.includes(t.dueDate));
  
  // مرتب کردن تسک‌ها بر اساس تاریخ (از قدیمی به جدید)
  completedTasks.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
  
  // به‌روزرسانی اطلاعات هفته
  const start = startOfWeek(new Date(), currentWeek);
  const end = new Date(start);
  end.setDate(start.getDate() + 6);
  
  document.getElementById('report-week-range').textContent = 
    `هفته: ${formatShort(start.toISOString().split('T')[0])} تا ${formatShort(end.toISOString().split('T')[0])}`;
  
  const now = new Date();
  document.getElementById('report-generation-date').textContent = 
    `تاریخ تولید: ${now.toLocaleDateString('fa-IR')} - ${now.toLocaleTimeString('fa-IR')}`;
  
  document.getElementById('report-footer-date').textContent = now.toLocaleDateString('fa-IR');

  // محاسبه آمار
  const totalTasks = completedTasks.length;
  const totalTime = completedTasks.reduce((sum, task) => sum + (task.studyTime || 0), 0);
  const avgTime = totalTasks > 0 ? (totalTime / 7).toFixed(1) : 0;

  document.getElementById('report-total-tasks').textContent = totalTasks;
  document.getElementById('report-total-time').textContent = totalTime.toFixed(1) + ' ساعت';
  document.getElementById('report-avg-time').textContent = avgTime + ' ساعت';

  // پر کردن جدول تسک‌ها
  const tasksTable = document.getElementById('report-tasks-table');
  tasksTable.innerHTML = '';
  
  if (completedTasks.length === 0) {
    tasksTable.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 30px; color: #666;">
          <i class="fas fa-inbox" style="font-size: 24px; margin-bottom: 10px; display: block;"></i>
          هیچ تسک تکمیل‌شده‌ای در این هفته وجود ندارد
        </td>
      </tr>
    `;
  } else {
    // گروه‌بندی تسک‌ها بر اساس تاریخ
    const tasksByDate = {};
    completedTasks.forEach(task => {
      if (!tasksByDate[task.dueDate]) {
        tasksByDate[task.dueDate] = [];
      }
      tasksByDate[task.dueDate].push(task);
    });

    // مرتب کردن تاریخ‌ها
    const sortedDates = Object.keys(tasksByDate).sort((a, b) => new Date(a) - new Date(b));
    
    let rowIndex = 1;
    
    sortedDates.forEach(date => {
      const dateTasks = tasksByDate[date];
      
      // اضافه کردن سطر تاریخ
      const dateRow = document.createElement('tr');
      dateRow.style.background = '#e8f4fd';
      dateRow.innerHTML = `
        <td colspan="7" style="font-weight: bold; padding: 15px 12px; color: #4f46e5; font-size: 16px;">
          📅 ${formatShort(date)} - ${dateTasks.length} تسک
        </td>
      `;
      tasksTable.appendChild(dateRow);
      
      // اضافه کردن تسک‌های این تاریخ
      dateTasks.forEach((task, taskIndex) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${rowIndex}</td>
          <td>${task.title}</td>
          <td>${getCategoryName(task.category)}</td>
          <td>${formatShort(task.dueDate)}</td>
          <td>${formatTimeForDisplay(task.studyTime || 0)}</td>
          <td>${task.important ? '⭐ مهم' : 'عادی'}</td>
          <td>${task.description || '-'}</td>
        `;
        tasksTable.appendChild(row);
        rowIndex++;
      });
    });
  }

  // توزیع زمانی روزهای هفته
  const timeDistribution = {};
  weekDates.forEach(date => {
    timeDistribution[date] = 0;
  });
  
  completedTasks.forEach(task => {
    timeDistribution[task.dueDate] += task.studyTime || 0;
  });

  const distributionContainer = document.querySelector('.print-summary:last-child div');
  if (distributionContainer) {
    distributionContainer.innerHTML = '';
    
    const days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه'];
    
    weekDates.forEach((date, index) => {
      const dayDiv = document.createElement('div');
      dayDiv.style.textAlign = 'center';
      dayDiv.style.padding = '12px';
      dayDiv.style.background = '#f8f9fa';
      dayDiv.style.borderRadius = '8px';
      dayDiv.style.border = '1px solid #e9ecef';
      
      dayDiv.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 6px; color: #4f46e5;">${days[index]}</div>
        <div style="color: #10b981; font-size: 14px; font-weight: bold;">${timeDistribution[date].toFixed(1)} ساعت</div>
      `;
      
      distributionContainer.appendChild(dayDiv);
    });
  }

  // نمایش گزارش و پرینت
  document.getElementById('printReport').style.display = 'block';
  setTimeout(() => {
    window.print();
    setTimeout(() => {
      document.getElementById('printReport').style.display = 'none';
    }, 100);
  }, 500);
}


async function loadFontAwesome() {
  if (document.querySelector('link[data-dopamine-fontawesome]')) return;
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.dataset.dopamineFontawesome = 'true';
  link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css';
  document.head.appendChild(link);
  await new Promise(resolve => { link.onload = resolve; link.onerror = resolve; });
}

async function loadChartJs() {
  if (window.Chart) { chartReady = true; return; }
  await new Promise((resolve, reject) => {
    const existing = document.getElementById('dopamine-chartjs');
    if (existing) { existing.addEventListener('load', () => { chartReady = true; resolve(); }); existing.addEventListener('error', reject); return; }
    const script = document.createElement('script');
    script.id = 'dopamine-chartjs';
    script.src = 'https://lib.arvancloud.ir/Chart.js/3.7.0/chart.js';
    script.onload = () => { chartReady = true; resolve(); };
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

async function loadPlanner() {
  try {
    loadPersonalListIds();
    const [rawTasks, rawLists] = await Promise.all([apiGetTasks(), apiGetLists()]);
    tasks = (Array.isArray(rawTasks) ? rawTasks : []).map(normalizeTask);
    lists = normalizeLists(rawLists);
    const validPredictionIds = lists.filter(l => !isPersonalList(l)).map(l => String(l.id));
    const currentPredictionIds = new Set(predictionSettings.enabledSubjects.map(String));
    const normalizedPredictionIds = validPredictionIds.filter(id => currentPredictionIds.has(id));
    predictionSettings.enabledSubjects = normalizedPredictionIds.length > 0
      ? normalizedPredictionIds
      : validPredictionIds;
    saveAll();
    renderAll();
  } catch(error) {
    console.error(error);
    showNotification('خطا در اتصال', 'داده‌های پلنر دریافت نشد. اتصال به سرور را بررسی کنید.');
  }
}
var EndTime = 0
var TimeCategory = ''
function bindPlannerEvents() {
  document.getElementById('predictionSettingsBtn')?.addEventListener('click', openPredictionSettingsModal);
  document.querySelectorAll('[data-close-modal]').forEach(btn => { btn.addEventListener('click', () => closeModal(btn.dataset.closeModal)); });
  document.getElementById('savePredictionSettingsBtn')?.addEventListener('click', savePredictionSettings);
  document.getElementById('cancelPredictionSettingsBtn')?.addEventListener('click', () => closeModal('predictionSettingsModal'));
  document.getElementById('predictionSettingsModal')?.addEventListener('click', e => { if(e.target.id === 'predictionSettingsModal') closeModal('predictionSettingsModal'); });
  document.getElementById('notification-close')?.addEventListener('click', hideNotification);
  document.getElementById('addListBtn')?.addEventListener('click', () => openListModal(null));
  document.getElementById('saveListBtn')?.addEventListener('click', saveListFromModal);
  document.getElementById('cancelListBtn')?.addEventListener('click', () => { editingListId=null; closeModal('listModal'); });
  document.getElementById('listModal')?.addEventListener('click', e => { if(e.target.id === 'listModal') closeModal('listModal'); });
  document.getElementById('openTaskModal')?.addEventListener('click', () => openTaskModal(null));
  document.getElementById('saveTaskBtn')?.addEventListener('click', saveTaskFromModal);
  document.getElementById('cancelTaskBtn')?.addEventListener('click', () => { editingTaskId=null; closeModal('taskModal'); });
  document.getElementById('taskModal')?.addEventListener('click', e => { if(e.target.id === 'taskModal'){ editingTaskId=null; closeModal('taskModal'); } });
  document.getElementById('searchInput')?.addEventListener('input', renderTasks);
  document.getElementById('view-inbox')?.addEventListener('click', () => setActiveView('inbox'));
  document.getElementById('view-today')?.addEventListener('click', () => setActiveView('today'));
  document.getElementById('view-week')?.addEventListener('click', () => setActiveView('week'));
  document.getElementById('view-important')?.addEventListener('click', () => setActiveView('important'));
  document.getElementById('view-league')?.addEventListener('click', () => setActiveView('league'));
  document.getElementById('prev-week')?.addEventListener('click', () => { currentWeek--; renderWeeklyPlanner(); renderCharts(); updateStats(); });
  document.getElementById('next-week')?.addEventListener('click', () => { currentWeek++; renderWeeklyPlanner(); renderCharts(); updateStats(); });
  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);
  document.getElementById('printReportBtn')?.addEventListener('click', generateWeeklyReport);

  document.getElementById('taskTimeUnitInput')?.addEventListener('change', function(){
    const input=document.getElementById('taskStudyTimeInput');
    if(this.value==='minutes'){ input.step='5'; input.placeholder='دقیقه'; } else { input.step='0.5'; input.placeholder='ساعت'; }
  });
  const recalc = () => {
    const start=document.getElementById('taskStartTimeInput')?.value;
    const value=parseFloat(document.getElementById('taskStudyTimeInput')?.value)||0;
    const unit=document.getElementById('taskTimeUnitInput')?.value;
    if(start && value>0){
      const hours=unit==='minutes'?value/60:value;
      EndTime = calculateEndTime(start,hours);
      TimeCategory = getTimeCategory(start);
    }
  };
  document.getElementById('taskStartTimeInput')?.addEventListener('change', recalc);
  document.getElementById('taskStudyTimeInput')?.addEventListener('change', recalc);
  document.getElementById('taskTitleInput')?.addEventListener('input', function(){
    const detected=detectCategoryFromTitle(this.value.trim());
    if(detected) document.getElementById('taskCategoryInput').value=detected;
  });

  const quickAdd=document.getElementById('new-task-input');
  quickAdd?.addEventListener('input', function(){
    const detected=detectCategoryFromTitle(this.value.trim());
    showCategoryDetection(detected);
  });
  quickAdd?.addEventListener('keyup', async function(e){
    if(e.key!=='Enter' || !this.value.trim()) return;
    const title=this.value.trim();
    const detected=detectCategoryFromTitle(title) || '';
    try {
      const created=normalizeTask(await apiCreateTask(toApiTask({title,description:'',completed:false,important:false,category:detected,dueDate:todayDate,startTime:null,endTime:null,reminder:'none',timeCategory:'',studyTime:1})));
      tasks.unshift(created);
      this.value='';
      document.getElementById('auto-category-detection').style.display='none';
      renderAll();
    } catch(error) { showNotification('خطا','افزودن سریع تسک انجام نشد.'); console.error(error); }
  });
}

onMounted(async () => {
  initTheme();
  themeObserver = watchExternalThemeChanges();
  bindPlannerEvents();
  try { await loadFontAwesome(); } catch(e) { console.warn('Font Awesome unavailable', e); }
  try { await loadChartJs(); } catch(e) { console.warn('Chart.js unavailable', e); }
  if ('Notification' in window && Notification.permission === 'default') {
    try { await Notification.requestPermission(); } catch(e) {}
  }
  await loadPlanner();
});

onBeforeUnmount(() => {
  themeObserver?.disconnect();
  themeObserver = null;
  reminderTimeouts.forEach(t => clearTimeout(t));
  if (studyChart) studyChart.destroy();
  if (progressChart) progressChart.destroy();
});


</script>

<style src="../assets/planner.css"></style>