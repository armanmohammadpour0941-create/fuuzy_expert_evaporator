import csv
import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import matplotlib.pyplot as plt
import numpy as np

from more_accurate_model.fuzzy_model.fuzzy_solver import fuzzy_solver
from more_accurate_model.problem import Params
from more_accurate_model.solution import (
    calculate_liquid_flow_from_sol,
    calculate_vapor_flow_from_sol,
)
from more_accurate_model.solver import evaporator_ode_solver

VARIABLES = (
    ("Level", "m", 0.22),
    ("Salinity", "wt%", 4.0),
    ("Temperature", "deg C", 25.0),
    ("Vapor flow", "kg/s", 15.0),
    ("Brine flow", "kg/s", 25.0),
)
STEP_VARIABLES = ("w_s", "w_f", "w_bin", "t_f")


def build_case(variable_name=None, step_change=0.0, count=1000):
    time = np.linspace(0.0, 1000.0, count)
    vectors = {
        "w_s": np.full(count, 20.0),
        "w_f": np.full(count, 40.0),
        "w_bin": np.full(count, 30.0),
        "t_f": np.full(count, 20.0),
    }
    if variable_name is not None:
        vectors[variable_name][count // 2 :] *= 1.0 + step_change

    params = Params(
        t_sin=55.0,
        A_s=8.64,
        A_o=0.025,
        A_e=2000.0,
        H=4.0,
        boiling_temp=50.0,
        seawater_salinity=4.0,
        previous_brine_salinity=6.0,
        previous_brine_temp=60.0,
    )
    inputs = [vectors["w_s"], vectors["w_f"], vectors["w_bin"]]
    disturbances = [vectors["t_f"]]
    return time, inputs, disturbances, params


def run_case(variable_name=None, step_change=0.0):
    time, inputs, disturbances, params = build_case(variable_name, step_change)
    initial_state = [0.05, 5.5, 45.0]
    fuzzy = fuzzy_solver(time, initial_state, inputs, disturbances, params)
    reference = evaporator_ode_solver(
        (time[0], time[-1]),
        time,
        initial_state,
        inputs,
        disturbances,
        time,
        params,
    )
    fuzzy_series = (fuzzy.y[0], fuzzy.y[1], fuzzy.y[2], fuzzy.w_v, fuzzy.w_b)
    reference_series = (
        reference.y[0],
        reference.y[1],
        reference.y[2],
        np.asarray(calculate_vapor_flow_from_sol(reference, inputs, disturbances, params)),
        np.asarray(calculate_liquid_flow_from_sol(reference, params)),
    )
    return time, fuzzy_series, reference_series


def main():
    scenarios = [("baseline", None, 0.0)]
    scenarios.extend((f"{name}_plus_20pct", name, 0.20) for name in STEP_VARIABLES)
    scenarios.extend((f"{name}_minus_20pct", name, -0.20) for name in STEP_VARIABLES)

    output_dir = ROOT_DIR / "validation"
    output_dir.mkdir(exist_ok=True)
    metrics_path = output_dir / "step_response_metrics.csv"
    compatibility_metrics_path = output_dir / "final_value_comparison.csv"
    figure_path = output_dir / "step_response_comparison.png"

    results = {}
    rows = []
    for scenario_name, variable_name, step_change in scenarios:
        time, fuzzy_series, reference_series = run_case(variable_name, step_change)
        results[scenario_name] = (time, fuzzy_series, reference_series)
        evaluation_slice = slice(len(time) // 2, None) if variable_name else slice(None)
        for (label, unit, scale), fuzzy_values, reference_values in zip(
            VARIABLES, fuzzy_series, reference_series, strict=True
        ):
            errors = fuzzy_values[evaluation_slice] - reference_values[evaluation_slice]
            rmse = float(np.sqrt(np.mean(errors**2)))
            rows.append(
                [
                    scenario_name,
                    label,
                    unit,
                    rmse,
                    100.0 * rmse / scale,
                    float(fuzzy_values[-1]),
                    float(reference_values[-1]),
                    float(abs(fuzzy_values[-1] - reference_values[-1])),
                ]
            )

    header = [
        "scenario",
        "variable",
        "unit",
        "rmse",
        "normalized_rmse_percent",
        "fuzzy_final",
        "ode_final",
        "final_absolute_error",
    ]
    for path in (metrics_path, compatibility_metrics_path):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)

    figure, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
    for column, step_variable in enumerate(STEP_VARIABLES):
        time, fuzzy_series, reference_series = results[f"{step_variable}_plus_20pct"]
        for row, (label, unit, _scale) in enumerate(VARIABLES[:3]):
            axes[row, column].plot(time, reference_series[row], label="ODE reference", lw=2.0)
            axes[row, column].plot(time, fuzzy_series[row], "--", label="Fuzzy", lw=1.6)
            axes[row, column].axvline(time[len(time) // 2], color="0.6", lw=0.8)
            axes[row, column].grid(alpha=0.25)
            axes[row, column].set_ylabel(f"{label} ({unit})")
        axes[0, column].set_title(f"+20% step in {step_variable}")
        axes[-1, column].set_xlabel("Time (s)")
    axes[0, 0].legend()
    figure.suptitle("Fuzzy MED model versus ODE reference: positive step tests")
    figure.tight_layout()
    figure.savefig(figure_path, dpi=180, bbox_inches="tight")
    plt.close(figure)

    state_labels = {"Level", "Salinity", "Temperature"}
    step_state_rows = [
        row for row in rows if row[0] != "baseline" and row[1] in state_labels
    ]
    worst = max(step_state_rows, key=lambda row: row[4])
    print(f"Saved {figure_path}")
    print(f"Saved {metrics_path}")
    print(
        "Worst step-response state NRMSE: "
        f"{worst[4]:.3f}% ({worst[0]}, {worst[1]})"
    )


if __name__ == "__main__":
    main()
