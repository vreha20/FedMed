import React from 'react'

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

        <div>
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

          <div className="security-card-top">
            <span className="security-card-label">
              Differential Privacy
            </span>

            <span
              className={`security-indicator ${
                differentialPrivacy?.enabled
                  ? 'enabled'
                  : 'disabled'
              }`}
            />
          </div>

          <strong className="security-value">
            {differentialPrivacy?.enabled
              ? 'Enabled'
              : 'Disabled'}
          </strong>

          <span
            className={`security-state ${
              differentialPrivacy?.enabled
                ? 'enabled'
                : 'disabled'
            }`}
          >
            {differentialPrivacy?.mechanism || 'No mechanism reported'}
          </span>

        </div>


        {/* Homomorphic Encryption */}

        <div className="security-card">

          <div className="security-card-top">
            <span className="security-card-label">
              Homomorphic Encryption
            </span>

            <span
              className={`security-indicator ${
                homomorphicEncryption?.enabled
                  ? 'enabled'
                  : 'disabled'
              }`}
            />
          </div>

          <strong className="security-value">
            {homomorphicEncryption?.enabled
              ? 'Enabled'
              : 'Disabled'}
          </strong>

          <span
            className={`security-state ${
              homomorphicEncryption?.enabled
                ? 'enabled'
                : 'disabled'
            }`}
          >
            {homomorphicEncryption?.library || 'Library unavailable'}
          </span>

        </div>


        {/* Encryption Scheme */}

        <div className="security-card">

          <div className="security-card-top">
            <span className="security-card-label">
              Encryption Scheme
            </span>
          </div>

          <strong className="security-value">
            {homomorphicEncryption?.scheme || 'N/A'}
          </strong>

          <span className="security-state neutral">
            Homomorphic encryption
          </span>

        </div>


        {/* Privacy Mechanism */}

        <div className="security-card">

          <div className="security-card-top">
            <span className="security-card-label">
              Privacy Mechanism
            </span>
          </div>

          <strong className="security-value">
            {differentialPrivacy?.mechanism || 'N/A'}
          </strong>

          <span className="security-state neutral">
            Differential privacy
          </span>

        </div>

      </div>

    </section>
  )
}

export default SecurityPanel
