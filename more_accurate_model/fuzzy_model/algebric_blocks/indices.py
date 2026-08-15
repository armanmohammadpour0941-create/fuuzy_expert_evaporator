import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    

from more_accurate_model import thermo as th


# I_Q
def calculate_heat_index(w_s, t_sin):
    lambda_s = th.calculate_steam_latent_heat(t_sin)
    I_q = w_s * lambda_s
    return I_q

# I_w_in
def calculate_inlet_flow_index(w_f, w_bin):
    I_w_in = w_f + w_bin
    return I_w_in

# I_s_in
def calculate_salt_inlet_index(w_f, w_bin, x_f, x_bin):
    w_f_x_f = w_f * x_f
    w_b_x_b = w_bin * x_bin
    I_s_in = w_f_x_f + w_b_x_b
    return I_s_in

# I_h_in
def calculate_inlet_flow_enthalpy_index(w_f, w_bin, t_f, t_bin):
    
    h_f = th.calculate_liquid_water_enthalpy(t_f)
    h_bin = th.calculate_liquid_water_enthalpy(t_bin)
    
    w_f_h_f = w_f * h_f
    w_b_h_b = w_bin * h_bin
    I_h_in = w_f_h_f + w_b_h_b
    return I_h_in

