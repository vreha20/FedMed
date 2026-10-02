import torch
import flwr as fl
from torch.utils.data import DataLoader
from monai.losses import DiceLoss
from monai.metrics import DiceMetric

from src.models.unet3d import build_unet3d
from src.data.dataset import BraTSVolumeDataset, group_slices_by_volume
from src.privacy.dp import add_dp_noise
from src.privacy.encryption import create_context, encrypt_array, decrypt_array


def get_model_params(model):
    return [val.cpu().numpy() for val in model.state_dict().values()]


def set_model_params(model, params):
    state_dict = model.state_dict()
    for key, val in zip(state_dict.keys(), params):
        state_dict[key] = torch.tensor(val)
    model.load_state_dict(state_dict)


class HospitalClient(fl.client.NumPyClient):
    def __init__(self, cid, data_dir, volume_ids, device, context=None,
                 target_size=(64, 64, 64)):
        self.cid = cid
        self.device = device
        self.context = context
        self.model = build_unet3d().to(device)
        self.dataset = BraTSVolumeDataset(
            data_dir, volume_ids, target_size=target_size
        )
        self.loss_fn = DiceLoss(sigmoid=True)
        self.dice_metric = DiceMetric(include_background=True, reduction="mean")

    def get_parameters(self, config):
        return get_model_params(self.model)

    def fit(self, parameters, config):
        set_model_params(self.model, parameters)
        # Get learning rate and batch size from config, with defaults
        learning_rate = config.get("learning_rate", 1e-3)
        batch_size = config.get("batch_size", 1)
        local_epochs = config.get("local_epochs", 1)
        dp_noise_multiplier = config.get("dp_noise_multiplier", 1.0)

        # Create DataLoader with the specified batch size
        loader = DataLoader(self.dataset, batch_size=batch_size, shuffle=True)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.model.train()
        for _ in range(local_epochs):
            for batch_idx, (images, masks) in enumerate(loader, start=1):
                print(
                    f"[client {self.cid}] training volume "
                    f"{batch_idx}/{len(loader)}",
                    flush=True,
                )
                images, masks = images.to(self.device), masks.to(self.device)
                optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.loss_fn(outputs, masks)
                loss.backward()
                optimizer.step()
        noisy_params = add_dp_noise(get_model_params(self.model), noise_multiplier=dp_noise_multiplier)
        print(f"[client {self.cid}] training complete; returning update", flush=True)

        # Optionally encrypt the final layer (weight + bias) with TenSEAL, then decrypt
        # This is a demonstration of the crypto pipeline; true cross-process handoff is not implemented.
        encryption_method = config.get("privacy", {}).get("encryption", "tenseal")
        if encryption_method == "tenseal":
            try:
                from src.privacy.encryption import create_context, encrypt_array, decrypt_array, is_tenseal_available
                if is_tenseal_available():
                    context = create_context()
                    final_weight_shape = noisy_params[61].shape
                    final_bias_shape = noisy_params[62].shape
                    enc_weight = encrypt_array(context, noisy_params[61])
                    enc_bias = encrypt_array(context, noisy_params[62])
                    dec_weight = decrypt_array(enc_weight, final_weight_shape)
                    dec_bias = decrypt_array(enc_bias, final_bias_shape)
                    noisy_params[61] = dec_weight.astype(noisy_params[61].dtype)
                    noisy_params[62] = dec_bias.astype(noisy_params[62].dtype)
                else:
                    print(f"[client {self.cid}] TenSEAL not available, skipping encryption demo", flush=True)
            except ImportError:
                print(f"[client {self.cid}] TenSEAL not available, skipping encryption demo", flush=True)
        else:
            print(f"[client {self.cid}] Encryption method {encryption_method} not implemented, skipping encryption demo", flush=True)

        return noisy_params, len(self.dataset), {"cid": self.cid}

    def evaluate(self, parameters, config):
        set_model_params(self.model, parameters)
        # Get batch size from config, with default
        batch_size = config.get("batch_size", 1)
        # Create DataLoader with the specified batch size
        loader = DataLoader(self.dataset, batch_size=batch_size, shuffle=False)

        self.model.eval()
        total_loss = 0
        self.dice_metric.reset()
        with torch.no_grad():
            for images, masks in loader:
                images, masks = images.to(self.device), masks.to(self.device)
                outputs = self.model(images)
                loss = self.loss_fn(outputs, masks)
                total_loss += loss.item()
                preds = torch.sigmoid(outputs) > 0.5
                self.dice_metric(y_pred=preds, y=masks)
        avg_loss = total_loss / len(loader)
        dice_score = self.dice_metric.aggregate().item()
        return avg_loss, len(self.dataset), {"cid": self.cid, "dice": dice_score}
