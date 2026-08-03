import thermo as th


def calculate_heat_index(sol, u):
    w_s_vec, _ = u
    t_v_vec = sol.y[2]
    lambda_s_vec = th.calculate_steam_latent_heat_as_vec(t_v_vec)
    I_q = [w_s * lambda_s for w_s, lambda_s in zip(w_s_vec, lambda_s_vec)]
    return I_q


def calculate_feed_thermal_input_index(sol, u, d):
    _, w_f_vec = u
    t_f_vec, x_f_vec, _, _, _ = d
    t_v_vec = sol.y[2]
    t_v = t_v_vec[-1]
    w_f = w_f_vec[-1]
    t_f = t_f_vec[-1]
    x_f = x_f_vec[-1]
    cp_f = th.calculate_heat_capacity(t_f, x_f)
    I_th_f = w_f * cp_f * (t_v - t_f)
    return I_th_f


# these function are better to calculte indices as vector not just final values
