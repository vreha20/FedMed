import React from 'react';
import './KPICard.css';

const KPICard = ({ title, value, suffix, icon, helpText }) => {
  // Format value: if it's a float, show 4 decimal places, else as integer
  const formattedValue = typeof value === 'number' && !Number.isInteger(value)
    ? value.toFixed(4)
    : value;

  return (
    <div className="kpi-card">
      <div className="kpi-card-content">
        <div className="kpi-card-icon">{icon}</div>
        <div className="kpi-card-body">
          <div className="kpi-card-title">{title}</div>
          <div className="kpi-card-value">
            <span className="kpi-card-number">{formattedValue}</span>
            <span className="kpi-card-suffix">{suffix}</span>
          </div>
          {helpText && <div className="kpi-card-help">{helpText}</div>}
        </div>
      </div>
    </div>
  );
};

export default KPICard;