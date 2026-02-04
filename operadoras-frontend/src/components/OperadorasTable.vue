<template>
<div>
<table>
<thead>
<tr>
<th>Razão Social</th>
<th>CNPJ</th>
<th>UF</th>
<th>Ações</th>
</tr>
</thead>
<tbody>
<tr v-for="op in operadoras" :key="op.id">
<td>{{ op.razao_social }}</td>
<td>{{ op.cnpj }}</td>
<td>{{ op.uf }}</td>
<td>
<router-link :to="`/operadoras/${op.cnpj}/despesas`">Detalhes</router-link>
</td>
</tr>
</tbody>
</table>
</div>
</template>


<script setup>
defineProps({ operadoras: Array })
</script>