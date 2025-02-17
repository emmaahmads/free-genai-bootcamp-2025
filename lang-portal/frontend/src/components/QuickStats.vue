<template>
  <div class="quick-stats">
    <h2>Quick Stats</h2>
    <p>Success Rate: {{ data.successRate }}%</p>
    <p>Total Study Sessions: {{ data.totalSessions }}</p>
    <p>Total Active Groups: {{ data.totalGroups }}</p>
    <p>Study Streak: {{ data.studyStreak }} days</p>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.quick-stats {
  margin-bottom: 20px;
}
</style>
