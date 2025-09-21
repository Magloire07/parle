import { config } from '@vue/test-utils'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'

// Configuration globale pour les tests
config.global.plugins = [createPinia(), ElementPlus]

// Mock des modules externes
vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      }
    }))
  }
}))

// Mock des services API
vi.mock('@/services/api', () => ({
  ocrService: {
    uploadImage: vi.fn(),
    analyzeText: vi.fn()
  },
  speechService: {
    analyzeSpeech: vi.fn(),
    analyzeProsody: vi.fn()
  },
  ttsService: {
    generateSpeech: vi.fn(),
    getAudioFile: vi.fn()
  },
  summaryService: {
    evaluateSummary: vi.fn(),
    generateSuggestions: vi.fn()
  },
  healthService: {
    checkHealth: vi.fn()
  }
}))

// Mock des modules audio
vi.mock('wavesurfer.js', () => ({
  default: vi.fn(() => ({
    load: vi.fn(),
    play: vi.fn(),
    pause: vi.fn(),
    stop: vi.fn(),
    destroy: vi.fn(),
    on: vi.fn(),
    off: vi.fn()
  }))
}))

// Mock des modules d'enregistrement
vi.mock('recordrtc', () => ({
  default: vi.fn(() => ({
    startRecording: vi.fn(),
    stopRecording: vi.fn(),
    getBlob: vi.fn(() => new Blob(['test'], { type: 'audio/wav' }))
  }))
}))

// Mock des modules de scan QR
vi.mock('html5-qrcode', () => ({
  Html5QrcodeScanner: vi.fn(() => ({
    render: vi.fn(),
    clear: vi.fn()
  }))
}))
