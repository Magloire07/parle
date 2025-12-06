<template>
  <div class="min-h-screen bg-[#0a0a0a] relative">
    <BackgroundWatermark />
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

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
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
          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-gray-800 shadow-lg">
            <BookOpenIcon class="w-8 h-8 mb-2 text-blue-500" />
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_flashcards || 0 }}</div>
            <div class="text-sm text-gray-400">Flashcards créées</div>
          </div>

          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-gray-800 shadow-lg">
            <CheckCircleIcon class="w-8 h-8 mb-2 text-green-500" />
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_reviews || 0 }}</div>
            <div class="text-sm text-gray-400">Révisions effectuées</div>
          </div>

          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-gray-800 shadow-lg">
            <MicrophoneIcon class="w-8 h-8 mb-2 text-[#5a189a]" />
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_recordings || 0 }}</div>
            <div class="text-sm text-gray-400">Enregistrements audio</div>
          </div>

          <div class="bg-[#1a1a1a] rounded-lg p-6 border border-gray-800 shadow-lg">
            <PencilSquareIcon class="w-8 h-8 mb-2 text-orange-500" />
            <div class="text-3xl font-bold text-white mb-1">{{ stats.total_journal_entries || 0 }}</div>
            <div class="text-sm text-gray-400">Entrées de journal</div>
          </div>
        </div>

        <!-- Study Time -->
        <div class="bg-[#1a1a1a] rounded-lg p-6 mb-8 border border-gray-800 shadow-lg">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <ClockIcon class="w-6 h-6 text-blue-500" />
            Temps d'étude
          </h3>
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

        <!-- Progression Chart -->
        <div class="bg-[#1a1a1a] rounded-lg p-6 mb-8 border border-gray-800 shadow-lg">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <ChartBarIcon class="w-6 h-6 text-green-500" />
            Évolution des Flashcards par Catégorie
          </h3>
          <div v-if="stats.progression_data && Object.keys(stats.progression_data).length > 0" class="h-80">
            <Line :data="chartData" :options="chartOptions" />
          </div>
          <div v-else class="text-center py-12 text-gray-400">
            Créez des flashcards pour voir votre progression
          </div>
        </div>

        <!-- Flashcards Stats -->
        <div class="bg-[#1a1a1a] rounded-lg p-6 mb-8 border border-gray-800 shadow-lg">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <ChartPieIcon class="w-6 h-6 text-indigo-500" />
            Répartition des Flashcards
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                <div v-if="!stats.flashcards_by_category || Object.keys(stats.flashcards_by_category).length === 0" class="text-gray-500 text-sm">
                  Aucune flashcard pour le moment
                </div>
              </div>
            </div>

            <div>
              <div class="text-sm text-gray-400 mb-2">Blocs de planning</div>
              <div class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-white">Total</span>
                  <span class="px-2 py-1 bg-[#1a1a1a] rounded text-gray-400">{{ stats.total_schedule_blocks || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-white">Complétés</span>
                  <span class="px-2 py-1 bg-green-600 rounded text-white">{{ stats.completed_schedule_blocks || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-[#1a1a1a] rounded-lg p-6 mb-8 border border-gray-800 shadow-lg">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <PresentationChartLineIcon class="w-6 h-6 text-purple-500" />
            Résumé
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div class="text-sm text-gray-400 mb-2">Enregistrements audio</div>
              <div class="text-2xl font-bold text-white">{{ formatSeconds(stats.total_recording_time_seconds) }}</div>
              <div class="text-sm text-gray-500">Temps total d'enregistrement</div>
            </div>
            <div>
              <div class="text-sm text-gray-400 mb-2">Planning</div>
              <div class="text-2xl font-bold text-white">
                {{ stats.completed_schedule_blocks || 0 }} / {{ stats.total_schedule_blocks || 0 }}
              </div>
              <div class="text-sm text-gray-500">Blocs complétés</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { progressAPI } from '@/services/parle-api'
import BackgroundWatermark from '@/components/BackgroundWatermark.vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import {
  BookOpenIcon,
  CheckCircleIcon,
  MicrophoneIcon,
  PencilSquareIcon,
  ClockIcon,
  ChartBarIcon,
  ChartPieIcon,
  PresentationChartLineIcon
} from '@heroicons/vue/24/outline'

// Enregistrer les composants Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const stats = ref({})
const loading = ref(false)
const dateRange = ref('month')
const selectedLanguage = ref('')
const recentActivity = ref([])

onMounted(() => {
  loadStats()
})

// Configuration du graphique
const chartData = computed(() => {
  if (!stats.value.progression_data) return null
  
  const progressionData = stats.value.progression_data
  const categories = Object.keys(progressionData)
  
  if (categories.length === 0) return null
  
  const labels = progressionData[categories[0]]?.dates || []
  
  const datasets = categories.map((category, index) => {
    const colors = {
      vocabulary: { border: 'rgb(59, 130, 246)', bg: 'rgba(59, 130, 246, 0.1)' },
      grammar: { border: 'rgb(139, 92, 246)', bg: 'rgba(139, 92, 246, 0.1)' },
      expression: { border: 'rgb(34, 197, 94)', bg: 'rgba(34, 197, 94, 0.1)' }
    }
    
    const categoryLabels = {
      vocabulary: 'Vocabulaire',
      grammar: 'Grammaire',
      expression: 'Expression'
    }
    
    return {
      label: categoryLabels[category] || category,
      data: progressionData[category].counts,
      borderColor: colors[category]?.border || 'rgb(156, 163, 175)',
      backgroundColor: colors[category]?.bg || 'rgba(156, 163, 175, 0.1)',
      borderWidth: 2,
      tension: 0.4,
      fill: true,
      pointRadius: 4,
      pointHoverRadius: 6
    }
  })
  
  return {
    labels: labels.map(date => {
      const d = new Date(date)
      return d.toLocaleDateString('fr-FR', { month: 'short', day: 'numeric' })
    }),
    datasets
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: 'rgb(156, 163, 175)',
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(37, 37, 37, 0.9)',
      titleColor: 'rgb(255, 255, 255)',
      bodyColor: 'rgb(209, 213, 219)',
      borderColor: 'rgb(75, 85, 99)',
      borderWidth: 1
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(75, 85, 99, 0.2)'
      },
      ticks: {
        color: 'rgb(156, 163, 175)'
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(75, 85, 99, 0.2)'
      },
      ticks: {
        color: 'rgb(156, 163, 175)',
        stepSize: 1
      }
    }
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false
  }
}

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

const formatSeconds = (seconds) => {
  if (!seconds) return '0min'
  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  if (hours > 0) return `${hours}h${mins}min`
  if (mins > 0) return `${mins}min${secs}s`
  return `${secs}s`
}

const calculateAverage = () => {
  if (!stats.value.study_days || !stats.value.total_study_time_minutes) return '0'
  const avgMinutes = stats.value.total_study_time_minutes / stats.value.study_days
  return (avgMinutes / 60).toFixed(1)
}
</script>
