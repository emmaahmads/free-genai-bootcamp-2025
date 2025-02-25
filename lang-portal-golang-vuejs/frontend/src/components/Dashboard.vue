<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="dashboard-grid">
      <div class="stats-card">
        <h3>Study Streak</h3>
        <div class="stat-value">{{ dashboardStats.study_streak_days }} days</div>
      </div>
      <div class="stats-card">
        <h3>Success Rate</h3>
        <div class="stat-value">{{ dashboardStats.success_rate }}%</div>
      </div>
      <div class="stats-card">
        <h3>Active Groups</h3>
        <div class="stat-value">{{ dashboardStats.total_active_groups }}</div>
      </div>
      <div class="stats-card">
        <h3>Total Sessions</h3>
        <div class="stat-value">{{ dashboardStats.total_study_sessions }}</div>
      </div>
    </div>
    <div class="actions">
      <button @click="startStudying" class="btn btn-primary">Start Studying</button>
      <router-link to="/study-activities" class="btn btn-secondary">View Activities</router-link>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'DashboardComponent',
  data() {
    return {
      dashboardStats: {
        study_streak_days: 0,
        success_rate: 0,
        total_active_groups: 0,
        total_study_sessions: 0,
      },
    };
  },
  mounted() {
    this.fetchDashboardStats();
  },
  methods: {
    async fetchDashboardStats() {
      try {
        const response = await axios.get('/dashboard/stats');
        this.dashboardStats = response.data;
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      }
    },
    startStudying() {
      this.$router.push('/study-activities');
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.stats-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.stats-card h3 {
  color: #666;
  margin: 0 0 10px 0;
  font-size: 1.1em;
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  color: #4CAF50;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.btn {
  padding: 12px 24px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
}

.btn:hover {
  opacity: 0.9;
}
</style>
