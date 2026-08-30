"""
src/models/unet3d.py

3D U-Net for BraTS brain tumor segmentation, built with MONAI.
Input: 4-channel MRI volume (T1, T1ce, T2, FLAIR)
Output: 3-channel segmentation mask (tumor sub-regions)
"""

from monai.networks.nets import UNet


def build_unet3d(in_channels=4, out_channels=3):
    model = UNet(
        spatial_dims=3,
        in_channels=in_channels,
        out_channels=out_channels,
        channels=(16, 32, 64, 128, 256),
        strides=(2, 2, 2, 2),
        num_res_units=2,
    )
    return model