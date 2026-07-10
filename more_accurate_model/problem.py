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

x0 = [0.1, 
      0.5, 
      30.0
]

u = [60, 
     80
]  

d = [    
    20,    # T_f - feed temperature (°C)
    4,     # x_f - feed salinity (wt% or fraction)
    50,     # W_bin - brine inlet flow (kg/s)
    6,     # x_bin - brine inlet salinity (fraction)
    40,    # T_bin - brine inlet temperature (°C)] 
] 

t_span = (0, 3600)
t_eval = np.linspace(0, 3600, 5000)

solver.evaporator_ode_solver(t_span, t_eval, x0, u, d, params)