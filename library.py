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

