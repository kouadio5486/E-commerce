<template>
  <div>
    <h2>Nos Produits</h2>
    <div v-for="p in products" :key="p.id" class="card">
      <h3>{{ p.name }}</h3>
      <p>{{ p.description }}</p>
      <p>{{ p.price }} €</p>
      <button @click="cart.addToCart(p.id)">Ajouter au panier</button>
      <button @click="fav.addFavorite(p.id)">❤️ Favori</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import { useProductStore } from '../stores/products'
import { useCartStore } from '../stores/cart'
import { useFavoriteStore } from '../stores/favorites'

const productsStore = useProductStore()
const cart = useCartStore()
const fav = useFavoriteStore()

onMounted(() => {
  productsStore.fetchProducts()
})

const products = productsStore.products
</script>