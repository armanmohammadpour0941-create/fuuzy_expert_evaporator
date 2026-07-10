def calculate_liquid_density(T, X):
    X = X * 10000.0  # convert salinity to ppm

    b = ((2 * X / 1000.0) - 150.0) / 150.0
    g1 = 0.5
    g2 = b
    g3 = 2 * b**2 - 1

    a1 = 4.03 * g1 + 0.1153 * g2 + 3.26e-4 * g3
    a2 = -0.1082 * g1 + 1.571e-3 * g2 - 4.23e-4 * g3
    a3 = -0.01224 * g1 + 1.74e-3 * g2 - 9.0e-6 * g3
    a4 = 6.92e-4 * g1 - 8.7e-5 * g2 - 5.3e-5 * g3

    a = ((2 * T) - 200.0) / 160.0
    f1 = 0.5
    f2 = a
    f3 = 2 * a**2 - 1
    f4 = 4 * a**3 - 3 * a

    rho_f = 1000.0 * (a1 * f1 + a2 * f2 + a3 * f3 + a4 * f4)
    return rho_f


def calculate_vapor_density(T):
    rho_v = (
        0.005059 + 0.00023748 * T + 1.777e-5 * T**2 - 4.327e-8 * T**3 + 4.342e-9 * T**4
    )
    return rho_v


def calculate_liquid_water_enthalpy(T):
    T = T + 273.15
    h_b = 0.063635409 + 4.21 * T - 6.2e-4 * T**2 + 4.459e-6 * T**3
    return h_b


def calculate_vapor_water_enthalpy(T):
    T = T + 273.15
    h_v = 2501.689 + 1.8096 * T + 5.087e-4 * T**2 - 1.221e-5 * T**3
    return h_v


def calculate_steam_latent_heat(T):
    h_b = calculate_liquid_water_enthalpy(T)
    h_v = calculate_vapor_water_enthalpy(T)
    latent_heat = h_v - h_b
    return latent_heat


def calculate_heat_capacity(T, X):
    T = T + 273.15    # convert to Kelvin
    X = X  # convert weight percentage to g/kg
    a = 4206.8 - 6.6179 * X + 1.2288e-2 * X**2
    b = -1.1262 + 5.4178e-2 * X - 2.2719e-4 * X**2
    c = 1.2026e-2 - 5.3366e-4 * X + 1.8906e-6 * X**2
    d = 6.8777e-7 + 1.517e-6 * X - 4.4267e-9 * X**2
    cp = a + b * T + c * T**2 + d * T**3
    return cp / 1000  # Convert from J/kg°C to kJ/kg°C


def bpe(T, X):
    T = T + 273.15
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
    bpe = (a0 + a1 * X + a2 * X**2 + a3 * X**3) * T + (b0 + b1 * X + b2 * X**2)
    return bpe

def Psat(T_C): 
    T = T_C
    return (10.1724607 - 0.6167302 * T + 1.832849e-2 * T**2
            - 1.77376e-4 * T**3 + 1.47068e-6 * T**4)    # P in kPa
 
def heat_transfer_coeff(T):
    """Heat transfer coefficient in kW/m²°C"""
    # Temperature dependent correlation
    U = 1.9695 + 1.2057e-2*T - 8.5989e-5*T**2 + 2.565e-7*T**3
    return U # Ensure minimum value

def heat_transfer_rate(t_t, t_v, a_e):
    u = heat_transfer_coeff(t_v)
    
    q = u * a_e * (t_t - t_v)
    return q
    
