import axios from 'axios'

const TENANT_ID = '9a76a8f5-e9f9-458e-9738-4f396a2c344c'

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
        'X-Tenant-ID': TENANT_ID,
    },
})

export function setTenantId(tenantId) {
    api.defaults.headers['X-Tenant-ID'] = tenantId
}

export async function criarAgendamento(dados) {
    const response = await api.post('/agendamentos/', dados)
    return response.data
}

export async function listarAgendamentos() {
    const response = await api.get('/agendamentos/')
    return response.data
}

export async function obterAgendamento(id) {
    const response = await api.get(`/agendamentos/${id}`)
    return response.data
}

export async function listarTriagens() {
    const response = await api.get('/triagens/')
    return response.data
}

export async function obterTriagem(agendamentoId) {
    const response = await api.get(`/triagens/${agendamentoId}`)
    return response.data
}

export async function analisarTriagem(triagemId) {
    const response = await api.post(`/analise/${triagemId}`)
    return response.data
}

export async function gerarComprovante(agendamentoId) {
    const response = await api.get(`/comprovantes/${agendamentoId}`)
    return response.data
}

export default api
