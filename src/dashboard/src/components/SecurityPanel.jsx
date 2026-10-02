import React from 'react'
import './SecurityPanel.css'

function SecurityPanel({ security, loading }) {
  if (loading && !security) {
    return (
      <section className="security-panel">
        <div className="security-loading">
          Loading privacy and security status...
        </div>
      </section>
    )
  }

  if (!security) {
    return (
      <section className="security-panel">
        <div className="security-empty">
          <span className="security-icon">!</span>

          <div>
            <strong>Security status unavailable</strong>

            <p>
              Unable to retrieve the current privacy configuration.
            </p>
          </div>
        </div>
      </section>
    )
  }

  const differentialPrivacy = security.differential_privacy
  const homomorphicEncryption = security.homomorphic_encryption

  return (
    <section className="security-panel">
      <div className="security-header">
        <div className="security-header-content">
          <span className="security-eyebrow">
            PRIVACY &amp; SECURITY
          </span>

          <h2>Federated Security</h2>

          <p>
            Privacy mechanisms currently reported by the FedMed backend.
          </p>
        </div>

        <div className="security-shield">
          ✓
        </div>
      </div>

      <div className="security-grid">
        {/* Differential Privacy */}
        <div className="security-card">
          <div className="security-card-header">
            <h3>Differential Privacy</h3>
          </div>
          <div className="security-card-body">
            <div className="security-status">
              <span className={`security-indicator ${
                differentialPrivacy?.enabled ? 'enabled' : 'disabled'
              }`} />
              <span className="security-status-text">
                {differentialPrivacy?.enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
            {differentialPrivacy?.enabled && (
              <p className="security-description">
                {differentialPrivacy?.mechanism || 'Gaussian noise applied to model updates'}
              </p>
            )}
            {!differentialPrivacy?.enabled && (
              <p className="security-description">
                Differential privacy is not enabled
              </p>
            )}
          </div>
        </div>

        {/* Homomorphic Encryption */}
        <div className="security-card">
          <div className="security-card-header">
            <h3>Homomorphic Encryption</h3>
          </div>
          <div className="security-card-body">
            <div className="security-status">
              <span className={`security-indicator ${
                homomorphicEncryption?.enabled ? 'enabled' : 'disabled'
              }`} />
              <span className="security-status-text">
                {homomorphicEncryption?.enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
            {homomorphicEncryption?.enabled && (
              <p className="security-description">
                {homomorphicEncryption?.library || 'TenSEAL library'}
              </p>
            )}
            {!homomorphicEncryption?.enabled && (
              <p className="security-description">
                Homomorphic encryption library unavailable
              </p>
            )}
          </div>
        </div>

        {/* Encryption Scheme */}
        <div className="security-card">
          <div className="security-card-header">
            <h3>Encryption Scheme</h3>
          </div>
          <div className="security-card-body">
            <p className="security-description">
              {homomorphicEncryption?.scheme || 'N/A'}
            </p>
          </div>
        </div>

        {/* Privacy Mechanism */}
        <div className="security-card">
          <div className="security-card-header">
            <h3>Privacy Mechanism</h3>
          </div>
          <div className="security-card-body">
            <p className="security-description">
              {differentialPrivacy?.mechanism || 'N/A'}
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default SecurityPanel