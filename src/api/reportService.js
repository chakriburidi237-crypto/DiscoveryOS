import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

/**
 * Fetch the report with all themes grouped by segment
 * @returns {Promise<Object>} Report data with segments and themes
 */
export const fetchReport = async () => {
  try {
    const response = await apiClient.get('/report')
    return response.data
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      throw new Error(
        `API Error: ${error.response.status} - ${
          error.response.data?.detail || 'Failed to fetch report'
        }`
      )
    } else if (error.request) {
      // Request made but no response received
      throw new Error(
        'Network Error: No response from server. Is the backend running?'
      )
    } else {
      throw new Error(`Error: ${error.message}`)
    }
  }
}

/**
 * Fetch health check status
 * @returns {Promise<Object>} Health status
 */
export const fetchHealth = async () => {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error) {
    throw new Error('Backend is not available')
  }
}

export default apiClient
