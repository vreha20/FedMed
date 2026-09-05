import random
import torch
import flwr as fl
from flwr.simulation import start_simulation

from flower_client import HospitalClient
from dataset import group_slices_by_volume


def make_client_fn(data_dir, shards, device):
    def client_fn(cid):
        return HospitalClient(
            cid=cid, data_dir=data_dir, volume_ids=shards[int(cid)], device=device
        ).to_client()
    return client_fn


def weighted_dice_average(metrics):
    total_examples = sum(num for num, _ in metrics)
    weighted_dice = sum(num * m["dice"] for num, m in metrics)
    return {"dice": weighted_dice / total_examples}


def run_simulation(data_dir, num_clients=3, num_rounds=5, volumes_per_client=6):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    groups = group_slices_by_volume(data_dir)
    all_ids = list(groups.keys())
    random.seed(42)
    random.shuffle(all_ids)

    shards = [
        all_ids[i * volumes_per_client:(i + 1) * volumes_per_client]
        for i in range(num_clients)
    ]

    client_fn = make_client_fn(data_dir, shards, device)

    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=num_clients,
        min_evaluate_clients=num_clients,
        min_available_clients=num_clients,
        evaluate_metrics_aggregation_fn=weighted_dice_average,
    )

    history = start_simulation(
        client_fn=client_fn,
        num_clients=num_clients,
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
        client_resources={"num_cpus": 1, "num_gpus": 1 if device.type == "cuda" else 0},
    )

    return history