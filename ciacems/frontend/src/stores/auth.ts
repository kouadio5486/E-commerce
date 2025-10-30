import { defineStore } from 'pinia'
import api from '../api/axios'
import authApi from '../api/auth'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    access: localStorage.getItem('access'),
    refresh: localStorage.getItem('refresh'),
  }),

  actions: {
    async register(email: string, first_name: string, last_name: string, password: string) {
      await authApi.post('register/', { email, first_name, last_name, password })
    },

    async login(email: string, password: string) {
      const { data } = await authApi.post('login/', { email, password })
      this.access = data.access
      this.refresh = data.refresh
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
    },

    async logout() {
      try {
        if (this.refresh) {
          await authApi.post('logout/', { refresh: this.refresh })
        }
      } catch (e) {
        // Ignorer les erreurs (401/400) et nettoyer l'état côté client
      } finally {
        this.access = null
        this.refresh = null
        this.user = null
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
      }
    },
  },
})