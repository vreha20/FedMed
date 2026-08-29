"""
src/data/dataset.py

Loads the BraTS2020 dataset (preprocessed as 2D slices in .h5 files) and
reconstructs 3D volumes by grouping slices belonging to the same patient
volume. Used to build a proper 3D U-Net baseline (per Axlero Project 2 spec).

Each .h5 file contains:
    image: (240, 240, 4)  -> 4 MRI modalities (T1, T1ce, T2, FLAIR)
    mask:  (240, 240, 3)  -> one-hot encoded tumor sub-regions
"""

import os
import re
import h5py
import numpy as np
from collections import defaultdict
from torch.utils.data import Dataset
import torch
import torch.nn.functional as F


def group_slices_by_volume(data_dir):
    volume_groups = defaultdict(list)
    pattern = re.compile(r"volume_(\d+)_slice_(\d+)\.h5")

    for fname in os.listdir(data_dir):
        match = pattern.match(fname)
        if match:
            vol_id, slice_id = int(match.group(1)), int(match.group(2))
            volume_groups[vol_id].append((slice_id, fname))

    for vol_id in volume_groups:
        volume_groups[vol_id].sort(key=lambda x: x[0])

    return volume_groups


class BraTSVolumeDataset(Dataset):
    def __init__(self, data_dir, volume_ids, target_size=(64, 128, 128)):
        self.data_dir = data_dir
        self.volume_ids = volume_ids
        self.target_size = target_size
        self.volume_groups = group_slices_by_volume(data_dir)

    def __len__(self):
        return len(self.volume_ids)

    def _load_volume(self, vol_id):
        slices = self.volume_groups[vol_id]
        images, masks = [], []

        for _, fname in slices:
            fpath = os.path.join(self.data_dir, fname)
            with h5py.File(fpath, "r") as f:
                images.append(f["image"][:])
                masks.append(f["mask"][:])

        image_vol = np.stack(images, axis=0)
        mask_vol = np.stack(masks, axis=0)

        image_vol = np.transpose(image_vol, (3, 0, 1, 2))
        mask_vol = np.transpose(mask_vol, (3, 0, 1, 2))

        return image_vol, mask_vol

    def __getitem__(self, idx):
        vol_id = self.volume_ids[idx]
        image_vol, mask_vol = self._load_volume(vol_id)

        image_tensor = torch.from_numpy(image_vol).float()
        mask_tensor = torch.from_numpy(mask_vol).float()

        image_tensor = F.interpolate(
            image_tensor.unsqueeze(0), size=self.target_size,
            mode="trilinear", align_corners=False
        ).squeeze(0)

        mask_tensor = F.interpolate(
            mask_tensor.unsqueeze(0), size=self.target_size,
            mode="nearest"
        ).squeeze(0)

        return image_tensor, mask_tensor