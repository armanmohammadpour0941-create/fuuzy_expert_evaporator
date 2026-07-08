import numpy as np

def Tsat(P_kPa):
    return (42.6776 - (3892.7 / (np.log(P_kPa) - 9.48654))) - 273.15
def Psat(T_C): 
    T = T_C
    return (10.1724607 - 0.6167302 * T + 1.832849e-2 * T**2
            - 1.77376e-4 * T**3 + 1.47068e-6 * T**4)    # P in kPa
    
def h_liquid(T_C):
    """Saturated liquid (brine/water) enthalpy [kJ/kg]  (Eq. A3)."""
    T = T_C
    return (0.063635409 + 4.207557011 * T - 6.200339e-4 * T**2
            + 4.459374e-6 * T**3)


def h_vapor(T_C):
    """Saturated vapor enthalpy [kJ/kg]  (Eq. A4)."""
    T = T_C
    return (2501.689845 + 1.806916015 * T + 5.087717e-4 * T**2
            - 1.221e-5 * T**3)


def latent_heat(T_C):
    """Latent heat of vaporization [kJ/kg]  (Eq. A5)."""
    T = T_C
    return 2589.583 + 0.9156 * T - 4.8343e-2 * T**2


# ----------------------------------------------------------------------
# A6 : seawater (brine) density.  X in ppm, T in degC  density in kg/m3
# ----------------------------------------------------------------------
def rho_seawater(T_C, X_ppm):
    T = T_C
    X = X_ppm
    B = (2.0 * (X / 1000.0) - 150.0) / 150.0
    G1, G2, G3 = 0.5, B, 2.0 * B**2 - 1.0

    A1 = 4.032219 * G1 + 0.115313 * G2 + 3.26e-4 * G3
    A2 = -0.108199 * G1 + 1.571e-3 * G2 - 4.23e-4 * G3
    A3 = -0.012247 * G1 + 1.74e-3 * G2 - 9e-6 * G3
    A4 = 6.92e-4 * G1 - 8.7e-5 * G2 - 5.3e-5 * G3

    A_ = (2.0 * T - 200.0) / 160.0
    F1 = 0.5
    F2 = A_
    F3 = 2.0 * A_**2 - 1.0
    F4 = 4.0 * A_**3 - 3.0 * A_

    return 1e3 * (A1 * F1 + A2 * F2 + A3 * F3 + A4 * F4)


# ----------------------------------------------------------------------
# A7 : vapor density.  T in degC
# ----------------------------------------------------------------------
def rho_vapor(T_C):
    T = T_C
    return (0.005059 + 0.00023748 * T + 1.777e-5 * T**2
            - 4.327e-8 * T**3 + 4.342e-9 * T**4)


def U_evaporator(T_b):
    T = T_b
    return (1.9695 + 1.2057e-2 * T - 8.5989e-5 * T**2 + 2.565e-7 * T**3)


# ----------------------------------------------------------------------
# A10 : specific heat of (sea)water at constant pressure [kJ/kg.K]
#        T in degC, X in g/kg
# ----------------------------------------------------------------------
def Cp_water(T_C, X_gkg):
    T = T_C
    X = X_gkg
    A = 4206.8 - 6.6197 * X + 1.2288e-2 * X**2
    B = -1.1262 + 5.4178e-2 * X - 2.2719e-4 * X**2
    C = 1.2026e-2 - 5.3566e-4 * X + 1.8906e-6 * X**2
    D = 6.8777e-7 + 1.517e-6 * X - 4.4268e-9 * X**2
    return 1e-3 * (A + B * T + C * T**2 + D * T**3)


# ----------------------------------------------------------------------
# A11 : boiling point elevation [degC].  T in degC, X in wt % (1-16 valid)
# ----------------------------------------------------------------------
def BPE(T_C, X_wt):
    T = T_C
    X = X_wt
    A = 8.325e-2 + 1.883e-4 * T + 4.02e-6 * T**2
    B = -7.625e-4 + 9.02e-5 * T - 5.2e-7 * T**2
    C = 1.522e-4 - 3e-6 * T - 3e-8 * T**2
    return X * (A + B * X + C * X**2)


# ----------------------------------------------------------------------
# unit-conversion wrappers so the rest of the code always works with
# the state variable X expressed in ppm
# ----------------------------------------------------------------------
def BPE_ppm(T_C, X_ppm):
    return BPE(T_C, X_ppm / 10000.0)   # ppm -> wt%


def Cp_ppm(T_C, X_ppm):
    return Cp_water(T_C, X_ppm / 1000.0)  # ppm -> g/kg


# ----------------------------------------------------------------------
# generic central-difference partial derivative helper
# ----------------------------------------------------------------------
def clip_T(T):
    """Keep temperature within the range the correlations were fitted over."""
    return float(np.clip(T, 10.0, 150.0))


def clip_X(X_ppm):
    """Keep salinity within the BPE correlation's valid range (1-16 wt%)."""
    return float(np.clip(X_ppm, 10000.0, 150000.0))


def partial(f, *args, wrt, h=None):
    """Numerical partial derivative of f(*args) w.r.t. args[wrt]."""
    args = list(args)
    x0 = args[wrt]
    if h is None:
        h = 1e-4 * abs(x0)
    args_p = args.copy(); args_p[wrt] = x0 + h
    args_m = args.copy(); args_m[wrt] = x0 - h
    return (f(*args_p) - f(*args_m)) / (2 * h)


