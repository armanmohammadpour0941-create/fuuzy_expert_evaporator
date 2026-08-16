import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = next(p for p in FILE_PATH.parents if p.name == "fuuzy_expert_evaporator")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pytest

from more_accurate_model.fuzzy_model.fuzzy_solver import fuzzy_solver
from more_accurate_model.fuzzy_model.normaliziation import (
    denormalize_scale,
    normalize_scale,
)
from more_accurate_model.problem import Params
from more_accurate_model.solver import evaporator_ode_solver


STATE_SCALES = np.array([0.22, 4.0, 25.0])


def make_case(step=None, count=600):
    time = np.linspace(0.0, 600.0, count)
    vectors = {
        "w_s": np.full(count, 20.0),
        "w_f": np.full(count, 40.0),
        "w_bin": np.full(count, 30.0),
        "t_f": np.full(count, 20.0),
    }
    if step is not None:
        target, fractional_change = step
        vectors[target][count // 2 :] *= 1.0 + fractional_change

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
    return fuzzy, reference


def test_piecewise_scaling_preserves_asymmetric_operating_point():
    physical_range = [3.0, 1.0, 9.0]
    assert normalize_scale(1.0, physical_range) == pytest.approx(-5.0)
    assert normalize_scale(3.0, physical_range) == pytest.approx(0.0)
    assert normalize_scale(9.0, physical_range) == pytest.approx(5.0)
    for value in (1.0, 2.0, 3.0, 6.0, 9.0):
        assert denormalize_scale(
            normalize_scale(value, physical_range), physical_range
        ) == pytest.approx(value)


def test_baseline_is_stable_and_matches_reference():
    fuzzy, reference = make_case()
    assert fuzzy.y.shape == reference.y.shape
    assert len(fuzzy.w_v) == len(fuzzy.t)
    assert len(fuzzy.w_b) == len(fuzzy.t)
    assert np.all(np.isfinite(fuzzy.y))
    assert np.max(np.abs(fuzzy.y[:, -1] - reference.y[:, -1])) < 2.0e-3
    assert np.max(np.abs(np.diff(fuzzy.y[:, -50:], axis=1))) < 2.0e-3


@pytest.mark.parametrize(
    "step",
    [
        ("w_s", 0.20),
        ("w_s", -0.20),
        ("w_f", 0.20),
        ("w_f", -0.20),
        ("w_bin", 0.20),
        ("w_bin", -0.20),
        ("t_f", 0.20),
        ("t_f", -0.20),
    ],
)
def test_step_trajectories_match_reference(step):
    fuzzy, reference = make_case(step)
    post_step = slice(len(fuzzy.t) // 2, None)
    nrmse = (
        np.sqrt(np.mean((fuzzy.y[:, post_step] - reference.y[:, post_step]) ** 2, axis=1))
        / STATE_SCALES
    )
    assert np.all(nrmse < np.array([0.025, 0.015, 0.020]))
    assert np.all(np.abs(fuzzy.y[:, -1] - reference.y[:, -1]) < [0.004, 0.04, 0.35])
    assert np.all((0.0 < fuzzy.y[0]) & (fuzzy.y[0] < 0.25))
    assert np.all((4.0 < fuzzy.y[1]) & (fuzzy.y[1] < 8.0))
    assert np.all((40.0 < fuzzy.y[2]) & (fuzzy.y[2] < 70.0))


def test_solver_rejects_invalid_vectors():
    fuzzy, _ = make_case()
    count = len(fuzzy.t)
    params = Params(55.0, 8.64, 0.025, 2000.0, 4.0, 50.0, 4.0, 6.0, 60.0)
    with pytest.raises(ValueError, match="strictly increasing"):
        fuzzy_solver(
            fuzzy.t[::-1],
            [0.05, 5.5, 45.0],
            [[20.0] * count, [40.0] * count, [30.0] * count],
            [[20.0] * count],
            params,
        )
    with pytest.raises(ValueError, match="same length"):
        fuzzy_solver(
            fuzzy.t,
            [0.05, 5.5, 45.0],
            [[20.0] * count, [40.0] * (count - 1), [30.0] * count],
            [[20.0] * count],
            params,
        )
