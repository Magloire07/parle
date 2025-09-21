import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import Home from '@/views/Home.vue'

describe('Home.vue', () => {
  it('renders properly', () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [createPinia(), ElementPlus]
      }
    })
    
    expect(wrapper.text()).toContain('Bienvenue sur Parle')
    expect(wrapper.text()).toContain('Commencer')
  })
  
  it('has correct navigation', () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [createPinia(), ElementPlus]
      }
    })
    
    const startButton = wrapper.find('[data-testid="start-button"]')
    expect(startButton.exists()).toBe(true)
  })
  
  it('displays features correctly', () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [createPinia(), ElementPlus]
      }
    })
    
    expect(wrapper.text()).toContain('Scan de Documents')
    expect(wrapper.text()).toContain('Analyse Vocale')
    expect(wrapper.text()).toContain('Résumés Oraux')
  })
})
