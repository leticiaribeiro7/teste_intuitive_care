<template>
  <div>
    <h2>{{ operadora?.razao_social }}</h2>
    <p><strong>CNPJ:</strong> {{ operadora?.cnpj }}</p>

    <hr />

    <h3>Histórico de Despesas</h3>

    <table v-if="despesas.length">
      <thead>
        <tr>
          <th>Ano</th>
          <th>Trimestre</th>
          <th>Valor das Despesas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in despesas" :key="d.id">
          <td>{{ d.ano }}</td>
          <td>{{ d.trimestre }}º</td>
          <td>
            R$ {{ d.valor_despesas.toLocaleString('pt-BR') }}
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Nenhuma despesa encontrada.</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getOperadora, getHistorico } from '../api/operadoras'

const route = useRoute()

const operadora = ref(null)
const despesas = ref([])

onMounted(async () => {
  const cnpj = route.params.cnpj
  console.log("cnpj", cnpj)

  // detalhes da operadora
  const opRes = await getOperadora(cnpj)
  operadora.value = opRes.data

  // histórico de despesas (ARRAY)
  const despRes = await getHistorico(cnpj)
  despesas.value = despRes.data
})
</script>
