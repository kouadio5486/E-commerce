<template>
  <div>
    <h2>Mes Favoris</h2>
    <div v-if="favorites.length === 0">Aucun favori pour le moment.</div>
    <ul>
      <li v-for="f in favorites" :key="f.id" class="card">
        <span>{{ f.product?.name || `Produit #${f.product}` }}</span>
        <button @click="fav.removeFavorite(f.id)">Retirer</button>
      </li>
    </ul>
  </div>
  </template>

<script lang="ts" setup>
import { onMounted, computed } from 'vue'
import { useFavoriteStore } from '../stores/favorites'

const fav = useFavoriteStore()

onMounted(() => {
  fav.fetchFavorites()
})

const favorites = computed(() => fav.favorites)
</script>

<style scoped>
.card { display: flex; gap: .5rem; align-items: center; margin: .5rem 0; }
</style>