import axios from 'axios';

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Get CSRF token and add it to the header
api.interceptors.request.use((config) => {
  if (config.method === 'post' || config.method === 'put' || config.method === 'delete') {
    const csrfToken = getCsrfTokenFromCookies();
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Helper function to get CSRF token from cookies
function getCsrfTokenFromCookies() {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') {
      return value;
    }
  }
  return null;
}

export default api;
