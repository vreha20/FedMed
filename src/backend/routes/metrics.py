"""Persistent metrics API shared by the Flower server and FastAPI process."""

import os
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Both processes resolve this to the same file. Deployments can point it at a
# shared mounted volume with FEDMED_METRICS_DB.
_DEFAULT_DB = Path(__file__).resolve().parents[3] / "data" / "metrics.sqlite3"
_DB_PATH = Path(os.environ.get("FEDMED_METRICS_DB", str(_DEFAULT_DB)))


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


@contextmanager
def _connect():
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(_DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def _initialize() -> None:
    with _connect() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS metrics (
                round INTEGER PRIMARY KEY,
                loss REAL NOT NULL,
                dice REAL,
                timestamp REAL NOT NULL
            )"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS client_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                round INTEGER NOT NULL,
                dice REAL NOT NULL,
                examples INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                UNIQUE(client_id, round)
            )"""
        )


def _row_to_metrics(row: sqlite3.Row) -> MetricsResponse:
    return MetricsResponse(**dict(row))


@router.get("/health")
def health():
    """Check API and metrics-store availability."""
    try:
        with _connect() as connection:
            connection.execute("SELECT 1")
        return {"status": "ok"}
    except sqlite3.Error as exc:
        raise HTTPException(status_code=503, detail="Metrics store unavailable") from exc


@router.get("/metrics", response_model=MetricsResponse)
def get_latest_metrics():
    with _connect() as connection:
        row = connection.execute(
            "SELECT round, loss, dice, timestamp FROM metrics ORDER BY round DESC LIMIT 1"
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No metrics available")
    return _row_to_metrics(row)


@router.get("/metrics/history", response_model=List[MetricsResponse])
def get_metrics_history():
    with _connect() as connection:
        rows = connection.execute(
            "SELECT round, loss, dice, timestamp FROM metrics ORDER BY round"
        ).fetchall()
    return [_row_to_metrics(row) for row in rows]


def update_metrics(
    round_num: int,
    loss: float,
    dice: Optional[float] = None,
    client_eval_results=None,
) -> None:
    """Persist aggregated and per-client evaluation results from Flower."""
    timestamp = time.time()
    with _connect() as connection:
        connection.execute(
            """INSERT INTO metrics(round, loss, dice, timestamp)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(round) DO UPDATE SET
                   loss=excluded.loss,
                   dice=excluded.dice,
                   timestamp=excluded.timestamp""",
            (round_num, loss, dice, timestamp),
        )
        for num_examples, metrics in client_eval_results or []:
            client_id = metrics.get("cid")
            dice_score = metrics.get("dice")
            if client_id is None or dice_score is None:
                continue
            connection.execute(
                """INSERT INTO client_metrics(client_id, round, dice, examples, timestamp)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(client_id, round) DO UPDATE SET
                       dice=excluded.dice,
                       examples=excluded.examples,
                       timestamp=excluded.timestamp""",
                (str(client_id), round_num, float(dice_score), int(num_examples), timestamp),
            )


@router.get("/metrics/clients", response_model=Dict[str, List[ClientMetricsResponse]])
def get_client_metrics():

    with _connect() as connection:
        rows = connection.execute(
            """SELECT client_id, round, dice, examples, timestamp
               FROM client_metrics ORDER BY client_id, round"""
        ).fetchall()
    result: Dict[str, List[ClientMetricsResponse]] = {}
    for row in rows:
        result.setdefault(row["client_id"], []).append(
            ClientMetricsResponse(
                round=row["round"],
                dice=row["dice"],
                examples=row["examples"],
                timestamp=row["timestamp"],
            )
        )
    return result


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


_initialize()