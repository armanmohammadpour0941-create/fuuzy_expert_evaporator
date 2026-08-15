import sys
from pathlib import Path

# Find the 'fuuzy_expert_evaporator' root folder automatically
FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from more_accurate_model import thermo as th


def calculate_vapor_flow_rate(x, x_f, x_bin, t_v, t_f, t_bin, t_sin, t_boil, w_s, w_f, w_bin):
    lambda_s = th.calculate_steam_latent_heat(t_sin)
    lambda_v = th.calculate_steam_latent_heat(t_v)
    cp_f = th.calculate_heat_capacity(t_f, x_f)
    cp_bin = th.calculate_heat_capacity(t_bin, x_bin)
    
    Q_e = w_s * lambda_s
    t_b = t_v + th.bpe(t_v, x)
    w_v_t = ((Q_e) + (w_f * cp_f * (t_f - t_boil))) / lambda_v
    w_v_f = w_bin * cp_bin * (t_bin - t_b) / lambda_v
    w_v = w_v_t + w_v_f
    return w_v
    
    
