"""
FastAPI backend for FedMed Week 1 scaffolding.
Provides health and metrics endpoints.
"""

import uvicorn
from fastapi import FastAPI

from .routes.metrics import router as metrics_router

app = FastAPI(title="FedMed Backend", version="0.1.0")

app.include_router(metrics_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "FedMed Backend is running"}


if __name__ == "__main__":
    # Run the API server on port 8000 to avoid clash with Flower's 8080
    uvicorn.run(app, host="0.0.0.0", port=8000)