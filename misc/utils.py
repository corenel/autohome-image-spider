"""Helpful fucntions for this project."""

import yaml


def str_to_dict(s):
    """Convert string to dict using yaml parser."""
    d = yaml.load(s)
    d = d if type(d) is dict else None
    return d


def get_car_model(response):
    """Get car model info."""
    return str_to_dict(response.xpath(
        "//script[contains(.,'__CarModel')]/text()").re("{.*}")[0])
