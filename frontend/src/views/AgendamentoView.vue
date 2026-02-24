<template>
  <div class="space-y-8">
    <!-- Hero -->
    <div class="text-center">
      <h1 class="text-3xl font-extrabold bg-gradient-to-r from-sepet-primary-light to-sepet-secondary bg-clip-text text-transparent">
        {{ $t('scheduling.title') }}
      </h1>
      <p class="text-sepet-text-muted mt-2">{{ $t('scheduling.subtitle') }}</p>
    </div>

    <!-- Stepper -->
    <div class="flex items-center justify-center gap-2 mb-8">
      <div
        v-for="(s, i) in translatedSteps"
        :key="i"
        class="flex items-center gap-2"
      >
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-500"
          :class="i <= step ? 'bg-sepet-primary text-white shadow-lg shadow-sepet-primary/40 scale-110' : 'bg-sepet-surface text-sepet-text-muted'"
        >
          {{ i < step ? '✓' : i + 1 }}
        </div>
        <span class="hidden sm:inline text-xs font-medium" :class="i <= step ? 'text-sepet-primary-light' : 'text-sepet-text-muted'">
          {{ s }}
        </span>
        <div v-if="i < translatedSteps.length - 1" class="w-8 h-0.5 rounded" :class="i < step ? 'bg-sepet-primary' : 'bg-sepet-surface-light'"></div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="enviado" class="glass-card p-8 text-center space-y-4 animate-fade-in">
      <span class="text-6xl">🎉</span>
      <h2 class="text-2xl font-bold text-sepet-success">{{ $t('scheduling.success.title') }}</h2>
      <p class="text-sepet-text-muted">{{ $t('scheduling.success.message') }}</p>
      <div class="glass-card p-4 inline-block">
        <p class="text-xs text-sepet-text-muted">{{ $t('scheduling.success.protocol') }}</p>
        <p class="text-lg font-mono font-bold text-sepet-primary-light">{{ agendamentoId }}</p>
      </div>
      <div class="pt-4">
        <button
          @click="resetForm"
          class="px-6 py-3 bg-sepet-primary text-white rounded-xl font-semibold hover:bg-sepet-primary-dark transition-all shadow-lg shadow-sepet-primary/30"
        >
          {{ $t('scheduling.buttons.newScheduling') }}
        </button>
      </div>
    </div>

    <!-- Step 1: Dados do Tutor e Pet -->
    <div v-else-if="step === 0" class="space-y-6">
      <div class="glass-card p-6">
        <h3 class="text-lg font-semibold text-sepet-primary-light mb-4">{{ $t('scheduling.tutor.title') }}</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <InputField v-model="form.nome_tutor" :label="$t('scheduling.tutor.fullName')" :placeholder="$t('scheduling.tutor.fullNamePlaceholder')" required />
          <InputField v-model="form.cpf_tutor" :label="$t('scheduling.tutor.cpf')" :placeholder="$t('scheduling.tutor.cpfPlaceholder')" required />
          <InputField v-model="form.telefone_tutor" :label="$t('scheduling.tutor.phone')" :placeholder="$t('scheduling.tutor.phonePlaceholder')" />
          <InputField v-model="form.email_tutor" :label="$t('scheduling.tutor.email')" :placeholder="$t('scheduling.tutor.emailPlaceholder')" type="email" />
        </div>
      </div>

      <div class="glass-card p-6">
        <h3 class="text-lg font-semibold text-sepet-primary-light mb-4">{{ $t('scheduling.pet.title') }}</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <InputField v-model="form.nome_animal" :label="$t('scheduling.pet.name')" :placeholder="$t('scheduling.pet.namePlaceholder')" required />
          <SelectField v-model="form.especie" :label="$t('scheduling.pet.species')" :options="['Canina', 'Felina']" required />
          <InputField v-model="form.raca" :label="$t('scheduling.pet.breed')" :placeholder="$t('scheduling.pet.breedPlaceholder')" />
          <SelectField v-model="form.porte" :label="$t('scheduling.pet.size')" :options="['P', 'M', 'G', 'XG']" required />
          <SelectField v-model="form.sexo" :label="$t('scheduling.pet.sex')" :options="['M', 'F']" required />
          <InputField v-model.number="form.peso_kg" :label="$t('scheduling.pet.weight')" :placeholder="$t('scheduling.pet.weightPlaceholder')" type="number" />
          <InputField v-model.number="form.idade_anos" :label="$t('scheduling.pet.ageYears')" :placeholder="$t('scheduling.pet.ageYearsPlaceholder')" type="number" />
          <InputField v-model.number="form.idade_meses" :label="$t('scheduling.pet.ageMonths')" :placeholder="$t('scheduling.pet.ageMonthsPlaceholder')" type="number" />
          <InputField v-model="form.data_atendimento" :label="$t('scheduling.pet.desiredDate')" type="date" required />
        </div>
      </div>

      <div class="flex justify-end">
        <button
          @click="nextStep"
          :disabled="!step1Valid"
          class="px-8 py-3 rounded-xl font-semibold text-white transition-all duration-300 shadow-lg"
          :class="step1Valid ? 'bg-sepet-primary hover:bg-sepet-primary-dark shadow-sepet-primary/30 hover:scale-105' : 'bg-sepet-surface-light cursor-not-allowed opacity-50'"
        >
          {{ $t('scheduling.buttons.nextTriage') }}
        </button>
      </div>
    </div>

    <!-- Step 2: Triagem -->
    <div v-else-if="step === 1">
      <TriagemForm v-model="form.triagem" />
      <div class="flex justify-between mt-6">
        <button @click="prevStep" class="px-6 py-3 rounded-xl font-semibold text-sepet-text-muted bg-sepet-surface hover:bg-sepet-surface-light transition-all">
          {{ $t('scheduling.buttons.back') }}
        </button>
        <button
          @click="nextStep"
          class="px-8 py-3 bg-sepet-primary text-white rounded-xl font-semibold hover:bg-sepet-primary-dark transition-all shadow-lg shadow-sepet-primary/30 hover:scale-105"
        >
          {{ $t('scheduling.buttons.nextAuth') }}
        </button>
      </div>
    </div>

    <!-- Step 3: Termo -->
    <div v-else-if="step === 2">
      <TermoAutorizacao
        v-model="termoAceito"
        :tutor-nome="form.nome_tutor"
        :tutor-cpf="form.cpf_tutor"
        :pet-nome="form.nome_animal"
        :pet-especie="form.especie"
        :pet-raca="form.raca"
      />
      <div class="flex justify-between mt-6">
        <button @click="prevStep" class="px-6 py-3 rounded-xl font-semibold text-sepet-text-muted bg-sepet-surface hover:bg-sepet-surface-light transition-all">
          {{ $t('scheduling.buttons.back') }}
        </button>
        <button
          @click="enviar"
          :disabled="!termoAceito || enviando"
          class="px-8 py-3 rounded-xl font-semibold text-white transition-all duration-300 shadow-lg"
          :class="termoAceito && !enviando ? 'bg-sepet-success hover:bg-green-600 shadow-sepet-success/30 hover:scale-105' : 'bg-sepet-surface-light cursor-not-allowed opacity-50'"
        >
          <span v-if="enviando" class="flex items-center gap-2">
            <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ $t('scheduling.buttons.sending') }}
          </span>
          <span v-else>{{ $t('scheduling.buttons.confirmSend') }}</span>
        </button>
      </div>

      <!-- Error -->
      <div v-if="erro" class="glass-card mt-4 p-4 border border-sepet-danger/40 text-sepet-danger text-sm">
        ❌ {{ erro }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import TriagemForm from '../components/TriagemForm.vue'
import TermoAutorizacao from '../components/TermoAutorizacao.vue'
import InputField from '../components/InputField.vue'
import SelectField from '../components/SelectField.vue'
import { criarAgendamento } from '../services/api'

const { t } = useI18n()

const translatedSteps = computed(() => [
  t('scheduling.steps.data'),
  t('scheduling.steps.triage'),
  t('scheduling.steps.authorization'),
])
const step = ref(0)
const termoAceito = ref(false)
const enviando = ref(false)
const enviado = ref(false)
const agendamentoId = ref('')
const erro = ref('')

const form = reactive({
  nome_tutor: '',
  cpf_tutor: '',
  telefone_tutor: '',
  email_tutor: '',
  nome_animal: '',
  especie: 'Canina',
  raca: 'SRD',
  porte: 'M',
  sexo: 'M',
  peso_kg: 0,
  idade_anos: 0,
  idade_meses: 0,
  data_atendimento: '',
  triagem: {},
})

const step1Valid = computed(() => {
  return form.nome_tutor && form.cpf_tutor &&
    form.nome_animal && form.especie && form.porte && form.sexo &&
    form.data_atendimento
})

function nextStep() { step.value++ }
function prevStep() { step.value-- }

async function enviar() {
  enviando.value = true
  erro.value = ''
  try {
    const result = await criarAgendamento(form)
    agendamentoId.value = result.id
    enviado.value = true
  } catch (e) {
    erro.value = e.response?.data?.detail || t('scheduling.error.generic')
  } finally {
    enviando.value = false
  }
}

function resetForm() {
  Object.assign(form, {
    nome_tutor: '', cpf_tutor: '', telefone_tutor: '', email_tutor: '',
    nome_animal: '', especie: 'Canina', raca: 'SRD',
    porte: 'M', sexo: 'M', peso_kg: 0, idade_anos: 0,
    idade_meses: 0, data_atendimento: '', triagem: {},
  })
  termoAceito.value = false
  enviado.value = false
  agendamentoId.value = ''
  step.value = 0
}
</script>
