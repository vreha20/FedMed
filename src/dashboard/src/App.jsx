import React, { useState, useEffect } from 'react'
import { fetchLatest, fetchHistory, fetchHealth, fetchClientMetrics } from './services/api'
import MetricsDisplay from './components/MetricsDisplay'
import MetricsHistory from './components/MetricsHistory'
import NodeStatus from './components/NodeStatus'
import './styles/App.css'

function App() {
  const [latest, setLatest] = useState(null)
  const [history, setHistory] = useState([])
  const [health, setHealth] = useState(null)
  const [clientMetrics, setClientMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [latestRes, historyRes, healthRes, clientMetricsRes] = await Promise.all([
        fetchLatest(),
        fetchHistory(),
        fetchHealth(),
        fetchClientMetrics()
      ])
      setLatest(latestRes)
      setHistory(historyRes)
      setHealth(healthRes)
      setClientMetrics(clientMetricsRes)
    } catch (err) {
      setError(err.message || 'Unknown error')
      console.error('Failed to fetch metrics:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000) // poll every 5 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading && latest === null && history.length === 0 && clientMetrics === null) {
    return <div className="container">Loading dashboard data...</div>
  }

  if (error) {
    return (
      <div className="container error">
        <h2>Error loading data</h2>
        <p>{error}</p>
        <button onClick={fetchData}>Retry</button>
      </div>
    )
  }

  return (
    <div className="container">
      <header className="app-header">
        <h1>FedMed Federated Learning Dashboard</h1>
        <div className="status-indicator">
          {health ? (
            <span className="status status-ok">Server: Online</span>
          ) : (
            <span className="status status-offline">Server: Offline</span>
          )}
        </div>
      </header>

      <main className="dashboard-content">
        <section className="kpi-cards">
          <MetricsDisplay latest={latest} loading={loading} />
        </section>

        <section className="node-status">
          <h2>Federation Nodes</h2>
          <NodeStatus latest={latest} clientMetrics={clientMetrics} loading={loading} />
        </section>

        <section className="visualization">
          <h2>Training Progress</h2>
          <MetricsHistory history={history} loading={loading} />
        </section>
      </main>

      <footer className="app-footer">
        <p>FedMed &copy; {new Date().getFullYear()} | Federated Learning Engine</p>
      </footer>
    </div>
  )
}

export default App
