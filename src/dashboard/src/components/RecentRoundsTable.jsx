import React from 'react'
import PropTypes from 'prop-types'
import './RecentRoundsTable.css'

const RecentRoundsTable = ({ history }) => {
  if (!history || history.length === 0) {
    return <div className="recent-rounds-table empty">No rounds yet</div>
  }

  const sorted = [...history].sort((a, b) => b.round - a.round)
  const latestTen = sorted.slice(0, 10)

  return (
    <div className="recent-rounds-table">
      <h3>Recent Rounds</h3>
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
          {latestTen.map((h) => (
            <tr key={h.round}>
              <td>{h.round}</td>
              <td>{h.loss.toFixed(4)}</td>
              <td>{h.dice !== null ? h.dice.toFixed(4) : 'N/A'}</td>
              <td>{new Date(h.timestamp * 1000).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

RecentRoundsTable.propTypes = {
  history: PropTypes.arrayOf(
    PropTypes.shape({
      round: PropTypes.number.isRequired,
      loss: PropTypes.number.isRequired,
      dice: PropTypes.oneOfType([PropTypes.number, PropTypes.null]),
      timestamp: PropTypes.number.isRequired
    })
  )
}

export default RecentRoundsTable;
