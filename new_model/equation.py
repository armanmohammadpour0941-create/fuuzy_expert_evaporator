def med_equation(t, x, u, d):
    l, x, t_v = x
    w_s, w_f = u
    t_f, x_f, w_bin, x_bin, t_bin, t_sin = d

    m = A_s * l * (rho_f + rho_v * ((H / l) - 1))
    dl = (w_f + w_bin - w_bout, w_v) / (A_s * (rho_f - rho_v))
    dx = ((w_f * (x_f - x)) + (w_bin * (x_bin - x)) + (w_v * x)) / (m)
    dt = (
        w_s * lambda_s
        + w_f * (h_f - h)
        + w_bin * (h_bin - h)
        - w_bout * (h_b - h)
        - w_v * (h_v - h)
    ) / (
        m
        * (
            (alpha * (e + 2 * f * t_v + 3 * g * t_v**2))
            + ((1 - alpha) * (b + 2 * c * t_v + 3 * d * t_v**2))
        )
    )
