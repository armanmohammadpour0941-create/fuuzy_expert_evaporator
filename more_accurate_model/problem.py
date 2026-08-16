import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from dataclasses import dataclass

import numpy as np

from more_accurate_model import index_calculation as ic
from more_accurate_model import solution as sl
from more_accurate_model import solver


@dataclass
class Params:
    t_sin: float  # steam input temperature(deg C)
    A_s: float  # cross area of effect (m2)
    A_o: float  # cross area of brine outlet pipe(m2)
    A_e: float  # heat transfer area(m2)
    H: float  # hight of effect(m)
    boiling_temp: float  # boiling temperature at the effect pressure (deg C)
    seawater_salinity: float
    previous_brine_salinity: float
    previous_brine_temp: float


def main():
    t_span = (0, 1000)
    t_eval = np.linspace(0, 1000, 1000)
    n_eval = len(t_eval)

    x0 = [0.01, 0.5, 30.0]
    w_s = [20] * n_eval
    w_f = [40] * n_eval
    w_bin = [30] * n_eval
    
    t_f = [20] * n_eval
    
    x_f = 4
    x_bin = 6
    t_bin = 60

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
        _ = change_precentage


    u = [w_s, w_f, w_bin]
    d = [t_f]   # T_f - feed temperature (°C)

    sol = solver.evaporator_ode_solver(t_span, t_eval, x0, u, d, t_eval, params)
    w_v = sl.calculate_vapor_flow_from_sol(sol, u, d, params)
    w_b = sl.calculate_liquid_flow_from_sol(sol, params)


    # sl.plot_solver_result(sol)

    # calculation Indices
    (indices, _, _) = ic.calculate_all_indices(sol, u, d, params)
    sl.print_final_value(sol, w_v, w_b, indices)
    sl.plot_complete_solution(sol, w_v, w_b)
    # sl.plot_indices(sol, indices, label, unit)
if __name__ == "__main__":
    main()