<template>
  <div class="p-6 max-w-4xl mx-auto bg-zinc-900 rounded-xl shadow-lg text-white">
    <h2 class="text-2xl font-semibold mb-4">Connect Your Apps</h2>

    <!-- Loading state -->
    <div v-if="loading" class="flex items-center justify-center h-32">
      <ThreeDotsLoader />
    </div>

    <!-- No apps available -->
    <div v-else-if="apps.length === 0" class="text-zinc-400 text-center">
      No apps available.
    </div>

    <!-- Apps grid -->
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
      <div v-for="app in apps" :key="app.id"
        class="bg-zinc-800 hover:bg-zinc-700 transition rounded-xl p-4 flex flex-col items-center text-center cursor-pointer">
        <img :src="app.icon" :alt="app.name" class="w-12 h-12 mb-2 object-contain" />
        <span class="text-sm font-medium">{{ app.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ThreeDotsLoader from './ThreeDotsLoader.vue' // loader component

const apps = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/api/apps') // Replace with real endpoint
    const data = await response.json()
    apps.value = data
  } catch (e) {
    console.error('Failed to fetch apps:', e)
  } finally {
    loading.value = false
  }
})
</script>
