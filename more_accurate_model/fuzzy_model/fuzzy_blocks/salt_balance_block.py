from more_accurate_model.fuzzy_model import rule_activation as ra

DIFFERENCE_RULES = [
    ["Z", "NS", "NL", "NL", "NL"],
    ["PS", "Z", "NS", "NL", "NL"],
    ["PL", "PS", "Z", "NS", "NL"],
    ["PL", "PL", "PS", "Z", "NS"],
    ["PL", "PL", "PL", "PS", "Z"],
]

# E_s
def salt_balance(i_s_in, w_b, x):
    return ra.calculate_fuzzy_block_output(
        i_s_in,
        w_b * x,
        [340.0, 300.0, 380.0],
        [340.0, 320.0, 360.0],
        [0.0, -50.0, 50.0],
        DIFFERENCE_RULES,
        "centroid",
    )
