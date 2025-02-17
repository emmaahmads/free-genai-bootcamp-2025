<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <LastStudySession :data="lastStudySession" />
    <StudyProgress :data="studyProgress" />
    <QuickStats :data="quickStats" />
    <button @click="startStudying">
      Start Studying
    </button>
  </div>
</template>

<script>
import LastStudySession from './LastStudySession.vue';
import StudyProgress from './StudyProgress.vue';
import QuickStats from './QuickStats.vue';
import axios from '../axios';

export default {
  name: 'DashboardComponent',
  components: {
    LastStudySession,
    StudyProgress,
    QuickStats,
  },
  data() {
    return {
      lastStudySession: {},
      studyProgress: {},
      quickStats: {},
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      console.log('Fetching dashboard data...');
      try {
        const [lastSession, progress, stats] = await Promise.all([
          axios.get('/dashboard/last_study_session'),
          axios.get('/dashboard/study_progress'),
          axios.get('/dashboard/quick_stats'),
        ]);
        console.log('Last study session data fetched.');
        console.log('Study progress data fetched.');
        console.log('Quick stats data fetched.');
        this.lastStudySession = lastSession.data;
        this.studyProgress = progress.data;
        this.quickStats = stats.data;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    },
    startStudying() {
      this.$router.push('/study_activities');
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
</style>
