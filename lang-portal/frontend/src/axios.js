import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8080/api', // Adjusted base URL
  timeout: 10000,
});

// Add any interceptors or configurations here

export default instance;
