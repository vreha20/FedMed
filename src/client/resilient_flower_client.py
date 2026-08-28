"""
Resilient Flower client wrapper using Flower's built-in retry configuration.

Provides a start_resilient_client function that wraps the existing
NumPyClient‑based FlowerClient and uses flwr.client.start_client with
configured max_retries and max_wait_time to add connection‑level resilience
without altering the Week 1 client implementation.
"""

import os
import flwr as fl
from .flower_client_base import FlowerClient


def start_resilient_client(
    server_address: str = "[::]:8080",
    max_retries: int = 5,
    max_wait_time: float | None = 5.0,
) -> None:
    """
    Start a Flower client with automatic retry on connection failures.

    Parameters
    ----------
    server_address : str
        Address of the Flower server (default: "[::]:8080").
    max_retries : int
        Maximum number of connection attempts before giving up.
        Passed directly to ``flwr.client.start_client``.
    max_wait_time : float | None
        Maximum time to wait between retry attempts (seconds).
        If None, no wait is applied between retries.
        Passed directly to ``flwr.client.start_client``.
    """
    # Read the client ID from the environment (same as the Week 1 launchers)
    cid = os.environ.get("CLIENT_ID", "0")
    # Create the existing NumPy‑client implementation from Week 1
    numpy_client = FlowerClient(cid)
    # Convert it to the newer ``Client`` type expected by ``start_client``
    client = numpy_client.to_client()
    # Start the client with built‑in retry parameters
    fl.client.start_client(
        server_address=server_address,
        client=client,
        max_retries=max_retries,
        max_wait_time=max_wait_time,
    )


# Optional command‑line entry point (useful for manual testing)
if __name__ == "__main__":
    start_resilient_client()
