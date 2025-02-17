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
    axios.get('https://new-base-url.com/dashboard/study_progress')
      .then(response => {
        this.localData = response.data;
      })
      .catch(error => {
        console.error(error);
      });
  },
};
</script>

<style scoped>
.study-progress {
  margin-bottom: 20px;
}
</style>
