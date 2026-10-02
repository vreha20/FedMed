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
        {/* Hospital Nodes */}
        <div className="architecture-nodes">
          <div className="architecture-node">
            <div className="node-icon">🏥</div>
            <div className="node-label">Federation Node A</div>
            <div className="node-detail">Local Data: Never Shared</div>
          </div>
          <div className="architecture-node">
            <div className="node-icon">🏥</div>
            <div className="node-label">Federation Node B</div>
            <div className="node-detail">Local Data: Never Shared</div>
          </div>
          <div className="architecture-node">
            <div className="node-icon">🏥</div>
            <div className="node-label">Federation Node C</div>
            <div className="node-detail">Local Data: Never Shared</div>
          </div>
        </div>

        {/* Arrows to Aggregation */}
        <div className="architecture-arrows-top">
          <div className="architecture-arrow"></div>
          <div className="architecture-arrow"></div>
          <div className="architecture-arrow"></div>
        </div>

        {/* Federated Aggregation (Server) */}
        <div className="architecture-aggregation">
          <div className="aggregation-icon">⚙️</div>
          <div className="aggregation-label">Federated Aggregation Server</div>
          <div className="aggregation-detail">Model updates aggregated with FedAvg</div>
        </div>

        {/* Arrow to Global Model */}
        <div className="architecture-arrows-bottom">
          <div className="architecture-arrow"></div>
        </div>

        {/* Global Model */}
        <div className="architecture-global-model">
          <div className="global-model-icon">🌐</div>
          <div className="global-model-label">Global Model</div>
          <div className="global-model-detail">Improved AI for Healthcare</div>
          <div className="global-model-note">* Raw data remains at each hospital • Only model updates shared</div>
        </div>
      </div>
    </section>
  );
};

export default SystemArchitecture;