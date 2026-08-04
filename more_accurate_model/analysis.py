import index_calculation as ic
import solution as sl
import solver


def find_states_and_outputs_bound(
    t_span,
    t_eval,
    x0,
    u_range: list[list[float]],
    d_range: list[list[float]],
    time_vec,
    params,
):
    n_eval = len(t_eval)
    w_s_range = u_range[0]
    w_f_range = u_range[1]

    t_f_range = d_range[0]
    x_f_range = d_range[1]
    w_bin_range = d_range[2]
    x_bin_range = d_range[3]
    t_bin_ranhe = d_range[4]

    w_s_op = w_s_range.pop(1)
    w_f_op = w_f_range.pop(1)

    t_f_op = t_f_range.pop(1)
    x_f_op = x_f_range.pop(1)
    w_bin_op = w_bin_range.pop(1)
    x_bin_op = x_bin_range.pop(1)
    t_bin_op = t_bin_ranhe.pop(1)

    input_and_distur_vec = [
        ("w_s", w_s_range),
        ("w_f", w_f_range),
        ("t_f", t_f_range),
        ("x_f", x_f_range),
        ("w_bin", w_bin_range),
        ("x_bin", x_bin_range),
        ("t_bin", t_bin_ranhe),
    ]
    output_resutl: list[list[list[float]]] = []
    for name, value in input_and_distur_vec:
        output_result_per_variable: list[list[float]] = [[], [], [], [], [], [], [], [], [], [], [], []]
        w_s = [w_s_op] * n_eval
        w_f = [w_f_op] * n_eval

        t_f = [t_f_op] * n_eval
        x_f = [x_f_op] * n_eval
        w_bin = [w_bin_op] * n_eval
        x_bin = [x_bin_op] * n_eval
        t_bin = [t_bin_op] * n_eval

        for i in range(2):
            if name == "w_s":
                w_s = [value[i]] * n_eval
            elif name == "w_f":
                w_f = [value[i]] * n_eval
            elif name == "t_f":
                t_f = [value[i]] * n_eval
            elif name == "x_f":
                x_f = [value[i]] * n_eval
            elif name == "w_bin":
                w_bin = [value[i]] * n_eval
            elif name == "x_bin":
                x_bin = [value[i]] * n_eval
            elif name == "t_bin":
                t_bin = [value[i]] * n_eval
            else:
                raise ValueError("the name not match")

            u = [w_s, w_f]
            d = [t_f, x_f, w_bin, x_bin, t_bin]
            sol = solver.evaporator_ode_solver(
                t_span, t_eval, x0, u, d, time_vec, params
            )
            w_v_vec = sl.calculate_vapor_flow_from_sol(sol, u, d, params)
            w_b_vec = sl.calculate_liquid_flow_from_sol(sol, params)
            (indices, _, _) = ic.calculate_all_indices(sol, u, d, params)

            l = sol.y[0][-1]
            x_b = sol.y[1][-1]
            t_v = sol.y[2][-1]
            w_v = w_v_vec[-1]
            w_b = w_b_vec[-1]
            i_q = indices[0][-1]
            i_th_f = indices[1][-1]
            i_th_b = indices[2][-1]
            i_w_in = indices[3][-1]
            i_s_in = indices[4][-1]
            i_h = indices[5][-1]
            i_h_in = indices[6][-1]

            iteration_result = [
                l,
                x_b,
                t_v,
                w_v,
                w_b,
                i_q,
                i_th_f,
                i_th_b,
                i_w_in,
                i_s_in,
                i_h,
                i_h_in,
            ]

            for j in range(len(iteration_result)):
                output_result_per_variable[j].append(iteration_result[j])
        output_resutl.append(output_result_per_variable)
    return output_resutl
