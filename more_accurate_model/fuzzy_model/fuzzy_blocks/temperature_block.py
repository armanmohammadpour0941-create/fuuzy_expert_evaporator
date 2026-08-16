from more_accurate_model.fuzzy_model import rule_activation as ra

INVERSE_INVENTORY_RULES = [
    ["NL", "NL", "NL", "NS", "NS"],
    ["NL", "NS", "NS", "NS", "NS"],
    ["Z", "Z", "Z", "Z", "Z"],
    ["PL", "PS", "PS", "PS", "PS"],
    ["PL", "PL", "PL", "PS", "PS"],
]

#dT/dt
def temperature_derivative(e_h, l):
    return ra.calculate_fuzzy_block_output(
        e_h,
        l,
        [0.0, -20000.0, 20000.0],
        [0.12, 0.04, 0.22],
        [0.0, -3.0, 3.0],
        INVERSE_INVENTORY_RULES,
        "centroid",
        "sensitive",
    )
