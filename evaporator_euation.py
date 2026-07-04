import math

from library import *

def evaporator_dynamic_model(t, x, u, d):
    l, x_b, T_effect = x
    W_s, W_f = u
    T_f, x_f, W_bin, x_bin, T_bin = d

    
      
    if t > 1800:
        #generate disturbances
        # T_f = 35  # feed temperature drops to 30°C after 180 seconds
        # x_f = 10  # feed salinity drops to 10% after 180 seconds

        # W_bin = 2  # brine inlet flow drops to 2 kg/s after 180 seconds

        # x_bin = 8  # brine salinity drops to 8% after 180 seconds

        # T_bin = 65  # brine temperature drops to 65°C after 180 seconds

        # #input changes
        # W_s = 35  # steam flow rate drops to 30 kg/s after 180 seconds

        W_f = 150  # feed flow rate drops to 150 kg/s after 180 seconds
        
    # Constants
    sea_dens = 1050    # kg/m3
    A = 8.64           # evaporator cross area m2
    A_o = 0.114        # cross area of brine outlet pipe
    C_d = 0.7          # discharge coefficient
    T_sin = 55         # heating steam temperature °C
    T_boiling = 50
    
    # l = max(l, 1e-4)  # Prevent non-physical negative values
    M_bp = sea_dens * A * l  # mass of brine in the evaporator
    
    T_t = (T_sin + T_effect) / 2
    lambda_t = latent_heat(T_t)  # Latent heat of vaporization (kJ/kg)
    Q_steam = W_s * lambda_t  # Heat provided by steam (kJ/s)
    lambda_eff = latent_heat(T_effect)  # Effective latent heat (kJ/kg)
    Cp_f = calculate_heat_capacity(T_f, x_f)  # Heat capacity of feed (kJ/kg°C)
    Cp_bin = calculate_heat_capacity(T_bin, x_bin)  # Heat capacity of brine inlet (kJ/kg°C)
    Cp_eff = calculate_heat_capacity(T_effect, x_b)  # Heat capacity of brine in evaporator (kJ/kg°C)
    V_film = (Q_steam - W_f * Cp_f * (T_boiling - T_f)) / lambda_eff
    # V_film = max(V_film, 0.0)  # Ensure non-negative vapor flow
    
    F_film_to_bp = W_f - V_film
    X_film = (W_f * x_f) / max(F_film_to_bp, 1e-3)  # Prevent division by zero
    
    v_bp = (W_bin * Cp_bin * (T_bin - T_boiling)) / lambda_eff
    # v_bp = max(v_bp, 0.0)  # Ensure non-negative vapor
    
    kb = sea_dens * C_d * A_o * math.sqrt(2 * 9.8)
    # W_bout = kb * math.sqrt(l)
    W_bout = kb * l
    dl_dt = (F_film_to_bp + W_bin - v_bp - W_bout) / (sea_dens * A)
    
    dx_dt = ((F_film_to_bp * (X_film - x_b)) + (W_bin * (x_bin - x_b))) / (M_bp)
    Q_in = Q_steam + W_f * Cp_f * T_f  + W_bin * Cp_bin * T_bin 
    Q_out = W_bout * Cp_eff * T_effect + (V_film + v_bp) * lambda_eff
    dT_effect_dt = (Q_in - Q_out) / (M_bp * Cp_eff)
    
    return [dl_dt, dx_dt, dT_effect_dt]

    