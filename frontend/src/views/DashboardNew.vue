<template>
  <div class="min-h-screen bg-[#0a0a0a]">
    <!-- Header -->
    <header class="bg-[#252525] border-b border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-white">Parle</h1>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-gray-400">{{ user?.email }}</span>
            <button
              @click="handleLogout"
              class="px-4 py-2 text-gray-300 hover:text-white transition-colors"
            >
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-white mb-2">Tableau de bord</h2>
        <p class="text-gray-400">Bienvenue sur votre plateforme d'apprentissage</p>
      </div>

      <!-- Language Selection -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
          <h3 class="text-2xl font-bold text-white mb-2">🇬🇧 English</h3>
          <p class="text-gray-400">Perfectionnez votre anglais de B2 à C2</p>
        </div>

        <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
          <h3 class="text-2xl font-bold text-white mb-2">🇫🇷 Français</h3>
          <p class="text-gray-400">Améliorez votre maîtrise du français</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <router-link
          to="/flashcards"
          class="bg-[#252525] rounded-lg p-4 border border-gray-800 text-center hover:border-[#3b82f6] transition-colors"
        >
          <div class="text-3xl mb-2">📚</div>
          <h4 class="text-white font-medium">Flashcards</h4>
        </router-link>

        <router-link
          to="/practice"
          class="bg-[#252525] rounded-lg p-4 border border-gray-800 text-center hover:border-[#3b82f6] transition-colors"
        >
          <div class="text-3xl mb-2">🎤</div>
          <h4 class="text-white font-medium">Practice</h4>
        </router-link>

        <router-link
          to="/schedule"
          class="bg-[#252525] rounded-lg p-4 border border-gray-800 text-center hover:border-[#3b82f6] transition-colors"
        >
          <div class="text-3xl mb-2">📅</div>
          <h4 class="text-white font-medium">Planning</h4>
        </router-link>

        <router-link
          to="/journal"
          class="bg-[#252525] rounded-lg p-4 border border-gray-800 text-center hover:border-[#3b82f6] transition-colors"
        >
          <div class="text-3xl mb-2">📝</div>
          <h4 class="text-white font-medium">Journal</h4>
        </router-link>

        <router-link
          to="/progress"
          class="bg-[#252525] rounded-lg p-4 border border-gray-800 text-center hover:border-[#3b82f6] transition-colors"
        >
          <div class="text-3xl mb-2">📊</div>
          <h4 class="text-white font-medium">Progrès</h4>
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  if (!user.value) {
    await authStore.fetchUser()
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
