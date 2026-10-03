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

    const xPadding = 60;
    const yPadding = 40;
    const chartWidth = 200;
    const chartHeight = 120;
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

  // Helper function to get point coordinates for plotting
  const getPointCoords = (xValues, yValues, yMin, yMax, validityFn) => {
    const coords = [];
    const xPadding = 60;
    const yPadding = 40;
    const chartWidth = 200;
    const chartHeight = 120;
    const range = yMax - yMin || 1;

    xValues.forEach((x, index) => {
      if (validityFn ? validityFn(xValues[index], yValues[index]) : yValues[index] !== null) {
        const xPos = xPadding + (index * (chartWidth / (xValues.length - 1 || 1)));
        const yPos = yPadding + chartHeight - (((yValues[index] - yMin) / range) * chartHeight);
        coords.push({ x: xPos, y: yPos, value: yValues[index] });
      }
    });

    return coords;
  };

  const lossPoints = getPointCoords(rounds, lossValues, lossMin, lossMax);
  const dicePoints = getPointCoords(rounds, diceValuesRaw, diceMin, diceMax, (_, val) => val !== null);

  return (
    <section className="charts-section">
      <div className="section-header">
        <h2>Training Performance</h2>
        <p>Loss and Dice Score across federated rounds</p>
        <p className="chart-note">Showing {history.length} completed round{history.length !== 1 ? 's' : ''}</p>
      </div>
      <div className="charts-container">
        <div className="chart-panel">
          <h3>Training Loss (Lower is Better)</h3>
          <div className="chart-wrapper">
            <svg className="training-chart" viewBox="0 0 320 200" aria-label="Loss Chart">
              {/* Background gradient */}
              <defs>
                <linearGradient id="lossGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" style={{ stopColor: '#ef4444', stopOpacity: 0.1 }} />
                  <stop offset="100%" style={{ stopColor: '#ef4444', stopOpacity: 0 }} />
                </linearGradient>
              </defs>

              {/* Grid lines */}
              <line x1="60" y1="40" x2="260" y2="40" className="grid-line" />
              <line x1="60" y1="80" x2="260" y2="80" className="grid-line" />
              <line x1="60" y1="120" x2="260" y2="120" className="grid-line" />
              <line x1="60" y1="160" x2="260" y2="160" className="grid-line" />

              {/* X-axis labels (rounds) */}
              {rounds.map((round, index) => {
                const x = 60 + (index * (200 / (rounds.length - 1 || 1)));
                return (
                  <text key={round} x={x} y="190" textAnchor="middle" fontSize="12" fill="#94a3b8">
                    R{round}
                  </text>
                );
              })}

              {/* Y-axis labels for loss */}
              {[0, 0.25, 0.5, 0.75, 1].map(percent => {
                const value = lossMin + (lossRangeAdjusted * percent);
                const y = 160 - (percent * 120);
                return (
                  <text key={value} x="50" y={y} textAnchor="end" fontSize="11" fill="#94a3b8">
                    {value.toFixed(3)}
                  </text>
                );
              })}

              {/* Loss area */}
              <path
                d={`
                  M 60 ${160}
                  ${drawLine(rounds, lossValues, lossMin, lossMax)}
                  L 260 ${160}
                  Z
                `}
                fill="url(#lossGrad)"
              />

              {/* Loss line */}
              <path
                d={drawLine(rounds, lossValues, lossMin, lossMax)}
                className="chart-line loss-line"
              />

              {/* Loss points */}
              {lossPoints.map((point, index) => (
                <g key={rounds[index]} className="point-group">
                  <circle
                    cx={point.x}
                    cy={point.y}
                    r="6"
                    className="chart-point loss-point"
                  />
                  <text
                    x={point.x}
                    y={point.y - 15}
                    textAnchor="middle"
                    fontSize="12"
                    fill="#ef4444"
                    fontWeight="600"
                  >
                    {point.value.toFixed(3)}
                  </text>
                </g>
              ))}

              {/* Y-axis label */}
              <text x="20" y="100" textAnchor="middle" transform="rotate(-90,20,100)" fontSize="12" fill="#94a3b8">
                Loss
              </text>
            </svg>
          </div>
        </div>

        <div className="chart-panel">
          <h3>Dice Score (Higher is Better)</h3>
          <div className="chart-wrapper">
            <svg className="training-chart" viewBox="0 0 320 200" aria-label="Dice Chart">
              {/* Background gradient */}
              <defs>
                <linearGradient id="diceGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" style={{ stopColor: '#10b981', stopOpacity: 0.1 }} />
                  <stop offset="100%" style={{ stopColor: '#10b981', stopOpacity: 0 }} />
                </linearGradient>
              </defs>

              {/* Grid lines */}
              <line x1="60" y1="40" x2="260" y2="40" className="grid-line" />
              <line x1="60" y1="80" x2="260" y2="80" className="grid-line" />
              <line x1="60" y1="120" x2="260" y2="120" className="grid-line" />
              <line x1="60" y1="160" x2="260" y2="160" className="grid-line" />

              {/* X-axis labels (rounds) */}
              {rounds.map((round, index) => {
                const x = 60 + (index * (200 / (rounds.length - 1 || 1)));
                return (
                  <text key={round} x={x} y="190" textAnchor="middle" fontSize="12" fill="#94a3b8">
                    R{round}
                  </text>
                );
              })}

              {/* Y-axis labels for dice */}
              {[0, 0.25, 0.5, 0.75, 1].map(percent => {
                const value = diceMin + (diceRangeAdjusted * percent);
                const y = 160 - (percent * 120);
                return (
                  <text key={value} x="50" y={y} textAnchor="end" fontSize="11" fill="#94a3b8">
                    {hasDiceData ? value.toFixed(4) : '0.0000'}
                  </text>
                );
              })}

              {/* Dice area */}
              <path
                d={`
                  M 60 ${160}
                  ${drawLine(rounds, diceValuesRaw, diceMin, diceMax, (_, val) => val !== null)}
                  L 260 ${160}
                  Z
                `}
                fill="url(#diceGrad)"
              />

              {/* Dice line */}
              <path
                d={drawLine(rounds, diceValuesRaw, diceMin, diceMax, (_, val) => val !== null)}
                className="chart-line dice-line"
              />

              {/* Dice points - only for non-null dice */}
              {dicePoints.map((point, index) => (
                <g key={rounds[index]} className="point-group">
                  <circle
                    cx={point.x}
                    cy={point.y}
                    r="6"
                    className="chart-point dice-point"
                  />
                  <text
                    x={point.x}
                    y={point.y - 15}
                    textAnchor="middle"
                    fontSize="12"
                    fill="#10b981"
                    fontWeight="600"
                  >
                    {point.value !== null ? point.value.toFixed(4) : null}
                  </text>
                </g>
              ))}

              {/* Y-axis label */}
              <text x="20" y="100" textAnchor="middle" transform="rotate(-90,20,100)" fontSize="12" fill="#94a3b8">
                Dice Score
              </text>
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TrainingCharts;