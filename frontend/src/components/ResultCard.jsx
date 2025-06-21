import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

export default function ResultCard({ result }) {
  const { isReal, details } = result

  return (
    <div className="bg-white shadow sm:rounded-lg overflow-hidden">
      {/* Header */}
      <div className={`px-6 py-4 ${isReal ? 'bg-green-50' : 'bg-red-50'}`}>
        <div className="flex items-center">
          {isReal ? (
            <CheckCircleIcon className="h-8 w-8 text-green-500 mr-3" />
          ) : (
            <XCircleIcon className="h-8 w-8 text-red-500 mr-3" />
          )}
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              {isReal ? 'Likely Authentic Image' : 'Potentially Manipulated Image'}
            </h3>
          </div>
        </div>
      </div>

      {/* Details */}
      <div className="px-6 py-4">
        <p className="text-sm text-gray-600">{details}</p>
      </div>

      {/* Explanation */}
      <div className="px-6 py-4 bg-gray-50">
        <h4 className="text-sm font-medium text-gray-900 mb-2">
          What does this mean?
        </h4>
        <p className="text-sm text-gray-600">
          {isReal
            ? "While our analysis suggests this image is authentic, we recommend verifying important images through multiple sources."
            : "Our analysis indicates this image may be manipulated. We recommend verifying through other sources."}
        </p>
      </div>
    </div>
  )
}
