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
    n_eval = len(time_vec)
    states = np.empty((3, n_eval), dtype=float)
    
    w_s_vec, w_f_vec = u
    t_f_vec, w_bin_vec = d

    x_f_vec = params.seawater_salinity
    x_bin_vec = params.previous_brine_salinity
    t_bin_vec = params.previous_brine_temp
    t_sin = params.t_sin
    t_boil = params.boiling_temp
    A_o = params.A_o
    w_v_out = []
    w_b_out = []   
    diagnostics = []
    
    states[:, 0] = np.asarray(x0, dtype=float)
    for sample in range(n_eval - 1):
        l = states[:, sample][0]
        x = states[:, sample][1]
        t_v = states[:, sample][2]

        w_s = w_s_vec[sample]
        w_f = w_f_vec[sample]

        t_f = t_f_vec[sample]
        w_bin = w_bin_vec[sample]

        x_f = x_f_vec[sample]
        x_bin = x_bin_vec[sample]
        t_bin = t_bin_vec[sample]

        w_v = vapor_flow.calculate_vapor_flow_rate(
            x, x_f, x_bin, t_v, t_f, t_bin, t_sin, t_boil, w_s, w_f, w_bin
        )
        w_b = liquid_flow.calculate_liquid_flow_rate(l, x, t_v, A_o)
        I_q = indices.calculate_heat_index(w_s, t_sin)
        I_w_in = indices.calculate_inlet_flow_index(w_f, w_bin)
        I_s_in = indices.calculate_salt_inlet_index(w_f, w_bin, x_f, x_bin)
        I_h_in = indices.calculate_inlet_flow_enthalpy_index(w_f, w_bin, t_f, t_bin)
        
        dl_dt = level_block.level_derivative(I_w_in, w_v, w_b)
        l_next = level_update_block.level_update(dl_dt, l)
        
        E_s = salt_balance_block.salt_balance(I_s_in, w_b, x)
        dx_dt = salt_block.salt_derivative(E_s, l_next)
        x_next = salt_update_block.salt_updte(dx_dt, x)
        
        E_h_in = I_q + I_h_in
        E_h_out = outlet_enthalpy_block.outlet_energy(w_v, w_b, t_v)
        E_h = enthalpy_balance_block.enthalpy_balance(E_h_in, E_h_out)
        
        dT_dt = temperature_block.temperature_derivative(E_h, l_next)
        t_v_next = temperature_update_block.temperature_update(dT_dt, t_v)
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
        
    solution = FuzzySolution(
        time_vec,
        states,
        w_v_out,
        w_b_out,
        diagnostics
    )
    return solution
