<template>
  <div class="study-progress">
    <h2>Study Progress</h2>
    <p>Total Words Studied: {{ localData.totalWordsStudied }} / {{ localData.totalWords }}</p>
    <p>Mastery Progress: {{ localData.masteryProgress }}%</p>
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
  data() {
    return {
      localData: { ...this.data }, // Create a local copy of the data prop
    };
  },
  mounted() {
    console.log('Fetching study progress data...');
    axios.get('/dashboard/study_progress')
      .then(response => {
        console.log('Study progress data fetched successfully.');
        this.localData = response.data;
      })
      .catch(error => {
        console.error('Error fetching study progress data:', error);
      });
  },
};
</script>

<style scoped>
.study-progress {
  margin-bottom: 20px;
}
</style>
