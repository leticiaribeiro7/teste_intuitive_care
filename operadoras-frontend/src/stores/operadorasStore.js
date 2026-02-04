import { defineStore } from 'pinia'
import { getOperadoras, getHistorico } from '../api/operadoras'


export const useOperadorasStore = defineStore('operadoras', {
state: () => ({
lista: [],
despesasUF: [],
loading: false,
error: null,
totalPages: 1
}),
actions: {
async fetchOperadoras(params) {
this.loading = true
try {
const res = await getOperadoras(params)
this.lista = res.data.data
this.totalPages = res.data.totalPages
} catch {
this.error = 'Erro ao carregar operadoras'
} finally {
this.loading = false
}
},
async fetchDespesasUF() {
const res = await getHistorico()
this.despesasUF = res.data
}
}
})