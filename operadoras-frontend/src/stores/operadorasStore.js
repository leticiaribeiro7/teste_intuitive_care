import { defineStore } from 'pinia'
import { getOperadoras } from '../api/operadoras'

export const useOperadorasStore = defineStore('operadoras', {
  state: () => ({
    lista: [],
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 1,
    loading: false,
    error: null
  }),

  actions: {
    async fetchOperadoras(page = 1) {
      this.loading = true
      this.error = null

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
    }
  }
})
