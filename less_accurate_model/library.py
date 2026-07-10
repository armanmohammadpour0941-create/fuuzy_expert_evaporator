import math
import numpy as np

G = 9.81  # m/s^2
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
    T_f, x_f, W_bin, x_bin, T_bin, p_sat = d
    t_effect_vec = sol.y[2]
    x_b_vec = sol.y[1]
    W_v_vec = []
   
    for i in range(len(t_effect_vec)):
        # if i > 2500:
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
      
        T_effect = t_effect_vec[i]
        x_b = x_b_vec[i]
        T_t = (T_sin + T_effect) / 2
        lambda_t = latent_heat(T_t)
        Cp_f = calculate_heat_capacity(T_f, x_f)
        Cp_bin = calculate_heat_capacity(T_bin, x_bin)
        lambda_eff = latent_heat(T_effect)
        T_b = T_effect + calculate_bpe(T_effect, x_b)
        t_sat = Tsat(p_sat)
        num = (W_s * lambda_t
            - W_f * Cp_f * (t_sat - T_f)
            + W_bin * Cp_bin * (T_bin - T_b))
        W_v = num / lambda_eff  # Vapor flow rate (kg/s) 
        

        W_v_vec.append(W_v)
    return W_v_vec

def calculate_liquid_flow(sol):  
    sea_dens = 1050    # kg/m3
    A_o = 0.114        # cross area of brine outlet pipe
    
    l_vec = sol.y[0]
    T_effect_vec = sol.y[2]
    W_bout_vec = []
   
    for i in range(0,len(l_vec)) :
        # if i > 2500:
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
        T_effect = T_effect_vec[i]
        l = l_vec[i]
        p = Psat(T_effect) * 1000.0  # Pa
        P_next = Psat(45.0) * 1000.0  # Pa
        rho_next = 1070.0
        L_next = 0.08
        v_2 = 2.0 * G * ((p / (sea_dens * G)) + l - ((P_next + rho_next * G * L_next) / (sea_dens * G)))
        v = np.sqrt(abs(v_2)) * np.sign(v_2)  # Brine outlet velocity (m/s)
        W_bout = sea_dens * v * A_o  # Brine outlet flow rate (kg/s)
        W_bout_vec.append(W_bout)

    return (W_bout_vec)
    
def calculate_heat_capacity(T, X):
    X = X * 10.0  # convert weight percentage to g/kg
    a = 4206.8 - 6.6179 * X + 1.2288e-2 * X**2
    b = -1.1262 + 5.4178e-2 * X - 2.2719e-4 * X**2
    c = 1.2026e-2 - 5.3366e-4 * X + 1.8906e-6 * X**2
    d = 6.8777e-7 + 1.517e-6 * X - 4.4267e-9 * X**2
    cp = a + b * T + c * T**2 + d * T**3
    return cp/1000  # Convert from J/kg°C to kJ/kg°C

def Psat(T_C): 
    T = T_C
    return (10.1724607 - 0.6167302 * T + 1.832849e-2 * T**2
            - 1.77376e-4 * T**3 + 1.47068e-6 * T**4)    # P in kPa
 
def Tsat(P_kPa):
    return (42.6776 - (3892.7 / (np.log(P_kPa / 1000.0) - 9.48654))) - 273.15

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
