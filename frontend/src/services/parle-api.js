import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Intercepteur pour gérer les erreurs d'authentification
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ========== Auth API ==========
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getMe: () => api.get('/auth/me'),
}

// ========== Flashcards API ==========
export const flashcardsAPI = {
  getAll: (params) => api.get('/flashcards', { params }),
  getById: (id) => api.get(`/flashcards/${id}`),
  create: (data) => api.post('/flashcards', data),
  update: (id, data) => api.put(`/flashcards/${id}`, data),
  review: (id, quality) => api.post(`/flashcards/${id}/review`, { quality }),
  delete: (id) => api.delete(`/flashcards/${id}`),
}

// ========== Recordings API ==========
export const recordingsAPI = {
  uploadAudio: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/recordings/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getAll: (params) => api.get('/recordings', { params }),
  getById: (id) => api.get(`/recordings/${id}`),
  create: (data) => api.post('/recordings', data),
  delete: (id) => api.delete(`/recordings/${id}`),
}

// ========== Journal API ==========
export const journalAPI = {
  getAll: (params) => api.get('/journal', { params }),
  getById: (id) => api.get(`/journal/${id}`),
  create: (data) => api.post('/journal', data),
  update: (id, data) => api.put(`/journal/${id}`, data),
  delete: (id) => api.delete(`/journal/${id}`),
}

// ========== Schedule API ==========
export const scheduleAPI = {
  getAll: (params) => api.get('/schedule', { params }),
  getById: (id) => api.get(`/schedule/${id}`),
  create: (data) => api.post('/schedule', data),
  update: (id, data) => api.put(`/schedule/${id}`, data),
  complete: (id) => api.patch(`/schedule/${id}/complete`),
  delete: (id) => api.delete(`/schedule/${id}`),
}

// ========== Progress API ==========
export const progressAPI = {
  getAll: (params) => api.get('/progress', { params }),
  getStats: (params) => api.get('/progress/stats', { params }),
  getById: (id) => api.get(`/progress/${id}`),
  create: (data) => api.post('/progress', data),
  update: (id, data) => api.put(`/progress/${id}`, data),
  delete: (id) => api.delete(`/progress/${id}`),
}

export default api
