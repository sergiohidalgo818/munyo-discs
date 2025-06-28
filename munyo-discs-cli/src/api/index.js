import axios from "axios";

const api = axios.create({
  baseURL: `${window.location.origin}/api`, // Adjust as needed
});

export default api;
