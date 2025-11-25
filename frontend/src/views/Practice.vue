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
            <h1 class="text-2xl font-bold text-white">Practice - Enregistrements Audio</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Language Selection -->
      <div class="mb-6">
        <label class="block text-sm text-gray-400 mb-2">Langue</label>
        <select
          v-model="selectedLanguage"
          @change="loadRecordings"
          class="px-4 py-2 bg-[#252525] border border-gray-700 rounded-lg text-white"
        >
          <option value="">Toutes</option>
          <option value="en">🇬🇧 Anglais</option>
          <option value="fr">🇫🇷 Français</option>
        </select>
      </div>

      <!-- Audio Recorder -->
      <div class="bg-[#252525] rounded-lg p-8 mb-8 border border-gray-800">
        <h2 class="text-xl font-bold text-white mb-6">Nouvel enregistrement</h2>
        
        <div class="text-center">
          <div v-if="!recording && !audioBlob" class="mb-6">
            <button
              @click="startRecording"
              class="w-32 h-32 rounded-full bg-red-600 hover:bg-red-700 transition-colors flex items-center justify-center mx-auto"
            >
              <span class="text-4xl">🎤</span>
            </button>
            <p class="text-gray-400 mt-4">Cliquez pour commencer</p>
          </div>

          <div v-if="recording" class="mb-6">
            <button
              @click="stopRecording"
              class="w-32 h-32 rounded-full bg-red-600 animate-pulse transition-colors flex items-center justify-center mx-auto"
            >
              <span class="text-4xl">⏸️</span>
            </button>
            <p class="text-white mt-4">Enregistrement... {{ recordingTime }}s</p>
          </div>

          <div v-if="audioBlob && !recording" class="space-y-4">
            <audio
              ref="audioPlayer"
              :src="audioUrl"
              controls
              class="w-full"
            ></audio>

            <div class="grid grid-cols-2 gap-4">
              <button
                @click="saveRecording"
                :disabled="saving"
                class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg"
              >
                {{ saving ? 'Sauvegarde...' : '💾 Sauvegarder' }}
              </button>
              <button
                @click="discardRecording"
                class="px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg"
              >
                🗑️ Recommencer
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Recordings List -->
      <div class="space-y-4">
        <h2 class="text-xl font-bold text-white mb-4">Mes enregistrements</h2>

        <div v-if="loading" class="text-center py-8 text-gray-400">
          Chargement...
        </div>

        <div v-else-if="recordings.length === 0" class="text-center py-8 text-gray-400">
          Aucun enregistrement pour le moment
        </div>

        <div
          v-for="recording in recordings"
          :key="recording.id"
          class="bg-[#252525] rounded-lg p-6 border border-gray-800"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <span class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-400">
                {{ recording.language === 'en' ? '🇬🇧 Anglais' : '🇫🇷 Français' }}
              </span>
              <div class="text-sm text-gray-500 mt-2">
                {{ formatDate(recording.created_at) }}
              </div>
            </div>
            <button
              @click="deleteRecording(recording.id)"
              class="text-gray-400 hover:text-red-500"
            >
              🗑️
            </button>
          </div>

          <audio
            :src="`http://localhost:8000${recording.audio_url}`"
            controls
            class="w-full mb-4"
          ></audio>

          <div v-if="recording.transcript" class="mt-4 p-4 bg-[#1a1a1a] rounded-lg">
            <div class="text-sm text-gray-400 mb-2">Transcription:</div>
            <div class="text-white">{{ recording.transcript }}</div>
          </div>

          <div v-if="recording.notes" class="mt-4 text-gray-400 text-sm">
            Notes: {{ recording.notes }}
          </div>

          <div v-if="recording.words_practiced && recording.words_practiced.length > 0" class="mt-4">
            <div class="text-sm text-gray-400 mb-2">Mots pratiqués:</div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="word in recording.words_practiced"
                :key="word"
                class="px-2 py-1 bg-[#1a1a1a] text-xs rounded text-gray-300"
              >
                {{ word }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { recordingsAPI } from '@/services/parle-api'

const selectedLanguage = ref('en')
const recordings = ref([])
const loading = ref(false)
const saving = ref(false)

// Recording state
const recording = ref(false)
const audioBlob = ref(null)
const audioUrl = ref(null)
const recordingTime = ref(0)
let mediaRecorder = null
let recordingInterval = null
let audioChunks = []

onMounted(() => {
  loadRecordings()
})

onUnmounted(() => {
  if (recordingInterval) {
    clearInterval(recordingInterval)
  }
})

const loadRecordings = async () => {
  loading.value = true
  try {
    const params = selectedLanguage.value ? { language: selectedLanguage.value } : {}
    const response = await recordingsAPI.getAll(params)
    recordings.value = response.data
  } catch (err) {
    console.error('Error loading recordings:', err)
  } finally {
    loading.value = false
  }
}

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      audioBlob.value = blob
      audioUrl.value = URL.createObjectURL(blob)
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.start()
    recording.value = true
    recordingTime.value = 0

    recordingInterval = setInterval(() => {
      recordingTime.value++
    }, 1000)
  } catch (err) {
    console.error('Error starting recording:', err)
    alert('Erreur: Impossible d\'accéder au microphone')
  }
}

const stopRecording = () => {
  if (mediaRecorder && recording.value) {
    mediaRecorder.stop()
    recording.value = false
    if (recordingInterval) {
      clearInterval(recordingInterval)
    }
  }
}

const saveRecording = async () => {
  if (!audioBlob.value) return

  saving.value = true
  try {
    const formData = new FormData()
    formData.append('file', audioBlob.value, 'recording.webm')
    formData.append('language', selectedLanguage.value)
    
    await recordingsAPI.upload(formData)
    
    discardRecording()
    loadRecordings()
  } catch (err) {
    console.error('Error saving recording:', err)
    alert('Erreur lors de la sauvegarde')
  } finally {
    saving.value = false
  }
}

const discardRecording = () => {
  audioBlob.value = null
  if (audioUrl.value) {
    URL.revokeObjectURL(audioUrl.value)
  }
  audioUrl.value = null
  recordingTime.value = 0
}

const deleteRecording = async (id) => {
  if (!confirm('Supprimer cet enregistrement ?')) return

  try {
    await recordingsAPI.delete(id)
    loadRecordings()
  } catch (err) {
    console.error('Error deleting recording:', err)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
