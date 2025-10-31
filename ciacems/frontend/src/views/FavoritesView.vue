<template>
   <div class="favorites-container">
    <h2>Mes Favoris</h2>
    <div v-if="favorites.length === 0" class="empty-message">
      Aucun favori pour le moment.
    </div>
    <table v-else class="favorites-table">
      <thead>
        <tr>
          <th>Produit</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="f in favorites" :key="f.id">
          <td>{{ f.product_detail?.name || `Produit #${f.product}` }}</td>
          <td>
            <button @click="fav.removeFavorite(f.id)">Retirer</button>
          </td>
        </tr>
      </tbody>
    </table>
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
.favorites-container {
  padding: 2rem;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.empty-message {
  text-align: center;
  color: #777;
  font-style: italic;
}

.favorites-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.favorites-table th,
.favorites-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.favorites-table th {
  background-color: #f0f0f0;
  font-weight: bold;
  color: #555;
}

.favorites-table td button {
  padding: 0.4rem 0.8rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.favorites-table td button:hover {
  background-color: #c82333;
}
</style>