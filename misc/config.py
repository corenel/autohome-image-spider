"""Configs for this project."""

import os

# data
data_root = os.path.abspath(
    os.path.expanduser("/media/Data/autohome"))
csv_root = os.path.join(data_root, "csv")
image_root = os.path.join(data_root, "image")
image_raw_root = os.path.join(data_root, "image_raw")

# selected
selected_brand_ids = [
    33,
    15,
    36,
    44,
    52,
    70,
    47,
    40,
    42,
    73,
    169,
    51,
    57,
    133,
    39,
    54,
    48,
]
selected_image_types = [
    1
]
