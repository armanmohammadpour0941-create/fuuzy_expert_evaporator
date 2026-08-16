from more_accurate_model.fuzzy_model import rule_activation as ra

INVERSE_INVENTORY_RULES = [
    ["NL", "NL", "NL", "NS", "NS"],
    ["NL", "NS", "NS", "NS", "NS"],
    ["Z", "Z", "Z", "Z", "Z"],
    ["PL", "PS", "PS", "PS", "PS"],
    ["PL", "PL", "PL", "PS", "PS"],
]


def salt_derivative(e_s, l):
    """Infer dx/dt; level changes magnitude but never reverses its sign."""

    return ra.calculate_fuzzy_block_output(
        e_s,
        l,
        [0.0, -50.0, 50.0],
        [0.12, 0.02, 0.22],
        [0.0, -0.003, 0.003],
        INVERSE_INVENTORY_RULES,
        "centroid",
    )
