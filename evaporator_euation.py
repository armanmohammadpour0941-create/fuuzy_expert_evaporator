import math
import numpy as np
from library import *

G = 9.81  # m/s^2
def evaporator_dynamic_model(t, x, u, d, T_sin):
    l, x_b, T_effect = x
    W_s, W_f = u
    T_f, x_f, W_bin, x_bin, T_bin, p_sat = d

    
      
    # if t > 1800:
        #generate disturbances
        # T_f = 25  # feed temperature drops to 30°C after 180 seconds
        # x_f = 10  # feed salinity drops to 10% after 180 seconds

        # W_bin = 20  # brine inlet flow drops to 2 kg/s after 180 seconds

        # x_bin = 10  # brine salinity drops to 8% after 180 seconds

        # T_bin = 45  # brine temperature drops to 65°C after 180 seconds
        
        # p_sat = 15.0  # saturation pressure (kPa)

        # #input changes
        # W_s = 25  # steam flow rate drops to 30 kg/s after 180 seconds

        # W_f = 120  # feed flow rate drops to 150 kg/s after 180 seconds
        
    # Constants
    sea_dens = 1050    # kg/m3
    A = 8.64           # evaporator cross area m2
    A_o = 0.114        # cross area of brine outlet pipe
    
    M_bp = sea_dens * A * l  # mass of brine in the evaporator
    
    T_t = 0.5 * T_sin + 0.5 *T_effect
    lambda_t = latent_heat(T_t)  # Latent heat of vaporization (kJ/kg)
    Q_steam = W_s * lambda_t  # Heat provided by steam (kJ/s)
    lambda_eff = latent_heat(T_effect)  # Effective latent heat (kJ/kg)
    Cp_f = calculate_heat_capacity(T_f, x_f)  # Heat capacity of feed (kJ/kg°C)
    Cp_bin = calculate_heat_capacity(T_bin, x_bin)  # Heat capacity of brine inlet (kJ/kg°C)
    Cp_eff = calculate_heat_capacity(T_effect, x_b)  # Heat capacity of brine in evaporator (kJ/kg°C)
    
    T_b = T_effect + calculate_bpe(T_effect, x_b)  # Boiling point elevation (°C)
    t_sat = Tsat(p_sat)  # Saturation temperature (°C)
    num = (W_s * lambda_t
           - W_f * Cp_f * (t_sat - T_f)
           - W_bin * Cp_bin * (T_bin - T_b))
    W_v = num / lambda_eff  # Vapor flow rate (kg/s)    
    Q_available = W_f * Cp_f * (t_sat - T_f) + W_bin * Cp_bin * (T_bin - T_b) + W_v * lambda_eff
    Q_e = min(Q_steam, Q_available)  # Actual heat transfer rate (kJ/s)
    p = Psat(T_effect) * 1000.0  # Pa
    P_next = Psat(45.0) * 1000.0  # Pa
    rho_next = 1070.0
    L_next = 0.08
    v_2 = 2.0 * G * ((p / (sea_dens * G)) + l - ((P_next + rho_next * G * L_next) / (sea_dens * G)))
    v = np.sqrt(abs(v_2)) * np.sign(v_2)  # Brine outlet velocity (m/s)
    W_bout = sea_dens * v * A_o  # Brine outlet flow rate (kg/s)
    dl_dt = (W_f + W_bin - W_v - W_bout) / (sea_dens * A)
    
    dx_dt = ((W_f * (x_f - x_b)) + (W_bin * (x_bin - x_b))) / (M_bp)
    Q_in = Q_e + W_f * Cp_f * T_f  + W_bin * Cp_bin * T_bin 
    Q_out = W_bout * Cp_eff * T_effect + W_v * lambda_eff
    dT_effect_dt = (Q_in - Q_out) / (M_bp * Cp_eff)
    
    return [dl_dt, dx_dt, dT_effect_dt]

    