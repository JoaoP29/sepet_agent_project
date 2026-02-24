import { createRouter, createWebHistory } from 'vue-router'
import AgendamentoView from '../views/AgendamentoView.vue'
import GestaoView from '../views/GestaoView.vue'
import i18n from '../i18n'

const routes = [
    {
        path: '/',
        name: 'agendamento',
        component: AgendamentoView,
        meta: { titleKey: 'routes.scheduling' },
    },
    {
        path: '/gestao',
        name: 'gestao',
        component: GestaoView,
        meta: { titleKey: 'routes.management' },
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to) => {
    const titleKey = to.meta?.titleKey
    document.title = titleKey ? i18n.global.t(titleKey) : 'SEPET'
})

export default router
