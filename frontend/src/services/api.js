import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Accept': 'application/json'
  },
  validateStatus: status => status < 500 // Don't reject if status is 400-499
})

export const analyzeImage = async ({ file, url }) => {
  try {
    const formData = new FormData()
    if (file) {
      formData.append('file', file)
    } else if (url) {
      formData.append('url', url)
    } else {
      throw new Error('Either file or url must be provided')
    }

    console.log('Sending request with:', { file: !!file, url: !!url })
    const response = await api.post('/predict', formData)
    console.log('Received response:', response.data)
    
    if (response.status >= 400) {
      throw new Error(response.data.detail || 'Error analyzing image')
    }

    if (!response.data || !response.data.prediction) {
      throw new Error('Invalid response from server')
    }

    const prediction = response.data.prediction.toLowerCase()
    const confidence = response.data.confidence || 0

    return {
      result: {
        isReal: prediction === 'real',
        confidence: confidence,
        details: prediction === 'real'
          ? 'This image appears to be authentic. However, always verify important images through multiple sources.'
          : 'This image appears to be manipulated or artificially generated. Please verify through other sources.'
      }
    }
  } catch (error) {
    console.error('API Error:', error)
    const errorMessage = error.response?.data?.detail || error.message || 'Failed to analyze image'
    throw new Error(errorMessage)
  }
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
