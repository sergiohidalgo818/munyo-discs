<template>
  <div class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
    <div class="bg-zinc-900 rounded-lg shadow-lg p-6 w-full max-w-md border border-zinc-700">
      <h2 class="text-xl font-semibold mb-4 text-white">
        {{ isEdit ? 'Edit CD' : 'Add CD' }}
      </h2>

      <div class="space-y-4">
        <div>
          <label class="block text-sm text-white mb-1">Artist</label>
          <input v-model="localArtist" type="text"
            class="w-full px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600 focus:outline-none" />
        </div>

        <div>
          <label class="block text-sm text-white mb-1">Disc</label>
          <input v-model="localDisc" type="text"
            class="w-full px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600 focus:outline-none" />
        </div>

        <div v-if="showStars">
          <label class="block text-sm text-white mb-1">Stars</label>
          <div class="flex space-x-1">
            <span v-for="n in 5" :key="n" class="cursor-pointer text-2xl"
              :class="n <= localStars ? 'text-yellow-400' : 'text-zinc-500'" @click="localStars = n">
              ★
            </span>
          </div>
        </div>
      </div>

      <div class="flex justify-end mt-6 space-x-3">
        <button @click="$emit('cancel')" class="px-4 py-2 rounded bg-zinc-700 text-white hover:bg-zinc-600 text-sm">
          Cancel
        </button>
        <button @click="handleSave" class="px-4 py-2 rounded bg-green-500 text-white hover:bg-green-400 text-sm">
          {{ isEdit ? 'Save' : 'Add' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  artist: String,
  disc: String,
  stars: Number,
  showStars: Boolean,
  isEdit: Boolean,
})

const emit = defineEmits(['cancel', 'save'])

const localArtist = ref(props.artist ?? '')
const localDisc = ref(props.disc ?? '')
const localStars = ref(props.showStars ? props.stars ?? 0 : undefined)

const handleSave = () => {
  const payload = {
    artist: localArtist.value,
    disc: localDisc.value,
  }

  if (props.showStars) {
    payload.stars = Number.isInteger(localStars.value) ? localStars.value : 0
  }

  emit('save', payload)
}
</script>
