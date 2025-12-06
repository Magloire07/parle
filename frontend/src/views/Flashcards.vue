<template>
  <div class="min-h-screen bg-[#0a0a0a] font-sans relative">
    <!-- Background Watermark -->
    <BackgroundWatermark />

    <!-- Header -->
    <header class="bg-[#252525]/80 backdrop-blur-md border-b border-gray-800 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-4">
            <router-link to="/dashboard" class="flex items-center gap-1 text-gray-400 hover:text-white transition-colors">
              <ArrowLeftIcon class="w-4 h-4" />
              <span>Retour</span>
            </router-link>
            <h1 class="text-2xl font-bold text-white">Flashcards</h1>
          </div>
          <button
            @click="showCreateModal = true"
            class="flex items-center gap-2 px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg transition-colors"
          >
            <PlusIcon class="w-5 h-5" />
            <span>Nouvelle Carte</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Filters -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 relative z-10">
      <div class="bg-[#252525]/90 backdrop-blur-sm rounded-lg p-4 mb-6 border border-gray-800 shadow-xl">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Langue</label>
            <select
              v-model="filters.language"
              @change="loadFlashcards"
              class="w-full px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-colors"
            >
              <option value="">Toutes</option>
              <option value="en">Anglais</option>
              <option value="fr">Français</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm text-gray-400 mb-2">Catégorie</label>
            <select
              v-model="filters.category"
              @change="loadFlashcards"
              class="w-full px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-colors"
            >
              <option value="">Toutes</option>
              <option value="vocabulary">Vocabulaire</option>
              <option value="grammar">Grammaire</option>
              <option value="expression">Expression</option>
            </select>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Statut</label>
            <select
              v-model="filters.due"
              @change="loadFlashcards"
              class="w-full px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-colors"
            >
              <option :value="false">Toutes</option>
              <option value="true">À réviser</option>
            </select>
          </div>

          <div class="flex items-end">
            <button
              @click="startReview"
              :disabled="flashcards.length === 0"
              class="flex items-center justify-center gap-2 w-full px-4 py-2 bg-[#8b5cf6] hover:bg-[#7c3aed] disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
            >
              <PlayCircleIcon class="w-5 h-5" />
              <span>Commencer Révision</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Flashcards Grid -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        <div class="mt-2 text-gray-400">Chargement...</div>
      </div>

      <div v-else-if="flashcards.length === 0" class="text-center py-12 relative z-10">
        <div class="text-gray-400 mb-4">Aucune flashcard trouvée</div>
        <button
          @click="showCreateModal = true"
          class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg"
        >
          Créer votre première carte
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
        <div
          v-for="(card, index) in flashcards"
          :key="card.id"
          class="group bg-[#252525]/90 backdrop-blur-sm rounded-xl p-6 border border-gray-800 hover:border-gray-600 transition-all duration-300 relative hover:shadow-lg hover:shadow-black/50"
        >
          <!-- Card Number Badge -->
          <div class="absolute top-4 left-4 w-8 h-8 bg-[#3b82f6]/20 text-[#3b82f6] border border-[#3b82f6]/30 rounded-full flex items-center justify-center font-bold text-sm">
            {{ index + 1 }}
          </div>

          <div class="flex justify-between items-start mb-6 pl-10">
            <span class="px-3 py-1 bg-[#1a1a1a] text-xs font-medium rounded-full text-gray-400 border border-gray-800">
              {{ card.language === 'en' ? '🇬🇧' : '🇫🇷' }} {{ getCategoryLabel(card.category) }}
            </span>
            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click.stop="editCard(card)"
                class="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                title="Modifier"
              >
                <PencilIcon class="w-5 h-5" />
              </button>
              <button
                @click.stop="deleteCard(card.id)"
                class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                title="Supprimer"
              >
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </div>

          <div class="mb-6 cursor-pointer" @click="viewCard(card)">
            <div class="text-white font-medium text-lg min-h-[4rem] flex items-center">{{ card.front }}</div>
          </div>

          <div class="flex flex-wrap gap-2 mb-6">
            <span
              v-for="tag in card.tags"
              :key="tag"
              class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-500 border border-gray-800"
            >
              #{{ tag }}
            </span>
          </div>

          <div class="pt-4 border-t border-gray-800/50">
            <div class="flex justify-between items-center text-xs text-gray-500">
              <span class="flex items-center gap-1.5">
                <ChartBarIcon class="w-4 h-4" />
                Révisée {{ card.review_count }} fois
              </span>
              <span class="flex items-center gap-1.5">
                <CalendarIcon class="w-4 h-4" />
                {{ formatDate(card.next_review) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-[#252525] rounded-xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-800 shadow-2xl">
        <h3 class="text-2xl font-bold text-white mb-6">
          {{ editingCard ? 'Modifier' : 'Nouvelle' }} Flashcard
        </h3>

        <form @submit.prevent="saveCard" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-400 mb-2">Langue *</label>
              <select
                v-model="form.language"
                required
                class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
              >
                <option value="en">🇬🇧 Anglais</option>
                <option value="fr">🇫🇷 Français</option>
              </select>
            </div>

            <div>
              <label class="block text-sm text-gray-400 mb-2">Catégorie *</label>
              <select
                v-model="form.category"
                required
                class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
              >
                <option value="vocabulary">Vocabulaire</option>
                <option value="grammar">Grammaire</option>
                <option value="expression">Expression</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Recto (Question) *</label>
            <textarea
              v-model="form.front"
              required
              rows="3"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
              placeholder="Ex: What does 'serendipity' mean?"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Verso (Réponse) *</label>
            <textarea
              v-model="form.back"
              required
              rows="3"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
              placeholder="Ex: The occurrence of events by chance in a happy way"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Tags (séparés par des virgules)</label>
            <input
              v-model="tagsInput"
              type="text"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
              placeholder="Ex: advanced, C2, formal"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20">{{ error }}</div>

          <div class="flex gap-4 pt-4 border-t border-gray-800 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg transition-colors border border-gray-700"
            >
              Annuler
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg transition-colors font-medium"
            >
              {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Review Modal -->
    <div
      v-if="reviewMode && currentReviewCard"
      class="fixed inset-0 bg-black/95 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
    >
      <div class="max-w-2xl w-full">
        <div class="flex justify-between items-center mb-6">
          <div class="text-gray-400">
            Carte {{ currentReviewIndex + 1 }} / {{ reviewCards.length }}
          </div>
          <button @click="endReview" class="text-gray-400 hover:text-white">
            <span class="text-2xl">&times;</span>
          </button>
        </div>

        <div
          class="flashcard-container cursor-pointer mb-8"
          @click="flipCard"
        >
          <div 
            class="flashcard"
            :class="{ 'flipped': showAnswer }"
          >
            <!-- Front Face -->
            <div class="flashcard-face flashcard-front border border-white/10 shadow-2xl">
              <div class="text-xs font-bold tracking-wider text-blue-400 mb-8 uppercase">Question</div>
              <div class="text-3xl font-serif text-white text-center">{{ currentReviewCard.front }}</div>
              <div class="mt-8 text-sm text-gray-500">Cliquez pour voir la réponse</div>
            </div>
            <!-- Back Face -->
            <div class="flashcard-face flashcard-back border border-white/10 shadow-2xl bg-[#1e1e1e]">
              <div class="text-xs font-bold tracking-wider text-green-400 mb-8 uppercase">Réponse</div>
              <div class="text-3xl font-serif text-white text-center mb-6">{{ currentReviewCard.back }}</div>
              <div class="text-base text-gray-400">{{ currentReviewCard.front }}</div>
            </div>
          </div>
        </div>

        <div v-if="showAnswer" class="grid grid-cols-3 gap-4">
          <button
            @click.stop="rateCard(1)"
            class="group flex flex-col items-center justify-center py-4 bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 hover:border-500 text-red-500 rounded-xl transition-all"
          >
            <span class="text-2xl mb-1">❌</span>
            <span class="font-medium">Difficile</span>
          </button>
          <button
            @click.stop="rateCard(3)"
            class="group flex flex-col items-center justify-center py-4 bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/20 hover:border-yellow-500 text-yellow-500 rounded-xl transition-all"
          >
            <span class="text-2xl mb-1">🤔</span>
            <span class="font-medium">Moyen</span>
          </button>
          <button
            @click.stop="rateCard(5)"
            class="group flex flex-col items-center justify-center py-4 bg-green-500/10 hover:bg-green-500/20 border border-green-500/20 hover:border-green-500 text-green-500 rounded-xl transition-all"
          >
            <span class="text-2xl mb-1">✅</span>
            <span class="font-medium">Facile</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Confirm Delete Dialog -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="Supprimer la flashcard"
      message="Êtes-vous sûr de vouloir supprimer cette flashcard ? Cette action est irréversible."
      confirm-text="Supprimer"
      cancel-text="Annuler"
      @confirm="confirmDelete"
    />

    <!-- Error Alert Dialog -->
    <AlertDialog
      v-model="showErrorAlert"
      title="Erreur"
      type="error"
      :message="errorMessage"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { flashcardsAPI } from '@/services/parle-api'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import AlertDialog from '@/components/AlertDialog.vue'
import BackgroundWatermark from '@/components/BackgroundWatermark.vue'
import { 
  PencilIcon, 
  TrashIcon, 
  ChartBarIcon, 
  CalendarIcon,
  PlayCircleIcon,
  ArrowLeftIcon,
  PlusIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const flashcards = ref([])
const loading = ref(false)
const showCreateModal = ref(false)
const editingCard = ref(null)
const saving = ref(false)
const error = ref('')

// Dialogs
const showDeleteConfirm = ref(false)
const cardToDelete = ref(null)
const showErrorAlert = ref(false)
const errorMessage = ref('')

const filters = ref({
  language: '',
  category: '',
  due: false
})

const form = ref({
  language: 'en',
  category: 'vocabulary',
  front: '',
  back: '',
  tags: []
})

const tagsInput = ref('')

// Review mode
const reviewMode = ref(false)
const reviewCards = ref([])
const currentReviewIndex = ref(0)
const currentReviewCard = ref(null)
const showAnswer = ref(false)

onMounted(() => {
  loadFlashcards()
})

const loadFlashcards = async () => {
  loading.value = true
  try {
    // Nettoyer les paramètres vides
    const params = {}
    if (filters.value.language) params.language = filters.value.language
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.due === true || filters.value.due === 'true') params.due = true
    
    const response = await flashcardsAPI.getAll(params)
    flashcards.value = response.data
  } catch (err) {
    console.error('Error loading flashcards:', err)
  } finally {
    loading.value = false
  }
}

const saveCard = async () => {
  saving.value = true
  error.value = ''
  
  try {
    // Parse tags
    form.value.tags = tagsInput.value
      .split(',')
      .map(t => t.trim())
      .filter(t => t)

    if (editingCard.value) {
      await flashcardsAPI.update(editingCard.value.id, form.value)
    } else {
      await flashcardsAPI.create(form.value)
    }

    closeModal()
    loadFlashcards()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la sauvegarde'
  } finally {
    saving.value = false
  }
}

const editCard = (card) => {
  editingCard.value = card
  form.value = {
    language: card.language,
    category: card.category,
    front: card.front,
    back: card.back,
    tags: [...card.tags]
  }
  tagsInput.value = card.tags.join(', ')
  showCreateModal.value = true
}

const deleteCard = (id) => {
  cardToDelete.value = id
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  try {
    await flashcardsAPI.delete(cardToDelete.value)
    loadFlashcards()
  } catch (err) {
    console.error('Error deleting card:', err)
  } finally {
    cardToDelete.value = null
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingCard.value = null
  form.value = {
    language: 'en',
    category: 'vocabulary',
    front: '',
    back: '',
    tags: []
  }
  tagsInput.value = ''
  error.value = ''
}

const startReview = () => {
  reviewCards.value = [...flashcards.value]
  if (reviewCards.value.length === 0) return
  
  currentReviewIndex.value = 0
  currentReviewCard.value = reviewCards.value[0]
  showAnswer.value = false
  reviewMode.value = true
}

const flipCard = () => {
  showAnswer.value = !showAnswer.value
}

const rateCard = async (quality) => {
  console.log('Rating card with quality:', quality)
  try {
    await flashcardsAPI.review(currentReviewCard.value.id, { quality })
    console.log('Card rated successfully')
    
    // Next card
    if (currentReviewIndex.value < reviewCards.value.length - 1) {
      currentReviewIndex.value++
      currentReviewCard.value = reviewCards.value[currentReviewIndex.value]
      showAnswer.value = false
      console.log('Moving to next card:', currentReviewIndex.value)
    } else {
      console.log('Review complete')
      endReview()
    }
  } catch (err) {
    console.error('Error rating card:', err)
    errorMessage.value = 'Erreur lors de la notation: ' + (err.response?.data?.detail || err.message)
    showErrorAlert.value = true
  }
}

const endReview = () => {
  reviewMode.value = false
  reviewCards.value = []
  currentReviewIndex.value = 0
  currentReviewCard.value = null
  loadFlashcards()
}

const getCategoryLabel = (category) => {
  const labels = {
    vocabulary: 'Vocabulaire',
    grammar: 'Grammaire',
    expression: 'Expression'
  }
  return labels[category] || category
}

const formatDate = (dateString) => {
  if (!dateString) return 'Maintenant'
  const date = new Date(dateString)
  const now = new Date()
  if (date <= now) return 'Maintenant'
  return date.toLocaleDateString('fr-FR')
}

const viewCard = (card) => {
  // Could open a detail view
  console.log('View card:', card)
}
</script>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}

.rotate-y-180 {
  transform: rotateY(180deg);
}
</style>
