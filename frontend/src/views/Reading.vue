<template>
  <div class="reading">
    <el-row :gutter="20" justify="center">
      <el-col :span="24" :md="20" :lg="16">
        <el-card class="reading-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h2>Lecture à Voix Haute</h2>
              <p>Lisez le texte à voix haute pour recevoir un feedback en temps réel</p>
            </div>
          </template>

          <!-- Progress Bar -->
          <div class="progress-section">
            <el-progress 
              :percentage="readingProgress" 
              :status="progressStatus"
              :stroke-width="8"
            />
            <p class="progress-text">Paragraphe {{ currentParagraph }} sur {{ totalParagraphs }}</p>
          </div>

          <!-- Current Paragraph -->
          <div class="paragraph-section">
            <h3>Paragraphe {{ currentParagraph }}</h3>
            <div class="text-content" :class="{ 'highlighted': isRecording }">
              <p v-for="(sentence, index) in currentText" :key="index" 
                 :class="getSentenceClass(index)">
                <span v-for="(part, i) in tokenizeSentence(sentence)" :key="i" :class="{ 'word-error': part.isError, 'word': true }">{{ part.text }}</span>
              </p>
            </div>
          </div>

          <!-- Recording Controls -->
          <div class="recording-section">
            <div class="recording-status" v-if="isRecording">
              <span class="timer">{{ formattedTime }}</span>
              <div class="vu-meter">
                <div class="vu-fill" :style="{ width: vuLevel + '%' }"></div>
              </div>
              <canvas ref="waveformRef" class="waveform-canvas"></canvas>
            </div>
            <el-button 
              v-if="!isRecording" 
              type="primary" 
              size="large" 
              @click="startRecording"
              :disabled="!currentText.length"
            >
              <el-icon><Microphone /></el-icon>
              Commencer l'Enregistrement
            </el-button>
            
            <el-button 
              v-if="isRecording" 
              type="danger" 
              size="large" 
              @click="stopRecording"
            >
              <el-icon><VideoPause /></el-icon>
              Arrêter l'Enregistrement
            </el-button>
            
            <el-button 
              v-if="hasRecording" 
              type="success" 
              size="large" 
              @click="analyzeRecording"
              :loading="analyzing"
            >
              <el-icon><Search /></el-icon>
              Analyser la Lecture
            </el-button>
          </div>

          <!-- Analysis Results -->
          <div v-if="analysisResult" class="analysis-section">
            <el-divider>Résultats de l'Analyse</el-divider>
            
            <el-alert
              :title="`Confiance: ${analysisResult.confidence}%`"
              :type="analysisResult.confidence > 80 ? 'success' : 'warning'"
              :closable="false"
              class="confidence-alert"
            />

            <div class="feedback-grid">
              <el-card class="feedback-card">
                <h4>Transcription</h4>
                <p>{{ analysisResult.transcription }}</p>
              </el-card>
              
              <el-card class="feedback-card">
                <h4>Erreurs Détectées</h4>
                <ul v-if="analysisResult.errors.length">
                  <li v-for="error in analysisResult.errors" :key="error.word">
                    <el-tag :type="getErrorType(error.severity)">
                      {{ error.word }}
                    </el-tag>
                    - {{ error.type }}
                  </li>
                </ul>
                <p v-else class="success-text">Aucune erreur détectée !</p>
              </el-card>
              
              <el-card class="feedback-card">
                <h4>Analyse Prosodique</h4>
                <div class="prosody-info">
                  <p><strong>Rythme:</strong> {{ analysisResult.prosody.rhythm.regularity * 100 }}% régulier</p>
                  <p><strong>Intonation:</strong> {{ analysisResult.prosody.intonation.monotone ? 'Monotone' : 'Variée' }}</p>
                  <p><strong>Tempo:</strong> {{ analysisResult.prosody.tempo }} BPM</p>
                </div>
              </el-card>
            </div>

            <!-- Model Audio -->
            <div class="model-audio-section">
              <h4>Écouter le Modèle</h4>
              <el-button @click="playModelAudio" :loading="loadingAudio">
                <el-icon><VideoPlay /></el-icon>
                Lire le Modèle
              </el-button>
              <audio ref="audioPlayer" controls style="margin-left: 10px;"></audio>
            </div>
          </div>

          <!-- Navigation -->
          <div class="navigation-section">
            <el-button 
              @click="previousParagraph" 
              :disabled="currentParagraph <= 1"
            >
              <el-icon><ArrowLeft /></el-icon>
              Précédent
            </el-button>
            
            <el-button 
              @click="nextParagraph" 
              :disabled="currentParagraph >= totalParagraphs"
              type="primary"
            >
              Suivant
              <el-icon><ArrowRight /></el-icon>
            </el-button>
            
            <el-button 
              v-if="currentParagraph >= 2" 
              @click="goToSummary" 
              type="success"
            >
              <el-icon><Document /></el-icon>
              Mode Résumé
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Microphone, 
  VideoPause, 
  Search, 
  VideoPlay, 
  ArrowLeft, 
  ArrowRight, 
  Document 
} from '@element-plus/icons-vue'
import { speechService } from '@/services/api'

const route = useRoute()
const router = useRouter()

// Reactive data
const currentParagraph = ref(1)
const totalParagraphs = ref(0)
const currentText = ref([])
const isRecording = ref(false)
const hasRecording = ref(false)
const analyzing = ref(false)
const loadingAudio = ref(false)
const analysisResult = ref(null)
const audioBlob = ref(null)
const audioPlayer = ref(null)

// Recording state
const mediaRecorder = ref(null)
const mediaStream = ref(null)
const audioChunks = ref([])
const audioContext = ref(null)
const analyserNode = ref(null)
const vuLevel = ref(0)
const rafId = ref(null)
const rafWaveId = ref(null)
const recordSeconds = ref(0)
let recordTimer = null
const waveformRef = ref(null)

// Error words cache
const errorWords = ref(new Set())

// Computed
const readingProgress = computed(() => {
  return totalParagraphs.value > 0 ? (currentParagraph.value / totalParagraphs.value) * 100 : 0
})

const progressStatus = computed(() => {
  if (isRecording.value) return 'active'
  if (analysisResult.value) return 'success'
  return ''
})

// Methods
const loadText = () => {
  // Charger le texte depuis localStorage ou l'API
  const savedText = localStorage.getItem('currentText')
  if (savedText) {
    const textData = JSON.parse(savedText)
    const paragraphText = textData.paragraphs[currentParagraph.value - 1] || ""
    currentText.value = paragraphText.split(/[.!?]+/).filter(sentence => sentence.trim())
    totalParagraphs.value = textData.paragraphs.length
  } else {
    // Texte de démonstration
    currentText.value = [
      "Ceci est un exemple de texte pour l'entraînement à l'oral",
      "Lisez ce paragraphe à voix haute pour recevoir un feedback",
      "L'application analysera votre prononciation et votre rythme"
    ]
    totalParagraphs.value = 3
  }
}

const startRecording = async () => {
  try {
    hasRecording.value = false
    analysisResult.value = null
    audioBlob.value = null

    // Acquire microphone
    // const stream = await navigator.mediaDevices.getUserMedia({
    //   audio: {
    //     echoCancellation: true,
    //     noiseSuppression: true,
    //     sampleRate: 44100
    //   }
    // })
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaStream.value = stream

    // Create MediaRecorder
    const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
      ? 'audio/webm;codecs=opus'
      : 'audio/webm'
    mediaRecorder.value = new MediaRecorder(stream, { mimeType })
    audioChunks.value = []

    mediaRecorder.value.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        audioChunks.value.push(e.data)
      }
    }

    mediaRecorder.value.onstop = () => {
      const blob = new Blob(audioChunks.value, { type: mimeType })
      audioBlob.value = blob
      hasRecording.value = true
      if (audioPlayer.value) {
        audioPlayer.value.src = URL.createObjectURL(blob)
      }
    }

    mediaRecorder.value.start()
    isRecording.value = true

    // Init audio context for VU meter (best-effort)
    try {
      audioContext.value = new (window.AudioContext || window.webkitAudioContext)()
      const source = audioContext.value.createMediaStreamSource(stream)
      analyserNode.value = audioContext.value.createAnalyser()
      analyserNode.value.fftSize = 2048
      source.connect(analyserNode.value)
    } catch (e) {
      console.warn('AudioContext init failed (waveform disabled):', e)
      analyserNode.value = null
    }

    const dataArray = analyserNode.value ? new Uint8Array(analyserNode.value.fftSize) : null
    const updateVu = () => {
      if (!analyserNode.value || !dataArray) return
      analyserNode.value.getByteTimeDomainData(dataArray)
      // Compute RMS
      let sum = 0
      for (let i = 0; i < dataArray.length; i++) {
        const v = (dataArray[i] - 128) / 128
        sum += v * v
      }
      const rms = Math.sqrt(sum / dataArray.length)
      vuLevel.value = Math.min(100, Math.max(0, Math.round(rms * 140)))
      rafId.value = requestAnimationFrame(updateVu)
    }
    rafId.value = requestAnimationFrame(updateVu)

    // Waveform drawing
    const waveformCanvas = waveformRef.value
    const drawWaveform = () => {
      if (!analyserNode.value || !waveformCanvas) return
      const canvas = waveformCanvas
      const ctx = canvas.getContext('2d')
      // Resize canvas to container width
      const parentWidth = canvas.parentElement ? canvas.parentElement.clientWidth : 500
      const height = 80
      if (canvas.width !== parentWidth) canvas.width = parentWidth
      if (canvas.height !== height) canvas.height = height

      const bufferLength = analyserNode.value.fftSize
      const data = new Uint8Array(bufferLength)
      analyserNode.value.getByteTimeDomainData(data)

      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.lineWidth = 2
      ctx.strokeStyle = '#409EFF'
      ctx.beginPath()

      const sliceWidth = canvas.width / bufferLength
      let x = 0
      for (let i = 0; i < bufferLength; i++) {
        const v = data[i] / 128.0
        const y = (v * canvas.height) / 2
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
        x += sliceWidth
      }
      ctx.lineTo(canvas.width, canvas.height / 2)
      ctx.stroke()

      rafWaveId.value = requestAnimationFrame(drawWaveform)
    }
    rafWaveId.value = requestAnimationFrame(drawWaveform)

    // Timer
    recordSeconds.value = 0
    if (recordTimer) clearInterval(recordTimer)
    recordTimer = setInterval(() => { recordSeconds.value += 1 }, 1000)
  } catch (error) {
    console.error(error)
    ElMessage.error('Impossible d\'accéder au microphone')
    isRecording.value = false
  }
}

const stopRecording = async () => {
  if (!mediaRecorder.value || !isRecording.value) {
    isRecording.value = false
    return
  }
  try {
    isRecording.value = false
    // Wait for onstop to flush the last data chunk and build the blob
    const stopPromise = new Promise((resolve) => {
      const handleStop = () => {
        mediaRecorder.value.removeEventListener('stop', handleStop)
        resolve()
      }
      mediaRecorder.value.addEventListener('stop', handleStop)
    })
    mediaRecorder.value.stop()
    await stopPromise

    // Now it's safe to stop tracks and cleanup audio context
    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(t => t.stop())
      mediaStream.value = null
    }
    if (rafId.value) cancelAnimationFrame(rafId.value)
    if (rafWaveId.value) cancelAnimationFrame(rafWaveId.value)
    if (audioContext.value) {
      try { audioContext.value.close() } catch (_) {}
      audioContext.value = null
      analyserNode.value = null
    }
    if (recordTimer) { clearInterval(recordTimer); recordTimer = null }
    ElMessage.success('Enregistrement terminé')
  } catch (_) {
    // noop
  }
}

const analyzeRecording = async () => {
  if (!audioBlob.value) {
    ElMessage.warning('Aucun enregistrement disponible')
    return
  }
  try {
    analyzing.value = true

    const formData = new FormData()
    const expectedText = currentText.value.join('. ').trim()
    formData.append('audio_file', audioBlob.value, 'reading.webm')
    if (expectedText) formData.append('expected_text', expectedText)

    const { data } = await speechService.analyzeSpeech(formData)
    analysisResult.value = {
      transcription: data.transcription || '',
      confidence: data.confidence ?? 0,
      errors: data.errors || [],
      prosody: data.prosody || { rhythm: { regularity: 0 }, intonation: { monotone: false }, tempo: 0 }
    }
    // Build error words set
    errorWords.value = new Set((analysisResult.value.errors || []).map(e => String(e.word || '').toLowerCase()))

    // Persist result and audio
    const reader = new FileReader()
    reader.onload = () => {
      const key = 'readingResults'
      const store = JSON.parse(localStorage.getItem(key) || '{}')
      store[currentParagraph.value] = {
        audioUrl: reader.result,
        analysis: analysisResult.value
      }
      localStorage.setItem(key, JSON.stringify(store))
    }
    reader.readAsDataURL(audioBlob.value)
    ElMessage.success('Analyse terminée')
  } catch (error) {
    console.error(error)
    ElMessage.error('Erreur lors de l\'analyse')
  } finally {
    analyzing.value = false
  }
}

const playModelAudio = async () => {
  try {
    loadingAudio.value = true
    
    // Simulation de la génération audio
    ElMessage.info('Génération du modèle audio...')
    
    // Ici, vous intégreriez l'API TTS
    setTimeout(() => {
      loadingAudio.value = false
      ElMessage.success('Modèle audio prêt')
    }, 1500)
    
  } catch (error) {
    ElMessage.error('Erreur lors de la génération audio')
    loadingAudio.value = false
  }
}

const getSentenceClass = (index) => {
  if (!analysisResult.value) return ''
  
  // Simulation de la mise en évidence des erreurs
  const sentence = currentText.value[index] || ''
  const words = sentence.toLowerCase().split(/\s+/)
  const hasErr = words.some(w => errorWords.value.has(w.replace(/[^\p{L}\p{N}'-]/gu, '')))
  return {
    'error-sentence': hasErr,
    'correct-sentence': !hasErr
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

const previousParagraph = () => {
  if (currentParagraph.value > 1) {
    currentParagraph.value--
    loadText()
    resetAnalysis()
  }
}

const nextParagraph = () => {
  if (currentParagraph.value < totalParagraphs.value) {
    currentParagraph.value++
    loadText()
    resetAnalysis()
  }
}

const goToSummary = () => {
  router.push({
    name: 'Summary',
    params: { textId: route.params.textId }
  })
}

const resetAnalysis = () => {
  analysisResult.value = null
  hasRecording.value = false
  isRecording.value = false
}

// Lifecycle
onMounted(() => {
  loadText()
  // Restore stored analysis/audio per paragraph
  try {
    const store = JSON.parse(localStorage.getItem('readingResults') || '{}')
    const saved = store[currentParagraph.value]
    if (saved) {
      analysisResult.value = saved.analysis
      errorWords.value = new Set((saved.analysis?.errors || []).map(e => String(e.word || '').toLowerCase()))
      hasRecording.value = !!saved.audioUrl
      if (audioPlayer.value && saved.audioUrl) {
        audioPlayer.value.src = saved.audioUrl
      }
    }
  } catch (_) {}
})

onUnmounted(() => {
  try {
    if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
      mediaRecorder.value.stop()
    }
  } catch (_) {}
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(t => t.stop())
  }
})

// Formatting helpers
const formattedTime = computed(() => {
  const m = String(Math.floor(recordSeconds.value / 60)).padStart(2, '0')
  const s = String(recordSeconds.value % 60).padStart(2, '0')
  return `${m}:${s}`
})

const tokenizeSentence = (sentence) => {
  const parts = []
  const tokens = sentence.split(/(\s+)/)
  for (const tok of tokens) {
    if (tok.trim().length === 0) {
      parts.push({ text: tok, isError: false })
      continue
    }
    const normalized = tok.toLowerCase().replace(/[^\p{L}\p{N}'-]/gu, '')
    parts.push({ text: tok, isError: errorWords.value.has(normalized) })
  }
  return parts
}
</script>

<style scoped>
.reading {
  max-width: 1200px;
  margin: 0 auto;
}

.reading-card {
  margin-bottom: 30px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.card-header p {
  color: #666;
  margin: 0;
}

.progress-section {
  margin: 30px 0;
  text-align: center;
}

.progress-text {
  margin-top: 15px;
  color: #666;
  font-size: 1.1rem;
}

.paragraph-section {
  margin: 30px 0;
}

.paragraph-section h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.text-content {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
  border-left: 4px solid #409EFF;
  min-height: 200px;
  transition: all 0.3s ease;
}

.text-content.highlighted {
  border-left-color: #E6A23C;
  background-color: #fdf6ec;
}

.text-content p {
  margin-bottom: 15px;
  line-height: 1.8;
  font-size: 1.1rem;
  color: #333;
}

.error-sentence {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 5px;
  border-radius: 4px;
}

.correct-sentence {
  color: #67c23a;
}

.recording-section {
  text-align: center;
  margin: 30px 0;
}

.recording-section .el-button {
  margin: 0 10px;
}

.recording-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.timer {
  font-weight: 600;
  color: #2c3e50;
}

.vu-meter {
  width: 100%;
  max-width: 480px;
  height: 8px;
  background: #ebeef5;
  border-radius: 6px;
  overflow: hidden;
}

.vu-fill {
  height: 100%;
  background: linear-gradient(90deg, #67c23a, #e6a23c, #f56c6c);
  transition: width 120ms linear;
}

.waveform-canvas {
  width: 100%;
  max-width: 640px;
  height: 80px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.analysis-section {
  margin: 30px 0;
}

.confidence-alert {
  margin: 20px 0;
}

.feedback-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.feedback-card h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.feedback-card ul {
  padding-left: 20px;
}

.feedback-card li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.success-text {
  color: #67c23a;
  font-weight: 500;
}

.prosody-info p {
  margin-bottom: 10px;
  color: #666;
}

.model-audio-section {
  margin: 30px 0;
  text-align: center;
}

.model-audio-section h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.navigation-section {
  text-align: center;
  margin: 30px 0;
}

.navigation-section .el-button {
  margin: 0 10px;
}

@media (max-width: 768px) {
  .recording-section .el-button,
  .navigation-section .el-button {
    display: block;
    width: 100%;
    margin: 10px 0;
  }
  
  .feedback-grid {
    grid-template-columns: 1fr;
  }
}
</style>
