<template>
  <div class="glass-card p-6 border-2 border-sepet-accent/30">
    <div class="text-center mb-6">
      <span class="text-4xl">📜</span>
      <h3 class="text-xl font-bold text-sepet-accent mt-2">Termo de Autorização Cirúrgica</h3>
    </div>

    <div class="bg-sepet-bg/60 rounded-xl p-5 text-sm text-sepet-text-muted leading-relaxed space-y-3">
      <p>
        Eu, <strong class="text-sepet-text">{{ tutorNome || '___________' }}</strong>, portador(a)
        do CPF <strong class="text-sepet-text">{{ tutorCpf || '___________' }}</strong>, na
        qualidade de tutor(a) responsável pelo animal
        <strong class="text-sepet-text">{{ petNome || '___________' }}</strong>, da espécie
        <strong class="text-sepet-text">{{ petEspecie || '___________' }}</strong>, raça
        <strong class="text-sepet-text">{{ petRaca || '___________' }}</strong>, declaro que:
      </p>

      <ul class="space-y-2 ml-4">
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>Respondi o questionário clínico com veracidade e assumo responsabilidade pelas informações prestadas.</span>
        </li>
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>Estou ciente de que <strong class="text-sepet-warning">o questionário de triagem é indispensável para a anestesia</strong> e que informações falsas podem colocar a vida do animal em risco.</span>
        </li>
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>Fui informado(a) sobre os riscos inerentes ao procedimento cirúrgico e anestésico, incluindo possíveis complicações.</span>
        </li>
        <li class="flex items-start gap-2">
          <span class="text-sepet-accent mt-0.5">•</span>
          <span>Autorizo a realização do procedimento de esterilização no animal acima identificado.</span>
        </li>
      </ul>

      <div class="mt-4 pt-4 border-t border-sepet-surface-light/30 text-xs">
        <p>📍 Av. Umberto Calderaro, 934 – Adrianópolis, Manaus-AM</p>
        <p>📧 agendamento@sepet.am.gov.br · 📞 (92) 99207-1671</p>
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
        Declaro que li, compreendi e concordo com os termos acima.
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
