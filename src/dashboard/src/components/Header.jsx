import React from 'react';
import './Header.css';

const Header = ({ latest, history, clientMetrics, health }) => {
  // Calculate system status from health
  const systemStatus = health ? 'online' : 'offline';
  const systemStatusText = health ? 'Operational' : 'Offline';

  // Calculate federation status: number of connected clients
  let connectedNodes = 0;
  let totalNodes = 0;
  if (clientMetrics) {
    totalNodes = Object.keys(clientMetrics).length;
    // A node is considered connected if it has at least one entry in clientMetrics
    connectedNodes = totalNodes; // In our setup, if they are in clientMetrics, they have participated
  } else {
    // If we don't have clientMetrics, we can't know, so assume 0
    totalNodes = 3; // We expect 3 nodes
    connectedNodes = 0;
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
            <div className="status-label">SYSTEM STATUS</div>
            <div className="status-value">
              <span className={`status-dot ${systemStatus}`} />
              {systemStatusText}
            </div>
          </div>

          <div className="status-item">
            <div className="status-label">FEDERATION</div>
            <div className="status-value">
              {connectedNodes} / {totalNodes} NODES
            </div>
          </div>

          <div className="status-item">
            <div className="status-label">LATEST ROUND</div>
            <div className="status-value">Round {latestRound}</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;