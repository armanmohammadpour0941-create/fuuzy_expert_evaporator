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
    flow_residual = i_w_in - (w_v + w_b)
    return ra.calculate_single_input_fuzzy_output(
        flow_residual,
        [0.0, -15.0, 15.0],
        [0.0, -0.00170, 0.00170],
    )
