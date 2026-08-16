import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import matplotlib.pyplot as plt
import numpy as np

from more_accurate_model import solution as sl
from more_accurate_model import solver
from more_accurate_model.fuzzy_model import fuzzy_solver
from more_accurate_model.problem import Params


def main(show_plots=True):
    t_span = (0, 1000)
    t_eval = np.linspace(0.0, 1000.0, 1000)
    n_eval = len(t_eval)

    x0 = [0.05, 5.5, 45.0]
    w_s = [20.0] * n_eval
    w_f = [40.0] * n_eval
    t_f = [20.0] * n_eval
    w_bin = [30.0] * n_eval
    
    x_f = 4.0
    x_bin = 6.0
    t_bin = 60.0

    params = Params(
        t_sin=55.0,
        A_s=8.64,
        A_o=0.025,
        A_e=2000.0,
        H=4.0,
        boiling_temp=50.0,
        seawater_salinity=x_f,
        previous_brine_salinity=x_bin,
        previous_brine_temp=t_bin,
    )

    for sample in range(n_eval // 2, n_eval):
        change_percentage = 0.10
        # w_s[sample] = 20.0 * (1.0 + change_percentage)
        # w_f[sample] = 40.0 * (1.0 + change_percentage)
        t_f[sample] = 20.0 * (1.0 + change_percentage)
        # w_bin[sample] = 30.0 * (1.0 + change_percentage)
        _ = change_percentage

    result = fuzzy_solver.fuzzy_solver(
        t_eval,
        x0,
        [w_s, w_f, w_bin],
        [t_f],
        params,
    )
    ode_result = solver.evaporator_ode_solver(t_span, t_eval, x0, [w_s, w_f, w_bin], [t_f], t_eval, params)
    ode_w_v = sl.calculate_vapor_flow_from_sol(ode_result, [w_s, w_f, w_bin], [t_f], params)
    ode_w_b = sl.calculate_liquid_flow_from_sol(ode_result, params)

    if show_plots:
        plt.figure(1)
        plt.plot(result.t, result.w_v, "--", label= "fuzzy model", lw=1.6)
        plt.plot(ode_result.t, ode_w_v, label="doe solver")
        plt.xlabel("time (s)")
        plt.ylabel("vapor flow (kg/s)")
        plt.grid()
        plt.legend()
        
        plt.figure(2)
        plt.plot(result.t, result.w_b, "--", label= "fuzzy model", lw=1.6)
        plt.plot(ode_result.t, ode_w_b, label="doe solver")
        plt.xlabel("time (s)")
        plt.ylabel("liquid flow (kg/s)")
        plt.grid()
        plt.legend()
        
        plt.figure(3)
        plt.plot(result.t, result.y[0], "--", label= "fuzzy model", lw=1.6)
        plt.plot(ode_result.t, ode_result.y[0], label="doe solver")
        plt.xlabel("time (s)")
        plt.ylabel("level (m)")
        plt.grid()
        plt.legend()
        
        plt.figure(4)
        plt.plot(result.t, result.y[1], "--", label= "fuzzy model", lw=1.6)
        plt.plot(ode_result.t, ode_result.y[1], label="doe solver")
        plt.xlabel("time (s)")
        plt.ylabel("salinity (g/g %)")
        plt.grid()
        plt.legend()
        
        plt.figure(5)
        plt.plot(result.t, result.y[2], "--", label= "fuzzy model", lw=1.6)
        plt.plot(ode_result.t, ode_result.y[2], label="doe solver")
        plt.xlabel("time (s)")
        plt.ylabel("temperature (C)")
        plt.grid()
        plt.legend()
        
        plt.show()
        
    return result


if __name__ == "__main__":
    main()
