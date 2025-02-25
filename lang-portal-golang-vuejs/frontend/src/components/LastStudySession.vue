<template>
  <div class="last-study-session">
    <h2>Last Study Session</h2>
    <p v-if="data.activityName">Activity: {{ data.activityName }}</p>
    <p v-if="data.groupName">Group: {{ data.groupName }}</p>
    <p v-if="data.startTime">Start Time: {{ data.startTime }}</p>
    <p v-if="data.endTime">End Time: {{ data.endTime }}</p>
    <p v-if="data.correctCount !== undefined && data.wrongCount !== undefined">
      Correct: {{ data.correctCount }}, Wrong: {{ data.wrongCount }}
    </p>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    console.log('Fetching last study session data...');
    axios.get('https://new-base-url.com/dashboard/last_study_session')
      .then(response => {
        console.log('Last study session data fetched successfully.');
        console.log(response.data);
      })
      .catch(error => {
        console.error('Failed to fetch last study session data:', error);
      });
  },
};
</script>

<style scoped>
.last-study-session {
  margin-bottom: 20px;
}
</style>
