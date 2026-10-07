"""
src/utils/data_path.py

Finds the BraTS dataset across Kaggle/Colab and local Windows
KaggleHub environments.
"""

import os
from pathlib import Path

CANDIDATE_PATHS = [
    # Kaggle environment
    "/kaggle/input/brats2020-training-data/BraTS2020_training_data/content/data",

    # Colab KaggleHub cache
    "/root/.cache/kagglehub/datasets/awsaf49/brats2020-training-data/versions/3/BraTS2020_training_data/content/data",

    # Local Windows KaggleHub cache
    str(
        Path.home()
        / ".cache"
        / "kagglehub"
        / "datasets"
        / "awsaf49"
        / "brats2020-training-data"
        / "versions"
        / "3"
        / "BraTS2020_training_data"
        / "content"
        / "data"
    ),
]


def find_dataset_path():
    for path in CANDIDATE_PATHS:
        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        "BraTS dataset not found. "
        "Make sure the BraTS2020 dataset is available through KaggleHub."
    )