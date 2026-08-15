import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np

from more_accurate_model import solution as sl
from more_accurate_model.fuzzy_model import fuzzy_solver
from more_accurate_model.problem import Params

t_span = (0, 500)
t_eval = np.linspace(0, 500, 500)
n_eval = len(t_eval)

x0 = [0.05, 5.5, 45.0]
w_s = [20] * n_eval
w_f = [40] * n_eval

t_f = [20] * n_eval
x_f = [4] * n_eval
w_bin = [30] * n_eval
x_bin = [6] * n_eval
t_bin = [60] * n_eval

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

for i in range(int(n_eval / 2), n_eval):
    change_precentage = 0.2

    # w_s[i] = 20 * (1 + change_precentage)
    # w_f[i] = 40 * (1 + change_precentage)

    # input negative change
    # w_s[i] = 20 * (1 - change_precentage)
    # w_f[i] = 80 * (1 - change_precentage)

    # disturbance positive change
    # t_f[i] = 20 * (1 + change_precentage)
    # w_bin[i] = 50 * (1 + change_precentage)

    # disturbance negative change
    # t_f[i] = 20 * (1 - change_precentage)
    # w_bin[i] = 50 * (1 - change_precentage)


u = [w_s, w_f]
d = [
    t_f,  # T_f - feed temperature (°C)
    w_bin,  # W_bin - brine inlet flow (kg/s)
]

solution = fuzzy_solver.fuzzy_solver(t_eval, x0, u, d, params)
sl.plot_time_vector(solution.t, solution.w_v, "vapor_flow", "kg/h")
sl.plot_time_vector(solution.t, solution.w_b, "liquid_flow", "kg/h")
sl.plot_time_vector(t_eval, solution.y[0,:], "level", "m")
sl.plot_time_vector(t_eval, solution.y[1,:], "salinity", "% kg")
sl.plot_time_vector(t_eval, solution.y[2,:], "temperature", "deg C")

