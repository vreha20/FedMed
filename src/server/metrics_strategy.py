"""
Custom Flower strategy that forwards aggregated metrics to the FastAPI store.
"""

from flwr.server.strategy import FedAvg
from src.backend.routes.metrics import update_metrics


def weighted_dice_average(metrics):
    """Aggregate client Dice scores weighted by the number of examples."""
    if not metrics:
        return {}

    total_examples = sum(num_examples for num_examples, _ in metrics)

    if total_examples == 0:
        return {}

    weighted_dice = sum(
        num_examples * metrics_dict.get("dice", 0.0)
        for num_examples, metrics_dict in metrics
    )

    return {"dice": weighted_dice / total_examples}


class MetricsFedAvg(FedAvg):
    """FedAvg strategy that forwards federated evaluation metrics."""

    def __init__(self, *args, **kwargs):
        """Configure FedAvg with Dice metric aggregation."""
        kwargs["evaluate_metrics_aggregation_fn"] = weighted_dice_average
        super().__init__(*args, **kwargs)

    def aggregate_fit(self, rnd, results, failures):
        """Aggregate client training results."""
        return super().aggregate_fit(rnd, results, failures)

    def aggregate_evaluate(self, rnd, results, failures):
        """Aggregate evaluation metrics and forward Dice score to the API."""
        aggregated_result = super().aggregate_evaluate(
            rnd, results, failures
        )

        if aggregated_result is not None:
            loss_agg, metrics_agg = aggregated_result

            loss = float(loss_agg) if loss_agg is not None else 0.0

            dice = metrics_agg.get("dice")
            if dice is not None:
                dice = float(dice)

            # Flower's aggregate_evaluate receives (ClientProxy, EvaluateRes)
            # pairs, while the metrics store expects (num_examples, metrics)
            # pairs. Normalize the current Flower response shape here.
            client_eval_results = [
                (
                    result.num_examples,
                    {**result.metrics, "cid": result.metrics.get("cid", client.cid)},
                )
                for client, result in results
            ]

            update_metrics(
                round_num=rnd,
                loss=loss,
                accuracy=dice,
                client_eval_results=client_eval_results,
            )

        return aggregated_result
