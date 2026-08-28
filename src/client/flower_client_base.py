"""
Reusable Flower client for FedMed Week 1 scaffolding.
Implements a minimal NumPyClient that can connect to the server.
"""

import os
from typing import List, Tuple, Dict, Optional

import flwr as fl
import numpy as np


class FlowerClient(fl.client.NumPyClient):
    """A simple Flower client returning dummy parameters."""

    def __init__(self, cid: str) -> None:
        self.cid = cid

    def get_parameters(self, config: Dict[str, fl.common.Scalar]) -> List[np.ndarray]:
        # Return dummy parameters (empty list) – will be replaced with real weights later
        return []

    def fit(
        self,
        parameters: List[np.ndarray],
        config: Dict[str, fl.common.Scalar],
    ) -> Tuple[List[np.ndarray], int, Dict[str, fl.common.Scalar]]:
        # Dummy training: just return same parameters and pretend we trained on 10 examples
        return parameters, 10, {"cid": self.cid}

    def evaluate(
        self,
        parameters: List[np.ndarray],
        config: Dict[str, fl.common.Scalar],
    ) -> Tuple[float, int, Dict[str, fl.common.Scalar]]:
        # Dummy evaluation: return loss 0.5 and accuracy 0.8
        return 0.5, 10, {"cid": self.cid, "accuracy": 0.8}


def start_client() -> None:
    """Start the Flower client."""
    cid = os.environ.get("CLIENT_ID", "0")
    client = FlowerClient(cid)
    fl.client.start_numpy_client(
        server_address="[::]:8080",
        client=client,
    )


if __name__ == "__main__":
    start_client()