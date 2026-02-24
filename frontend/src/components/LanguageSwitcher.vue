<template>
  <div class="flex items-center gap-1">
    <button
      v-for="loc in locales"
      :key="loc.code"
      @click="switchLocale(loc.code)"
      class="px-2 py-1 rounded-lg text-xs font-semibold transition-all duration-300"
      :class="currentLocale === loc.code
        ? 'bg-sepet-primary/20 text-sepet-primary-light ring-1 ring-sepet-primary/40'
        : 'text-sepet-text-muted hover:text-white hover:bg-sepet-surface-light'"
      :title="loc.label"
    >
      {{ loc.flag }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const locales = [
  { code: 'pt-BR', flag: '🇧🇷', label: 'Português' },
  { code: 'en', flag: '🇺🇸', label: 'English' },
  { code: 'es', flag: '🇪🇸', label: 'Español' },
]

const currentLocale = computed(() => locale.value)

function switchLocale(code) {
  locale.value = code
  localStorage.setItem('sepet-locale', code)
  document.documentElement.lang = code
}
</script>
