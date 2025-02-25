import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import StudyActivities from '../components/StudyActivities.vue';

const routes = [
  { path: '/dashboard', component: Dashboard },
  { path: '/study-activities', component: StudyActivities },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
