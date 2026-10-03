import React from 'react';
import PropTypes from 'prop-types';
import './RecentRoundsTable.css';

const RecentRoundsTable = ({ history }) => {
  if (!history || history.length === 0) {
    return (
      <div className="recent-rounds-section">
        <div className="section-header">
          <h3>Recent Federated Rounds</h3>
          <p>No rounds completed yet</p>
        </div>
      </div>
    );
  }

  // Sort by round descending (most recent first)
  const sorted = [...history].sort((a, b) => b.round - a.round);
  // Take the latest 10 rounds
  const latestTen = sorted.slice(0, 10);

  return (
    <section className="recent-rounds-section">
      <div className="section-header">
        <h3>Recent Federated Rounds</h3>
        <p>Completed training rounds in the federated learning process</p>
      </div>
      <div className="table-container">
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
            {latestTen.map((h) => {
              const formattedTime = new Date(h.timestamp * 1000).toLocaleString(
                undefined,
                {
                  month: 'short',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                }
              );

              return (
                <tr key={h.round}>
                  <td>{h.round}</td>
                  <td>{h.loss.toFixed(4)}</td>
                  <td>{h.dice !== null ? h.dice.toFixed(4) : 'N/A'}</td>
                  <td>{formattedTime}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
};

RecentRoundsTable.propTypes = {
  history: PropTypes.arrayOf(
    PropTypes.shape({
      round: PropTypes.number.isRequired,
      loss: PropTypes.number.isRequired,
      dice: PropTypes.oneOfType([PropTypes.number, PropTypes.null]),
      timestamp: PropTypes.number.isRequired
    })
  )
};

export default RecentRoundsTable;