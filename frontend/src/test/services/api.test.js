import { describe, it, expect, vi } from 'vitest'
import { ocrService, speechService, ttsService, summaryService } from '@/services/api'

// Mock axios
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

describe('API Services', () => {
  describe('OCR Service', () => {
    it('should have uploadImage method', () => {
      expect(typeof ocrService.uploadImage).toBe('function')
    })
    
    it('should have analyzeText method', () => {
      expect(typeof ocrService.analyzeText).toBe('function')
    })
  })
  
  describe('Speech Service', () => {
    it('should have analyzeSpeech method', () => {
      expect(typeof speechService.analyzeSpeech).toBe('function')
    })
    
    it('should have analyzeProsody method', () => {
      expect(typeof speechService.analyzeProsody).toBe('function')
    })
  })
  
  describe('TTS Service', () => {
    it('should have generateSpeech method', () => {
      expect(typeof ttsService.generateSpeech).toBe('function')
    })
    
    it('should have getAudioFile method', () => {
      expect(typeof ttsService.getAudioFile).toBe('function')
    })
  })
  
  describe('Summary Service', () => {
    it('should have evaluateSummary method', () => {
      expect(typeof summaryService.evaluateSummary).toBe('function')
    })
    
    it('should have generateSuggestions method', () => {
      expect(typeof summaryService.generateSuggestions).toBe('function')
    })
  })
})
