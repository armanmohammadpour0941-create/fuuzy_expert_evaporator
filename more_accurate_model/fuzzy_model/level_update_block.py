import rule_activation as ra


def level_update(dl_dt, last_l):
    rule_table = [
        ["NL", "NL", "NL", "NS", "Z"],
        ["NL", "NS", "NS", "Z", "PS"],
        ["NL", "NS", "Z", "PS", "PL"],
        ["NS", "Z", "PS", "PL", "PL"],
        ["Z", "PS", "PL", "PL", "PL"],
    ]
    # dl/dt
    input1_range = [0, -10, 10]
    # L(k-1)
    input2_range = [0.11, 0, 0.22]
    # L(k)
    output_range = [0.11, 0, 0.22]

    input1_crisp_value = dl_dt
    input2_crisp_value = last_l

    l = ra.calculate_fuzzy_block_output(
        input1_crisp_value,
        input2_crisp_value,
        input1_range,
        input2_range,
        output_range,
        rule_table,
    )
    return l

