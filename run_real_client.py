import sys
import torch
import flwr as fl
from src.client.flower_client import HospitalClient
from src.data.dataset import group_slices_by_volume
import random

DATA_DIR = r"C:\Users\Vrehaa\.cache\kagglehub\datasets\awsaf49\brats2020-training-data\versions\3\BraTS2020_training_data\content\data"

def main():
    cid = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    num_clients = 3

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    groups = group_slices_by_volume(DATA_DIR)
    all_ids = list(groups.keys())
    random.seed(42)
    random.shuffle(all_ids)

    volumes_per_client = len(all_ids) // num_clients
    shards = [
        all_ids[i * volumes_per_client:(i + 1) * volumes_per_client]
        for i in range(num_clients)
    ]

    client = HospitalClient(
        cid=cid, data_dir=DATA_DIR, volume_ids=shards[cid], device=device
    ).to_client()

    fl.client.start_client(
        server_address="127.0.0.1:8080",
        client=client,
    )

if __name__ == "__main__":
    main()