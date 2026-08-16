# Fuzzy-state solver correction

## Root cause

The algebraic vapor and brine-flow equations were not the source of the bad
state trajectories. The recurrent state update was.

The previous implementation defuzzified an absolute next state from
`(state derivative, previous state)` at every sample. With only five output
sets, this quantized the recurrent state. `som` made the problem larger by
selecting the left edge of a maximum. For example, a zero derivative at the
physical steady point did not preserve `(L, x, T) = (0.12, 5.74, 57.28)`.

There were also two rule-design problems:

- the level and balance tables were not consistent inlet-minus-outlet tables;
- the salinity and temperature derivative tables allowed level to reverse the
  derivative sign, although inventory should change only its magnitude.

Finally, the old derivative ranges (`±5 m/s`, `±100 wt%/s`, `±100 °C/s`) were
too wide for this process and removed useful resolution around the operating
point.

## Changes

- fuzzy blocks still infer `dL/dt`, `dx/dt`, and `dT/dt`;
- state update blocks now integrate those fuzzy derivatives with the actual
  sample interval: `state[k+1] = state[k] + dt * derivative[k]`;
- continuous fuzzy blocks use centroid defuzzification;
- physical ranges are centered on the verified operating point and use
  piecewise scaling when the operating point is not the midpoint;
- inputs are clipped to the normalized universe so out-of-range disturbances
  activate shoulder sets instead of producing an empty aggregate;
- all returned time, state, vapor-flow, and brine-flow arrays now have equal
  length;
- state bounds prevent invalid thermodynamic calls during large transients.

## Baseline validation

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python more_accurate_model/fuzzy_model/fuzzy_problem.py
python more_accurate_model/fuzzy_model/validate_fuzzy_model.py
pytest -q
```

For the included 500-second baseline case, the corrected fuzzy model gives
approximately:

| Variable | Fuzzy model | ODE reference |
| --- | ---: | ---: |
| Level (m) | 0.1187 | 0.1197 |
| Salinity (wt%) | 5.7847 | 5.7385 |
| Temperature (°C) | 57.7057 | 57.2829 |
| Vapor flow (kg/s) | 10.6155 | 10.7509 |
| Brine flow (kg/s) | 58.9845 | 59.2223 |

The validation script also tests positive and negative step changes and writes
the comparison figure and final-value metrics under `validation/`.
