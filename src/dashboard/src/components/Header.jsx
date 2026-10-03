import React from 'react';
import './Header.css';

const Header = ({ latest, history, clientMetrics, health }) => {
  // Calculate API connection status from health
  const apiStatus = health ? 'online' : 'offline';
  const apiStatusText = apiStatus === 'online' ? 'Online' : 'Offline';

  // Calculate last updated timestamp from latest or history
  let lastUpdatedTimestamp = null;
  if (latest && latest.timestamp) {
    lastUpdatedTimestamp = latest.timestamp;
  } else if (history.length > 0) {
    lastUpdatedTimestamp = history[history.length - 1].timestamp;
  }

  // Format last updated time (e.g., "2m ago", "Just now")
  const getLastUpdatedString = (timestamp) => {
    if (!timestamp) return '';
    const now = Math.floor(Date.now() / 1000);
    const diff = now - timestamp;
    if (diff < 5) return 'Just now';
    if (diff < 60) return `${diff}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    return `${Math.floor(diff / 3600)}h ago`;
  };
  const lastUpdatedString = getLastUpdatedString(lastUpdatedTimestamp);

  // Calculate active federation nodes: clients with data in the latest round
  let activeNodes = 0;
  let totalNodes = 0;
  if (clientMetrics && latest && latest.round > 0) {
    const latestRound = latest.round;
    totalNodes = Object.keys(clientMetrics).length;
    activeNodes = Object.values(clientMetrics).filter(clientData =>
      clientData.some(entry => entry.round === latestRound)
    ).length;
  } else {
    totalNodes = clientMetrics ? Object.keys(clientMetrics).length : 0;
  }

  // Get latest round from history or latest
  const latestRound = (latest && latest.round) ||
                     (history.length > 0 ? history[history.length - 1].round : 0);

  return (
    <header className="app-header">
      <div className="header-content">
        <div className="brand-section">
          <div className="brand-mark">FM</div>
          <div className="brand-text">
            <h1>FedMed</h1>
            <p className="tagline">Federated Healthcare Intelligence</p>
          </div>
        </div>

        <div className="header-status">
          <div className="status-item">
            <div className="status-label">API STATUS</div>
            <div className="status-value">
              <span className={`status-dot ${apiStatus}`} />
              {apiStatusText}
              {lastUpdatedString && (
                <span className="status-detail">{lastUpdatedString}</span>
              )}
            </div>
          </div>

          <div className="status-item">
            <div className="status-label">ACTIVE NODES</div>
            <div className="status-value">
              {activeNodes} / {totalNodes}
            </div>
          </div>

          <div className="status-item">
            <div className="status-label">CURRENT ROUND</div>
            <div className="status-value">
              Round {latestRound}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;