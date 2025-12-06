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
            <h1 class="text-2xl font-bold text-white">Quiz & Évaluations</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
      <div class="mb-8 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">Testez vos connaissances</h2>
        <p class="text-gray-400 max-w-2xl mx-auto">
          Sélectionnez une catégorie pour commencer un quiz et évaluer votre progression.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Mock Categories -->
        <div 
          v-for="cat in categories" 
          :key="cat.id"
          class="bg-[#1a1a1a] rounded-xl p-6 border border-gray-800 hover:border-[#5a189a] transition-all duration-300 group cursor-pointer shadow-lg hover:shadow-[#5a189a]/20"
        >
          <div :class="`w-12 h-12 rounded-lg ${cat.bg} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`">
            <component :is="cat.icon" :class="`w-6 h-6 ${cat.text}`" />
          </div>
          <h3 class="text-xl font-bold text-white mb-2">{{ cat.title }}</h3>
          <p class="text-gray-400 text-sm mb-4">{{ cat.description }}</p>
          <div class="flex items-center justify-between">
            <span class="text-xs font-mono text-gray-500">{{ cat.count }} questions</span>
            <button class="px-4 py-2 bg-[#5a189a] hover:bg-[#7b2cbf] text-white text-sm rounded-lg transition-colors">
              Commencer
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BackgroundWatermark from '@/components/BackgroundWatermark.vue'
import {
  ChatBubbleBottomCenterTextIcon,
  BookOpenIcon,
  SpeakerWaveIcon,
  LanguageIcon,
  PuzzlePieceIcon,
  AcademicCapIcon
} from '@heroicons/vue/24/outline'

const categories = ref([
  {
    id: 1,
    title: 'Vocabulaire Essentiel',
    description: 'Testez votre maîtrise des mots les plus courants.',
    icon: BookOpenIcon,
    bg: 'bg-blue-500/20',
    text: 'text-blue-500',
    count: 20
  },
  {
    id: 2,
    title: 'Grammaire & Conjugaison',
    description: 'Exercez-vous sur les temps et la structure des phrases.',
    icon: PuzzlePieceIcon,
    bg: 'bg-green-500/20',
    text: 'text-green-500',
    count: 15
  },
  {
    id: 3,
    title: 'Compréhension Orale',
    description: 'Écoutez des extraits et répondez aux questions.',
    icon: SpeakerWaveIcon,
    bg: 'bg-purple-500/20',
    text: 'text-purple-500',
    count: 10
  },
  {
    id: 4,
    title: 'Expressions Idiomatiques',
    description: 'Apprenez les expressions natives pour sonner plus naturel.',
    icon: ChatBubbleBottomCenterTextIcon,
    bg: 'bg-orange-500/20',
    text: 'text-orange-500',
    count: 12
  },
  {
    id: 5,
    title: 'Culture & Civilisation',
    description: 'Découvrez la culture liée à la langue cible.',
    icon: GlobeEuropeAfricaIcon,
    bg: 'bg-indigo-500/20',
    text: 'text-indigo-500',
    count: 10
  },
  {
    id: 6,
    title: 'Test de Niveau Global',
    description: 'Évaluation complète de toutes vos compétences.',
    icon: AcademicCapIcon,
    bg: 'bg-red-500/20',
    text: 'text-red-500',
    count: 50
  }
])

// Import for the 5th item specifically (not in the initial list above)
import { GlobeEuropeAfricaIcon } from '@heroicons/vue/24/outline'
</script>
