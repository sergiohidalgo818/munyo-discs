import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ConnectView from "../views/ConnectView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/connect", component: ConnectView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
