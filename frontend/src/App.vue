<template>
  <div id="app">
    <el-container>
      <!-- Header -->
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">
            <el-icon><Microphone /></el-icon>
            Parle
          </h1>
          <p class="app-subtitle">Entraînement à l'oral</p>
        </div>
      </el-header>

      <!-- Main Content -->
      <el-main class="app-main">
        <router-view />
      </el-main>

      <!-- Footer -->
      <el-footer class="app-footer">
        <p>&copy; 2024 Parle - Application d'entraînement à l'oral</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { Microphone } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px;
}

.header-content {
  text-align: center;
}

.app-title {
  margin: 0;
  font-size: 2.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.app-subtitle {
  margin: 5px 0 0 0;
  font-size: 1.2rem;
  opacity: 0.9;
}

.app-main {
  min-height: calc(100vh - 120px);
  padding: 20px;
  background-color: #f5f5f5;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 15px;
  margin: 0;
}

.app-footer p {
  margin: 0;
  font-size: 0.9rem;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
}

.el-container {
  min-height: 100vh;
}

.el-main {
  padding: 20px;
}
</style>
