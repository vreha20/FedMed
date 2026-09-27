import React from 'react'
import PropTypes from 'prop-types'
import './MetricsHistory.css'

const MetricsHistory = ({ history, loading }) => {
  // Loading state
  if (loading) {
    return (
      <div className="metrics-history loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading training history...</p>
      </div>
    )
  }

  // Empty state (no data)
  if (!history || history.length === 0) {
    return (
      <div className="metrics-history empty">
        <div className="empty-icon">📊</div>
        <p className="empty-text">No training history available</p>
        <p className="empty-subtext">Waiting for federated learning rounds to complete...</p>
      </div>
    )
  }

  // Prepare data for simple bar chart
  const lossData = history.map(h => h.loss)
  const accData = history.map(h => h.accuracy !== null ? h.accuracy : 0)

  const maxLoss = Math.max(...lossData) || 1
  const maxAcc = Math.max(...accData) || 1

  return (
    <div className="metrics-history">
      <div className="chart-container">
        <h3>Loss / Dice Score Over Rounds</h3>
        <div className="chart">
          {history.map((h) => {
            const lossPct = (h.loss / maxLoss) * 100
            const accPct = (h.accuracy !== null ? (h.accuracy / maxAcc) * 100 : 0)
            const lossPctStr = lossPct + '%'
            const accPctStr = accPct + '%'
            return (
              <div key={h.round} className="chart-group">
                <div className="chart-bar loss" style={{ height: lossPctStr }} title={'Loss: ' + h.loss.toFixed(4)} />
                <div className="chart-bar acc" style={{ height: accPctStr }} title={'Dice Score: ' + (h.accuracy !== null ? h.accuracy.toFixed(4) : 'N/A')} />
                <div className="chart-label">R{h.round}</div>
              </div>
            )
          })}
        </div>
      </div>

      <div className="history-table">
        <h3>Recent Rounds Table</h3>
        <table>
          <thead>
            <tr>
              <th>Round</th>
              <th>Loss</th>
              <th>Dice Score</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {history.slice(-10).map((h) => (
              <tr key={h.round}>
                <td>{h.round}</td>
                <td>{h.loss.toFixed(4)}</td>
                <td>{h.accuracy !== null ? h.accuracy.toFixed(4) : 'N/A'}</td>
                <td>{new Date(h.timestamp * 1000).toLocaleTimeString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

MetricsHistory.propTypes = {
  history: PropTypes.arrayOf(
    PropTypes.shape({
      round: PropTypes.number.isRequired,
      loss: PropTypes.number.isRequired,
      accuracy: PropTypes.oneOfType([PropTypes.number, PropTypes.null]),
      timestamp: PropTypes.number.isRequired
    })
  ),
  loading: PropTypes.bool
}

MetricsHistory.defaultProps = {
  loading: false
}

export default MetricsHistory;
