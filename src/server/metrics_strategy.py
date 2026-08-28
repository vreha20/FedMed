"""
Custom Flower strategy that forwards aggregated metrics to the FastAPI store.
"""

from flwr.server.strategy import FedAvg
# Import the helper that already exists in the metrics router
from src.backend.routes.metrics import update_metrics


class MetricsFedAvg(FedAvg):
    """FedAvg that calls update_metrics after each aggregation round."""

    def aggregate_fit(
        self, rnd, results, failures
    ):
        # Run the original FedAvg aggregation
        aggregated_result = super().aggregate_fit(rnd, results, failures)
        if aggregated_result is not None:
            parameters_agg, metrics_agg = aggregated_result
            # Extract loss/accuracy (use defaults if missing)
            loss = float(metrics_agg.get("loss", 0.0))
            accuracy = metrics_agg.get("accuracy")
            if accuracy is not None:
                accuracy = float(accuracy)
            # Push to the FastAPI in‑memory store
            update_metrics(round_num=rnd, loss=loss, accuracy=accuracy)
        return aggregated_result

    def aggregate_evaluate(
        self, rnd, results, failures
    ):
        aggregated_result = super().aggregate_evaluate(rnd, results, failures)
        if aggregated_result is not None:
            loss_agg, metrics_agg = aggregated_result
            loss = float(loss_agg) if loss_agg is not None else 0.0
            accuracy = metrics_agg.get("accuracy")
            if accuracy is not None:
                accuracy = float(accuracy)
            update_metrics(round_num=rnd, loss=loss, accuracy=accuracy)
        return aggregated_result