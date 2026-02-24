<template>
  <div class="glass-card p-6 border-2 border-sepet-accent/30">
    <div class="text-center mb-6">
      <span class="text-4xl">📜</span>
      <h3 class="text-xl font-bold text-sepet-accent mt-2">{{ $t('authorization.title') }}</h3>
    </div>

    <div class="bg-sepet-bg/60 rounded-xl p-5 text-sm text-sepet-text-muted leading-relaxed space-y-3">
      <p>
        {{ $t('authorization.bodyIntro', {
          tutorName: tutorNome || '___________',
          cpf: tutorCpf || '___________',
          petName: petNome || '___________',
          species: petEspecie || '___________',
          breed: petRaca || '___________'
        }) }}
      </p>

      <ul class="space-y-2 ml-4">
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>{{ $t('authorization.item1') }}</span>
        </li>
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>{{ $t('authorization.item2') }}</span>
        </li>
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>{{ $t('authorization.item3') }}</span>
        </li>
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>{{ $t('authorization.item4') }}</span>
        </li>
      </ul>

      <div class="mt-4 pt-4 border-t border-sepet-surface-light/30 text-xs">
        <p>{{ $t('footer.line2') }}</p>
        <p>{{ $t('footer.line1') }}</p>
      </div>
    </div>

    <label
      class="flex items-center gap-3 mt-6 p-4 rounded-xl cursor-pointer transition-all duration-300"
      :class="modelValue ? 'bg-sepet-success/10 ring-1 ring-sepet-success/40' : 'bg-sepet-bg/50 hover:bg-sepet-surface-light/30'"
    >
      <input
        type="checkbox"
        :checked="modelValue"
        @change="$emit('update:modelValue', $event.target.checked)"
        class="w-5 h-5 rounded border-sepet-surface-light text-sepet-success focus:ring-sepet-success/50 bg-sepet-bg"
      />
      <span class="text-sm font-medium" :class="modelValue ? 'text-sepet-success' : 'text-sepet-text'">
        {{ $t('authorization.checkbox') }}
      </span>
    </label>
  </div>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  tutorNome: String,
  tutorCpf: String,
  petNome: String,
  petEspecie: String,
  petRaca: String,
})

defineEmits(['update:modelValue'])
</script>
