import { defineStore } from 'pinia'

import api from '../api/axios'

interface User {
    id: number
    username: string
    email: string
}

export const useAuthStore = defineStore('auth',{
    state: () => ({
    user: null as User | null,
    access: localStorage.getItem('access'),
    refresh: localStorage.getItem('refresh'),
}),
actions: {
    async register(username: string, email: string, password: string) {
      await api.post('users/register/', { username, email, password })
    },

    async login(username: string, password: string) {
      const { data } = await api.post('users/login/', { username, password })
      this.access = data.access
      this.refresh = data.refresh
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
    },

    async logout() {
      await api.post('users/logout/', { refresh: this.refresh })
      this.access = null
      this.refresh = null
      this.user = null
      localStorage.clear()
    },
  },
})