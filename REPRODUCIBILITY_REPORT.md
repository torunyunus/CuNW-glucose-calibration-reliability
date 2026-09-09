# Reproducibility validation report

The packaged repository was executed end-to-end in the supplied environment using:

```bash
python run_all.py
pytest -q
```

## End-to-end run

Status: **PASS**

Runtime in the validation environment: approximately 34 s.

Core reproduced values:

- detected change points: 111, 165, 213, 263, 319, 365, 411, 462, 514 s
- calibration reconstruction MAE: 0.5658 µA
- calibration reconstruction RMSE: 0.6444 µA
- median lag-1 plateau correlation: 0.6879
- approximate median AR(1) effective sample size: 3.883
- free-knot optimum: 595.30 µM
- profile-based transition-support region: 462.72–740.95 µM
- fixed-segmented low slope: 0.2365467 µA/µM
- fixed-segmented high slope: 0.0151518 µA/µM
- low/high slope ratio: 15.6118×
- wild-bootstrap slope-ratio interval: approximately 12.53–20.11×
- fixed-segmented forward LOCO RMSE: approximately 8.32 µA
- fixed-segmented all-level inverse LOCO RMSE: 367.37 µM
- fixed-segmented interior-only inverse LOCO RMSE: 262.93 µM
- Langmuir all-level inverse LOCO RMSE: 321.16 µM
- parameter-grid reconstruction RMSE range: 0.610–0.898 µA
- parameter-grid slope-ratio range: 15.26–15.79×
- jackknife slope-ratio range: 12.09–16.64×
- jackknife breakpoint range: 559.5–826.6 µM

Supporting electrochemical calculations also reproduce the manuscript values for scan-rate analysis, applied-potential drift/noise, interference perturbations, and EIS parameter ratios.

## Regression tests

Status: **PASS — 4/4 tests**

The tests freeze the main experimental-analysis results so later code changes can be checked for unintended numerical drift.

## Important open provenance issue

The approximately 36–37 s difference between the nominal dosing clock and the raw-trace event clock remains unresolved. The repository deliberately records this as an open provenance issue and does not assign a causal explanation.
