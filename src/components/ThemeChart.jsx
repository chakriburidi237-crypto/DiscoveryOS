import React, { useMemo } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts'

const ThemeChart = ({ themes }) => {
  // Process data for chart: get top 5 themes by priority_score
  const chartData = useMemo(() => {
    if (!themes || themes.length === 0) {
      return []
    }

    // Sort by priority_score descending and take top 5
    return themes
      .sort((a, b) => b.priority_score - a.priority_score)
      .slice(0, 5)
      .map((theme) => ({
        name: theme.name.length > 20 ? theme.name.substring(0, 17) + '...' : theme.name,
        fullName: theme.name,
        priority_score: parseFloat(theme.priority_score.toFixed(2)),
        business_impact: parseFloat(theme.business_impact.toFixed(2)),
        insight_count: theme.insight_count,
      }))
  }, [themes])

  // Colors for bars
  const colors = [
    '#0ea5e9', // primary-500
    '#06b6d4', // cyan-500
    '#10b981', // emerald-500
    '#f59e0b', // amber-500
    '#ef4444', // red-500
  ]

  if (chartData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 border border-gray-200">
        <div className="flex items-center justify-center h-80">
          <p className="text-gray-500 text-center">
            No themes available for chart
          </p>
        </div>
      </div>
    )
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-sm text-gray-900">{data.fullName}</p>
          <p className="text-xs text-primary-600">
            Priority: {data.priority_score.toFixed(2)}
          </p>
          <p className="text-xs text-amber-600">
            Impact: {data.business_impact.toFixed(2)}/5.0
          </p>
          <p className="text-xs text-gray-600">
            Frequency: {data.insight_count}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Top 5 Themes by Priority</h2>
        <p className="text-gray-600 text-sm mt-2">
          Themes ranked by priority score (frequency × business impact)
        </p>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#e5e7eb"
            vertical={false}
          />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={100}
            tick={{ fontSize: 12, fill: '#6b7280' }}
          />
          <YAxis
            label={{
              value: 'Priority Score',
              angle: -90,
              position: 'insideLeft',
              style: { textAnchor: 'middle', fill: '#6b7280' },
            }}
            tick={{ fontSize: 12, fill: '#6b7280' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="square"
          />
          <Bar
            dataKey="priority_score"
            fill="#0ea5e9"
            name="Priority Score"
            radius={[8, 8, 0, 0]}
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Legend info */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
          <div className="text-xs font-semibold text-blue-700 uppercase">
            Highest Priority
          </div>
          <div className="text-lg font-bold text-blue-900 mt-1">
            {chartData[0]?.priority_score.toFixed(2) || 'N/A'}
          </div>
        </div>
        <div className="bg-amber-50 rounded-lg p-4 border border-amber-100">
          <div className="text-xs font-semibold text-amber-700 uppercase">
            Average Priority
          </div>
          <div className="text-lg font-bold text-amber-900 mt-1">
            {(
              chartData.reduce((sum, d) => sum + d.priority_score, 0) /
              chartData.length
            ).toFixed(2)}
          </div>
        </div>
        <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-100">
          <div className="text-xs font-semibold text-emerald-700 uppercase">
            Total Themes Shown
          </div>
          <div className="text-lg font-bold text-emerald-900 mt-1">
            {chartData.length}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ThemeChart
