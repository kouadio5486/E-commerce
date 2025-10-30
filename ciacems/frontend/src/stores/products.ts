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
      const { data } = await api.get('products/')
      this.products = data
    },
  },
})