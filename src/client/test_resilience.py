"""
Focused tests for the resilient Flower client wrapper.
"""
import unittest
from unittest.mock import patch, MagicMock

# Import the function to test
from src.client.resilient_flower_client import start_resilient_client


class TestResilientFlowerClient(unittest.TestCase):
    @patch("src.client.resilient_flower_client.fl.client.start_client")
    @patch("src.client.resilient_flower_client.FlowerClient")
    def test_start_resilient_client_uses_env_cid(
            self, mock_flower_client, mock_start_client
    ):
        # Arrange
        mock_numpy_instance = MagicMock()
        mock_client_instance = MagicMock()
        mock_numpy_instance.to_client.return_value = mock_client_instance
        mock_flower_client.return_value = mock_numpy_instance
        mock_start_client.return_value = None

        # Act with patched environment
        with patch("src.client.resilient_flower_client.os.environ", {"CLIENT_ID": "42"}):
            start_resilient_client()

        # Assert FlowerClient was called with cid="42"
        mock_flower_client.assert_called_once_with("42")
        # Assert to_client was called
        mock_numpy_instance.to_client.assert_called_once()
        # Assert start_client received the converted client
        args, kwargs = mock_start_client.call_args
        self.assertEqual(kwargs.get("client"), mock_client_instance)
        # Assert server_address default
        self.assertEqual(kwargs.get("server_address"), "[::]:8080")
        # Assert default max_retries and max_wait_time (as defined in function)
        self.assertEqual(kwargs.get("max_retries"), 5)
        self.assertEqual(kwargs.get("max_wait_time"), 5.0)

    @patch("src.client.resilient_flower_client.fl.client.start_client")
    @patch("src.client.resilient_flower_client.FlowerClient")
    def test_start_resilient_client_forward_custom_params(
            self, mock_flower_client, mock_start_client
    ):
        # Arrange
        mock_numpy_instance = MagicMock()
        mock_client_instance = MagicMock()
        mock_numpy_instance.to_client.return_value = mock_client_instance
        mock_flower_client.return_value = mock_numpy_instance
        mock_start_client.return_value = None

        # Act
        start_resilient_client(
            server_address="[::]:9000",
            max_retries=2,
            max_wait_time=0.0,
        )

        # Assert
        mock_flower_client.assert_called_once_with("0")  # default CID
        mock_numpy_instance.to_client.assert_called_once()
        args, kwargs = mock_start_client.call_args
        self.assertEqual(kwargs.get("server_address"), "[::]:9000")
        self.assertEqual(kwargs.get("max_retries"), 2)
        self.assertEqual(kwargs.get("max_wait_time"), 0.0)
        self.assertEqual(kwargs.get("client"), mock_client_instance)


if __name__ == "__main__":
    unittest.main()
