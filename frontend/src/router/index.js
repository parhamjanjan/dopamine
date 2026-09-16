import { createRouter, createWebHistory } from 'vue-router'

import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'

import MainLayout from '../layouts/MainLayout.vue'

import HomeView from '../views/HomeView.vue'
import PlannerView from '../views/PlannerView.vue'
import ProfileView from '../views/ProfileView.vue'
import RoomsView from '../views/RoomsView.vue'

import StudyRoomView from '../views/StudyRoomView.vue'
import ExamsView from '../views/ExamsView.vue'

import ExamTakingView from '../views/ExamTakingView.vue'
import ExamResultView from '../views/ExamResultView.vue'


/* =========================================================
   PLACEHOLDER
========================================================= */

const PlaceholderView = {
  template: `
    <div
      style="
        min-height:100vh;
        display:flex;
        align-items:center;
        justify-content:center;
        padding:24px;
        font-family:Vazirmatn,sans-serif;
      "
    >
      <div style="text-align:center">
        <h1
          style="
            margin:0 0 8px;
            font-size:24px;
            font-weight:700;
          "
        >
          این صفحه به‌زودی ساخته می‌شود
        </h1>

        <p
          style="
            margin:0;
            color:#64748b;
          "
        >
          فعلاً ساختار ناوبری آماده است.
        </p>
      </div>
    </div>
  `
}


/* =========================================================
   ROUTER
========================================================= */

const router = createRouter({
  history: createWebHistory(),

  routes: [

    /*
    |--------------------------------------------------------------------------
    | Authentication
    |--------------------------------------------------------------------------
    */

    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView
    },


    /*
    |--------------------------------------------------------------------------
    | Main Application
    |
    | تمام صفحات داخل MainLayout دارای Taskbar هستند.
    |--------------------------------------------------------------------------
    */

    {
      path: '/',
      component: MainLayout,

      children: [

        {
          path: '',
          redirect: '/home'
        },

        {
          path: 'home',
          name: 'home',
          component: HomeView
        },

        {
          path: 'planner',
          name: 'planner',
          component: PlannerView
        },

        {
          path: 'rooms',
          name: 'rooms',
          component: RoomsView
        },

        {
          path: 'rooms/:roomId',
          name: 'study-room',
          component: StudyRoomView
        },

        {
          path: 'exams',
          name: 'exams',
          component: ExamsView
        },

        {
          path: 'messages',
          name: 'messages',
          component: PlaceholderView
        },

        {
          path: 'profile',
          name: 'profile',
          component: ProfileView
        }
      ]
    },


    /*
    |--------------------------------------------------------------------------
    | EXAM TAKING
    |
    | خارج از MainLayout
    |
    | بنابراین Taskbar نمایش داده نمی‌شود.
    |--------------------------------------------------------------------------
    */

    {
      path: '/exams/:id/taking',
      name: 'ExamTaking',
      component: ExamTakingView
    },


    /*
    |--------------------------------------------------------------------------
    | EXAM RESULT
    |
    | خارج از MainLayout
    |
    | بنابراین Taskbar نمایش داده نمی‌شود.
    |--------------------------------------------------------------------------
    */

    {
      path: '/exams/result/:id',
      name: 'ExamResult',
      component: ExamResultView
    }
  ]
})


/* =========================================================
   EXPORT
========================================================= */

export default router