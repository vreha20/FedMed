# FedMed — Week 1 & 2 Results Summary

## Centralized Baseline (Week 1)
- Model: 3D U-Net (MONAI), ~4.8M parameters
- Data: 20-volume subset of BraTS2020, resized to 64x128x128
- Training: 20 epochs, lr=1e-3, Adam optimizer, Dice loss
- **Result: Dice score = 0.1945**
- Note: trained on a 20-volume subset (of 369 total) due to free-tier Colab compute limits; loss curve was still decreasing at epoch 20, indicating room for further improvement with more epochs/data.

## Federated Learning (Week 2)
- Framework: Flower, FedAvg strategy
- Setup: 3 simulated hospital clients, non-overlapping 6-volume shards each
- Rounds: 5 communication rounds, 1 local epoch per round per client

| Round | Federated Dice Score |
|---|---|
| 1 | 0.0334 |
| 2 | 0.0398 |
| 3 | 0.0453 |
| 4 | 0.0535 |
| 5 | 0.0588 |

**Key finding:** Dice score improved consistently every round, confirming that FedAvg aggregation is correctly combining updates from independently-trained hospital nodes — without any hospital ever sharing raw patient data.

## Interpretation
The federated Dice score (0.0588 at round 5) is lower than the centralized baseline (0.1945) because:
1. Each client saw only 6 volumes vs. 16 for the centralized baseline
2. Only 5 communication rounds were run vs. 20 epochs centrally
3. This is expected and standard in early-stage federated learning experiments — the goal at this stage is proving correctness of the pipeline, not matching centralized accuracy yet

## Next steps (Week 3-4)
- TenSEAL homomorphic encryption on weight updates
- Differential privacy noise injection
- More federated rounds for closer baseline comparison