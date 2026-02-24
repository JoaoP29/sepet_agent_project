<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-sepet-primary-light">{{ $t('triage.title') }}</h2>
      <p class="text-sepet-text-muted text-sm mt-2">{{ $t('triage.subtitle') }}</p>
    </div>

    <!-- Perguntas Clínicas -->
    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-accent mb-4">{{ $t('triage.clinicalSigns.title') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.tosse" :label="$t('triage.clinicalSigns.cough')" />
        <ToggleQuestion v-model="form.espirro" :label="$t('triage.clinicalSigns.sneezing')" />
        <ToggleQuestion v-model="form.vomito" :label="$t('triage.clinicalSigns.vomiting')" />
        <ToggleQuestion v-model="form.diarreia" :label="$t('triage.clinicalSigns.diarrhea')" />
        <ToggleQuestion v-model="form.perda_apetite" :label="$t('triage.clinicalSigns.appetiteLoss')" />
        <ToggleQuestion v-model="form.perda_peso" :label="$t('triage.clinicalSigns.weightLoss')" />
        <ToggleQuestion v-model="form.apatia" :label="$t('triage.clinicalSigns.apathy')" />
      </div>
    </div>

    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-danger mb-4">{{ $t('triage.severeSigns.title') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.desmaio" :label="$t('triage.severeSigns.fainting')" danger />
        <ToggleQuestion v-model="form.convulsao" :label="$t('triage.severeSigns.seizure')" danger />
        <ToggleQuestion v-model="form.dificuldade_respirar" :label="$t('triage.severeSigns.breathingDifficulty')" danger />
      </div>
    </div>

    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-secondary mb-4">{{ $t('triage.otherSymptoms.title') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.secrecao_nasal" :label="$t('triage.otherSymptoms.nasalDischarge')" />
        <ToggleQuestion v-model="form.secrecao_ocular" :label="$t('triage.otherSymptoms.ocularDischarge')" />
        <ToggleQuestion v-model="form.lesoes_pele" :label="$t('triage.otherSymptoms.skinLesions')" />
        <ToggleQuestion v-model="form.alergias" :label="$t('triage.otherSymptoms.allergies')" />
      </div>
    </div>

    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-primary-light mb-4">{{ $t('triage.history.title') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.cirurgia_anterior" :label="$t('triage.history.previousSurgery')" />
        <ToggleQuestion v-model="form.medicacao_uso" :label="$t('triage.history.currentMedication')" />
        <ToggleQuestion v-model="form.vacinas_em_dia" :label="$t('triage.history.vaccinesUpToDate')" positive />
        <ToggleQuestion v-model="form.jejum_12h" :label="$t('triage.history.fasting12h')" positive />
      </div>
    </div>

    <div class="glass-card p-6 border-2 border-sepet-warning/40">
      <h3 class="text-lg font-semibold text-sepet-warning mb-4">{{ $t('triage.anestheticRisk.title') }}</h3>
      <ToggleQuestion
        v-model="form.entendeu_risco_anestesico"
        :label="$t('triage.anestheticRisk.question')"
        positive
      />
    </div>

    <!-- Observações -->
    <div class="glass-card p-6">
      <label class="block text-sm font-medium text-sepet-text-muted mb-2">
        {{ $t('triage.observations.label') }}
      </label>
      <textarea
        v-model="form.observacoes"
        rows="3"
        class="w-full bg-sepet-bg border border-sepet-surface-light rounded-lg px-4 py-3 text-sepet-text placeholder-sepet-text-muted/50 focus:outline-none focus:ring-2 focus:ring-sepet-primary/50 transition-all resize-none"
        :placeholder="$t('triage.observations.placeholder')"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import ToggleQuestion from './ToggleQuestion.vue'

const emit = defineEmits(['update:modelValue'])

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
})

const form = reactive({
  tosse: false,
  espirro: false,
  vomito: false,
  diarreia: false,
  perda_apetite: false,
  perda_peso: false,
  apatia: false,
  desmaio: false,
  convulsao: false,
  dificuldade_respirar: false,
  secrecao_nasal: false,
  secrecao_ocular: false,
  lesoes_pele: false,
  alergias: false,
  cirurgia_anterior: false,
  medicacao_uso: false,
  vacinas_em_dia: false,
  jejum_12h: false,
  entendeu_risco_anestesico: false,
  observacoes: '',
  ...props.modelValue,
})

watch(form, (val) => {
  emit('update:modelValue', { ...val })
}, { deep: true })
</script>
