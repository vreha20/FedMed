import React from 'react';
import KPICard from './KPICard';
import './KPISection.css';

const KPISection = ({ latest, history, clientMetrics }) => {
  // Calculate active federation nodes: clients that have data in the latest round
  let activeNodes = 0;
  if (clientMetrics && latest && latest.round > 0) {
    const latestRound = latest.round;
    activeNodes = Object.values(clientMetrics).filter(clientData =>
      clientData.some(entry => entry.round === latestRound)
    ).length;
  }

  // Get latest loss and dice
  const latestLoss = latest ? latest.loss : 0;
  const latestDice = latest && latest.dice !== null ? latest.dice : 'N/A';

  // Get latest round
  const latestRound = latest ? latest.round : 0;

  return (
    <section className="kpi-section">
      <div className="kpi-grid">
        <KPICard
          title="Current Round"
          value={latestRound}
          suffix=""
          icon="🔄"
          helpText="Current federated learning round"
        />
        <KPICard
          title="Loss"
          value={latestLoss}
          suffix=""
          icon="📉"
          helpText="Training loss (lower is better)"
        />
        <KPICard
          title="Dice Score"
          value={latestDice}
          suffix=""
          icon="🎯"
          helpText="Segmentation overlap score"
        />
        <KPICard
          title="Active Nodes"
          value={activeNodes}
          suffix=""
          icon="🏥"
          helpText="Number of participating healthcare nodes"
        />
      </div>
    </section>
  );
};

export default KPISection;