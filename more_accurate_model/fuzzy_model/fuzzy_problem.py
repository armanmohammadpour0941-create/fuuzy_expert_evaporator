"""Runnable example for the fuzzy evaporator model."""

import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np

from more_accurate_model import solution as sl
from more_accurate_model.fuzzy_model import fuzzy_solver
from more_accurate_model.problem import Params


def main(show_plots=True):
    t_eval = np.linspace(0.0, 1000.0, 1000)
    n_eval = len(t_eval)

    x0 = [0.05, 5.5, 45.0]
    w_s = [20.0] * n_eval
    w_f = [40.0] * n_eval
    t_f = [20.0] * n_eval
    x_f = [4.0] * n_eval
    w_bin = [30.0] * n_eval
    x_bin = [6.0] * n_eval
    t_bin = [60.0] * n_eval

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

    # Uncomment an assignment to create a 20% step at t = 250 s.
    for sample in range(n_eval // 2, n_eval):
        change_percentage = 0.10
        # w_s[sample] = 20.0 * (1.0 + change_percentage)
        # w_f[sample] = 40.0 * (1.0 + change_percentage)
        # t_f[sample] = 20.0 * (1.0 + change_percentage)
        # w_bin[sample] = 30.0 * (1.0 + change_percentage)
        _ = change_percentage

    result = fuzzy_solver.fuzzy_solver(
        t_eval,
        x0,
        [w_s, w_f],
        [t_f, w_bin],
        params,
    )

    print(
        f"Final level: {result.y[0, -1]:.4f} m\n"
        f"Final salinity: {result.y[1, -1]:.4f} wt%\n"
        f"Final temperature: {result.y[2, -1]:.4f} deg C\n"
        f"Final vapor flow: {result.w_v[-1]:.4f} kg/s\n"
        f"Final brine flow: {result.w_b[-1]:.4f} kg/s"
    )

    if show_plots:
        sl.plot_time_vector(result.t, result.w_v, "vapor flow", "kg/s")
        sl.plot_time_vector(result.t, result.w_b, "liquid flow", "kg/s")
        sl.plot_time_vector(result.t, result.y[0], "level", "m")
        sl.plot_time_vector(result.t, result.y[1], "salinity", "wt%")
        sl.plot_time_vector(result.t, result.y[2], "temperature", "deg C")
    return result


if __name__ == "__main__":
    main()
