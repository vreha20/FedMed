import React from 'react';
import './SystemArchitecture.css';

const SystemArchitecture = () => {
  return (
    <section className="architecture-section">
      <div className="architecture-header">
        <h2>Federated Learning Architecture</h2>
        <p>How FedMed orchestrates privacy-preserving collaborative learning</p>
      </div>
      <div className="architecture-diagram">
        {/* Federation Nodes */}
        <div className="architecture-nodes">
          <div className="architecture-node">
            <div className="node-icon">🏥</div>
            <div className="node-label">Federation Nodes</div>
            <div className="node-detail">Local Data: Never Shared</div>
          </div>
        </div>

        {/* Arrows to Local Model Training */}
        <div className="architecture-arrows-top">
          <div className="architecture-arrow"></div>
        </div>

        {/* Local Model Training */}
        <div className="architecture-node">
          <div className="node-icon">💻</div>
          <div className="node-label">Local Model Training</div>
          <div className="node-detail">Private Computation on Local Data</div>
        </div>

        {/* Arrows to Model Updates */}
        <div className="architecture-arrows-top">
          <div className="architecture-arrow"></div>
        </div>

        {/* Model Updates */}
        <div className="architecture-node">
          <div className="node-icon">📤</div>
          <div className="node-label">Model Updates</div>
          <div className="node-detail">Model Updates Shared</div>
        </div>

        {/* Arrows to FedAvg Aggregation */}
        <div className="architecture-arrows-top">
          <div className="architecture-arrow"></div>
        </div>

        {/* Federated Aggregation (Server) */}
        <div className="architecture-aggregation">
          <div className="aggregation-icon">⚙️</div>
          <div className="aggregation-label">FedAvg Aggregation</div>
          <div className="aggregation-detail">Model Update Aggregation</div>
        </div>

        {/* Arrow to Global Model */}
        <div className="architecture-arrows-top">
          <div className="architecture-arrow"></div>
        </div>

        {/* Global Model */}
        <div className="architecture-global-model">
          <div className="global-model-icon">🌐</div>
          <div className="global-model-label">Global Model</div>
          <div className="global-model-detail">Improved AI for Healthcare</div>
          <div className="global-model-note">
            * Raw data remains at each hospital • Only model updates shared
          </div>
        </div>

        {/* Arrow to Metrics / Dashboard */}
        <div className="architecture-arrows-top">
          <div className="architecture-arrow"></div>
        </div>

        {/* Metrics / Dashboard */}
        <div className="architecture-node">
          <div className="node-icon">📊</div>
          <div className="node-label">Metrics & Dashboard</div>
          <div className="node-detail">Real-time Monitoring & Analytics</div>
        </div>
      </div>
    </section>
  );
};

export default SystemArchitecture;