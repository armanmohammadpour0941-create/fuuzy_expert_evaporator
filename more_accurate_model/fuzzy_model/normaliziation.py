"""Scaling helpers for the normalized fuzzy universe ``[-5, 5]``.

The first item in every range is the operating point, not necessarily the
midpoint of the lower and upper bounds.  Scaling each side independently keeps
the operating point exactly at zero and maps both physical bounds exactly to
the fuzzy-universe bounds.
"""

import numpy as np


def _validate_range(physical_range):
    if len(physical_range) != 3:
        raise ValueError("A range must be [operating_point, lower_bound, upper_bound].")
    operating_point, lower_bound, upper_bound = map(float, physical_range)
    if not lower_bound < operating_point < upper_bound:
        raise ValueError(
            "The range must satisfy lower_bound < operating_point < upper_bound."
        )
    return operating_point, lower_bound, upper_bound


def normalize_scale(value, physical_range, *, clip=True):
    operating_point, lower_bound, upper_bound = _validate_range(physical_range)
    value = float(value)
    span = (
        operating_point - lower_bound
        if value < operating_point
        else upper_bound - operating_point
    )
    normalized_value = 5.0 * (value - operating_point) / span
    if clip:
        normalized_value = np.clip(normalized_value, -5.0, 5.0)
    return float(normalized_value)


def denormalize_scale(normal_value, physical_range, *, clip=True):
    operating_point, lower_bound, upper_bound = _validate_range(physical_range)
    normal_value = float(normal_value)
    if clip:
        normal_value = float(np.clip(normal_value, -5.0, 5.0))
    span = (
        operating_point - lower_bound
        if normal_value < 0.0
        else upper_bound - operating_point
    )
    return operating_point + normal_value * span / 5.0
    
