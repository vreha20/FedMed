import React from 'react';
import './NodeCard.css';

const NodeCard = ({ clientId, clientData }) => {
  // Sort data by round ascending to get latest
  const sortedData = [...clientData].sort((a, b) => a.round - b.round);
  const latestEntry = sortedData[sortedData.length - 1];
  const participationCount = sortedData.length;

  // Determine connection status: if there is any data, consider reporting
  // We'll check if there is data from the latest round (within a reasonable time)
  // For simplicity, we'll say if there is data, it's reporting; otherwise, no recent data
  const isReporting = clientData.length > 0;
  const hasRecentData = latestEntry && (Date.now() / 1000 - latestEntry.timestamp) < 3600; // within last hour

  // Format the latest dice and loss (we don't have loss in clientMetrics, only dice)
  // The clientMetrics from backend only has dice, examples, round, timestamp
  const latestDice = latestEntry ? latestEntry.dice : 0;
  const latestExamples = latestEntry ? latestEntry.examples : 0;
  const latestTimestamp = latestEntry ? latestEntry.timestamp : 0;

  // Format timestamp to HH:MM
  const formattedTime = latestTimestamp
    ? new Date(latestTimestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : '--:--';

  return (
    <div className="node-card">
      <div className="node-card-header">
        <h3>Federation Node {clientId}</h3>
        <div className="node-status">
          <span className={`status-dot ${isReporting && hasRecentData ? 'connected' : 'disconnected'}`} />
          <span>{isReporting && hasRecentData ? 'Reporting' : 'No recent data'}</span>
        </div>
      </div>

      <div className="node-card-body">
        <div className="node-metric">
          <div className="metric-label">Last Round</div>
          <div className="metric-value">{latestEntry ? latestEntry.round : 'N/A'}</div>
        </div>

        <div className="node-metric">
          <div className="metric-label">Dice Score</div>
          <div className="metric-value">{latestDice !== undefined ? latestDice.toFixed(4) : 'N/A'}</div>
        </div>

        <div className="node-metric">
          <div className="metric-label">Training Examples</div>
          <div className="metric-value">{latestExamples}</div>
        </div>

        <div className="node-metric">
          <div className="metric-label">Participation</div>
          <div className="metric-value">{participationCount} rounds</div>
        </div>

        <div className="node-metric">
          <div className="metric-label">Last Updated</div>
          <div className="metric-value">{formattedTime}</div>
        </div>
      </div>
    </div>
  );
};

export default NodeCard;