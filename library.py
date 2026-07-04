import math


def latent_heat(T):
    """Latent heat of vaporization in kJ/kg at temperature T (°C)"""
    # Using the Watson correlation with reference at 100°C (2257 kJ/kg)
    Tc = 374.15  # Critical temperature of water in °C
    Tr = (T + 273.15) / (Tc + 273.15)  # Reduced temperature
    if Tr > 0.99:
        Tr = 0.99
    h_vap = 2257 * ((1 - Tr) / (1 - 373.15/(Tc+273.15))) ** 0.38
    return h_vap

def calculate_bpe(T, X):
    """Boiling point elevation in °C"""
    # More accurate correlation
    if X < 0.001:
        return 0
    # NaCl solution BPE
    a0 = -0.0007
    a1 = -0.0561
    a2 = 0.0891
    a3 = -0.0006
    b0 = -0.0004
    b1 = 0.0540
    b2 = -0.0002
    bpe = (a0 + a1*X + a2*X**2 + a3*X**3) * T + (b0 + b1*X + b2*X**2)
    return max(bpe, 0)

def heat_transfer_coeff(T):
    """Heat transfer coefficient in kW/m²°C"""
    # Temperature dependent correlation
    U = 1.9695 + 1.2057e-2*T - 8.5989e-5*T**2 + 2.565e-7*T**3
    return max(U, 0.5)  # Ensure minimum value


def heat_transfer_rate(T_b, x, T_f, T_t, A_heat):
    """Heat transfer rate in kW from steam to brine."""
    T_v = T_b - calculate_bpe(T_b, x)
    # Prevent division by zero and ensure a physically meaningful driving temperature
    delta_T1 = max(T_t - T_v, 0.1)
    delta_T2 = max(T_v - T_f, 0.1)
    U_ht = heat_transfer_coeff(T_b)
    return U_ht * A_heat * ((T_t + T_f) - 2 * T_v) / math.log(delta_T1 / delta_T2)

def calculate_vapor_flow(sol, u, T_sin, d):
    W_s , W_f = u
    T_f, x_f, W_bin, x_bin, T_bin = d
    t_effect_vec = sol.y[2]
    Cp = 4.2
    W_v_vec = []
   
    for i in range(len(t_effect_vec)):
        T_effect = t_effect_vec[i]
        T_t = (T_sin + T_effect) / 2
        lambda_t = latent_heat(T_t)
        Q_steam = W_s * lambda_t
        lambda_eff = latent_heat(T_effect)
        V_film = (Q_steam - W_f * Cp * (T_effect - T_f)) / lambda_eff
        v_bp = (W_bin * Cp * (T_bin - T_effect)) / lambda_eff
        W_v = v_bp + V_film
        

        W_v_vec.append(W_v)
    return W_v_vec

def calculate_liquid_flow(sol):  
    sea_dens = 1050    # kg/m3
    A_o = 0.114        # cross area of brine outlet pipe
    C_d = 0.7          # discharge coefficient

    l_vec = sol.y[0]
    W_bout_vec = []
   
    for i in range(0,len(l_vec)) :
        l = l_vec[i]
        kb = sea_dens * C_d * A_o * math.sqrt(2 * 9.8)
        W_bout = kb * math.sqrt(l)
        W_bout_vec.append(W_bout)

    return (W_bout_vec)
    
def plot(sol, W_v, W_b):
    import matplotlib.pyplot as plt

    plt.figure(1)
    plt.plot(sol.t, sol.y[0], label="brine level")
    plt.xlabel("time (s)")
    plt.ylabel("level")
    plt.grid()
    plt.legend()

    plt.figure(2)
    plt.plot(sol.t, sol.y[1], label="salinity")
    plt.xlabel("time (s)")
    plt.ylabel("x")
    plt.grid()
    plt.legend()

    plt.figure(3)
    plt.plot(sol.t, sol.y[2], label="brine temperature")
    plt.xlabel("time (s)")
    plt.ylabel("Temperature")
    plt.grid()
    plt.legend()

    plt.figure(4)
    plt.plot(sol.t, W_v, label="vapor rate")
    plt.xlabel("time (s)")
    plt.ylabel("kg/h")
    plt.grid()
    plt.legend()

    plt.figure(5)
    plt.plot(sol.t, W_b, label="brine liq rate")
    plt.xlabel("time (s)")
    plt.ylabel("kg/h")
    plt.grid()
    plt.legend()

    plt.show() 
