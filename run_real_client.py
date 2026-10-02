import sys
import torch
import flwr as fl
from src.client.flower_client import HospitalClient
from src.data.dataset import group_slices_by_volume
import random

DATA_DIR = r"C:\Users\Vrehaa\.cache\kagglehub\datasets\awsaf49\brats2020-training-data\versions\3\BraTS2020_training_data\content\data"
VOLUMES_PER_CLIENT = 2
DEMO_TARGET_SIZE = (32, 32, 32)

def main():
    cid = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    num_clients = 3
    if cid < 0 or cid >= num_clients:
        raise ValueError(f"Client ID must be between 0 and {num_clients - 1}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    groups = group_slices_by_volume(DATA_DIR)
    all_ids = list(groups.keys())
    if len(all_ids) < num_clients * VOLUMES_PER_CLIENT:
        raise RuntimeError(
            f"Need at least {num_clients * VOLUMES_PER_CLIENT} volumes, "
            f"found {len(all_ids)} in {DATA_DIR}"
        )
    random.seed(42)
    random.shuffle(all_ids)

    # Keep the real-client smoke run small enough to finish on a local machine.
    demo_ids = all_ids[:num_clients * VOLUMES_PER_CLIENT]
    shards = [
        demo_ids[i * VOLUMES_PER_CLIENT:(i + 1) * VOLUMES_PER_CLIENT]
        for i in range(num_clients)
    ]
    print(
        f"[client {cid}] using {len(shards[cid])} of {len(all_ids)} volumes "
        f"at {DEMO_TARGET_SIZE}",
        flush=True,
    )

    client = HospitalClient(
        cid=cid,
        data_dir=DATA_DIR,
        volume_ids=shards[cid],
        device=device,
        target_size=DEMO_TARGET_SIZE,
    ).to_client()

    fl.client.start_client(
        server_address="127.0.0.1:8080",
        client=client,
    )

if __name__ == "__main__":
    main()
