import React from 'react'
import PropTypes from 'prop-types'
import './NodeStatus.css'

const NodeStatus = ({ latest, loading }) => {
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
  if (!latest) {
    return (
      <div className="node-status empty">
        <div className="empty-icon">🏥</div>
        <p className="empty-text">No node data available</p>
        <p className="empty-subtext">Waiting for federated learning to start...</p>
      </div>
    )
  }

  const nodes = [
    { id: 1, name: 'Hospital 1' },
    { id: 2, name: 'Hospital 2' },
    { id: 3, name: 'Hospital 3' }
  ]

  const isOnline = !!latest

  return (
    <div className="node-status">
      {nodes.map(node => {
        const cardClass = isOnline ? 'node-card online' : 'node-card offline';
        return (
          <div key={node.id} className={cardClass}>
            <h3>{node.name}</h3>
            <p className="status">{isOnline ? 'Online' : 'Offline'}</p>
            {latest && (
              <p className="detail">
                Last round: {latest.round}
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
  loading: PropTypes.bool
}

NodeStatus.defaultProps = {
  loading: false
}

export default NodeStatus;
