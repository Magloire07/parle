<template>
  <div class="summary">
    <el-row :gutter="20" justify="center">
      <el-col :span="24" :md="20" :lg="16">
        <el-card class="summary-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h2>Mode Résumé</h2>
              <p>Résumez oralement les deux paragraphes précédents</p>
            </div>
          </template>

          <!-- Source Text -->
          <div class="source-text-section">
            <h3>Texte Source</h3>
            <div class="source-content">
              <p v-for="(paragraph, index) in sourceText" :key="index">
                <strong>Paragraphe {{ index + 1 }}:</strong> {{ paragraph }}
              </p>
            </div>
          </div>

          <!-- Recording Section -->
          <div class="recording-section">
            <h3>Enregistrement du Résumé</h3>
            <p class="instruction-text">
              Résumez en vos propres mots le contenu des paragraphes ci-dessus. 
              Parlez clairement et utilisez des mots de liaison.
            </p>
            
            <div class="recording-controls">
              <el-button 
                v-if="!isRecording" 
                type="primary" 
                size="large" 
                @click="startRecording"
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
                @click="evaluateSummary"
                :loading="evaluating"
              >
                <el-icon><Search /></el-icon>
                Évaluer le Résumé
              </el-button>
            </div>

            <!-- Recording Status -->
            <div v-if="isRecording" class="recording-status">
              <el-icon class="recording-icon"><Microphone /></el-icon>
              <span>Enregistrement en cours...</span>
            </div>
          </div>

          <!-- Evaluation Results -->
          <div v-if="evaluationResult" class="evaluation-section">
            <el-divider>Résultats de l'Évaluation</el-divider>
            
            <!-- Scores -->
            <div class="scores-section">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-card class="score-card">
                    <div class="score-content">
                      <div class="score-number">{{ Math.round(evaluationResult.relevance_score * 100) }}%</div>
                      <div class="score-label">Pertinence</div>
                    </div>
                  </el-card>
                </el-col>
                <el-col :span="12">
                  <el-card class="score-card">
                    <div class="score-content">
                      <div class="score-number">{{ Math.round(evaluationResult.quality_score * 100) }}%</div>
                      <div class="score-label">Qualité</div>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>

            <!-- Transcription -->
            <div class="transcription-section">
              <h4>Transcription de votre résumé :</h4>
              <div class="transcription-content">
                {{ evaluationResult.transcription }}
              </div>
            </div>

            <!-- Suggestions -->
            <div class="suggestions-section">
              <h4>Suggestions d'Amélioration :</h4>
              <ul class="suggestions-list">
                <li v-for="(suggestion, index) in evaluationResult.suggestions" :key="index">
                  <el-icon><InfoFilled /></el-icon>
                  {{ suggestion }}
                </li>
              </ul>
            </div>

            <!-- Transitions -->
            <div class="transitions-section">
              <h4>Mots de Liaison Suggérés :</h4>
              <div class="transitions-tags">
                <el-tag 
                  v-for="transition in evaluationResult.transitions" 
                  :key="transition"
                  class="transition-tag"
                >
                  {{ transition }}
                </el-tag>
              </div>
            </div>

            <!-- Errors -->
            <div v-if="evaluationResult.errors.length" class="errors-section">
              <h4>Erreurs Détectées :</h4>
              <ul class="errors-list">
                <li v-for="error in evaluationResult.errors" :key="error.word">
                  <el-tag :type="getErrorType(error.severity)">
                    {{ error.word }}
                  </el-tag>
                  - {{ error.type }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Example Summaries -->
          <div class="examples-section">
            <h3>Exemples de Résumés</h3>
            <el-collapse v-model="activeExamples">
              <el-collapse-item title="Résumé Court" name="short">
                <p>{{ exampleSummaries.short }}</p>
              </el-collapse-item>
              <el-collapse-item title="Résumé Moyen" name="medium">
                <p>{{ exampleSummaries.medium }}</p>
              </el-collapse-item>
              <el-collapse-item title="Résumé Long" name="long">
                <p>{{ exampleSummaries.long }}</p>
              </el-collapse-item>
            </el-collapse>
          </div>

          <!-- Navigation -->
          <div class="navigation-section">
            <el-button @click="goBack">
              <el-icon><ArrowLeft /></el-icon>
              Retour à la Lecture
            </el-button>
            
            <el-button 
              @click="continueReading" 
              type="primary"
            >
              Continuer la Lecture
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Microphone, 
  VideoPause, 
  Search, 
  ArrowLeft, 
  ArrowRight,
  InfoFilled
} from '@element-plus/icons-vue'
import { summaryService } from '@/services/api'

const route = useRoute()
const router = useRouter()

// Reactive data
const sourceText = ref([])
const isRecording = ref(false)
const hasRecording = ref(false)
const evaluating = ref(false)
const evaluationResult = ref(null)
const activeExamples = ref([])
const exampleSummaries = ref({
  short: "Résumé court simulé du texte source",
  medium: "Résumé moyen simulé avec plus de détails et d'analyse",
  long: "Résumé long simulé avec tous les éléments importants et des transitions fluides"
})

// Methods
const loadSourceText = () => {
  // Charger le texte source depuis localStorage ou l'API
  const savedText = localStorage.getItem('currentText')
  if (savedText) {
    const textData = JSON.parse(savedText)
    // Prendre les deux derniers paragraphes
    sourceText.value = textData.paragraphs.slice(-2)
  } else {
    // Texte de démonstration
    sourceText.value = [
      "Ceci est le premier paragraphe du texte source qui contient les informations principales.",
      "Ceci est le deuxième paragraphe qui complète les informations du premier paragraphe."
    ]
  }
}

const startRecording = async () => {
  try {
    isRecording.value = true
    hasRecording.value = false
    evaluationResult.value = null
    
    ElMessage.info('Enregistrement du résumé en cours...')
    
    // Simulation de l'enregistrement
    setTimeout(() => {
      stopRecording()
    }, 5000)
    
  } catch (error) {
    ElMessage.error('Erreur lors du démarrage de l\'enregistrement')
    isRecording.value = false
  }
}

const stopRecording = () => {
  isRecording.value = false
  hasRecording.value = true
  ElMessage.success('Enregistrement du résumé terminé')
}

const evaluateSummary = async () => {
  try {
    evaluating.value = true
    
    // Simulation de l'évaluation
    const mockResult = {
      transcription: "Ceci est un résumé simulé des deux paragraphes précédents qui démontre la compréhension du contenu.",
      relevance_score: 0.85,
      quality_score: 0.78,
      suggestions: [
        "Utilisez plus de mots de liaison pour améliorer la fluidité",
        "Ajoutez des détails spécifiques du texte source",
        "Structurez mieux votre résumé avec une introduction et une conclusion"
      ],
      transitions: ["Cependant", "De plus", "En conclusion", "Par ailleurs", "En outre"],
      errors: [
        { word: "démontre", type: "prononciation", severity: "low" }
      ]
    }
    
    // Simuler un délai d'évaluation
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    evaluationResult.value = mockResult
    ElMessage.success('Évaluation terminée')
    
  } catch (error) {
    ElMessage.error('Erreur lors de l\'évaluation')
  } finally {
    evaluating.value = false
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

const goBack = () => {
  router.go(-1)
}

const continueReading = () => {
  router.push({
    name: 'Reading',
    params: { textId: route.params.textId }
  })
}

// Lifecycle
onMounted(() => {
  loadSourceText()
})
</script>

<style scoped>
.summary {
  max-width: 1200px;
  margin: 0 auto;
}

.summary-card {
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

.source-text-section {
  margin: 30px 0;
}

.source-text-section h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.source-content {
  background-color: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  border-left: 4px solid #67C23A;
}

.source-content p {
  margin-bottom: 15px;
  line-height: 1.8;
  color: #333;
}

.recording-section {
  margin: 30px 0;
  text-align: center;
}

.recording-section h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.instruction-text {
  color: #666;
  margin-bottom: 25px;
  font-style: italic;
}

.recording-controls .el-button {
  margin: 0 10px;
}

.recording-status {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  color: #E6A23C;
  font-weight: 500;
}

.recording-icon {
  margin-right: 8px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.evaluation-section {
  margin: 30px 0;
}

.scores-section {
  margin: 20px 0;
}

.score-card {
  text-align: center;
}

.score-content {
  padding: 20px;
}

.score-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.score-label {
  color: #666;
  font-size: 1.1rem;
}

.transcription-section {
  margin: 25px 0;
}

.transcription-section h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.transcription-content {
  background-color: #f0f9ff;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
  font-style: italic;
  line-height: 1.6;
}

.suggestions-section {
  margin: 25px 0;
}

.suggestions-section h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.suggestions-list {
  list-style: none;
  padding: 0;
}

.suggestions-list li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f9ff;
  border-radius: 6px;
  color: #666;
}

.suggestions-list .el-icon {
  margin-right: 10px;
  color: #409EFF;
}

.transitions-section {
  margin: 25px 0;
}

.transitions-section h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.transitions-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.transition-tag {
  margin: 0;
}

.errors-section {
  margin: 25px 0;
}

.errors-section h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.errors-list {
  list-style: none;
  padding: 0;
}

.errors-list li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.examples-section {
  margin: 30px 0;
}

.examples-section h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.navigation-section {
  text-align: center;
  margin: 30px 0;
}

.navigation-section .el-button {
  margin: 0 10px;
}

@media (max-width: 768px) {
  .recording-controls .el-button,
  .navigation-section .el-button {
    display: block;
    width: 100%;
    margin: 10px 0;
  }
  
  .transitions-tags {
    justify-content: center;
  }
}
</style>
