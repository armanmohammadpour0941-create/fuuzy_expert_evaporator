import numpy as np
import skfuzzy as fuzz

from more_accurate_model.fuzzy_model import normaliziation as norm

LABELS = ("NL", "NS", "Z", "PS", "PL")


def _membership_functions(variable_range, profile):
    if profile == "smooth":
        points = (
            (-5.0, -5.0, -3.0),
            (-4.0, -2.5, -1.0),
            (-2.0, 0.0, 2.0),
            (1.0, 2.5, 4.0),
            (3.0, 5.0, 5.0),
        )
    elif profile == "sensitive":
        # Adjacent negative/positive sets meet at zero.  This removes the
        # [-1, 1] normalized dead band of the smooth profile, which is useful
        # for balance residuals and state derivatives that must converge to
        # zero after a step.
        points = (
            (-5.0, -5.0, -2.5),
            (-5.0, -2.5, 0.0),
            (-1.5, 0.0, 1.5),
            (0.0, 2.5, 5.0),
            (2.5, 5.0, 5.0),
        )
    elif profile == "linear":
        # Ruspini partition used by one-input identity rules.  Adjacent
        # memberships sum to one, so height defuzzification reproduces a
        # linear residual without the gain humps of clipped-area centroid.
        points = (
            (-5.0, -5.0, -2.5),
            (-5.0, -2.5, 0.0),
            (-2.5, 0.0, 2.5),
            (0.0, 2.5, 5.0),
            (2.5, 5.0, 5.0),
        )
    else:
        raise ValueError("profile must be 'smooth', 'sensitive', or 'linear'.")
    return [fuzz.trimf(variable_range, point) for point in points]


def calculate_fuzzy_block_output(
    input1_crisp_value,
    input2_crisp_value,
    input1_range,
    input2_range,
    output_range,
    rule_table,
    mod="centroid",
    profile="smooth",
):
    if len(rule_table) != 5 or any(len(row) != 5 for row in rule_table):
        raise ValueError("rule_table must be a 5 x 5 table.")
    unknown = {label for row in rule_table for label in row} - set(LABELS)
    if unknown:
        raise ValueError(f"Unknown fuzzy labels: {sorted(unknown)}")

    variable_range = np.linspace(-5.0, 5.0, 201)
    membership_functions = _membership_functions(variable_range, profile)

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


def calculate_single_input_fuzzy_output(
    crisp_value,
    input_range,
    output_range,
    rule_labels=LABELS,
    mod="height",
    profile="linear",
):
    if len(rule_labels) != len(LABELS) or set(rule_labels) - set(LABELS):
        raise ValueError("rule_labels must contain five known fuzzy labels.")

    variable_range = np.linspace(-5.0, 5.0, 201)
    membership_functions = _membership_functions(variable_range, profile)
    normalized_input = norm.normalize_scale(crisp_value, input_range)
    input_memberships = [
        fuzz.interp_membership(variable_range, mf, normalized_input)
        for mf in membership_functions
    ]

    activations = {label: 0.0 for label in LABELS}
    for input_label_index, strength in enumerate(input_memberships):
        output_label = rule_labels[input_label_index]
        activations[output_label] = max(
            activations[output_label], float(strength)
        )

    if mod == "height":
        label_centers = dict(zip(LABELS, (-5.0, -2.5, 0.0, 2.5, 5.0)))
        total_activation = sum(input_memberships)
        if total_activation <= 0.0:
            raise ValueError("No single-input fuzzy rule was activated.")
        output_normal = sum(
            strength * label_centers[rule_labels[index]]
            for index, strength in enumerate(input_memberships)
        ) / total_activation
    else:
        clipped_outputs = [
            np.fmin(activations[label], membership_functions[index])
            for index, label in enumerate(LABELS)
        ]
        aggregated = np.maximum.reduce(clipped_outputs)
        if not np.any(aggregated > 0.0):
            raise ValueError("No single-input fuzzy rule was activated.")
        output_normal = fuzz.defuzz(variable_range, aggregated, mod)
    return norm.denormalize_scale(output_normal, output_range)
