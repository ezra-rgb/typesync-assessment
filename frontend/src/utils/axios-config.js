import axios from 'axios'

const instance = axios.create({
  baseURL: '/',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor to ensure proper JSON serialization
instance.interceptors.request.use(
  config => {
    if (config.data && typeof config.data === 'object') {
      config.data = JSON.stringify(config.data)
    }
    return config
  },
  error => Promise.reject(error)
)

export default instance
