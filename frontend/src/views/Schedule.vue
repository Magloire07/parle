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
            <h1 class="text-2xl font-bold text-white">Planning Hebdomadaire</h1>
          </div>
          <button
            @click="showCreateModal = true"
            class="px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg transition-colors"
          >
            + Ajouter un bloc
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
      <div class="bg-[#252525] rounded-lg overflow-hidden border border-gray-800">
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
              class="p-2 rounded bg-[#3b82f6] text-white text-xs mb-1 cursor-pointer hover:bg-[#2563eb]"
              @click.stop="editBlock(block)"
            >
              <div class="font-medium">{{ block.title }}</div>
              <div class="text-[10px] opacity-75">
                {{ formatTime(block.start_time) }} - {{ formatTime(block.end_time) }}
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
            <label class="block text-sm text-gray-400 mb-2">Titre *</label>
            <input
              v-model="form.title"
              required
              type="text"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Ex: Session Flashcards Anglais"
            />
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Jour *</label>
            <input
              v-model="form.day_of_week"
              required
              type="date"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
            />
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
              <label class="block text-sm text-gray-400 mb-2">Heure fin *</label>
              <input
                v-model="form.end_time"
                required
                type="time"
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
              <option value="flashcards">📚 Flashcards</option>
              <option value="practice">🎤 Practice Audio</option>
              <option value="reading">📖 Lecture</option>
              <option value="writing">✍️ Écriture</option>
              <option value="grammar">📝 Grammaire</option>
              <option value="other">➕ Autre</option>
            </select>
          </div>

          <div>
            <label class="block text-sm text-gray-400 mb-2">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
              placeholder="Détails de la session..."
            ></textarea>
          </div>

          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

          <div class="flex gap-4 pt-4">
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg"
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { scheduleAPI } from '@/services/parle-api'

const currentWeekStart = ref(new Date())
const scheduleBlocks = ref([])
const showCreateModal = ref(false)
const editingBlock = ref(null)
const saving = ref(false)
const error = ref('')

const form = ref({
  title: '',
  day_of_week: '',
  start_time: '',
  end_time: '',
  activity_type: 'flashcards',
  description: ''
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
  const dateStr = formatDateForAPI(date)
  return scheduleBlocks.value.filter(block => {
    const blockDate = block.day_of_week
    const blockHour = parseInt(block.start_time.split(':')[0])
    return blockDate === dateStr && blockHour === hour
  })
}

const selectTimeSlot = (date, hour) => {
  form.value.day_of_week = formatDateForAPI(date)
  form.value.start_time = `${hour.toString().padStart(2, '0')}:00`
  form.value.end_time = `${(hour + 1).toString().padStart(2, '0')}:00`
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
    title: block.title,
    day_of_week: block.day_of_week,
    start_time: block.start_time,
    end_time: block.end_time,
    activity_type: block.activity_type,
    description: block.description || ''
  }
  showCreateModal.value = true
}

const deleteBlock = async () => {
  if (!confirm('Supprimer ce bloc ?')) return
  
  try {
    await scheduleAPI.delete(editingBlock.value.id)
    closeModal()
    loadSchedule()
  } catch (err) {
    console.error('Error deleting block:', err)
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingBlock.value = null
  form.value = {
    title: '',
    day_of_week: '',
    start_time: '',
    end_time: '',
    activity_type: 'flashcards',
    description: ''
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
