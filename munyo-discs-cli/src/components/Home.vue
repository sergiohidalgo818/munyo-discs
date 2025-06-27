
<template>
  <div class="min-h-screen bg-zinc-900 text-white flex items-center justify-center flex-col p-6">
    <div class="bg-zinc-800 p-8 rounded-xl shadow-lg text-center max-w-md w-full mb-6">
      <h1 class="text-3xl font-bold mb-4">Welcome to Munyo Discs</h1>
      <p class="text-zinc-400 mb-6">
        Connect your favorite apps and manage your integrations in one place.
      </p>
    </div>

    <MainActions />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import MainActions from '../components/MainActions.vue'
</script>

