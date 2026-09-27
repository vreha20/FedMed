import React from 'react'
import PropTypes from 'prop-types'
import './MetricsDisplay.css'

const MetricsDisplay = ({ latest, loading }) => {
  // Loading state
  if (loading) {
    return (
      <div className="metrics-display loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Fetching latest metrics...</p>
      </div>
    )
  }

  // Empty state (no data)
  if (!latest) {
    return (
      <div className="metrics-display empty">
        <div className="empty-icon">⚠️</div>
        <p className="empty-text">No metrics data available</p>
        <p className="empty-subtext">Waiting for federated learning to start...</p>
      </div>
    )
  }

  // Data available
  const { round, loss, accuracy, timestamp } = latest
  const date = timestamp ? new Date(timestamp * 1000).toLocaleTimeString() : 'N/A'

  return (
    <div className="metrics-display">
      <div className="kpi-card">
        <h3>Current Round</h3>
        <p className="value">{round}</p>
      </div>
      <div className="kpi-card">
        <h3>Loss</h3>
        <p className="value">{loss.toFixed(4)}</p>
      </div>
      <div className="kpi-card">
        <h3>Dice Score</h3>
        <p className="value">
          {accuracy !== null ? accuracy.toFixed(4) : 'N/A'}
        </p>
      </div>
      <div className="kpi-card">
        <h3>Last Updated</h3>
        <p className="value">{date}</p>
      </div>
    </div>
  )
}

MetricsDisplay.propTypes = {
  latest: PropTypes.shape({
    round: PropTypes.number,
    loss: PropTypes.number,
    accuracy: PropTypes.oneOfType([PropTypes.number, PropTypes.null]),
    timestamp: PropTypes.number
  }),
  loading: PropTypes.bool
}

MetricsDisplay.defaultProps = {
  loading: false
}

export default MetricsDisplay
