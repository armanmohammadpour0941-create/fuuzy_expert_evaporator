from scipy.integrate import solve_ivp
import math
import numpy as np

X0 = [
    0.1,   # brine level (m)
    0.1,   # salinity (fraction)
    25,    # brine temperature (°C)
]

U = [
    20,     # W_s - steam flow rate (kg/s)
    130,   # W_f - feed flow rate (kg/s)
]

D = [
    25,    # T_f - feed temperature (°C)
    7,     # x_f - feed salinity (wt% or fraction)
    1,     # W_bin - brine inlet flow (kg/s)
    6,     # x_bin - brine inlet salinity (fraction)
    57,    # T_bin - brine inlet temperature (°C)
]

t_span = (0, 3600)
t_eval = np.linspace(0, 3600, 5000)

def evaporator_corrected(t, X, U, D):
    l, x, T_b = X
    W_s, W_f = U
    T_f, x_f, W_bin, x_bin, T_bin = D
    if t > 1800 :
       T_f = 30

    # Constants
    sea_dens = 1050    # kg/m3
    A = 8.64           # evaporator cross area m2
    A_o = 0.114        # cross area of brine outlet pipe
    C_d = 0.7          # discharge coefficient
    T_t = 55           # heating steam temperature °C
    Cp = 4.2           # kJ/kg°C
    A_heat = 2000      # heat transfer area m2
    
    # Calculate physical properties
    BPE = bpe(T_b, x)
    T_v = T_b - BPE  # Vapor temperature
    
    # Latent heats
    lambda_b = latent_heat(T_v)  # kJ/kg
    lambda_t = latent_heat(T_t)  # kJ/kg
    
    # Heat transfer rate (kW)
    Q_transfer = heat_transfer_rate(T_b, x, T_f, T_t, A_heat)
    
    # Maximum heat available from steam (kW)
    Q_steam = W_s * lambda_t
    
    # Actual heat transfer (kW)
    Q_e = min(Q_transfer, Q_steam)
    
    # Brine outlet flow (kg/s) - orifice equation
    kb = sea_dens * C_d * A_o * math.sqrt(2 * 9.8)
    W_bout = kb * math.sqrt(l)
    
    # Vaporization rate (kg/s)
    W_v = Q_e / lambda_b
    
    # ---- MASS BALANCES ----
    # Total mass balance
    dldt = (W_f + W_bin - W_bout - W_v) / (sea_dens * A)
    
    # Salt balance
    dxdt = (W_f*(x_f - x) + W_bin*(x_bin - x) + W_v*x) / (sea_dens * A * l)
    
    # ---- ENERGY BALANCE (CORRECTED) ----
    # The energy balance for the brine pool:
    # d(ρ*A*l*Cp*T_b)/dt = Energy_in - Energy_out
    
    # Energy_in:
    # - Sensible heat from feed: W_f*Cp*T_f
    # - Sensible heat from brine inlet: W_bin*Cp*T_bin  
    # - Heat transfer from steam: Q_e
    
    # Energy_out:
    # - Latent heat of vaporization: W_v*lambda_b
    # - Sensible heat of vapor: W_v*Cp*T_v (vapor carries some sensible heat)
    # - Sensible heat in brine outlet: W_bout*Cp*T_b
    
    # Accumulation term includes:
    # - Sensible heat of liquid
    # - Heat of mixing (neglected)
    
    # CORRECT FORMULATION:
    # ρ*A*Cp * d(l*T_b)/dt = Energy_in - Energy_out
    # ρ*A*Cp * (l*dT_b/dt + T_b*dl/dt) = Energy_in - Energy_out
    
    # Rearranging for dT_bdt:
    # l*dT_bdt = (Energy_in - Energy_out)/(ρ*A*Cp) - T_b*dl/dt
    
    energy_in = W_f * Cp * T_f + W_bin * Cp * T_bin + Q_e
    energy_out = W_v * lambda_b + W_v * Cp * T_v + W_bout * Cp * T_b
    
    # Option 1: Direct formulation (if dl/dt is small)
    # dT_bdt = (energy_in - energy_out) / (sea_dens * A * l * Cp)
    
    # Option 2: Proper formulation accounting for level change
    # This is more accurate
    term1 = (energy_in - energy_out) / (sea_dens * A * Cp)
    term2 = T_b * dldt
    dT_bdt = (term1 - term2) / l
    
    # Safety: Ensure temperature doesn't go below feed temperature
    # The feed is the minimum possible temperature
    if T_b < T_f and dT_bdt < 0:
        dT_bdt = max(dT_bdt, (T_f - T_b) * 0.01)  # Slowly warm up to feed temp
    
    # Print for debugging (optional)
    # if t % 100 < 0.1:
    #     print(f"t={t:.1f}, T_b={T_b:.2f}, Q_e={Q_e:.1f}, W_v={W_v:.2f}, dT={dT_bdt:.3f}")
    
    return [dldt, dxdt, dT_bdt]

def calculate_vapor_flow(sol, W_s, T_f=D[0]):
    T_t = 55           # heating steam temperature °C
    A_heat = 2000      # heat transfer area m2
    
    x_vec = sol.y[1]
    T_b_vec = sol.y[2]
    W_v_vec = []
   
    for i in range(len(T_b_vec)):
        if i > 2500:
            T_f = 30
        t_b = T_b_vec[i]
        x = x_vec[i]
        t_v = t_b - bpe(t_b, x)
            
        lambda_b = latent_heat(t_v)  # kJ/kg
        lambda_t = latent_heat(T_t)  # kJ/kg
        
        # Heat transfer rate (kW)
        Q_transfer = heat_transfer_rate(t_b, x, T_f, T_t, A_heat)
        
        # Maximum heat available from steam (kW)
        Q_steam = W_s * lambda_t
        
        # Actual heat transfer (kW)
        Q_e = min(Q_transfer, Q_steam)
    
        # Vaporization rate (kg/s)
        W_v = max(Q_e / lambda_b, 0.0)

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
    

def latent_heat(T):
    """Latent heat of vaporization in kJ/kg at temperature T (°C)"""
    # Using the Watson correlation with reference at 100°C (2257 kJ/kg)
    Tc = 374.15  # Critical temperature of water in °C
    Tr = (T + 273.15) / (Tc + 273.15)  # Reduced temperature
    if Tr > 0.99:
        Tr = 0.99
    h_vap = 2257 * ((1 - Tr) / (1 - 373.15/(Tc+273.15))) ** 0.38
    return h_vap

def bpe(T, X):
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
    T_v = T_b - bpe(T_b, x)
    # Prevent division by zero and ensure a physically meaningful driving temperature
    delta_T1 = max(T_t - T_v, 0.1)
    delta_T2 = max(T_v - T_f, 0.1)
    U_ht = heat_transfer_coeff(T_b)
    return U_ht * A_heat * ((T_t + T_f) - 2 * T_v) / math.log(delta_T1 / delta_T2)


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

# Run simulation with better solver settings
sol = solve_ivp(
    evaporator_corrected,
    t_span,
    X0,
    args=(U, D),
    method='Radau',  # Better for stiff systems
    t_eval=t_eval,
    rtol=1e-6,
    atol=1e-9,
    max_step=10  # Limit step size for stability
)
W_v = calculate_vapor_flow(sol, U[0])
W_b = calculate_liquid_flow(sol)
plot(sol, W_v, W_b)