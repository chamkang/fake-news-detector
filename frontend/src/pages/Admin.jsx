import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useDropzone } from 'react-dropzone'
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline'
import { getTrainingData, uploadTrainingData, trainModel } from '../services/api'

export default function Admin() {
  const [selectedLabel, setSelectedLabel] = useState('real')
  const queryClient = useQueryClient()

  // Fetch training data
  const { data: trainingData, isLoading: isLoadingData } = useQuery(
    ['training-data'],
    getTrainingData
  )

  // Upload mutation
  const { mutate: upload, isLoading: isUploading } = useMutation(
    uploadTrainingData,
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['training-data'])
      }
    }
  )

  // Train model mutation
  const { mutate: train, isLoading: isTraining } = useMutation(trainModel)

  // Handle file drop
  const onDrop = (acceptedFiles) => {
    acceptedFiles.forEach((file) => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('label', selectedLabel)
      upload(formData)
    })
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    }
  })

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>

      {/* Upload Section */}
      <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
        <h2 className="text-xl font-medium mb-4">Upload Training Data</h2>
        <div className="grid grid-cols-1 gap-6">
          {/* Label Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Image Label
            </label>
            <select
              value={selectedLabel}
              onChange={(e) => setSelectedLabel(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="real">Real Image</option>
              <option value="fake">Fake Image</option>
            </select>
          </div>

          {/* Upload Zone */}
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
              ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-500'}`}
          >
            <input {...getInputProps()} />
            <ArrowUpTrayIcon className="h-8 w-8 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600">
              {isDragActive
                ? "Drop the images here"
                : "Drag and drop images, or click to select"}
            </p>
            {isUploading && (
              <p className="text-primary-600 mt-2">Uploading...</p>
            )}
          </div>
        </div>
      </div>

      {/* Training Data List */}
      <div className="bg-white shadow sm:rounded-lg p-6 mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-medium">Training Data</h2>
          <button
            onClick={() => train()}
            disabled={isTraining}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50"
          >
            {isTraining ? 'Training...' : 'Train Model'}
          </button>
        </div>

        {isLoadingData ? (
          <p>Loading...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Filename
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Label
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Uploaded
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {trainingData?.training_data.map((item) => (
                  <tr key={item.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {item.filename}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {item.label}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
