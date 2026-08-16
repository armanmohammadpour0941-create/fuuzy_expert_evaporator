# Fuzzy MED solver: step-response correction

## Root causes

The operating-point match hid three transient-model errors:

1. The level block normalized inlet flow over `60-80 kg/s` but outlet flow over
   `68-72 kg/s`. The same physical flow change therefore received very
   different linguistic weight.
2. The salinity path used `I_s,in - w_b*x` and then treated the result directly
   as a concentration derivative. That is a total salt-inventory balance; it
   omits the concentration effect of changing liquid inventory.
3. The old outlet-enthalpy fuzzy block used only vapor flow, brine flow and
   temperature. It could not represent all terms in the ODE temperature
   balance, and its narrow ranges clipped step inputs. Steam-flow steps could
   consequently produce the wrong temperature-derivative sign.

The original five-set membership family also left a normalized dead band around
zero. Balance errors could stop inside that dead band rather than converge to
the physical equilibrium.

## Implemented changes

- Level now fuzzifies the physical flow residual
  `w_f + w_bin - w_v - w_b` over `[-15, 15] kg/s` and maps it to
  `[-0.00170, 0.00170] m/s`.
- The salt residual is now
  `I_s,in - x*(w_f + w_bin - w_v)`, which is the numerator that drives
  concentration change.
- The temperature path uses an algebraic energy-demand index containing the
  mixture-enthalpy and inventory terms required by the temperature balance.
  The energy residual is still fuzzified before the temperature-derivative
  block.
- One-input balance blocks use a linear five-set partition and height
  defuzzification. This keeps fuzzification/linguistic rules while removing the
  artificial gain hump and zero dead band of clipped-area centroid inference.
- Salinity and temperature derivative blocks use an overlapping sensitive
  five-set profile near zero; general blocks retain the smoother original
  membership profile.
- The ODE-reference vapor-output function now uses the same steam latent-heat
  definition as `equation.py` and the fuzzy algebraic vapor block.
- Solver input shapes and finite values are validated explicitly.
- Validation now covers baseline plus positive and negative 20% steps in
  `w_s`, `w_f`, `w_bin`, and `t_f`.

## Validation result

For the included 1000-second cases, the worst post-step normalized trajectory
errors are:

| Variable | Worst NRMSE | Scenario |
| --- | ---: | --- |
| Level | 0.958% | -20% feed flow |
| Salinity | 0.121% | +20% steam flow |
| Temperature | 0.434% | -20% steam flow |
| Vapor flow | 0.119% | +20% steam flow |
| Brine flow | 0.757% | -20% feed flow |

Final-state errors in the tested cases are below `0.00033 m` for level,
`0.00019 wt%` for salinity, and `0.012 deg C` for temperature.

The tested range is the local operating envelope represented by the supplied
rules and ranges. Larger steps should be added to the validation matrix before
the fuzzy model is used outside this envelope.

## Run

From the repository root:

```bash
python -m pip install -r requirements.txt
python more_accurate_model/fuzzy_model/fuzzy_problem.py
python more_accurate_model/fuzzy_model/validate_fuzzy_model.py
pytest -q
```

Validation outputs are written to `validation/step_response_comparison.png` and
`validation/step_response_metrics.csv`.
