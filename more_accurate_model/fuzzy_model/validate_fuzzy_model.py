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


def build_case():
    count = 1000
    time = np.linspace(0.0, 1000.0, count)
    steam = np.full(count, 20.0)
    feed = np.full(count, 40.0)
    feed_temperature = np.full(count, 20.0)
    previous_brine = np.full(count, 30.0)
    params = Params(
        t_sin=55.0,
        A_s=8.64,
        A_o=0.025,
        A_e=2000.0,
        H=4.0,
        boiling_temp=50.0,
        seawater_salinity=np.full(count, 4.0),
        previous_brine_salinity=np.full(count, 6.0),
        previous_brine_temp=np.full(count, 60.0),
    )
    return time, [steam, feed], [feed_temperature, previous_brine], params


def main():
    time, inputs, disturbances, params = build_case()
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
    reference_vapor = np.asarray(
        calculate_vapor_flow_from_sol(reference, inputs, disturbances, params)
    )
    reference_brine = np.asarray(calculate_liquid_flow_from_sol(reference, params))

    output_dir = ROOT_DIR / "validation"
    output_dir.mkdir(exist_ok=True)
    figure_path = output_dir / "fuzzy_vs_dynamic.png"
    metrics_path = output_dir / "final_value_comparison.csv"

    series = [
        (fuzzy.y[0], reference.y[0], "Level", "m"),
        (fuzzy.y[1], reference.y[1], "Salinity", "wt%"),
        (fuzzy.y[2], reference.y[2], "Temperature", "°C"),
        (fuzzy.w_v, reference_vapor, "Vapor flow", "kg/s"),
        (fuzzy.w_b, reference_brine, "Brine flow", "kg/s"),
    ]
    figure, axes = plt.subplots(3, 2, figsize=(12, 10), sharex=True)
    for axis, (fuzzy_values, reference_values, label, unit) in zip(
        axes.flat, series, strict=False
    ):
        axis.plot(time, reference_values, label="ODE reference", linewidth=2.0)
        axis.plot(time, fuzzy_values, label="Corrected fuzzy", linewidth=1.8)
        axis.set_ylabel(f"{label} ({unit})")
        axis.grid(alpha=0.25)
    axes.flat[-1].axis("off")
    axes[0, 0].legend()
    axes[2, 0].set_xlabel("Time (s)")
    axes[1, 1].set_xlabel("Time (s)")
    figure.suptitle("Corrected fuzzy MED model vs dynamic reference")
    figure.tight_layout()
    figure.savefig(figure_path, dpi=180, bbox_inches="tight")
    plt.close(figure)

    with metrics_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["variable", "fuzzy_final", "ode_final", "absolute_error", "relative_error_percent"]
        )
        for fuzzy_values, reference_values, label, _ in series:
            fuzzy_final = float(fuzzy_values[-1])
            reference_final = float(reference_values[-1])
            absolute_error = abs(fuzzy_final - reference_final)
            relative_error = 100.0 * absolute_error / abs(reference_final)
            writer.writerow(
                [label, fuzzy_final, reference_final, absolute_error, relative_error]
            )

    print(f"Saved {figure_path}")
    print(f"Saved {metrics_path}")


if __name__ == "__main__":
    main()
