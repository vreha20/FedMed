import React, { useState, useEffect } from 'react'
import {
  fetchLatest,
  fetchHistory,
  fetchHealth,
  fetchClientMetrics,
  fetchSecurity
} from './services/api'

import MetricsDisplay from './components/MetricsDisplay'
import MetricsHistory from './components/MetricsHistory'
import NodeStatus from './components/NodeStatus'
import SecurityPanel from './components/SecurityPanel'

import './styles/App.css'

function App() {
  const [latest, setLatest] = useState(null)
  const [history, setHistory] = useState([])
  const [health, setHealth] = useState(null)
  const [clientMetrics, setClientMetrics] = useState(null)
  const [security, setSecurity] = useState(null)
  const [securityLoading, setSecurityLoading] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = async () => {
    setLoading(true)
    setSecurityLoading(true)
    setError(null)

    try {
      // Use real data from APIs
      const [
        latestRes,
        historyRes,
        healthRes,
        clientMetricsRes,
        securityRes
      ] = await Promise.all([
        fetchLatest(),
        fetchHistory(),
        fetchHealth(),
        fetchClientMetrics(),
        fetchSecurity()
      ])

      setLatest(latestRes)
      setHistory(historyRes)
      setHealth(healthRes)
      setClientMetrics(clientMetricsRes)
      setSecurity(securityRes)
    } catch (err) {
      setError(err.message || 'Unknown error')
      console.error('Failed to fetch dashboard data:', err)
    } finally {
      setLoading(false)
      setSecurityLoading(false)
    }
  }

  useEffect(() => {
    fetchData()

    const interval = setInterval(fetchData, 5000)

    return () => clearInterval(interval)
  }, [])

  if (
    loading &&
    latest === null &&
    history.length === 0 &&
    clientMetrics === null
  ) {
    return (
      <div className="container">
        <div className="loading-state">
          <div className="loading-spinner" />

          <h2>Loading FedMed</h2>

          <p>
            Connecting to federated learning services...
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">

          <div className="error-icon">
            !
          </div>

          <h2>
            Unable to load dashboard
          </h2>

          <p>
            {error}
          </p>

          <button onClick={fetchData}>
            Retry Connection
          </button>

        </div>
      </div>
    )
  }

  return (
    <div className="container">

      {/* ==================== HEADER ==================== */}

      <header className="app-header">

        <div className="brand-section">

          <div className="brand-mark">
            FM
          </div>

          <div className="brand-content">

            <h1>
              FedMed
            </h1>

            <p className="subtitle">
              Federated Healthcare Intelligence
            </p>

          </div>

        </div>

        <div className="header-status">

          <span
            className={`status-dot ${
              health ? 'online' : 'offline'
            }`}
          />

          <div className="status-content">

            <span className="status-label">
              {health
                ? 'System Online'
                : 'System Offline'}
            </span>

            <span className="status-description">
              {health
                ? 'Federation services operational'
                : 'Unable to reach server'}
            </span>

          </div>

        </div>

      </header>


      {/* ==================== DASHBOARD ==================== */}

      <main className="dashboard-content">

        {/* KPI SECTION */}

        <section className="kpi-cards">

          <div className="section-heading">

            <div>

              <h2>
                Federation Overview
              </h2>

              <p>
                Real-time global model performance
              </p>

            </div>

          </div>

          <MetricsDisplay
            latest={latest}
            loading={loading}
          />

        </section>


        {/* NODE STATUS */}

        <section className="node-status">

          <div className="section-heading">

            <div>

              <h2>
                Federation Nodes
              </h2>

              <p>
                Connected healthcare training nodes
              </p>

            </div>

            <span className="live-badge">
              LIVE
            </span>

          </div>

          <NodeStatus
            latest={latest}
            clientMetrics={clientMetrics}
            loading={loading}
          />

        </section>


        {/* TRAINING PROGRESS */}

        <section className="visualization">

          <div className="section-heading">

            <div>

              <h2>
                Training Progress
              </h2>

              <p>
                Global model convergence across federated rounds
              </p>

            </div>

          </div>

          <MetricsHistory
            history={history}
            loading={loading}
          />

        </section>


        {/* PRIVACY & SECURITY */}

        <SecurityPanel
          security={security}
          loading={securityLoading}
        />

      </main>


      {/* ==================== FOOTER ==================== */}

      <footer className="app-footer">

        <span>
          FedMed
        </span>

        <span className="footer-divider">
          •
        </span>

        <span>
          Privacy-Preserving Federated Learning
        </span>

        <span className="footer-divider">
          •
        </span>

        <span>
          © {new Date().getFullYear()}
        </span>

      </footer>

    </div>
  )
}

export default App