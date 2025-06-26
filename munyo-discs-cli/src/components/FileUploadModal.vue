<template>
  <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 w-full max-w-4xl mx-auto p-6">
    <button v-for="action in actions" :key="action.label" @click="action.handler"
      class="bg-zinc-800 hover:bg-zinc-700 text-white font-medium py-3 px-4 rounded-lg shadow text-center transition">
      {{ action.label }}
    </button>
  </div>

  <!-- 📂 Modal triggered if response is false -->
  <FileUploadModal :visible="showModal" @close="showModal = false" @file-selected="handleFileUpload" />
</template>
