"""Numerical state update for the fuzzy temperature derivative."""

import numpy as np


def temperature_update(dT_dt, last_T, dt=1.0):
    if dt <= 0.0:
        raise ValueError("dt must be positive.")
    return float(np.clip(last_T + dt * dT_dt, 40.0, 65.0))
