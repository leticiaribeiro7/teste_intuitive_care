<script setup>
import { ref, onMounted } from 'vue'
import { useOperadorasStore } from '../stores/operadorasStore'
import OperadorasTable from '../components/OperadorasTable.vue'

const store = useOperadorasStore()
const cnpj = ref('')

onMounted(() => {
  store.fetchOperadoras(1)
})

function buscar() {
  if (!cnpj.value) return
  store.buscarPorCnpj(cnpj.value)
}

function limpar() {
  cnpj.value = ''
  store.fetchOperadoras(1)
}

function changePage(newPage) {
  store.fetchOperadoras(newPage)
}
</script>

<template>
  <h2>Operadoras</h2>

  <!-- BUSCA -->
  <div style="margin-bottom: 16px">
    <input
      v-model="cnpj"
      placeholder="Digite o CNPJ"
    />

    <button @click="buscar" style="margin-left: 8px">
      OK
    </button>

    <button
      v-if="store.modoBusca"
      @click="limpar"
      style="margin-left: 8px"
    >
      Limpar
    </button>
  </div>

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
