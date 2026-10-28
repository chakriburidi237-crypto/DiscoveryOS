import React from 'react'

const Header = ({ totalThemes, totalSegments, timestamp, isLoading }) => {
  const formatTimestamp = (isoString) => {
    try {
      const date = new Date(isoString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
    } catch {
      return 'Unknown'
    }
  }

  return (
    <header className="bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Main title */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-primary-400 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold">DiscoveryOS Dashboard</h1>
          </div>
          <p className="text-primary-100 text-sm md:text-base">
            Product discovery themes intelligence and priority ranking
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-primary-500 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
            <div className="text-primary-100 text-sm font-medium uppercase tracking-wide">
              Total Themes
            </div>
            <div className="text-3xl font-bold mt-2">
              {isLoading ? '—' : totalThemes}
            </div>
          </div>
          <div className="bg-primary-500 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
            <div className="text-primary-100 text-sm font-medium uppercase tracking-wide">
              User Segments
            </div>
            <div className="text-3xl font-bold mt-2">
              {isLoading ? '—' : totalSegments}
            </div>
          </div>
          <div className="bg-primary-500 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
            <div className="text-primary-100 text-sm font-medium uppercase tracking-wide">
              Last Updated
            </div>
            <div className="text-sm font-mono mt-2">
              {isLoading ? 'Loading...' : formatTimestamp(timestamp)}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
