import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import StudyActivities from '../components/StudyActivities.vue';
import HomeView from '../components/Home.vue';
import MalayChatbox from '../components/MalayChatbox.vue';
import PracticeJawi from '../components/PracticeJawi.vue';
import ListeningSpeaking from '../components/ListeningSpeaking.vue';
import PictureGame from '../components/PictureGame.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/dashboard', component: Dashboard },
  { path: '/study-activities', component: StudyActivities },
  { path: '/malay-chatbox', component: MalayChatbox },
  { path: '/practice-jawi', component: PracticeJawi },
  { path: '/listening-speaking', component: ListeningSpeaking },
  { path: '/picture-game', component: PictureGame },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
