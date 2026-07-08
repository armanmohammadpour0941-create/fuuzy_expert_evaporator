import numpy as np
from scipy.integrate import solve_ivp
import thermo as th
from model import (MEDConfig, effect_static_properties, vapor_flow_out,
                        brine_flow_out, build_k_coeffs, state_derivatives_from_k,
                        )


def rhs(t, y, cfg: MEDConfig):
    N = cfg.N
    L, T, X = y
    W_feed = cfg.W_feed_total / N
    T_feed = cfg.T_feed
    X_feed = cfg.X_feed

    prop = effect_static_properties(T, X)
    prop['Xppm'] = X * 10000.0

       
    W_v_prev, T_v_prev = cfg.W_steam, cfg.T_steam
    W_b_prev, T_b_prev, X_b_prev = cfg.W_b_prev, cfg.T_b_prev, cfg.X_b_prev

    W_v = vapor_flow_out(prop, W_v_prev, T_b_prev, W_b_prev, T_b_prev, X_b_prev, T, T_feed, W_feed, X_feed)
    W_v = max(W_v, 0.0)

    L_next = cfg.L_next
    T_next = cfg.T_next
    X_next = cfg.X_next
    W_b = brine_flow_out(prop, cfg, L, T, L_next, T_next, X_next)
    W_b = max(W_b, 0.0)

    As = cfg.A_s
    Lv = max(cfg.H_vessel - L, 1e-3)


    h_b_prev = th.h_liquid(cfg.T_feed)

    U_E = th.U_evaporator(prop['Tb'])
    if T_v_prev > T > cfg.T_feed:
        lmtd = ((T_v_prev + cfg.T_feed) - 2 * T) / np.log((T_v_prev - T) / (T - cfg.T_feed))
    else:
        lmtd = max(T_v_prev - T, 0.1)
    Q_E = U_E * cfg.A_E * lmtd

    W_v_in = cfg.W_steam 
    Q_available = W_v_in * th.latent_heat(T_v_prev)
    Q_E = min(Q_E, 0.95 * max(Q_available, 0.0))

    k = build_k_coeffs(L, X, prop, Lv, As, Q_E, W_feed, T_feed, X_feed, W_b_prev, X_b_prev, W_b, W_v, h_b_prev)
    dL, dT, dX = state_derivatives_from_k(k)
    dydt = [dL, dT, dX]

    return dydt, W_v, W_b


def rhs_ode(t, y, cfg):
    dydt, _, _ = rhs(t, y, cfg)
    return dydt


def run_simulation(cfg: MEDConfig, y0, t_span, n_eval):
    t_eval = np.linspace(*t_span, n_eval)
    sol = solve_ivp(rhs_ode, t_span, y0, args=(cfg,), method='BDF',
                     t_eval=t_eval, rtol=1e-6, atol=1e-6, max_step=10.0)
    return sol

def plot_sol(sol):
    import matplotlib.pyplot as plt

    plt.figure(1)
    plt.plot(sol.t, sol.y[0], label="brine level")
    plt.xlabel("time (s)")
    plt.ylabel("level")
    plt.grid()
    plt.legend()

    plt.figure(2)
    plt.plot(sol.t, sol.y[2], label="salinity")
    plt.xlabel("time (s)")
    plt.ylabel("x")
    plt.grid()
    plt.legend()

    plt.figure(3)
    plt.plot(sol.t, sol.y[1], label="brine temperature")
    plt.xlabel("time (s)")
    plt.ylabel("Temperature")
    plt.grid()
    plt.legend()

    plt.show() 
