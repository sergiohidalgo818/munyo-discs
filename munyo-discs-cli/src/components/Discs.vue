<template>
  <div class="max-w-5xl mx-auto p-6 text-white">
    <!-- Header -->
    <!-- Header with left and right columns -->
    <div class="flex flex-wrap justify-between items-start gap-4 mb-6">
      <!-- Left side: Tabs and Controls -->
      <div class="flex flex-col gap-3">
        <!-- Tabs -->
        <div class="flex space-x-4">
          <button :class="tab === 'owned' ? activeTabClass : tabClass" @click="tab = 'owned'">Owned CDs</button>
          <button :class="tab === 'wished' ? activeTabClass : tabClass" @click="tab = 'wished'">Wished CDs</button>
        </div>
        <!-- Controls -->
        <div class="flex flex-wrap gap-3 mt-2">
          <button class="bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded-lg text-sm" @click="startAdding">
            + Add CD
          </button>
          <button class="bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded-lg text-sm" @click="showUploadModal = true">
            Upload CSV
          </button>
          <button class="bg-zinc-700 hover:bg-zinc-600 px-4 py-2 rounded-lg text-sm" @click="downloadCsv">
            Download CSV
          </button>
        </div>
      </div>

      <!-- Right side: Search and Sort -->
      <div class="flex flex-col w-full sm:w-72 ml-auto">
        <input v-model="search" type="text" placeholder="Search discs or artists..."
          class="bg-zinc-800 text-white text-sm px-3 py-2 rounded-lg border border-zinc-600 mb-2" />
        <select v-model="sortBy"
          class="bg-zinc-800 text-white text-sm px-3 py-2 rounded-lg border border-zinc-600 w-40 self-end">
          <option value="disc">Sort by Disc</option>
          <option value="artist">Sort by Artist</option>
          <option v-if="tab === 'wished'" value="stars">Sort by Stars</option>
        </select>
      </div>
    </div>
    <!-- Table -->
    <div v-if="paginated.length > 0" class="bg-zinc-900 rounded-lg overflow-hidden border border-zinc-700">
      <ul>
        <li v-for="(disc, index) in paginated" :key="index"
          class="px-4 py-3 border-b border-zinc-700 last:border-b-0 flex justify-between items-center">
          <div>
            <span class="text-base font-medium text-white">{{ disc.disc }}</span>
            <span class="text-sm text-zinc-400 ml-2 italic">by {{ disc.artist }}</span>
            <span v-if="tab === 'wished'" class="text-yellow-400 ml-3 text-sm">
              {{ '★'.repeat(Math.min(Math.max(disc.stars || 0, 0), 5)) }}
            </span>
          </div>
          <div class="flex gap-2">
            <button class="bg-zinc-700 hover:bg-zinc-600 text-sm px-3 py-1 rounded" @click="startEditing(disc)">
              Edit
            </button>
            <button class="bg-red-500 hover:bg-red-400 text-sm px-3 py-1 rounded"
              @click="handleDeleteCd(disc.artist, disc.disc)">
              Delete
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="loading" class="text-zinc-400 italic text-sm text-center mt-8">
      Loading discs...
    </div>
    <div v-else-if="paginated.length === 0" class="text-zinc-400 italic text-sm text-center mt-8">
      No {{ tab }} discs found.
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-6 flex justify-center items-center space-x-2">
      <button @click="page = 1" :disabled="page === 1" class="page-btn">First</button>
      <button @click="page--" :disabled="page === 1" class="page-btn">Prev</button>
      <span v-for="pageNum in visiblePages" :key="pageNum" @click="page = pageNum"
        :class="pageNum === page ? activePageClass : pageClass" class="cursor-pointer">
        {{ pageNum }}
      </span>
      <button @click="page++" :disabled="page === totalPages" class="page-btn">Next</button>
      <button @click="page = totalPages" :disabled="page === totalPages" class="page-btn">Last</button>
    </div>

    <!-- Modals -->
    <FileUploadModal v-if="showUploadModal" :type="tab" @close="showUploadModal = false" @uploaded="handleUploaded" />
    <DiscEditModal v-if="showEditModal" :artist="editArtist" :disc="editDisc" :stars="editStars"
      :showStars="tab === 'wished'" :isEdit="isEditing" @save="handleSaveCd" @cancel="showEditModal = false" />
    <AcceptModal v-if="showAddCDEmpty" title="CD With Empty Fields" message="Cannot add CD with empty fields."
      @accept="showAddCDEmpty = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDiscStore } from '@/stores/discs'
import FileUploadModal from '@/components/FileUploadModal.vue'
import DiscEditModal from '@/components/DiscEditModal.vue'
import AcceptModal from '@/components/AcceptModal.vue'

import {
  downloadOwnedCds,
  addOwnedCd,
  deleteOwnedCd,
  modifyOwnedCd,
  getOwnedCds
} from '@/api/ownedCds'

import {
  downloadWishedCds,
  addWishedCd,
  deleteWishedCd,
  modifyWishedCd,
  getWishedCds
} from '@/api/wishedCds'

const discStore = useDiscStore()
const tab = ref('owned')
const page = ref(1)
const perPage = 10
const sortBy = ref('disc')
const search = ref('')

const showUploadModal = ref(false)
const showEditModal = ref(false)

const editArtist = ref('')
const editDisc = ref('')
const editStars = ref(0)
const editingOriginal = ref(null)
const isEditing = ref(false)

const loading = ref(true)

const showAddCDEmpty = ref(false)


onMounted(() => discStore.fetchDiscs())

async function fetchDiscs() {
  try {
    const [ownedRes, wishedRes] = await Promise.all([
      getOwnedCds(),
      getWishedCds()
    ])
    discStore.owned = ownedRes.data || []
    discStore.wished = wishedRes.data || []
    loading = ref(fals)
  } catch (e) {
    console.error('fetchDiscs error:', e)
  }
}

onMounted(fetchDiscs)

function normalize(str) {
  return str?.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase() || ''
}

const currentList = computed(() => {
  const list = tab.value === 'owned' ? discStore.owned : discStore.wished
  return list.filter((d) => {
    const query = normalize(search.value)
    return normalize(d.artist).includes(query) || normalize(d.disc).includes(query)
  }).sort((a, b) => {
    if (sortBy.value === 'stars') return (b.stars || 0) - (a.stars || 0)
    return normalize(a[sortBy.value]).localeCompare(normalize(b[sortBy.value]))
  })
})

const totalPages = computed(() => Math.ceil(currentList.value.length / perPage))
const paginated = computed(() => currentList.value.slice((page.value - 1) * perPage, page.value * perPage))
const visiblePages = computed(() => {
  const range = 2
  const start = Math.max(1, page.value - range)
  const end = Math.min(totalPages.value, page.value + range)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)

})

watch([sortBy, tab, search], () => page.value = 1)
watch([currentList, totalPages], () => {
  if (page.value > totalPages.value) page.value = totalPages.value || 1
})

function startEditing(disc) {
  editingOriginal.value = disc
  editArtist.value = disc.artist
  editDisc.value = disc.disc
  editStars.value = disc.stars || 0
  isEditing.value = true
  showEditModal.value = true
}

function startAdding() {
  editArtist.value = ''
  editDisc.value = ''
  editStars.value = 0
  isEditing.value = false
  showEditModal.value = true
}

async function handleUploaded() {
  await fetchDiscs()
  showUploadModal.value = false
}

async function handleSaveCd({ artist, disc, stars }) {
  const trimmedArtist = artist?.trim()
  const trimmedDisc = disc?.trim()

  if (!trimmedArtist || !trimmedDisc) {
    showAddCDEmpty.value = true

    return
  }

  try {
    if (isEditing.value) {
      const { artist: oldArtist, disc: oldDisc } = editingOriginal.value
      if (tab.value === 'owned') {
        await modifyOwnedCd(oldArtist, oldDisc, trimmedArtist, trimmedDisc)
      } else {
        await modifyWishedCd(oldArtist, oldDisc, trimmedArtist, trimmedDisc, stars)
      }
    } else {
      if (tab.value === 'owned') {
        await addOwnedCd(trimmedArtist, trimmedDisc)
      } else {
        await addWishedCd(trimmedArtist, trimmedDisc, stars)
      }
    }
    await fetchDiscs()
    showEditModal.value = false
  } catch (error) {
    showAddCDEmpty.value = true
  }
}


async function handleDeleteCd(artist, disc) {
  try {
    if (tab.value === 'owned') {
      await deleteOwnedCd(artist, disc)
    } else {
      await deleteWishedCd(artist, disc)
    }
    await fetchDiscs()
  } catch (error) {
    alert("Delete failed.")
  }
}

const tabClass = 'px-4 py-2 rounded-lg text-sm bg-zinc-700 hover:bg-zinc-600 transition'
const activeTabClass = 'px-4 py-2 rounded-lg text-sm bg-green-500 text-white shadow'
const pageClass = 'px-3 py-1 rounded-md text-sm bg-zinc-700 hover:bg-zinc-600'
const activePageClass = 'px-3 py-1 rounded-md text-sm bg-green-500 text-white'
</script>

<style scoped>
.page-btn {
  @apply px-3 py-1 rounded-md text-sm bg-zinc-700 hover:bg-zinc-600 disabled:opacity-50;
}
</style>
