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
            <h1 class="text-2xl font-bold text-white">Journal d'Apprentissage</h1>
          </div>
          <button
            @click="createNewEntry"
            class="px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg transition-colors"
          >
            + Nouvelle Entrée
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Filters -->
      <div class="mb-6 flex gap-4">
        <select
          v-model="filterLanguage"
          @change="loadEntries"
          class="px-4 py-2 bg-[#252525] border border-gray-700 rounded-lg text-white"
        >
          <option value="">Toutes les langues</option>
          <option value="en">🇬🇧 Anglais</option>
          <option value="fr">🇫🇷 Français</option>
        </select>
      </div>

      <!-- Editor (when creating/editing) -->
      <div v-if="editing" class="bg-[#252525] rounded-lg p-6 mb-6 border border-gray-800">
        <form @submit.prevent="saveEntry" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Langue</label>
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
            <label class="block text-sm text-gray-400 mb-2">Titre *</label>
            <input
              v-model="form.title"
              required
              type="text"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Titre de votre entrée..."
            />
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Contenu *</label>
            <textarea
              v-model="form.content"
              required
              rows="10"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white font-mono"
              placeholder="Décrivez ce que vous avez appris aujourd'hui, vos difficultés, vos progrès..."
            ></textarea>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Mots clés (séparés par des virgules)</label>
            <input
              v-model="tagsInput"
              type="text"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Ex: conditionals, subjunctive, pronunciation"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

          <div class="flex gap-4">
            <button
              type="submit"
              :disabled="saving"
              class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg"
            >
              {{ saving ? 'Sauvegarde...' : '💾 Sauvegarder' }}
            </button>
            <button
              type="button"
              @click="cancelEdit"
              class="px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>

      <!-- Entries List -->
      <div v-if="loading" class="text-center py-12 text-gray-400">
        Chargement...
      </div>

      <div v-else-if="entries.length === 0 && !editing" class="text-center py-12">
        <div class="text-gray-400 mb-4">Aucune entrée de journal</div>
        <button
          @click="createNewEntry"
          class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg"
        >
          Créer votre première entrée
        </button>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="entry in entries"
          :key="entry.id"
          class="bg-[#252525] rounded-lg p-6 border border-gray-800 hover:border-gray-700 transition-colors"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-xl font-bold text-white mb-2">{{ entry.title }}</h3>
              <div class="flex items-center gap-4 text-sm text-gray-400">
                <span>{{ entry.language === 'en' ? '🇬🇧 Anglais' : '🇫🇷 Français' }}</span>
                <span>{{ formatDate(entry.created_at) }}</span>
              </div>
            </div>
            <div class="flex gap-2">
              <button
                @click="editEntry(entry)"
                class="text-gray-400 hover:text-white"
              >
                ✏️
              </button>
              <button
                @click="deleteEntry(entry.id)"
                class="text-gray-400 hover:text-red-500"
              >
                🗑️
              </button>
            </div>
          </div>

          <div class="text-gray-300 whitespace-pre-wrap mb-4">
            {{ truncateContent(entry.content) }}
          </div>

          <div v-if="entry.tags && entry.tags.length > 0" class="flex flex-wrap gap-2">
            <span
              v-for="tag in entry.tags"
              :key="tag"
              class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-400"
            >
              #{{ tag }}
            </span>
          </div>

          <button
            v-if="entry.content.length > 300"
            @click="viewFullEntry(entry)"
            class="mt-4 text-[#3b82f6] hover:text-[#2563eb] text-sm"
          >
            Lire la suite →
          </button>
        </div>
      </div>
    </div>

    <!-- Full Entry Modal -->
    <div
      v-if="viewingEntry"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
      @click.self="viewingEntry = null"
    >
      <div class="bg-[#252525] rounded-lg p-6 max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-2xl font-bold text-white">{{ viewingEntry.title }}</h2>
          <button
            @click="viewingEntry = null"
            class="text-gray-400 hover:text-white"
          >
            ✕
          </button>
        </div>

        <div class="text-sm text-gray-400 mb-6">
          {{ formatDate(viewingEntry.created_at) }} • {{ viewingEntry.language === 'en' ? '🇬🇧 Anglais' : '🇫🇷 Français' }}
        </div>

        <div class="text-gray-300 whitespace-pre-wrap mb-6">
          {{ viewingEntry.content }}
        </div>

        <div v-if="viewingEntry.tags && viewingEntry.tags.length > 0" class="flex flex-wrap gap-2">
          <span
            v-for="tag in viewingEntry.tags"
            :key="tag"
            class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-400"
          >
            #{{ tag }}
          </span>
        </div>
      </div>
    </div>

    <!-- Confirm Delete Dialog -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="Supprimer l'entrée"
      message="Êtes-vous sûr de vouloir supprimer cette entrée de journal ? Cette action est irréversible."
      confirm-text="Supprimer"
      cancel-text="Annuler"
      @confirm="confirmDeleteEntry"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { journalAPI } from '@/services/parle-api'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const entries = ref([])
const loading = ref(false)
const editing = ref(false)

// Dialogs
const showDeleteConfirm = ref(false)
const entryToDelete = ref(null)
const editingEntry = ref(null)
const viewingEntry = ref(null)
const saving = ref(false)
const error = ref('')
const filterLanguage = ref('')

const form = ref({
  language: 'en',
  title: '',
  content: '',
  tags: []
})

const tagsInput = ref('')

onMounted(() => {
  loadEntries()
})

const loadEntries = async () => {
  loading.value = true
  try {
    const params = filterLanguage.value ? { language: filterLanguage.value } : {}
    const response = await journalAPI.getAll(params)
    entries.value = response.data
  } catch (err) {
    console.error('Error loading entries:', err)
  } finally {
    loading.value = false
  }
}

const createNewEntry = () => {
  editing.value = true
  editingEntry.value = null
  form.value = {
    language: filterLanguage.value || 'en',
    title: '',
    content: '',
    tags: []
  }
  tagsInput.value = ''
}

const editEntry = (entry) => {
  editing.value = true
  editingEntry.value = entry
  form.value = {
    language: entry.language,
    title: entry.title,
    content: entry.content,
    tags: [...(entry.tags || [])]
  }
  tagsInput.value = entry.tags?.join(', ') || ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const saveEntry = async () => {
  saving.value = true
  error.value = ''
  
  try {
    // Parse tags
    form.value.tags = tagsInput.value
      .split(',')
      .map(t => t.trim())
      .filter(t => t)

    if (editingEntry.value) {
      await journalAPI.update(editingEntry.value.id, form.value)
    } else {
      await journalAPI.create(form.value)
    }

    editing.value = false
    editingEntry.value = null
    loadEntries()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la sauvegarde'
  } finally {
    saving.value = false
  }
}

const deleteEntry = (id) => {
  entryToDelete.value = id
  showDeleteConfirm.value = true
}

const confirmDeleteEntry = async () => {
  try {
    await journalAPI.delete(entryToDelete.value)
    loadEntries()
  } catch (err) {
    console.error('Error deleting entry:', err)
  } finally {
    entryToDelete.value = null
  }
}

const cancelEdit = () => {
  editing.value = false
  editingEntry.value = null
  form.value = {
    language: 'en',
    title: '',
    content: '',
    tags: []
  }
  tagsInput.value = ''
  error.value = ''
}

const viewFullEntry = (entry) => {
  viewingEntry.value = entry
}

const truncateContent = (content) => {
  if (content.length <= 300) return content
  return content.substring(0, 300) + '...'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
