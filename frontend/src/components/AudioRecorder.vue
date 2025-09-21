<template>
  <div class="audio-recorder">
    <div class="recorder-controls">
      <el-button 
        v-if="!isRecording" 
        type="primary" 
        size="large" 
        @click="startRecording"
        :disabled="disabled"
      >
        <el-icon><Microphone /></el-icon>
        {{ startButtonText }}
      </el-button>
      
      <el-button 
        v-if="isRecording" 
        type="danger" 
        size="large" 
        @click="stopRecording"
      >
        <el-icon><VideoPause /></el-icon>
        Arrêter
      </el-button>
      
      <el-button 
        v-if="hasRecording && !isProcessing" 
        type="success" 
        size="large" 
        @click="processRecording"
      >
        <el-icon><Search /></el-icon>
        Analyser
      </el-button>
    </div>

    <!-- Recording Status -->
    <div v-if="isRecording" class="recording-status">
      <div class="recording-indicator">
        <el-icon class="pulse-icon"><Microphone /></el-icon>
        <span>{{ recordingTime }}s</span>
      </div>
      <p>Enregistrement en cours...</p>
    </div>

    <!-- Processing Status -->
    <div v-if="isProcessing" class="processing-status">
      <el-progress 
        :percentage="processingProgress" 
        :status="processingStatus"
        :stroke-width="8"
      />
      <p>{{ processingText }}</p>
    </div>

    <!-- Audio Player -->
    <div v-if="audioUrl" class="audio-player">
      <h4>Votre enregistrement :</h4>
      <audio :src="audioUrl" controls class="audio-element"></audio>
    </div>

    <!-- Results -->
    <div v-if="analysisResult" class="analysis-results">
      <el-divider>Résultats de l'Analyse</el-divider>
      
      <el-alert
        :title="`Confiance: ${analysisResult.confidence}%`"
        :type="analysisResult.confidence > 80 ? 'success' : 'warning'"
        :closable="false"
        class="confidence-alert"
      />

      <div class="result-grid">
        <el-card class="result-card">
          <h4>Transcription</h4>
          <p>{{ analysisResult.transcription }}</p>
        </el-card>
        
        <el-card class="result-card">
          <h4>Erreurs Détectées</h4>
          <div v-if="analysisResult.errors.length">
            <el-tag 
              v-for="error in analysisResult.errors" 
              :key="error.word"
              :type="getErrorType(error.severity)"
              class="error-tag"
            >
              {{ error.word }}
            </el-tag>
          </div>
          <p v-else class="success-text">Aucune erreur détectée !</p>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Microphone, VideoPause, Search } from '@element-plus/icons-vue'
import { speechService } from '@/services/api'

// Props
const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  startButtonText: {
    type: String,
    default: 'Commencer l\'Enregistrement'
  },
  expectedText: {
    type: String,
    default: ''
  }
})

// Emits
const emit = defineEmits(['recording-started', 'recording-stopped', 'analysis-complete'])

// Reactive data
const isRecording = ref(false)
const hasRecording = ref(false)
const isProcessing = ref(false)
const recordingTime = ref(0)
const processingProgress = ref(0)
const processingStatus = ref('active')
const processingText = ref('')
const audioUrl = ref('')
const analysisResult = ref(null)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const recordingInterval = ref(null)

// Computed
const canRecord = computed(() => {
  return !props.disabled && !isRecording.value && !isProcessing.value
})

// Methods
const startRecording = async () => {
  try {
    // Demander l'autorisation d'accès au microphone
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 44100
      } 
    })
    
    // Créer le MediaRecorder
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    // Gérer les données d'enregistrement
    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    // Gérer la fin d'enregistrement
    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
      audioUrl.value = URL.createObjectURL(audioBlob)
      hasRecording.value = true
      emit('recording-stopped', audioBlob)
    }
    
    // Démarrer l'enregistrement
    mediaRecorder.value.start()
    isRecording.value = true
    recordingTime.value = 0
    
    // Démarrer le timer
    recordingInterval.value = setInterval(() => {
      recordingTime.value++
    }, 1000)
    
    emit('recording-started')
    ElMessage.success('Enregistrement démarré')
    
  } catch (error) {
    console.error('Erreur accès microphone:', error)
    ElMessage.error('Impossible d\'accéder au microphone')
  }
}

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
    isRecording.value = false
    
    // Arrêter le timer
    if (recordingInterval.value) {
      clearInterval(recordingInterval.value)
      recordingInterval.value = null
    }
    
    // Arrêter le stream
    const tracks = mediaRecorder.value.stream.getTracks()
    tracks.forEach(track => track.stop())
    
    ElMessage.success('Enregistrement terminé')
  }
}

const processRecording = async () => {
  try {
    isProcessing.value = true
    processingProgress.value = 0
    processingStatus.value = 'active'
    processingText.value = 'Analyse en cours...'
    
    // Simulation du progrès
    const progressInterval = setInterval(() => {
      if (processingProgress.value < 90) {
        processingProgress.value += 10
      }
    }, 200)
    
    // Créer un FormData pour l'envoi
    const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
    const formData = new FormData()
    formData.append('audio_file', audioBlob, 'recording.wav')
    if (props.expectedText) {
      formData.append('expected_text', props.expectedText)
    }
    
    // Appel à l'API (simulation pour l'instant)
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Résultat simulé
    const mockResult = {
      transcription: "Transcription simulée de l'enregistrement",
      confidence: 85.5,
      errors: [
        { word: "exemple", type: "prononciation", severity: "medium" }
      ],
      prosody: {
        rhythm: { regularity: 0.8 },
        intonation: { monotone: false },
        tempo: 120
      }
    }
    
    clearInterval(progressInterval)
    processingProgress.value = 100
    processingStatus.value = 'success'
    processingText.value = 'Analyse terminée !'
    
    analysisResult.value = mockResult
    emit('analysis-complete', mockResult)
    
    ElMessage.success('Analyse terminée')
    
  } catch (error) {
    console.error('Erreur analyse:', error)
    processingStatus.value = 'exception'
    processingText.value = 'Erreur lors de l\'analyse'
    ElMessage.error('Erreur lors de l\'analyse')
  } finally {
    isProcessing.value = false
  }
}

const getErrorType = (severity) => {
  switch (severity) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'info'
    default: return 'info'
  }
}

const reset = () => {
  isRecording.value = false
  hasRecording.value = false
  isProcessing.value = false
  recordingTime.value = 0
  processingProgress.value = 0
  audioUrl.value = ''
  analysisResult.value = null
  
  if (recordingInterval.value) {
    clearInterval(recordingInterval.value)
    recordingInterval.value = null
  }
}

// Lifecycle
onMounted(() => {
  // Vérifier la disponibilité de l'API MediaRecorder
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    ElMessage.warning('L\'enregistrement audio n\'est pas supporté sur ce navigateur')
  }
})

onUnmounted(() => {
  if (recordingInterval.value) {
    clearInterval(recordingInterval.value)
  }
  
  if (mediaRecorder.value && mediaRecorder.value.stream) {
    const tracks = mediaRecorder.value.stream.getTracks()
    tracks.forEach(track => track.stop())
  }
})

// Exposer les méthodes
defineExpose({
  reset,
  startRecording,
  stopRecording
})
</script>

<style scoped>
.audio-recorder {
  text-align: center;
  padding: 20px;
}

.recorder-controls .el-button {
  margin: 0 10px;
}

.recording-status {
  margin: 20px 0;
  padding: 20px;
  background-color: #fef0f0;
  border-radius: 8px;
  border-left: 4px solid #f56c6c;
}

.recording-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: bold;
  color: #f56c6c;
}

.pulse-icon {
  margin-right: 10px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.processing-status {
  margin: 20px 0;
  padding: 20px;
  background-color: #f0f9ff;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.processing-status p {
  margin-top: 15px;
  color: #666;
  font-size: 1.1rem;
}

.audio-player {
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.audio-player h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.audio-element {
  width: 100%;
  max-width: 500px;
}

.analysis-results {
  margin: 30px 0;
  text-align: left;
}

.confidence-alert {
  margin: 20px 0;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.result-card h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.error-tag {
  margin: 5px;
}

.success-text {
  color: #67c23a;
  font-weight: 500;
}

@media (max-width: 768px) {
  .recorder-controls .el-button {
    display: block;
    width: 100%;
    margin: 10px 0;
  }
  
  .result-grid {
    grid-template-columns: 1fr;
  }
}
</style>
