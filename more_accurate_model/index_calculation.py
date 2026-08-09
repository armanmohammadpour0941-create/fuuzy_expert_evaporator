import thermo as th


def calculate_all_indices(sol, u, d, params):
    i_q = calculate_heat_index(u)
    i_th_f = calculate_feed_thermal_input_index(u, d)
    i_th_b = calculate_brine_thermal_input_index(d)
    i_w_in = calculate_inlet_flow_index(u, d)
    i_s_in =calculate_salt_inlet_index(u, d)
    i_h = calculate_hold_up_index(sol, params)
    i_h_in = calculate_inlet_enthalpy_index(u, d)
    indices_vec = [i_q, i_th_f, i_th_b, i_w_in, i_s_in, i_h, i_h_in]
    label_vec = ["heat Index", "feed thermal index", "brine thermal index", "inlet flow index", "inlet salt index", "hold up index", "inlet enthalpy index"]
    unit_vec = ["kj/h", "kj/h", "kj/h", "kg/h", "", "kg","kj/kg"]
    return (indices_vec, label_vec, unit_vec)

def calculate_heat_index(u):
    w_s_vec, _ = u
    t_sin = [55] * len(w_s_vec)
    lambda_s_vec = th.calculate_steam_latent_heat_as_vec(t_sin)
    I_q = [w_s * lambda_s for w_s, lambda_s in zip(w_s_vec, lambda_s_vec)]
    return I_q


def calculate_feed_thermal_input_index(u, d):
    _, w_f_vec = u
    t_f_vec, x_f_vec, _, _, _ = d
    
    I_th_f_vec = []
    for i in range(len(w_f_vec)):          
        w_f = w_f_vec[i]
        t_f = t_f_vec[i]
        x_f = x_f_vec[i]
        cp_f = th.calculate_heat_capacity(t_f, x_f)
        I_th_f = w_f * cp_f * t_f
        I_th_f_vec.append(I_th_f)
    return I_th_f_vec

def calculate_brine_thermal_input_index(d):
    _, _, w_bin_vec, x_bin_vec, t_bin_vec = d
    I_th_b_vec = []
    for i in range(len(w_bin_vec)):          
        w_bin = w_bin_vec[i]
        t_bin = t_bin_vec[i]
        x_bin = x_bin_vec[i]
        cp_bin = th.calculate_heat_capacity(t_bin, x_bin)
        I_th_b = w_bin * cp_bin * t_bin
        I_th_b_vec.append(I_th_b)
    return I_th_b_vec

def calculate_inlet_flow_index(u, d):
    _, w_f_vec = u
    _, _, w_bin_vec, _, _ = d 
    I_w_in = [w_f + w_bin for w_f, w_bin in zip(w_f_vec, w_bin_vec)]
    return I_w_in

def calculate_salt_inlet_index(u, d):
    _, w_f_vec = u
    _, x_f_vec, w_bin_vec, x_bin_vec, _ = d 
    w_f_x_f = [w_f * x_f for w_f, x_f in zip(w_f_vec, x_f_vec)]
    w_b_x_b = [w_b * x_b for w_b, x_b in zip(w_bin_vec, x_bin_vec)]
    I_s_in = [feed + brine for feed, brine in zip(w_f_x_f, w_b_x_b)]
    return I_s_in

def calculate_hold_up_index(sol, params):
    l_vec = sol.y[0]
    x_vec = sol.y[1]
    t_v_vec = sol.y[2]
    
    A = params.A_s
    I_h_vec = []
    for i in range(len(l_vec)):
        l = l_vec[i]
        t_v = t_v_vec[i]
        x = x_vec[i]
        rho = th.calculate_liquid_density(t_v, x)
        i_h = rho * A * l
        I_h_vec.append(i_h)
    return I_h_vec

def calculate_inlet_enthalpy_index(u, d):
    _, w_f_vec = u
    t_f_vec, _, w_bin_vec, _, t_bin_vec = d
    h_f_vec = th.calculate_liquid_water_enthalpy_as_vec(t_f_vec)
    h_b_vec = th.calculate_liquid_water_enthalpy_as_vec(t_bin_vec)
    
    w_f_h_f = [w_f * h_f for w_f, h_f in zip(w_f_vec, h_f_vec)]
    w_b_h_b = [w_b * h_b for w_b, h_b in zip(w_bin_vec, h_b_vec)]
    I_h_in = [feed + brine for feed, brine in zip(w_f_h_f, w_b_h_b)]
    return I_h_in

        
    
    




