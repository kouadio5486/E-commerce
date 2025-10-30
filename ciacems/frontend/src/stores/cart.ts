import { defineStore } from 'pinia'
import api from '../api/axios'

interface CartItem {
  id: number
  product: number
  quantity: number
}
// items contient tous les articles du panier pour l’utilisateur connecté.
export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),
//Récupère les articles du panier depuis l’API et les stocke dans items.
  actions: {
    async fetchCart() {
      const { data } = await api.get('cart/')
      this.items = data
    },
// Envoie une requête POST à l’API pour ajouter un produit au panier.
    async addToCart(productId: number, quantity = 1) {
      await api.post('cart/', { product: productId, quantity })
      //Recharge ensuite le panier avec fetchCart().
      this.fetchCart()
    },
//Supprime un article du panier via l’API, puis recharge le panier.
    async removeFromCart(itemId: number) {
      await api.delete(`cart/${itemId}/`)
      this.fetchCart()
    },
 //Envoie une commande à l’API pour valider l’achat.
    async checkout() {
      const { data } = await api.post('orders/create/')
      alert(`✅ ${data.message}`)
      this.items = []
    },
  },
})