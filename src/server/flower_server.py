"""
Flower server for FedMed Week 1 scaffolding.
Starts a simple Federated Averaging server.
"""

from flwr.server import start_server, ServerConfig
from flwr.server.strategy import FedAvg
import yaml
from pathlib import Path


def load_config() -> dict:
    """Load configuration from configs/config.yaml."""
    config_path = Path(__file__).parents[2] / "configs" / "config.yaml"
    with config_path.open("r") as f:
        return yaml.safe_load(f)


def main() -> None:
    """Start Flower server."""
    cfg = load_config()
    fed_cfg = cfg.get("federated", {})
    num_rounds = int(fed_cfg.get("rounds", 1))
    # Use FedAvg strategy, requiring all three clients to be available
    strategy = FedAvg(
        fraction_fit=1.0,  # sample all available clients
        fraction_evaluate=1.0,
        min_fit_clients=3,
        min_evaluate_clients=3,
        min_available_clients=3,
    )
    start_server(
        server_address="[::]:8080",
        config=ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
    )


if __name__ == "__main__":
    main()