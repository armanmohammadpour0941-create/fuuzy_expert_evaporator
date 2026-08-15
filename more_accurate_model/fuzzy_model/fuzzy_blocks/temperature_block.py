import rule_activation as ra


def temperature_derivative(e_h, l):
    rule_table = [
        ["Z", "NS", "NS", "NL", "NL"],
        ["PS", "Z", "NS", "NS","NL"],
        ["PL", "PS", "Z", "NS", "NL"],
        ["PL", "PS", "PS", "Z", "NS"],
        ["PL", "PL", "PS", "PS", "Z"]
    ]

    # E_h
    input1_range = [0, -1000, 1000]
    # level
    input2_range = [0.11, 0, 0.22]
    # dT/dt
    output_range = [0, -10, 10]

    input1_crisp_value = e_h
    input2_crisp_value = l

    dT_dt = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return dT_dt

