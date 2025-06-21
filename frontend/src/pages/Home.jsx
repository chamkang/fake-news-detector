import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { useMutation } from '@tanstack/react-query'
import { ArrowUpTrayIcon, GlobeAltIcon } from '@heroicons/react/24/outline'
import { analyzeImage } from '../services/api'
import ResultCard from '../components/ResultCard'

export default function Home() {
  const [imageUrl, setImageUrl] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)

  const { mutate: analyze, isLoading } = useMutation(analyzeImage, {
    onSuccess: (data) => {
      console.log('Analysis successful:', data)
      setResult(data.result)
      setError(null)
    },
    onError: (error) => {
      console.error('Error analyzing image:', error)
      setError(error.message || 'Error analyzing image. Please try again.')
      setResult(null)
    }
  })

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles?.length > 0) {
      try {
        const file = acceptedFiles[0]
        setPreviewUrl(URL.createObjectURL(file))
        setResult(null) // Clear previous results
        setError(null) // Clear previous errors
        setImageUrl('') // Clear URL input when file is uploaded
        await analyze({ file })
      } catch (error) {
        console.error('Drop error:', error)
        setError('Failed to process image. Please try again.')
      }
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  })

  const handleUrlSubmit = async (e) => {
    e.preventDefault()
    if (imageUrl) {
      try {
        setPreviewUrl(imageUrl)
        setResult(null) // Clear previous results
        setError(null) // Clear previous errors
        await analyze({ url: imageUrl })
      } catch (error) {
        console.error('URL submit error:', error)
        setError('Failed to analyze image URL. Please try again.')
      }
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">
        VeriFact
      </h1>
      <p className="text-gray-600 text-center mb-8">
        AI-Powered Image Authenticity Verification
      </p>

      <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          {/* File Upload */}
          <div>
            <h2 className="text-lg font-medium mb-4">Upload Image</h2>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
                ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-500'}`}
            >
              <input {...getInputProps()} />
              {isLoading ? (
                <div className="text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Analyzing image...</p>
                </div>
              ) : previewUrl ? (
                <div className="relative">
                  <img
                    src={previewUrl}
                    alt="Preview"
                    className="max-h-48 mx-auto rounded-lg"
                  />
                  <p className="mt-2 text-sm text-gray-600">
                    {error ? "Drop new image to try again" : "Drop new image to replace"}
                  </p>
                </div>
              ) : (
                <>
                  <ArrowUpTrayIcon className="h-8 w-8 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-600">
                    {isDragActive
                      ? "Drop the image here"
                      : "Drag and drop an image, or click to select"}
                  </p>
                </>
              )}
            </div>
          </div>

          {/* URL Input */}
          <div>
            <h2 className="text-lg font-medium mb-4">Image URL</h2>
            <form onSubmit={handleUrlSubmit} className="space-y-4">
              <div>
                <input
                  type="url"
                  value={imageUrl}
                  onChange={(e) => setImageUrl(e.target.value)}
                  placeholder="Enter image URL"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <button
                type="submit"
                disabled={!imageUrl || isLoading}
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                {isLoading ? 'Analyzing...' : 'Analyze URL'}
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && !error && <ResultCard result={result} />}
    </div>
  )
}
