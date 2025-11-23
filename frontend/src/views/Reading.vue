<template>
  <div class="reading two-pane">
    <el-row :gutter="20" justify="start">
      <el-col :span="24" :md="14" :lg="14">
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
                <template v-for="(part, i) in tokenizeSentence(sentence, index)" :key="i">
                  <el-tooltip
                    v-if="part.tooltip"
                    effect="dark"
                    :content="part.tooltip"
                    placement="top"
                  >
                    <span :class="getWordClass(part)">{{ part.text }}</span>
                  </el-tooltip>
                  <span v-else :class="getWordClass(part)">{{ part.text }}</span>
                </template>
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
              :title="`Confiance: ${displayConfidence}%`"
              :type="displayConfidence >= 70 ? 'success' : 'warning'"
              :closable="false"
              class="confidence-alert"
            />

            <div class="feedback-grid">
              <el-card class="feedback-card">
                <h4>Transcription</h4>
                <p v-if="analysisResult.transcription && analysisResult.transcription.length">{{ analysisResult.transcription }}</p>
                <p v-else class="muted">(Aucune transcription renvoyée)</p>
              </el-card>
              
              <el-card class="feedback-card">
                <h4>Analyse Prosodique</h4>
                <div class="prosody-info">
                  <p><strong>Rythme:</strong> {{ (analysisResult.prosody?.rhythm?.regularity ?? 0) * 100 }}% régulier</p>
                  <p><strong>Intonation:</strong> {{ analysisResult.prosody?.intonation?.monotone ? 'Monotone' : 'Variée' }}</p>
                  <p><strong>Tempo:</strong> {{ analysisResult.prosody?.tempo ?? 0 }} BPM</p>
                </div>
              </el-card>
            </div>

            <el-collapse>
              <el-collapse-item title="Détails (réponse brute)" name="raw">
                <pre class="raw-json">{{ rawResponsePretty }}</pre>
              </el-collapse-item>
            </el-collapse>

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
      <!-- Summary Panel -->
      <el-col :span="24" :md="10" :lg="10">
        <el-card class="summary-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h3>Mode Résumé (Oral)</h3>
              <p>Enregistrez votre résumé des paragraphes lus puis évaluez-le.</p>
            </div>
          </template>
          <div class="summary-source-text">
            <el-input
              type="textarea"
              :rows="5"
              v-model="summarySourceText"
              placeholder="Texte source (pré-rempli avec les paragraphes courants)"
            />
          </div>
          <div class="summary-recording-section">
            <div v-if="isSummaryRecording" class="recording-status small">
              <span class="timer">{{ summaryFormattedTime }}</span>
              <div class="vu-meter">
                <div class="vu-fill" :style="{ width: summaryVuLevel + '%' }"></div>
              </div>
            </div>
            <el-button v-if="!isSummaryRecording" type="primary" size="default" @click="startSummaryRecording">
              <el-icon><Microphone /></el-icon>
              Enregistrer Résumé
            </el-button>
            <el-button v-if="isSummaryRecording" type="danger" size="default" @click="stopSummaryRecording">
              <el-icon><VideoPause /></el-icon>
              Stop
            </el-button>
            <el-button v-if="hasSummaryRecording && !summaryAnalyzing" type="success" size="default" @click="evaluateSummary">
              <el-icon><Search /></el-icon>
              Évaluer
            </el-button>
            <el-button v-if="summaryResult && !summaryAnalyzing" type="warning" size="default" @click="llmEvaluateSummary">
              GPT / LLM
            </el-button>
            <el-button v-if="summaryAnalyzing" :loading="true" type="info">Analyse…</el-button>
          </div>
          <div v-if="summaryResult" class="summary-results">
            <el-divider>Résultats Résumé</el-divider>
            <el-alert
              :title="`Pertinence: ${(summaryResult.relevance_score*100).toFixed(0)}% | Qualité: ${(summaryResult.quality_score*100).toFixed(0)}%`"
              type="info"
              :closable="false"
              class="mb-2"
            />
            <p><strong>Transcription:</strong> {{ summaryResult.transcription }}</p>
            <div v-if="summaryResult.suggestions?.length">
              <h4>Suggestions</h4>
              <ul>
                <li v-for="(s,i) in summaryResult.suggestions" :key="i">{{ s }}</li>
              </ul>
            </div>
            <div v-if="summaryResult.transitions?.length">
              <h4>Transitions détectées</h4>
              <el-tag v-for="(t,i) in summaryResult.transitions" :key="i" class="mr-1 mb-1">{{ t }}</el-tag>
            </div>
            <div v-if="summaryResult.errors?.length">
              <h4>Erreurs</h4>
              <ul>
                <li v-for="(e,i) in summaryResult.errors" :key="i">{{ e.type }} - {{ e.word || e.sentence || '' }} ({{ e.severity || e.count || '' }})</li>
              </ul>
            </div>
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
import { speechService, ttsService, summaryService } from '@/services/api'

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
const rawResponse = ref(null)

// Summary panel state
const summarySourceText = ref('')
const isSummaryRecording = ref(false)
const hasSummaryRecording = ref(false)
const summaryAnalyzing = ref(false)
const summaryAudioBlob = ref(null)
const summaryMediaRecorder = ref(null)
const summaryChunks = ref([])
const summarySeconds = ref(0)
let summaryTimer = null
const summaryVuLevel = ref(0)
const summaryStream = ref(null)
const summaryResult = ref(null)

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
const errorWordMap = ref(new Map()) // normalizedWord -> array of error objects
const correctWords = ref(new Set()) // mots correctement prononcés
const pronouncedWords = ref(new Set()) // tous les mots prononcés (pour identifier les non-prononcés)
const similarWords = ref(new Set()) // mots presque corrects (similarité élevée)
// Position-aware highlighting structures
const expectedNormTokens = ref([])      // tokens normalisés du texte attendu
const sentenceTokenRanges = ref([])     // par phrase: [start, end)
const tokenStatus = ref([])             // statut par index j: 'correct' | 'similar' | 'error' | 'neutral'
const tokenTooltip = ref([])            // tooltip par index j

// Computed
const readingProgress = computed(() => {
  return totalParagraphs.value > 0 ? (currentParagraph.value / totalParagraphs.value) * 100 : 0
})

const progressStatus = computed(() => {
  if (isRecording.value) return 'active'
  if (analysisResult.value) return 'success'
  return ''
})

// Affichage confiance en pourcentage (backend renvoie 0..1)
const displayConfidence = computed(() => {
// Summary formatted time
const summaryFormattedTime = computed(() => {
  const m = String(Math.floor(summarySeconds.value / 60)).padStart(2, '0')
  const s = String(summarySeconds.value % 60).padStart(2, '0')
  return `${m}:${s}`
})
  const c = Number(analysisResult.value?.confidence ?? 0)
  if (Number.isNaN(c)) return 0
  return Math.round(Math.max(0, Math.min(1, c)) * 100)
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
  // Recompute expected structure for highlighting
  computeExpectedStructure()
  // Pré-remplir la zone source pour le résumé avec le paragraphe courant (ou combiner plusieurs)
  summarySourceText.value = currentText.value.join('. ').trim()
}

const startRecording = async () => {
  try {
    hasRecording.value = false
    analysisResult.value = null
    audioBlob.value = null

    // Acquire microphone
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 44100
      }
    })
    //const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

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
    rawResponse.value = data
    analysisResult.value = {
      transcription: data?.transcription || '',
      confidence: data?.confidence ?? 0,
      errors: data?.errors || [],
      prosody: data?.prosody || { rhythm: { regularity: 0 }, intonation: { monotone: false }, tempo: 0 },
      alignment: data?.alignment || {}
    }
    
    // Utiliser les ops d'alignement comme source de vérité principale
    buildWordClassificationFromAlignment()

    // Build correct and pronounced words sets
    updateWordSets()

  // Recompute expected structure after analysis
  computeExpectedStructure()

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
  if (!currentText.value.length) {
    ElMessage.warning('Aucun texte à synthétiser')
    return
  }
  try {
    loadingAudio.value = true
    const text = currentText.value.join('. ').trim()
    if (!text) {
      ElMessage.warning('Texte vide')
      loadingAudio.value = false
      return
    }
    ElMessage.info('Génération audio…')
    const lang = analysisResult.value?.prosody?.language || 'fr'
    const { data } = await ttsService.generateSpeech(text, lang, false)
    const url = data?.audio_url
    if (!url) {
      throw new Error('URL audio manquante dans la réponse')
    }
    // Utiliser le même proxy /api si nécessaire
    const finalUrl = url.startsWith('http') ? url : `/api${url}`
    if (audioPlayer.value) {
      audioPlayer.value.src = finalUrl
      await audioPlayer.value.play().catch(() => { /* autoplay blocked */ })
    }
    loadingAudio.value = false
    ElMessage.success('Lecture du modèle prête')
  } catch (error) {
    console.error(error)
    ElMessage.error("Échec génération TTS")
    loadingAudio.value = false
  }
}

// --- Summary Recording Logic ---
const startSummaryRecording = async () => {
  try {
    summaryResult.value = null
    hasSummaryRecording.value = false
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    summaryStream.value = stream
    const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : 'audio/webm'
    summaryMediaRecorder.value = new MediaRecorder(stream, { mimeType })
    summaryChunks.value = []
    summaryMediaRecorder.value.ondataavailable = e => { if (e.data && e.data.size) summaryChunks.value.push(e.data) }
    summaryMediaRecorder.value.onstop = () => {
      const blob = new Blob(summaryChunks.value, { type: mimeType })
      summaryAudioBlob.value = blob
      hasSummaryRecording.value = true
    }
    summaryMediaRecorder.value.start()
    isSummaryRecording.value = true
    summarySeconds.value = 0
    if (summaryTimer) clearInterval(summaryTimer)
    summaryTimer = setInterval(() => { summarySeconds.value += 1 }, 1000)
    // Simple VU (best-effort)
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)()
      const src = audioCtx.createMediaStreamSource(stream)
      const analyser = audioCtx.createAnalyser()
      analyser.fftSize = 512
      src.connect(analyser)
      const data = new Uint8Array(analyser.fftSize)
      const loop = () => {
        if (!isSummaryRecording.value) return
        analyser.getByteTimeDomainData(data)
        let sum = 0
        for (let i=0;i<data.length;i++) { const v=(data[i]-128)/128; sum+=v*v }
        const rms = Math.sqrt(sum/data.length)
        summaryVuLevel.value = Math.min(100, Math.round(rms*140))
        requestAnimationFrame(loop)
      }
      loop()
    } catch(_){}
  } catch (e) {
    ElMessage.error('Micro indisponible (résumé)')
  }
}

const stopSummaryRecording = () => {
  if (!summaryMediaRecorder.value || !isSummaryRecording.value) return
  try {
    isSummaryRecording.value = false
    const p = new Promise(res => {
      const h = () => { summaryMediaRecorder.value.removeEventListener('stop', h); res() }
      summaryMediaRecorder.value.addEventListener('stop', h)
    })
    summaryMediaRecorder.value.stop()
    if (summaryStream.value) {
      summaryStream.value.getTracks().forEach(t=>t.stop())
      summaryStream.value = null
    }
    if (summaryTimer) { clearInterval(summaryTimer); summaryTimer = null }
    return p
  } catch { /* noop */ }
}

const evaluateSummary = async () => {
  if (!summaryAudioBlob.value) { ElMessage.warning('Aucun enregistrement de résumé'); return }
  try {
    summaryAnalyzing.value = true
    const form = new FormData()
    form.append('audio_file', summaryAudioBlob.value, 'summary.webm')
    form.append('source_text', summarySourceText.value || '')
    const { data } = await summaryService.evaluateSummary(form)
    summaryResult.value = data
    ElMessage.success('Résumé évalué')
  } catch (e) {
    console.error(e)
    ElMessage.error('Erreur évaluation résumé')
  } finally {
    summaryAnalyzing.value = false
  }
}

const llmEvaluateSummary = async () => {
  try {
    summaryAnalyzing.value = true
    const text = summaryResult.value?.transcription || summarySourceText.value
    const { data } = await summaryService.llmEvaluateSummary(text)
    // Fusionner suggestions / transitions si différent
    summaryResult.value = {
      ...data,
      transcription: data.transcription || text
    }
    ElMessage.success('Analyse LLM terminée')
  } catch (e) {
    console.error(e)
    ElMessage.error('Erreur LLM')
  } finally {
    summaryAnalyzing.value = false
  }
}

const getSentenceClass = (index) => {
  if (!analysisResult.value) return ''
  
  // Simulation de la mise en évidence des erreurs
  const sentence = currentText.value[index] || ''
  const words = sentence.split(/\s+/)
  const hasErr = words.some(w => {
    const norm = normalizeToken(w)
    return errorWords.value.has(norm)
  })
  return {
    'error-sentence': hasErr
  }
}

const updateWordSets = () => {
  if (!analysisResult.value) return

  const expectedText = currentText.value.join('. ').trim()
  const transcription = analysisResult.value.transcription || ''
  
  // Normaliser les mots du texte attendu
  const expectedWords = expectedText.split(/\s+/).map(normalizeToken).filter(w => w.length > 0)
  
  // Normaliser les mots de la transcription
  const transcribedWords = transcription.split(/\s+/).map(normalizeToken).filter(w => w.length > 0)
  
  // Mots prononcés (dans la transcription)
  pronouncedWords.value = new Set(transcribedWords)
  
  // Si on n'a pas d'alignment ops, utiliser la logique de fallback
  if (!analysisResult.value.alignment?.ops) {
    // Logique simplifiée : privilégier les mots corrects
    const correctSet = new Set()
    const similarSet = new Set()
    
    for (const word of expectedWords) {
      if (errorWords.value.has(word)) {
        // Mot explicitement marqué comme erreur → reste rouge
        continue
      } else if (pronouncedWords.value.has(word)) {
        // Mot présent dans la transcription et pas d'erreur → vert
        correctSet.add(word)
      } else {
        // Mot absent, vérifier similarité → jaune potentiel
        const similarWord = findSimilarWord(word, transcribedWords)
        if (similarWord) {
          similarSet.add(word)
        }
      }
    }
    
    // Analyser les erreurs pour détecter les mots similaires (jaunes)
    const errors = analysisResult.value.errors || []
    for (const error of errors) {
      if (error.type === 'mispronunciation' && error.word && error.expected) {
        const expected = String(error.expected).toLowerCase()
        const pronounced = String(error.word).toLowerCase()
        const similarity = calculateSimilarity(pronounced, expected)
        
        if (similarity >= 0.3 && similarity < 0.9) { 
          // Similarité moyenne → jaune
          similarSet.add(expected)
          // Retirer des erreurs car c'est un effort valable
          errorWords.value.delete(expected)
        } else if (similarity >= 0.9) {
          // Très similaire → considérer comme correct
          correctSet.add(expected)
          errorWords.value.delete(expected)
        }
        // Si similarity < 0.3, reste rouge (vraie erreur)
      }
    }
    
    correctWords.value = correctSet
    similarWords.value = similarSet
  }
  // Si on a des alignment ops, la classification est déjà faite par buildWordClassificationFromAlignment
}

// Nouvelle fonction utilisant les ops d'alignement comme source de vérité
// helpers de normalisation (insensible aux accents)
const stripDiacritics = (s) => s.normalize('NFD').replace(/\p{M}+/gu, '')
const normalizeToken = (s) => stripDiacritics(String(s || '').toLowerCase()).replace(/[^\p{L}\p{N}'-]/gu, '')

const buildWordClassificationFromAlignment = () => {
  if (!analysisResult.value?.alignment?.ops) return
  
  const correctSet = new Set()
  const similarSet = new Set()
  const errorSet = new Set()
  const map = new Map()
  
  const ops = analysisResult.value.alignment.ops || []
  const expectedWords = Array.isArray(analysisResult.value.alignment.expected_words)
    ? analysisResult.value.alignment.expected_words
    : []
  tokenStatus.value = Array(expectedWords.length).fill('neutral')
  tokenTooltip.value = Array(expectedWords.length).fill('')
  
  for (const op of ops) {
    if (op.op === 'match') {
      // Match parfait → VERT
      const word = normalizeToken(op.exp)
      if (word) correctSet.add(word)
      if (typeof op.j === 'number') tokenStatus.value[op.j] = 'correct'
    } else if (op.op === 'sub') {
      // Substitution → vérifier similarité
      const expected = normalizeToken(op.exp)
      const pronounced = normalizeToken(op.trans)
      if (expected && pronounced) {
        // Utiliser le score renvoyé par le backend si présent
        const similarity = typeof op.sim === 'number' ? op.sim : calculateSimilarity(pronounced, expected)
        if (similarity >= 0.85) {
          // très proche → considérer correct pour ne pas pénaliser les variantes
          correctSet.add(expected)
          if (typeof op.j === 'number') tokenStatus.value[op.j] = 'correct'
        } else if (similarity >= 0.6) {
          // Similarité élevée → JAUNE
          similarSet.add(expected)
          if (!map.has(expected)) map.set(expected, [])
          map.get(expected).push({
            type: 'near_miss',
            word: pronounced,
            expected,
            severity: 'low',
            similarity: Math.round(similarity * 100) / 100
          })
          if (typeof op.j === 'number') {
            tokenStatus.value[op.j] = 'similar'
            tokenTooltip.value[op.j] = `Presque correct: ${pronounced} → ${expected} (sim=${Math.round(similarity*100)/100})`
          }
        } else {
          // Vraie erreur → ROUGE
          errorSet.add(expected)
          if (!map.has(expected)) map.set(expected, [])
          map.get(expected).push({
            type: 'mispronunciation',
            word: pronounced,
            expected: expected,
            severity: 'medium'
          })
          if (typeof op.j === 'number') {
            tokenStatus.value[op.j] = 'error'
            tokenTooltip.value[op.j] = `Mal prononcé: ${pronounced} → ${expected}`
          }
        }
      }
    } else if (op.op === 'del') {
      // Deletion (mot dans transcription pas dans attendu) → ignorer pour le surlignage
    } else if (op.op === 'ins') {
      // Insertion (mot attendu manqué) → ROUGE
      const word = normalizeToken(op.exp)
      if (word) {
        errorSet.add(word)
        if (!map.has(word)) map.set(word, [])
        map.get(word).push({
          type: 'deletion',
          expected: word,
          severity: 'high'
        })
        if (typeof op.j === 'number') {
          tokenStatus.value[op.j] = 'error'
          tokenTooltip.value[op.j] = `Mot manqué: ${word}`
        }
      }
    }
  }
  
  correctWords.value = correctSet
  similarWords.value = similarSet  
  errorWords.value = errorSet
  errorWordMap.value = map
}

// Recompute expected tokenization and sentence ranges for position-aware mapping
const computeExpectedStructure = () => {
  const ranges = []
  let cursor = 0

  // If we have alignment expected_words, use them as the single source of truth
  const alignedExpected = Array.isArray(analysisResult.value?.alignment?.expected_words)
    ? analysisResult.value.alignment.expected_words.map(normalizeToken).filter(Boolean)
    : null

  if (alignedExpected && alignedExpected.length > 0) {
    const total = alignedExpected.length
    const sentences = currentText.value
    for (let idx = 0; idx < sentences.length; idx++) {
      const sentence = sentences[idx]
      const countInSentence = sentence.split(/\s+/).map(normalizeToken).filter(w => w.length > 0).length
      // Clamp to remaining tokens if needed
      const remaining = Math.max(0, total - cursor)
      const take = idx === sentences.length - 1 ? remaining : Math.min(countInSentence, remaining)
      const start = cursor
      const end = start + take
      ranges.push([start, end])
      cursor = end
    }
    // If there are still tokens unassigned (e.g., punctuation/tokenization differences), extend the last range
    if (cursor < total && ranges.length > 0) {
      ranges[ranges.length - 1][1] = total
      cursor = total
    }
    expectedNormTokens.value = alignedExpected
    sentenceTokenRanges.value = ranges
    return
  }

  // Fallback to computing from displayed text when no alignment yet
  const normTokens = []
  cursor = 0
  for (const sentence of currentText.value) {
    const tokens = sentence.split(/\s+/).map(normalizeToken).filter(w => w.length > 0)
    const start = cursor
    const end = start + tokens.length
    ranges.push([start, end])
    normTokens.push(...tokens)
    cursor = end
  }
  expectedNormTokens.value = normTokens
  sentenceTokenRanges.value = ranges
}

// Fonction de calcul de similarité (distance de Levenshtein normalisée)
const calculateSimilarity = (word1, word2) => {
  if (!word1 || !word2) return 0
  
  const len1 = word1.length
  const len2 = word2.length
  
  if (len1 === 0) return len2 === 0 ? 1 : 0
  if (len2 === 0) return 0
  
  // Matrice de distance de Levenshtein
  const matrix = Array(len1 + 1).fill(null).map(() => Array(len2 + 1).fill(null))
  
  for (let i = 0; i <= len1; i++) matrix[i][0] = i
  for (let j = 0; j <= len2; j++) matrix[0][j] = j
  
  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = word1[i - 1] === word2[j - 1] ? 0 : 1
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,     // deletion
        matrix[i][j - 1] + 1,     // insertion
        matrix[i - 1][j - 1] + cost // substitution
      )
    }
  }
  
  const distance = matrix[len1][len2]
  const maxLen = Math.max(len1, len2)
  
  return 1 - (distance / maxLen) // Normaliser entre 0 et 1
}

// Trouver un mot similaire dans la liste des mots transcrits
const findSimilarWord = (expectedWord, transcribedWords) => {
  let bestMatch = null
  let bestSimilarity = 0
  
  for (const transcribedWord of transcribedWords) {
    const similarity = calculateSimilarity(expectedWord, transcribedWord)
    if (similarity > bestSimilarity && similarity > 0.5) { // Seuil minimum de 50%
      bestSimilarity = similarity
      bestMatch = transcribedWord
    }
  }
  
  return bestMatch
}

const getWordClass = (part) => {
  if (!part.text.trim()) return '' // Espaces
  
  const normalized = normalizeToken(part.text)
  if (!normalized) return ''
  
  const classes = ['word']
  
  if (analysisResult.value && part.status) {
    if (part.status === 'error') classes.push('word-error')
    else if (part.status === 'similar') classes.push('word-similar')
    else if (part.status === 'correct') classes.push('word-correct')
  } else if (analysisResult.value) {
    if (errorWords.value.has(normalized)) {
      classes.push('word-error') // Rouge
    } else if (similarWords.value.has(normalized)) {
      classes.push('word-similar') // Jaune
    } else if (correctWords.value.has(normalized)) {
      classes.push('word-correct') // Vert
    }
    // Sinon, pas de classe spéciale (couleur normale pour non-prononcé)
  }
  
  return classes.join(' ')
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
  errorWords.value.clear()
  errorWordMap.value.clear()
  correctWords.value.clear()
  pronouncedWords.value.clear()
  similarWords.value.clear()
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
      const errs = saved.analysis?.errors || []
      // ignorer les quasi-corrects
      const realErrs = errs.filter(e => !['near_miss'].includes(String(e.type)))
      errorWords.value = new Set(realErrs.map(e => normalizeToken((e.word ?? e.expected) || '')))
      const map = new Map()
      for (const e of realErrs) {
        const key = normalizeToken((e.word ?? e.expected) || '')
        if (!key) continue
        if (!map.has(key)) map.set(key, [])
        map.get(key).push(e)
      }
      errorWordMap.value = map
      
      // Reconstruire la classification à partir des ops si présents
      if (analysisResult.value?.alignment?.ops) {
        buildWordClassificationFromAlignment()
      } else {
        updateWordSets()
      }
      
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
  if (summaryStream.value) {
    summaryStream.value.getTracks().forEach(t => t.stop())
  }
})

// Formatting helpers
const formattedTime = computed(() => {
  const m = String(Math.floor(recordSeconds.value / 60)).padStart(2, '0')
  const s = String(recordSeconds.value % 60).padStart(2, '0')
  return `${m}:${s}`
})

const tokenizeSentence = (sentence, sentenceIndex) => {
  const parts = []
  const tokens = sentence.split(/(\s+)/)
  const range = sentenceTokenRanges.value[sentenceIndex] || [0, 0]
  let ptr = range[0]
  for (const tok of tokens) {
    if (tok.trim().length === 0) {
      parts.push({ text: tok })
      continue
    }
    const normalized = normalizeToken(tok)
    let status, tooltip = ''
    if (normalized) {
      const j = ptr
      status = tokenStatus.value[j]
      tooltip = tokenTooltip.value[j] || ''
      if (ptr < range[1]) ptr += 1
    }
    // Fallback tooltip via errorWordMap si pas de tooltip positionnel
    if (!tooltip && errorWordMap.value.has(normalized)) {
      const errs = errorWordMap.value.get(normalized) || []
      const lines = errs.map(e => {
        if (e.type === 'deletion') return `Mot manqué: ${e.expected || e.word}`
        if (e.type === 'mispronunciation') return `Mal prononcé: ${e.word} → Attendu: ${e.expected}`
        if (e.type === 'substitution_or_skip') return `Substitution/écart: ${e.word}`
        if (e.type === 'near_miss') return `Presque correct: ${e.word} → ${e.expected}`
        return `${e.type}: ${e.word || ''}`
      })
      tooltip = lines.join('\n')
    }
    parts.push({ text: tok, status, tooltip })
  }
  return parts
}

// Raw JSON pretty
const rawResponsePretty = computed(() => {
  try { return JSON.stringify(rawResponse.value ?? {}, null, 2) } catch { return '{}' }
})
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

.word {
  transition: all 0.3s ease;
}

.word-error {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
}

.word-correct {
  background-color: #f0f9ff;
  color: #67c23a;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
}

.word-similar {
  background-color: #fefce8;
  color: #eab308;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
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
