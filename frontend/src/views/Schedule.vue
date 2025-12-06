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
            <h1 class="text-2xl font-bold text-white">Planning Hebdomadaire</h1>
          </div>
          <button
            @click="showCreateModal = true"
            class="px-4 py-2 bg-[#5a189a] hover:bg-[#7b2cbf] text-white rounded-lg transition-colors shadow-lg shadow-[#5a189a]/20"
          >
            + Ajouter un bloc
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
      <!-- Week Selector -->
      <div class="flex items-center justify-between mb-6">
        <button
          @click="previousWeek"
          class="px-4 py-2 bg-[#252525] hover:bg-[#2a2a2a] border border-gray-800 text-white rounded-lg"
        >
          ← Semaine précédente
        </button>
        <div class="text-white font-medium">
          Semaine du {{ formatWeekStart() }}
        </div>
        <button
          @click="nextWeek"
          class="px-4 py-2 bg-[#252525] hover:bg-[#2a2a2a] border border-gray-800 text-white rounded-lg"
        >
          Semaine suivante →
        </button>
      </div>

      <!-- Calendar Grid -->
      <div class="bg-[#1a1a1a] rounded-lg overflow-hidden border border-gray-800 shadow-xl">
        <div class="grid grid-cols-8 border-b border-gray-800">
          <div class="p-4"></div>
          <div
            v-for="day in weekDays"
            :key="day.date"
            class="p-4 text-center border-l border-gray-800"
            :class="{ 'bg-[#1a1a1a]': isToday(day.date) }"
          >
            <div class="text-sm text-gray-400">{{ day.name }}</div>
            <div class="text-white font-medium">{{ day.dateStr }}</div>
          </div>
        </div>

        <div v-for="hour in hours" :key="hour" class="grid grid-cols-8 border-b border-gray-800">
          <div class="p-4 text-sm text-gray-400 border-r border-gray-800">
            {{ hour }}:00
          </div>
          <div
            v-for="day in weekDays"
            :key="`${day.date}-${hour}`"
            class="p-2 border-l border-gray-800 min-h-[80px] relative hover:bg-[#1a1a1a] cursor-pointer"
            @click="selectTimeSlot(day.date, hour)"
          >
              <div
                v-for="block in getBlocksForSlot(day.date, hour)"
                :key="block.id"
                class="p-2 rounded bg-[#5a189a] text-white text-xs mb-1 cursor-pointer hover:bg-[#7b2cbf] shadow-sm"
                @click.stop="editBlock(block)"
              >
              <div class="font-medium">{{ block.activity_name }}</div>
              <div class="text-[10px] opacity-75">
                {{ formatTime(block.start_time) }} - {{ block.duration }}min
              </div>
            </div>
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
      <div class="bg-[#252525] rounded-lg p-6 max-w-lg w-full">
        <h3 class="text-2xl font-bold text-white mb-6">
          {{ editingBlock ? 'Modifier' : 'Nouveau' }} bloc de planning
        </h3>

        <form @submit.prevent="saveBlock" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Nom de l'activité *</label>
            <input
              v-model="form.activity_name"
              required
              type="text"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Ex: Session Flashcards Anglais"
            />
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Jour *</label>
            <select
              v-model.number="form.day_of_week"
              required
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
            >
              <option :value="0">Lundi</option>
              <option :value="1">Mardi</option>
              <option :value="2">Mercredi</option>
              <option :value="3">Jeudi</option>
              <option :value="4">Vendredi</option>
              <option :value="5">Samedi</option>
              <option :value="6">Dimanche</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-400 mb-2">Heure début *</label>
              <input
                v-model="form.start_time"
                required
                type="time"
                class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              />
            </div>
            <div>
              <label class="block text-sm text-gray-400 mb-2">Durée (min) *</label>
              <input
                v-model.number="form.duration"
                required
                type="number"
                min="0"
                class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Type d'activité *</label>
            <select
              v-model="form.activity_type"
              required
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
            >
              <option value="anki">📚 Flashcards (Anki)</option>
              <option value="speaking">🎤 Speaking Practice</option>
              <option value="reading">📖 Lecture</option>
              <option value="writing">✍️ Écriture</option>
              <option value="listening">👂 Écoute</option>
            </select>
          </div>

          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

          <div class="flex gap-4 pt-4">
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 px-6 py-3 bg-[#5a189a] hover:bg-[#7b2cbf] disabled:bg-gray-600 text-white rounded-lg shadow-lg shadow-[#5a189a]/20"
            >
              {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
            <button
              v-if="editingBlock"
              type="button"
              @click="deleteBlock"
              class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg"
            >
              Supprimer
            </button>
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirm Delete Dialog -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="Supprimer le bloc"
      message="Êtes-vous sûr de vouloir supprimer ce bloc de planning ? Cette action est irréversible."
      confirm-text="Supprimer"
      cancel-text="Annuler"
      @confirm="confirmDeleteBlock"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { scheduleAPI } from '@/services/parle-api'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import BackgroundWatermark from '@/components/BackgroundWatermark.vue'

const currentWeekStart = ref(new Date())
const scheduleBlocks = ref([])
const showCreateModal = ref(false)
const editingBlock = ref(null)

// Dialogs
const showDeleteConfirm = ref(false)
const blockToDelete = ref(null)
const saving = ref(false)
const error = ref('')

const form = ref({
  day_of_week: 0,
  start_time: '',
  duration: 60,
  activity_type: 'reading',
  activity_name: ''
})

const hours = Array.from({ length: 24 }, (_, i) => i)

const weekDays = computed(() => {
  const days = []
  const start = new Date(currentWeekStart.value)
  start.setDate(start.getDate() - start.getDay() + 1) // Start from Monday
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(start)
    date.setDate(start.getDate() + i)
    days.push({
      name: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'][i],
      date: date,
      dateStr: date.getDate()
    })
  }
  return days
})

onMounted(() => {
  loadSchedule()
})

const loadSchedule = async () => {
  try {
    const response = await scheduleAPI.getAll()
    scheduleBlocks.value = response.data
  } catch (err) {
    console.error('Error loading schedule:', err)
  }
}

const getBlocksForSlot = (date, hour) => {
  // Calculer day_of_week (0=Lundi, 6=Dimanche)
  const dayOfWeek = (date.getDay() + 6) % 7
  return scheduleBlocks.value.filter(block => {
    const blockHour = parseInt(block.start_time.split(':')[0])
    return block.day_of_week === dayOfWeek && blockHour === hour
  })
}

const selectTimeSlot = (date, hour) => {
  // Calculer day_of_week (0=Lundi, 6=Dimanche)
  const dayOfWeek = (date.getDay() + 6) % 7
  form.value.day_of_week = dayOfWeek
  form.value.start_time = `${hour.toString().padStart(2, '0')}:00`
  form.value.duration = 60
  form.value.activity_name = ''
  showCreateModal.value = true
}

const saveBlock = async () => {
  saving.value = true
  error.value = ''
  
  try {
    if (editingBlock.value) {
      await scheduleAPI.update(editingBlock.value.id, form.value)
    } else {
      await scheduleAPI.create(form.value)
    }
    
    closeModal()
    loadSchedule()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la sauvegarde'
  } finally {
    saving.value = false
  }
}

const editBlock = (block) => {
  editingBlock.value = block
  form.value = {
    day_of_week: block.day_of_week,
    start_time: block.start_time,
    duration: block.duration,
    activity_type: block.activity_type,
    activity_name: block.activity_name
  }
  showCreateModal.value = true
}

const deleteBlock = () => {
  blockToDelete.value = editingBlock.value.id
  showDeleteConfirm.value = true
}

const confirmDeleteBlock = async () => {
  try {
    await scheduleAPI.delete(blockToDelete.value)
    closeModal()
    loadSchedule()
  } catch (err) {
    console.error('Error deleting block:', err)
  } finally {
    blockToDelete.value = null
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingBlock.value = null
  form.value = {
    day_of_week: 0,
    start_time: '',
    duration: 60,
    activity_type: 'reading',
    activity_name: ''
  }
  error.value = ''
}

const previousWeek = () => {
  const newDate = new Date(currentWeekStart.value)
  newDate.setDate(newDate.getDate() - 7)
  currentWeekStart.value = newDate
}

const nextWeek = () => {
  const newDate = new Date(currentWeekStart.value)
  newDate.setDate(newDate.getDate() + 7)
  currentWeekStart.value = newDate
}

const formatWeekStart = () => {
  const start = new Date(currentWeekStart.value)
  start.setDate(start.getDate() - start.getDay() + 1)
  return start.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const formatDateForAPI = (date) => {
  return date.toISOString().split('T')[0]
}

const formatTime = (timeStr) => {
  return timeStr.substring(0, 5)
}

const isToday = (date) => {
  const today = new Date()
  return date.toDateString() === today.toDateString()
}
</script>
