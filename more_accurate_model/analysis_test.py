import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from dataclasses import dataclass

import numpy as np

from more_accurate_model import analysis


@dataclass
class Params:
    t_sin: float  # steam input temperature(deg C)
    A_s: float  # cross area of effect (m2)
    A_o: float  # cross area of brine outlet pipe(m2)
    A_e: float  # heat transfer area(m2)
    H: float  # hight of effect(m)
    boiling_temp: float  # boiling temperature at the effect pressure (deg C)
    seawater_salinity: list[float]
    previous_brine_salinity: list[float]
    previous_brine_temp: list[float]


t_span = (0, 1000)
t_eval = np.linspace(0, 1000, 1000)
n_eval = len(t_eval)

x0 = [0.1, 0.5, 30.0]

input_ranges = [
    [10, 20, 30],
    [30, 40, 50],
    [25, 30, 35],
]

disturbance_ranges = [
    [15, 20, 25],
]

x_bin = 6
t_bin = 60
x_f = 4
params = Params(
    t_sin=55.0,
    A_s=8.64,
    A_o=0.025,
    A_e=2000.0,
    H=4.0,
    boiling_temp=50.0,
    seawater_salinity=x_f,  # x_f - feed salinity (wt% or fraction)
    previous_brine_salinity=x_bin,  # x_bin - brine inlet salinity (fraction)
    previous_brine_temp=t_bin,  # T_bin - brine inlet temperature (°C)]
)

res = analysis.find_states_and_outputs_bound(
    t_span, t_eval, x0, input_ranges, disturbance_ranges, t_eval, params
)
analysis.save_result_to_csv(res)
