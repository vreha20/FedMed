import React from 'react'
import PropTypes from 'prop-types'
import './NodeStatus.css'

const NodeStatus = ({ latest }) => {
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
  })
};

export default NodeStatus;
