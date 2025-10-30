<template>
  <div class="login">
    <h2>Connexion</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Nom d’utilisateur" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">Se connecter</button>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const login = async () => {
  try {
    await auth.login(username.value, password.value)
    router.push('/products')
  } catch (error) {
    alert('Erreur de connexion')
  }
}
</script>