import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import StudyActivities from '../components/StudyActivities.vue';
import Home from '../components/Home.vue';
import MalayChatbox from '../components/MalayChatbox.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/dashboard', component: Dashboard },
  { path: '/study-activities', component: StudyActivities },
  { path: '/malay-chatbox', component: MalayChatbox },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
