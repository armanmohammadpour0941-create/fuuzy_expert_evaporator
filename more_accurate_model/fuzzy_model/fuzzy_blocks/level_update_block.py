def level_update(dl_dt, last_l, dt=1.0):
    if dt <= 0.0:
        raise ValueError("dt must be positive.")
    return float(last_l + dt * dl_dt)
    # return float(np.clip(last_l + dt * dl_dt, 0.0, 0.22))
