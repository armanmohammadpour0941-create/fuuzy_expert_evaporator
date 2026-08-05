from dataclasses import dataclass

import analysis
import numpy as np


@dataclass
class Params:
    t_sin: float  # steam input temperature(deg C)
    A_s: float  # cross area of effect (m2)
    A_o: float  # cross area of brine outlet pipe(m2)
    A_e: float  # heat transfer area(m2)
    H: float  # hight of effect(m)


params = Params(
    t_sin=55.0,
    A_s=8.64,
    A_o=0.025,
    A_e=2000.0,
    H=4.0,
)

t_span = (0, 5000)
t_eval = np.linspace(0, 5000, 5000)
n_eval = len(t_eval)

x0 = [0.1, 0.5, 30.0]

input_ranges = [
    [10, 20, 30],
    [30, 80, 130],
]

disturbance_ranges = [
    [15, 20, 25],
    [3, 4, 5],
    [25, 50, 75],
    [5, 6, 7],
    [35, 40, 45],
]

res = analysis.find_states_and_outputs_bound(t_span, t_eval, x0, input_ranges, disturbance_ranges, t_eval, params)
analysis.save_result_to_csv(res)