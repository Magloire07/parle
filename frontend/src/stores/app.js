import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const currentText = ref(null)
  const currentParagraph = ref(1)
  const totalParagraphs = ref(0)
  const isRecording = ref(false)
  const analysisResults = ref([])
  const userProgress = ref({
    totalReadings: 0,
    totalSummaries: 0,
    averageConfidence: 0,
    lastActivity: null
  })

  // Getters
  const readingProgress = computed(() => {
    return totalParagraphs.value > 0 ? (currentParagraph.value / totalParagraphs.value) * 100 : 0
  })

  const canGoToSummary = computed(() => {
    return currentParagraph.value >= 2
  })

  const hasAnalysisResults = computed(() => {
    return analysisResults.value.length > 0
  })

  // Actions
  const setCurrentText = (textData) => {
    currentText.value = textData
    totalParagraphs.value = textData.paragraphs.length
    currentParagraph.value = 1
  }

  const nextParagraph = () => {
    if (currentParagraph.value < totalParagraphs.value) {
      currentParagraph.value++
    }
  }

  const previousParagraph = () => {
    if (currentParagraph.value > 1) {
      currentParagraph.value--
    }
  }

  const setRecording = (recording) => {
    isRecording.value = recording
  }

  const addAnalysisResult = (result) => {
    analysisResults.value.push({
      ...result,
      paragraph: currentParagraph.value,
      timestamp: new Date().toISOString()
    })
  }

  const updateProgress = (newProgress) => {
    userProgress.value = { ...userProgress.value, ...newProgress }
  }

  const reset = () => {
    currentText.value = null
    currentParagraph.value = 1
    totalParagraphs.value = 0
    isRecording.value = false
    analysisResults.value = []
  }

  return {
    // State
    currentText,
    currentParagraph,
    totalParagraphs,
    isRecording,
    analysisResults,
    userProgress,
    
    // Getters
    readingProgress,
    canGoToSummary,
    hasAnalysisResults,
    
    // Actions
    setCurrentText,
    nextParagraph,
    previousParagraph,
    setRecording,
    addAnalysisResult,
    updateProgress,
    reset
  }
})
