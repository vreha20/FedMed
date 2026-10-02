"""
Metrics router for FedMed FastAPI backend.
Provides stub endpoints for health and metrics.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time

router = APIRouter()

# In-memory store for demonstration
_metrics_store = {
    "latest": None,
    "history": [],
    "client_metrics": {},  # {client_id: [{"round": int, "dice": float, "examples": int, "timestamp": float}]}
}


class MetricsResponse(BaseModel):
    round: int
    loss: float
    dice: Optional[float] = None
    timestamp: float


class ClientMetricsResponse(BaseModel):
    round: int
    dice: float
    examples: int
    timestamp: float


@router.get("/health")
def health():
    """Simple health check."""
    return {"status": "ok"}


@router.get("/metrics", response_model=MetricsResponse)
def get_latest_metrics():
    """Return the most recent metrics."""
    if _metrics_store["latest"] is None:
        raise HTTPException(status_code=404, detail="No metrics available")
    return _metrics_store["latest"]


@router.get("/metrics/history", response_model=List[MetricsResponse])
def get_metrics_history():
    """Return the history of metrics."""
    return _metrics_store["history"]


# Helper function to be called from elsewhere (e.g., Flower strategy callback)
def update_metrics(round_num: int, loss: float, dice: Optional[float] = None,
                   client_eval_results: Optional[List[tuple]] = None):
    """Update the in‑memory metrics store."""
    metrics = MetricsResponse(
        round=round_num,
        loss=loss,
        dice=dice,
        timestamp=time.time(),
    )
    _metrics_store["latest"] = metrics
    _metrics_store["history"].append(metrics)

    # Store per-client evaluation results if provided
    if client_eval_results:
        for num_examples, metrics_dict in client_eval_results:
            client_id = metrics_dict.get("cid")
            dice_score = metrics_dict.get("dice")

            # Only store if we have both client ID and dice score
            if client_id is not None and dice_score is not None:
                client_metrics = {
                    "round": round_num,
                    "dice": float(dice_score),
                    "examples": int(num_examples),
                    "timestamp": time.time()
                }

                # Initialize client list if not present
                if client_id not in _metrics_store["client_metrics"]:
                    _metrics_store["client_metrics"][client_id] = []

                # Append this round's metrics
                _metrics_store["client_metrics"][client_id].append(client_metrics)


@router.get("/metrics/clients", response_model=Dict[str, List[ClientMetricsResponse]])
def get_client_metrics():
    """Return per-client metrics history."""
    return _metrics_store["client_metrics"]

@router.get("/security")
def get_security_status():
    """Return the privacy and security capabilities implemented in FedMed."""
    return {
        "differential_privacy": {
            "enabled": True,
            "mechanism": "Gaussian noise",
        },
        "homomorphic_encryption": {
            "enabled": True,
            "scheme": "CKKS",
            "library": "TenSEAL",
        },
    }