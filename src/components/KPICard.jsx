import React from 'react'

function KPICard({ title, value, unit, icon, color }) {
  const getColorClasses = () => {
    switch (color) {
      case 'blue':
        return 'bg-blue-900 border-blue-700 text-blue-100'
      case 'green':
        return 'bg-green-900 border-green-700 text-green-100'
      case 'orange':
        return 'bg-orange-900 border-orange-700 text-orange-100'
      case 'purple':
        return 'bg-purple-900 border-purple-700 text-purple-100'
      default:
        return 'bg-gray-800 border-gray-700 text-gray-100'
    }
  }

  const getValueColor = () => {
    switch (color) {
      case 'blue':
        return 'text-blue-300'
      case 'green':
        return 'text-green-300'
      case 'orange':
        return 'text-orange-300'
      case 'purple':
        return 'text-purple-300'
      default:
        return 'text-gray-300'
    }
  }

  return (
    <div
      className={`rounded-lg border p-6 transition-transform hover:scale-105 hover:shadow-lg ${getColorClasses()}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-300 uppercase tracking-wide">
            {title}
          </p>
          <p className={`text-3xl font-bold mt-2 ${getValueColor()}`}>
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          <p className="text-xs text-gray-400 mt-1">{unit}</p>
        </div>
        <div className="text-3xl">{icon}</div>
      </div>
    </div>
  )
}

export default KPICard
