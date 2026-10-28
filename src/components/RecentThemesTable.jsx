import React from 'react'

function RecentThemesTable({ themes, onThemeClick }) {
  const getImpactBadgeColor = (impact) => {
    const score = typeof impact === 'string' 
      ? (impact === 'Critical' ? 5 : impact === 'High' ? 4 : impact === 'Medium' ? 3 : 2)
      : impact

    if (score >= 4) return 'bg-red-900 text-red-200 border-red-700'
    if (score >= 3) return 'bg-orange-900 text-orange-200 border-orange-700'
    if (score >= 2) return 'bg-yellow-900 text-yellow-200 border-yellow-700'
    return 'bg-green-900 text-green-200 border-green-700'
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    } catch {
      return 'N/A'
    }
  }

  return (
    <div className="overflow-x-auto bg-gray-800 rounded-lg border border-gray-700">
      <table className="w-full">
        <thead className="bg-gray-900 border-b border-gray-700">
          <tr>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">
              Theme
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">
              Segment
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">
              Frequency
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">
              Impact
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">
              Score
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          {themes.map((theme, idx) => (
            <tr
              key={theme.id || idx}
              className="border-b border-gray-700 hover:bg-gray-700 transition-colors"
            >
              <td className="px-6 py-4 text-sm text-gray-200">
                <div className="font-medium">{theme.name}</div>
                <div className="text-xs text-gray-400 truncate">
                  {theme.summary}
                </div>
              </td>
              <td className="px-6 py-4 text-sm text-gray-300">
                {theme.segment || 'N/A'}
              </td>
              <td className="px-6 py-4 text-sm text-gray-300">
                {theme.insight_count || theme.frequency || 0}
              </td>
              <td className="px-6 py-4">
                <span className={`inline-block px-3 py-1 text-xs font-medium rounded border ${getImpactBadgeColor(theme.business_impact)}`}>
                  {theme.business_impact ? theme.business_impact.toFixed(1) : 'N/A'}
                </span>
              </td>
              <td className="px-6 py-4 text-sm font-bold text-blue-300">
                {theme.priority_score ? theme.priority_score.toFixed(1) : 'N/A'}
              </td>
              <td className="px-6 py-4 text-sm">
                <button
                  onClick={() => onThemeClick(theme)}
                  className="text-blue-400 hover:text-blue-300 underline transition-colors"
                >
                  View Details
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RecentThemesTable
