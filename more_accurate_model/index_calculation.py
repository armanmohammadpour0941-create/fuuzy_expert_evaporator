import thermo as th


def calculate_all_indices(sol, u, d, params):
    i_q = calculate_heat_index(u)
    i_w_in = calculate_inlet_flow_index(u, d)
    i_h_in = calculate_inlet_enthalpy_index(u, d, params)
    indices_vec = [i_q, i_w_in, i_h_in]
    label_vec = ["heat Index", "inlet flow index", "inlet salt index", "inlet enthalpy index"]
    unit_vec = ["kj/h", "kj/h", "kj/h", "kg/h", "", "kg","kj/kg"]
    return (indices_vec, label_vec, unit_vec)

def calculate_heat_index(u):
    w_s_vec, _ = u
    t_sin = [55] * len(w_s_vec)
    lambda_s_vec = th.calculate_steam_latent_heat_as_vec(t_sin)
    I_q = [w_s * lambda_s for w_s, lambda_s in zip(w_s_vec, lambda_s_vec)]
    return I_q

def calculate_inlet_flow_index(u, d):
    _, w_f_vec = u
    _, w_bin_vec = d 
    I_w_in = [w_f + w_bin for w_f, w_bin in zip(w_f_vec, w_bin_vec)]
    return I_w_in

def calculate_inlet_enthalpy_index(u, d, params):
    _, w_f_vec = u
    t_f_vec, w_bin_vec, = d
    t_bin_vec = params.previous_brine_temp
    h_f_vec = th.calculate_liquid_water_enthalpy_as_vec(t_f_vec)
    h_b_vec = th.calculate_liquid_water_enthalpy_as_vec(t_bin_vec)
    
    w_f_h_f = [w_f * h_f for w_f, h_f in zip(w_f_vec, h_f_vec)]
    w_b_h_b = [w_b * h_b for w_b, h_b in zip(w_bin_vec, h_b_vec)]
    I_h_in = [feed + brine for feed, brine in zip(w_f_h_f, w_b_h_b)]
    return I_h_in

        
    
    




