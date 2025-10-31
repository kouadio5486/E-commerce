<template>
   <div class="cart-container">
    <h2>Mon Panier</h2>
    <div v-if="items.length === 0" class="empty-message">
      Votre panier est vide.
    </div>
    <table v-else class="cart-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Produit</th>
          <th>Quantité</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.product_detail?.name || ('#' + item.product) }}</td>
          <td>{{ item.quantity }}</td>
          <td>
            <button @click="cart.removeFromCart(item.id)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button v-if="items.length" class="checkout-button" @click="cart.checkout()">Passer la commande</button>
    <div v-if="cart.notice" class="checkout-notice" :class="cart.notice.type">
      {{ cart.notice.text }}
    </div>



  </div>
</template>

<script lang="ts" setup>
import { onMounted, computed } from 'vue'
import { useCartStore } from '../stores/cart'
import '../assets/style/carts.css'



const cart = useCartStore()

onMounted(() => {
  cart.fetchCart()
})

const items = computed(() => cart.items)
const insufficientItems = computed(() => {
  // Bloque si product_detail est manquant (stock inconnu) ou insuffisant
  return items.value
    .filter((i: any) => !i.product_detail || i.quantity > i.product_detail.stock)
    .map((i: any) => (i.product_detail ? i.product_detail.name : `#${i.product}`))
})
</script>

