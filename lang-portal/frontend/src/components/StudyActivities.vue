<template>
  <div class="study-activities">
    <h1>Study Activities</h1>
    <div v-for="activity in activities" :key="activity.id" class="activity-card">
      <img :src="activity.thumbnail" alt="Activity Thumbnail" />
      <h2>{{ activity.name }}</h2>
      <button @click="launchActivity(activity.id)">Launch</button>
      <button @click="viewActivity(activity.id)">View</button>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      activities: [],
    };
  },
  methods: {
    async fetchActivities() {
      try {
        const response = await axios.get('/study_activities');
        this.activities = response.data;
      } catch (error) {
        console.error('Error fetching study activities:', error);
      }
    },
    launchActivity(id) {
      this.$router.push(`/study_activities/${id}`);
    },
    viewActivity(id) {
      this.$router.push(`/study_activities/${id}`);
    },
  },
  mounted() {
    this.fetchActivities();
  },
};
</script>

<style scoped>
.study-activities {
  display: flex;
  flex-direction: column;
}
.activity-card {
  margin: 10px;
  border: 1px solid #ccc;
  padding: 10px;
}
</style>
