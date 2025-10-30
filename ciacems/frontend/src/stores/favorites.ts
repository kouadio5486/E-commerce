import { defineStore } from 'pinia'
import api from '../api/axios'

export const useFavoriteStore = defineStore('favorites', {
  state: () => ({
    favorites: [] as any[],
  }),

  actions: {
    async fetchFavorites() {
      const { data } = await api.get('favorites/')
      this.favorites = data
    },

    async addFavorite(productId: number) {
      await api.post('favorites/', { product: productId })
      this.fetchFavorites()
    },

    async removeFavorite(favoriteId: number) {
      await api.delete(`favorites/${favoriteId}/`)
      this.fetchFavorites()
    },
  },
})