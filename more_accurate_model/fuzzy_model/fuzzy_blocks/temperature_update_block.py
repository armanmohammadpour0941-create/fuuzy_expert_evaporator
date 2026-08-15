import rule_activation as ra


def temperature_update(dT_dt, last_T):
    rule_table = [
        ["NL", "NL", "NL", "NS", "Z"],
        ["NL", "NS", "NS", "Z", "PS"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["NS", "Z", "PS", "PL", "PL"],
        ["Z", "PS", "PL", "PL", "PL"],
    ]
    # dT/dt
    input1_range = [0, -10, 10]
    # T(k-1)
    input2_range = [50, 40, 60]
    # T(k)
    output_range = [50, 40, 60]

    input1_crisp_value = dT_dt
    input2_crisp_value = last_T

    t = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return t
