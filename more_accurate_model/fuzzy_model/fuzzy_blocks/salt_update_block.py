"""Numerical state update for the fuzzy salinity derivative."""

import numpy as np


def salt_update(dx_dt, last_x, dt=1.0):
    if dt <= 0.0:
        raise ValueError("dt must be positive.")
    return float(np.clip(last_x + dt * dx_dt, 4.0, 8.0))


def salt_updte(dx_dt, last_x, dt=1.0):
    """Backward-compatible alias for the original misspelled function."""

    return salt_update(dx_dt, last_x, dt)
