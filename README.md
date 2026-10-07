# FedMed — Cross-Silo Federated Learning Engine

Privacy-preserving brain tumor segmentation across simulated hospital nodes, without any hospital ever sharing raw patient MRI data.

## Problem

Training accurate medical imaging models needs large datasets, but hospitals can't legally pool raw patient data (HIPAA/GDPR). FedMed solves this with **federated learning**: each hospital trains locally, and only encrypted model weight updates — never patient data — are shared with a central aggregator.

## Architecture

- **Model**: 3D U-Net (MONAI) for MRI tumor segmentation
- **Federated Learning**: Flower framework, FedAvg aggregation across 3 simulated hospital nodes
- **Privacy**: TenSEAL homomorphic encryption on weight updates + differential privacy noise
- **Backend**: FastAPI + gRPC (secure node communication)
- **Dashboard**: React — live training metrics, segmentation visualizations

## Project Structure

See `docs/architecture.md` for the full breakdown.

## Setup

```bash
pip install -r requirements.txt
```

## Team

| Member | Role |
|---|---|
| Vreha Attri | Backend — FastAPI metrics APIs, SQLite metrics persistence, federated evaluation metrics integration, backend validation |
| Nishanth | Infra/Backend — Flower node setup, gRPC communication, live metrics, React dashboard |

## Status

- **Week 1 — Centralized baseline:** Complete — 3D U-Net baseline trained on BraTS 2020 data
- **Week 2 — Federated learning:** Complete — Flower + FedAvg simulation with 3 simulated hospital clients
- **Backend & metrics:** Complete — FastAPI APIs, SQLite persistence, aggregate and per-client Dice metrics
- **Frontend & dashboard:** Complete — dashboard integrated with backend metrics and training visualizations
- **Privacy & security:** Implemented — Gaussian-noise privacy mechanism and TenSEAL CKKS encryption/decryption demonstration
- **Final validation:** Complete — 2 federated rounds completed with 3 clients and 0 client failures

## Final Project Status

FedMed has reached the final project implementation stage. The system combines federated medical image segmentation, backend metrics persistence, dashboard monitoring, and privacy/security components into an integrated workflow.

The final local federated experiment used:

- 3 simulated hospital clients
- 369 BraTS volumes
- 123 volumes per client
- 2 federated rounds
- 1 local epoch per round
- 0 client failures
- FedAvg aggregation