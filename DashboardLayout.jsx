import React, { useState, useEffect, useCallback } from 'react'
import Header from './Header'
import KPICard from './KPICard'
import ThemeChart from './ThemeChart'
import SegmentChart from './SegmentChart'
import ThemeGrid from './ThemeGrid'
import RecentThemesTable from './RecentThemesTable'
import LoadingSpinner from './LoadingSpinner'
import ErrorAlert from './ErrorAlert'
import ErrorBoundary from './ErrorBoundary'
import ThemeDetailModal from './ThemeDetailModal'
import { fetchReport } from '../api/reportService'

function DashboardLayout() {
  const [dashboardData, setDashboardData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedTheme, setSelectedTheme] = useState(null)
  const [filteredSegment, setFilteredSegment] = useState(null)
  const [lastRefresh, setLastRefresh] = useState(new Date())

  // Fetch dashboard data
  const loadDashboard = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await fetchReport()
      
      // Validate data structure
      if (!data) {
        throw new Error('No data returned from API')
      }
      
      // The response should have segments array
      if (!data.segments || !Array.isArray(data.segments)) {
        console.warn('Unexpected data structure:', data)
        // Create mock data if backend returns empty
        if (!data.segments) {
          data.segments = []
        }
      }
      
      setDashboardData(data)
      setLastRefresh(new Date())
      setError(null)
    } catch (err) {
      console.error('Error loading dashboard:', err)
      setError(
        err.message || 'Failed to load dashboard. Please check the backend connection.'
      )
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Load dashboard on component mount
  useEffect(() => {
    loadDashboard()
  }, [loadDashboard])

  // Auto-refresh every 60 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      loadDashboard()
    }, 60000)
    return () => clearInterval(interval)
  }, [loadDashboard])

  // Calculate KPI metrics from API response
  const calculateMetrics = () => {
    if (!dashboardData) {
      return {
        totalInsights: 0,
        themesFound: 0,
        topPriorityScore: 0,
        segments: 0,
        avgImpact: 0
      }
    }

    // Get all themes from all segments
    const allThemes = dashboardData.segments 
      ? dashboardData.segments.flatMap(s => s.themes || [])
      : []
    
    const topScore = allThemes.length > 0 
      ? Math.max(...allThemes.map(t => parseFloat(t.priority_score) || 0))
      : 0
    
    const avgImpact = allThemes.length > 0
      ? (allThemes.reduce((sum, t) => sum + (parseFloat(t.business_impact) || 0), 0) / allThemes.length).toFixed(1)
      : 0

    return {
      totalInsights: dashboardData.total_themes ? dashboardData.total_themes * 10 : allThemes.reduce((sum, t) => sum + (t.insight_count || 0), 0),
      themesFound: allThemes.length,
      topPriorityScore: topScore.toFixed(1),
      segments: dashboardData.total_segments || dashboardData.segments.length,
      avgImpact
    }
  }

  const metrics = calculateMetrics()

  // Get all themes (for charts)
  const allThemes = dashboardData && dashboardData.segments
    ? dashboardData.segments.flatMap(s => s.themes || [])
    : []

  // Get recent themes
  const recentThemes = allThemes.slice(0, 5)

  // Filter themes by segment if selected
  const filteredThemes = filteredSegment
    ? dashboardData?.segments
        ?.filter(s => s.segment === filteredSegment)
        .flatMap(s => s.themes || [])
    : allThemes

  if (isLoading && !dashboardData) {
    return <LoadingSpinner message="Loading Dashboard..." />
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Header */}
        <Header
          totalThemes={metrics.themesFound}
          totalSegments={metrics.segments}
          timestamp={dashboardData?.report_timestamp || lastRefresh.toISOString()}
          isLoading={isLoading}
        />

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Error Alert */}
          {error && (
            <ErrorAlert
              error={error}
              onRetry={loadDashboard}
              showRetry={true}
            />
          )}

          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <KPICard
              title="Total Insights"
              value={metrics.totalInsights}
              unit="insights"
              icon="📊"
              color="blue"
            />
            <KPICard
              title="Themes Found"
              value={metrics.themesFound}
              unit="themes"
              icon="🏷️"
              color="green"
            />
            <KPICard
              title="Top Priority"
              value={metrics.topPriorityScore}
              unit="/100"
              icon="⭐"
              color="orange"
            />
            <KPICard
              title="Avg Impact"
              value={metrics.avgImpact}
              unit="/5"
              icon="📈"
              color="purple"
            />
          </div>

          {/* Charts Section */}
          {dashboardData && allThemes.length > 0 && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
              {/* Top 5 Themes Chart */}
              <div className="bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
                <h2 className="text-2xl font-bold mb-6">Top 5 Priority Themes</h2>
                {allThemes.length > 0 ? (
                  <ThemeChart themes={allThemes.slice(0, 5)} />
                ) : (
                  <p className="text-gray-400">No theme data available</p>
                )}
              </div>

              {/* Segment Breakdown Chart */}
              <div className="bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
                <h2 className="text-2xl font-bold mb-6">Segment Breakdown</h2>
                {dashboardData.segments && dashboardData.segments.length > 0 ? (
                  <SegmentChart segments={dashboardData.segments} />
                ) : (
                  <p className="text-gray-400">No segment data available</p>
                )}
              </div>
            </div>
          )}

          {/* Segment Filter Tabs */}
          {dashboardData && dashboardData.segments && dashboardData.segments.length > 0 && (
            <div className="mb-8">
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setFilteredSegment(null)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    !filteredSegment
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  All Segments ({allThemes.length})
                </button>
                {dashboardData.segments.map(segment => (
                  <button
                    key={segment.segment}
                    onClick={() => setFilteredSegment(segment.segment)}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      filteredSegment === segment.segment
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    {segment.segment} ({segment.theme_count || segment.themes.length})
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Themes Grid */}
          {filteredThemes.length > 0 ? (
            <div className="mb-12">
              <h2 className="text-2xl font-bold mb-6">
                {filteredSegment ? `${filteredSegment} Themes` : 'All Themes'}
              </h2>
              <ThemeGrid
                themes={filteredThemes}
                onThemeClick={setSelectedTheme}
              />
            </div>
          ) : allThemes.length === 0 ? (
            <div className="bg-yellow-900 border border-yellow-700 rounded-lg p-8 text-center mb-12">
              <p className="text-yellow-100 text-lg mb-4">
                No themes found yet. Ingest data via the API to generate themes.
              </p>
              <p className="text-yellow-200 text-sm">
                Use POST /ingest to upload feedback texts
              </p>
            </div>
          ) : (
            <div className="bg-yellow-900 border border-yellow-700 rounded-lg p-8 text-center mb-12">
              <p className="text-yellow-100">
                No themes found in {filteredSegment || 'selected filter'}
              </p>
            </div>
          )}

          {/* Recent Themes Table */}
          {recentThemes.length > 0 && (
            <div className="mb-12">
              <h2 className="text-2xl font-bold mb-6">Recent Themes</h2>
              <RecentThemesTable
                themes={recentThemes}
                onThemeClick={setSelectedTheme}
              />
            </div>
          )}

          {/* Refresh Notice */}
          <div className="text-center text-gray-400 py-8 border-t border-gray-700">
            <p>Last updated: {lastRefresh.toLocaleTimeString()}</p>
            <p className="text-sm mt-2">Dashboard auto-refreshes every 60 seconds</p>
            <button
              onClick={loadDashboard}
              disabled={isLoading}
              className="mt-4 inline-block px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              {isLoading ? '⏳ Refreshing...' : '🔄 Refresh Now'}
            </button>
          </div>
        </main>

        {/* Theme Detail Modal */}
        {selectedTheme && (
          <ThemeDetailModal
            theme={selectedTheme}
            onClose={() => setSelectedTheme(null)}
          />
        )}

        {/* Footer */}
        <footer className="bg-gray-800 text-gray-400 border-t border-gray-700 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="font-semibold text-white mb-2">DiscoveryOS</h3>
                <p className="text-sm">
                  AI-powered product discovery platform
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-white mb-2">Status</h3>
                <p className={`text-sm ${error ? 'text-red-400' : 'text-green-400'}`}>
                  {error ? '🔴 Backend Error' : '🟢 Backend Connected'}
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-white mb-2">Built With</h3>
                <p className="text-sm">React 18 + Vite + Tailwind CSS</p>
              </div>
            </div>
            <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-500">
              <p>&copy; 2025 DiscoveryOS. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </ErrorBoundary>
  )
}

export default DashboardLayout
