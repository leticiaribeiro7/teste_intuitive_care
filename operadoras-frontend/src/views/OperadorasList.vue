<template>
<input v-model="search" placeholder="Buscar razão social ou CNPJ" />


<OperadorasTable :operadoras="store.lista" />


<DespesasChart :chartData="chartData" />
</template>


<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useOperadorasStore } from '../stores/operadorasStore'
import OperadorasTable from '../components/OperadorasTable.vue'
import DespesasChart from '../components/DespesasChart.vue'


const store = useOperadorasStore()
const search = ref('')


onMounted(() => {
store.fetchOperadoras({ page: 1 })
store.fetchDespesasUF()
})


watch(search, (value) => {
store.fetchOperadoras({ search: value, page: 1 })
})


const chartData = computed(() => ({
labels: store.despesasUF.map(d => d.uf),
datasets: [{
label: 'Despesas por UF',
data: store.despesasUF.map(d => d.total)
}]
}))
</script>