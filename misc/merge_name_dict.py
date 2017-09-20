"""Merge all name dicts into a .pt file."""

import pickle

import torch

if __name__ == '__main__':
    with open("brand_name_dict.pkl", "rb") as f:
        brand = pickle.load(f)
    with open("fct_name_dict.pkl", "rb") as f:
        fct = pickle.load(f)
    with open("series_name_dict.pkl", "rb") as f:
        series = pickle.load(f)
    with open("spec_name_dict.pkl", "rb") as f:
        spec = pickle.load(f)

    name_dict = {
        "brand": brand,
        "fct": fct,
        "series": series,
        "spec": spec
    }

    torch.save(name_dict, "name_dict.pt")
