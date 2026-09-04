"""
src/client/flower_client.py

Real Flower client (replaces Week 1 dummy scaffolding): trains the
3D U-Net locally on a hospital's data shard and returns updated
weights to the server for FedAvg aggregation.
"""

import torch
import flwr as fl
from torch.utils.data import DataLoader
from monai.losses import DiceLoss

from src.models.unet3d import build_unet3d
from src.data.dataset import BraTSVolumeDataset


def get_model_params(model):
    return [val.cpu().numpy() for val in model.state_dict().values()]


def set_model_params(model, params):
    state_dict = model.state_dict()
    for key, val in zip(state_dict.keys(), params):
        state_dict[key] = torch.tensor(val)
    model.load_state_dict(state_dict)


class HospitalClient(fl.client.NumPyClient):
    def __init__(self, cid, data_dir, volume_ids, device):
        self.cid = cid
        self.device = device
        self.model = build_unet3d().to(device)
        self.dataset = BraTSVolumeDataset(data_dir, volume_ids)
        self.loader = DataLoader(self.dataset, batch_size=1, shuffle=True)
        self.loss_fn = DiceLoss(sigmoid=True)

    def get_parameters(self, config):
        return get_model_params(self.model)

    def fit(self, parameters, config):
        set_model_params(self.model, parameters)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        self.model.train()
        local_epochs = config.get("local_epochs", 1)
        for _ in range(local_epochs):
            for images, masks in self.loader:
                images, masks = images.to(self.device), masks.to(self.device)
                optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.loss_fn(outputs, masks)
                loss.backward()
                optimizer.step()
        return get_model_params(self.model), len(self.dataset), {"cid": self.cid}

    def evaluate(self, parameters, config):
        set_model_params(self.model, parameters)
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for images, masks in self.loader:
                images, masks = images.to(self.device), masks.to(self.device)
                outputs = self.model(images)
                loss = self.loss_fn(outputs, masks)
                total_loss += loss.item()
        avg_loss = total_loss / len(self.loader)
        return avg_loss, len(self.dataset), {"cid": self.cid}