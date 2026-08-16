import numpy as np
import skfuzzy as fuzz

from more_accurate_model.fuzzy_model import normaliziation as norm

LABELS = ("NL", "NS", "Z", "PS", "PL")


def calculate_fuzzy_block_output(
    input1_crisp_value,
    input2_crisp_value,
    input1_range,
    input2_range,
    output_range,
    rule_table,
    mod="centroid",
):
    """Evaluate a two-input Mamdani block and return a physical crisp value."""

    if len(rule_table) != 5 or any(len(row) != 5 for row in rule_table):
        raise ValueError("rule_table must be a 5 x 5 table.")
    unknown = {label for row in rule_table for label in row} - set(LABELS)
    if unknown:
        raise ValueError(f"Unknown fuzzy labels: {sorted(unknown)}")

    variable_range = np.linspace(-5.0, 5.0, 201)
    membership_functions = [
        fuzz.trimf(variable_range, [-5.0, -5.0, -3.0]),
        fuzz.trimf(variable_range, [-4.0, -2.5, -1.0]),
        fuzz.trimf(variable_range, [-2.0, 0.0, 2.0]),
        fuzz.trimf(variable_range, [1.0, 2.5, 4.0]),
        fuzz.trimf(variable_range, [3.0, 5.0, 5.0]),
    ]

    input1_normal = norm.normalize_scale(input1_crisp_value, input1_range)
    input2_normal = norm.normalize_scale(input2_crisp_value, input2_range)
    input1_memberships = [
        fuzz.interp_membership(variable_range, mf, input1_normal)
        for mf in membership_functions
    ]
    input2_memberships = [
        fuzz.interp_membership(variable_range, mf, input2_normal)
        for mf in membership_functions
    ]

    activations = {label: 0.0 for label in LABELS}
    for row, input1_membership in enumerate(input1_memberships):
        for column, input2_membership in enumerate(input2_memberships):
            label = rule_table[row][column]
            strength = float(np.fmin(input1_membership, input2_membership))
            activations[label] = max(activations[label], strength)

    clipped_outputs = [
        np.fmin(activations[label], membership_functions[index])
        for index, label in enumerate(LABELS)
    ]
    aggregated = np.maximum.reduce(clipped_outputs)
    if not np.any(aggregated > 0.0):
        raise ValueError(
            "No fuzzy rule was activated. Check the physical ranges and crisp inputs."
        )

    output_normal = fuzz.defuzz(variable_range, aggregated, mod)
    return norm.denormalize_scale(output_normal, output_range)
