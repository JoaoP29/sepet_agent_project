<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-sepet-primary-light">📋 Questionário de Triagem Clínica</h2>
      <p class="text-sepet-text-muted text-sm mt-2">Responda com atenção — este questionário é indispensável para a anestesia.</p>
    </div>

    <!-- Perguntas Clínicas -->
    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-accent mb-4">🩺 Sinais Clínicos</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.tosse" label="O animal apresenta tosse?" />
        <ToggleQuestion v-model="form.espirro" label="O animal apresenta espirro?" />
        <ToggleQuestion v-model="form.vomito" label="O animal apresenta vômito?" />
        <ToggleQuestion v-model="form.diarreia" label="O animal apresenta diarréia?" />
        <ToggleQuestion v-model="form.perda_apetite" label="Houve perda de apetite?" />
        <ToggleQuestion v-model="form.perda_peso" label="Houve perda de peso?" />
        <ToggleQuestion v-model="form.apatia" label="O animal está apático?" />
      </div>
    </div>

    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-danger mb-4">⚠️ Sinais Graves</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.desmaio" label="O animal já desmaiou?" danger />
        <ToggleQuestion v-model="form.convulsao" label="O animal já teve convulsão?" danger />
        <ToggleQuestion v-model="form.dificuldade_respirar" label="Dificuldade para respirar?" danger />
      </div>
    </div>

    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-secondary mb-4">🔍 Outros Sintomas</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.secrecao_nasal" label="Secreção nasal?" />
        <ToggleQuestion v-model="form.secrecao_ocular" label="Secreção ocular?" />
        <ToggleQuestion v-model="form.lesoes_pele" label="Lesões de pele?" />
        <ToggleQuestion v-model="form.alergias" label="Alergias conhecidas?" />
      </div>
    </div>

    <div class="glass-card p-6">
      <h3 class="text-lg font-semibold text-sepet-primary-light mb-4">📒 Histórico</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ToggleQuestion v-model="form.cirurgia_anterior" label="Já fez cirurgia anterior?" />
        <ToggleQuestion v-model="form.medicacao_uso" label="Está em uso de medicação?" />
        <ToggleQuestion v-model="form.vacinas_em_dia" label="Vacinas estão em dia?" positive />
        <ToggleQuestion v-model="form.jejum_12h" label="Está em jejum de 12 horas?" positive />
      </div>
    </div>

    <div class="glass-card p-6 border-2 border-sepet-warning/40">
      <h3 class="text-lg font-semibold text-sepet-warning mb-4">⚡ Risco Anestésico</h3>
      <ToggleQuestion
        v-model="form.entendeu_risco_anestesico"
        label="O tutor compreendeu e aceita o risco anestésico?"
        positive
      />
    </div>

    <!-- Observações -->
    <div class="glass-card p-6">
      <label class="block text-sm font-medium text-sepet-text-muted mb-2">
        📝 Observações adicionais
      </label>
      <textarea
        v-model="form.observacoes"
        rows="3"
        class="w-full bg-sepet-bg border border-sepet-surface-light rounded-lg px-4 py-3 text-sepet-text placeholder-sepet-text-muted/50 focus:outline-none focus:ring-2 focus:ring-sepet-primary/50 transition-all resize-none"
        placeholder="Informações relevantes sobre o animal..."
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
