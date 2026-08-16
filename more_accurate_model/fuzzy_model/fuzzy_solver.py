import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dataclasses import dataclass

import numpy as np

from more_accurate_model.fuzzy_model.algebric_blocks import (
    indices,
    liquid_flow,
    vapor_flow,
)
from more_accurate_model.fuzzy_model.fuzzy_blocks import (
    enthalpy_balance_block,
    level_block,
    level_update_block,
    outlet_enthalpy_block,
    salt_balance_block,
    salt_block,
    salt_update_block,
    temperature_block,
    temperature_update_block,
)
from more_accurate_model.fuzzy_model.fuzzy_blocks.library import FuzzyStepResult


@dataclass
class FuzzySolution:
    
    t: np.ndarray
    y: np.ndarray
    w_v: np.ndarray
    w_b: np.ndarray
    diagnostics: list[FuzzyStepResult]
    
    
def fuzzy_solver(time_vec, x0, u, d, params):
    time_vec = np.asarray(time_vec, dtype=float)
    if time_vec.ndim != 1 or len(time_vec) < 2:
        raise ValueError("time_vec must be a one-dimensional vector with at least 2 points.")
    if np.any(np.diff(time_vec) <= 0.0):
        raise ValueError("time_vec must be strictly increasing.")

    n_eval = len(time_vec)
    states = np.empty((3, n_eval), dtype=float)

    if len(u) != 3:
        raise ValueError("u must contain [w_s, w_f, w_bin].")
    if len(d) != 1:
        raise ValueError("d must contain [t_f].")

    def trajectory(name, values):
        values = np.asarray(values, dtype=float)
        if values.shape != (n_eval,):
            raise ValueError(f"{name} must have the same length as time_vec.")
        if not np.all(np.isfinite(values)):
            raise ValueError(f"{name} must contain only finite values.")
        return values

    w_s_vec, w_f_vec, w_bin_vec = (
        trajectory("w_s", u[0]),
        trajectory("w_f", u[1]),
        trajectory("w_bin", u[2]),
    )
    t_f_vec = trajectory("t_f", d[0])

    x_f = params.seawater_salinity
    x_bin = params.previous_brine_salinity
    t_bin = params.previous_brine_temp
    t_sin = params.t_sin
    t_boil = params.boiling_temp
    A_o = params.A_o
    w_v_out = []
    w_b_out = []   
    diagnostics = []
    
    initial_state = np.asarray(x0, dtype=float)
    if initial_state.shape != (3,) or not np.all(np.isfinite(initial_state)):
        raise ValueError("x0 must contain three finite state values [level, salinity, temperature].")
    states[:, 0] = initial_state
    for sample in range(n_eval - 1):
        dt = time_vec[sample + 1] - time_vec[sample]
        l = states[:, sample][0]
        x = states[:, sample][1]
        t_v = states[:, sample][2]

        w_s = w_s_vec[sample]
        w_f = w_f_vec[sample]

        t_f = t_f_vec[sample]
        w_bin = w_bin_vec[sample]

        w_v = vapor_flow.calculate_vapor_flow_rate(
            x, x_f, x_bin, t_v, t_f, t_bin, t_sin, t_boil, w_s, w_f, w_bin
        )
        w_b = liquid_flow.calculate_liquid_flow_rate(l, x, t_v, A_o)
        I_q = indices.calculate_heat_index(w_s, t_sin)
        I_w_in = indices.calculate_inlet_flow_index(w_f, w_bin)
        I_s_in = indices.calculate_salt_inlet_index(w_f, w_bin, x_f, x_bin)
        I_h_in = indices.calculate_inlet_flow_enthalpy_index(w_f, w_bin, t_f, t_bin)
        
        dl_dt = level_block.level_derivative(I_w_in, w_v, w_b)
        l_next = level_update_block.level_update(dl_dt, l, dt)
        
        E_s = salt_balance_block.salt_balance(I_s_in, I_w_in, w_v, x)
        dx_dt = salt_block.salt_derivative(E_s, l_next)
        x_next = salt_update_block.salt_update(dx_dt, x, dt)
        
        E_h_in = I_q + I_h_in
        E_h_out = outlet_enthalpy_block.outlet_energy(
            w_v, w_f, w_bin, l_next, x_next, t_v, params
        )
        E_h = enthalpy_balance_block.enthalpy_balance(E_h_in, E_h_out)
        
        dT_dt = temperature_block.temperature_derivative(E_h, l_next)
        t_v_next = temperature_update_block.temperature_update(dT_dt, t_v, dt)
        next_state = [l_next, x_next, t_v_next]
        states[:, sample + 1] = np.asarray(next_state, dtype=float)
        step_result = FuzzyStepResult(
            l,
            x,
            t_v,
            dl_dt,
            l_next,
            E_s,
            dx_dt,
            x_next,
            E_h_in,
            E_h_out,
            E_h,
            dT_dt,
            t_v_next
        )
        diagnostics.append(step_result)
        w_v_out.append(w_v)
        w_b_out.append(w_b)

    # Evaluate algebraic outputs at the final state as well so every returned
    # trajectory has the same length as time_vec.
    l, x, t_v = states[:, -1]
    w_v_out.append(
        vapor_flow.calculate_vapor_flow_rate(
            x,
            x_f,
            x_bin,
            t_v,
            t_f_vec[-1],
            t_bin,
            t_sin,
            t_boil,
            w_s_vec[-1],
            w_f_vec[-1],
            w_bin_vec[-1],
        )
    )
    w_b_out.append(liquid_flow.calculate_liquid_flow_rate(l, x, t_v, A_o))
        
    solution = FuzzySolution(
        time_vec,
        states,
        np.asarray(w_v_out, dtype=float),
        np.asarray(w_b_out, dtype=float),
        diagnostics
    )
    return solution
