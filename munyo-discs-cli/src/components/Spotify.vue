<template>
  <div class="max-w-5xl mx-auto p-6 text-white">
    <AcceptModal title="Part Under Construction"
      message="This part is under construction. You will be redirected to the main page."
      @accept="redirectToMainPage" />
  </div>
</template>

<script setup>
import AcceptModal from '@/components/AcceptModal.vue'
import { useRouter } from 'vue-router'

const router = useRouter()


async function redirectToMainPage() {
  router.push('/')

}
</script>
