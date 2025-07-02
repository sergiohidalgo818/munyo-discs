<template>
  <div class="flex gap-1">
    <span v-for="n in 5" :key="n" class="cursor-pointer text-2xl transition"
      :class="n <= (hovered || modelValue) ? 'text-yellow-400' : 'text-zinc-600'" @click="$emit('update:modelValue', n)"
      @mouseover="hovered = n" @mouseleave="hovered = null">
      ★
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  modelValue: Number
})

defineEmits(['update:modelValue'])

const hovered = ref(null)
</script>
