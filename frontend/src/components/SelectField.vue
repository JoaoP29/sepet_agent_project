<template>
  <div>
    <label class="block text-sm font-medium text-sepet-text-muted mb-1">
      {{ label }} <span v-if="required" class="text-sepet-danger">*</span>
    </label>
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :required="required"
      class="w-full bg-sepet-bg border border-sepet-surface-light rounded-lg px-4 py-2.5 text-sepet-text focus:outline-none focus:ring-2 focus:ring-sepet-primary/50 focus:border-sepet-primary transition-all"
    >
      <option value="" disabled>Selecione...</option>
      <option v-for="opt in options" :key="opt" :value="opt">{{ opt }}</option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  label: String,
  options: Array,
  required: Boolean,
})
defineEmits(['update:modelValue'])
</script>
