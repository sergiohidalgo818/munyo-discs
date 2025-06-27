
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-zinc-900 text-white p-6 rounded-2xl shadow-2xl w-full max-w-md space-y-4 border border-zinc-700">
      <h2 class="text-xl font-semibold text-white">Upload {{ type }} CDs</h2>


<!-- Custom styled file upload -->
<div>
  <span class="text-sm text-zinc-400">Select a .csv file</span>

  <label
    class="mt-2 block w-full px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-white text-sm rounded-lg border border-zinc-600 cursor-pointer transition text-center"
  >
    {{ selectedFile?.name || 'Choose File' }}
    <input
      type="file"
      accept=".csv"
      @change="onFileChange"
      class="hidden"
    />
  </label>
</div>


      <!-- Show selected file name -->
      <div v-if="selectedFile" class="text-sm text-zinc-300 italic truncate">
        Selected: {{ selectedFile.name }}
      </div>

      <div class="flex justify-end space-x-3 pt-4">
        <button
          @click="$emit('close')"
          class="bg-zinc-700 hover:bg-zinc-600 text-white px-4 py-2 rounded-lg transition"
        >
          Cancel
        </button>
        <button
          :disabled="!selectedFile || uploading"
          @click="uploadFile"
          class="bg-green-600 hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition"
        >
          {{ uploading ? 'Uploading...' : 'Upload' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadOwnedCds } from '@/api/ownedCds'
import { uploadWishedCds } from '@/api/wishedCds'

const { type } = defineProps({
  type: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['close', 'uploaded'])

const selectedFile = ref(null)
const uploading = ref(false)

function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function uploadFile() {
  if (!selectedFile.value) return

  try {
    uploading.value = true
    if (type === 'owned') {
      await uploadOwnedCds(selectedFile.value)
    } else if (type === 'wished') {
      await uploadWishedCds(selectedFile.value)
    } else {
      throw new Error('Invalid upload type')
    }

    emit('uploaded', selectedFile.value)
  } catch (error) {
    console.error('Upload failed:', error)
    alert('Upload failed: ' + error.message)
  } finally {
    uploading.value = false
  }
}
</script>

