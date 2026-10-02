"""
src/federated/fed_simulation.py

Runs Flower's simulation mode with 3 hospital clients, each training
on a separate data shard, aggregated via FedAvg. Configuration
(num_clients, rounds, local_epochs) is read from configs/config.yaml
rather than hardcoded, so hyperparameters can be tuned without
touching this file.
"""

import random
import yaml
import torch
import flwr as fl
from flwr.simulation import start_simulation

from src.client.flower_client import HospitalClient
from src.data.dataset import group_slices_by_volume


def load_config(path="configs/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def make_client_fn(data_dir, shards, device):
    def client_fn(cid):
        return HospitalClient(
            cid=cid, data_dir=data_dir, volume_ids=shards[int(cid)], device=device
        ).to_client()
    return client_fn


def weighted_dice_average(metrics):
    """Aggregates Dice scores across clients, weighted by dataset size."""
    total_examples = sum(num for num, _ in metrics)
    weighted_dice = sum(num * m["dice"] for num, m in metrics)
    return {"dice": weighted_dice / total_examples}


def run_simulation(data_dir, config_path="configs/config.yaml"):
    cfg = load_config(config_path)
    fed_cfg = cfg["federated"]
    train_cfg = cfg["training"]

    num_clients = fed_cfg["num_clients"]
    num_rounds = fed_cfg["rounds"]
    local_epochs = fed_cfg["local_epochs"]
    dp_noise_multiplier = cfg["privacy"]["dp_noise_multiplier"]
    learning_rate = train_cfg["learning_rate"]
    batch_size = train_cfg["batch_size"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    groups = group_slices_by_volume(data_dir)
    all_ids = list(groups.keys())
    random.seed(42)
    random.shuffle(all_ids)

    # Split into non-overlapping shards - one per simulated hospital,
    # so no patient data is ever shared between clients
    volumes_per_client = len(all_ids) // num_clients
    shards = [
        all_ids[i * volumes_per_client:(i + 1) * volumes_per_client]
        for i in range(num_clients)
    ]

    client_fn = make_client_fn(data_dir, shards, device)

    from src.server.metrics_strategy import MetricsFedAvg
    strategy = MetricsFedAvg(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=num_clients,
        min_evaluate_clients=num_clients,
        min_available_clients=num_clients,
        evaluate_metrics_aggregation_fn=weighted_dice_average,
        on_fit_config_fn=lambda rnd: {
            "local_epochs": local_epochs,
            "dp_noise_multiplier": dp_noise_multiplier,
            "learning_rate": learning_rate,
            "batch_size": batch_size
        },
    )

    history = start_simulation(
        client_fn=client_fn,
        num_clients=num_clients,
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
        client_resources={"num_cpus": 1, "num_gpus": 1 if device.type == "cuda" else 0},
    )

    return history


if __name__ == "__main__":
    from src.utils.data_path import find_dataset_path
    DATA_DIR = find_dataset_path()
    history = run_simulation(DATA_DIR)
    print("Dice history:", history.metrics_distributed)