"""Helpful fucntions for this project."""

import yaml


def str_to_dict(s):
    """Convert string to dict using yaml parser."""
    d = yaml.load(s)
    d = d if type(d) is dict else None
    return d
