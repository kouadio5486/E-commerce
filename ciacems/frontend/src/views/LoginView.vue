<template>
  <div class="login">
    <h2>Connexion</h2>
    <form @submit.prevent="login">
      <label for="email">Email</label>
      <input v-model="email" placeholder="Email" type="email" required />
      <label for="password">Mot de passe</label>
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">Se connecter</button>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const login = async () => {
  try {
    await auth.login(email.value, password.value)
    router.push('/products')
  } catch (error) {
    alert('Erreur de connexion')
  }
}
</script>