import rule_activation as ra


def salt_balance(i_s_in, w_b, x):
    rule_table = [
        ["Z", "NS", "NS", "NL", "NL"],
        ["PS", "Z", "NS", "NS", "NL"],
        ["PL", "PS", "Z", "NS", "NL"],
        ["PL", "PS", "PS", "Z", "NS"],
        ["PL", "PL", "PS", "PS", "Z"],
    ]

    # I_sin
    input1_range = [340, 300, 380]
    # I_sout
    input2_range = [340, 300, 380]
    # E_s
    output_range = [0, -100, 100]
    

    input1_crisp_value = i_s_in
    input2_crisp_value = w_b * x

    E_s = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return E_s

