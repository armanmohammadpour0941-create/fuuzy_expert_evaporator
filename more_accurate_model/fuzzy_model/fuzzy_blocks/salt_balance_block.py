from more_accurate_model.fuzzy_model import rule_activation as ra

DIFFERENCE_RULES = [
    ["Z", "NS", "NL", "NL", "NL"],
    ["PS", "Z", "NS", "NL", "NL"],
    ["PL", "PS", "Z", "NS", "NL"],
    ["PL", "PL", "PS", "Z", "NS"],
    ["PL", "PL", "PL", "PS", "Z"],
]

# Concentration-driving salt residual.  The second operand is the salt that
# would enter the liquid inventory if its concentration stayed at x.  Using
# w_b*x here gives a total salt-inventory balance, not dx/dt, and therefore
# gives the wrong transient sign whenever the brine level changes.
def salt_balance(i_s_in, i_w_in, w_v, x):
    concentration_demand = (i_w_in - w_v) * x
    concentration_residual = i_s_in - concentration_demand
    return ra.calculate_single_input_fuzzy_output(
        concentration_residual,
        [0.0, -60.0, 60.0],
        [0.0, -60.0, 60.0],
    )
