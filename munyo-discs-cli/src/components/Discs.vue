
<template>
  <div class="max-w-5xl mx-auto p-6 text-white">
    <!-- Header: Tabs + Search + Sort + Upload + Download -->
    <div class="flex justify-between items-center mb-6 flex-wrap gap-4">
      <!-- Tabs -->
      <div class="flex space-x-4">
        <button
          :class="tab === 'owned' ? activeTabClass : tabClass"
          @click="tab = 'owned'"
        >
          Owned CDs
        </button>
        <button
          :class="tab === 'wished' ? activeTabClass : tabClass"
          @click="tab = 'wished'"
        >
          Wished CDs
        </button>
      </div>

      <!-- Search -->
      <input
        v-model="search"
        type="text"
        placeholder="Search discs or artists..."
        class="bg-zinc-800 text-white text-sm px-3 py-2 rounded-lg border border-zinc-600 w-full sm:w-64"
      />

      <!-- Right controls -->
      <div class="flex items-center gap-4">
        <select
          v-model="sortBy"
          class="bg-zinc-800 text-white text-sm px-3 py-2 rounded-lg border border-zinc-600"
        >
          <option value="disc">Sort by Disc</option>
          <option value="artist">Sort by Artist</option>
          <option v-if="tab === 'wished'" value="stars">Sort by Stars</option>
        </select>

        <button
          class="bg-zinc-800 hover:bg-zinc-700 px-4 py-2 rounded-lg text-sm"
          @click="showUploadModal = true"
        >
          Upload CSV
        </button>

        <button
          class="bg-zinc-800 hover:bg-zinc-700 px-4 py-2 rounded-lg text-sm"
          @click="downloadCsv"
        >
          Download CSV
        </button>
      </div>
    </div>

    <!-- Table -->
    <div
      v-if="paginated.length > 0"
      class="bg-zinc-900 rounded-lg overflow-hidden border border-zinc-700"
    >
      <ul>
        <li
          v-for="(disc, index) in paginated"
          :key="index"
          class="px-4 py-3 border-b border-zinc-700 last:border-b-0"
        >
          <span class="text-base font-medium text-white">{{ disc.disc }}</span>
          <span class="text-sm text-zinc-400 ml-2 italic">by {{ disc.artist }}</span>

          <span
            v-if="tab === 'wished'"
            class="text-yellow-400 ml-3 text-sm"
          >
            {{ '★'.repeat(Math.min(Math.max(disc.stars || 0, 0), 5)) }}
          </span>
        </li>
      </ul>
    </div>
    <div v-else class="text-zinc-400 italic text-sm text-center mt-8">
      No {{ tab }} discs found.
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-6 flex justify-center items-center space-x-2">
      <button
        @click="page = 1"
        :disabled="page === 1"
        class="px-3 py-1 rounded-md text-sm bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50"
      >
        First
      </button>

      <button
        @click="page--"
        :disabled="page === 1"
        class="px-3 py-1 rounded-md text-sm bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50"
      >
        Prev
      </button>

      <span
        v-for="pageNum in visiblePages"
        :key="pageNum"
        @click="page = pageNum"
        :class="pageNum === page ? activePageClass : pageClass"
        class="cursor-pointer"
      >
        {{ pageNum }}
      </span>

      <button
        @click="page++"
        :disabled="page === totalPages"
        class="px-3 py-1 rounded-md text-sm bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50"
      >
        Next
      </button>

      <button
        @click="page = totalPages"
        :disabled="page === totalPages"
        class="px-3 py-1 rounded-md text-sm bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50"
      >
        Last
      </button>
    </div>

    <!-- Delete Collisions Button -->
    <div v-if="tab === 'wished'" class="mt-6 text-center">
      <button
        @click="showConfirmModal = true"
        class="bg-red-600 hover:bg-red-500 text-white px-6 py-2 rounded-lg text-sm transition"
      >
        Remove Owned from Wished
      </button>
    </div>

    <!-- Upload Modal -->
    <FileUploadModal
      v-if="showUploadModal"
      :type="tab"
      @close="showUploadModal = false"
      @uploaded="handleUploaded"
    />

    <!-- Confirm Modal -->
    <ConfirmModal
      v-if="showConfirmModal"
      title="Remove Collisions"
      message="This will remove any discs from the wished list that already exist in the owned list. Are you sure?"
      @confirm="confirmDeleteCollisions"
      @cancel="showConfirmModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDiscStore } from '@/stores/discs'
import FileUploadModal from '@/components/FileUploadModal.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import { downloadOwnedCds } from '@/api/ownedCds'
import { downloadWishedCds } from '@/api/wishedCds'

const discStore = useDiscStore()

const tab = ref('owned')
const page = ref(1)
const perPage = 10
const showUploadModal = ref(false)
const showConfirmModal = ref(false)
const sortBy = ref('disc')
const search = ref('')

// Load on mount
onMounted(() => {
  discStore.fetchDiscs()
})

// Normalize for accent-insensitive search
function normalize(str) {
  return str?.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase() || ''
}

// Sorted & filtered list
const currentList = computed(() => {
  const list = tab.value === 'owned' ? discStore.owned : discStore.wished

  const filtered = list.filter((disc) => {
    const query = normalize(search.value)
    return (
      normalize(disc.artist).includes(query) ||
      normalize(disc.disc).includes(query)
    )
  })

  return filtered.sort((a, b) => {
    if (sortBy.value === 'stars') {
      return (b.stars || 0) - (a.stars || 0)
    }
    const aVal = normalize(a[sortBy.value])
    const bVal = normalize(b[sortBy.value])
    return aVal.localeCompare(bVal)
  })
})

// Pagination logic
const totalPages = computed(() =>
  Math.ceil(currentList.value.length / perPage)
)

const paginated = computed(() => {
  const start = (page.value - 1) * perPage
  return currentList.value.slice(start, start + perPage)
})

const visiblePages = computed(() => {
  const range = 2
  const start = Math.max(1, page.value - range)
  const end = Math.min(totalPages.value, page.value + range)
  const pages = []
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

// Reset page on changes
watch([sortBy, tab, search], () => {
  page.value = 1
})

watch([currentList, totalPages], () => {
  if (page.value > totalPages.value) {
    page.value = totalPages.value || 1
  }
})

// Actions
function handleUploaded() {
  discStore.fetchDiscs()
  showUploadModal.value = false
}

async function confirmDeleteCollisions() {
  await discStore.removeCollisions()
  showConfirmModal.value = false
}

// CSV Download using your updated API modules
async function downloadCsv() {
  try {
    const response =
      tab.value === 'owned'
        ? await downloadOwnedCds()
        : await downloadWishedCds()

    const blob = new Blob([response.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${tab.value}-cds.csv`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Download failed:', error)
    alert('Failed to download CSV: ' + error.message)
  }
}

// Styles
const tabClass =
  'px-4 py-2 rounded-lg text-sm bg-zinc-800 hover:bg-zinc-700 transition'
const activeTabClass =
  'px-4 py-2 rounded-lg text-sm bg-green-600 text-white shadow'

const pageClass =
  'px-3 py-1 rounded-md text-sm bg-zinc-800 hover:bg-zinc-700'
const activePageClass =
  'px-3 py-1 rounded-md text-sm bg-green-600 text-white'
</script>

