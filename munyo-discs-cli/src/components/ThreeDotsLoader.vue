<template>
  <div class="flex space-x-2">
    <span class="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:-0.3s]"></span>
    <span class="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:-0.15s]"></span>
    <span class="w-2 h-2 bg-white rounded-full animate-bounce"></span>
  </div>
</template>

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
