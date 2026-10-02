"""
src/utils/data_path.py

Portable BraTS2020 dataset discovery and validation.

Priority:
1. FEDMED_DATA_DIR environment variable
2. Local project data/brats_mini
3. Common Kaggle/KaggleHub locations
"""

import os
import re
import h5py


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CANDIDATE_PATHS = [
    os.path.join(PROJECT_ROOT, "data", "brats_mini"),

    "/kaggle/input/brats2020-training-data/BraTS2020_training_data/content/data",

    "/root/.cache/kagglehub/datasets/awsaf49/brats2020-training-data/versions/3/BraTS2020_training_data/content/data",

    os.path.expanduser(
        "~/.cache/kagglehub/datasets/awsaf49/"
        "brats2020-training-data/versions/3/"
        "BraTS2020_training_data/content/data"
    ),
]


def _is_valid_dataset(path):
    if not os.path.isdir(path):
        return False

    try:
        files = os.listdir(path)
    except OSError:
        return False

    return any(
        filename.endswith(".h5")
        for filename in files
    )


def find_dataset_path():
    """
    Find the BraTS dataset on the current machine.

    FEDMED_DATA_DIR can be used to explicitly specify the dataset:

        export FEDMED_DATA_DIR="/path/to/BraTS/data"
    """

    env_path = os.environ.get("FEDMED_DATA_DIR")

    if env_path:
        env_path = os.path.abspath(os.path.expanduser(env_path))

        if _is_valid_dataset(env_path):
            return env_path

        raise FileNotFoundError(
            f"FEDMED_DATA_DIR was set but is not a valid BraTS dataset: "
            f"{env_path}"
        )

    for path in CANDIDATE_PATHS:
        path = os.path.abspath(os.path.expanduser(path))

        if _is_valid_dataset(path):
            return path

    raise FileNotFoundError(
        "BraTS2020 dataset not found.\n\n"
        "Set FEDMED_DATA_DIR to the directory containing the .h5 files.\n"
        "Example:\n"
        '  export FEDMED_DATA_DIR="/path/to/BraTS2020/data"\n'
    )


def validate_dataset(path):
    """
    Validate the BraTS dataset at the given path.

    Returns a dictionary with validation results.
    """
    if not os.path.isdir(path):
        return {
            "status": "ERROR",
            "error": f"Path does not exist: {path}",
            "dataset_path": path,
        }

    # Pattern for BraTS2020 volume slice files
    pattern = re.compile(r"volume_(\d+)_slice_(\d+)\.h5")

    volume_groups = {}
    h5_files = []
    invalid_files = []

    try:
        files = os.listdir(path)
    except OSError as e:
        return {
            "status": "ERROR",
            "error": f"Cannot list directory: {e}",
            "dataset_path": path,
        }

    for fname in files:
        if fname.endswith(".h5"):
            h5_files.append(fname)
            match = pattern.match(fname)
            if match:
                vol_id = int(match.group(1))
                slice_id = int(match.group(2))
                if vol_id not in volume_groups:
                    volume_groups[vol_id] = []
                volume_groups[vol_id].append((slice_id, fname))
            else:
                invalid_files.append(fname)

    # Check each volume for complete slices and correct shapes
    valid_volumes = []
    invalid_volumes = []
    modalities = None
    mask_channels = None

    for vol_id, slices in volume_groups.items():
        # Sort by slice ID
        slices.sort(key=lambda x: x[0])
        slice_ids = [s[0] for s in slices]
        expected_slices = list(range(min(slice_ids), max(slice_ids) + 1))
        if slice_ids != expected_slices:
            # Missing slices
            invalid_volumes.append((vol_id, f"Missing slices. Have {len(slices)} slices, expected {len(expected_slices)}"))
            continue

        # Check the first file to get shape info
        first_file = os.path.join(path, slices[0][1])
        try:
            with h5py.File(first_file, "r") as f:
                image_shape = f["image"].shape
                mask_shape = f["mask"].shape
                # Expected: image (240, 240, 4), mask (240, 240, 3)
                if len(image_shape) != 3 or image_shape[2] != 4:
                    invalid_volumes.append((vol_id, f"Unexpected image shape: {image_shape}"))
                    continue
                if len(mask_shape) != 3 or mask_shape[2] != 3:
                    invalid_volumes.append((vol_id, f"Unexpected mask shape: {mask_shape}"))
                    continue
                if modalities is None:
                    modalities = image_shape[2]
                if mask_channels is None:
                    mask_channels = mask_shape[2]
                # Additionally, check that all files in the volume can be opened and have the same shape
                valid_volumes.append(vol_id)
        except Exception as e:
            invalid_volumes.append((vol_id, f"Error reading file: {e}"))
            continue

    # If we found at least one valid volume, we can set modalities and mask channels from it
    if modalities is None and valid_volumes:
        # Try to get from the first valid volume
        vol_id = valid_volumes[0]
        slices = volume_groups[vol_id]
        first_file = os.path.join(path, slices[0][1])
        try:
            with h5py.File(first_file, "r") as f:
                modalities = f["image"].shape[2]
                mask_channels = f["mask"].shape[2]
        except Exception:
            modalities = 4
            mask_channels = 3

    total_h5 = len(h5_files)
    total_volumes = len(volume_groups)
    valid_volume_count = len(valid_volumes)
    invalid_volume_count = len(invalid_volumes)
    invalid_file_count = len(invalid_files)

    status = "READY" if valid_volume_count > 0 and invalid_volume_count == 0 and invalid_file_count == 0 else "NOT_READY"

    return {
        "status": status,
        "dataset_path": path,
        "h5_files": total_h5,
        "volumes": total_volumes,
        "valid_volumes": valid_volume_count,
        "invalid_volumes": invalid_volume_count,
        "invalid_files": invalid_file_count,
        "modalities": modalities,
        "mask_channels": mask_channels,
        "invalid_volume_details": invalid_volumes,
        "invalid_file_list": invalid_files,
    }