import csv

from more_accurate_model import index_calculation as ic
from more_accurate_model import solution as sl
from more_accurate_model import solver


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
    w_bin_range = u_range[2]
    
    t_f_range = d_range[0]
    

    w_s_op = w_s_range.pop(1)
    w_f_op = w_f_range.pop(1)
    w_bin_op = w_bin_range.pop(1)
    
    t_f_op = t_f_range.pop(1)
    
    input_and_distur_vec = [
        ("w_s", w_s_range),
        ("w_f", w_f_range),
        ("t_f", t_f_range),
        ("w_bin", w_bin_range),
    ]
    output_resutl: list[list[list[float]]] = []
    for name, value in input_and_distur_vec:
        output_result_per_variable: list[list[float]] = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        w_s = [w_s_op] * n_eval
        w_f = [w_f_op] * n_eval

        t_f = [t_f_op] * n_eval
        w_bin = [w_bin_op] * n_eval

        for i in range(2):
            if name == "w_s":
                w_s = [value[i]] * n_eval
            elif name == "w_f":
                w_f = [value[i]] * n_eval
            elif name == "t_f":
                t_f = [value[i]] * n_eval
            elif name == "w_bin":
                w_bin = [value[i]] * n_eval
            else:
                raise ValueError("the name not match")

            u = [w_s, w_f, w_bin]
            d = [t_f]
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
            i_w_in = indices[0][-1]
            i_s_in = indices[1][-1]
            E_s = indices[2][-1]
            E_w_v = indices[3][-1] 
            E_w_b = indices[4][-1]
            E_h_out = indices[5][-1]
            E_h_in = indices[6][-1]
            E_h = indices[7][-1]

            iteration_result = [
                l,
                x_b,
                t_v,
                w_v,
                w_b,
                i_w_in,
                i_s_in,
                E_s,
                E_w_v,
                E_w_b,
                E_h_out,
                E_h_in,
                E_h,
            ]

            for j in range(len(iteration_result)):
                output_result_per_variable[j].append(iteration_result[j])
        output_resutl.append(output_result_per_variable)
    return output_resutl



def save_result_to_csv(result, filename="excel_files/output_result.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header (optional)
        num_cols = len(result[0])
        writer.writerow([f"Col {i}" for i in range(num_cols)])

        # Write each row
        for row in result:
            writer.writerow([f"[{x:.6f}, {y:.6f}]" for x, y in row])

    print(f"CSV file saved as '{filename}'")