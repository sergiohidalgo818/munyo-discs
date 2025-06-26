<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-zinc-900 text-white rounded-xl p-6 shadow-lg w-64 text-center">
      <div class="flex justify-center mb-4">
        <div class="flex space-x-2">
          <span class="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:-0.3s]"></span>
          <span class="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:-0.15s]"></span>
          <span class="w-2 h-2 bg-white rounded-full animate-bounce"></span>
        </div>
      </div>
      <p class="text-sm text-zinc-300">Checking your collection...</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  visible: Boolean,
})
</script>

<style scoped>
@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-8px);
  }
}

.animate-bounce {
  animation: bounce 0.6s infinite;
}
</style>
