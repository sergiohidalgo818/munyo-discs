import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Adjust as needed
});

export default api;
