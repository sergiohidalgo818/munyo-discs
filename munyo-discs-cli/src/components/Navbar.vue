<template>
  <nav class="bg-zinc-800 text-white px-6 py-4 flex justify-between items-center shadow-md">
    <h1 class="text-xl font-bold tracking-wide">Munyo Discs</h1>
    <div class="space-x-4 text-sm font-medium">
      <RouterLink to="/" class="hover:underline hover:text-green-400 transition" active-class="text-green-400"
        exact-active-class="text-green-400">
        Home
      </RouterLink>
      <RouterLink to="/connect" class="hover:underline hover:text-green-400 transition" active-class="text-green-400">
        Connect
      </RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
