<template>
  <div class="home">
    <el-row :gutter="20" justify="center">
      <el-col :span="24" :md="20" :lg="16">
        <!-- Hero Section -->
        <el-card class="hero-card" shadow="hover">
          <div class="hero-content">
            <h2 class="hero-title">Bienvenue sur Parle</h2>
            <p class="hero-description">
              Améliorez votre expression orale en lisant des textes à voix haute. 
              Notre application analyse votre prononciation, intonation et rythme 
              pour vous aider à progresser.
            </p>
            <el-button 
              type="primary" 
              size="large" 
              @click="$router.push('/upload')"
              class="start-button"
            >
              <el-icon><Upload /></el-icon>
              Commencer
            </el-button>
          </div>
        </el-card>

        <!-- Features Section -->
        <el-row :gutter="20" class="features-section">
          <el-col :span="24" :md="8">
            <el-card class="feature-card" shadow="hover">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40" color="#409EFF">
                  <Camera />
                </el-icon>
                <h3>Scan de Documents</h3>
                <p>Scannez des pages de livre et convertissez-les en texte pour l'entraînement.</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="24" :md="8">
            <el-card class="feature-card" shadow="hover">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40" color="#67C23A">
                  <Microphone />
                </el-icon>
                <h3>Analyse Vocale</h3>
                <p>Analysez votre prononciation, intonation et rythme en temps réel.</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="24" :md="8">
            <el-card class="feature-card" shadow="hover">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40" color="#E6A23C">
                  <Document />
                </el-icon>
                <h3>Résumés Oraux</h3>
                <p>Résumez oralement et recevez des suggestions d'amélioration.</p>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- How it Works Section -->
        <el-card class="how-it-works-card" shadow="hover">
          <h3 class="section-title">Comment ça marche ?</h3>
          <el-steps :active="3" align-center>
            <el-step title="Scanner" description="Uploadez une image de page de livre" />
            <el-step title="Lire" description="Lisez le texte à voix haute" />
            <el-step title="Analyser" description="Recevez un feedback détaillé" />
            <el-step title="Résumer" description="Résumez oralement et progressez" />
          </el-steps>
        </el-card>

        <!-- Stats Section -->
        <el-row :gutter="20" class="stats-section">
          <el-col :span="24" :md="8">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-number">95%</div>
                <div class="stat-label">Précision OCR</div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="24" :md="8">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-number">10+</div>
                <div class="stat-label">Langues Supportées</div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="24" :md="8">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Disponible</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { Upload, Camera, Microphone, Document } from '@element-plus/icons-vue'
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-card {
  margin-bottom: 40px;
  text-align: center;
}

.hero-content {
  padding: 40px 20px;
}

.hero-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
}

.hero-description {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.8;
}

.start-button {
  padding: 15px 30px;
  font-size: 1.1rem;
}

.features-section {
  margin-bottom: 40px;
}

.feature-card {
  height: 100%;
  margin-bottom: 20px;
}

.feature-content {
  text-align: center;
  padding: 20px;
}

.feature-icon {
  margin-bottom: 15px;
}

.feature-content h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.feature-content p {
  color: #666;
  line-height: 1.6;
}

.how-it-works-card {
  margin-bottom: 40px;
  padding: 30px;
}

.section-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 1.8rem;
}

.stats-section {
  margin-bottom: 40px;
}

.stat-card {
  height: 100%;
  margin-bottom: 20px;
}

.stat-content {
  text-align: center;
  padding: 20px;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1.1rem;
  color: #666;
  font-weight: 500;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .stat-number {
    font-size: 2.5rem;
  }
}
</style>
