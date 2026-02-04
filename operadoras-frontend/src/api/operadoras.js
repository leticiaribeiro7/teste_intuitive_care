import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

export const getOperadoras = (params) =>
  api.get('/operadoras', { params })

export const getOperadora = (cnpj) =>
  api.get(`/operadoras/${cnpj}`)

export const getHistorico = (cnpj) =>
  api.get(`/operadoras/${cnpj}/despesas`)

export const getEstatisticas = () =>
  api.get('/estatisticas')
