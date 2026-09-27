import React from 'react'
import PropTypes from 'prop-types'
import './NodeStatus.css'

const NodeStatus = ({ latest, clientMetrics, loading }) => {
  // Loading state
  if (loading) {
    return (
      <div className="node-status loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading node status...</p>
      </div>
    )
  }

  // Empty state (no data)
  if (!latest && (!clientMetrics || Object.keys(clientMetrics).length === 0)) {
    return (
      <div className="node-status empty">
        <div className="empty-icon">🏥</div>
        <p className="empty-text">No node data available</p>
        <p className="empty-subtext">Waiting for federated learning to start...</p>
      </div>
    )
  }

  // Determine which clients we have data for
  const clientIds = clientMetrics ? Object.keys(clientMetrics).map(id => parseInt(id)) : []

  // If we have client metrics, use those; otherwise fall back to hardcoded for compatibility
  const nodesToShow = clientIds.length > 0
    ? clientIds.map(id => ({ id, name: `Hospital ${id}` }))
    : [
      { id: 1, name: 'Hospital 1' },
      { id: 2, name: 'Hospital 2' },
      { id: 3, name: 'Hospital 3' }
    ];

  const isOnline = !!latest

  return (
    <div className="node-status">
      {nodesToShow.map(node => {
        const nodeId = String(node.id);
        const clientData = clientMetrics && clientMetrics[nodeId]
          ? clientMetrics[nodeId]
          : [];

        // Get the most recent metrics for this client
        const latestClientData = clientData.length > 0
          ? clientData[clientData.length - 1]
          : null;

        const isClientOnline = latestClientData !== null;
        const cardClass = isClientOnline ? 'node-card online' : 'node-card offline';

        return (
          <div key={node.id} className={cardClass}>
            <h3>{node.name}</h3>
            <p className="status">{isClientOnline ? 'Online' : 'Offline'}</p>
            {isClientOnline && latestClientData && (
              <>
                <p className="detail">
                  Last round: {latestClientData.round}
                </p>
                <p className="detail">
                  Dice score: {latestClientData.dice.toFixed(4)}
                </p>
                <p className="detail">
                  Examples: {latestClientData.examples}
                </p>
                <p className="detail">
                  Last updated: {new Date(latestClientData.timestamp * 1000).toLocaleTimeString()}
                </p>
                {clientData.length > 1 && (
                  <p className="detail">
                    Participation: {clientData.length} rounds
                  </p>
                )}
              </>
            )}
            {!isClientOnline && latest && (
              <p className="detail">
                Last global round: {latest.round}
              </p>
            )}
          </div>
        );
      })}
    </div>
  )
};

NodeStatus.propTypes = {
  latest: PropTypes.shape({
    round: PropTypes.number
  }),
  clientMetrics: PropTypes.objectOf(
    PropTypes.arrayOf(
      PropTypes.shape({
        round: PropTypes.number.isRequired,
        dice: PropTypes.number.isRequired,
        examples: PropTypes.number.isRequired,
        timestamp: PropTypes.number.isRequired
      })
    )
  ),
  loading: PropTypes.bool
}

NodeStatus.defaultProps = {
  loading: false,
  clientMetrics: null
}

export default NodeStatus;
