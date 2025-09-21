import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import Upload from '@/views/Upload.vue'

// Mock des services
vi.mock('@/services/api', () => ({
  ocrService: {
    uploadImage: vi.fn(() => Promise.resolve({
      data: {
        success: true,
        text: 'Test text',
        paragraphs: ['Test paragraph 1', 'Test paragraph 2'],
        confidence: 95.0,
        language: 'fr'
      }
    }))
  }
}))

describe('Upload Integration', () => {
  it('should handle file upload successfully', async () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [createPinia(), ElementPlus]
      }
    })
    
    // Simuler la sélection d'un fichier
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    const input = wrapper.find('input[type="file"]')
    await input.setValue(file)
    
    // Vérifier que le fichier est sélectionné
    expect(wrapper.vm.fileList).toHaveLength(1)
  })
  
  it('should validate file type', async () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [createPinia(), ElementPlus]
      }
    })
    
    // Simuler la sélection d'un fichier invalide
    const file = new File(['test'], 'test.txt', { type: 'text/plain' })
    const input = wrapper.find('input[type="file"]')
    await input.setValue(file)
    
    // Vérifier que le fichier n'est pas accepté
    expect(wrapper.vm.fileList).toHaveLength(0)
  })
  
  it('should process image and show results', async () => {
    const wrapper = mount(Upload, {
      global: {
        plugins: [createPinia(), ElementPlus]
      }
    })
    
    // Simuler la sélection d'un fichier valide
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    const input = wrapper.find('input[type="file"]')
    await input.setValue(file)
    
    // Simuler le traitement
    await wrapper.vm.submitUpload()
    
    // Vérifier que les résultats sont affichés
    expect(wrapper.vm.ocrResult).toBeTruthy()
    expect(wrapper.vm.ocrResult.success).toBe(true)
  })
})
