import rule_activation as ra


def salt_updte(dx_dt, last_x):
    rule_table = [
        ["NL", "NL", "NL", "NS", "Z"],
        ["NL", "NS", "NS", "Z", "PS"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["NS", "Z", "PS", "PL", "PL"],
        ["Z", "PS", "PL", "PL", "PL"],
    ]
    # dx/dt
    input1_range = [0, -10, 10]
    # x(k-1)
    input2_range = [6, 5, 7]
    # x(k)
    output_range = [6, 5, 7]

    input1_crisp_value = dx_dt
    input2_crisp_value = last_x

    x = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return x

