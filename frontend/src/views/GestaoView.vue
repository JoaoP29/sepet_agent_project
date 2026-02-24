<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-extrabold bg-gradient-to-r from-sepet-secondary to-sepet-primary-light bg-clip-text text-transparent">
          {{ $t('management.title') }}
        </h1>
        <p class="text-sepet-text-muted mt-1">{{ $t('management.subtitle') }}</p>
      </div>
      <button @click="carregar" :disabled="carregando" class="px-4 py-2 bg-sepet-secondary text-white rounded-xl font-semibold hover:bg-sepet-secondary-dark transition-all shadow-lg shadow-sepet-secondary/30 flex items-center gap-2">
        <svg v-if="carregando" class="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
        🔄 {{ $t('management.refresh') }}
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="glass-card p-4 text-center">
        <p class="text-3xl font-bold text-sepet-primary-light">{{ agendamentos.length }}</p>
        <p class="text-xs text-sepet-text-muted mt-1">{{ $t('management.stats.schedulings') }}</p>
      </div>
      <div class="glass-card p-4 text-center">
        <p class="text-3xl font-bold text-sepet-warning">{{ alertas }}</p>
        <p class="text-xs text-sepet-text-muted mt-1">{{ $t('management.stats.riskAlerts') }}</p>
      </div>
      <div class="glass-card p-4 text-center">
        <p class="text-3xl font-bold text-sepet-success">{{ pareceres }}</p>
        <p class="text-xs text-sepet-text-muted mt-1">{{ $t('management.stats.aiOpinions') }}</p>
      </div>
    </div>

    <!-- Error -->
    <div v-if="erro" class="glass-card p-4 border border-sepet-danger/40 text-sepet-danger text-sm">
      ❌ {{ erro }}
    </div>

    <!-- Empty -->
    <div v-if="!carregando && agendamentos.length === 0" class="glass-card p-12 text-center">
      <span class="text-5xl">📭</span>
      <p class="text-sepet-text-muted mt-4">{{ $t('management.empty') }}</p>
    </div>

    <!-- Cards -->
    <div class="space-y-4">
      <div
        v-for="ag in agendamentos"
        :key="ag.id"
        class="glass-card p-5 hover:border-sepet-primary/30 transition-all duration-300"
        :class="{ 'border-l-4 border-l-sepet-danger': getTriagem(ag.id)?.alerta_risco }"
      >
        <div class="flex flex-col lg:flex-row lg:items-start gap-4">
          <!-- Info -->
          <div class="flex-1 space-y-2">
            <div class="flex items-center gap-3">
              <span class="text-2xl">{{ ag.especie === 'Canina' ? '🐕' : '🐈' }}</span>
              <div>
                <h3 class="font-bold text-lg text-sepet-text">{{ ag.nome_animal }}</h3>
                <p class="text-xs text-sepet-text-muted">
                  {{ ag.especie }} · {{ ag.raca }} · Porte {{ ag.porte }}
                </p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span class="text-sepet-text-muted">{{ $t('management.labels.tutor') }}</span>
                <span class="text-sepet-text ml-1">{{ ag.nome_tutor }}</span>
              </div>
              <div>
                <span class="text-sepet-text-muted">{{ $t('management.labels.cpf') }}</span>
                <span class="text-sepet-text ml-1">{{ ag.cpf_tutor }}</span>
              </div>
              <div>
                <span class="text-sepet-text-muted">{{ $t('management.labels.date') }}</span>
                <span class="text-sepet-text ml-1">{{ formatDate(ag.data_atendimento) }}</span>
              </div>
              <div>
                <span class="text-sepet-text-muted">{{ $t('management.labels.status') }}</span>
                <span
                  class="ml-1 px-2 py-0.5 rounded-full text-xs font-semibold"
                  :class="statusClass(ag.status_ia)"
                >
                  {{ ag.status_ia }}
                </span>
              </div>
            </div>
          </div>

          <!-- Triagem & Parecer IA -->
          <div class="lg:w-96 space-y-3">
            <div v-if="getTriagem(ag.id)" class="space-y-2">
              <!-- Alerta -->
              <div
                v-if="getTriagem(ag.id).alerta_risco"
                class="bg-sepet-danger/10 border border-sepet-danger/30 rounded-xl p-3 flex items-center gap-2"
              >
                <span class="text-xl">🚨</span>
                <span class="text-sm font-semibold text-sepet-danger">{{ $t('management.labels.riskAlert') }}</span>
              </div>

              <!-- Detalhes triagem -->
              <button
                @click="toggleTriagem(ag.id)"
                class="w-full text-left bg-sepet-bg/50 hover:bg-sepet-surface-light/30 rounded-xl p-3 transition-all text-sm"
              >
                <span class="text-sepet-text-muted">{{ $t('management.labels.viewTriage') }}</span>
              </button>
              <div v-if="triagemAberta === ag.id" class="bg-sepet-bg/60 rounded-xl p-3 text-xs space-y-1">
                <div
                  v-for="(val, key) in filterTriagemResponses(getTriagem(ag.id).respostas_triagem)"
                  :key="key"
                  class="flex justify-between"
                >
                  <span class="text-sepet-text-muted capitalize">{{ formatKey(key) }}</span>
                  <span :class="typeof val === 'boolean' ? (val ? 'text-sepet-warning' : 'text-sepet-success') : 'text-sepet-text'">
                    {{ typeof val === 'boolean' ? (val ? $t('management.booleans.yes') : $t('management.booleans.no')) : val }}
                  </span>
                </div>
              </div>

              <!-- Parecer IA -->
              <div v-if="getTriagem(ag.id).parecer_ia" class="bg-sepet-secondary/10 border border-sepet-secondary/30 rounded-xl p-4">
                <p class="text-xs font-semibold text-sepet-secondary mb-1">{{ $t('management.labels.aiOpinion') }}</p>
                <p class="text-sm text-sepet-text leading-relaxed">{{ getTriagem(ag.id).parecer_ia }}</p>
              </div>
              <div v-else class="bg-sepet-surface/50 rounded-xl p-3 text-center">
                <p class="text-xs text-sepet-text-muted">{{ $t('management.labels.aiPending') }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { listarAgendamentos, listarTriagens } from '../services/api'

const { t, locale } = useI18n()

const agendamentos = ref([])
const triagens = ref([])
const carregando = ref(false)
const erro = ref('')
const triagemAberta = ref(null)

const alertas = computed(() => triagens.value.filter(t => t.alerta_risco).length)
const pareceres = computed(() => triagens.value.filter(t => t.parecer_ia).length)

function getTriagem(agId) {
  return triagens.value.find(t => t.agendamento_id === agId)
}

function toggleTriagem(agId) {
  triagemAberta.value = triagemAberta.value === agId ? null : agId
}

function filterTriagemResponses(respostas) {
  if (!respostas) return {}
  const filtered = {}
  for (const [key, val] of Object.entries(respostas)) {
    if (!key.startsWith('_meta')) {
      filtered[key] = val
    }
  }
  return filtered
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString(locale.value)
}

function formatKey(key) {
  return key.replace(/_/g, ' ')
}

function statusClass(status) {
  const map = {
    Pendente: 'bg-sepet-warning/20 text-sepet-warning',
    Analisado: 'bg-sepet-success/20 text-sepet-success',
    Cancelado: 'bg-sepet-danger/20 text-sepet-danger',
  }
  return map[status] || 'bg-sepet-surface-light text-sepet-text-muted'
}

async function carregar() {
  carregando.value = true
  erro.value = ''
  try {
    const [ag, tr] = await Promise.all([listarAgendamentos(), listarTriagens()])
    agendamentos.value = ag
    triagens.value = tr
  } catch (e) {
    erro.value = e.response?.data?.detail || t('management.error.generic')
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>
