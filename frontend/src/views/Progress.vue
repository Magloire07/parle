<template>
  <div class="min-h-screen bg-[#0a0a0a]">
    <!-- Header -->
    <header class="bg-[#252525] border-b border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-4">
            <router-link to="/dashboard" class="text-gray-400 hover:text-white">
              ← Retour
            </router-link>
            <h1 class="text-2xl font-bold text-white">Progrès & Statistiques</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Date Range Selector -->
      <div class="mb-8 flex gap-4">
        <select
          v-model="dateRange"
          @change="loadStats"
          class="px-4 py-2 bg-[#252525] border border-gray-700 rounded-lg text-white"
        >
          <option value="week">Cette semaine</option>
          <option value="month">Ce mois</option>
          <option value="3months">3 derniers mois</option>
          <option value="year">Cette année</option>
          <option value="all">Tout</option>
        </select>

        <select
          v-model="selectedLanguage"
          @change="loadStats"
          class="px-4 py-2 bg-[#252525] border border-gray-700 rounded-lg text-white"
        >
          <option value="">Toutes les langues</option>
          <option value="en">🇬🇧 Anglais</option>
          <option value="fr">🇫🇷 Français</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12 text-gray-400">
        Chargement des statistiques...
      </div>

      <!-- Stats Grid -->
      <div v-else>
        <!-- Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
            <div class="text-4xl mb-2">📚</div>
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_flashcards || 0 }}</div>
            <div class="text-sm text-gray-400">Flashcards créées</div>
          </div>

          <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
            <div class="text-4xl mb-2">🎯</div>
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_reviews || 0 }}</div>
            <div class="text-sm text-gray-400">Révisions effectuées</div>
          </div>

          <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
            <div class="text-4xl mb-2">🎤</div>
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_recordings || 0 }}</div>
            <div class="text-sm text-gray-400">Enregistrements audio</div>
          </div>

          <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
            <div class="text-4xl mb-2">📝</div>
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_journal_entries || 0 }}</div>
            <div class="text-sm text-gray-400">Entrées de journal</div>
          </div>
        </div>

        <!-- Study Time -->
        <div class="bg-[#252525] rounded-lg p-6 mb-8 border border-gray-800">
          <h3 class="text-xl font-bold text-white mb-4">⏱️ Temps d'étude</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div class="text-2xl font-bold text-white">{{ formatMinutes(stats.total_study_time_minutes) }}</div>
              <div class="text-sm text-gray-400">Temps total</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">{{ stats.study_days || 0 }}</div>
              <div class="text-sm text-gray-400">Jours d'étude</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">{{ calculateAverage() }}h/jour</div>
              <div class="text-sm text-gray-400">Moyenne quotidienne</div>
            </div>
          </div>
        </div>

        <!-- Flashcards Stats -->
        <div class="bg-[#252525] rounded-lg p-6 mb-8 border border-gray-800">
          <h3 class="text-xl font-bold text-white mb-4">📊 Répartition des Flashcards</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div class="text-sm text-gray-400 mb-2">Par catégorie</div>
              <div class="space-y-2">
                <div
                  v-for="(count, category) in stats.flashcards_by_category"
                  :key="category"
                  class="flex justify-between items-center"
                >
                  <span class="text-white">{{ getCategoryLabel(category) }}</span>
                  <span class="px-2 py-1 bg-[#1a1a1a] rounded text-gray-400">{{ count }}</span>
                </div>
              </div>
            </div>

            <div>
              <div class="text-sm text-gray-400 mb-2">Par langue</div>
              <div class="space-y-2">
                <div
                  v-for="(count, lang) in stats.flashcards_by_language"
                  :key="lang"
                  class="flex justify-between items-center"
                >
                  <span class="text-white">{{ lang === 'en' ? '🇬🇧 Anglais' : '🇫🇷 Français' }}</span>
                  <span class="px-2 py-1 bg-[#1a1a1a] rounded text-gray-400">{{ count }}</span>
                </div>
              </div>
            </div>

            <div>
              <div class="text-sm text-gray-400 mb-2">Statut révision</div>
              <div class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-white">À réviser</span>
                  <span class="px-2 py-1 bg-red-600 rounded text-white">{{ stats.due_flashcards || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-white">À jour</span>
                  <span class="px-2 py-1 bg-green-600 rounded text-white">
                    {{ (stats.total_flashcards || 0) - (stats.due_flashcards || 0) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-[#252525] rounded-lg p-6 border border-gray-800">
          <h3 class="text-xl font-bold text-white mb-4">🕐 Activité récente</h3>
          <div class="space-y-3">
            <div
              v-for="activity in recentActivity"
              :key="activity.id"
              class="flex items-center gap-4 p-3 bg-[#1a1a1a] rounded-lg"
            >
              <div class="text-2xl">{{ activity.icon }}</div>
              <div class="flex-1">
                <div class="text-white">{{ activity.title }}</div>
                <div class="text-sm text-gray-400">{{ activity.date }}</div>
              </div>
              <div class="text-gray-500">{{ activity.count }}</div>
            </div>
          </div>
        </div>

        <!-- Streak -->
        <div class="mt-8 bg-gradient-to-r from-[#3b82f6] to-[#8b5cf6] rounded-lg p-6">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-white text-lg mb-1">🔥 Série actuelle</div>
              <div class="text-white text-4xl font-bold">{{ stats.current_streak || 0 }} jours</div>
            </div>
            <div class="text-right">
              <div class="text-white text-sm opacity-75 mb-1">Record</div>
              <div class="text-white text-2xl font-bold">{{ stats.longest_streak || 0 }} jours</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { progressAPI } from '@/services/parle-api'

const stats = ref({})
const loading = ref(false)
const dateRange = ref('month')
const selectedLanguage = ref('')
const recentActivity = ref([])

onMounted(() => {
  loadStats()
})

const loadStats = async () => {
  loading.value = true
  try {
    const params = {
      period: dateRange.value
    }
    if (selectedLanguage.value) {
      params.language = selectedLanguage.value
    }

    const response = await progressAPI.getStats(params)
    stats.value = response.data

    // Mock recent activity (would come from backend)
    recentActivity.value = [
      { id: 1, icon: '📚', title: 'Révision flashcards', date: 'Aujourd\'hui', count: '15 cartes' },
      { id: 2, icon: '🎤', title: 'Enregistrement audio', date: 'Hier', count: '3 min' },
      { id: 3, icon: '📝', title: 'Entrée journal', date: 'Il y a 2 jours', count: '1 entrée' }
    ]
  } catch (err) {
    console.error('Error loading stats:', err)
  } finally {
    loading.value = false
  }
}

const getCategoryLabel = (category) => {
  const labels = {
    vocabulary: 'Vocabulaire',
    grammar: 'Grammaire',
    expression: 'Expression'
  }
  return labels[category] || category
}

const formatMinutes = (minutes) => {
  if (!minutes) return '0h'
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours === 0) return `${mins}min`
  if (mins === 0) return `${hours}h`
  return `${hours}h${mins}min`
}

const calculateAverage = () => {
  if (!stats.value.study_days || !stats.value.total_study_time_minutes) return '0'
  const avgMinutes = stats.value.total_study_time_minutes / stats.value.study_days
  return (avgMinutes / 60).toFixed(1)
}
</script>
