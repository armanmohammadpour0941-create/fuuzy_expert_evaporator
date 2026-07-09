import numpy as np
from evaporator_ode_solver import evaporator_ode_solver
X0 = [
    0.1,   # brine level (m)
    0.1,   # salinity (fraction)
    25,    # brine temperature (°C)
]

U = [
    20,     # W_s - steam flow rate (kg/s)
    100,   # W_f - feed flow rate (kg/s)
]

D = [
    20,    # T_f - feed temperature (°C)
    7,     # x_f - feed salinity (wt% or fraction)
    10,     # W_bin - brine inlet flow (kg/s)
    6,     # x_bin - brine inlet salinity (fraction)
    40,    # T_bin - brine inlet temperature (°C)
    18.0   # p_sat - saturation pressure (kPa)
]

t_span = (0, 3600)
t_eval = np.linspace(0, 3600, 5000)

evaporator_ode_solver(t_span, t_eval, X0, U, D, T_sin=55)