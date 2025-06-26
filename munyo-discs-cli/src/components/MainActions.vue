<template>
  <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 w-full max-w-4xl mx-auto p-6">
    <button v-for="action in actions" :key="action.label" @click="action.handler"
      class="bg-zinc-800 hover:bg-zinc-700 text-white font-medium py-3 px-4 rounded-lg shadow text-center transition">
      {{ action.label }}
    </button>
  </div>
</template>



<script setup>
import { ref } from 'vue'
import FileUploadModal from './FileUploadModal.vue'
import LoadingModal from './LoadingModal.vue'

const showUploadModal = ref(false)
const showLoadingModal = ref(false)

const actions = [
  {
    label: 'Download Spotify Likes',
    handler: () => console.log('Downloading Spotify Likes...'),
  },
  {
    label: 'Download Spotify Playlists',
    handler: () => console.log('Downloading Spotify Playlists...'),
  },
  {
    label: 'Download Spotify Artists',
    handler: () => console.log('Downloading Spotify Artists...'),
  },
  {
    label: 'Owned CDs',
    handler: async () => {
      await handleProtectedCheck('/api/owned-cds')
    },
  },
  {
    label: 'Wished CDs',
    handler: async () => {
      await handleProtectedCheck('/api/wished-cds')
    },
  },
  {
    label: 'Disclogs CDs',
    handler: async () => {
      await handleProtectedCheck('/api/discogs-cds')
    },
  },
  {
    label: 'Show Downloaded Spotify Likes',
    handler: () => console.log('Downloaded Likes'),
  },
  {
    label: 'Show Downloaded Spotify Playlists',
    handler: () => console.log('Downloaded Playlists'),
  },
  {
    label: 'Show Downloaded Spotify Artists',
    handler: () => console.log('Downloaded Artists'),
  },
]

async function handleProtectedCheck(endpoint) {
  try {
    showLoadingModal.value = true
    const res = await fetch(endpoint)
    const result = await res.json()
    if (result === false) {
      showUploadModal.value = true
    }
  } catch (e) {
    console.error('Request failed:', e)
    showUploadModal.value = true
  } finally {
    showLoadingModal.value = false
  }
}

function handleFileUpload(file) {
  console.log('Uploaded file:', file)
  showUploadModal.value = false
}
</script>
