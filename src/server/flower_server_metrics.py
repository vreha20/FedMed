"""
Flower server with live‑metrics integration.
Re‑uses the Week‑1 configuration loading but plugs in MetricsFedAvg.
"""

from flwr.server import start_server, ServerConfig
from src.server.metrics_strategy import MetricsFedAvg   # our custom strategy
import yaml
from pathlib import Path


def load_config() -> dict:
    """Duplicate of the Week‑1 loader – keeps this file independent."""
    config_path = Path(__file__).parents[1] / "configs" / "config.yaml"
    with config_path.open("r") as f:
        return yaml.safe_load(f)


def main() -> None:
    """Start Flower server with metrics‑forwarding strategy."""
    cfg = load_config()
    fed_cfg = cfg.get("federated", {})
    num_rounds = int(fed_cfg.get("rounds", 1))

    strategy = MetricsFedAvg(
        fraction_fit=1.0,
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