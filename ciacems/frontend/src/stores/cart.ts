import { defineStore } from 'pinia'
import api from '../api/axios'

interface CartItem {
  id: number
  product: number
  quantity: number
}

// Durée en ms avant disparition du message
const MESSAGE_TIMEOUT = 1000 // 1 seconde
type NoticeType = 'success' | 'error'
interface Notice { type: NoticeType; text: string }
// items contient tous les articles du panier pour l’utilisateur connecté.
export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
    notice: null as Notice | null,
  }),
//Récupère les articles du panier depuis l’API et les stocke dans items.
  actions: {
    async fetchCart() {
      const { data } = await api.get('carts/')
      this.items = data
    },
    clearNotice() {
      this.notice = null
    },
// Envoie une requête POST à l’API pour ajouter un produit au panier.
    async addToCart(productId: number, quantity = 1) {
      await api.post('carts/', { product: productId, quantity })
      //Recharge ensuite le panier avec fetchCart().
      this.fetchCart()
    },
//Supprime un article du panier via l’API, puis recharge le panier.
    async removeFromCart(itemId: number) {
      await api.delete(`carts/${itemId}/`)
      this.fetchCart()
    },
 //Envoie une commande à l’API pour valider l’achat.
    async checkout() {
      try {
        const { data } = await api.post('orders/create/')
        this.notice = { type: 'success', text: data.message }
        this.items = []
        // Effacer le message de succès après 1 seconde
        setTimeout(() => this.clearNotice(), MESSAGE_TIMEOUT)
      } catch (error: any) {
        const status = error?.response?.status
        const payload = error?.response?.data || {}
        if (status === 400) {
          const msg = payload.error || payload.detail || 'Commande invalide'
          this.notice = { type: 'error', text: msg }
          // Effacer le message d'erreur après 1 seconde
          setTimeout(() => this.clearNotice(), MESSAGE_TIMEOUT)
          return
        }
        if (status === 401) {
          this.notice = { type: 'error', text: 'Veuillez vous connecter pour passer la commande' }
          // Effacer le message d'erreur après 1 seconde
          setTimeout(() => this.clearNotice(), MESSAGE_TIMEOUT)
          return
        }
        console.error('Checkout error:', error)
        this.notice = { type: 'error', text: 'Une erreur est survenue, réessayez plus tard' }
        // Effacer le message d'erreur après 1 seconde
        setTimeout(() => this.clearNotice(), MESSAGE_TIMEOUT)
      }
    },
    
  },
})