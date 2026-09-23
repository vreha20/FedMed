import numpy as np

def add_dp_noise(params, noise_multiplier=1.0):
    """Adds Gaussian noise to model parameters before sending to server."""
    noisy_params = []
    for p in params:
        noise = np.random.normal(0, noise_multiplier * 0.01, p.shape).astype(p.dtype)
        noisy_params.append(p + noise)
    return noisy_params
