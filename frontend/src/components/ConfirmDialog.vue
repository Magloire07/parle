<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      @click.self="cancel"
    >
      <div class="bg-[#252525] rounded-lg shadow-xl max-w-md w-full mx-4 border border-gray-800 animate-fade-in">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-800">
          <h3 class="text-lg font-semibold text-white">{{ title }}</h3>
        </div>

        <!-- Body -->
        <div class="px-6 py-4">
          <p class="text-gray-300">{{ message }}</p>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-gray-800 flex justify-end gap-3">
          <button
            @click="cancel"
            class="px-4 py-2 bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white rounded-lg transition-colors"
          >
            {{ cancelText }}
          </button>
          <button
            @click="confirm"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            :class="confirmClass"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirmation'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirmer'
  },
  cancelText: {
    type: String,
    default: 'Annuler'
  },
  confirmClass: {
    type: String,
    default: 'bg-red-600 hover:bg-red-700'
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const confirm = () => {
  emit('confirm')
  emit('update:modelValue', false)
}

const cancel = () => {
  emit('cancel')
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
