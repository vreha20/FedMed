"""
Command-line tool to validate the BraTS2020 dataset.

Usage:
    python -m src.utils.validate_dataset
    or
    FEDMED_DATA_DIR=/path/to/data python -m src.utils.validate_dataset
"""

import sys
from src.utils.data_path import validate_dataset, find_dataset_path


def main():
    try:
        # Try to get dataset path from environment or default locations
        dataset_path = find_dataset_path()
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)

    # Validate the dataset
    result = validate_dataset(dataset_path)

    # Print validation report
    print("BraTS Dataset Validation")
    print("------------------------")
    print(f"Dataset path: {result['dataset_path']}")
    print(f"H5 files: {result['h5_files']}")
    print(f"Volumes: {result['volumes']}")
    print(f"Valid volumes: {result['valid_volumes']}")
    if result['invalid_volumes'] > 0:
        print(f"Invalid volumes: {result['invalid_volumes']}")
        for vol_id, reason in result['invalid_volume_details']:
            print(f"  Volume {vol_id}: {reason}")
    if result['invalid_files'] > 0:
        print(f"Invalid files: {result['invalid_files']}")
        for fname in result['invalid_file_list']:
            print(f"  {fname}")
    print(f"Modalities: {result['modalities']}")
    print(f"Mask channels: {result['mask_channels']}")
    print(f"Status: {result['status']}")

    if result['status'] != "READY":
        sys.exit(1)


if __name__ == "__main__":
    main()