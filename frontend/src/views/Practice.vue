<template>
  <div class="min-h-screen bg-[#0a0a0a] font-light relative">
    <!-- Background Watermark -->
    <BackgroundWatermark />

    <!-- Header -->
    <header class="bg-[#111111]/80 backdrop-blur-md border-b border-[#1f1f1f] sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-12 lg:px-16">
        <div class="flex justify-between items-center py-10">
          <div class="flex items-center gap-12">
            <router-link to="/dashboard" class="text-gray-500 hover:text-gray-200 transition-colors text-sm font-light tracking-wide">
              ← Back
            </router-link>
            <h1 class="text-3xl font-light text-gray-100 tracking-tight">Practice</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-6xl mx-auto px-12 lg:px-16 py-16 relative z-10">
      <!-- Language Selection -->
      <div class="mb-16">
        <label class="block text-xs font-light text-gray-500 uppercase tracking-widest mb-4">Language</label>
        <div class="flex gap-4">
          <button
            @click="selectedLanguage = ''; loadRecordings()"
            class="px-6 py-3 rounded-lg border transition-all duration-300 font-light"
            :class="selectedLanguage === '' ? 'bg-[#5a189a] border-[#5a189a] text-white shadow-lg shadow-[#5a189a]/20' : 'bg-[#111111]/90 border-[#1f1f1f] text-gray-400 hover:border-gray-600 hover:text-gray-200'"
          >
            All Languages
          </button>
          <button
            @click="selectedLanguage = 'en'; loadRecordings()"
            class="flex items-center gap-2 px-6 py-3 rounded-lg border transition-all duration-300 font-light"
            :class="selectedLanguage === 'en' ? 'bg-[#5a189a] border-[#5a189a] text-white shadow-lg shadow-[#5a189a]/20' : 'bg-[#111111]/90 border-[#1f1f1f] text-gray-400 hover:border-gray-600 hover:text-gray-200'"
          >
            <span>🇬🇧</span> English
          </button>
          <button
            @click="selectedLanguage = 'fr'; loadRecordings()"
            class="flex items-center gap-2 px-6 py-3 rounded-lg border transition-all duration-300 font-light"
            :class="selectedLanguage === 'fr' ? 'bg-[#5a189a] border-[#5a189a] text-white shadow-lg shadow-[#5a189a]/20' : 'bg-[#111111]/90 border-[#1f1f1f] text-gray-400 hover:border-gray-600 hover:text-gray-200'"
          >
            <span>🇫🇷</span> Français
          </button>
        </div>
      </div>

      <!-- Audio Recorder -->
      <div class="bg-[#111111]/90 backdrop-blur-sm rounded-2xl p-16 mb-20 border border-[#1f1f1f] shadow-2xl">
        <h2 class="text-2xl font-light text-gray-100 mb-12 text-center tracking-tight">New Recording</h2>
        
        <div class="text-center">
          <div v-if="!recording && !audioBlob" class="mb-12">
            <button
              @click="startRecording"
              class="w-40 h-40 rounded-full bg-[#5a189a] hover:bg-[#7b2cbf] shadow-lg shadow-[#5a189a]/30 transition-all flex items-center justify-center mx-auto hover:scale-105 group"
            >
              <svg class="w-16 h-16 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
              </svg>
            </button>
            <p class="text-gray-500 mt-8 font-light text-sm tracking-wide">Click to start recording</p>
          </div>

          <div v-if="recording" class="mb-12">
            <button
              @click="stopRecording"
              class="w-40 h-40 rounded-full bg-red-600 hover:bg-red-500 shadow-lg shadow-red-500/30 animate-pulse transition-all flex items-center justify-center mx-auto"
            >
              <svg class="w-16 h-16 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M6 6h12v12H6z"/>
              </svg>
            </button>
            <p class="text-gray-100 mt-8 font-light tracking-wide">Recording... {{ recordingTime }}s</p>
          </div>

          <div v-if="audioBlob && !recording" class="space-y-8">
            <audio
              ref="audioPlayer"
              :src="audioUrl"
              controls
              class="w-full"
            ></audio>

            <div class="text-left">
              <label class="block text-xs font-light text-gray-500 uppercase tracking-widest mb-4">Notes (optional)</label>
              <textarea
                v-model="recordingNotes"
                rows="4"
                placeholder="Add your notes about this recording..."
                class="w-full px-6 py-4 bg-[#0a0a0a]/50 border border-[#1f1f1f] rounded-lg text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-[#2f2f2f] transition-colors font-light"
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-6">
              <button
                @click="saveRecording"
                :disabled="saving"
                class="group flex items-center justify-center gap-3 px-8 py-4 bg-gray-100 hover:bg-white disabled:bg-[#1f1f1f] text-[#0a0a0a] disabled:text-gray-600 rounded-lg transition-all font-light tracking-wide"
              >
                <svg class="w-5 h-5 text-green-600 group-disabled:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
                </svg>
                {{ saving ? 'Saving...' : 'Save' }}
              </button>
              <button
                @click="discardRecording"
                class="group flex items-center justify-center gap-3 px-8 py-4 bg-[#111111] hover:bg-[#1a1a1a] text-gray-200 border border-[#1f1f1f] rounded-lg transition-all font-light tracking-wide"
              >
                <svg class="w-5 h-5 text-red-500 group-hover:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Restart
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Recordings List -->
      <div class="space-y-12">
        <h2 class="text-2xl font-light text-gray-100 mb-12 tracking-tight">My Recordings</h2>

        <div v-if="loading" class="text-center py-20 text-gray-500 font-light tracking-wide">
          Loading...
        </div>

        <div v-else-if="groupedRecordings.length === 0" class="text-center py-20 bg-[#111111]/90 backdrop-blur-sm rounded-2xl border border-[#1f1f1f]">
          <p class="text-gray-500 font-light tracking-wide">No recordings yet</p>
          <p class="text-gray-600 text-sm mt-3 font-light">Create your first recording to get started</p>
        </div>

        <!-- Recording Groups (Vertical List) -->
        <div
          v-for="group in groupedRecordings"
          :key="group.id"
          class="bg-[#111111]/90 backdrop-blur-sm rounded-2xl p-12 border border-[#1f1f1f]"
        >
          <!-- Title from first version (v1) with edit capability -->
          <div v-if="group.versions[group.versions.length - 1]?.notes" class="mb-10">
            <div v-if="editingTitleGroupId !== group.id" class="flex items-center gap-4 group">
              <h3 class="text-xl text-gray-100 font-light tracking-tight">{{ group.versions[group.versions.length - 1].notes }}</h3>
              <button
                @click="startEditingTitle(group)"
                class="opacity-0 group-hover:opacity-100 text-[#7b2cbf] hover:text-[#5a189a] transition-all p-2"
                title="Edit title"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </button>
            </div>
            <div v-else class="flex items-center gap-3">
              <input
                v-model="editingTitleText"
                type="text"
                class="flex-1 px-6 py-3 bg-[#0a0a0a] border border-[#1f1f1f] rounded-lg text-gray-200 focus:outline-none focus:border-[#2f2f2f] transition-colors font-light"
                @keyup.enter="saveTitle(group)"
                @keyup.esc="cancelEditingTitle"
              />
              <button
                @click="saveTitle(group)"
                :disabled="savingTitle"
                class="group px-6 py-3 bg-gray-100 hover:bg-white disabled:opacity-50 text-[#0a0a0a] rounded-lg transition-all"
              >
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 13l4 4L19 7"/>
                </svg>
              </button>
              <button
                @click="cancelEditingTitle"
                class="group px-6 py-3 bg-[#111111] hover:bg-[#1a1a1a] text-gray-200 border border-[#1f1f1f] rounded-lg transition-all"
              >
                <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Horizontal Scrollable Versions List -->
          <div class="overflow-x-auto -mx-2 px-2">
            <div class="flex gap-8">
              <div
                v-for="(recording, vIndex) in group.versions"
                :key="recording.id"
                class="flex-shrink-0 w-96 bg-[#0a0a0a]/50 rounded-xl p-8 border transition-all"
                :class="vIndex === 0 ? 'border-gray-100' : 'border-[#1f1f1f]'"
              >
                <!-- Version Header with Date -->
                <div class="flex justify-between items-start mb-6">
                  <div class="flex items-center gap-3 text-sm font-light">
                    <span 
                      :class="vIndex === 0 ? 'bg-[#d4af37] text-black font-medium' : 'bg-[#111111] text-[#d4af37] border border-[#d4af37]/30'"
                      class="px-3 py-1.5 rounded-lg transition-colors"
                    >
                      v{{ recording.version }}
                    </span>
                    <span class="px-3 py-1.5 bg-[#111111] border border-[#1f1f1f] rounded-lg" :class="recording.language === 'en' ? 'text-[#7b2cbf]' : 'text-purple-400'">
                      {{ recording.language === 'en' ? '🇬🇧 EN' : '🇫🇷 FR' }}
                    </span>
                    <span class="text-gray-600 text-xs tracking-wide">
                      {{ formatDate(recording.created_at) }}
                    </span>
                  </div>
                  <button
                    @click="deleteRecording(recording.id)"
                    class="text-gray-500 hover:text-red-500 transition-colors p-1"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>

                <!-- Audio Player -->
                <audio
                  :src="`http://localhost:8000${recording.audio_url}`"
                  controls
                  class="w-full mb-6 rounded-lg"
                ></audio>

                <!-- Improve Button (only for latest version) -->
                <button
                  v-if="vIndex === 0"
                  @click="openImproveModal(recording)"
                  class="group w-full flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 hover:bg-white text-[#0a0a0a] rounded-lg transition-all font-light tracking-wide"
                >
                  <svg class="w-5 h-5 text-[#5a189a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  Improve
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
    class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-8"
    @click.self="closeImproveModal"
  >
    <div class="bg-[#111111]/90 backdrop-blur-sm rounded-2xl p-16 max-w-2xl w-full border border-[#1f1f1f] shadow-2xl">
      <h3 class="text-3xl font-light text-gray-100 mb-3 text-center tracking-tight">
        Improve Recording
      </h3>
      <p class="text-center text-gray-500 mb-12 font-light tracking-wide">Version {{ (improvingRecording?.version || 0) + 1 }}</p>

      <div class="text-center mb-12">
        <div v-if="!improvingAudioBlob && !recordingImprovement">
          <button
            @click="startImprovementRecording"
            class="w-40 h-40 rounded-full bg-[#5a189a] hover:bg-[#7b2cbf] shadow-lg shadow-[#5a189a]/30 transition-all flex items-center justify-center mx-auto hover:scale-105 group"
          >
            <svg class="w-16 h-16 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
            </svg>
          </button>
          <p class="text-gray-500 mt-8 font-light text-sm tracking-wide">Click to record new version</p>
        </div>

        <div v-if="recordingImprovement">
          <button
            @click="stopImprovementRecording"
            class="w-40 h-40 rounded-full bg-red-600 hover:bg-red-500 shadow-lg shadow-red-500/30 animate-pulse transition-all flex items-center justify-center mx-auto"
          >
            <svg class="w-16 h-16 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 6h12v12H6z"/>
            </svg>
          </button>
          <p class="text-gray-100 mt-8 font-light tracking-wide">Recording... {{ improvementRecordingTime }}s</p>
        </div>

        <div v-if="improvingAudioBlob && !recordingImprovement" class="space-y-8">
          <audio
            :src="improvingAudioUrl"
            controls
            class="w-full rounded-lg"
          ></audio>

          <div class="text-left">
            <label class="block text-xs font-light text-gray-500 uppercase tracking-widest mb-4">Notes</label>
            <textarea
              v-model="improvementNotes"
              rows="4"
              placeholder="Add your notes about this improvement..."
              class="w-full px-6 py-4 bg-[#0a0a0a] border border-[#1f1f1f] rounded-lg text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-[#2f2f2f] transition-colors font-light"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <button
              @click="saveImprovement"
              :disabled="savingImprovement"
              class="group flex items-center justify-center gap-2 px-8 py-4 bg-gray-100 hover:bg-white disabled:bg-[#1f1f1f] text-[#0a0a0a] disabled:text-gray-600 rounded-lg transition-all font-light tracking-wide"
            >
              <svg class="w-5 h-5 text-green-600 group-disabled:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
              </svg>
              {{ savingImprovement ? 'Saving...' : 'Save' }}
            </button>
            <button
              @click="discardImprovement"
              class="group flex items-center justify-center gap-2 px-8 py-4 bg-[#111111] hover:bg-[#1a1a1a] text-gray-200 border border-[#1f1f1f] rounded-lg transition-all font-light tracking-wide"
            >
              <svg class="w-5 h-5 text-red-500 group-hover:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Restart
            </button>
          </div>
        </div>
      </div>

      <button
        @click="closeImproveModal"
        class="w-full mt-8 px-8 py-4 bg-[#111111] hover:bg-[#1a1a1a] text-gray-200 border border-[#1f1f1f] rounded-lg transition-all font-light tracking-wide"
      >
        Cancel
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
import BackgroundWatermark from '@/components/BackgroundWatermark.vue'

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

// Title editing
const editingTitleGroupId = ref(null)
const editingTitleText = ref('')
const savingTitle = ref(false)

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

const startEditingTitle = (group) => {
  const firstVersion = group.versions[group.versions.length - 1]
  editingTitleGroupId.value = group.id
  editingTitleText.value = firstVersion.notes || ''
}

const cancelEditingTitle = () => {
  editingTitleGroupId.value = null
  editingTitleText.value = ''
}

const saveTitle = async (group) => {
  const firstVersion = group.versions[group.versions.length - 1]
  if (!editingTitleText.value.trim() || savingTitle.value) return

  savingTitle.value = true
  try {
    await recordingsAPI.update(firstVersion.id, {
      notes: editingTitleText.value.trim()
    })
    
    // Update local state
    firstVersion.notes = editingTitleText.value.trim()
    editingTitleGroupId.value = null
    editingTitleText.value = ''
  } catch (err) {
    console.error('Error updating title:', err)
    errorMessage.value = 'Impossible de modifier le titre'
    errorType.value = 'error'
    showErrorAlert.value = true
  } finally {
    savingTitle.value = false
  }
}
</script>
