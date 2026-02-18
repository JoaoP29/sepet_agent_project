import { createRouter, createWebHistory } from 'vue-router'
import AgendamentoView from '../views/AgendamentoView.vue'
import GestaoView from '../views/GestaoView.vue'

const routes = [
    {
        path: '/',
        name: 'agendamento',
        component: AgendamentoView,
        meta: { title: 'Agendamento – SEPET' },
    },
    {
        path: '/gestao',
        name: 'gestao',
        component: GestaoView,
        meta: { title: 'Gestão – SEPET' },
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to) => {
    document.title = to.meta?.title || 'SEPET'
})

export default router
