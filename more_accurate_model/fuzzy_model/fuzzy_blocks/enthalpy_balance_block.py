from more_accurate_model.fuzzy_model import rule_activation as ra

DIFFERENCE_RULES = [
    ["Z", "NS", "NL", "NL", "NL"],
    ["PS", "Z", "NS", "NL", "NL"],
    ["PL", "PS", "Z", "NS", "NL"],
    ["PL", "PL", "PS", "Z", "NS"],
    ["PL", "PL", "PL", "PS", "Z"],
]

# E_h
def enthalpy_balance(e_h_in, e_h_out):
    return ra.calculate_fuzzy_block_output(
        e_h_in,
        e_h_out,
        [60670.99, 30000.0, 90000.0],
        [59624.67, 58000.0, 61250.0],
        [0.0, -10000.0, 10000.0],
        DIFFERENCE_RULES,
        "centroid",
    )
