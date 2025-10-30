import { defineStore } from 'pinia'
import api from '../api/axios'

export interface Product {
  id: number
  name: string
  description: string
  price: number
  stock: number
}

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [] as Product[],
  }),

  actions: {
    async fetchProducts() {
      try {
        const { data } = await api.get('products/')
        this.products = data
      } catch (error: any) {
        const status = error?.response?.status
        if (status === 401) {
          // Token invalide/expiré: nettoyer et réessayer en public
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
          const { data } = await api.get('products/')
          this.products = data
        } else {
          throw error
        }
      }
    },
  },
})