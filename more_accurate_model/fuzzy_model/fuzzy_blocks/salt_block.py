from more_accurate_model.fuzzy_model import rule_activation as ra

INVERSE_INVENTORY_RULES = [
    ["NL", "NL", "NL", "NS", "NS"],
    ["NL", "NS", "NS", "NS", "NS"],
    ["Z", "Z", "Z", "Z", "Z"],
    ["PL", "PS", "PS", "PS", "PS"],
    ["PL", "PL", "PL", "PS", "PS"],
]

# dx/dt
def salt_derivative(e_s, l):
    return ra.calculate_fuzzy_block_output(
        e_s,
        l,
        [0.0, -60.0, 60.0],
        [0.12, 0.04, 0.22],
        [0.0, -0.030, 0.030],
        INVERSE_INVENTORY_RULES,
        "centroid",
        "sensitive",
    )
