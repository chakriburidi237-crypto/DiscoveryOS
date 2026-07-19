import React, { useMemo } from 'react'
import {
  PieChart,
  Pie,
  Cell,
  Legend,
  Tooltip,
  ResponsiveContainer
} from 'recharts'

const COLORS = ['#8B5CF6', '#0EA5E9', '#FFA500', '#10B981', '#6B7280']

function SegmentChart({ segments }) {
  // Process data for pie chart
  const chartData = useMemo(() => {
    if (!segments || segments.length === 0) {
      return []
    }

    return segments
      .filter(s => s.theme_count > 0)
      .map((segment, idx) => ({
        name: segment.segment,
        value: segment.theme_count,
        percentage: ((segment.theme_count / segments.reduce((sum, s) => sum + s.theme_count, 0)) * 100).toFixed(1)
      }))
  }, [segments])

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-80">
        <p className="text-gray-500">No segment data available</p>
      </div>
    )
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-gray-900 p-3 rounded-lg shadow-lg border border-gray-700">
          <p className="font-semibold text-gray-100">{data.name}</p>
          <p className="text-xs text-blue-300">
            Themes: {data.value}
          </p>
          <p className="text-xs text-gray-400">
            {data.percentage}%
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          paddingAngle={2}
          dataKey="value"
          label={({ name, percentage }) => `${name} (${percentage}%)`}
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend 
          verticalAlign="bottom" 
          height={36}
          wrapperStyle={{ paddingTop: '20px' }}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}

export default SegmentChart
