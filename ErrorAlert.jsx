import React, { useState } from 'react'

const ErrorAlert = ({ error, onRetry, showRetry = true }) => {
  const [isVisible, setIsVisible] = useState(true)

  if (!isVisible || !error) return null

  return (
    <div className="fixed top-4 right-4 z-50 max-w-md animate-in fade-in slide-in-from-top-2">
      <div className="bg-red-50 border-l-4 border-red-500 rounded-lg shadow-lg p-4">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 mt-0.5">
            <svg
              className="h-5 w-5 text-red-500"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-red-900 text-sm">Error</h3>
            <p className="text-red-700 text-sm mt-1">{error}</p>
            {showRetry && (
              <div className="flex gap-2 mt-3">
                <button
                  onClick={onRetry}
                  className="inline-flex items-center px-3 py-1 bg-red-600 text-white text-xs font-medium rounded hover:bg-red-700 transition-colors"
                >
                  Retry
                </button>
                <button
                  onClick={() => setIsVisible(false)}
                  className="inline-flex items-center px-3 py-1 bg-red-200 text-red-800 text-xs font-medium rounded hover:bg-red-300 transition-colors"
                >
                  Dismiss
                </button>
              </div>
            )}
          </div>
          <button
            onClick={() => setIsVisible(false)}
            className="flex-shrink-0 text-red-500 hover:text-red-700 transition-colors"
          >
            <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

export default ErrorAlert
