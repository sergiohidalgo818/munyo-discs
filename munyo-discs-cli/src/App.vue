<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen bg-zinc-900 text-white">
    <Navbar />
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>
