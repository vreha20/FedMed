const API_BASE = ''

export const fetchLatest = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/metrics`)
    if (response.status === 404) {
      return null
    }
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (err) {
    throw err
  }
}

export const fetchHistory = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/metrics/history`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (err) {
    throw err
  }
}

export const fetchHealth = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/health`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (err) {
    throw err
  }
}
