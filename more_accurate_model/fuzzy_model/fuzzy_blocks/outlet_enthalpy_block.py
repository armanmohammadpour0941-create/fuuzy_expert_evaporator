from more_accurate_model.fuzzy_model import rule_activation as ra

ADDITION_RULES = [
    ["NL", "NL", "NL", "NS", "Z"],
    ["NL", "NS", "NS", "Z", "PS"],
    ["NL", "NS", "Z", "PS", "PL"],
    ["NS", "Z", "PS", "PL", "PL"],
    ["Z", "PS", "PL", "PL", "PL"],
]

VAPOR_ENERGY_RANGE = [29184.44, 27000.0, 31370.0]
LIQUID_ENERGY_RANGE = [30440.22, 25800.0, 35000.0]

# E_h_out
def outlet_energy(w_v, w_b, temperature):
    vapor_energy = ra.calculate_fuzzy_block_output(
        w_v,
        temperature,
        [10.75, 5.0, 16.5],
        [57.28, 55.0, 59.0],
        VAPOR_ENERGY_RANGE,
        ADDITION_RULES,
        "centroid",
    )
    liquid_energy = ra.calculate_fuzzy_block_output(
        w_b,
        temperature,
        [59.25, 50.0, 70.0],
        [57.28, 55.0, 59.0],
        LIQUID_ENERGY_RANGE,
        ADDITION_RULES,
        "centroid",
    )
    return ra.calculate_fuzzy_block_output(
        vapor_energy,
        liquid_energy,
        VAPOR_ENERGY_RANGE,
        LIQUID_ENERGY_RANGE,
        [59624.67, 53000.0, 66300.0],
        ADDITION_RULES,
        "centroid",
    )
