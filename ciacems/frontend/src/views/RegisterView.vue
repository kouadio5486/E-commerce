<template>
  <div class="register">
    <h2>Inscription</h2>
    <form @submit.prevent="register">
      <input v-model="email" placeholder="Email" type="email" required />
      <input v-model="first_name" placeholder="Prénom" required />
      <input v-model="last_name" placeholder="Nom" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">S'inscrire</button>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const first_name = ref('')
const last_name = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const register = async () => {
  try {
    await auth.register(email.value, first_name.value, last_name.value, password.value)
    router.push('/login')
  } catch (error) {
    alert('Erreur lors de l\'inscription')
  }
}
</script>

<style scoped>
.register { max-width: 360px; }
form { display: flex; flex-direction: column; gap: .5rem; }
</style>