<script setup>
import { onMounted } from 'vue'
import { useOperadorasStore } from '../stores/operadorasStore'
import OperadorasTable from '../components/OperadorasTable.vue'

const store = useOperadorasStore()

onMounted(() => {
  store.fetchOperadoras(1)
})

function changePage(newPage) {
  store.fetchOperadoras(newPage)
}
</script>

<template>
  <h2>Operadoras</h2>

  <p v-if="store.loading">Carregando...</p>
  <p v-if="store.error">{{ store.error }}</p>

  <OperadorasTable
    v-if="!store.loading"
    :operadoras="store.lista"
    :page="store.page"
    :totalPages="store.totalPages"
    @page-change="changePage"
  />
</template>
