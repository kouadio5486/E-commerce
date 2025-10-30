import axios from 'axios'

const serverURL = import.meta.env.VITE_API_SERVER_URL || 'http://127.0.0.1:8000/'

const authApi = axios.create({
  baseURL: serverURL + 'auth/',
})

authApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default authApi