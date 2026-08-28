"""
Metrics router for FedMed FastAPI backend.
Provides stub endpoints for health and metrics.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()

# In-memory store for demonstration
_metrics_store = {
    "latest": None,
    "history": [],
}


class MetricsResponse(BaseModel):
    round: int
    loss: float
    accuracy: Optional[float] = None
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
def update_metrics(round_num: int, loss: float, accuracy: Optional[float] = None):
    """Update the in‑memory metrics store."""
    metrics = MetricsResponse(
        round=round_num,
        loss=loss,
        accuracy=accuracy,
        timestamp=time.time(),
    )
    _metrics_store["latest"] = metrics
    _metrics_store["history"].append(metrics)