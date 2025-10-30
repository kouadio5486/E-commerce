<template>
  <div>
    <h2>Mon Panier</h2>
    <div v-if="items.length === 0">Votre panier est vide.</div>
    <ul>
      <li v-for="item in items" :key="item.id" class="card">
        <span>Article #{{ item.id }} • Produit #{{ item.product }}</span>
        <span>Quantité: {{ item.quantity }}</span>
        <button @click="cart.removeFromCart(item.id)">Supprimer</button>
      </li>
    </ul>
    <button v-if="items.length" @click="cart.checkout()">Passer la commande</button>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, computed } from 'vue'
import { useCartStore } from '../stores/cart'

const cart = useCartStore()

onMounted(() => {
  cart.fetchCart()
})

const items = computed(() => cart.items)
</script>

<style scoped>
.card { display: flex; gap: .5rem; align-items: center; margin: .5rem 0; }
</style>