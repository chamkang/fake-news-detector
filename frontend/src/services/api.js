import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export const analyzeImage = async ({ file, url }) => {
  const formData = new FormData()
  if (file) {
    formData.append('file', file)
  } else if (url) {
    formData.append('url', url)
  }
  const response = await api.post('/image/analyze', formData)
  return response.data
}

export const getTrainingData = async () => {
  const response = await api.get('/admin/training-data')
  return response.data
}

export const uploadTrainingData = async (formData) => {
  const response = await api.post('/admin/training-data', formData)
  return response.data
}

export const trainModel = async () => {
  const response = await api.post('/admin/model/train')
  return response.data
}

export const getModelStatus = async () => {
  const response = await api.get('/admin/model/status')
  return response.data
}
