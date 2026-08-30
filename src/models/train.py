"""
src/models/train.py

Trains the 3D U-Net on the BraTS dataset to establish the centralized
baseline Dice score — the number the federated model (Week 2) must
approach without ever seeing pooled patient data.
"""

import random
import torch
from torch.utils.data import DataLoader, random_split
from monai.losses import DiceLoss
from monai.metrics import DiceMetric

from dataset import group_slices_by_volume, BraTSVolumeDataset
from model import build_unet3d


def train_baseline(data_dir, epochs=20, batch_size=1, lr=1e-3, num_volumes=20, seed=42):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    groups = group_slices_by_volume(data_dir)
    all_ids = list(groups.keys())
    random.seed(seed)
    volume_ids = random.sample(all_ids, num_volumes)

    dataset = BraTSVolumeDataset(data_dir, volume_ids)

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    model = build_unet3d().to(device)
    loss_fn = DiceLoss(sigmoid=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    dice_metric = DiceMetric(include_background=True, reduction="mean")

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for images, masks in train_loader:
            images, masks = images.to(device), masks.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = loss_fn(outputs, masks)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")

    model.eval()
    dice_metric.reset()
    with torch.no_grad():
        for images, masks in val_loader:
            images, masks = images.to(device), masks.to(device)
            outputs = model(images)
            outputs = torch.sigmoid(outputs) > 0.5
            dice_metric(y_pred=outputs, y=masks)

    baseline_dice = dice_metric.aggregate().item()
    print(f"\nBaseline Dice Score: {baseline_dice:.4f}")

    return model, baseline_dice