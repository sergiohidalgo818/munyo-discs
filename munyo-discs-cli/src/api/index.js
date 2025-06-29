import axios from "axios";

const api = axios.create({
  // baseURL: `${window.location.origin}/api`, // Adjust as needed
  baseURL: `http://127.0.0.1:8218/api`, // Adjust as needed
});

export default api;
