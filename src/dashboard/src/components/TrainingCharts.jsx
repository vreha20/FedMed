import React from 'react';
import './TrainingCharts.css';

const TrainingCharts = ({ history }) => {
  if (!history || history.length === 0) {
    return (
      <section className="charts-section">
        <div className="charts-empty">
          <h3>Training Performance</h3>
          <p>No training data available yet</p>
        </div>
      </section>
    );
  }

  // Sort history by round ascending
  const sortedHistory = [...history].sort((a, b) => a.round - b.round);
  const rounds = sortedHistory.map(item => item.round);
  const lossValues = sortedHistory.map(item => item.loss);
  const diceValuesRaw = sortedHistory.map(item => item.dice);

  // Filter out null dice for min/max calculation
  const diceValuesNonNull = diceValuesRaw.filter(v => v !== null);
  const hasDiceData = diceValuesNonNull.length > 0;

  // Find min and max for loss (assuming no nulls in loss)
  const minLoss = Math.min(...lossValues);
  const maxLoss = Math.max(...lossValues);

  // Find min and max for dice (only non-null)
  let minDice = 0;
  let maxDice = 1;
  if (hasDiceData) {
    minDice = Math.min(...diceValuesNonNull);
    maxDice = Math.max(...diceValuesNonNull);
  }

  // Add padding to avoid points touching the edges
  const lossRange = maxLoss - minLoss;
  const diceRange = maxDice - minDice;
  const lossPadding = lossRange * 0.1;
  const dicePadding = diceRange * 0.1;
  const lossMin = minLoss - lossPadding;
  const lossMax = maxLoss + lossPadding;
  const diceMin = minDice - dicePadding;
  const diceMax = maxDice + dicePadding;

  // If range is zero, set a default range
  const lossRangeAdjusted = lossMax - lossMin || 1;
  const diceRangeAdjusted = diceMax - diceMin || 1;

  // Helper function to generate SVG path data for a line chart, handling nulls by breaking the line
  const drawLine = (xValues, yValues, yMin, yMax, validityFn) => {
    if (xValues.length === 0) return '';

    const xPadding = 50;
    const yPadding = 20;
    const chartWidth = 100;
    const chartHeight = 80;
    const range = yMax - yMin || 1;

    const points = [];
    let currentSegment = [];

    xValues.forEach((x, index) => {
      if (validityFn ? validityFn(xValues[index], yValues[index]) : yValues[index] !== null) {
        const xPos = xPadding + (index * (chartWidth / (xValues.length - 1 || 1)));
        const yPos = yPadding + chartHeight - (((yValues[index] - yMin) / range) * chartHeight);
        currentSegment.push(`${xPos},${yPos}`);
      } else {
        // If we have a current segment, add it to points and reset
        if (currentSegment.length > 0) {
          points.push(currentSegment.join(' L '));
          currentSegment = [];
        }
      }
    });

    // Add the last segment if exists
    if (currentSegment.length > 0) {
      points.push(currentSegment.join(' L '));
    }

    // Return the path data for all segments
    return points.map(segment => `M ${segment}`).join(' ');
  };

  return (
    <section className="charts-section">
      <div className="section-header">
        <h2>Training Performance</h2>
        <p>Loss and Dice Score across federated rounds</p>
      </div>
      <div className="charts-container">
        <div className="chart-panel">
          <h3>Loss (Lower is Better)</h3>
          <div className="chart-wrapper">
            <svg className="training-chart" viewBox="0 0 200 120" aria-label="Loss Chart">
              {/* Grid lines */}
              <line x1="0" y1="20" x2="200" y2="20" className="grid-line" />
              <line x1="0" y1="40" x2="200" y2="40" className="grid-line" />
              <line x1="0" y1="60" x2="200" y2="60" className="grid-line" />
              <line x1="0" y1="80" x2="200" y2="80" className="grid-line" />
              <line x1="0" y1="100" x2="200" y2="100" className="grid-line" />

              {/* X-axis labels (rounds) */}
              {rounds.map((round, index) => {
                const x = 50 + (index * (100 / (rounds.length - 1 || 1)));
                return (
                  <text key={round} x={x} y="115" textAnchor="middle" fontSize="10" fill="#94a3b8">
                    R{round}
                  </text>
                );
              })}

              {/* Y-axis labels for loss */}
              {[0, 0.25, 0.5, 0.75, 1].map(percent => {
                const value = lossMin + (lossRangeAdjusted * percent);
                const y = 100 - (percent * 80);
                return (
                  <text key={value} x="40" y={y} textAnchor="end" fontSize="10" fill="#94a3b8">
                    {value.toFixed(3)}
                  </text>
                );
              })}

              {/* Loss line */}
              <path
                d={drawLine(rounds, lossValues, lossMin, lossMax)}
                className="chart-line loss-line"
              />
              {/* Loss points */}
              {rounds.map((round, index) => {
                const x = 50 + (index * (100 / (rounds.length - 1 || 1)));
                const y = 100 - (((lossValues[index] - lossMin) / lossRangeAdjusted) * 80);
                return (
                  <circle key={round} cx={x} cy={y} r="4" className="chart-point loss-point" />
                );
              })}
            </svg>
          </div>
        </div>

        <div className="chart-panel">
          <h3>Dice Score (Higher is Better)</h3>
          <div className="chart-wrapper">
            <svg className="training-chart" viewBox="0 0 200 120" aria-label="Dice Chart">
              {/* Grid lines */}
              <line x1="0" y1="20" x2="200" y2="20" className="grid-line" />
              <line x1="0" y1="40" x2="200" y2="40" className="grid-line" />
              <line x1="0" y1="60" x2="200" y2="60" className="grid-line" />
              <line x1="0" y1="80" x2="200" y2="80" className="grid-line" />
              <line x1="0" y1="100" x2="200" y2="100" className="grid-line" />

              {/* X-axis labels (rounds) */}
              {rounds.map((round, index) => {
                const x = 50 + (index * (100 / (rounds.length - 1 || 1)));
                return (
                  <text key={round} x={x} y="115" textAnchor="middle" fontSize="10" fill="#94a3b8">
                    R{round}
                  </text>
                );
              })}

              {/* Y-axis labels for dice */}
              {[0, 0.25, 0.5, 0.75, 1].map(percent => {
                const value = diceMin + (diceRangeAdjusted * percent);
                const y = 100 - (percent * 80);
                return (
                  <text key={value} x="40" y={y} textAnchor="end" fontSize="10" fill="#94a3b8">
                    {hasDiceData ? value.toFixed(4) : '0.0000'}
                  </text>
                );
              })}

              {/* Dice line */}
              <path
                d={drawLine(rounds, diceValuesRaw, diceMin, diceMax, (_, val) => val !== null)}
                className="chart-line dice-line"
              />
              {/* Dice points - only for non-null dice */}
              {sortedHistory.map((item, index) => {
                if (item.dice !== null) {
                  const x = 50 + (index * (100 / (rounds.length - 1 || 1)));
                  const y = 100 - (((item.dice - diceMin) / diceRangeAdjusted) * 80);
                  return (
                    <circle key={item.round} cx={x} cy={y} r="4" className="chart-point dice-point" />
                  );
                }
                return null;
              })}
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TrainingCharts;