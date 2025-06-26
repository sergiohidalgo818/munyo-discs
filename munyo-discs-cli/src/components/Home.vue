<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import SpotifyActions from '../components/MainActions.vue'

const shouldShowButton = ref(false)

onMounted(async () => {
  try {
    const response = await fetch('/api/hasConnectedApps')
    const result = await response.json()
    shouldShowButton.value = result === false
  } catch (error) {
    console.error('Failed to check connected apps:', error)
    shouldShowButton.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-zinc-900 text-white flex items-center justify-center flex-col p-6">
    <div class="bg-zinc-800 p-8 rounded-xl shadow-lg text-center max-w-md w-full mb-6">
      <h1 class="text-3xl font-bold mb-4">Welcome to Munyo Discs</h1>
      <p class="text-zinc-400 mb-6">
        Connect your favorite apps and manage your integrations in one place.
      </p>

      <RouterLink v-if="shouldShowButton" to="/connect">
        <button class="bg-green-500 hover:bg-green-400 text-white font-semibold py-2 px-4 rounded-lg transition">
          Connect Apps
        </button>
      </RouterLink>
    </div>

    <SpotifyActions v-if="!shouldShowButton" />
  </div>
</template>
