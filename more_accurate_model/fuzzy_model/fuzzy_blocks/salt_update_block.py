def salt_update(dx_dt, last_x, dt=1.0):
    if dt <= 0.0:
        raise ValueError("dt must be positive.")
    return last_x + dt * dx_dt


def salt_updte(dx_dt, last_x, dt=1.0):
    return salt_update(dx_dt, last_x, dt)
