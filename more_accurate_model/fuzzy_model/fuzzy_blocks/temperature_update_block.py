def temperature_update(dT_dt, last_T, dt=1.0):
    if dt <= 0.0:
        raise ValueError("dt must be positive.")
    return last_T + dt * dT_dt
