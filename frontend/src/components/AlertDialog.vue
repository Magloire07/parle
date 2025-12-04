<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      @click.self="close"
    >
      <div class="bg-[#252525] rounded-lg shadow-xl max-w-md w-full mx-4 border border-gray-800 animate-fade-in">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-800 flex items-center gap-3">
          <span class="text-2xl" :class="iconClass">{{ icon }}</span>
          <h3 class="text-lg font-semibold text-white">{{ title }}</h3>
        </div>

        <!-- Body -->
        <div class="px-6 py-4">
          <p class="text-gray-300">{{ message }}</p>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-gray-800 flex justify-end">
          <button
            @click="close"
            class="px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg transition-colors"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Information'
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info', // 'info', 'success', 'error', 'warning'
    validator: (value) => ['info', 'success', 'error', 'warning'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const icon = computed(() => {
  const icons = {
    info: 'ℹ️',
    success: '✅',
    error: '❌',
    warning: '⚠️'
  }
  return icons[props.type]
})

const iconClass = computed(() => {
  const classes = {
    info: 'text-blue-500',
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500'
  }
  return classes[props.type]
})

const close = () => {
  emit('close')
  emit('update:modelValue', false)
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>
