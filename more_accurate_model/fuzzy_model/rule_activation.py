
import numpy as np
import skfuzzy as fuzz

from more_accurate_model.fuzzy_model import normaliziation as norm


def calculate_fuzzy_block_output(
    input1_crisp_value,
    input2_crisp_value,
    input1_range: list[float, float, float],
    input2_range: list[float, float, float],
    output_range: list[float, float, float],
    rule_table: list[list[str]]
):
    variable_range = np.arange(-5, 5.5, 0.5)

    nl = fuzz.trimf(variable_range, [-5, -5, -3])
    ns = fuzz.trimf(variable_range, [-4, -2.5, -1])
    z = fuzz.trimf(variable_range, [-2, 0, 2])
    ps = fuzz.trimf(variable_range, [1, 2.5, 4])
    pl = fuzz.trimf(variable_range, [3, 5, 5])
    mf_list = [nl, ns, z, ps, pl]

    input1_normal_value = norm.normalize_scale(input1_crisp_value, input1_range)
    input2_normal_value = norm.normalize_scale(input2_crisp_value, input2_range)
    input1_membership = []
    input2_membership = []
    rule_activation_matrix: list[list[(str, float)]] = [[], [], [], [], []]
    for mf in mf_list:
        input1 = fuzz.interp_membership(variable_range, mf, input1_normal_value)
        input2 = fuzz.interp_membership(variable_range, mf, input2_normal_value)
        input1_membership.append(input1)
        input2_membership.append(input2)
    for i in range(len(input1_membership)):
        input1_mf = input1_membership[i]
        for j in range(len(input2_membership)):
            input2_mf = input2_membership[j]
            activation = np.fmin(input1_mf, input2_mf)
            rule_activation_matrix[i].append((rule_table[i][j], activation))
    N_l = []
    N_s = []
    zero = []
    P_s = []
    P_l = []
    for row in rule_activation_matrix:
        for name, activation in row:
            if name == "NL":
                N_l.append(activation)
            elif name == "NS":
                N_s.append(activation)
            elif name == "Z":
                zero.append(activation)
            elif name == "PS":
                P_s.append(activation)
            elif name == "PL":
                P_l.append(activation)
    output_nl = np.fmin(max(N_l), nl)
    output_ns = np.fmin(max(N_s), ns)
    output_z = np.fmin(max(zero), z)
    output_ps = np.fmin(max(P_s), ps)
    output_pl = np.fmin(max(P_l), pl)

    aggregated = np.fmax(output_nl, np.fmax(output_ns, np.fmax(output_z, np.fmax(output_ps, output_pl))))
    output_normal = fuzz.defuzz(variable_range, aggregated, 'mom')
    denormal_output = norm.denormalize_scale(output_normal, output_range)
    
    # dl0 = np.zeros_like(variable_range)
    # fig, ax0 = plt.subplots(figsize=(8, 3)) 
    # ax0.fill_between(variable_range, dl0, output_nl, facecolor='b', alpha=0.7)
    # ax0.plot(variable_range, nl, 'b', linewidth=0.5, linestyle='--', )
    # ax0.fill_between(variable_range, dl0, output_ns, facecolor='g', alpha=0.7)
    # ax0.plot(variable_range, ns, 'g', linewidth=0.5, linestyle='--')
    # ax0.fill_between(variable_range, dl0, output_z, facecolor='r', alpha=0.7)
    # ax0.plot(variable_range, z, 'r', linewidth=0.5, linestyle='--')
    # ax0.fill_between(variable_range, dl0, output_ps, facecolor='g', alpha=0.7)
    # ax0.plot(variable_range, ps, 'g', linewidth=0.5, linestyle='--')
    # ax0.fill_between(variable_range, dl0, output_pl, facecolor='r', alpha=0.7)
    # ax0.plot(variable_range, pl, 'r', linewidth=0.5, linestyle='--')
    # ax0.set_title('Output membership activity')

    # # Turn off top/right axes
    # for ax in (ax0,):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()

    # plt.tight_layout()
    # # plt.show()
    return denormal_output
