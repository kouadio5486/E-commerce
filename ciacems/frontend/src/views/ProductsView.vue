<template>
  <div class="product-table-container">
    <h2>Nos Produits</h2>
    <table class="product-table">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Description</th>
          <th>Prix</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in products" :key="p.id">
          <td>{{ p.name }}</td>
          <td>{{ p.description }}</td>
          <td>{{ p.price }} €</td>
          <td>
            <button @click="cart.addToCart(p.id)">Ajouter au panier</button>
            <button @click="fav.addFavorite(p.id)">❤️ Favori</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import { useProductStore } from '../stores/products'
import { useCartStore } from '../stores/cart'
import { useFavoriteStore } from '../stores/favorites'
import '../assets/style/products.css'



const productsStore = useProductStore()
const cart = useCartStore()
const fav = useFavoriteStore()

onMounted(() => {
  productsStore.fetchProducts()
})

const products = productsStore.products
</script>

