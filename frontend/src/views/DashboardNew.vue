<template>
  <div class="min-h-screen bg-[#0a0a0a] font-sans relative">
    <!-- Background Watermark -->
    <BackgroundWatermark />

    <!-- Header -->
    <header class="bg-[#1a1a1a]/80 backdrop-blur-md border-b border-white/5 sticky top-0 z-50 relative">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-2">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#5a189a] to-[#d4af37] flex items-center justify-center shadow-lg shadow-[#5a189a]/30 group hover:scale-105 transition-transform duration-300">
              <MicrophoneIconSolid class="w-6 h-6 text-white" />
            </div>
            <h1 class="text-xl font-bold text-white tracking-tight">Parle</h1>
          </div>
          <div class="flex items-center gap-6">
            <span class="text-gray-400 text-sm font-medium">{{ user?.email }}</span>
            <button
              @click="handleLogout"
              class="flex items-center gap-2 px-4 py-2 rounded-full border border-red-500/20 text-red-400 hover:text-red-300 hover:bg-red-500/10 hover:border-red-500/30 transition-all duration-200 text-sm font-medium"
            >
              <ArrowRightOnRectangleIcon class="w-4 h-4" />
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 relative z-10">
      <div class="mb-12">
        <h2 class="text-4xl font-bold text-white mb-3 tracking-tight">Tableau de bord</h2>
        <p class="text-gray-400 text-lg">Bienvenue sur votre plateforme d'apprentissage</p>
      </div>

      <!-- Language Selection -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <!-- English Card -->
        <div class="group relative bg-[#1a1a1a]/90 backdrop-blur-sm rounded-2xl p-8 border border-white/5 hover:border-blue-500/30 transition-all duration-300 overflow-hidden shadow-2xl">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative z-10">
            <div class="flex justify-between items-start mb-6">
              <div class="p-3 rounded-xl bg-blue-500/20 text-blue-400 group-hover:bg-blue-500 group-hover:text-white transition-colors duration-300">
                <span class="text-4xl">🇬🇧</span>
              </div>
              <ArrowUpRightIcon class="w-6 h-6 text-gray-500 group-hover:text-blue-400 transition-colors" />
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">English</h3>
            <p class="text-gray-400 mb-6">Perfectionnez votre anglais de B2 à C2 avec des exercices ciblés.</p>
            <div class="flex items-center gap-2 text-sm font-medium text-blue-400">
              <span>Continuer</span>
              <ArrowLongRightIcon class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>

        <!-- French Card -->
        <div class="group relative bg-[#1a1a1a]/90 backdrop-blur-sm rounded-2xl p-8 border border-white/5 hover:border-purple-500/30 transition-all duration-300 overflow-hidden shadow-2xl">
          <div class="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative z-10">
            <div class="flex justify-between items-start mb-6">
              <div class="p-3 rounded-xl bg-purple-500/20 text-purple-400 group-hover:bg-purple-500 group-hover:text-white transition-colors duration-300">
                <span class="text-4xl">🇫🇷</span>
              </div>
              <ArrowUpRightIcon class="w-6 h-6 text-gray-500 group-hover:text-purple-400 transition-colors" />
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Français</h3>
            <p class="text-gray-400 mb-6">Améliorez votre maîtrise du français vers l'excellence.</p>
            <div class="flex items-center gap-2 text-sm font-medium text-purple-400">
              <span>Continuer</span>
              <ArrowLongRightIcon class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions Title -->
      <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
        <SparklesIcon class="w-5 h-5 text-yellow-500" />
        Accès Rapide
      </h3>

      <!-- Quick Actions Grid -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <router-link
          v-for="action in quickActions"
          :key="action.path"
          :to="action.path"
          class="group flex flex-col items-center justify-center bg-[#1a1a1a]/90 backdrop-blur-sm rounded-xl p-6 border border-white/5 hover:bg-[#252525] hover:border-white/10 transition-all duration-200"
        >
          <div :class="`p-3 rounded-lg bg-opacity-20 mb-3 transition-transform group-hover:scale-110 ${action.colorBg} ${action.colorText}`">
            <component :is="action.icon" class="w-6 h-6" />
          </div>
          <h4 class="text-gray-300 font-medium group-hover:text-white transition-colors">{{ action.name }}</h4>
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
import BackgroundWatermark from '@/components/BackgroundWatermark.vue'
import { 
  ArrowRightOnRectangleIcon, 
  ArrowUpRightIcon, 
  ArrowLongRightIcon,
  SparklesIcon,
  RectangleStackIcon,
  MicrophoneIcon,
  CalendarIcon,
  PencilSquareIcon,
  ChartBarIcon,
  AcademicCapIcon
} from '@heroicons/vue/24/outline'
import { MicrophoneIcon as MicrophoneIconSolid } from '@heroicons/vue/24/solid'

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const quickActions = [
  { name: 'Flashcards', path: '/flashcards', icon: RectangleStackIcon, colorBg: 'bg-green-500', colorText: 'text-green-500' },
  { name: 'Pratique', path: '/practice', icon: MicrophoneIcon, colorBg: 'bg-red-500', colorText: 'text-red-500' },
  { name: 'Planning', path: '/schedule', icon: CalendarIcon, colorBg: 'bg-orange-500', colorText: 'text-orange-500' },
  { name: 'Journal', path: '/journal', icon: PencilSquareIcon, colorBg: 'bg-blue-500', colorText: 'text-blue-500' },
  { name: 'Progrès', path: '/progress', icon: ChartBarIcon, colorBg: 'bg-indigo-500', colorText: 'text-indigo-500' },
  { name: 'Quiz', path: '/quiz', icon: AcademicCapIcon, colorBg: 'bg-yellow-500', colorText: 'text-yellow-500' },
]

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
