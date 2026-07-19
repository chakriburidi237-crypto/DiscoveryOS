import React, { useEffect } from 'react'

function ThemeDetailModal({ theme, onClose }) {
  useEffect(() => {
    // Close modal when ESC key is pressed
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [onClose])

  const getImpactColor = (impact) => {
    const score = typeof impact === 'number' ? impact : 0
    if (score >= 4.5) return 'text-red-400 bg-red-900/20'
    if (score >= 3.5) return 'text-orange-400 bg-orange-900/20'
    if (score >= 2.5) return 'text-yellow-400 bg-yellow-900/20'
    return 'text-green-400 bg-green-900/20'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-700">
        {/* Header */}
        <div className="sticky top-0 bg-gray-900 border-b border-gray-700 px-6 py-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-white">{theme.name}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors text-2xl"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Summary */}
          <div>
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-2">
              Summary
            </h3>
            <p className="text-gray-100">{theme.summary}</p>
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-2 gap-4">
            {/* Frequency */}
            <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
              <p className="text-xs font-semibold text-gray-400 uppercase">
                Frequency
              </p>
              <p className="text-3xl font-bold text-blue-400 mt-2">
                {theme.insight_count || theme.frequency || 0}
              </p>
              <p className="text-xs text-gray-500 mt-1">insights</p>
            </div>

            {/* Business Impact */}
            <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
              <p className="text-xs font-semibold text-gray-400 uppercase">
                Impact
              </p>
              <p className={`text-3xl font-bold mt-2 ${getImpactColor(theme.business_impact)}`}>
                {theme.business_impact ? theme.business_impact.toFixed(2) : 'N/A'}
              </p>
              <p className="text-xs text-gray-500 mt-1">/5.0</p>
            </div>
          </div>

          {/* Priority Score */}
          <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
            <p className="text-xs font-semibold text-gray-400 uppercase mb-2">
              Priority Score
            </p>
            <div className="flex items-end gap-2">
              <p className="text-4xl font-bold text-purple-400">
                {theme.priority_score ? theme.priority_score.toFixed(2) : 'N/A'}
              </p>
              <p className="text-sm text-gray-400 mb-1">
                (Frequency × Impact)
              </p>
            </div>
          </div>

          {/* Segment */}
          <div>
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
              Segment
            </h3>
            <div className="inline-block px-4 py-2 bg-blue-900/30 text-blue-300 border border-blue-700 rounded-lg">
              {theme.segment || 'Not specified'}
            </div>
          </div>

          {/* Metadata */}
          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-700">
            <div>
              <p className="text-xs font-semibold text-gray-400 uppercase">
                Created
              </p>
              <p className="text-sm text-gray-200 mt-1">
                {theme.created_at
                  ? new Date(theme.created_at).toLocaleDateString()
                  : 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-400 uppercase">
                Theme ID
              </p>
              <p className="text-sm text-gray-200 mt-1 font-mono">{theme.id}</p>
            </div>
          </div>

          {/* Insights Preview */}
          {theme.insights && theme.insights.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
                Sample Insights ({theme.insights.length})
              </h3>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {theme.insights.slice(0, 3).map((insight, idx) => (
                  <div
                    key={idx}
                    className="bg-gray-900 p-3 rounded border border-gray-700 text-sm text-gray-300"
                  >
                    "{insight.substring(0, 100)}..."
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-900 border-t border-gray-700 px-6 py-4 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors font-medium"
          >
            Close
          </button>
          <button
            className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
          >
            Add to Roadmap
          </button>
        </div>
      </div>
    </div>
  )
}

export default ThemeDetailModal
