import numpy as np
from dataclasses import dataclass
import thermo as th

G = 9.81

@dataclass
class MEDConfig:
    N: int = 1                      # number of effects
    A_s: float = 8.64               # brine pool cross-sectional area [m2] (per effect)
    A_E: float = 2000.0             # heat-transfer area, effect 1 [m2]
    A_E_taper: float = 0.85         # each subsequent effect's area = taper * previous
    # (sized so that U_E*A_E*LMTD is roughly consistent with the vapor
    #  generation rate implied by the Eq. 21 flash energy balance at the
    #  chosen flow rates -- otherwise the effect has no choice but to cool
    #  continuously to make up the energy shortfall. Area is tapered down
    #  along the train because later effects condense progressively less
    #  vapor.)

    def A_E_i(self, i):
        return self.A_E * (self.A_E_taper ** i)
    A_b: float = 0.1296             # brine downcomer/orifice cross-section [m2]
    # (sized so that, together with the small ~kPa inter-effect pressure
    #  drop, the resulting Bernoulli flow (Eq. 23) comes out the same
    #  order of magnitude as the feed/vapor flows chosen above -- a real
    #  design would size this from the actual mass-balance requirement)

    H_vessel: float = 4.0           # total vessel height used for vapor-space level [m]

    W_feed_total: float = 130.0      # total feed flow [kg/s], split evenly among effects
    T_feed: float = 25.0            # feed temperature [degC] (assumed pre-heated)
    X_feed: float = 6.0             # feed salinity [weight percentage]

    W_steam: float = 20.0            # motive/heating steam flow to effect 1 [kg/s]
    T_steam: float = 57.0            # motive steam (saturation) temperature [degC]
    
    W_b_prev: float = 90.0          # brine flow comes froms previous effect [kg/s]
    T_b_prev: float = 40.0          # previous effect brine pool temperature [degC]
    X_b_prev: float = 4.7           # previous effect brine salinity [weight percentage]
    
    T_next: float = 36.0
    L_next: float = 0.31
    X_next: float = 5.1

    # blow-down / final brine sump boundary condition (drives Eq. 23 for last effect)
    P_sump_kPa: float = None        # if None -> Psat(25 C)
    L_sump: float = 0.0

    def __post_init__(self):
        if self.P_sump_kPa is None:
            self.P_sump_kPa = th.Psat(25.0)


def effect_static_properties(T , X):
    """All algebraic (non-dynamic) properties of effect i needed by the
    balances: T_b,i, rho_f,i, rho_v,i, h_b,i, h_v,i, latent heat, and the
    required partial derivatives."""
    X_ppm = X * 10000.0
    Tb = T + th.BPE(T, X)
    rho_f = th.rho_seawater(Tb, X_ppm)
    rho_v = th.rho_vapor(T)
    h_b = th.h_liquid(Tb)
    h_v = th.h_vapor(T)
    lat = th.latent_heat(T)

    dBPE_dT = th.partial(th.BPE, T, X, wrt=0)
    dBPE_dX = th.partial(th.BPE, T, X, wrt=1)

    drhof_dTb = th.partial(th.rho_seawater, Tb, X_ppm, wrt=0)
    drhof_dX = th.partial(th.rho_seawater, Tb, X_ppm, wrt=1)

    drhov_dT = th.partial(th.rho_vapor, T, wrt=0)

    dhb_dTb = th.partial(th.h_liquid, Tb, wrt=0)
    dhv_dT = th.partial(th.h_vapor, T, wrt=0)

    return dict(Tb=Tb, rho_f=rho_f, rho_v=rho_v, h_b=h_b, h_v=h_v, lat=lat,
                dBPE_dT=dBPE_dT, dBPE_dX=dBPE_dX,
                drhof_dTb=drhof_dTb, drhof_dX=drhof_dX,
                drhov_dT=drhov_dT, dhb_dTb=dhb_dTb, dhv_dT=dhv_dT)

def vapor_flow_out(properties, 
                   W_v_prev, T_v_prev, W_b_prev, T_b_prev, X_b_prev,
                   T_v, T_feed, W_feed, X_feed):
    X_feed_gkg = X_feed * 10.0      # wight percentge to g/kg
    X_b_prev_gkg = X_b_prev * 10.0  # wight percentge to g/kg
    Cpf = th.Cp_water(T_feed, X_feed_gkg)
    Cpb_prev = th.Cp_water(T_b_prev, X_b_prev_gkg)
    latent_prev = th.latent_heat(T_v_prev)
    latent = properties['lat']
    
    num = (W_v_prev * latent_prev
           - W_feed * Cpf * (T_v - T_feed)
           + W_b_prev * Cpb_prev * (T_b_prev - T_v))
    return num / latent

def brine_flow_out(properties, cfg,
                   L, T_v,
                   L_next, T_next, X_next):
    A_b = cfg.A_b
    rho_f = properties['rho_f']
    p = th.Psat(T_v) * 1000.0       #Pa
    P_next = th.Psat(T_next) * 1000.0 #Pa
    
    X_next_ppm = X_next * 10000.0
    rho_next = th.rho_seawater(T_next, X_next_ppm)
    
    v_2 = 2.0 * G * ((p / (rho_f * G)) + L - ((P_next + rho_next * G * L_next) / (rho_f * G)))
    v = np.sqrt(v_2) if v_2 > 0.0 else 0.0
    return rho_f * v * A_b

def effect_derivatives(state, cfg, upstream):
    L, T, X = state
    
    W_feed = cfg.W_feed_total / cfg.N
    T_feed, X_feed = cfg.T_feed, cfg.X_feed

    prop = effect_static_properties(T, X, cfg)
    prop['Xppm'] = X * 10000.0
    Lv = max(cfg.H_vessel - L, 1e-3)

    # upstream is the detail of steam and brin inlet into effect
    W_v_prev = upstream['W_v_prev']
    T_v_prev = upstream['T_v_prev']
    W_b_prev = upstream['W_b_prev']
    T_b_prev = upstream['T_b_prev']
    X_b_prev = upstream['X_b_prev']
    
    W_v = vapor_flow_out(prop, W_v_prev, T_v_prev, W_b_prev, T_b_prev, X_b_prev, T, T_feed, W_feed, X_feed)
    W_v = max(W_v, 0.0)

    U_E = th.U_evaporator(prop['Tb'])
    if T_v_prev > T > T_feed:
        lmtd = ((T_v_prev + T_feed) - 2 * T) / np.log((T_v_prev - T) / (T - T_feed))
    else:
        lmtd = max(T_v_prev - T, 0.1)
    Q_E = U_E * cfg.A_E * lmtd

    return prop, Lv, W_v, Q_E
    
def build_k_coeffs(L, X, prop, Lv, As, Q_E,
                    W_feed, T_feed, X_feed,
                    W_b_prev, X_b_prev,
                    W_b, W_v, h_b_prev):
    rho_f, rho_v = prop['rho_f'], prop['rho_v']
    h_b, h_v = prop['h_b'], prop['h_v']
    dBPE_dT, dBPE_dX = prop['dBPE_dT'], prop['dBPE_dX']
    drhof_dTb, drhof_dX = prop['drhof_dTb'], prop['drhof_dX']
    drhov_dT = prop['drhov_dT']
    dhb_dTb, dhv_dT = prop['dhb_dTb'], prop['dhv_dT']

    k1 = As * rho_f - As * rho_v
    k2 = As * L * drhof_dTb * (1 + dBPE_dT) + As * Lv * drhov_dT
    k3 = As * L * (drhof_dTb * dBPE_dX + drhof_dX)
    k4 = W_feed + W_b_prev - W_b - W_v

    k5 = As * h_b * rho_f - As * h_v * rho_v
    k6 = (As * L * rho_f * dhb_dTb * (1 + dBPE_dT) + rho_v * As * Lv * dhv_dT) \
         + (As * L * h_b * drhof_dTb * (1 + dBPE_dT) + h_v * As * Lv * drhov_dT)
    k7 = As * L * rho_f * (dhb_dTb * dBPE_dX + 0.0) \
         + As * L * h_b * (drhof_dTb * dBPE_dX + drhof_dX)
    k8 = W_feed * th.h_liquid(T_feed) + W_b_prev * h_b_prev - W_b * h_b - W_v * h_v + Q_E

    k9 = As * rho_f * X
    k10 = As * X * L * drhof_dTb * (1 + dBPE_dT)
    k11 = As * L * (X * drhof_dTb * dBPE_dX + X * drhof_dX + rho_f)
    k12 = W_feed * X_feed + W_b_prev * X_b_prev - W_b * X

    return k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12

def state_derivatives_from_k(k):
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12 = k
    A = k1 * k11 - k3 * k9
    B = k2 * k11 - k3 * k10
    C = k4 * k11 - k3 * k12
    D = k5 * k11 - k7 * k9
    E = k6 * k11 - k7 * k10
    F = k8 * k11 - k7 * k12

    denom = A * E - B * D
    eps = 1e-9
    if abs(denom) < eps:
        denom = eps if denom >= 0 else -eps

    dL = (C * E - B * F) / denom
    dT = (A * F - C * D) / denom
    dX = (k12 - k9 * dL - k10 * dT) / k11
    return dL, dT, dX

    
    
    
