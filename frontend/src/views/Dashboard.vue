<template>
  <div class="dashboard">
    <el-row :gutter="20" justify="center">
      <el-col :span="24" :md="22" :lg="20">
        <el-card class="dashboard-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h2>Tableau de Bord</h2>
              <p>Suivez vos progrès et vos statistiques d'apprentissage</p>
            </div>
          </template>

          <!-- Stats Overview -->
          <div class="stats-overview">
            <el-row :gutter="20">
              <el-col :span="24" :md="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="40" color="#409EFF"><Document /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.totalTexts }}</div>
                      <div class="stat-label">Textes Lus</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="24" :md="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="40" color="#67C23A"><Microphone /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.totalReadings }}</div>
                      <div class="stat-label">Sessions de Lecture</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="24" :md="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="40" color="#E6A23C"><ChatDotRound /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.totalSummaries }}</div>
                      <div class="stat-label">Résumés Oraux</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="24" :md="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="40" color="#F56C6C"><Trophy /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ Math.round(stats.averageConfidence) }}%</div>
                      <div class="stat-label">Confiance Moyenne</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <!-- Progress Charts -->
          <div class="charts-section">
            <el-row :gutter="20">
              <el-col :span="24" :lg="12">
                <el-card class="chart-card">
                  <template #header>
                    <h3>Progrès Hebdomadaire</h3>
                  </template>
                  <div class="chart-container">
                    <div class="chart-placeholder">
                      <el-icon size="60" color="#ddd"><TrendCharts /></el-icon>
                      <p>Graphique de progression</p>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="24" :lg="12">
                <el-card class="chart-card">
                  <template #header>
                    <h3>Répartition des Erreurs</h3>
                  </template>
                  <div class="chart-container">
                    <div class="chart-placeholder">
                      <el-icon size="60" color="#ddd"><PieChart /></el-icon>
                      <p>Graphique des erreurs</p>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <!-- Recent Activity -->
          <div class="activity-section">
            <el-card class="activity-card">
              <template #header>
                <h3>Activité Récente</h3>
              </template>
              
              <el-timeline>
                <el-timeline-item
                  v-for="activity in recentActivities"
                  :key="activity.id"
                  :timestamp="activity.timestamp"
                  :type="activity.type"
                >
                  <el-card>
                    <h4>{{ activity.title }}</h4>
                    <p>{{ activity.description }}</p>
                    <div class="activity-meta">
                      <el-tag :type="getActivityTagType(activity.status)">
                        {{ activity.status }}
                      </el-tag>
                      <span class="activity-score" v-if="activity.score">
                        Score: {{ activity.score }}%
                      </span>
                    </div>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </div>

          <!-- Improvement Areas -->
          <div class="improvement-section">
            <el-card class="improvement-card">
              <template #header>
                <h3>Domaines d'Amélioration</h3>
              </template>
              
              <div class="improvement-list">
                <div 
                  v-for="area in improvementAreas" 
                  :key="area.name"
                  class="improvement-item"
                >
                  <div class="improvement-header">
                    <h4>{{ area.name }}</h4>
                    <el-progress 
                      :percentage="area.progress" 
                      :status="getProgressStatus(area.progress)"
                      :stroke-width="8"
                    />
                  </div>
                  <p class="improvement-description">{{ area.description }}</p>
                  <div class="improvement-suggestions">
                    <h5>Suggestions :</h5>
                    <ul>
                      <li v-for="suggestion in area.suggestions" :key="suggestion">
                        {{ suggestion }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </el-card>
          </div>

          <!-- Achievements -->
          <div class="achievements-section">
            <el-card class="achievements-card">
              <template #header>
                <h3>Réalisations</h3>
              </template>
              
              <div class="achievements-grid">
                <div 
                  v-for="achievement in achievements" 
                  :key="achievement.id"
                  class="achievement-item"
                  :class="{ 'unlocked': achievement.unlocked }"
                >
                  <div class="achievement-icon">
                    <el-icon size="40" :color="achievement.unlocked ? '#E6A23C' : '#ddd'">
                      <Trophy />
                    </el-icon>
                  </div>
                  <div class="achievement-info">
                    <h4>{{ achievement.name }}</h4>
                    <p>{{ achievement.description }}</p>
                    <el-tag 
                      :type="achievement.unlocked ? 'success' : 'info'"
                      size="small"
                    >
                      {{ achievement.unlocked ? 'Débloqué' : 'Verrouillé' }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-card>
          </div>

          <!-- Quick Actions -->
          <div class="actions-section">
            <el-card class="actions-card">
              <template #header>
                <h3>Actions Rapides</h3>
              </template>
              
              <div class="actions-grid">
                <el-button 
                  type="primary" 
                  size="large"
                  @click="$router.push('/upload')"
                >
                  <el-icon><Upload /></el-icon>
                  Nouveau Document
                </el-button>
                
                <el-button 
                  type="success" 
                  size="large"
                  @click="exportProgress"
                >
                  <el-icon><Download /></el-icon>
                  Exporter Progrès
                </el-button>
                
                <el-button 
                  type="info" 
                  size="large"
                  @click="viewHistory"
                >
                  <el-icon><Clock /></el-icon>
                  Historique Complet
                </el-button>
                
                <el-button 
                  type="warning" 
                  size="large"
                  @click="settings"
                >
                  <el-icon><Setting /></el-icon>
                  Paramètres
                </el-button>
              </div>
            </el-card>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Document, 
  Microphone, 
  ChatDotRound, 
  Trophy, 
  TrendCharts, 
  PieChart,
  Upload,
  Download,
  Clock,
  Setting
} from '@element-plus/icons-vue'

// Reactive data
const stats = ref({
  totalTexts: 12,
  totalReadings: 45,
  totalSummaries: 23,
  averageConfidence: 78.5
})

const recentActivities = ref([
  {
    id: 1,
    title: "Lecture terminée",
    description: "Texte sur l'écologie - Paragraphes 1-3",
    timestamp: "Il y a 2 heures",
    type: "success",
    status: "Terminé",
    score: 85
  },
  {
    id: 2,
    title: "Résumé évalué",
    description: "Résumé oral du chapitre 2",
    timestamp: "Il y a 1 jour",
    type: "primary",
    status: "Évalué",
    score: 72
  },
  {
    id: 3,
    title: "Nouveau document",
    description: "Article de presse scanné",
    timestamp: "Il y a 2 jours",
    type: "info",
    status: "Ajouté"
  }
])

const improvementAreas = ref([
  {
    name: "Prononciation",
    progress: 75,
    description: "Amélioration de la clarté de la prononciation",
    suggestions: [
      "Pratiquez les sons difficiles",
      "Parlez plus lentement",
      "Écoutez les modèles audio"
    ]
  },
  {
    name: "Intonation",
    progress: 60,
    description: "Variation de la hauteur de voix",
    suggestions: [
      "Écoutez des podcasts",
      "Pratiquez les questions et exclamations",
      "Utilisez des marqueurs d'intonation"
    ]
  },
  {
    name: "Rythme",
    progress: 80,
    description: "Fluidité et régularité du débit",
    suggestions: [
      "Pratiquez avec un métronome",
      "Faites des pauses naturelles",
      "Lisez à voix haute régulièrement"
    ]
  }
])

const achievements = ref([
  {
    id: 1,
    name: "Premier Pas",
    description: "Complétez votre première lecture",
    unlocked: true
  },
  {
    id: 2,
    name: "Lecteur Assidu",
    description: "Lisez 10 textes",
    unlocked: true
  },
  {
    id: 3,
    name: "Maître de la Prononciation",
    description: "Atteignez 90% de confiance",
    unlocked: false
  },
  {
    id: 4,
    name: "Orateur Confirmé",
    description: "Complétez 50 sessions",
    unlocked: false
  }
])

// Methods
const getActivityTagType = (status) => {
  switch (status) {
    case 'Terminé': return 'success'
    case 'Évalué': return 'primary'
    case 'Ajouté': return 'info'
    default: return 'info'
  }
}

const getProgressStatus = (progress) => {
  if (progress >= 80) return 'success'
  if (progress >= 60) return 'warning'
  return 'exception'
}

const exportProgress = () => {
  ElMessage.success('Export des progrès en cours...')
  // Ici, vous implémenteriez l'export des données
}

const viewHistory = () => {
  ElMessage.info('Ouverture de l\'historique...')
  // Ici, vous implémenteriez la navigation vers l'historique
}

const settings = () => {
  ElMessage.info('Ouverture des paramètres...')
  // Ici, vous implémenteriez la navigation vers les paramètres
}

// Lifecycle
onMounted(() => {
  // Charger les données du tableau de bord
  console.log('Tableau de bord chargé')
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-card {
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

.stats-overview {
  margin: 30px 0;
}

.stat-card {
  height: 100%;
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  margin-right: 20px;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 1rem;
}

.charts-section {
  margin: 30px 0;
}

.chart-card {
  height: 100%;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #999;
}

.chart-placeholder p {
  margin-top: 10px;
  font-size: 1.1rem;
}

.activity-section {
  margin: 30px 0;
}

.activity-card h3 {
  color: #2c3e50;
  margin: 0;
}

.activity-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.activity-score {
  color: #666;
  font-weight: 500;
}

.improvement-section {
  margin: 30px 0;
}

.improvement-card h3 {
  color: #2c3e50;
  margin: 0;
}

.improvement-item {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.improvement-header {
  margin-bottom: 15px;
}

.improvement-header h4 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.improvement-description {
  color: #666;
  margin-bottom: 15px;
}

.improvement-suggestions h5 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.improvement-suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.improvement-suggestions li {
  color: #666;
  margin-bottom: 5px;
}

.achievements-section {
  margin: 30px 0;
}

.achievements-card h3 {
  color: #2c3e50;
  margin: 0;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-item {
  display: flex;
  align-items: center;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.achievement-item.unlocked {
  border-color: #E6A23C;
  background-color: #fdf6ec;
}

.achievement-icon {
  margin-right: 20px;
}

.achievement-info h4 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.achievement-info p {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.actions-section {
  margin: 30px 0;
}

.actions-card h3 {
  color: #2c3e50;
  margin: 0;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.actions-grid .el-button {
  width: 100%;
  height: 60px;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .stat-content {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
