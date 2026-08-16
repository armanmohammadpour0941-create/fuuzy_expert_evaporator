from more_accurate_model.fuzzy_model import rule_activation as ra

DIFFERENCE_RULES = [
    ["Z", "NS", "NL", "NL", "NL"],
    ["PS", "Z", "NS", "NL", "NL"],
    ["PL", "PS", "Z", "NS", "NL"],
    ["PL", "PL", "PS", "Z", "NS"],
    ["PL", "PL", "PL", "PS", "Z"],
]

# dl/dt
def level_derivative(i_w_in, w_v, w_b):

    return ra.calculate_fuzzy_block_output(
        i_w_in,
        w_v + w_b,
        [70.0, 60.0, 80.0],
        [70.0, 68.0, 72.0],
        [0.0, -0.0005, 0.0005],
        DIFFERENCE_RULES,
        "centroid",
    )
