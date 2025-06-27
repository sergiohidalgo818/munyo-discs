
<template>
  <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 w-full max-w-4xl mx-auto p-6">
    <button
      v-for="action in actions"
      :key="action.label"
      @click="action.handler"
      class="bg-zinc-800 hover:bg-zinc-700 text-white font-medium py-3 px-4 rounded-lg shadow text-center transition"
    >
      {{ action.label }}
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const actions = [
  {
    label: 'Spotify',
    handler: () => router.push('/spotify'),
  },
  {
    label: 'CDs',
    handler: () => router.push('/discs'),
  },
]
</script>

