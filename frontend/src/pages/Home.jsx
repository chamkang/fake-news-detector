import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { useMutation } from '@tanstack/react-query'
import { ArrowUpTrayIcon, GlobeAltIcon } from '@heroicons/react/24/outline'
import { analyzeImage } from '../services/api'
import ResultCard from '../components/ResultCard'

export default function Home() {
  const [imageUrl, setImageUrl] = useState('')
  const [result, setResult] = useState(null)

  const { mutate: analyze, isLoading } = useMutation(analyzeImage, {
    onSuccess: (data) => setResult(data.result),
    onError: (error) => {
      console.error('Error analyzing image:', error)
      alert('Error analyzing image. Please try again.')
    }
  })

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles?.length > 0) {
      const file = acceptedFiles[0]
      analyze({ file })
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  })

  const handleUrlSubmit = (e) => {
    e.preventDefault()
    if (imageUrl) {
      analyze({ url: imageUrl })
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
        Fake News Image Detector
      </h1>

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
              <ArrowUpTrayIcon className="h-8 w-8 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600">
                {isDragActive
                  ? "Drop the image here"
                  : "Drag and drop an image, or click to select"}
              </p>
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

      {/* Results */}
      {result && <ResultCard result={result} />}
    </div>
  )
}
