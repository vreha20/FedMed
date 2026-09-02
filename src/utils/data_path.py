"""
src/utils/data_path.py

Auto-detects the BraTS dataset path across different Colab session
locations (kagglehub cache vs Kaggle's mounted input directory).
"""

import os

CANDIDATE_PATHS = [
    "/kaggle/input/brats2020-training-data/BraTS2020_training_data/content/data",
    "/root/.cache/kagglehub/datasets/awsaf49/brats2020-training-data/versions/3/BraTS2020_training_data/content/data",
]


def find_dataset_path():
    for path in CANDIDATE_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "BraTS dataset not found in any known location. "
        "Run kagglehub.dataset_download('awsaf49/brats2020-training-data') first."
    )