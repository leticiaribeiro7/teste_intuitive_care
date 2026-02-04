<template>
  <div>
    <table v-if="operadoras.length">
      <thead>
        <tr>
          <th>Razão Social</th>
          <th>CNPJ</th>
          <th>UF</th>
          <th>Ações</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="op in operadoras" :key="op.cnpj">
          <td>{{ op.razao_social }}</td>
          <td>{{ op.cnpj }}</td>
          <td>{{ op.uf }}</td>
          <td>
            <router-link :to="`/operadoras/${op.cnpj}/despesas`">
              Detalhes
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Nenhuma operadora encontrada.</p>

    <!-- PAGINAÇÃO -->
    <div v-if="totalPages > 1" style="margin-top: 16px">
      <button
        :disabled="page === 1"
        @click="$emit('page-change', page - 1)"
      >
        Anterior
      </button>

      <span style="margin: 0 8px">
        Página {{ page }} de {{ totalPages }}
      </span>

      <button
        :disabled="page === totalPages"
        @click="$emit('page-change', page + 1)"
      >
        Próxima
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  operadoras: {
    type: Array,
    default: () => []
  },
  page: Number,
  totalPages: Number
})
</script>
