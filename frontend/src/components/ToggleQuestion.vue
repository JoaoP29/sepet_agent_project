<template>
  <div
    class="flex items-center justify-between p-3 rounded-xl transition-all duration-300 cursor-pointer select-none"
    :class="containerClass"
    @click="toggle"
  >
    <span class="text-sm font-medium" :class="modelValue ? activeTextClass : 'text-sepet-text'">
      {{ label }}
    </span>
    <div
      class="relative w-12 h-6 rounded-full transition-all duration-300"
      :class="modelValue ? activeBgClass : 'bg-sepet-surface-light'"
    >
      <div
        class="absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-md transition-all duration-300"
        :class="modelValue ? 'left-6' : 'left-0.5'"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  label: String,
  danger: Boolean,
  positive: Boolean,
})

const emit = defineEmits(['update:modelValue'])

function toggle() {
  emit('update:modelValue', !props.modelValue)
}

const containerClass = computed(() => {
  if (!props.modelValue) return 'bg-sepet-bg/50 hover:bg-sepet-surface-light/30'
  if (props.danger) return 'bg-sepet-danger/10 ring-1 ring-sepet-danger/30'
  if (props.positive) return 'bg-sepet-success/10 ring-1 ring-sepet-success/30'
  return 'bg-sepet-warning/10 ring-1 ring-sepet-warning/30'
})

const activeBgClass = computed(() => {
  if (props.danger) return 'bg-sepet-danger'
  if (props.positive) return 'bg-sepet-success'
  return 'bg-sepet-warning'
})

const activeTextClass = computed(() => {
  if (props.danger) return 'text-sepet-danger'
  if (props.positive) return 'text-sepet-success'
  return 'text-sepet-warning'
})
</script>
