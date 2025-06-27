import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ConnectView from "../views/ConnectView.vue";
import DiscsView from "../views/DiscsView.vue";
import SpotifyView from "../views/SpotifyView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/connect", component: ConnectView },
  { path: "/discs", component: DiscsView },
  { path: "/spotify", component: SpotifyView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
