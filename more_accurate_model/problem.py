import numpy as np
from dataclasses import dataclass
import solver 

@dataclass
class Params:
    t_sin: float       # steam input temperature(deg C)
    A_s: float         # cross area of effect (m2)
    A_o: float         # cross area of brine outlet pipe(m2)
    A_e: float         # heat transfer area(m2)
    H: float           # hight of effect(m)
    
    
params = Params(
    t_sin=55.0,
    A_s=8.64,
    A_o=0.025,
    A_e=2000.0,
    H=4.0,
)

t_span = (0, 3600)
t_eval = np.linspace(0, 3600, 5000)
n_eval = len(t_eval)

x0 = [0.1, 
      0.5, 
      30.0
]

w_s = [60] * n_eval
w_f = [80] * n_eval
u = [w_s, 
     w_f
]  

t_f = [20] * n_eval
x_f = [4] * n_eval
w_bin = [50] * n_eval
x_bin = [6] * n_eval
t_bin = [40] * n_eval
d = [    
    t_f,    # T_f - feed temperature (°C)
    x_f,     # x_f - feed salinity (wt% or fraction)
    w_bin,     # W_bin - brine inlet flow (kg/s)
    x_bin,     # x_bin - brine inlet salinity (fraction)
    t_bin,    # T_bin - brine inlet temperature (°C)] 
] 

solver.evaporator_ode_solver(t_span, t_eval, x0, u, d, t_eval, params)