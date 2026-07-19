import React from 'react'

function ThemeGrid({ themes, onThemeClick }) {
  if (!themes || themes.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-800 rounded-lg border border-gray-700">
        <p className="text-gray-400">No themes to display</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {themes.map((theme) => (
        <div
          key={theme.id}
          className="bg-gray-800 border border-gray-700 rounded-lg p-6 cursor-pointer hover:border-blue-500 transition-colors"
          onClick={() => onThemeClick(theme)}
        >
          <div className="flex items-start justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex-1">{theme.name}</h3>
            <span className="ml-2 px-2 py-1 bg-blue-900 text-blue-200 rounded text-xs font-medium">
              {theme.priority_score?.toFixed(1) || '0'}
            </span>
          </div>
          <p className="text-gray-400 text-sm mb-4 line-clamp-2">{theme.summary}</p>
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>{theme.insight_count} insights</span>
            <span className="text-yellow-400">★ {theme.business_impact?.toFixed(1) || '0'}/5</span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ThemeGrid
