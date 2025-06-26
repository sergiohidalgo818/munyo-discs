import { computed, ref } from "vue";
import { defineStore } from "pinia";

export const useSpotifyStore = defineStore("spotify", () => {
  const token = ref(null);

  // Optional: get whether token is valid
  const isAuthenticated = computed(() => !!token.value);

  function setToken(newToken) {
    token.value = newToken;
  }

  function clearToken() {
    token.value = null;
  }

  return {
    token,
    isAuthenticated,
    setToken,
    clearToken,
  };
});
