import torch
import flwr as fl
from torch.utils.data import DataLoader
from monai.losses import DiceLoss
from monai.metrics import DiceMetric

from src.models.unet3d import build_unet3d
from src.data.dataset import BraTSVolumeDataset, group_slices_by_volume
from src.privacy.dp import add_dp_noise


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
        self.dice_metric = DiceMetric(include_background=True, reduction="mean")

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
        noisy_params = add_dp_noise(get_model_params(self.model), noise_multiplier=config.get("dp_noise_multiplier", 1.0))
        return noisy_params, len(self.dataset), {"cid": self.cid}

    def evaluate(self, parameters, config):
        set_model_params(self.model, parameters)
        self.model.eval()
        total_loss = 0
        self.dice_metric.reset()
        with torch.no_grad():
            for images, masks in self.loader:
                images, masks = images.to(self.device), masks.to(self.device)
                outputs = self.model(images)
                loss = self.loss_fn(outputs, masks)
                total_loss += loss.item()
                preds = torch.sigmoid(outputs) > 0.5
                self.dice_metric(y_pred=preds, y=masks)
        avg_loss = total_loss / len(self.loader)
        dice_score = self.dice_metric.aggregate().item()
        return avg_loss, len(self.dataset), {"cid": self.cid, "dice": dice_score}