import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use((response) => {
  if (response.data && response.data.sessionId) {
    document.cookie = `sessionId=${response.data.sessionId}; path=/;`
  }
  return response
})

export default api

