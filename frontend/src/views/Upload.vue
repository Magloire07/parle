<template>
  <div class="upload">
    <el-row :gutter="20" justify="center">
      <el-col :span="24" :md="20" :lg="16">
        <el-card class="upload-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h2>Scanner un Document</h2>
              <p>Uploadez une image de page de livre pour commencer l'entraînement</p>
            </div>
          </template>

          <!-- Upload Area -->
          <el-upload
            ref="uploadRef"
            class="upload-dragger"
            drag
            :action="uploadUrl"
            :before-upload="beforeUpload"
            :on-success="handleSuccess"
            :on-error="handleError"
            :file-list="fileList"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            accept="image/*;capture=camera"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              Glissez-déposez votre image ici ou <em>cliquez pour sélectionner</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                Formats supportés: JPG, PNG, GIF (max 10MB)
              </div>
            </template>
          </el-upload>

          <!-- File Info -->
          <div v-if="fileList.length > 0" class="file-info">
            <el-alert
              :title="`Fichier sélectionné: ${fileList[0].name}`"
              type="info"
              :closable="false"
              show-icon
            />
          </div>

          <!-- Upload Actions -->
          <div class="upload-actions">
            <el-button 
              type="primary" 
              size="large" 
              @click="submitUpload"
              :loading="uploading"
              :disabled="fileList.length === 0"
            >
              <el-icon><Upload /></el-icon>
              Traiter l'Image
            </el-button>

            <el-button 
              size="large"
              @click="openCamera"
            >
              Ouvrir la Caméra
            </el-button>
          </div>

          <!-- Camera Dialog -->
          <el-dialog
            v-model="showCamera"
            width="600px"
            :close-on-click-modal="false"
            @close="closeCamera"
            title="Prendre une photo"
          >
            <div class="camera-wrapper">
              <video ref="videoRef" autoplay playsinline class="camera-video"></video>
              <canvas ref="canvasRef" class="camera-canvas" style="display:none"></canvas>
            </div>

            <template #footer>
              <span class="dialog-footer">
                <el-button @click="closeCamera">Annuler</el-button>
                <el-button type="primary" @click="capturePhoto">Capturer</el-button>
              </span>
            </template>
          </el-dialog>

          <!-- Processing Status -->
          <div v-if="processing" class="processing-status">
            <el-progress 
              :percentage="progress" 
              :status="progressStatus"
              :stroke-width="8"
            />
            <p class="processing-text">{{ processingText }}</p>
          </div>

          <!-- Results -->
          <div v-if="ocrResult" class="results-section">
            <el-divider>Résultat de l'OCR</el-divider>
            
            <el-alert
              :title="`Texte extrait avec ${ocrResult.confidence}% de confiance`"
              :type="ocrResult.confidence > 80 ? 'success' : 'warning'"
              :closable="false"
              class="confidence-alert"
            />

            <div class="text-preview">
              <h4>Texte extrait :</h4>
              <div class="text-content">
                <p v-for="(paragraph, index) in ocrResult.paragraphs" :key="index">
                  {{ paragraph }}
                </p>
              </div>
            </div>

            <div class="text-actions">
              <el-button 
                type="primary" 
                @click="startReading"
                :disabled="!ocrResult.paragraphs.length"
              >
                <el-icon><Microphone /></el-icon>
                Commencer la Lecture
              </el-button>
              
              <el-button @click="resetUpload">
                <el-icon><Refresh /></el-icon>
                Nouveau Document
              </el-button>
            </div>
          </div>
        </el-card>

        <!-- Instructions -->
        <el-card class="instructions-card" shadow="hover">
          <template #header>
            <h3>Conseils pour un meilleur résultat</h3>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="24" :md="12">
              <h4>✅ Bonnes pratiques :</h4>
              <ul>
                <li>Éclairage uniforme sur la page</li>
                <li>Page bien à plat, sans plis</li>
                <li>Image nette et bien cadrée</li>
                <li>Contraste suffisant entre texte et fond</li>
              </ul>
            </el-col>
            
            <el-col :span="24" :md="12">
              <h4>❌ À éviter :</h4>
              <ul>
                <li>Ombres portées sur le texte</li>
                <li>Reflets ou éblouissements</li>
                <li>Page pliée ou déchirée</li>
                <li>Image floue ou de mauvaise qualité</li>
              </ul>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Upload, UploadFilled, Microphone, Refresh } from '@element-plus/icons-vue'
import { ocrService } from '@/services/api'

const router = useRouter()

// Reactive data
const uploadRef = ref()
const fileList = ref([])
const uploading = ref(false)
const processing = ref(false)
const progress = ref(0)
const progressStatus = ref('')
const processingText = ref('')
const ocrResult = ref(null)

// Camera
const showCamera = ref(false)
const videoRef = ref(null)
const canvasRef = ref(null)
const cameraStream = ref(null)

// Upload configuration
const uploadUrl = '/api/ocr/upload'

// Methods
const handleFileChange = (file, files) => {
  // Mettre à jour la liste des fichiers
  fileList.value = files
  
  // Vérifier le fichier
  const isImage = file.raw && file.raw.type.startsWith('image/')
  const isLt10M = file.raw && file.raw.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('Le fichier doit être une image!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('La taille de l\'image ne doit pas dépasser 10MB!')
    return false
  }
  
  ElMessage.success('Image sélectionnée avec succès!')

  // Persister l'image sélectionnée (si disponible sous forme d'URL)
  try {
    if (file && file.raw) {
      const reader = new FileReader()
      reader.onload = () => {
        localStorage.setItem('lastUploadImage', reader.result)
        localStorage.setItem('lastUploadName', file.name || file.raw.name || 'image.jpg')
      }
      reader.readAsDataURL(file.raw)
    }
  } catch (e) { /* noop */ }
  return true
}

const handleFileRemove = (file, files) => {
  // Mettre à jour la liste des fichiers
  fileList.value = files
  
  // Supprimer les données persistées dans localStorage quand un fichier est supprimé
  localStorage.removeItem('lastUploadImage')
  localStorage.removeItem('lastUploadName')
  
  // Réinitialiser les résultats OCR si ils existent
  ocrResult.value = null
  
  ElMessage.success('Fichier supprimé')
  
  return true
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('Le fichier doit être une image!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('La taille de l\'image ne doit pas dépasser 10MB!')
    return false
  }
  return true
}

// Camera helpers
const openCamera = async () => {
  showCamera.value = true
  await nextTick()
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' } },
      audio: false
    })
    cameraStream.value = stream
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
  } catch (err) {
    ElMessage.error('Impossible d\'accéder à la caméra')
    showCamera.value = false
  }
}

const closeCamera = () => {
  if (cameraStream.value) {
    cameraStream.value.getTracks().forEach(t => t.stop())
    cameraStream.value = null
  }
  showCamera.value = false
}

const capturePhoto = () => {
  try {
    const video = videoRef.value
    const canvas = canvasRef.value
    if (!video || !canvas) return
    const width = video.videoWidth
    const height = video.videoHeight
    canvas.width = width
    canvas.height = height
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, width, height)
    canvas.toBlob((blob) => {
      if (!blob) return
      const fileName = `photo-${Date.now()}.jpg`
      const file = new File([blob], fileName, { type: 'image/jpeg' })
      const uploadItem = {
        name: fileName,
        size: file.size,
        status: 'ready',
        percentage: 0,
        raw: file,
        url: URL.createObjectURL(blob)
      }
      fileList.value = [uploadItem]

      // Persister en localStorage
      const reader = new FileReader()
      reader.onload = () => {
        localStorage.setItem('lastUploadImage', reader.result)
        localStorage.setItem('lastUploadName', fileName)
      }
      reader.readAsDataURL(file)

      ElMessage.success('Photo capturée')
      closeCamera()
    }, 'image/jpeg', 0.92)
  } catch (e) {
    ElMessage.error('Échec de la capture')
  }
}

// Restore last file on refresh
onMounted(() => {
  const dataUrl = localStorage.getItem('lastUploadImage')
  const name = localStorage.getItem('lastUploadName') || 'image.jpg'
  if (dataUrl && fileList.value.length === 0) {
    fetch(dataUrl)
      .then(res => res.blob())
      .then(blob => {
        const file = new File([blob], name, { type: blob.type || 'image/jpeg' })
        const uploadItem = {
          name,
          size: file.size,
          status: 'ready',
          percentage: 0,
          raw: file,
          url: dataUrl
        }
        fileList.value = [uploadItem]
      })
      .catch(() => {})
  }
})

onUnmounted(() => {
  if (cameraStream.value) {
    cameraStream.value.getTracks().forEach(t => t.stop())
  }
})

const submitUpload = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('Veuillez sélectionner une image')
    return
  }

  uploading.value = true
  processing.value = true
  progress.value = 0
  progressStatus.value = 'active'
  processingText.value = 'Traitement de l\'image...'

  try {
    // Simulation du progrès
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += 10
      }
    }, 200)

    const formData = new FormData()
    formData.append('file', fileList.value[0].raw)

    const response = await ocrService.uploadImage(formData)
    
    clearInterval(progressInterval)
    progress.value = 100
    progressStatus.value = 'success'
    processingText.value = 'Traitement terminé!'

    ocrResult.value = response.data

    ElMessage.success('Image traitée avec succès!')
    
    // Redirection vers la lecture après un délai
    setTimeout(() => {
      startReading()
    }, 1500)

  } catch (error) {
    console.error('Erreur upload:', error)
    progressStatus.value = 'exception'
    processingText.value = 'Erreur lors du traitement'
    ElMessage.error('Erreur lors du traitement de l\'image')
  } finally {
    uploading.value = false
    processing.value = false
  }
}

const handleSuccess = (response) => {
  console.log('Upload success:', response)
}

const handleError = (error) => {
  console.error('Upload error:', error)
  ElMessage.error('Erreur lors de l\'upload')
}

const startReading = () => {
  if (ocrResult.value && ocrResult.value.paragraphs.length > 0) {
    // Sauvegarde du texte dans le store ou localStorage
    localStorage.setItem('currentText', JSON.stringify(ocrResult.value))
    
    // Redirection vers la page de lecture
    router.push({
      name: 'Reading',
      params: { textId: 'current' }
    })
  }
}

const resetUpload = () => {
  fileList.value = []
  ocrResult.value = null
  processing.value = false
  progress.value = 0
  uploadRef.value.clearFiles()
  
  // Supprimer les données persistées dans localStorage
  localStorage.removeItem('lastUploadImage')
  localStorage.removeItem('lastUploadName')
}
</script>

<style scoped>
.upload {
  max-width: 1200px;
  margin: 0 auto;
}

.upload-card {
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

.upload-dragger {
  margin: 30px 0;
}

.file-info {
  margin: 20px 0;
}

.upload-actions {
  text-align: center;
  margin: 30px 0;
}

.camera-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
}

.camera-video {
  width: 100%;
  max-width: 540px;
  border-radius: 8px;
  background: #000;
}

.processing-status {
  margin: 30px 0;
  text-align: center;
}

.processing-text {
  margin-top: 15px;
  color: #666;
  font-size: 1.1rem;
}

.results-section {
  margin-top: 30px;
}

.confidence-alert {
  margin: 20px 0;
}

.text-preview {
  margin: 20px 0;
}

.text-preview h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.text-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
  max-height: 300px;
  overflow-y: auto;
}

.text-content p {
  margin-bottom: 15px;
  line-height: 1.6;
  color: #333;
}

.text-actions {
  text-align: center;
  margin: 30px 0;
}

.text-actions .el-button {
  margin: 0 10px;
}

.instructions-card {
  margin-top: 30px;
}

.instructions-card h3 {
  color: #2c3e50;
  margin: 0;
}

.instructions-card h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.instructions-card ul {
  padding-left: 20px;
}

.instructions-card li {
  margin-bottom: 8px;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .text-actions .el-button {
    display: block;
    width: 100%;
    margin: 10px 0;
  }
}
</style>
