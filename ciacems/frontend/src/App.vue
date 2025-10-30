<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const isLogged = computed(() => !!auth.access)

const handleLogout = async () => {
  try {
    await auth.logout()
  } catch (e) {
    alert('Erreur lors de la déconnexion')
  }
}
</script>

<template>
  <header class="nav">
    <nav>
      <router-link to="/products">Produits</router-link>
      <router-link to="/favorites">Favoris</router-link>
      <router-link to="/cart">Panier</router-link>
      <span class="spacer" />
      <router-link v-if="!isLogged" to="/login">Connexion</router-link>
      <router-link v-if="!isLogged" to="/register">Inscription</router-link>
      <button v-if="isLogged" @click="handleLogout">Se déconnecter</button>
    </nav>
  </header>

  <main>
    <router-view />
  </main>
</template>

<style scoped>
.nav {
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 1rem;
}
nav {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 1rem;
}
.spacer {
  flex: 1;
}
main {
  padding: 1rem;
}
</style>
