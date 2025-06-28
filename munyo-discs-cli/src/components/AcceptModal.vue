<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-zinc-900 text-white p-6 rounded-xl shadow-2xl w-full max-w-sm space-y-4 border border-zinc-700">
      <h2 class="text-lg font-semibold">{{ title }}</h2>
      <p class="text-sm text-zinc-400">{{ message }}</p>

      <div class="flex justify-center pt-4">
        <button @click="$emit('accept')"
          class="bg-green-600 hover:bg-green-500 text-white px-6 py-2 rounded-lg transition">
          Ok
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  message: String,
})
defineEmits(['accept'])
</script>
