import React from 'react'
import PropTypes from 'prop-types'
import './MetricsDisplay.css'

const MetricsDisplay = ({ latest }) => {
  if (!latest) {
    return <div className="metrics-display empty">No data available</div>
  }

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
        <h3>Accuracy</h3>
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
  })
}

export default MetricsDisplay
