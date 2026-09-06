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
| Vreha | PPML/ML core — U-Net baseline, federated training loop, encryption, differential privacy |
| Nishanth | Infra/Backend — Flower node setup, gRPC comms, live metrics, React dashboard |

## Status

- Week 1 (Centralized baseline): Complete — 3D U-Net trained on BraTS subset, Dice score 0.1945
- Week 2 (Federated learning): Complete — Flower client + FedAvg simulation working, config-driven, Dice score improving across rounds
- Week 3-4 (Encryption + differential privacy): Not yet started