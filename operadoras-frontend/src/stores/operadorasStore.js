import { defineStore } from 'pinia'
import { getOperadoras, getOperadora } from '../api/operadoras'

export const useOperadorasStore = defineStore('operadoras', {
  state: () => ({
    lista: [],
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 1,
    loading: false,
    error: null,
    modoBusca: false
  }),

  actions: {
    async fetchOperadoras(page = 1) {
      this.loading = true
      this.error = null
      this.modoBusca = false

      try {
        const res = await getOperadoras({
          page,
          limit: this.limit
        })

        this.lista = res.data.data
        this.page = res.data.page
        this.total = res.data.total
        this.totalPages = Math.ceil(this.total / this.limit)

      } catch (e) {
        this.error = 'Erro ao carregar operadoras'
      } finally {
        this.loading = false
      }
    },

    async buscarPorCnpj(cnpj) {
      this.loading = true
      this.error = null
      this.modoBusca = true

      try {
        const res = await getOperadora(cnpj)

        this.lista = [res.data]

        this.page = 1
        this.totalPages = 1

      } catch (e) {
        this.lista = []
      } finally {
        this.loading = false
      }
    }
  }
})
