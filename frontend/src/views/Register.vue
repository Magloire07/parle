<template>
  <div class="min-h-screen bg-[#0a0a0a] flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white mb-2">Parle</h1>
        <p class="text-gray-400">Créez votre compte</p>
      </div>

      <div class="bg-[#252525] rounded-lg p-8 shadow-xl">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#3b82f6] transition-colors"
              placeholder="votre@email.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
              Mot de passe
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              minlength="6"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#3b82f6] transition-colors"
              placeholder="••••••••"
            />
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-300 mb-2">
              Confirmer le mot de passe
            </label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#3b82f6] transition-colors"
              placeholder="••••••••"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors"
          >
            {{ loading ? 'Inscription...' : "S'inscrire" }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-gray-400">
            Déjà un compte ?
            <router-link to="/login" class="text-[#3b82f6] hover:text-[#2563eb] font-medium">
              Se connecter
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  error.value = ''
  
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Les mots de passe ne correspondent pas'
    return
  }

  if (form.value.password.length < 6) {
    error.value = 'Le mot de passe doit contenir au moins 6 caractères'
    return
  }

  loading.value = true
  
  try {
    // Envoyer seulement email et password au backend
    await authStore.register({
      email: form.value.email,
      password: form.value.password
    })
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || "Erreur lors de l'inscription"
  } finally {
    loading.value = false
  }
}
</script>
