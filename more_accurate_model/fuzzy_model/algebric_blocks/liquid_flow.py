import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
import numpy as np

from more_accurate_model import thermo as th


def calculate_liquid_flow_rate(l, x, t_v, A_o):
    G = 9.81  # gravitational acceleration (m/s^2)
    t_b = t_v + th.bpe(t_v, x)
    rho_b = th.calculate_liquid_density(t_b, x)
    p_sat = th.Psat(t_v) * 1000.0
    p_sat_next = p_sat - 2000.0
    l_next = 0.0
    rho_next = rho_b + 5.0
    v_2 = (
        2.0
        * G
        * (
            (p_sat / (rho_b * G))
            + l
            - ((p_sat_next + rho_next * G * l_next) / (rho_b * G))
        )
    )
    v_b = np.sqrt(abs(v_2)) * np.sign(v_2)  # Brine outlet velocity (m/s)
    w_b = rho_b * v_b * A_o
    return w_b

    
    
