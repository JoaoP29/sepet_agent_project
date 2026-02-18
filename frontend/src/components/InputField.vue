<template>
  <div>
    <label class="block text-sm font-medium text-sepet-text-muted mb-1">
      {{ label }} <span v-if="required" class="text-sepet-danger">*</span>
    </label>
    <input
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :required="required"
      class="w-full bg-sepet-bg border border-sepet-surface-light rounded-lg px-4 py-2.5 text-sepet-text placeholder-sepet-text-muted/50 focus:outline-none focus:ring-2 focus:ring-sepet-primary/50 focus:border-sepet-primary transition-all"
    />
  </div>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  placeholder: String,
  type: { type: String, default: 'text' },
  required: Boolean,
})
defineEmits(['update:modelValue'])
</script>
