import solution as sl
import thermo as th


def calculate_all_indices(sol, u, d, params):
    i_w_in = calculate_inlet_flow_index(u, d)
    i_s_in = calculate_salt_inlet_index(u, d, params)
    E_s = calculate_salt_balance_index(sol, u, d, params)
    E_w_v = calculate_vapor_energy(sol, u, d, params)
    E_w_b = calculate_liquid_energy(sol, params)
    E_h_out = calculate_outlet_enthalpy_index(sol, u, d, params)
    E_h_in = calculate_inlet_enthalpy_index(u, d, params)
    E_h = calculate_energy_balance_index(sol, u, d, params)
    indices_vec = [i_w_in, i_s_in, E_s, E_w_v, E_w_b, E_h_out, E_h_in, E_h]
    label_vec = [
        "inlet flow index", 
        "inlet salt index", 
        "salt balance index",
        "vapor energy idex",
        "liquid energy index",
        "outlet enthalpy index",
        "inlet enthalpy index",
        "energy balance index"
        ]
    unit_vec = [
        "kg/h", 
        "kg/h", 
        "kg", 
        "kj/h", 
        "kj/h", 
        "kj/kg",
        "kj/kg",
        "kj"
        ]
    return (indices_vec, label_vec, unit_vec)

# I_Q
def calculate_heat_index(u):
    w_s_vec, _ = u
    t_sin = [55] * len(w_s_vec)
    lambda_s_vec = th.calculate_steam_latent_heat_as_vec(t_sin)
    I_q = [w_s * lambda_s for w_s, lambda_s in zip(w_s_vec, lambda_s_vec)]
    return I_q

# I_w_in
def calculate_inlet_flow_index(u, d):
    _, w_f_vec = u
    _, w_bin_vec = d 
    I_w_in = [w_f + w_bin for w_f, w_bin in zip(w_f_vec, w_bin_vec)]
    return I_w_in

# I_s_in
def calculate_salt_inlet_index(u, d, params):
    _, w_f_vec = u
    _, w_bin_vec= d 
    x_f_vec = params.seawater_salinity
    x_bin_vec = params.previous_brine_salinity
    w_f_x_f = [w_f * x_f for w_f, x_f in zip(w_f_vec, x_f_vec)]
    w_b_x_b = [w_b * x_b for w_b, x_b in zip(w_bin_vec, x_bin_vec)]
    I_s_in = [feed + brine for feed, brine in zip(w_f_x_f, w_b_x_b)]
    return I_s_in

# I_s_out
def calculate_salt_outlet_index(sol, params):
    x_b_vec = sol.y[1]
    w_b_vec = sl.calculate_liquid_flow_from_sol(sol, params)
    I_s_out = [x_b * w_b for x_b, w_b in zip(x_b_vec, w_b_vec)]
    return I_s_out

# E_s = I_s_in - I_s_out
def calculate_salt_balance_index(sol, u, d, params):
    i_s_in_vec = calculate_salt_inlet_index(u, d, params)
    i_s_out_vec = calculate_salt_outlet_index(sol, params)
    E_s = [i_s_in - i_s_out for i_s_in, i_s_out in zip(i_s_in_vec, i_s_out_vec)]
    return E_s

# I_h_in
def calculate_inlet_flow_enthalpy_index(u, d, params):
    _, w_f_vec = u
    t_f_vec, w_bin_vec, = d
    t_bin_vec = params.previous_brine_temp
    h_f_vec = th.calculate_liquid_water_enthalpy_as_vec(t_f_vec)
    h_b_vec = th.calculate_liquid_water_enthalpy_as_vec(t_bin_vec)
    
    w_f_h_f = [w_f * h_f for w_f, h_f in zip(w_f_vec, h_f_vec)]
    w_b_h_b = [w_b * h_b for w_b, h_b in zip(w_bin_vec, h_b_vec)]
    I_h_in = [feed + brine for feed, brine in zip(w_f_h_f, w_b_h_b)]
    return I_h_in

# E_w_v
def calculate_vapor_energy(sol, u, d, params):
    t_vec = sol.y[2]
    w_v_vec = sl.calculate_vapor_flow_from_sol(sol, u, d, params)
    h_v_vec = th.calculate_vapor_water_enthalpy_as_vec(t_vec)
    E_w_v = [w_v * h_v for w_v, h_v in zip(w_v_vec, h_v_vec)]
    return E_w_v

# E_w_b
def calculate_liquid_energy(sol, params):
    # x_vec = sol.y[1]
    t_vec = sol.y[2]
    t_b_vec = [t_v + 65.0 for t_v in t_vec]
    w_b_vec = sl.calculate_liquid_flow_from_sol(sol, params)
    h_b_vec = th.calculate_liquid_water_enthalpy_as_vec(t_b_vec)
    E_w_b = [w_b * h_b for w_b, h_b in zip(w_b_vec, h_b_vec)]
    return E_w_b
    
# E_h_out
def calculate_outlet_enthalpy_index(sol, u, d, params):
    E_w_v_vec = calculate_vapor_energy(sol, u, d, params)
    E_w_b_vec = calculate_liquid_energy(sol, params)
    E_h_out = [E_w_v + E_w_b for E_w_v, E_w_b in zip(E_w_v_vec, E_w_b_vec)]
    return E_h_out

# E_h_in
def calculate_inlet_enthalpy_index(u, d, params):
    I_q_vec = calculate_heat_index(u)
    I_h_in_vec = calculate_inlet_flow_enthalpy_index(u, d, params)
    E_h_in = [I_q + I_h_in for I_q, I_h_in in zip(I_q_vec, I_h_in_vec)]
    return E_h_in

# E_h = E_h_in - E_h_out
def calculate_energy_balance_index(sol, u, d, params):
    E_h_in_vec = calculate_inlet_enthalpy_index(u, d, params)
    E_h_out_vec = calculate_outlet_enthalpy_index(sol, u, d, params)
    E_h = [h_in - h_out for h_in, h_out in zip(E_h_in_vec, E_h_out_vec)]
    return E_h
    


    
    




