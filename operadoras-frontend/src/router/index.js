import { createRouter, createWebHistory } from 'vue-router'
import OperadorasList from '../views/OperadorasList.vue'
import OperadoraDetalhe from '../views/OperadoraDetalhe.vue'


const routes = [
{ path: '/', component: OperadorasList },
{ path: '/operadoras/:cnpj/despesas', component: OperadoraDetalhe }
]


export default createRouter({
history: createWebHistory(),
routes
})