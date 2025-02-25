<template>
  <div class="study-activities">
    <h1>Study Activities</h1>
    <div class="activities-grid">
      <div v-for="activity in activities" :key="activity.id" class="activity-card">
        <div class="activity-content">
          <h2>{{ activity.name }}</h2>
          <p class="activity-date">Created: {{ new Date(activity.created_at).toLocaleDateString() }}</p>
          <div class="activity-actions">
            <a :href="activity.url" target="_blank" class="btn btn-primary">Launch</a>
            <button @click="viewActivity(activity.id)" class="btn btn-secondary">View</button>
          </div>
        </div>
      </div>
    </div>
    <div class="pagination">
      <button :disabled="offset === 0" @click="previousPage" class="btn">Previous</button>
      <span>Page {{ currentPage }}</span>
      <button :disabled="activities.length < limit" @click="nextPage" class="btn">Next</button>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      activities: [],
      offset: 0,
      limit: 10,
    };
  },
  computed: {
    currentPage() {
      return Math.floor(this.offset / this.limit) + 1;
    },
  },
  methods: {
    async fetchActivities() {
      try {
        const response = await axios.get(`/study-activities?limit=${this.limit}&offset=${this.offset}`);
        this.activities = response.data;
      } catch (error) {
        console.error('Error fetching study activities:', error);
      }
    },
    viewActivity(id) {
      //TODO
      this.$router.push(`/study-activities/${id}`);
    },
    nextPage() {
      this.offset += this.limit;
      this.fetchActivities();
    },
    previousPage() {
      this.offset = Math.max(0, this.offset - this.limit);
      this.fetchActivities();
    },
  },
  mounted() {
    this.fetchActivities();
  },
};
</script>

<style scoped>
.study-activities {
  padding: 20px;
}

.activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.activity-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.activity-content {
  padding: 16px;
}

.activity-date {
  color: #666;
  font-size: 0.9em;
  margin: 8px 0;
}

.activity-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
}

.btn:hover {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}
</style>
