import axios from 'axios'

// Configuration de base d'axios
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour les requêtes
api.interceptors.request.use(
  (config) => {
    // Ajout du token d'authentification si disponible
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour les réponses
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Redirection vers la page de connexion
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Service OCR
export const ocrService = {
  uploadImage: (formData) => {
    return api.post('/ocr/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  analyzeText: (text) => {
    return api.post('/ocr/analyze', { text })
  }
}

// Service de traitement de la parole
export const speechService = {
  analyzeSpeech: (formData) => {
    return api.post('/speech/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  analyzeProsody: (audioFile, expectedText) => {
    const formData = new FormData()
    formData.append('audio_file', audioFile)
    formData.append('expected_text', expectedText)
    
    return api.post('/speech/prosody', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

// Service de synthèse vocale
export const ttsService = {
  generateSpeech: (text, language = 'fr', slow = false) => {
    return api.post('/tts/read', {
      text,
      language,
      slow
    })
  },
  
  getAudioFile: (filename) => {
    return api.get(`/tts/audio/${filename}`)
  }
}

// Service d'évaluation des résumés
export const summaryService = {
  evaluateSummary: (formData) => {
    return api.post('/summary/evaluate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  generateSuggestions: (sourceText) => {
    return api.post('/summary/generate', {
      source_text: sourceText
    })
  }
}

// Service de santé
export const healthService = {
  checkHealth: () => {
    return api.get('/health/')
  }
}

export default api
