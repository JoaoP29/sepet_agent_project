import { createI18n } from 'vue-i18n'
import ptBR from './locales/pt-BR.json'
import en from './locales/en.json'
import es from './locales/es.json'

const savedLocale = localStorage.getItem('sepet-locale') || 'pt-BR'

const i18n = createI18n({
    legacy: false,
    locale: savedLocale,
    fallbackLocale: 'pt-BR',
    messages: {
        'pt-BR': ptBR,
        'en': en,
        'es': es,
    },
})

export default i18n
