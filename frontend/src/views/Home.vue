<template>
  <div class="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
    <div class="text-center px-4">
      <h1 class="text-5xl font-bold text-white mb-4">Parle</h1>
      <p class="text-xl text-gray-400 mb-8">Plateforme d'apprentissage linguistique</p>
      <div class="flex gap-4 justify-center">
        <router-link 
          to="/login" 
          class="px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-lg font-medium transition-colors"
        >
          Se connecter
        </router-link>
        <router-link 
          to="/register" 
          class="px-6 py-3 bg-[#252525] text-white rounded-lg font-medium border border-gray-700 hover:border-gray-600 transition-colors"
        >
          S'inscrire
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// Page d'accueil temporaire
</script>

