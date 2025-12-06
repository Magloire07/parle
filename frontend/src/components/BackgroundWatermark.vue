<template>
  <div class="fixed inset-0 overflow-hidden pointer-events-none select-none z-0">

    
    <!-- Random Watermark Icons -->
    <div class="absolute inset-0">
      <component
        v-for="(item, index) in watermarkItems"
        :key="index"
        :is="item.component"
        class="absolute text-[#3b82f6] stroke-1 transform transition-transform duration-1000 ease-in-out hover:scale-110 hover:text-white hover:opacity-100 opacity-[0.4]"
        :style="{
          top: `${item.top}%`,
          left: `${item.left}%`,
          width: `${item.size}px`,
          height: `${item.size}px`,
          transform: `rotate(${item.rotation}deg)`
        }"
      />
    </div>
    
    <!-- Gradient Overlay to fade edges and blend -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#0a0a0a] via-[#0a0a0a]/80 to-[#0a0a0a] opacity-[0.4]"></div>

    <!-- Dot Pattern (on top for visibility) -->
    <div class="absolute inset-0 opacity-[0.1]" 
         style="background-image: radial-gradient(#ffffff 1px, transparent 1px); background-size: 24px 24px;">
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { 
  MicrophoneIcon, 
  BookOpenIcon, 
  PencilIcon, 
  SpeakerWaveIcon,
  ChatBubbleBottomCenterTextIcon,
  AcademicCapIcon,
  GlobeEuropeAfricaIcon
} from '@heroicons/vue/24/outline'

const icons = [
  MicrophoneIcon, 
  BookOpenIcon, 
  PencilIcon, 
  SpeakerWaveIcon,
  ChatBubbleBottomCenterTextIcon,
  AcademicCapIcon,
  GlobeEuropeAfricaIcon
]

const watermarkItems = ref([])

onMounted(() => {
  // Grid based generation to prevent overlaps
  const rows = 3
  const cols = 4
  const cellWidth = 100 / cols
  const cellHeight = 100 / rows
  const padding = 10 // % padding to keep away from edges of the cell

  watermarkItems.value = []

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      // Select random icon
      const component = icons[Math.floor(Math.random() * icons.length)]
      
      // Calculate random position within the cell
      // We limit the range so icons stay roughly centered in their grid cells
      // and definitely don't overlap with neighbors
      const top = (r * cellHeight) + (Math.random() * (cellHeight - 20)) + 5
      const left = (c * cellWidth) + (Math.random() * (cellWidth - 20)) + 5
      
      const size = 32 + Math.random() * 40 // Reduced by half as requested
      const rotation = Math.random() * 360

      watermarkItems.value.push({
        component,
        top,
        left,
        rotation,
        size
      })
    }
  }
})
</script>
