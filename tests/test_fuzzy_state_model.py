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


def make_case(step=None):
    count = 1000
    time = np.linspace(0.0, 1000.0, count)
    steam = np.full(count, 20.0)
    feed = np.full(count, 40.0)
    feed_temperature = np.full(count, 20.0)
    previous_brine = np.full(count, 30.0)
    if step is not None:
        target, change = step
        vectors = {
            "steam": steam,
            "feed": feed,
            "feed_temperature": feed_temperature,
            "previous_brine": previous_brine,
        }
        vectors[target][count // 2 :] += change

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
    return fuzzy_solver(
        time,
        [0.05, 5.5, 45.0],
        [steam, feed],
        [feed_temperature, previous_brine],
        params,
    )


def test_piecewise_scaling_preserves_asymmetric_operating_point():
    physical_range = [3.0, 1.0, 9.0]
    assert normalize_scale(1.0, physical_range) == pytest.approx(-5.0)
    assert normalize_scale(3.0, physical_range) == pytest.approx(0.0)
    assert normalize_scale(9.0, physical_range) == pytest.approx(5.0)
    for value in (1.0, 2.0, 3.0, 6.0, 9.0):
        assert denormalize_scale(
            normalize_scale(value, physical_range), physical_range
        ) == pytest.approx(value)


def test_baseline_is_stable_and_close_to_reference_operating_point():
    result = make_case()
    assert result.y.shape == (3, len(result.t))
    assert len(result.w_v) == len(result.t)
    assert len(result.w_b) == len(result.t)
    assert np.all(np.isfinite(result.y))
    assert result.y[0, -1] == pytest.approx(0.1197, abs=0.01)
    assert result.y[1, -1] == pytest.approx(5.7385, abs=0.15)
    assert result.y[2, -1] == pytest.approx(57.2829, abs=1.0)
    assert np.max(np.abs(np.diff(result.y[:, -50:], axis=1))) < 2.0e-3


@pytest.mark.parametrize(
    "step",
    [
        ("steam", 4.0),
        ("steam", -4.0),
        ("feed", 8.0),
        ("previous_brine", 6.0),
        ("feed_temperature", 4.0),
    ],
)
def test_step_cases_remain_finite_and_inside_state_bounds(step):
    result = make_case(step)
    assert np.all(np.isfinite(result.y))
    assert np.all((0.0 <= result.y[0]) & (result.y[0] <= 0.22))
    assert np.all((4.0 <= result.y[1]) & (result.y[1] <= 8.0))
    assert np.all((40.0 <= result.y[2]) & (result.y[2] <= 65.0))


def test_time_vector_must_be_increasing():
    result = make_case()
    with pytest.raises(ValueError, match="strictly increasing"):
        fuzzy_solver(
            result.t[::-1],
            [0.05, 5.5, 45.0],
            [[20.0] * len(result.t), [40.0] * len(result.t)],
            [[20.0] * len(result.t), [30.0] * len(result.t)],
            Params(
                55.0,
                8.64,
                0.025,
                2000.0,
                4.0,
                50.0,
                [4.0] * len(result.t),
                [6.0] * len(result.t),
                [60.0] * len(result.t),
            ),
        )
