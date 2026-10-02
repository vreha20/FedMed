import React, { useState, useEffect } from 'react';
import {
  fetchLatest,
  fetchHistory,
  fetchClientMetrics,
  fetchSecurity,
  fetchHealth
} from './services/api';

import Header from './components/Header';
import KPISection from './components/KPISection';
import FederationNodes from './components/FederationNodes';
import TrainingCharts from './components/TrainingCharts';
import RecentRoundsTable from './components/RecentRoundsTable';
import SecurityPanel from './components/SecurityPanel';
import SystemArchitecture from './components/SystemArchitecture';

import './styles/App.css';

function App() {
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);
  const [clientMetrics, setClientMetrics] = useState(null);
  const [security, setSecurity] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [
        latestRes,
        historyRes,
        clientMetricsRes,
        securityRes,
        healthRes
      ] = await Promise.all([
        fetchLatest(),
        fetchHistory(),
        fetchClientMetrics(),
        fetchSecurity(),
        fetchHealth()
      ]);

      setLatest(latestRes);
      setHistory(historyRes);
      setClientMetrics(clientMetricsRes);
      setSecurity(securityRes);
      setHealth(healthRes);
    } catch (err) {
      setError(err.message || 'Unknown error');
      console.error('Failed to fetch dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  if (loading && !latest && history.length === 0 && !clientMetrics) {
    return (
      <div className="app-container">
        <div className="loading-state">
          <div className="loading-spinner" />
          <h2>Loading FedMed</h2>
          <p>Connecting to federated learning services...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="error-state">
          <div className="error-icon">!</div>
          <h2>Unable to load dashboard</h2>
          <p>{error}</p>
          <button onClick={fetchData}>Retry Connection</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Header
        latest={latest}
        history={history}
        clientMetrics={clientMetrics}
        health={health}
      />
      <main className="dashboard-content">
        <section className="kpi-section">
          <KPISection
            latest={latest}
            history={history}
            clientMetrics={clientMetrics}
          />
        </section>

        <section className="nodes-section">
          <FederationNodes
            clientMetrics={clientMetrics}
          />
        </section>

        <section className="charts-section">
          <TrainingCharts
            history={history}
          />
        </section>

        <section className="table-section">
          <RecentRoundsTable
            history={history}
          />
        </section>

        <section className="security-section">
          <SecurityPanel
            security={security}
          />
        </section>

        <section className="architecture-section">
          <SystemArchitecture />
        </section>
      </main>
      <footer className="app-footer">
        <span>
          FedMed
        </span>
        <span className="footer-divider">•</span>
        <span>
          Privacy-Preserving Federated Learning
        </span>
        <span className="footer-divider">•</span>
        <span>
          © {new Date().getFullYear()}
        </span>
      </footer>
    </div>
  );
}

export default App;