"""
Unit tests for MetricsFedAvg strategy.
"""
import unittest
from unittest.mock import patch

from src.server.metrics_strategy import MetricsFedAvg
from src.backend.routes.metrics import update_metrics


class TestMetricsFedAvg(unittest.TestCase):
    @patch("flwr.server.strategy.FedAvg.aggregate_fit")
    def test_aggregate_fit_calls_update_metrics(self, mock_super_agg):
        # Arrange
        mock_super_agg.return_value = ([], {"loss": 0.5, "accuracy": 0.8})
        strategy = MetricsFedAvg(
            fraction_fit=1.0,
            fraction_evaluate=1.0,
            min_fit_clients=3,
            min_evaluate_clients=3,
            min_available_clients=3,
        )
        with patch("src.server.metrics_strategy.update_metrics") as mock_update:
            # Act
            result = strategy.aggregate_fit(rnd=1, results=[], failures=[])
            # Assert
            mock_super_agg.assert_called_once_with(1, [], [])
            mock_update.assert_called_once()
            args, kwargs = mock_update.call_args
            self.assertEqual(kwargs.get("round_num"), 1)
            self.assertEqual(kwargs.get("loss"), 0.5)
            self.assertEqual(kwargs.get("accuracy"), 0.8)
            self.assertEqual(result, ([], {"loss": 0.5, "accuracy": 0.8}))

    @patch("flwr.server.strategy.FedAvg.aggregate_evaluate")
    def test_aggregate_evaluate_calls_update_metrics(self, mock_super_agg):
        # Arrange
        mock_super_agg.return_value = (0.3, {"accuracy": 0.75})
        strategy = MetricsFedAvg(
            fraction_fit=1.0,
            fraction_evaluate=1.0,
            min_fit_clients=3,
            min_evaluate_clients=3,
            min_available_clients=3,
        )
        with patch("src.server.metrics_strategy.update_metrics") as mock_update:
            # Act
            result = strategy.aggregate_evaluate(rnd=2, results=[], failures=[])
            # Assert
            mock_super_agg.assert_called_once_with(2, [], [])
            mock_update.assert_called_once()
            args, kwargs = mock_update.call_args
            self.assertEqual(kwargs.get("round_num"), 2)
            self.assertEqual(kwargs.get("loss"), 0.3)
            self.assertEqual(kwargs.get("accuracy"), 0.75)
            self.assertEqual(result, (0.3, {"accuracy": 0.75}))

    @patch("flwr.server.strategy.FedAvg.aggregate_fit")
    def test_aggregate_fit_handles_none_result(self, mock_super_agg):
        # Arrange
        mock_super_agg.return_value = None
        strategy = MetricsFedAvg(
            fraction_fit=1.0,
            fraction_evaluate=1.0,
            min_fit_clients=3,
            min_evaluate_clients=3,
            min_available_clients=3,
        )
        with patch("src.server.metrics_strategy.update_metrics") as mock_update:
            # Act
            result = strategy.aggregate_fit(rnd=3, results=[], failures=[])
            # Assert
            mock_super_agg.assert_called_once_with(3, [], [])
            mock_update.assert_not_called()
            self.assertIsNone(result)

    @patch("flwr.server.strategy.FedAvg.aggregate_evaluate")
    def test_aggregate_evaluate_handles_none_result(self, mock_super_agg):
        # Arrange
        mock_super_agg.return_value = None
        strategy = MetricsFedAvg(
            fraction_fit=1.0,
            fraction_evaluate=1.0,
            min_fit_clients=3,
            min_evaluate_clients=3,
            min_available_clients=3,
        )
        with patch("src.server.metrics_strategy.update_metrics") as mock_update:
            # Act
            result = strategy.aggregate_evaluate(rnd=4, results=[], failures=[])
            # Assert
            mock_super_agg.assert_called_once_with(4, [], [])
            mock_update.assert_not_called()
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()