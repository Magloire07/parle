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
                {{ sentence }}
              </p>
            </div>
          </div>

          <!-- Recording Controls -->
          <div class="recording-section">
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
import { ref, onMounted, computed } from 'vue'
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
    isRecording.value = true
    hasRecording.value = false
    analysisResult.value = null
    
    // Simulation de l'enregistrement
    ElMessage.info('Enregistrement en cours...')
    
    // Ici, vous intégreriez l'API d'enregistrement réel
    setTimeout(() => {
      stopRecording()
    }, 3000)
    
  } catch (error) {
    ElMessage.error('Erreur lors du démarrage de l\'enregistrement')
    isRecording.value = false
  }
}

const stopRecording = () => {
  isRecording.value = false
  hasRecording.value = true
  ElMessage.success('Enregistrement terminé')
}

const analyzeRecording = async () => {
  try {
    analyzing.value = true
    
    // Simulation de l'analyse
    const mockResult = {
      transcription: "Ceci est un exemple de transcription simulée",
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
    
    // Simuler un délai d'analyse
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    analysisResult.value = mockResult
    ElMessage.success('Analyse terminée')
    
  } catch (error) {
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
  return {
    'error-sentence': index === 1, // Simuler une erreur sur la deuxième phrase
    'correct-sentence': index !== 1
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
