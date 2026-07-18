import thermo as th
import numpy as np
import matplotlib.pyplot as plt


def calculate_vapor_flow_from_sol(sol, u, d, params):
    w_s_vec, w_f_vec = u
    t_f_vec, x_f_vec, w_bin_vec, x_bin_vec, t_bin_vec = d
    t_v_vec = sol.y[2]
    x_vec = sol.y[1]
    t_sin = params.t_sin
    A_e = params.A_e
    W_v_vec = []

    for i in range(len(t_v_vec)):
        # if i > 2500:
        # generate disturbances
        # T_f = 25  # feed temperature drops to 30°C after 180 seconds
        # x_f = 10  # feed salinity drops to 10% after 180 seconds

        # W_bin = 20  # brine inlet flow drops to 2 kg/s after 180 seconds

        # x_bin = 10  # brine salinity drops to 8% after 180 seconds

        # T_bin = 45  # brine temperature drops to 65°C after 180 seconds

        # p_sat = 15.0  # saturation pressure (kPa)

        # #input changes
        # W_s = 25  # steam flow rate drops to 30 kg/s after 180 seconds

        # W_f = 120  # feed flow rate drops to 150 kg/s after 180 seconds
        w_s = w_s_vec[i]
        w_f = w_f_vec[i]
        t_f = t_f_vec[i]
        x_f = x_f_vec[i]
        w_bin = w_bin_vec[i]
        x_bin = x_bin_vec[i]
        t_bin = t_bin_vec[i]

        t_v = t_v_vec[i]
        x = x_vec[i]
        t_b = t_v + th.bpe(t_v, x)
        t_t = 0.5 * t_sin + 0.5 * t_v
        lambda_s = th.calculate_steam_latent_heat(t_t)
        lambda_v = th.calculate_steam_latent_heat(t_v)
        cp_f = th.calculate_heat_capacity(t_f, x_f)
        cp_bin = th.calculate_heat_capacity(t_bin, x_bin)

        Q_e = th.heat_transfer_rate(t_sin, t_v, A_e)
        Q_e = max(w_s * lambda_s, Q_e)
        w_v = (
            (Q_e) - (w_f * cp_f * (t_v - t_f)) + (w_bin * cp_bin * (t_bin - t_b))
        ) / lambda_v

        W_v_vec.append(w_v)
    return W_v_vec


def calculate_liquid_flow_from_sol(sol, params):
    W_b_vec = []
    l_b_vec = sol.y[0]
    x_b_vec = sol.y[1]
    t_v_vec = sol.y[2]

    A_o = params.A_o
    G = 9.81
    for i in range(len(l_b_vec)):
        # if i > 2500:
        # generate disturbances
        # T_f = 25  # feed temperature drops to 30°C after 180 seconds
        # x_f = 10  # feed salinity drops to 10% after 180 seconds

        # W_bin = 20  # brine inlet flow drops to 2 kg/s after 180 seconds

        # x_bin = 10  # brine salinity drops to 8% after 180 seconds

        # T_bin = 45  # brine temperature drops to 65°C after 180 seconds

        # p_sat = 15.0  # saturation pressure (kPa)

        # #input changes
        # W_s = 25  # steam flow rate drops to 30 kg/s after 180 seconds

        # W_f = 120  # feed flow rate drops to 150 kg/s after 180 seconds
        t_v = t_v_vec[i]
        x_b = x_b_vec[i]
        l_b = l_b_vec[i]
        t_b = t_v + th.bpe(t_v, x_b)

        rho = th.calculate_liquid_density(t_b, x_b)
        p_sat = th.Psat(t_v) * 1000.0
        p_sat_next = p_sat - 2500.0
        l_next = 0.0
        rho_next = rho + 20.0
        v_2 = (
            2.0
            * G
            * (
                (p_sat / (rho * G))
                + l_b
                - ((p_sat_next + rho_next * G * l_next) / (rho * G))
            )
        )
        v_b = np.sqrt(abs(v_2)) * np.sign(v_2)  # Brine outlet velocity (m/s)
        w_b = rho * v_b * A_o
        W_b_vec.append(w_b)
    return W_b_vec


def plot_solver_result(sol):

    plt.figure(1)
    plt.plot(sol.t, sol.y[0], label="brine level")
    plt.xlabel("time (s)")
    plt.ylabel("level")
    plt.grid()
    plt.legend()

    plt.figure(2)
    plt.plot(sol.t, sol.y[1], label="salinity")
    plt.xlabel("time (s)")
    plt.ylabel("x")
    plt.grid()
    plt.legend()

    plt.figure(3)
    plt.plot(sol.t, sol.y[2], label="brine temperature")
    plt.xlabel("time (s)")
    plt.ylabel("Temperature")
    plt.grid()
    plt.legend()

    plt.show()


def plot_complete_solution(sol, W_v, W_b):

    plt.figure(1)
    plt.plot(sol.t, sol.y[0], label="brine level")
    plt.xlabel("time (s)")
    plt.ylabel("level")
    plt.grid()
    plt.legend()

    plt.figure(2)
    plt.plot(sol.t, sol.y[1], label="salinity")
    plt.xlabel("time (s)")
    plt.ylabel("x")
    plt.grid()
    plt.legend()

    plt.figure(3)
    plt.plot(sol.t, sol.y[2], label="brine temperature")
    plt.xlabel("time (s)")
    plt.ylabel("Temperature")
    plt.grid()
    plt.legend()

    plt.figure(4)
    plt.plot(sol.t, W_v, label="vapor rate")
    plt.xlabel("time (s)")
    plt.ylabel("kg/h")
    plt.grid()
    plt.legend()

    plt.figure(5)
    plt.plot(sol.t, W_b, label="brine liq rate")
    plt.xlabel("time (s)")
    plt.ylabel("kg/h")
    plt.grid()
    plt.legend()

    plt.show()


def print_final_value(sol, w_v, w_bout):
    level = sol.y[0][-1]
    x_b = sol.y[1][-1]
    t_v = sol.y[2][-1]
    w_v = w_v[-1]
    w_bout = w_bout[-1]
    print(
        f"brine pool level: {level:.2f} m\nbrinepool salinity: {x_b:.2f} weight percentage\neffect temperature: {t_v:.2f} deg C\nvapor flow rate: {w_v:.2f} kg/s\nliquid flow rate: {w_bout:.2f} kg/s"
    )
