import rule_activation as ra


def enthalpy_balance(e_h_in, e_h_out):
    rule_table = [
        ["Z", "NS", "NL", "NL", "NL"],
        ["PS", "Z", "NS", "NL", "NL"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["PL", "PL", "PS", "Z", "NS"],
        ["PL", "PL", "PL", "PS", "Z"],
    ]

    # E_h_in
    input1_range = [60670.99, 30000, 90000]
    # E_h_out
    input2_range = [59624.67, 53000, 66300]
    #E_h
    output_range = [0, -1000, 1000]

    input1_crisp_value = e_h_in
    input2_crisp_value = e_h_out
    e_h = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return e_h