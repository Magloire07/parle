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
            <h1 class="text-2xl font-bold text-white">Flashcards</h1>
          </div>
          <button
            @click="showCreateModal = true"
            class="px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg transition-colors"
          >
            + Nouvelle Carte
          </button>
        </div>
      </div>
    </header>

    <!-- Filters -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-[#252525] rounded-lg p-4 mb-6 border border-gray-800">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Langue</label>
            <select
              v-model="filters.language"
              @change="loadFlashcards"
              class="w-full px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
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
              class="w-full px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
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
              class="w-full px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
            >
              <option :value="false">Toutes</option>
              <option value="true">À réviser</option>
            </select>
          </div>

          <div class="flex items-end">
            <button
              @click="startReview"
              :disabled="flashcards.length === 0"
              class="w-full px-4 py-2 bg-[#8b5cf6] hover:bg-[#7c3aed] disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              🎯 Commencer Révision
            </button>
          </div>
        </div>
      </div>

      <!-- Flashcards Grid -->
      <div v-if="loading" class="text-center py-12">
        <div class="text-gray-400">Chargement...</div>
      </div>

      <div v-else-if="flashcards.length === 0" class="text-center py-12">
        <div class="text-gray-400 mb-4">Aucune flashcard trouvée</div>
        <button
          @click="showCreateModal = true"
          class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg"
        >
          Créer votre première carte
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="card in flashcards"
          :key="card.id"
          class="bg-[#252525] rounded-lg p-6 border border-gray-800 hover:border-gray-700 transition-colors cursor-pointer"
          @click="viewCard(card)"
        >
          <div class="flex justify-between items-start mb-4">
            <span class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-400">
              {{ card.language === 'en' ? '🇬🇧' : '🇫🇷' }} {{ getCategoryLabel(card.category) }}
            </span>
            <div class="flex gap-2">
              <button
                @click.stop="editCard(card)"
                class="text-gray-400 hover:text-white"
              >
                ✏️
              </button>
              <button
                @click.stop="deleteCard(card.id)"
                class="text-gray-400 hover:text-red-500"
              >
                🗑️
              </button>
            </div>
          </div>

          <div class="mb-4">
            <div class="text-white font-medium mb-2">{{ card.front }}</div>
            <div class="text-gray-400 text-sm">{{ card.back }}</div>
          </div>

          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in card.tags"
              :key="tag"
              class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-500"
            >
              #{{ tag }}
            </span>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-800 text-xs text-gray-500">
            Prochaine révision: {{ formatDate(card.next_review) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-[#252525] rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <h3 class="text-2xl font-bold text-white mb-6">
          {{ editingCard ? 'Modifier' : 'Nouvelle' }} Flashcard
        </h3>

        <form @submit.prevent="saveCard" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Langue *</label>
            <select
              v-model="form.language"
              required
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
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
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
            >
              <option value="vocabulary">Vocabulaire</option>
              <option value="grammar">Grammaire</option>
              <option value="expression">Expression</option>
            </select>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Recto (Question) *</label>
            <textarea
              v-model="form.front"
              required
              rows="3"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Ex: What does 'serendipity' mean?"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Verso (Réponse) *</label>
            <textarea
              v-model="form.back"
              required
              rows="3"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Ex: The occurrence of events by chance in a happy way"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Tags (séparés par des virgules)</label>
            <input
              v-model="tagsInput"
              type="text"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Ex: advanced, C2, formal"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

          <div class="flex gap-4 pt-4">
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg transition-colors"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Review Modal -->
    <div
      v-if="reviewMode && currentReviewCard"
      class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-4"
    >
      <div class="max-w-2xl w-full">
        <div class="text-center mb-4 text-gray-400">
          Carte {{ currentReviewIndex + 1 }} / {{ reviewCards.length }}
        </div>

        <div
          class="bg-[#252525] rounded-lg p-12 cursor-pointer perspective-1000"
          @click="flipCard"
        >
          <div :class="{ 'rotate-y-180': showAnswer }" class="transition-transform duration-500">
            <div v-if="!showAnswer" class="text-center">
              <div class="text-sm text-gray-400 mb-4">QUESTION</div>
              <div class="text-2xl text-white">{{ currentReviewCard.front }}</div>
            </div>
            <div v-else class="text-center">
              <div class="text-sm text-gray-400 mb-4">RÉPONSE</div>
              <div class="text-2xl text-white mb-4">{{ currentReviewCard.back }}</div>
              <div class="text-sm text-gray-500">{{ currentReviewCard.front }}</div>
            </div>
          </div>
        </div>

        <div v-if="showAnswer" class="grid grid-cols-3 gap-4 mt-6">
          <button
            @click="rateCard(1)"
            class="px-6 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg"
          >
            ❌ Difficile
          </button>
          <button
            @click="rateCard(3)"
            class="px-6 py-4 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg"
          >
            🤔 Moyen
          </button>
          <button
            @click="rateCard(5)"
            class="px-6 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg"
          >
            ✅ Facile
          </button>
        </div>

        <button
          @click="endReview"
          class="mt-6 w-full px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg"
        >
          Terminer la révision
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { flashcardsAPI } from '@/services/parle-api'

const router = useRouter()
const flashcards = ref([])
const loading = ref(false)
const showCreateModal = ref(false)
const editingCard = ref(null)
const saving = ref(false)
const error = ref('')

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

const deleteCard = async (id) => {
  if (!confirm('Supprimer cette flashcard ?')) return
  
  try {
    await flashcardsAPI.delete(id)
    loadFlashcards()
  } catch (err) {
    console.error('Error deleting card:', err)
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
  try {
    await flashcardsAPI.review(currentReviewCard.value.id, { quality })
    
    // Next card
    if (currentReviewIndex.value < reviewCards.value.length - 1) {
      currentReviewIndex.value++
      currentReviewCard.value = reviewCards.value[currentReviewIndex.value]
      showAnswer.value = false
    } else {
      endReview()
    }
  } catch (err) {
    console.error('Error rating card:', err)
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
