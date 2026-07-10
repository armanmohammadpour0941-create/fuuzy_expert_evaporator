import numpy as np
import thermo as th


def med_equation(t, x, u, distur, params, time_vec):
    l_b, x, t_v = x
    w_s_vec, w_f_vec = u
    t_f_vec, x_f_vec, w_bin_vec, x_bin_vec, t_bin_vec = distur
    
  
    w_s = np.interp(t, time_vec, w_s_vec)
    w_f = np.interp(t, time_vec, w_f_vec)
    t_f = np.interp(t, time_vec, t_f_vec)
    x_f = np.interp(t, time_vec, x_f_vec)
    w_bin = np.interp(t, time_vec, w_bin_vec)
    x_bin = np.interp(t, time_vec, x_bin_vec)
    t_bin = np.interp(t, time_vec, t_bin_vec)
    
    G = 9.81  # gravity
    t_sin = params.t_sin  # incoming steam temperature (°C)
    A_s = params.A_s  # cross-sectional area of the evaporator (m2)
    A_o = params.A_o  # cross-sectional area of the brine outlet pipe (m2)
    A_e = params.A_e  # heat transfer area (m2)
    H = params.H  # height of the evaporator (m)
    b = 4.21  # constant for enthalphy calculation
    c = -6.2e-4  # constant for enthalphy calculation
    d = 4.459e-6  # constant for enthalphy calculation
    e = 1.8096  # constant for enthalphy calculation
    f = 5.087e-4  # constant for enthalphy calculation
    g = -1.221e-5  # constant for enthalphy calculation

    t_t = 0.5 * t_sin + 0.5 * t_v
    t_b = t_v + th.bpe(t_v, x)

    rho_b = th.calculate_liquid_density(t_b, x)  # density of brine pool (kg/m3)
    rho_v = th.calculate_vapor_density(t_v)  # density of vapor (kg/m3)

    m_b = rho_b * A_s * l_b  # mass of brine in the evaporator (kg)
    m_v = rho_v * A_s * (H - l_b)  # mass of vapor in the evaporator (kg)
    m = m_b + m_v  # total mass in the evaporator (kg)
    alpha = m_v / m  # mass fraction of vapor in the evaporator

    lambda_s = th.calculate_steam_latent_heat(t_t)
    lambda_v = th.calculate_steam_latent_heat(t_v)
    cp_f = th.calculate_heat_capacity(t_f, x_f)
    cp_bin = th.calculate_heat_capacity(t_bin, x_bin)

    h_f = th.calculate_liquid_water_enthalpy(t_f)
    h_bin = th.calculate_liquid_water_enthalpy(t_bin)
    h_b = th.calculate_liquid_water_enthalpy(t_b)
    h_v = th.calculate_vapor_water_enthalpy(t_v)
    h = (alpha * h_v) + ((1 - alpha) * h_b)
    Q_e = th.heat_transfer_rate(t_sin, t_v, A_e)
    Q_e = min(w_s * lambda_s, Q_e)
    w_v = (
        (Q_e) - (w_f * cp_f * (t_v - t_f)) + (w_bin * cp_bin * (t_bin - t_v))
    ) / lambda_v

    p_sat = th.Psat(t_v) * 1000.0
    p_sat_next = (
        p_sat - 2500.0
    )  # saturated pressure in next effect must be lower then previous effect
    l_next = 0.08  # level of next effect
    rho_next = rho_b + 20.0  # density of next level
    v_2 = (
        2.0
        * G
        * (
            (p_sat / (rho_b * G))
            + l_b
            - ((p_sat_next + rho_next * G * l_next) / (rho_b * G))
        )
    )
    v_b = np.sqrt(abs(v_2)) * np.sign(v_2)  # Brine outlet velocity (m/s)
    w_bout = rho_b * v_b * A_o

    dl = (w_f + w_bin - w_bout - w_v) / (A_s * (rho_b - rho_v))
    dx = ((w_f * (x_f - x)) + (w_bin * (x_bin - x)) + (w_v * x)) / (m)
    dt = (
        Q_e
        + w_f * (h_f - h)
        + w_bin * (h_bin - h)
        - w_bout * (h_b - h)      
    ) / (
        m
        * (
            (alpha * (e + 2 * f * t_v + 3 * g * t_v**2))
            + ((1 - alpha) * (b + 2 * c * t_b + 3 * d * t_b**2))
        )
    )

    return [dl, dx, dt]
