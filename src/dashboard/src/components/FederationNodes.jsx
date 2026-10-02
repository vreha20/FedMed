import React from 'react';
import NodeCard from './NodeCard';
import './FederationNodes.css';

const FederationNodes = ({ clientMetrics }) => {
  if (!clientMetrics) {
    return (
      <section className="nodes-section">
        <div className="section-header">
          <h2>Federation Nodes</h2>
          <p>Waiting for node data...</p>
        </div>
      </section>
    );
  }

  const nodes = Object.entries(clientMetrics).map(([clientId, data]) => ({
    id: clientId,
    data
  }));

  return (
    <section className="nodes-section">
      <div className="section-header">
        <h2>Federation Nodes</h2>
        <p>Participating healthcare nodes in the federated learning network</p>
      </div>
      <div className="nodes-grid">
        {nodes.map(({ id, data }) => (
          <NodeCard key={id} clientId={id} clientData={data} />
        ))}
      </div>
    </section>
  );
};

export default FederationNodes;