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

            <div class="text-left">
              <label class="block text-sm text-gray-400 mb-2">Commentaire (optionnel)</label>
              <textarea
                v-model="recordingNotes"
                rows="3"
                placeholder="Ajoutez un commentaire sur cet enregistrement..."
                class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 resize-none"
              ></textarea>
            </div>

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

        <div v-else-if="groupedRecordings.length === 0" class="text-center py-8 text-gray-400">
          Aucun enregistrement pour le moment
        </div>

        <!-- Recording Groups (Vertical List) -->
        <div
          v-for="group in groupedRecordings"
          :key="group.id"
          class="bg-[#252525] rounded-lg p-6 border border-gray-800"
        >
          <!-- Title from first version (v1) -->
          <div v-if="group.versions[group.versions.length - 1]?.notes" class="text-lg text-white font-semibold mb-4">
            {{ group.versions[group.versions.length - 1].notes }}
          </div>

          <!-- Horizontal Scrollable Versions List -->
          <div class="overflow-x-auto">
            <div class="flex gap-4 pb-2" style="min-width: min-content;">
              <div
                v-for="(recording, vIndex) in group.versions"
                :key="recording.id"
                class="flex-shrink-0 w-96 bg-[#1a1a1a] rounded-lg p-4 border border-gray-700"
                :class="{ 'border-blue-500': vIndex === 0 }"
              >
                <!-- Version Header with Date -->
                <div class="flex justify-between items-start mb-4">
                  <div class="flex items-center gap-2">
                    <span 
                      v-if="vIndex === 0" 
                      class="px-2 py-1 bg-blue-600 text-xs rounded text-white font-bold"
                    >
                      v{{ recording.version }}
                    </span>
                    <span 
                      v-else 
                      class="px-2 py-1 bg-gray-700 text-xs rounded text-gray-400"
                    >
                      v{{ recording.version }}
                    </span>
                    <span class="px-2 py-1 bg-[#252525] text-xs rounded text-gray-400">
                      {{ recording.language === 'en' ? '🇬🇧' : '🇫🇷' }}
                    </span>
                    <span class="text-xs text-gray-500">
                      {{ formatDate(recording.created_at) }}
                    </span>
                  </div>
                  <button
                    @click="deleteRecording(recording.id)"
                    class="text-gray-400 hover:text-red-500"
                  >
                    🗑️
                  </button>
                </div>

                <!-- Audio Player -->
                <audio
                  :src="`http://localhost:8000${recording.audio_url}`"
                  controls
                  class="w-full mb-2"
                ></audio>

                <!-- Improve Button (only for latest version) -->
                <button
                  v-if="vIndex === 0"
                  @click="openImproveModal(recording)"
                  class="w-full px-3 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg text-sm transition-colors"
                >
                  ✨ Améliorer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Delete Dialog -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="Supprimer l'enregistrement"
      message="Êtes-vous sûr de vouloir supprimer cet enregistrement ? Cette action est irréversible."
      confirm-text="Supprimer"
      cancel-text="Annuler"
      @confirm="confirmDeleteRecording"
    />

    <!-- Improve Recording Modal -->
    <div
      v-if="showImproveModal"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
      @click.self="closeImproveModal"
    >
      <div class="bg-[#252525] rounded-lg p-6 max-w-2xl w-full border border-gray-800">
        <h3 class="text-2xl font-bold text-white mb-6">
          ✨ Améliorer l'enregistrement - Version {{ (improvingRecording?.version || 0) + 1 }}
        </h3>

        <div class="text-center mb-6">
          <div v-if="!improvingAudioBlob && !recordingImprovement">
            <button
              @click="startImprovementRecording"
              class="w-32 h-32 rounded-full bg-red-600 hover:bg-red-700 transition-colors flex items-center justify-center mx-auto"
            >
              <span class="text-4xl">🎤</span>
            </button>
            <p class="text-gray-400 mt-4">Cliquez pour enregistrer la nouvelle version</p>
          </div>

          <div v-if="recordingImprovement">
            <button
              @click="stopImprovementRecording"
              class="w-32 h-32 rounded-full bg-red-600 animate-pulse transition-colors flex items-center justify-center mx-auto"
            >
              <span class="text-4xl">⏸️</span>
            </button>
            <p class="text-white mt-4">Enregistrement... {{ improvementRecordingTime }}s</p>
          </div>

          <div v-if="improvingAudioBlob && !recordingImprovement" class="space-y-4">
            <audio
              :src="improvingAudioUrl"
              controls
              class="w-full"
            ></audio>

            <div class="text-left">
              <label class="block text-sm text-gray-400 mb-2">Commentaire (optionnel)</label>
              <textarea
                v-model="improvementNotes"
                rows="3"
                placeholder="Ajoutez un commentaire sur cette amélioration..."
                class="w-full px-4 py-3 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 resize-none"
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <button
                @click="saveImprovement"
                :disabled="savingImprovement"
                class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-gray-600 text-white rounded-lg"
              >
                {{ savingImprovement ? 'Sauvegarde...' : '💾 Sauvegarder' }}
              </button>
              <button
                @click="discardImprovement"
                class="px-6 py-3 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg"
              >
                🗑️ Recommencer
              </button>
            </div>
          </div>
        </div>

        <button
          @click="closeImproveModal"
          class="w-full px-4 py-2 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg"
        >
          Annuler
        </button>
      </div>
    </div>

    <!-- Error/Info Alert Dialog -->
    <AlertDialog
      v-model="showErrorAlert"
      :type="errorType"
      :title="errorType === 'error' ? 'Erreur' : 'Information'"
      :message="errorMessage"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { recordingsAPI } from '@/services/parle-api'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import AlertDialog from '@/components/AlertDialog.vue'

const selectedLanguage = ref('en')
const recordings = ref([])
const loading = ref(false)
const saving = ref(false)

// Dialogs
const showDeleteConfirm = ref(false)
const recordingToDelete = ref(null)
const showErrorAlert = ref(false)
const errorMessage = ref('')
const errorType = ref('error')

// Improve modal
const showImproveModal = ref(false)
const improvingRecording = ref(null)
const recordingImprovement = ref(false)
const improvingAudioBlob = ref(null)
const improvingAudioUrl = ref(null)
const improvementRecordingTime = ref(0)
const improvementNotes = ref('')
const savingImprovement = ref(false)
let improvementMediaRecorder = null
let improvementRecordingInterval = null
let improvementAudioChunks = []

// Recording state
const recording = ref(false)
const audioBlob = ref(null)
const audioUrl = ref(null)
const recordingTime = ref(0)
const recordingNotes = ref('')
let mediaRecorder = null
let recordingInterval = null
let audioChunks = []

// Group recordings by parent_id or id for versioning
const groupedRecordings = computed(() => {
  const groups = []
  const processed = new Set()

  // Sort recordings by created_at desc to get latest first
  const sortedRecordings = [...recordings.value].sort((a, b) => 
    new Date(b.created_at) - new Date(a.created_at)
  )

  sortedRecordings.forEach(recording => {
    if (processed.has(recording.id)) return

    // Find all versions (including this one)
    const parentId = recording.parent_id || recording.id
    const versions = sortedRecordings.filter(r => 
      (r.parent_id === parentId || r.id === parentId) && !processed.has(r.id)
    ).sort((a, b) => b.version - a.version) // Latest version first

    versions.forEach(v => processed.add(v.id))

    groups.push({
      id: parentId,
      versions: versions
    })
  })

  return groups
})

onMounted(() => {
  loadRecordings()
})

onUnmounted(() => {
  if (recordingInterval) {
    clearInterval(recordingInterval)
  }
  if (improvementRecordingInterval) {
    clearInterval(improvementRecordingInterval)
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
    errorMessage.value = 'Impossible d\'accéder au microphone. Vérifiez les permissions de votre navigateur.'
    errorType.value = 'error'
    showErrorAlert.value = true
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
    // 1. Upload le fichier audio
    const uploadResponse = await recordingsAPI.uploadAudio(audioBlob.value)
    const audioUrl = uploadResponse.data.audio_url
    
    // 2. Créer l'enregistrement avec l'URL
    await recordingsAPI.create({
      language: selectedLanguage.value,
      audio_url: audioUrl,
      exercise_type: 'pronunciation',
      duration: recordingTime.value,
      notes: recordingNotes.value || null
    })
    
    discardRecording()
    loadRecordings()
  } catch (err) {
    console.error('Error saving recording:', err)
    errorMessage.value = 'Erreur lors de la sauvegarde: ' + (err.response?.data?.detail || err.message)
    errorType.value = 'error'
    showErrorAlert.value = true
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
  recordingNotes.value = ''
}

// Improve recording functions
const openImproveModal = (recording) => {
  improvingRecording.value = recording
  showImproveModal.value = true
}

const closeImproveModal = () => {
  showImproveModal.value = false
  improvingRecording.value = null
  discardImprovement()
}

const startImprovementRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    improvementMediaRecorder = new MediaRecorder(stream)
    improvementAudioChunks = []

    improvementMediaRecorder.ondataavailable = (event) => {
      improvementAudioChunks.push(event.data)
    }

    improvementMediaRecorder.onstop = () => {
      const blob = new Blob(improvementAudioChunks, { type: 'audio/webm' })
      improvingAudioBlob.value = blob
      improvingAudioUrl.value = URL.createObjectURL(blob)
      stream.getTracks().forEach(track => track.stop())
    }

    improvementMediaRecorder.start()
    recordingImprovement.value = true
    improvementRecordingTime.value = 0

    improvementRecordingInterval = setInterval(() => {
      improvementRecordingTime.value++
    }, 1000)
  } catch (err) {
    console.error('Error starting improvement recording:', err)
    errorMessage.value = 'Impossible d\'accéder au microphone.'
    errorType.value = 'error'
    showErrorAlert.value = true
  }
}

const stopImprovementRecording = () => {
  if (improvementMediaRecorder && recordingImprovement.value) {
    improvementMediaRecorder.stop()
    recordingImprovement.value = false
    if (improvementRecordingInterval) {
      clearInterval(improvementRecordingInterval)
    }
  }
}

const saveImprovement = async () => {
  if (!improvingAudioBlob.value || !improvingRecording.value) return

  savingImprovement.value = true
  try {
    // 1. Upload le fichier audio
    const uploadResponse = await recordingsAPI.uploadAudio(improvingAudioBlob.value)
    const audioUrl = uploadResponse.data.audio_url
    
    // 2. Créer la nouvelle version
    const parentId = improvingRecording.value.parent_id || improvingRecording.value.id
    await recordingsAPI.create({
      language: improvingRecording.value.language,
      audio_url: audioUrl,
      exercise_type: improvingRecording.value.exercise_type,
      duration: improvementRecordingTime.value,
      notes: improvementNotes.value || null,
      parent_id: parentId,
      version: improvingRecording.value.version + 1
    })
    
    closeImproveModal()
    loadRecordings()
  } catch (err) {
    console.error('Error saving improvement:', err)
    errorMessage.value = 'Erreur lors de la sauvegarde: ' + (err.response?.data?.detail || err.message)
    errorType.value = 'error'
    showErrorAlert.value = true
  } finally {
    savingImprovement.value = false
  }
}

const discardImprovement = () => {
  improvingAudioBlob.value = null
  if (improvingAudioUrl.value) {
    URL.revokeObjectURL(improvingAudioUrl.value)
  }
  improvingAudioUrl.value = null
  improvementRecordingTime.value = 0
  improvementNotes.value = ''
}

const deleteRecording = (id) => {
  recordingToDelete.value = id
  showDeleteConfirm.value = true
}

const confirmDeleteRecording = async () => {
  try {
    await recordingsAPI.delete(recordingToDelete.value)
    loadRecordings()
  } catch (err) {
    console.error('Error deleting recording:', err)
  } finally {
    recordingToDelete.value = null
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
