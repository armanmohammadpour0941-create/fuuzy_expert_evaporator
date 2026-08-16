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
    energy_residual = e_h_in - e_h_out
    return ra.calculate_single_input_fuzzy_output(
        energy_residual,
        [0.0, -20000.0, 20000.0],
        [0.0, -20000.0, 20000.0],
    )
