import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

export default function ResultCard({ result }) {
  const { is_fake, confidence, metadata } = result
  const confidencePercent = (confidence * 100).toFixed(1)

  return (
    <div className="bg-white shadow sm:rounded-lg overflow-hidden">
      {/* Header */}
      <div className={`px-6 py-4 ${is_fake ? 'bg-red-50' : 'bg-green-50'}`}>
        <div className="flex items-center">
          {is_fake ? (
            <XCircleIcon className="h-8 w-8 text-red-500 mr-3" />
          ) : (
            <CheckCircleIcon className="h-8 w-8 text-green-500 mr-3" />
          )}
          <div>
            <h3 className="text-lg font-medium">
              {is_fake ? 'Potentially Fake Image' : 'Likely Authentic Image'}
            </h3>
            <p className="text-sm text-gray-600">
              Confidence: {confidencePercent}%
            </p>
          </div>
        </div>
      </div>

      {/* Metadata */}
      {metadata && Object.keys(metadata).length > 0 && (
        <div className="px-6 py-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3">
            Image Metadata
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(metadata).map(([key, value]) => (
              <div key={key} className="flex items-start">
                <dt className="text-sm font-medium text-gray-500 mr-2">
                  {key}:
                </dt>
                <dd className="text-sm text-gray-900">
                  {typeof value === 'object' ? JSON.stringify(value) : value}
                </dd>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Explanation */}
      <div className="px-6 py-4 bg-gray-50">
        <h4 className="text-sm font-medium text-gray-900 mb-2">
          What does this mean?
        </h4>
        <p className="text-sm text-gray-600">
          {is_fake
            ? "Our analysis suggests this image may have been manipulated or artificially generated. However, please note that this is not definitive proof - we recommend cross-referencing with other sources."
            : "Our analysis suggests this image is likely authentic. However, no detection system is perfect - always verify important images through multiple sources."}
        </p>
      </div>
    </div>
  )
}
