import React from 'react'

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="text-center">
        {/* Spinner animation */}
        <div className="inline-block">
          <div className="relative w-16 h-16">
            <div
              className="absolute w-16 h-16 border-4 border-gray-200 rounded-full"
              style={{
                animation: 'spin 3s linear infinite',
                borderTopColor: '#0ea5e9',
                borderRightColor: '#0ea5e9',
              }}
            />
            <div
              className="absolute inset-0 w-16 h-16 border-4 border-gray-200 rounded-full"
              style={{
                animation: 'spin 1.5s linear infinite reverse',
                borderBottomColor: '#06b6d4',
                borderLeftColor: '#06b6d4',
              }}
            />
          </div>
        </div>
        <p className="mt-6 text-lg font-medium text-gray-700">{message}</p>
        <p className="mt-2 text-sm text-gray-500">
          This may take a moment...
        </p>

        <style>{`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </div>
  )
}

export default LoadingSpinner
